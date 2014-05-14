from InputFile import *

class Transform:

	def __init__(self,inFile):
		self.inputF = inFile

		
		self.operations = self.inputF.getOperations()
		self.defines = self.inputF.getDefines()
		self.memory = self.inputF.getMemory()
		self.access = self.inputF.getAccess()
		self.inputs = self.inputF.getInputs()
		self.outputs = self.inputF.getOutputs()

		self.defVars = []

		self.transOp = []
		self.loopsInd = []
		self.pattern = self.inputF.getPattern()


		for key, value in self.defines.items():
			self.defVars.append(key)
		
		for op in self.operations:
			newOp = ''
			loops = []
			psuInfo = []
			reduct = []
			redSplit = []
			loops2 = []

			opI = op['operation']
			splitL = re.split(' |=|\+|\-|\*|\/',opI)

			for i in splitL:
				if i != '':
					psuInfo.append(i)

			for i in psuInfo:
				splitI = re.split(':\(|,|\)',i)
				redSplit.append(splitI)
				for j in range(len(splitI)):
					if j>0 and splitI[j] != '':

						indx = []
						if not splitI[j] in loops:
							indx.append(splitI[j])
							indx.append(op['vars'][splitI[0]][splitI[j]])
							loops.append(splitI[j])
							loops2.append(indx)
						if not splitI[j] in self.loopsInd:
							self.loopsInd.append(splitI[j])


			acum = 1;
			inter = []

			outR = redSplit[0]



			inR2 = []
				
			for i in range(1,len(redSplit)):
				inR = list(set(outR) & set(redSplit[i]))
				for j in inR:
					if not j in inR2:
						inR2.append(j)
				



			for i in inR2:
				for j in range(len(redSplit)):
					if i in redSplit[j]:
						redSplit[j].remove(i)
				

			for i in range(len(redSplit)):
				if len(redSplit[i]) > 1:
					for j in range(1,len(redSplit[i])):
						if not redSplit[i][j] in inter:
							inter.append(redSplit[i][j])
						if redSplit[i][j] in loops:
							loops.remove(redSplit[i][j])
			
			if self.memory == 'column':
				loops.reverse()



			acumS = 1
			for i in loops:
				temp = ''
				for j in range(acumS):
					newOp = newOp + '\t'
				for k in loops2:
					if k[0] == i:
						temp = k[1]
				newOp = newOp + 'for('+i + ' = 0; '+i+' < '+temp+'; '+i+'++){\n'
				acumS = acumS+1

			for i in inter:
				temp=''
				for k in loops2:
					if k[0] == i:
						temp = k[1]

				for j in range(acumS):
					newOp = newOp + '\t'
				newOp = newOp + 'for('+i + ' = 0; '+i+' < '+temp+'; '+i+'++){\n'
				acumS = acumS+1

			if self.access == 'multidimension':
				op2 = re.sub(':\(','[',op['operation'])
				op2 = re.sub(',','][',op2)
				op2 = re.sub('\)',']',op2)

			elif self.access == 'linearize':
				cont = []
				op3 = ''
				op2 = re.sub(':\(','[',op['operation'])
				
				split3 = re.split('(\+|=| |\*|\-|\/)',op2)
				for it in range(len(split3)):
					var = split3[it]
					ver = 0
					if var != '' and var != ' ' and var != '=' and var != '(' and var != '+' and var != '-' and var != '*' and var != '/':
						counter = var.count(',')
	
						s5 = re.split('(\(|\[|\]|\)|,)',var)
						if s5[0] in self.outputs:
	
							s6 = re.split(',',self.outputs[s5[0]]['size'])
							ver = 1
	
							if self.pattern == 'contigous':
								acum3 = 1
								for i in range(2,len(s5)-2):
									if s5[i] != ',':
										tempP = s5[i]
										for j in range(acum3,len(s6)):
											tempP = tempP + '*'+s6[j]
										acum3 = acum3+1
										s5[i] = tempP
										
							elif self.pattern == 'strided':
								acum3 = 0
								counter = 0
								for i in range(2,len(s5)-3):
									if s5[i] == ',':
										counter = counter+1
									if s5[i] != ',':
										tempP = s5[i]
										
										tempP = tempP + '+'+s6[acum3]
										acum3 = acum3+1
										s5[i] = tempP
								for i in range(counter-1):
									s5.append(')')
									
						if s5[0] in self.inputs and ver == 0:
	
							s6 = re.split(',',self.inputs[s5[0]]['size'])
							if self.pattern == 'contigous':
								acum3 = 1
								for i in range(2,len(s5)-2):
									if s5[i] != ',':
										tempP = s5[i]
										for j in range(acum3,len(s6)):
											tempP = tempP + '*'+s6[j]
										acum3 = acum3+1
										s5[i] = tempP

							elif self.pattern == 'strided':
								acum3 = 0
								counter = 0
								for i in range(2,len(s5)-3):
									if s5[i] == ',':
										counter = counter+1
									if s5[i] != ',':
										tempP = s5[i]
										
										tempP = tempP + '+'+s6[acum3]
										acum3 = acum3+1
										s5[i] = tempP
								for i in range(counter-1):
									s5.append(')')
							


						tempT = ''
						for i in s5:
							tempT = tempT + i
						if self.pattern == 'contigous':
							tempT = tempT[:-1]
						split3[it] = tempT + ']'
						
					op3 = op3 + split3[it]

				if self.pattern == 'contigous':
					op2 = re.sub(',',' + ',op3)
					

				elif self.pattern == 'strided':

					op2 = re.sub(',',' *(',op3)
					


			for j in range(acumS):
				newOp = newOp + '\t'

			newOp = newOp + op2 + ';\n'

			acumS = acumS-1

			for i in loops:
				for j in range(acumS):
					newOp = newOp + '\t'
				newOp = newOp + '}\n'
				acumS = acumS -1

			if self.pattern == 'contigous':
				newOp = newOp +'\t}\n'


			self.transOp.append(newOp)


	def printInfo(self):

		for op in range(len(self.operations)):
			print "Original Operation: ",self.operations[op]['operation']
			print "Generated Operation: \n",self.transOp[op]

	def getTransOp(self):
		return self.transOp

	def getInputFile(self):
		return self.inputF

	def getLoopsIndeces(self):
		return self.loopsInd
