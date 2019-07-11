import numpy as np
from scipy.fftpack import fft
import scipy
import pygame
from pydub import AudioSegment
from clint.textui.colored import red, green, magenta, black
from scipy.io import wavfile as wav
import scipy.signal
import time
#The music is visualised by converting the audio file from the frequency domain to the time domain using
#fast fourier transformation (FFT)
#refer to the article mentioned below for more information.
#https://dahvisualize.wordpress.com/2011/11/29/visualising-audio-in-the-time-and-frequency-domain/

print('''
    _______________________________
   | \___===____________________()_\
   | |                              |
   | |   _________________________  |
   | |  |                        |  |
   | |  |                        |  |
   | |  |                        |  |
   | |  |                        |  |
   | |  |                        |  |
   | |  |                        |  |
   | |  |                        |  |
   | |  |                        |  |
   | |  |                        |  |
   | |  |                        |  |
   | |  |________________________|  |
   | |                              |
   | |                              |
   | |              @@@@            |
   | |           @@@Menu@@@         |
   | |          @@@@@@@@@@@@        |
   | |         @<<@@@()@@@>>@       |
   | |          @@@@@@@@@@@@        |
   | |           @@@ ||>@@@         |
   | |              @@@@            |
   | |                              |
   | |                              |
   | |                              |
   | |                              |
    \|______________________________|

------------------------------------------------
Thank you for visiting https://asciiart.website/
This ASCII pic can be found at
https://asciiart.website/index.php?art=objects/audio%20equipment

    ''')

print(black("\n--------------------------------------------------------------------------"))
print(magenta("Welcome to python music visualiser written by Soumya Saurav"))
print(black("--------------------------------------------------------------------------\n"))
while(True):
	try:
		filname = input(green("Enter a file name: "))
		if filname[len(filname)-3:len(filname)] == "mp3":
			print(red("Mp3 file detected, converting to wav file, this may take some time \n"))
			sound = AudioSegment.from_mp3(filname)
			sound.export("converted.wav", format="wav")
			print(green("Loading the audio file...."))
			pygame.mixer.init()
			pygame.mixer.music.load("converted.wav")
			rate, data = wav.read('converted.wav')
			#pygame.mixer.music.play()
			break
		else:
			print(green("Loading the audio file...."))
			pygame.mixer.init()
			pygame.mixer.music.load(filname)
			#pygame.mixer.music.play()
			rate, data = wav.read(filname)
			break
	except:
		print(red("Invalid Name, please try again or press ctrl+Z to exit."))

percentage_displayed_f = 0.7                              
max_height_percentile = 99.8
fftlength = 2048
entertainment = False

print(green("Stereo to Mono Conversion"))
music = scipy.mean(data, axis=1)

print(green('Doing Fourier Transform'))
f, t, Sxx = scipy.signal.spectrogram(music, rate,nperseg=fftlength)                                          
no_of_displayed_f = int(len(f)*percentage_displayed_f+0.5)
Sxx = Sxx[:no_of_displayed_f-2].transpose()   
f = f[:no_of_displayed_f-2]

print(green("Playing song!!!!"))

#setting up screen
pygame.init()
screen = pygame.display.set_mode((1000, 1000))                                                    
rect_scale_factor = 1000/scipy.percentile(Sxx, max_height_percentile)
done = False
dt= t[1] - t[0]

#Title of the song on screen
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 15)
title = myfont.render(filname, False, (0, 255, 255))


#Initialising colour array for rectangles
colours = []
colour_f = 0.05     
for i in range(no_of_displayed_f):
    green   = scipy.sin(colour_f*i + 0) * 127 + 128
    blue = scipy.sin(colour_f*i + 2) * 127 + 128
    red  = scipy.sin(colour_f*i + 4) * 127 + 128
    colours.append((red, green, blue))
 
start_time = time.time()
#Precalulations to make animation smoother
Sxx_len = len(Sxx)
rect_width = 1000/no_of_displayed_f
done = False

pygame.mixer.music.play()

#Animation Loop
while not done:
    try:
        cur_time = time.time() - start_time

        timer = myfont.render(str(int(cur_time))+ "s", False, (0, 255, 255))                            
        screen.blit(timer,(10,1000 - 60))                                                               
        screen.blit(title, (10, 1000 -30))                                                             
        
        main_time_index = int(cur_time//dt)

        for index, frequency in enumerate(Sxx[(main_time_index)]):
            proportion_of_tleft = main_time_index - (main_time_index)
            height = max(proportion_of_tleft*frequency + (1- proportion_of_tleft)*Sxx[(main_time_index)+1][index], 2/rect_scale_factor)
            #Draws rectangles where height combines 2 nearest time bins by proportion for each frequency (height of 2px if no amplitude)
            if entertainment:
                multiplication_factor = 1 if index%2 else -1
                pygame.draw.rect(screen, colours[(index*multiplication_factor)%len(colours)], pygame.Rect((screen_w/2+multiplication_factor*0.5*(index+1)*screen_w/no_of_displayed_f), 20, screen_w/no_of_displayed_f, height*rect_scale_factor))
            else:
                pygame.draw.rect(screen, colours[index], pygame.Rect((index+1)*rect_width, 20, rect_width, height*rect_scale_factor))

        pygame.display.flip()
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.mixer.music.stop()
                    break

    except:
        pygame.display.quit()
        pygame.mixer.music.stop()
        break
        
