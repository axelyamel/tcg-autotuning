Tensor-Contraction Generator and Autotuning
===========================================

The Tensor-Contraction generator is a Python program that generates C code based on a simplified input. The TCG input is based on the Tensor-Contration Engine and Build To Order BLAS to create a simple interface that can be extended to every single user.

The core of this framework is to generate CUDA code that run in NVIDIA GPUs. This code contains loop transformations, created by using Autotuning techniques, to achieve performance and better use of the features provided by the device. This is done by generating CUDA-CHiLL script, which are scripts that presents the transformations to be perform over a C code and produce CUDA code. This scripts can be use with the CHiLL compiler (http://ctop.cs.utah.edu).

Developer:

	Axel Y. Rivera
	University of Utah
	axel.rivera at utah.edu

Updates:

	v0.451:Fixed minor bug in the CUDA-CHiLL script output at the cudaize level

	v0.45: Added Naive Autotuning which parries CUDA Threads, Blocks, Registers as well 
		perform	Permutation depending on loop indeces, data access and memory (row 
		or column major).
	       Produce a CUDA-CHiLL script file using the information generated.
	       Added the flag "-s" to specify the name of the output script file.
	       Added the flag "-g" to specify the when the user want to print in screen the 
		generated codes.
	       Added the flag "-no_auto" to prevent Autotuning
	       Fixed the order of parameters when function is created, outputs first and then
		inputs.
	       Matrix-Vector multiplication example added.

	v0.4:  Massive update to the data structure to improve performance and memory handling.
	       Cleaner implementation using Python Dictionaries.
    	       Fixed the tab and spaces in the input. Now user can use tab, spaces or non of
		them when writing start of lines, as well between assignations and operators.
	       Output now don't use C Compound assignment (+=), however it is needed in the
		input because it represents the summation symbol for the Einstein Notation.
	       Input, Output and IO section were fused in one section: "variables".
	       "defines" section was renemade to "define".
	       "operation" section was renamed to "operations".
	       Transformed operations now only show the output operation rather than the full 
		loop nest for a cleaner screen.
	       Stamp added to the output code.
	       
	v0.3:  Very naive CUDA-CHiLL scripts generation added: just check the loop access and
		decides what goes for threads, blocks, register and permute.

	v0.25: Support for higher abstraction.
	       User can now define a Tensor by the order without specify the dimensions' sizes.
	       "jumping" value is now "strided"
	       "inline" value is now "linearize"
	       "io" sectiond added, this is for declaring tensors that are input as well outputs. 
		This section was created due to the definition of Input and Ouput.
	       Fixed bugs in the output code where a variable was input and output.
	
	v0.2:  Support for higher abstraction. 
	       Specify the values of access, memory, pattern and define section.
	       If memory, access and pattern aren't specified, it will select a default.
	       Error handling for undeclarted input/ouput.
	       Fixed bugs in output code.
	       Fixed bugs in input arguments.

	v0.15: Arguments for handling help, wrong input file, printing information, prevent code 
		generation and specifying output file name.
	       Pattern variable added in the input file for handling access data: contigous 
		(matrix multiply like) or jumping (dependant of loop upper bound: j+Jb*(i+Ib)).
	       Reduction loop fixes when specifying column major order.
	
	v0.1:  First implementation, read a file and transform code.
	       Early alpha stage (not recomended for use).
		
Files:

	TCG.py			|	Main file
	InputFile.py		|	Module for handling the Input File
	Transform.py		|	Module for handling code transformation
	CodeGen.py		|	Module for handling code generation
	Autotuning.py		|	Module for handling Autotuning (not save)
	kernels:		|	Directory with examples
		mxm.m		|	Classic matrix multiply
		mxv.m		|	Classic matrix-vector multiply (use it with "-no_auto")
		nek.m		|	TC in Nekbone
		tce.m		|	TC d1 presented in NWCHEM
		tce2.m		|	TC s1 presented in NWCHEM
		eq2.m		|	2D Poisson example

Install:

	Just run it through Python. Install CUDA-CHiLL for using the generated scripts.
	CUDA-CHiLL Link: http://ctop.cs.utah.edu/downloads/chill_rose.tar.gz
	NVIDIA CUDA Link: https://developer.nvidia.com/cuda-downloads

Use:

	Usage: python TCG.py [flags] filename.m [-o filename.c]
	Flags:
		-i		 | 	Print information
		-no_code	 | 	Prevent Code Generation
		-s		 |	Specify output script
		-no_auto	 |	Prevent Autotuning
		-g		 |	Print Generated Code and Script
		-o		 | 	Specify output filename
		-h		 | 	Help

Input file:

	Check folder kernels for some examples.

	File type: filename.m

	File content  ("--" = means explanation, no needed in the input file):


	function name				-- Name of the function (mandatory first)
	access: multidimension | linearize	--(optional)default: multidimension	[i][j] | [i*N+j]
	accelerator: GPU			--(optional)default: GPU		For future work
	memory: row | column			--(optional)default: row		Row or Column major
	pattern: contigous | strided		--(optional)default: contigous		Access pattern
	define:					-- (Optional)Define variables 
		var1 = val
		var2 = val
		    *
   		    *
		    *
		varN = val
	variables:					-- Define input and output data with sizes
		Ti1:(size1, ... ,sizeN)	| orderN	
		    *
		    *
		    *
		Tin:(size1, ..., sizeN) | orderN
		To1:(size1, ... ,sizeN) | orderN		
		    *
		    *
		    *
		Ton:(size1, ..., sizeN) | orderN
	operations:				-- Define the Tensor-Contraction to be done with loop indices
						-- Assignment: += | -=
						-- Operator: + | - | * | /

		ToX1(l1r, ..., lNs) [assingment] TiY1(l1t, ...,lNt) [operator] TiZ1(l1s,...,lNs)
							*
							*
							*
		ToX1(l1r, ..., lNs) [assingment] TiY1(l1t, ...,lNt) [operator] TiZ1(l1s,...,lNs)

Notes:

	Use the C Compound assignment (+=) to express reductions. It represents the classical
	summation symbol in mathematics. This is used to represent the Einstein's Notation
	for Tensors.
	Each operation is binary (one output and two inputs) because of the definition of 
	Tensor-Contraction.
	Autotuning still a work in progress (WiP), output will be naive and only oriented for
	small sizes problems. Future work will be expanded to generate higher levels.
	The output will only produce variables of "double" type. Future update will introduce
	type definitions.
					
Known bugs:

	No explicit form of commenting a line (user must delete it).
	Code generation works only with tensors of order1 or higher.
	Autotuning works only for tensor of order2 or higher.


