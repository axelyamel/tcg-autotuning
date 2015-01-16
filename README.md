Tensor contraction Representation
=================================

The tensor contraction representation is a Python program that generates C code based on a simplified input. It adds an annotion to the code which will be used by Orio Performance-Tuning system for applying autotuning. The goal of this interface is to generate CUDA code that run in NVIDIA GPUs. This code contains loop transformations, created by a decision algrothim, to achieve better performance and use the features available in the device. The output of this program can be used with Orio (http://trac.mcs.anl.gov/projects/performance/wiki/Orio).

Developer:

	Axel Y. Rivera
	University of Utah
	axel.rivera at utah.edu

Updates:

	v0.63: Orio constrains generated automatically.
	       Option for specifying the ammoun of runs in the search algorithm.
	       Option for automatically launch Orio and output the best version
		automatically (see Usage section).


	v0.625:Minor update to the Main function for errors handling.
	       Added "-h" flag for help option. This flag show the new stuffs like
		specify compiler, compiler flags, among others. Everyting between 
		brackets ([]) means that is the default value.
	       Updated some bugs related to the annotation generator.
	       Installer that use cx_freeze added for simplified use.
	    

	v0.62: Huge update in the structure. Support for multiple multiplications. 
       	       Increase the search space. Fixes on decision algorithm. Better 
		object orientation implementations. Due to the massive update, the 
                automatic Orio was removed temporary, as well the compiler specification.
               Main file still a WIP. File type for input file changed from .m to .oct 
                (output still .c).


	v0.50: A tensor of order N can be used with other orders while it have the same
		data size (see example kernels/nek.m), only works for linearized access
	       Fixed the Output information for Autotuning  (information now stored in 
                fileName_Autotuning.txt)
	       Added support for calling Orio automatically (Orio must be installed)
	       Print the information of the final output (Source file and time)
 	       Final output from the exhaustive tests stored in filename_Orio.cu
	       

	v0.46: Removed the production of CUDA-CHill code and Orio annotations are created
		using the same autotuning techniques.
	       Output already contains the annotations, code is ready to use with Orio.
	       Added support to loop unrolling at reduction loops (Register levels).
	       Added support to specify the compiler to be used (GNU or PGI)
	       Added support to specify the amount of tests to be performed.


	v0.452:Fixed Copy to registers not having the statement.
	       Fixed tile_by_index not having the statement index.
	       If there is more than one operation with the same the outer most loop index,
		then they are fused.
	       

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

	tcr.py			|	Main file
	setup.py		|	Setup file
	README.md		|	This file
	src:			|	Directory for Source codes
		InputFile.py	|	Module for handling the Input File
		CodeGen.py	|	Module for handling code generation
		Decision.py	|	Module for handling Autotuning 
	kernels:		|	Directory with examples
		test_SPEM	|	Directory with spectral element examples	
		test_tce	|	Directory with CCSD d1 examples
		test_mxm	|	Directory with MxM exmaples

Install:
	
	Install cx-Freeze: sudo apt-get install cx-freeze
	Type: sudo python setup.py install

Usage: 

	Type: tcr filename.oct [OPTIONS]

	Options:

		 -h 	 Help print

		 Code generation options:
			 -search=STRATEGY 	 Orio search-space study strategy 
						 STRATEGY=[Exahustive] or Mlsearch
			 -arch=ARCH 		 Specify type of architecture 
						 ARCH=[x86_64] or x86
			 -reps=N 		 Specify the ammount of repetitions for tests 
						 N=[100] or integer
			 -s_runs=N 		 Specify the ammount of runs in the search algorithm 
						 N=[100] or integer
			 -Orio 			 Launch Orio with the created file 
						 Warning: Make sure Orio is installed



		 Compiler options:
			 CXX 			 Specify the C++ compiler 
						 CXX=[g++] or prefered compiler
			 CFLAGS 		 Specify the C++ compiler flags 
						 CFLAGS =["-O3"] or "list of flags"
			 CUDA 			 Specify where are located the CUDA files 
						 CUDA=[/usr/local/cuda] or prefered path


	If you want to use Orio, make sure that CUDA-CHiLL, Orio and CUDA are installed.

	CUDA-CHiLL Link: http://ctop.cs.utah.edu/ctop/?page_id=21
	Orio Link: http://trac.mcs.anl.gov/projects/performance/wiki/Orio
	NVIDIA CUDA Link: https://developer.nvidia.com/cuda-downloads

Input file:

	Check folder kernels for some examples.

	File type: filename.oct

	File content  ("--" = means explanation, no needed in the input file):


	function name				-- Name of the function (mandatory first)
	access: [multidimension] | linearize	--(optional) [i][j] | [i*N+j]
	memory: [row] | column			--(optional) Row or Column major
	pattern: [contigous] | strided		--(optional) Access pattern
	define:					--(optional) Define variables 
		var1 = val
		var2 = val
		    .
   		    .
		    .
		varN = val
	variables:					-- Define input and output data with sizes
		Ti1:(size1, ... ,sizeN)	| orderN	
		    .
		    .
		    .
		Tin:(size1, ..., sizeN) | orderN
		To1:(size1, ... ,sizeN) | orderN		
		    .
		    .
		    .
		Ton:(size1, ..., sizeN) | orderN
	operations:				-- Define the Tensor-Contraction to be done with loop indices
						-- Assignment: += | -=
						

		ToX1(l1r, ..., lNs) [assingment] TiY1(l1t, ...,lNt) * TiZ1(l1s,...,lNs)
							.
							.
							.
		ToX1(l1r, ..., lNs) [assingment] TiY1(l1t, ...,lNt) * TiZ1(l1s,...,lNs)

Notes:

	Use the C Compound assignment (+=) to express reductions. It represents the classical
	summation symbol in mathematics. This is used to represent the Einstein's Notation
	for Tensors.
	Decision Algorithm produces a huge search space, if you are using exhaustive search
	to study , this test will take a while.
	The output will only produce variables of "double" type. Future update will introduce
	type definitions.
	Even though the framework works without defining the dimension's sizes, for better 
	use of autotuning, please specify the dimension's sizes.
					
Known bugs:

	No explicit form of commenting a line (user must delete it).
	Code generation works only with tensors of order_1 (arrays) or higher.
	When using more than one operations, keep the same index variables from outer to inner.
	Any bug you find, please report it into the gibhub link.



