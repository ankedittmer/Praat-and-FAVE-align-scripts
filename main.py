##
## This script takes in a data directory full of sound- and corresponding 
## TextGrid files (with word-transcriptions sectiond in breath groups), cuts
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


## Set up
editor = "gedit" # Type in your editor of choice in which you want to edit missing dictionary entries
praat = '/home/adittmer/Downloads/praat' # full path to your praat executable
data = '/data' # name of your data-directory. If it differs from 'data' you need to change your praat scripts also
dir_path = os.getcwd()
unknown_words = []


## Chop our sound and textgrid files into smaller pieces (breath groups)
praatrunner = PraatRunner(praat)	# start an instance of the praatrunner with the path to your praat-executable
praatrunner.chop()  # run a script in praat to chop the data


for root, dir_names, file_names in os.walk(dir_path + data):
 
	for file_name in file_names:
		if not '_' in file_name:
			os.remove('data/' + file_name)
		if file_name[-3:] == 'txt' and (not file_name[-11:] == 'unknown.txt') and ((file_name + 'unknown.txt') not in file_names):
			os.system("python FAAValign.py -c data/" + file_name + "unknown.txt " + "data/" + file_name)

for root, dir_names, file_names in os.walk(dir_path + '/data'):

	for file_name in file_names:
		os.stat(dir_path + "/data/" + file_name).st_size
		if file_name[-11:] == 'unknown.txt' and os.path.getsize(dir_path + "/data/" + file_name) > 0:
			with open(dir_path + "/data/" + file_name) as file:
				for line in file:
					newline = line.strip()
					unknown_words.append(newline)

			
	unknown_words.sort()
	
	with open(dir_path + '/data/unknown.txt', 'w') as file:
		for line in unknown_words:
			file.write(line + '\n')
	os.system(editor + ' ' + dir_path + '/data/unknown.txt') 

	for file_name in file_names:
		if file_name[-3:] == 'wav': #and os.path.getsize(dir_path + "/data/" + file_name[:-3] + "txtunknown.txt") == 0:
			os.system("python FAAValign.py -i data/unknown.txt data/" + file_name)


praatrunner.getCoG()