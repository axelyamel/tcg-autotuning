from CodeGen import *

class Decision(CodeGen):

	def __init__(self,filename,CUDA,CXX,FLAGS,searchAlgo,ARCH,REPS):

		CodeGen.__init__(self,filename)

		self.OrioAnnot = {}

		self.OrioAnnot['params'] = []
		self.OrioAnnot['unrollParams'] = []
		self.OrioAnnot['cuda'] = []
		self.OrioAnnot['reg'] = []
		self.OrioAnnot['permute'] = []
		self.OrioAnnot['unrolls'] = []
		self.OrioAnnot['stm'] = []
		stm = 0

		print 'Running decision Algorithm for: '+ self.FuncName
		smt = 0
		for ops in self.InputFile['operations']:
		
			Indices = []
			summations = []

			ThreadX = []
			TB = []
			
			opsInfo = filter(None,re.split(':|\+=|\-=|\(|\)|\*',ops))

			i = 0
			size = len(opsInfo)
			while(i < len(opsInfo)):
				indices = filter(None,re.split(',',opsInfo[i+1]))
				for ind in indices:
					if ind not in opsInfo[1]:
						summations.append(ind)
					
				
				else:
					if opsInfo[i] in self.tempVar:
						info = filter(None,re.split('\(|,|\)',opsInfo[i+1]))
						Indices.append(info)
				i+= 2
			
			if self.InputFile['memory'] == 'column':
				Indices[0].reverse()


			i = len(Indices[0])-1
			
			while(len(Indices) > 1):
				
				tx = Indices[0][i]
				j=1
				while (j<len(Indices)):

					if tx in Indices[j]:
						ThreadX.append(tx)
						Indices.pop(j)
						
					j+=1
				TB.append(Indices[0][i])
				i-=1

			while(len(TB)<4):

				if len(Indices[0]) > 3:
					TB.append(Indices[0][i])
					i-=1
				else:
					TB.append('1')

			tx = ''
			if len(ThreadX) > 1:

				tx = '['
				for i in ThreadX:
					tx += '\"' + i + '\",'
				tx = tx[:-1] + ']'

			else:
				tx = '[\"' + ThreadX[0] + '\"]'

				TB = []
				for j in range(len(Indices[0])-1,-1,-1):
					TB.append(Indices[0][j])

				while(len(TB)<4):
				    TB.append('1')
					
			self.OrioAnnot['params'].append('param TX' + str(stm) + '[] = ' + tx + ';')

                        TB=list(set(TB))
                        

			TBx = '['
			for i in TB:
				TBx += '\"' + i + '\",'
			TBx = TBx[:-1] + ']'

                        BXx = TBx.replace(",\"1\"","")
                        TYx = TBx
                        BYx = TBx
                        if len(Indices[0]) < 3:
                            TYx = "[\"1\"]"
                            BYx = TYx

			self.OrioAnnot['params'].append('param TY' + str(stm) + '[] = ' + TYx + ';')
			self.OrioAnnot['params'].append('param BX' + str(stm) + '[] = ' + BXx + ';')
			self.OrioAnnot['params'].append('param BY' + str(stm) + '[] = ' + BYx + ';')

			self.OrioAnnot['cuda'].append('cuda('+str(stm)+',block={BX'+ str(stm) + ',BY' + str(stm) + '},thread={TX'+str(stm)+',TY' + str(smt)+'})')

			self.OrioAnnot['reg'].append('registers('+ str(stm) +',\"'+summations[0] + '\")')

			statement = ',('
			permute = ',('

			for ind in self.loopIndices[stm]:
				statement += '\"' + ind + '\",'

				if self.InputFile['memory'] == 'column':
					if ind in TB or ind in summations:
						permute += '\"' + ind + '\",'
					else:
						permute = '\"' + ind + '\",' + permute


			
			statement = statement[:-1] + ')'

			self.OrioAnnot['stm'].append('stm('+ str(stm) + statement + ',\"' + opsInfo[0] + '\")')
			
			if self.InputFile['memory'] == 'column':
				permute = permute[:-1] + ')'
				self.OrioAnnot['permute'].append('permute('+str(stm) + permute + ')')


			sizeInd = self.loopIndices[stm].index(summations[len(summations)-1])
			sizeVar = self.loopIndicesSize[stm][sizeInd]


			unrolls = 'param UF_'+str(stm)+'[] = ['

			val = int(self.Defs[sizeVar])

			for i in range(1,val+1):
				unrolls += str(i) + ','
			unrolls = unrolls[:-1] + '];'

			self.OrioAnnot['unrollParams'].append(unrolls)
			unrolls = 'unroll('+str(stm) + ',\"' + summations[len(summations)-1]+'\",UF_'+str(stm)+')'
			self.OrioAnnot['unrolls'].append(unrolls)

			stm += 1
			
		self.buildAnnotation(stm,CUDA,CXX,FLAGS,searchAlgo,ARCH,REPS)


	def buildAnnotation(self,stmAmmount,CUDA,CXX,FLAGS,searchAlgo,ARCH,REPS):

                cuLibs ='/lib'+ARCH
                comp = CXX + ' ' + FLAGS
		annotation = '/*@ begin PerfTuning ( \ndef build {\n   arg build_command = \''+comp+'\';\n   arg libs = \'rose__orio_chill_.o -I'+CUDA+'/include -L'+CUDA+cuLibs+' -lcudart -lcuda -lm -lrt\';\n }\n'

		annotation +=  ' def performance_counter {\n   arg repetitions = '+REPS+';\n }\n def performance_params {\n'

		for values in self.OrioAnnot['params']:
			annotation += '   ' + values + '\n'


		annotation += '\n\n'
		for values in self.OrioAnnot['unrollParams']:
			annotation += '   ' + values + '\n'


		annotation += ' }\n def input_params {\n'

		for values in self.InputFile['define']:

			val = filter(None,re.split('=',values))

			annotation += '   param ' + val[0] + '[] = [' + str(val[1]) + '];\n'

		annotation += ' }\n  def input_vars {\n'

		for values in self.InputFile['variables']:

			val = filter(None,re.split(':|\(|\)',values))
			val[1] = val[1].replace(',','*')
			
			annotation += '   decl dynamic double ' + val[0] + '[' + val[1] + '] = random;\n'
		annotation += '}\n def search {\n   arg algorithm = \''+searchAlgo+'\';\n }\n   ) @*/\n/*@ begin CHiLL ( \n\n'

		acum = 0

		#for values in self.OrioAnnot['stm']:
		#	annotation += '\t'+ values + '\n'
		#	acum += 1

		#annotation += '\n'
		if stmAmmount > 1:

			annotation += '\tdistribute(1)\n'

		annotation += '\n'

		if self.InputFile['memory'] == 'column':
			for values in self.OrioAnnot['permute']:
				annotation += '\t' + values + '\n'

			annotation += '\n'


		for values in self.OrioAnnot['cuda']:

			annotation += '\t' + values+ '\n'

		annotation += '\n'

		for values in self.OrioAnnot['reg']:

			annotation += '\t' + values+ '\n'

		for values in self.OrioAnnot['unrolls']:

			annotation += '\t' + values+ '\n'


		annotation += '   ) @*/\n'

		self.Annotation = annotation

	def getAnnotation(self):
		return self.Annotation





		




			





