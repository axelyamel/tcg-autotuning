from InputFile import *
import copy
import sys

class CodeGen(InputFile):

	def __init__(self,filename):

		InputFile.__init__(self,filename)

		defines = ''
		
		funcDec = 'void ' + self.FuncName + '('
		self.tempVar = {}


		print 'Generating code for: '+ self.FuncName
		self.loopIndices = []
		self.loopIndicesSize = []
		self.Defs = {}

		for defs2 in self.InputFile['define']:

			var = filter(None,re.split('=',defs2))
			defines += '#define ' + var[0] + ' ' + var[1] + '\n'
			self.Defs[var[0]] = var[1]

		for var in self.InputFile['variables']:

			var2 = filter(None,re.split(':',var))
			funcDec += 'double *' + var2[0] + ','
			self.tempVar[var2[0]] = var2[1]

		funcDec = funcDec[:-1] + ')\n{'

		body = ''
		Indices = []

		
		for ops in self.InputFile['operations']:


			newOp = ''
			ops2 = filter(None,re.split(':|\+=|-=|\*|\(|\)',ops))
			

			tempInd = filter(None,re.split('\(|\)|,',ops2[1]))
			indSize = filter(None,re.split('\(|\)|,',self.tempVar[ops2[0]]))

			tempInd2 = copy.deepcopy(tempInd)

		
			if self.InputFile['memory'] == 'column':
				tempInd2.reverse()


			newOp += ops2[0] 
			if self.InputFile['access'] == 'linearize':

				newOp += '[' 
				if self.InputFile['pattern'] == 'contiguous':

					acum = 1
					for index in tempInd:

						newOp += index
						if acum != len(indSize):
							for k in range(acum,len(indSize)):
								newOp += '*' + indSize[k]
						newOp += ' + '
						acum += 1

				else:

					closing = ''
					for i in range(len(tempInd)):

						newOp += tempInd[i]
						if i != len(tempInd)-1:
							newOp += ' + '+indSize[i]+ '*('
							closing += ')'

					newOp += closing + '  '

						
				newOp = newOp[:-2] + ']'


			else:
				acc = ops[1].replace('(','[')
				acc = acc.replace(',','][')
				acc = acc.replace(')', ']')

				newOp += acc

			sing = filter(None,re.split('(\+|\-)',ops))[1]
			
			newOp += ' = ' + newOp + ' ' + sing + ' ('

			acum = 2
			while(ops2[acum] not in self.tempVar):

				tempInd.append(ops2[acum])
				tempInd2.append(ops2[acum])
				indSize.append('')
				acum+=1

			for i in range(acum,len(ops2),2):

				ind2 = filter(None,re.split('\(|\)|,',ops2[i+1]))
				ind3 = filter(None,re.split('\(|\)|,',self.tempVar[ops2[i]]))

				newOp += ops2[i]

				newOp += '['
				if self.InputFile['access'] == 'multidimensional':
					acc = ops2[i+1].replace('(','')
					acc = acc.replace(',','][')
					acc = acc.replace(')', '')

					newOp += acc + ' * '
				

				acum2 = 1
				closing = '  '
				for j in range(len(ind2)):
					if ind2[j] not in tempInd:
						tempInd.append(ind2[j])
						tempInd2.append(ind2[j])
						indSize.append(ind3[j])
					if ind2[j] not in Indices:
						Indices.append(ind2[j])

					if self.InputFile['access'] == 'linearize':

						if self.InputFile['pattern'] == 'contiguous':
							newOp += ind2[j]
							for k in range(acum2,len(ind3)):
								newOp += '*' + ind3[k] 
							newOp += ' + '
							acum2 += 1
							closing = ''
					
						else:
							newOp += ind2[j]

							if j != len(ind3)-1:
								newOp += ' + ' +  ind3[j] + '*('
								closing = ')' + closing


					index = tempInd.index(ind2[j])
					if indSize[index] == '':
						indSize[index] = ind3[j]

				newOp += closing
				newOp = newOp[:-2] + '] * '

			newOp = newOp[:-3] +');'
			

			space = '  '
			closing = ''
			for i in range(len(tempInd2)):

				body += space + 'for (' + tempInd[i] + '=0; ' + tempInd[i] + '<' + indSize[i] + '; ' + tempInd[i] + '++){\n'

				closing = space + '}\n' + closing

				space += ' '
			
			body += '\n'+ space + newOp + '\n\n' + closing + '\n'
			self.loopIndices.append(tempInd2)
			self.loopIndicesSize.append(indSize)

		ind = '  int '
		for index in Indices:
			ind += index + ','

		ind += 'dummyLoop;\n'

		body = ind +'  for (dummyLoop=0; dummyLoop<1; dummyLoop++){\n\n' + body + '  } //end of dummy \n'

		self.funcDec = funcDec
		self.defines = defines
		
		self.body = body


	def generate_code(self,*arg):
		if len(arg) == 0:
			code = self.defines + '\n' + self.funcDec + '\n' + self.body + '}'
			
			
		else:
			annot = arg[0]
			code = self.funcDec + '\n' + annot + '\n' + self.body + '/*@ end @*/   // CHiLL\n\n/*@ end @*/   // PerfTuning\n\n}'
			
		
		return code




