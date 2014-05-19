import re
import sys

class InputFile:

	def __init__(self, fname):

		self.filew = open(fname,'r')
		self.filename = fname

		
		self.fileOut = fname[:-1]
		self.fileOut = self.fileOut+'c'

		self.funcName = self.filew.readline()
		self.funcName = re.sub('\n','',self.funcName)
		self.access = ''
		self.accelerator = ''
		self.memory = ''
		self.pattern = ''
		self.variables = {}
		self.defines = {}
		self.operation = []
		defs = 0
		ops = 0
		varsIO = 0

		mem=0
		accel = 0
		acc = 0
		patt =0

		for line in self.filew:
			splitL = re.split('\t| |: | \n|:|\n|=',line)
			splitL = filter(None, splitL)
			start = 1

			if len(splitL) > 0:
				if splitL[0] == 'access':
					defs = 0
					varsIO=0
					ops = 0
					acc = 1
					self.access = splitL[1]
					start = 0

				if splitL[0] == 'pattern':
					defs = 0
					ops = 0
					patt =1
					varsIO=0
					self.pattern = splitL[1]
					start = 0

				if splitL[0] == 'accelerator':
					defs = 0
					varsIO = 0
					ops = 0
					accel = 0
					self.accelerator = splitL[1]
					start = 0

				if splitL[0] == 'memory':
					defs = 0
					varsIO = 0
					ops = 0
					mem = 1
					self.memory = splitL[1]
					start = 0

				if splitL[0] == 'define':
					defs = 1
					ops = 0
					varsIO=0
					start = 0

				if splitL[0] == 'variables':
					defs = 0
					varsIO = 1
					ops = 0
					start = 0

				if splitL[0] == 'operations':
					defs = 0
					ops = 1
					varsIO=0
					start = 0

				if defs == 1 and start ==1:
					self.defines[splitL[0]] = splitL[1]

				if varsIO == 1 and start==1:
					split2 = re.split('order|\(|\)',splitL[1])
					split2 = filter(None,split2)
					orderN = 0
					sizeN = ''

					if split2[0].isdigit() == True:
						orderN = int(split2[0])
						for i in range(orderN):
							sizeN = sizeN + splitL[0]+'D'+str(i+1)+','
						sizeN=sizeN[:-1]

					else:
						counter = split2[0].count(',')
						orderN = counter+1
						sizeN = split2[0]

					self.variables[splitL[0]] = {}
					self.variables[splitL[0]]['order'] = orderN
					
		
					self.variables[splitL[0]]['size'] = sizeN
					self.variables[splitL[0]]['io'] = 'input'

		

				if ops == 1 and start==1:

					split4 = re.split('(=|\+|\*|\-|\/)| |\t|\n',line)
					split4 = filter(None,split4)					
					acum=0


					assigment = split4[1] + split4[2]
					opI = split4[4]

					
					if not (assigment == '+=' or assigment == '-=' or assigment == '=-' or assigment == '=+'):
						print '\033[91m'+ 'Error: Operation ' + line + ' is not a Tensor-Contraction.' + '\033[0m'
						sys.exit()


					s5 = filter(None,re.split('\(|,|\)|:',split4[0]))
					s6 = filter(None,re.split('\(|,|\)|:',split4[3]))
					s7 = filter(None,re.split('\(|,|\)|:',split4[5]))


					varsT = [s5,s6,s7]

					for i in range(3):
						if varsT[i][0] not in self.variables:

							print '\033[91m'+ 'Error: Variable ' + varsT[i][0]+ ' not declared in variables section' + '\033[0m'
							sys.exit()

					var = split4[0]

					outputVar = filter(None,re.split(':|\(|,|\)',split4[0]))
					
					self.variables[outputVar[0]]['io'] = 'output'

					tempOp = {}
					tempOp['output'] = split4[0]
					tempOp['input1'] = split4[3]
					tempOp['input2'] = split4[5]
					tempOp['operation']=opI
					tempOp['assignment'] = assigment
		

					self.operation.append(tempOp)

		
		self.filew.close()

		if mem == 0:
			self.memory = 'row'
		if patt == 0:
			self.pattern = 'contigous'
		if accel == 0:
			self.accelerator = 'GPU'
		if acc == 0:
			self.access = 'multidimension' 
	
	def printInfo(self):
		print "Filename: ",self.filename
		print "Name of fucntion: ",self.funcName
		print "Memory access: ",self.memory
		print "Array access: ",self.access
		print "Accelerator: ",self.accelerator
		print "Pattern: ",self.pattern
		print "\nDefined Values: "

		for key, value in self.defines.items():
			print "\t",key," = ",value

		print "\nInput Data:"
		print "\t-------------------------------------------------------------"
		print "\tTensor\t|\tMode\t|\tOrder\t|\tSize\t"
		print "\t-------------------------------------------------------------"
		
		for key,value in self.variables.items():
			print "\t",key,"\t|\t",value['io'],"\t|\t",value['order'],"\t|\t",value['size']

		print "\nOperations:"
		for op in self.operation:
			print "\t",op['output'],op['assignment'],op['input1'],op['operation'],op['input2']


	def getOperations(self):
		return self.operation

	def getDefines(self):
		return self.defines

	def getMemory(self):
		return self.memory

	def getAccess(self):
		return self.access

	def getVariables(self):
		return self.variables

	def getFuncName(self):
		return self.funcName

	def getFileOut(self):
		return self.fileOut

	def getPattern(self):
		return self.pattern


