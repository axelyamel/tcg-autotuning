from Transform import *

class CodeGen:

	def __init__(self,transOps):

		self.TransOp = transOps

		self.inputF = self.TransOp.getInputFile()

		self.defines = self.inputF.getDefines()

		self.inputs = self.inputF.getInputs()
		self.outputs = self.inputF.getOutputs()
		self.funcName = self.inputF.getFuncName()
		self.access = self.inputF.getAccess()
		self.loops = self.TransOp.getLoopsIndeces()
		self.Ops = self.TransOp.getTransOp()

		defs = ''

		for key,value in self.defines.items():

			defs = defs + '#define '+key+' '+value+'\n'


		func = '\nvoid '+self.funcName+'('

		for key,value in self.inputs.items():
			addVar = ''
			splitS = re.split(',',value['size'])

			for vi in splitS:
				if vi.isdigit() == False:
					defined = 0
					vi2 = re.split('(\*)',vi)
					if len(vi2) > 2:
						if vi2[1] == '*':
							defined = 1
					for key2,value2 in self.defines.items():
						if vi == key2:
							defined = 1
							break
					if defined == 0:
						addVar = addVar + 'int '+vi+','

			if self.access == 'linearize':
				addVar = addVar + 'double *'+key+','
			elif self.access == 'multidimension':
				addVar = addVar + 'double '+key+'['
				sp = re.sub(',','][',value['size'])
				addVar = addVar+sp+'],'
			func = func + addVar

		for key,value in self.outputs.items():
			addVar = ''
			splitS = re.split(',',value['size'])

			for vi in splitS:
				if vi.isdigit() == False:
					defined = 0
					for key2,value2 in self.defines.items():
						if vi == key2:
							defined = 1
							break
					if defined == 0:
						addVar = addVar + 'int '+vi+','

			if self.access == 'linearize':
				addVar = addVar + 'double *'+key+','
			elif self.access == 'multidimension':
				addVar = addVar + 'double '+key+'['
				sp = re.sub(',','][',value['size'])
				addVar = addVar+sp+'],'
			func = func + addVar

		func = func[:-1]
		func = func + '){\n\n'
	
		body = ''

		for i in self.loops:

			body = body + '\tint ' + i + ';\n'

		body = body + '\n'

		for j in self.Ops:
			body = body + j + '\n'
		
		body = body + '}'
		
		self.code = defs + func + body

		
	def printCode(self):
		print self.code

	def OutToFile(self,outfile):

		filename = outfile
		fileN = open(filename,'w')
		fileN.write(self.code)

		fileN.close()
		
	
