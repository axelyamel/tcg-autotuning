from Transform import *

class Orio:

	def __init__(self,transOPs,reps,compiler):


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


		if numOps > 1:
			self.Script = self.Script + '\ndistribute(1)'
		
		acum = 0
		for OP in self.OPs:

			outVar = filter(None,re.split(':|\(|,|\)',self.orOP[acum]['output']))[0]
			TB = []
			PR = []
			REG = []
			UNR = []
			
			parL = OP['parallelLoops']
			parSize = OP['parallelSize']
			redL = OP['reductionLoops']
			redSize = OP['reductionSize']

			numLoops = len(parL)
			threads = 'thread={'
			blocks = 'block={'

			if self.Memory == 'column' and numLoops > 5:

				temp = parL[0]
				parL[0] = parL[1]
				parL[1] = temp

				PR.append(parL[0])
				PR.append(parL[1])

				Permute = Permute + '\tpermute(' + str(acum) + ','
				Permute = Permute + '('
				for i in parL:
					Permute = Permute + '\"'+i+'\",'

				for i in redL:
					Permute = Permute + '\"'+i+'\",'

				Permute = Permute[:-1] + '))\n\n'

			

			self.Permutes.append(PR)

			Stms = Stms + '\tsmt(' + str(acum) + ',('
			for i in parL:
				Stms = Stms + '\"' + i + '\",'

			for i in redL:
				Stms = Stms + '\"' + i + '\",'

			Stms = Stms[:-1] + '),\"' +outVar+'\")\n'

			if numLoops < 3:
				threads = threads + '\"' + parL[1] + '\"'
				blocks = blocks + '\"' + parL[0] + '\"'
			elif numLoops == 3:
				threads = threads + '\"' + parL[2] + '\",\"' + parL[1] + '\"' 
				blocks = blocks + '\"' + parL[0] + '\"'
			elif numLoops > 3:

				threads = threads + '\"' + parL[numLoops-1] + '\",\"' +parL[numLoops-2] + '\"' 
				blocks = blocks + '\"' + parL[numLoops-4] + '\",' + '\"' + parL[numLoops-3] + '\"'

 
			threads = threads + '}'
			blocks = blocks + '}'

			TB.append(threads)
			TB.append(blocks)

			self.TBlocks.append(TB)

			sizes = ''

			Cudaize = Cudaize + '\tcuda(' + str(acum) + ','+blocks+','+threads+')\n\n'



			for i in redL:

				Registers = Registers + '\tregisters(' + str(acum) + ',\"' + i + '\")\n\n'

				REG.append(outVar)
				REG.append(i)

			self.Registers.append(REG)

			acum1 = 0
			
			for i in redSize:
				
				self.PerfParams = self.PerfParams + '    param UF' + str(acum) + '[] = ['
				fullUnroll = 1
	
				sizeT = filter(None,re.split('\*',i))
				
				for j in sizeT:

					fullUnroll = fullUnroll * int(self.Defines[j])

				for i in range(2,11):
					mods = fullUnroll % i
					if mods == 0 and i < fullUnroll:
						
						self.PerfParams = self.PerfParams + str(i) + ','
						self.perfAcum = self.perfAcum + 1
						UNR.append(str(i))
				
				finalUnroll = ''
				if fullUnroll > 20:
					finalUnroll = ''
					self.PerfParams = self.PerfParams[:-1]
				else:
					finalUnroll = str(fullUnroll)
					UNR.append(str(fullUnroll))

				self.Unrolls.append(UNR)



				self.PerfParams = self.PerfParams + finalUnroll + '];\n'
				Unrolls = Unrolls + '\tunroll(' + str(acum) + ',\"' + redL[acum1] + '\", UF' + str(acum) +')\n'
				acum1 = acum1 + 1
				

			if self.perfAcum == 0:
				self.PerfParams = self.PerfParams + '    param Dummy' + str(acum) + '[] = [1];\n'

			acum = acum+1
			
		self.PerfParams = self.PerfParams + ' }\n'

		self.CHILL = '/* begin CHiLL ( \n\n' + Stms + Permute  + Cudaize + Registers  + Unrolls  +'   ) @*/\n'

		self.Perf = '/*@ begin PerfTuning ( \n' + self.BuildCMD + self.PerfParams + self.InputParams + self.InputVar + self.Search + '   ) @*/\n'

		self.Script = self.Perf + self.CHILL

		self.outS = filter(None,re.split('\/',self.fOut))
		self.outF = ''
		outL = len(self.outS)-1
		self.outF = self.outS[outL]




	def printInfo(self):


		print "Autotuning Information: "
		acum = 0
		for op in self.orOP:

			print "\nGenerated transformations for: ",op['output'],op['assignment'],op['input1'],op['operation'],op['input2']

			
			if len(self.Permutes[acum]) > 0:
				print"\tLoops Permuted: ",self.Permutes[acum][1],":",self.Permutes[acum][0]," -> ",self.Permutes[acum][0],":",self.Permutes[acum][1]

			print "\tCUDA Thread-Blocks: ",self.TBlocks[acum][0],", ",self.TBlocks[acum][1]
			if len(self.Registers) > 1:
				print "\tCUDA Registers Operations: Array",self.Registers[acum][0]," at loop ",self.Registers[acum][1]

			if self.perfAcum > 0:
				unrolls = ''
				for i in self.Unrolls[acum]:
					unrolls = unrolls + i + ', '
				unrolls = unrolls[:-1]

				print "\tUnroll ammounts Register loop: " + unrolls

			acum = acum+1

	def printScript(self):
		print '\nScript Generated:\n',self.Script

	def getAnnotation(self):
		return self.Script
