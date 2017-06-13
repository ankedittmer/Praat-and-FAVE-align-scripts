import os
from subprocess import call

class PraatRunner:

	def chop(self):

		call([self.praat, '--run', self.praat_chop_path])

	def getCoG(self):

		call([self.praat, '--run', self.praat_CoG_path])


	def __init__(self):

		self.praat = '/home/adittmer/Downloads/praat' #full path to the praat executable
		self.dir_path = os.getcwd()
		self.praat_chop_path = os.path.join(self.dir_path, 'chopper.txt')
		self.praat_CoG_path = os.path.join(self.dir_path, 'CoG.txt')

