from Transform import *

class Autotuning:

	def __init__(self,transOPs):
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

		self.Permutes = []
		self.TBlocks = []

		self.Registers = []

		for key,value in self.Defines.items():

			self.Script = self.Script + key + ' = ' + str(value) + '\n'

		if numOps > 1:
			self.Script = self.Script + '\ndistribute({'
			for i in range(numOps):
				self.Script = self.Script + str(i) + ','

			self.Script = self.Script[:-1] + '},1)\n\n'
		
		acum = 0
		for OP in self.OPs:

			TB = []
			PR = []
			REG = []

			parL = OP['parallelLoops']
			redL = OP['reductionLoops']
			numLoops = len(parL)
			threads = 'thread={'
			blocks = 'block={'

			if self.Memory == 'column' and numLoops > 5:

				temp = parL[0]
				parL[0] = parL[1]
				parL[1] = temp

				PR.append(parL[0])
				PR.append(parL[1])

				Permute = Permute + 'tile_by_index(' + str(acum) + ','
				Permute = Permute + '{},{},{},{'
				for i in parL:
					Permute = Permute + '\"'+i+'\",'

				for i in redL:
					Permute = Permute + '\"'+i+'\",'

				Permute = Permute[:-1] + '})\n\n'


			self.Permutes.append(PR)

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


			for key,value in self.dVars.items():

				sizeT = filter(None,re.sub(',','*',value['size']))
				sizes = sizes + key + '=' +sizeT + ','
			sizes = sizes[:-1]

			Cudaize = Cudaize + 'cudaize(' + str(acum) + ',\"' + self.funcName + '_GPU_' + str(acum) + '\",{' + sizes + '},{'+blocks+','+threads+'},{})\n\n'


			outVar = filter(None,re.split(':|\(|,|\)',self.orOP[acum]['output']))[0]

			for i in redL:

				Registers = Registers + 'copy_to_registers(' + str(acum) + ',\"' + i + '\",\"' + outVar + '\")\n\n'

				REG.append(outVar)
				REG.append(i)

			self.Registers.append(REG)

			acum = acum+1
			

		self.Script = self.Script + Permute + Cudaize + Registers

		self.outS = filter(None,re.split('\/',self.fOut))
		self.outF = ''
		outL = len(self.outS)-1
		self.outF = self.outS[outL]


		self.fScript = 'init(\"'+self.outF + '\",\"'+self.funcName+'\",0)\n'
		self.fScript = self.fScript + 'dofile(\"cudaize.lua\")\n\n'

		self.fScript = self.fScript + self.Script



	def printInfo(self):


		print "Autotuning Information: "
		acum = 0
		for op in self.orOP:

			print "\nGenerated transformations for: ",op['output'],op['assignment'],op['input1'],op['operation'],op['input2']

			
			if len(self.Permutes[acum]) > 0:
				print"\tLoops Permuted: ",self.Permutes[acum][1],":",self.Permutes[acum][0]," -> ",self.Permutes[acum][0],":",self.Permutes[acum][1]

			print "\tCUDA Thread-Blocks: ",self.TBlocks[acum][0],", ",self.TBlocks[acum][1]
			print "\tCUDA Registers Operations: Array",self.Registers[acum][0]," at loop ",self.Registers[acum][1]


			acum = acum+1

	def printScript(self):
		print '\nScript Generated:\n',self.fScript

	def OutToFile(self,outfile):
		
		filename = outfile
		fileN = open(filename,'w')
		fileN.write(self.fScript)

		fileN.close()
