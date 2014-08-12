from InputFile import *
from Transform import *
from CodeGen import *
from Orio import *
import glob

import sys
import os

print "Tensor-Contraction Generator ver0.2"
print "Developed by: Axel Y. Rivera, University of Utah\n"


if sys.argv[1] == '-h':
	print "\nHelp:"
	print "\tUsage: python TCG.py filename.m\n"
	print "\t-i\t\t | \tPrint information"
	print "\t-no_code\t | \tPrevent Code Generation"
	print "\t-o\t\t | \tSpecify output filename"
	print "\t-s\t\t | \tSpecify output script"
	print "\t-no_auto\t | \tPrevent Autotuning"
	print "\t-g\t\t | \tPrint Generated Code and Script"
	print "\t-compiler\t | \tSet compiler, use values GNU or PGI (default = GNU)"
	print "\t-reps\t\t | \tSet amount of tests per Kernel (default = 100)"
	print "\t-Orio\t\t | \tCall Orio to study the generated code"
	print "\t-h\t\t | \tThis help"
	sys.exit()
	
if len(sys.argv) < 2:
	print '\033[91m'+ 'Error: Usage is python TCG.py filename.m'+'\033[0m'
	sys.exit()

info = 0
codegen = 1
autotune = 1
fileFound = 0
outfile = 0
outscript = 0
wrongFile = 0
printCode = 0
OrioCall = 0
OutputFile = ''
OutputScript = ''
Annotation = ''
reps = '100'
compiler = 'GNU'

for i in range(len(sys.argv)):
	if i>0:
		if sys.argv[i] == '-i':
			info = 1
		if sys.argv[i] == '-no_code':
			codegen = 0

		if sys.argv[i] == '-no_auto':
			autotune = 0

		if sys.argv[i] == '-g':
			printCode = 1

		if sys.argv[i] == '-Orio':
			OrioCall = 1

		if sys.argv[i] == '-h':
			print "\nHelp:"
			print "\tUsage: python TCG.py filename.m\n"
			print "\t-i\t\t | \tPrint information"
			print "\t-no_code\t | \tPrevent Code Generation"
			print "\t-o\t\t | \tSpecify output filename"
			print "\t-s\t\t | \tSpecify output script"
			print "\t-no_auto\t | \tPrevent Autotuning"
			print "\t-g\t\t | \tPrint Generated Code and Script"
			print "\t-compiler\t | \tSet compiler, use values GNU or PGI (default = GNU)"
			print "\t-reps\t | \tSet amount of tests per Kernel (default = 100)"
			print "\t-Orio\t | \tCall Orio to process the generated file (not default)"
			print "\t-h\t\t | \tThis help"
			sys.exit()
	
		if sys.argv[i] == '-o':
			OutputFile = sys.argv[i+1]
			outfile = 1
			print "Output file specified: ",OutputFile

	
		if sys.argv[i] == '-reps':
			reps = sys.argv[i+1]
			print "Number of tests per kernel: ",reps

		if sys.argv[i] == '-s':
			OutputScript = sys.argv[i+1]
			outscript = 1
			print "Output script specified: ",OutputScript

		if sys.argv[i] == '-compiler':
			compiler = sys.argv[i+1]
			print "Compiler set as: ",compiler


		if os.path.isfile(sys.argv[i]):
			fileName, fileExtension = os.path.splitext(sys.argv[i])
			if fileExtension != '.m' and fileFound == 0:
				filename = sys.argv[i]
				wrongFile =1
				fileFound = 1
			elif fileExtension == '.m':
				filename = sys.argv[i]
				fileFound = 1
				wrongFile = 0
			if outfile == 0:
				OutputFile = fileName+'.c'

			if outscript == 0:
				OutputScript = fileName+'.lua'

if fileFound == 0:
	print '\033[91m'+ 'Error: No input file'+'\033[0m'
	sys.exit()
if wrongFile == 1:
	print '\033[91m'+ 'Error: Wrong file type: ' + filename +'\033[0m'
	sys.exit()

print "Parsing Input file: ",filename
inFile = InputFile(filename)
if info == 1:
	print "\nInput file information:"
	inFile.printInfo()
	print "\n\n"
print "Transforming operations"
transOP = Transform(inFile)
if info == 1:
	print "\nTransform information"
	transOP.printInfo()
	print "\n\n"

if autotune == 1:
	print "\nGenerating Orio Annotation"
	auto = Orio(transOP,reps,compiler,fileName)
	if info == 1:
		auto.printInfo()
	if printCode == 1:
		auto.printScript()
	Annotation = auto.getAnnotation()

if codegen == 1:
	print "Generating Code"
	code = CodeGen(transOP,Annotation)
	if printCode == 1:
		code.printCode()

	code.OutToFile(OutputFile)
	print "Output file: ",OutputFile

if OrioCall == 1:
	print "Calling Orio"
	wkdir = os.path.dirname(os.path.abspath(OutputFile))
	wrkdirTemp = os.getcwd()
	os.chdir(wkdir)
	OrioFile = filter(None,re.split('\/',OutputFile))
	var = 'N'
	if os.path.isfile("_" + OrioFile[len(OrioFile)-1]) == True:
		var = raw_input("Orio Analysis previously done. Do you want to use these results or perform a new scan? Yes[Y/y] or No [N/n]:  ")
	else:
		var = 'y'

	cmd = 'orcc ' + OrioFile[len(OrioFile)-1]
	cmd2 = 'cp ' + wrkdirTemp + '/clean.sh' + ' ./'
	cmd3 = 'cp ' + wrkdirTemp + '/cudaize.lua' + ' ./'
	if var == 'Y' or var == 'y':
		try:
			os.system(cmd2)
			os.system('./clean.sh')
			os.system(cmd3)
			os.system(cmd)
		except:
			print '\033[91m'+ 'Orio not available' + '\033[0m'
			sys.exit()
	
	bestfile = ''
	bestTime = 1000000
	acumAll = 0



	for filename2 in glob.glob("./times/time_of_*"):

		#print filename2

		acum = 0
		timesAcum = 0

		f = open(filename2)

		for line in f:

			split1 = re.split(': | |\n',line)
		if len(split1) > 3 and split1[0] == 'Time':
			timesAcum = timesAcum + float(split1[5])
			acum = acum + 1

		f.close()

		if acum >0 and timesAcum>0:
			timesAcum = timesAcum / acum


			if timesAcum < bestTime:
				bestfile = filename2
				bestTime = timesAcum
				acumAll = acum


	finalRes = filter(None,re.split('of',bestfile))


	finalName =  OrioFile[len(OrioFile)-1][:-2] + '_Orio.cu'
	fastFile = finalRes[len(finalRes)-1][:-4] + '.cu'
	cmd = 'cp ./outputs/rose__orio_chill' + fastFile + ' ./' + finalName
	
	
	os.system(cmd)
	os.chdir(wrkdirTemp)

	print "\nFinal Output file: " + fileName + "_Orio.cu"
	print "Consumed time: " + str(bestTime) + "sec."
	print "Source file of best output: ./outputs/rose__orio_chill" + fastFile + '\n'







