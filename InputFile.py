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
		self.inputs = {}
		self.outputs = {}
		self.defines = {}
		self.operation = []
		defs = 0
		inps = 0
		outs = 0
		ops = 0
		ioputs = 0

		mem=0
		accel = 0
		acc = 0
		patt =0

		for line in self.filew:
			splitL = re.split('\t| |: | \n|:|\n',line)
			if splitL[0] == 'access':
				defs = 0
				inps = 0
				outs = 0
				ops = 0
				acc = 1
				ioputs = 0
				self.access = splitL[1]
			if splitL[0] == 'pattern':
				defs = 0
				inps = 0
				outs = 0
				ops = 0
				patt =1
				ioputs=0
				self.pattern = splitL[1]

			if splitL[0] == 'accelerator':
				defs = 0
				inps = 0
				outs = 0
				ops = 0
				accel = 0
				ioputs=0
				self.accelerator = splitL[1]
			if splitL[0] == 'memory':
				defs = 0
				inps = 0
				outs = 0
				ops = 0
				mem = 1
				ioputs=0
				self.memory = splitL[1]

			if splitL[0] == 'defines':
				defs = 1
				inps = 0
				outs = 0
				ops = 0
				ioputs=0

			if splitL[0] == 'input':
				defs = 0
				inps = 1
				outs = 0
				ops = 0
				ioputs=0


			if splitL[0] == 'output':
				defs = 0
				inps = 0
				outs = 1
				ops = 0
				ioputs=0


			if splitL[0] == 'io':
				defs = 0
				inps = 0
				outs = 0
				ops = 0
				ioputs=1


			if splitL[0] == 'operation':
				defs = 0
				inps = 0
				outs = 0
				ops = 1
				ioputs=0


			if defs == 1 and splitL[0] == '' and splitL[1] != '':
				self.defines[splitL[1]] = splitL[3]

			if inps == 1 and splitL[0] == '' and splitL[1] != '':
				split2 = re.split('order|\(|\)',splitL[2])
				orderN = 0
				if split2[1].isdigit() == True:
					orderN = int(split2[1])
				else:
					counter = split2[1].count(',')
					orderN = counter+1
				self.inputs[splitL[1]] = {}
				self.inputs[splitL[1]]['order'] = orderN
				sizeN = ''
				inVar = splitL[1]
				if len(split2) < 3:
					for i in range(orderN):
						sizeN = sizeN + inVar+'D'+str(i+1)+','
					sizeN=sizeN[:-1]
				else:
					sizeN = split2[1]
				
	
				self.inputs[splitL[1]]['size'] = sizeN
		
			if outs == 1 and splitL[0] == '' and splitL[1] != '':
				split2 = re.split('order|\(|\)',splitL[2])
				orderN = 0
				if split2[1].isdigit() == True:
					orderN = int(split2[1])
				else:
					counter = split2[1].count(',')
					orderN = counter+1

				self.outputs[splitL[1]] = {}
				self.outputs[splitL[1]]['order'] = orderN
				sizeN = ''
				outVar = splitL[1]
				if len(split2) < 3:
					for i in range(orderN):
						sizeN = sizeN + outVar+'D'+str(i+1)+','
					sizeN=sizeN[:-1]
				else:
					sizeN = split2[1]

				self.outputs[splitL[1]]['size'] = sizeN


			if ioputs == 1 and splitL[0] == '' and splitL[1] != '':
				split2 = re.split('order|\(|\)',splitL[2])
				orderN = 0
				if split2[1].isdigit() == True:
					orderN = int(split2[1])
				else:
					counter = split2[1].count(',')
					orderN = counter+1

				self.inputs[splitL[1]] = {}
				self.inputs[splitL[1]]['order'] = orderN
				sizeN = ''
				inVar = splitL[1]
				if len(split2) < 3:
					for i in range(orderN):
						sizeN = sizeN + inVar+'D'+str(i+1)+','
					sizeN=sizeN[:-1]
				else:
					sizeN = split2[1]
				
	
				self.inputs[splitL[1]]['size'] = sizeN
		
				self.outputs[splitL[1]] = {}
				self.outputs[splitL[1]]['order'] = orderN

				self.outputs[splitL[1]]['size'] = sizeN

	

			if ops == 1 and splitL[0] == '' and splitL[1] != '':
				split3 = re.split('\t|\n',line)

				split4 = re.split('(=)|\+|\*|\-|\/| |',split3[1])

				acum=0

				var = split4[0]
				tempOp = {}
				tempOp['operation']=split3[1]
				tempOp['vars'] = {}
	
				while var != '=':

					if var is not None and var is not '':
						s5 = re.split('\(|,|\)|:',var)
						v1 = s5[0]

						if v1 not in self.outputs:
							print '\033[91m'+ 'Error: Variable ' + v1 + ' not declared in output section' + '\033[0m'
							sys.exit()

						s6 = self.outputs[v1]['size']
						loopsV = {}
						s7 = re.split(',',s6)
						for j in range(2,len(s5)-1):
							if j is not '':
								loopsV[s5[j]] = s7[j-2]

						tempOp['vars'][v1] = loopsV
					acum = acum+1
					var = split4[acum]

				
				for vi in range(acum+1,len(split4)):

					var = split4[vi]
					if var is not None and var is not '':
						s5 = re.split('\(|,|\)|:',var)
						v1 = s5[0]
						if v1 not in self.inputs:
							print '\033[91m' + 'Error: Variable ' + v1 + ' not declared in input section' + '\033[0m'
							sys.exit()


						s6 = self.inputs[v1]['size']
						loopsV = {}
						s7 = re.split(',',s6)
						
						for j in range(2,len(s5)-1):
							if j is not '':
								loopsV[s5[j]] = s7[j-2]

						tempOp['vars'][v1] = loopsV

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

		for op in self.operation:
			split4 = re.split('=|\+|\*|\-|\/|',op['operation'])
			split4.remove('')
			counter1 = (split4[1].count(','))+1
			var1 = re.split(':',split4[1])
			var2 = re.split(':',split4[2])
			ovar = re.split(':',split4[0])
			counter2 = (split4[2].count(','))+1
			errVar = 0		
			for it in range(len(var1)):
				var1[it] = re.sub(' ','',var1[it])
				var2[it] = re.sub(' ','',var2[it])
				ovar[it] = re.sub(' ','',ovar[it])

		
			if counter1 != self.inputs[var1[0]]['order']:
				self.access = 'linearize'

	
			if counter2 != self.inputs[var2[0]]['order']:
				self.access = 'linearize'

	
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
		print "\t------------------------------------------"
		print "\tTensor\t|\tOrder\t|\tSize\t"
		print "\t------------------------------------------"
		
		for key,value in self.inputs.items():
			print "\t",key,"\t|\t",value['order'],"\t|\t",value['size']

		print "\nOutput Data:"
		print "\t------------------------------------------"
		print "\tTensor\t|\tOrder\t|\tSize\t"
		print "\t------------------------------------------"
		
		for key,value in self.outputs.items():
			print "\t",key,"\t|\t",value['order'],"\t|\t",value['size']

		print "\nOperations:"
		for op in self.operation:
			print "\t",op['operation']," "


	def getOperations(self):
		return self.operation

	def getDefines(self):
		return self.defines

	def getMemory(self):
		return self.memory

	def getAccess(self):
		return self.access

	def getInputs(self):
		return self.inputs

	def getOutputs(self):
		return self.outputs

	def getFuncName(self):
		return self.funcName

	def getFileOut(self):
		return self.fileOut

	def getPattern(self):
		return self.pattern


