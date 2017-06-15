import os
from subprocess import call

class PraatRunner:

	def chop(self):

		call([self._praat, '--run', self.praat_chopper_path])

	def getCoG(self):

		call([self._praat, '--run', self.praat_CoG_path])


	def __init__(self, praat):

		self._praat = praat
		self.dir_path = os.getcwd()
		self.praat_chopper_path = os.path.join(self.dir_path, 'chopper.txt')
		self.praat_CoG_path = os.path.join(self.dir_path, 'CoG.txt')
