from Transform import *
import copy
import collections

class Orio:

	def __init__(self,transOPs,reps,compiler,fileNameT):


		self.Compiler = compiler
		self.Repetitions = reps
		self.transformOP = transOPs
		self.inFile = self.transformOP.getInputFile()
		self.Defines = self.inFile.getDefines()
		self.dVars = self.inFile.getVariables()
		self.funcName = self.inFile.getFuncName()
		self.fOut = self.inFile.getFileOut()
		self.orOP = self.inFile.getOperations()
		self.OPs = self.transformOP.getTransOp()
		self.Memory = self.inFile.getMemory()
		self.pattern = self.inFile.getPattern()
		self.fileNameT = fileNameT

		numOps = len(self.OPs)

		self.Script = ''

		Permute = ''
		Cudaize = ''
		Registers = ''
		Tiles = ''
		Stms = ''
		Unrolls = ''
		comp = ''

		self.Permutes = []
		self.TBlocks = []
		self.Registers = []
		self.Unrolls = []

		if self.Compiler == 'PGI':
			comp = 'pgc++ -fast'
		elif self.Compiler == 'GNU':
			comp = 'g++ -O3'

		self.BuildCMD = ' def build {\n   arg build_command = \'' + comp + '\';\n   arg libs = \'rose__orio_chill_.o -I/usr/local/cuda-5.5/include -L/usr/local/cuda-5.5/lib64 -lcudart -lcuda -lm -lrt\';\n }\n def performance_counter {\n   arg repetitions = '+ self.Repetitions +';\n }\n'

		self.InputParams = ' def input_params {\n'
		
		for key,value in self.Defines.items():

			self.InputParams = self.InputParams + '   param ' + key + '[]  = [' + str(value) + '];\n'
		self.InputParams = self.InputParams +' }\n'

		self.PerfParams = ' def performance_params {\n'
		self.perfAcum = 0
		self.InputVar = '  def input_vars {\n'

		for key,value in self.dVars.items():
			sizeT = filter(None,re.sub(',','*',value['size']))
			self.InputVar = self.InputVar + '   decl dynamic double ' + key + '[' + sizeT +'] = random;\n'

		self.InputVar = self.InputVar + ' }\n'

		self.Search = ' def search {\n   arg algorithm = \'Exhaustive\';\n }\n'

		self.distribute = ''
		if numOps > 1:
			self.distribute = '\n\tdistribute(1)\n'
		
		acum = 0
		for OP in self.OPs:

			outVar = filter(None,re.split(':|\(|,|\)',self.orOP[acum]['output']))[0]
			TB = []
			PR = []
			REG = []
			UNR = []
			
			parL = OP['parallelLoops']
			parPos = []
			parSize = OP['parallelSize']
			redL = OP['reductionLoops']
			redSize = OP['reductionSize']

			numLoops = len(parL)

			ThreadsA = []
			BlockA = []

			Stms = Stms + '\tstm(' + str(acum) + ',('
			
			for i in range(len(parL)):
				parPos.append(i)


			for i in parL:
				Stms = Stms + '\"' + i + '\",'

			for i in redL:
				Stms = Stms + '\"' + i + '\",'

			Stms = Stms[:-1] + '),\"' +outVar+'\")\n'

			sizeThread = 1
			In1Loop = []
			In2Loop = []
			TBdec = []
			TBpos = []
			acumIOVars = 0
			for i in OP['variables']:
				splitIOVars = filter(None,re.split('\[|\*| |\(|\)|\]|\+',i))
				sizeIOV = len(splitIOVars)
				added = 0

				for j in range(0,sizeIOV):
					if splitIOVars[j] in redL or splitIOVars[j] in self.Defines:
						splitIOVars[j] = None

				splitIOVars = filter(None,splitIOVars)

				splitIOVars.pop(0)
				

				if acumIOVars == 1:
					In1Loop = splitIOVars				

				if acumIOVars == 2:
					In2Loop = splitIOVars

	
				acumIOVars = acumIOVars+1


			largestNest = 0
			longNest = []
			shortNest = []

			if len(In1Loop) >= len(In2Loop):
				largestNest = len(In1Loop)
				longNest = In1Loop
				shortNest = In2Loop
			else:
				largestNest = len(In2Loop)
				longNest = In2Loop
				shortNest = In1Loop

			for i in range(0,4):

				in1 = ''
				in2 = ''
				
				if len(In2Loop) > 0:

					if i == 1:
						tmp = In1Loop.pop()
						ind = parL.index(tmp)
						TBpos.append(ind)
						TBdec.append(tmp)
						parPos[ind] = -1

					else:
						tmp = In2Loop.pop(0)
						ind = parL.index(tmp)
						TBpos.append(ind)
						TBdec.append(tmp)
						parPos[ind] = -1

				if len(In2Loop) == 0:
					In2Loop = In1Loop



			for i in range(len(TBpos)):
				for j in range(len(TBpos)):
					if TBpos[i]<TBpos[j]:
						tmp = TBpos[i]
						TBpos[i] = TBpos[j]
						TBpos[j] = tmp
						tmp = TBdec[i]
						TBdec[i] = TBdec[j]
						TBdec[j] = tmp

	


	
			threads = 'thread={\"' + TBdec[len(TBdec)-1] + '\"'
			blocks = 'block={\"' + TBdec[0] + '\"'

			if len(TBdec)-1 > len(TBdec)/2:
				threads = threads + ',\"' +  TBdec[len(TBdec)-2] + '\"'
				
				if len(TBdec)/2 == 2:
					blocks = blocks + ',\"' + TBdec[1] + '\"'

			threads = threads + '}'
			blocks = blocks + '}'
			
			self.TBlocks.append([blocks,threads])
			
		
			parNew = copy.deepcopy(parL)
			if self.Memory == 'column' and len(parL) > 1:

				eqArr = 1

				for i in range(len(parL)-1):
					pos = i
					j = i + 1
					stop = 0
					if(parPos[i] == -1):
						stop = 1


					while (stop != 1):

						if parPos[j] != -1 and parPos[j] > parPos[i]:
							pos = j

						if parPos[j] == -1:
							stop = 1

						j = j+1

					tmp = parPos[pos]
					parPos[pos] = parPos[i]
					parPos[i] = tmp

					tmp = parL[pos]
					parL[pos] = parL[i]
					parL[i] = tmp

					if parL[pos] != parL[i]:

						tempPerm = []
						tempPerm.append('\"'+parL[pos]+'\"')
						tempPerm.append('\"'+parL[i]+'\"')
					
						self.Permutes.append(tempPerm)

				for i in range(len(parNew)):
					if parNew[i] != parL[i]:
						eqArr = 0

				if eqArr == 0:
					tempPerm = ''
					Permute = Permute + '\tpermute(' + str(acum) + ','
					Permute = Permute + '('
					for i in parL:
						Permute = Permute + '\"'+i+'\",'

					for i in redL:
						Permute = Permute + '\"'+i+'\",'


					Permute = Permute[:-1] + '))\n\n'


			Cudaize = Cudaize + '\tcuda(' + str(acum) + ','+blocks+','+threads+')\n\n'



			for i in redL:

				Registers = Registers + '\tregisters(' + str(acum) + ',\"' + i + '\")\n\n'
				

				REG.append(outVar)
				REG.append(i)
				self.Registers.append(REG)

			acum1 = 0
			
			for i in redSize:
				
				self.PerfParams = self.PerfParams + '    param UF' + str(acum) + '[] = [1,'
				fullUnroll = 1
	
				sizeT = filter(None,re.split('\*',i))
				
				for j in sizeT:

					fullUnroll = fullUnroll * int(self.Defines[j])

				
				for i in range(2,fullUnroll):
					mods = fullUnroll % i
					if mods == 0 and i < fullUnroll:
						
						self.PerfParams = self.PerfParams + str(i) + ','
						self.perfAcum = self.perfAcum + 1
						UNR.append(str(i))
				
				finalUnroll = str(fullUnroll)
				UNR.append(str(fullUnroll))

				self.Unrolls.append(UNR)



				self.PerfParams = self.PerfParams + finalUnroll + '];\n'
				Unrolls = Unrolls + '\tunroll(' + str(acum) + ',\"' + redL[acum1] + '\",UF' + str(acum) +')\n'
				acum1 = acum1 + 1
				

			if self.perfAcum == 0:
				self.PerfParams = self.PerfParams + '    param Dummy' + str(acum) + '[] = [1];\n'

			acum = acum+1
			
		self.PerfParams = self.PerfParams + ' }\n'

		self.CHILL = '/*@ begin CHiLL ( \n\n' + Stms + self.distribute + Permute  + Cudaize + Registers  + Unrolls  +'   ) @*/\n'

		self.Perf = '/*@ begin PerfTuning ( \n' + self.BuildCMD + self.PerfParams + self.InputParams + self.InputVar + self.Search + '   ) @*/\n'

		self.Script = self.Perf + self.CHILL

		self.outS = filter(None,re.split('\/',self.fOut))
		self.outF = ''
		outL = len(self.outS)-1
		self.outF = self.outS[outL]




	def printInfo(self):


		print "Autotuning Information: "
		acum = 0

		fname = self.fileNameT + '_Autotuning.txt'
		f = open(fname,'w')
		for op in self.orOP:


			transOPInfo = "\nGenerated transformations for: " + op['output'] + op['assignment'] + op['input1'] + op['operation'] + op['input2']


			print transOPInfo
			if len(self.Permutes) > 0:	
				if len(self.Permutes[acum]) > 0:
					permsInfo = "\tLoops Permuted: " + self.Permutes[acum][1] + " : " + self.Permutes[acum][0] + " -> " + self.Permutes[acum][0] + " : " + self.Permutes[acum][1]

					print permsInfop

			cudaInfo = "\tCUDA Thread-Blocks: " + self.TBlocks[acum][0] + ", " +self.TBlocks[acum][1]

			print cudaInfo
			if len(self.Registers) > 0:
				regInfo = "\tCUDA Registers Operations: Array " + self.Registers[acum][0] + " at loop " +self.Registers[acum][1]

				print regInfo

			if self.perfAcum > 0:
				unrolls = ''
				for i in self.Unrolls[acum]:
					unrolls = unrolls + i + ', '
				unrolls = unrolls[:-2]
				unInfo = "\tUnroll ammounts Register loop: no unroll, " + unrolls

				print unInfo

			acum = acum+1


		    	f.write(transOPInfo+'\n')
			if len(self.Permutes) > 0:
				f.write(permsInfo+'\n')
			f.write(cudaInfo+'\n')
			if len(self.Registers) > 0:
				f.write(regInfo+'\n')
			if self.perfAcum > 0:
				f.write(unInfo+'\n')

		f.close()

	def printScript(self):
		print '\nScript Generated:\n',self.Script

	def getAnnotation(self):
		return self.Script
