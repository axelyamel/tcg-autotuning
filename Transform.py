from InputFile import *

class Transform:

	def __init__(self,inFile):
		self.inputF = inFile

		
		self.operations = self.inputF.getOperations()
		self.defines = self.inputF.getDefines()
		self.memory = self.inputF.getMemory()
		self.access = self.inputF.getAccess()
		self.variables = self.inputF.getVariables()

		self.transOp = []
		self.pattern = self.inputF.getPattern()
		self.Index = []

		acumLoop = 0

		for op in self.operations:


			tOP = {}
			tVars = []

			dVars = []
			tSize2 = []
			tOpI2 = []

			varsI = filter(None,re.split(':|\(|\)',op['output']))
			dVars.append(varsI[0])
		
			varsI2 = filter(None,re.split(',',varsI[1]))
			tOpI2.append(varsI2)

				
			sizeI = self.variables[varsI[0]]['size']
			sizeI2 = filter(None,re.split(',',sizeI))
			tSize2.append(sizeI2)



			varsI = filter(None,re.split(':|\(|\)',op['input1']))
			dVars.append(varsI[0])
	
			varsI2 = filter(None,re.split(',',varsI[1]))
			tOpI2.append(varsI2)

			sizeI = self.variables[varsI[0]]['size']
			sizeI2 = filter(None,re.split(',',sizeI))
			tSize2.append(sizeI2)


			varsI = filter(None,re.split(':|\(|\)',op['input2']))
			dVars.append(varsI[0])
	
			varsI2 = filter(None,re.split(',',varsI[1]))
			tOpI2.append(varsI2)

			sizeI = self.variables[varsI[0]]['size']
			sizeI2 = filter(None,re.split(',',sizeI))
			tSize2.append(sizeI2)


			OutsizeT = 1
			InSizeT = 1

			for i in tSize2[0]:
				sizeTempI = filter(None,re.split('(\*|\+|\-|\/)',i))
				for j in sizeTempI:
					if j != '*':
						OutsizeT = OutsizeT * int(self.defines[j])
						
			for k in range(1,len(tSize2)):
				InSizeT = 1
				for i in tSize2[k]:
					sizeTempI = filter(None,re.split('(\*|\+|\-|\/)',i))
					for j in sizeTempI:
						if j != '*':
							InSizeT = InSizeT * int(self.defines[j])

				if InSizeT == OutsizeT:
					tSize2[k] = tSize2[0]


			newOP = ''
			if self.access == 'multidimension':
				varT = re.sub(':\(','[',op['output'])
				varT = re.sub(',','][',varT)
				varT = re.sub('\)',']',varT)
				
				tVars.append(varT)

				varT = re.sub(':\(','[',op['input1'])
				varT = re.sub(',','][',varT)
				varT = re.sub('\)',']',varT)
				tVars.append(varT)

				varT = re.sub(':\(','[',op['input2'])
				varT = re.sub(',','][',varT)
				varT = re.sub('\)',']',varT)
				tVars.append(varT)

			elif self.access == 'linearize':

			
				varT = ''
				if self.pattern == 'contigous':
					
					for l in range(3):
						varT = ''
						varT = varT + dVars[l] + '['
						acum = 1
						for i in tOpI2[l]:
							varT = varT + i
							for j in range(acum,len(tSize2[l])):
								varT = varT + '*' + tSize2[l][j]
							varT = varT + ' + '

							acum = acum +1
						varT = varT[:-3] + ']'
						tVars.append(varT)

				if self.pattern == 'strided':
					
					for l in range(3):
						varT = ''
						varT = varT + dVars[l] + '['
						acum = 0
						for i in tOpI2[l]:
							addS = ''
							if acum < (len(tSize2[l]) - 1):
								addS = tSize2[l][acum+1]
							varT = varT + i+ ' + ' + addS + '*('

							acum = acum +1
						addS = ''
						varT = varT[:-5]
						for i in range(1,len(tOpI2[l])):
							addS = addS + ')'
						varT = varT + addS + ']'
						tVars.append(varT)

			assig = ' = ' + tVars[0] 
			if op['assignment'] == '+=':
				assig = assig + ' + '
			elif op['assignment'] == '-=':
				assig = assig + ' - '

			tOP['operation'] = tVars[0] + ' ' + assig + ' (' + tVars[1] + ' ' + op['operation'] + ' ' + tVars[2]+')'

			tOP['variables'] = tVars



			loopNest = []
			reduction = []
			
			if self.memory == 'column':
				tOpI2[0].reverse()
				tSize2[0].reverse()


			loopNest.append(tOpI2[0])
			loopNest.append(tSize2[0])

			tarr = []
			tarr2 = []
			for i in range(1,3):
				for j in range(len(tOpI2[i])):
					if tOpI2[i][j] not in loopNest[0] and tOpI2[i][j] not in tarr:	
						tarr.append(tOpI2[i][j])
						tarr2.append(tSize2[i][j])
			reduction.append(tarr)
			reduction.append(tarr2)


			loopGen = ''
			acum = 1
			highL = ''
			if acumLoop == 0 and len(self.operations) > 1:
				
				highL = highL + '\tfor(' + loopNest[0][0] +' = 0; '+loopNest[0][0]+' < ' +loopNest[1][0] + '; '+loopNest[0][0] + '++){\n'
				acumLoop = acumLoop +1
	
			for i in range(len(loopNest[0])):

				if loopNest[0][i] not in self.Index:
					self.Index.append(loopNest[0][i])

				for j in range(acum):
					loopGen = loopGen + '\t'
				
				if len(self.operations)==1:
			
					loopGen = loopGen + 'for(' + loopNest[0][i] +' = 0; '+loopNest[0][i]+' < ' +loopNest[1][i] + '; '+loopNest[0][i] + '++){\n'
				else:
					if i != 0:
						loopGen = loopGen + 'for(' + loopNest[0][i] +' = 0; '+loopNest[0][i]+' < ' +loopNest[1][i] + '; '+loopNest[0][i] + '++){\n'
					else:
						loopGen = loopGen + '\n'

				
				acum = acum +1 
			tOP['parallelLoops'] = loopNest[0]
			tOP['parallelSize'] = loopNest[1]

			for i in range(len(reduction[0])):
				
				if reduction[0][i] not in self.Index:
					self.Index.append(reduction[0][i])

				for j in range(acum):
					loopGen = loopGen + '\t'
				loopGen = loopGen + 'for(' + reduction[0][i] +' = 0; '+reduction[0][i]+' < ' +reduction[1][i] + '; '+reduction[0][i] + '++){\n'
				acum = acum +1 

			tOP['reductionLoops'] = reduction[0]
			tOP['reductionSize'] = reduction[1]

			print loopGen

			for j in range(acum):
				loopGen = loopGen + '\t'
			closeL = '\n'

			acum = acum-1
			for i in range(len(reduction[0])):
				
				for j in range(acum):
					closeL = closeL + '\t'
				closeL = closeL + '}\n'
				acum = acum -1

			for i in range(len(loopNest[0])):
				for j in range(acum):
					closeL = closeL + '\t'
				closeL = closeL + '}\n'
				acum = acum -1

			if len(self.operations) > 1:
				closeL = closeL[:-2] + '\n'

			tOP['loopGen'] = loopGen
			tOP['close'] = closeL
			tOP['highLoop'] = highL

			self.transOp.append(tOP)


	def printInfo(self):

		for op in range(len(self.operations)):
			print "Original Operation: ",self.operations[op]['output'],self.operations[op]['assignment'],self.operations[op]['input1'],self.operations[op]['operation'],self.operations[op]['input2']

			print "Generated Operation: ",self.transOp[op]['operation'],"\n"

	def getTransOp(self):
		return self.transOp

	def getInputFile(self):
		return self.inputF

	def getLoopsIndeces(self):
		return self.Index
