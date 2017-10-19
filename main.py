##
## This script takes in a data directory full of sound- and corresponding 
## TextGrid files (with word-transcriptions sectioned in breath groups), cuts
## the data in smaller pieces, so that the FAVE-aligner can align the data
## properly and gives out a CSV-file (with header) in which all occurances of
## /s/ and /sh/ are listed with their centre of gravity (after a preemphasis
## of 750 HZ).
##
## Written by Anke Dittmer 2017
## 

import os
from praatrunner import PraatRunner
import subprocess
from tempfile import mkstemp
from shutil import move
import re


## Set up
editor = "gedit" # Type in your editor of choice in which you want to edit missing dictionary entries
praat = '/home/ankedittmer/Downloads/praat' # full path to your praat executable
data = '/data' # name of your data-directory. If it differs from 'data' you need to change CoG.txt and chopper.txt also
dir_path = os.getcwd()
unknown_words = [] # in here should all out-of-dictionary-words be saved


# A function to check the file with out of dictionary words, it it matches the pattern requirements for FAVE
def checkUnknownFile(path):
	with open(path) as file:
		for line in file: # go through the out-of-dictionary-words written in this file
			newline = line.strip()
			# does the line match the pattern requirement?
			if re.match("[-A-Z\']+\t([A-Z]+[0-2]? )*[A-Z]+[0-2]?(, ([A-Z]+[0-2]? )*[A-Z]+[0-2]?)*", newline):
				correct = True
			else:
				return False
		return correct


## Chop our sound and textgrid files into smaller pieces (breath groups)
praatrunner = PraatRunner(praat)	# start an instance of the praatrunner with the path to your praat-executable
praatrunner.chop()  # run a script in praat to chop the data


# Check for out-of-dictionary-words in the transcribtions
for root, dir_names, file_names in os.walk(dir_path + data): # go through all files in the data directory
	print(file_names) 
	for file_name in file_names: # in the data directory are the original files as well as the chopped pieces, so:
		if not '_' in file_name: # delete the original data, aligning those wouldn't work they are to long
			os.remove('data/' + file_name)
		# take all text files that are not already the outcome of out-of-dictionary-checks or were already checked
		if file_name[-3:] == 'txt' and (not file_name[-11:] == 'unknown.txt') and ((file_name + 'unknown.txt') not in file_names): 
			# and check them for out-of-dictionary-words with a Fave-align command. Write the missing words in a file called like the
			# one that is checked but with an unknown.txt added 
			os.system("python FAAValign.py -c data/" + file_name + "unknown.txt " + "data/" + file_name)

# Write all unknown words in one file and open said file so that unknown words can be transcribed
for root, dir_names, file_names in os.walk(dir_path + '/data'): # go through all files in the data directory
	print(file_names)
	for file_name in file_names: # for all files in there
		# if the file is a file with out-of-dictionary words and is not empty
		if file_name[-11:] == 'unknown.txt' and os.path.getsize(dir_path + "/data/" + file_name) > 0:
			with open(dir_path + "/data/" + file_name) as file:
				for line in file: # go through the out-of-dictionary-words written in this file
					newline = line.strip()
					unknown_words.append(newline) # and save them in a python list

			
	unknown_words.sort() # sort all out-of-dictionary-words alphabetically
	
	# write all out-of-dictionary-words in a file called unknown.txt
	with open(dir_path + '/data/unknown.txt', 'w') as file:
		for line in unknown_words:
			file.write(line + '\n')
	# open the file with the out-of-dictionary-words in an editor and wait till it is closed (and the words are hopefully transcribed by hand)
	os.system(editor + ' ' + dir_path + '/data/unknown.txt')

	# check if the file with out of dictionary words and hand written transcriptions matches the requirements of FAVE, otherwise open it again
	# so that it can be changed
	check = False
	if os.path.getsize(dir_path + '/data/unknown.txt') > 0: # only check if the file is not empty
		while(check == False):

			if not checkUnknownFile(dir_path + '/data/unknown.txt'): # check if file matches the pattern requirements
				print("Please check again your transcription, leave no empty lines and be sure to seperate word and transcription with one tab")
				os.system(editor + ' ' + dir_path + '/data/unknown.txt') # open the file again
			else:
				check = True

	# align all wav files with their transcriptions and use the now transcribed out-of-dictionary-words
	for file_name in file_names:
		if file_name[-3:] == 'wav': # if the file is a sound file do the aligning, if the textGrid file is named the same as the 
									# corresponding wav, Fave-align finds it itself 
			os.system("python FAAValign.py -i data/unknown.txt data/" + file_name)

# Run the actual centre of gravity script
praatrunner.getCoG() # run a script in praat to get the centre of gravity of s / sh sounds and informations about their surroundings


