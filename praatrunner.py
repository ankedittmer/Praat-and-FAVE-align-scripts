##
## This class can run praat to either chop data or run a script to get 
## the centre of gravities of s / sh sounds, given the path to the praat executable
##
## Written by Anke Dittmer 2017
##

import os
from subprocess import call

class PraatRunner:

	# run the script to chop data in praat
	def chop(self):

		call([self._praat, '--run', self.praat_chopper_path])

	# run the script to get the centre of gravities in praat
	def getCoG(self):

		call([self._praat, '--run', self.praat_CoG_path])

	def __init__(self, praat):

		self._praat = praat # this is the path to the praat executable
		self.dir_path = os.getcwd()
		self.praat_chopper_path = os.path.join(self.dir_path, 'chopper.txt') # path to the chopper praat script
		self.praat_CoG_path = os.path.join(self.dir_path, 'CoG.txt') # path to the CoG praat script
