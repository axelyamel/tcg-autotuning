from InputFile import *
from Transform import *
from CodeGen import *
from Autotuning import *

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
	print "\t-h\t\t | \tThis help"
	sys.exit()
	
if len(sys.argv) < 2:
	print '\033[91m'+ 'Error: Usage is python TCG.py filename.m'+'\033[0m'
	sys.exit()

info = 0
codegen = 1
fileFound = 0
outfile = 0
wrongFile = 0
OutputFile = ''
for i in range(len(sys.argv)):
	if i>0:
		if sys.argv[i] == '-i':
			info = 1
		if sys.argv[i] == '-no_code':
			codegen = 0

		if sys.argv[i] == '-h':
			print "\nHelp:"
			print "\tUsage: python TCG.py filename.m\n"
			print "\t-i\t\t | \tPrint information"
			print "\t-no_code\t | \tPrevent Code Generation"
			print "\t-o\t\t | \tSpecify output filename"
			print "\t-h\t\t | \tThis help"
			sys.exit()
	
		if sys.argv[i] == '-o':
			OutputFile = sys.argv[i+1]
			outfile = 1
			print "Output file specified: ",OutputFile

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

if fileFound == 0:
	print '\033[91m'+ 'Error: No input file'+'\033[0m'
	sys.exit()
if wrongFile == 1:
	print '\033[91m'+ 'Error: Wrong file type: ' + filename +'\033[0m'
	sys.exit()

print "Parsing Input file: ",filename
x = InputFile(filename)
if info == 1:
	print "\nInput file information:"
	x.printInfo()
	print "\n\n"
print "Transforming operations"
y = Transform(x)
if info == 1:
	print "\nTransform information"
	y.printInfo()
	print "\n\n"

print "Generating Code"
z = CodeGen(y)
if info == 1:
	z.printCode()
if codegen == 1:
	z.OutToFile(OutputFile)
	print "Output file: ",OutputFile

##print "Generating CUDA-CHiLL scripts"
##auto = Autotuning(x)
##auto.getScript()
