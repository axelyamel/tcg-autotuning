from InputFile import *
from Transform import *
from CodeGen import *
from Orio import *

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
	print "\t-reps\t | \tSet amount of tests per Kernel (default = 100)"
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
	auto = Orio(transOP,reps,compiler)
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


