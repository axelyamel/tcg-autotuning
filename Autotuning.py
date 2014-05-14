from InputFile import *

class Autotuning:

	def __init__(self,inFile):
		self.inputF = inFile

		
		self.operations = self.inputF.getOperations()
		self.defines = self.inputF.getDefines()
		self.memory = self.inputF.getMemory()
		self.access = self.inputF.getAccess()
		self.inputs = self.inputF.getInputs()
		self.outputs = self.inputF.getOutputs()
		self.funcName = self.inputF.getFuncName()
		self.fOut = self.inputF.getFileOut()

		self.defVars = []

		self.transOp = []
		self.loopsInd = []
		self.pattern = self.inputF.getPattern()

		self.OpLen = len(self.operations)

		self.Script = ''


		curOp = 0

		print "Number of operations: ",self.OpLen

		for key, value in self.defines.items():
			self.defVars.append(key)
			self.Script = self.Script + key + ' = ' + value + '\n'

		
		for op in self.operations:
			newOp = ''
			loops = []
			psuInfo = []
			reduct = []
			redSplit = []
			loops2 = []

			blocks = []
			threads = []
			permutes = []
			registers = []

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

			loopsLen = len(loops)

			threads.append(loops[loopsLen-1])

			if loopsLen > 3:
				blocks.append(loops[loopsLen-4])
			if loopsLen > 2:
				blocks.append(loops[loopsLen-3])
				threads.append(loops[loopsLen-2])
			if loopsLen <= 2:
				blocks.append(loops[loopsLen-2])

			print "CUDA Blocks:",blocks
			print "CUDA Threads:",threads
		
			if loopsLen > 5:
				permutes.append(loops[loopsLen-5])
				permutes.append(loops[loopsLen-6])

				tmpL = loops[loopsLen-5]
				loops[loopsLen-5] = loops[loopsLen-6]
				loops[loopsLen-6] = tmpL

				print "Permutes: ",permutes

			if len(inter) > 0:

				for i in inter:
					registers.append(i)
				print "Registers: ",registers


			if len(permutes) > 0:
				perm = 'tile_by_index('
				if self.OpLen > 1:
					perm = perm + str(curOp) + ','
				perm = perm + '{},{},{},{'
				for li in loops:
					perm = perm + '\"' + li + '\",'

				perm = perm[:-1]
				perm = perm +'})'

				self.Script = self.Script + "\n" + perm + "\n"

			varsOP = []

			for varI in splitL:
				if varI != '':
					varsOP.append(varI)


			cudaize = 'cudaize(' + str(curOp) +',\"'+self.funcName+'_'+str(curOp+1)+'_GPU_\",{'
			for varI in varsOP:
				splitV = re.split(':',varI)
				sizeT = ''

				if splitV[0] in self.outputs:
					sizeT = self.outputs[splitV[0]]['size']
				else:
					sizeT = self.inputs[splitV[0]]['size']

				sizeT = sizeT.replace(',','*')
				cudaize = cudaize + splitV[0] + '=' + sizeT+','

			cudaize = cudaize[:-1]


			cudaize = cudaize + '},{block={' 
			for bi in blocks:
				cudaize = cudaize + '\"' + bi + '\",'
			cudaize = cudaize[:-1]
			cudaize = cudaize + '},thread={'
			for ti in threads:
				cudaize = cudaize + '\"'+ ti + '\",'
			cudaize = cudaize[:-1]
			cudaize = cudaize + '}},{})\n'

			self.Script = self.Script + cudaize



			curOp = curOp +1

	def getScript(self):

		self.fScript = 'init(\"'+self.fOut + '\",\"'+self.funcName+'\",0)\n'
		self.fScript = self.fScript + 'dofile(\"cudaize.lua\")\n'

		self.fScript = self.fScript + self.Script

		print '\nScript Generated:\n',self.fScript

