import os
from praatrunner import PraatRunner
import subprocess
from tempfile import mkstemp
from shutil import move

editor = "gedit"
dir_path = os.getcwd()
unknown_words = []


praatrunner = PraatRunner()
praatrunner.chop()

# Run the Prosodylab aligner, go through all data in the folder data and create 
# aligned TextGrid files for every pair of samenamed .wav and .lab files


# Ohne einzelne Ordner
for root, dir_names, file_names in os.walk(dir_path + '/data'):
 
	for file_name in file_names:
		if file_name.split('.')[0][-1] == 'g':
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