from Transform import *
import datetime

class CodeGen:

	def __init__(self,transOps):

		self.transformOP = transOps
		self.transOP = self.transformOP.getTransOp()
		self.inFile = self.transformOP.getInputFile()
		self.Defines = self.inFile.getDefines()
		self.dVars = self.inFile.getVariables()
		self.funcName = self.inFile.getFuncName()
		self.access = self.inFile.getAccess()
		self.Index = self.transformOP.getLoopsIndeces()
		now = datetime.datetime.now()

		self.Stamp = '/*This code was generated using the Tensor-Contraction Autotuning tool,\ndeveloped by Axel Y. Rivera (University of Utah).\nCode Generated Date and hour: ' + now.strftime("%Y-%m-%d %H:%M") + '*/\n\n'
		self.code = self.Stamp
		self.func = ''
		self.body = ''
		
		
		for key,value in self.Defines.items():

			self.code = self.code + '#define ' + key + ' ' + str(value) + '\n'
		self.code = self.code + '\nvoid ' + self.funcName + '('
		for key,value in self.dVars.items():

			sizes = filter(None,re.split(',|\*',value['size']))

			for i in sizes:
				if i not in self.Defines:
					self.code = self.code + 'int ' + i + ', '

			if self.access == 'multidimension':
				varT = re.sub(',','][',value['size'])
				self.code = self.code + 'double ' + key + '[' + varT +'], '
			elif self.access == 'linearize':
				self.code = self.code + 'double *' + key + ', '

		self.code = self.code[:-2] + '){\n\n\tint '

		for i in self.Index:
			self.code = self.code + i + ', '
		self.code = self.code[:-2] + ';\n\n'

		for i in self.transOP:

			self.code = self.code + i['loopGen'] + i['operation'] +';' + i['close']

		self.code = self.code + '}'

		


		
	def printCode(self):
		print self.code

	def OutToFile(self,outfile):

		filename = outfile
		fileN = open(filename,'w')
		fileN.write(self.code)

		fileN.close()
		
	
