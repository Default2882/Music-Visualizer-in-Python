import numpy as np
from scipy.fftpack import fft
import pygame
from pydub import AudioSegment
from clint.textui.colored import red, green, magenta, black

print(magenta("\nWelcome to python music visualiser written in .... and  ... by Soumya Saurav\n"))

while(True):
	try:
		filname = input(green("Enter a file name: "))
		if filname[len(filname)-3:len(filname)] == "mp3":
			print(red("Mp3 file detected, converting to wav file, this may take some time \n"))
			sound = AudioSegment.from_mp3(filname)
			sound.export("converted.wav", format="wav")
			print(green("Paying song!!"))
			pygame.mixer.init()
			pygame.mixer.music.load("converted.wav")
			pygame.mixer.music.play()
		else:
			print(green("Paying song!!"))
			pygame.mixer.init()
			pygame.mixer.music.load(filname)
			pygame.mixer.music.play()
	except:
		print(red("Invalid Name, please try again or press ctrl+Z to exit."))


