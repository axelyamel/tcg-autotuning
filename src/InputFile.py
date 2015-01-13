import re

class InputFile:

	def __init__(self,filename):

		tensorFile = open(filename)

		self.FileName = filename
		self.FileName = self.FileName[:-3] + 'c'

		self.InputFile = {}

		self.InputFile['memory'] = 'row'
		self.InputFile['pattern'] = 'contiguous'
		self.InputFile['access'] = 'multidimensional'

		self.fileInput = filename

		self.FuncName = tensorFile.readline()
		self.FuncName = self.FuncName[:-1]
		
		print 'Reading input file: '+ filename
		ClassInput = ''
		tempInfo = []
		for line in tensorFile:

			lineInfo = filter(None, re.split('(\t)| |\n',line))


			if len(lineInfo) > 0:
				if lineInfo[0] != '\t':
	
					if ClassInput != '':
						self.InputFile[ClassInput] = tempInfo


					ClassInput = lineInfo[0][:-1]
					tempInfo = []

					if len(lineInfo) > 1:
						self.InputFile[ClassInput] = lineInfo[1]
						ClassInput = ''

					
				else:
					lineInput = ''
					for i in range(1,len(lineInfo)):
						lineInput += lineInfo[i]

					tempInfo.append(lineInput)


		self.InputFile[ClassInput] = tempInfo
		tempInfo = []



	def getFileName(self):
		return self.FileName

		



