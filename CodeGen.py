from Transform import *
import datetime

class CodeGen:

	def __init__(self,transOps,annot):

		self.Annotation = annot
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
		
		
		#for key,value in self.Defines.items():

		#	self.code = self.code + '#define ' + key + ' ' + str(value) + '\n'
		
		self.code = self.code + '\nvoid ' + self.funcName + '('



		ins = ''
		outs = ''

		for key,value in self.dVars.items():

			sizes = filter(None,re.split(',|\*',value['size']))

			tDec = ''
			for i in sizes:
				if i not in self.Defines:
					tDec = tDec + 'int ' + i + ', '

			if self.access == 'multidimension':
				varT = re.sub(',','][',value['size'])
				tDec = tDec + 'double ' + key + '[' + varT +'], '
			elif self.access == 'linearize':
				tDec = tDec + 'double *' + key + ', '

			if value['io'] == 'input':
				ins = ins + tDec
			elif value['io'] == 'output':
				outs = outs + tDec

		self.code = self.code + outs + ins

		self.code = self.code[:-2] + '){\n\n'


		self.code = self.code + self.Annotation


		self.code = self.code + '\n\n\tint '



		for i in self.Index:
			self.code = self.code + i + ', '
		self.code = self.code[:-2] + ';\n\n'

		self.body = ''
		acum = 0
		for i in self.transOP:

			self.body = self.body + i['highLoop'] + i['loopGen'] + i['operation'] +';' + i['close']
			if i['highLoop'] != '':
				acum = 1
	
		if acum == 1:
			self.body = self.body + '\t}\n'


		
		self.CloseA = ''
		if self.Annotation != '':

			self.CloseA = self.CloseA + '/*@ end @*/   // CHiLL\n\n/*@ end @*/   // PerfTuning'



		self.code = self.code + self.body + self.CloseA + '\n}'
		
	def printCode(self):
		print self.code

	def OutToFile(self,outfile):

		filename = outfile
		fileN = open(filename,'w')
		fileN.write(self.code)

		fileN.close()
		
	
