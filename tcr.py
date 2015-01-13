import sys, os
wdir = os.getcwd()
path2=''
if getattr(sys, 'frozen', False):
    # frozen
    path2 = os.path.dirname(sys.executable)
else:
    # unfrozen
    path2 = os.path.dirname(os.path.realpath(__file__))

path = path2 + '/src'
sys.path.append(path)
from Decision import *


def main(fileName,CUDA,CXX,FLAGS,OrioRun,searchAlgo,ARCH,REPS):

    tensor = Decision(fileName,CUDA,CXX,FLAGS,searchAlgo,ARCH,REPS)
    annotation = tensor.getAnnotation()
    code = tensor.generate_code(annotation)

    newfile = open(tensor.getFileName(),'w')

    newfile.write(code)

    newfile.close()

    print 'Output generated in: ' + tensor.getFileName()

def print_help():
    print "Tensor-contraction representation \nAxel Y. Rivera\nUniversity of Utah\n"
    print "Usage: tcr filename.oct [OPTIONS]\n"
    print "Options:\n"
    print "\t -h \t This help"
    print "\n\t Code generation options:" 
    print "\t\t -search=STRATEGY \t Orio search-space study strategy \n\t\t\t\t\t STRATEGY=[Exahustive] or Mlsearch"
    print "\t\t -arch=ARCH \t\t Specify type of architecture \n\t\t\t\t\t ARCH=[x86_64] or x86"
    print "\t\t -reps=N \t\t Specify the ammount of repetitions for tests \n\t\t\t\t\t N=[100] or integer"
    print "\n\t Compiler options:"
    print "\t\t CXX \t\t\t Specify the C++ compiler \n\t\t\t\t\t CXX=[g++] or prefered compiler"
    print "\t\t CFLAGS \t\t Specify the C++ compiler flags \n\t\t\t\t\t CFLAGS =[\"-O3\"] or \"list of flags\""
    print "\t\t CUDA \t\t\t Specify where are located the CUDA files \n\t\t\t\t\t CUDA=[/usr/local/cuda] or prefered path"
    sys.exit()
    


if __name__ == "__main__":

    fileFound = False

    if len(sys.argv) == 1:
        print_help()

    if sys.argv[1] == '-h':
        print_help()

    fileName = sys.argv[1]

    try:
        test = open(fileName)
    except IOError:
        print ('Error: File not found. Usage: python tcr.py filename.oct [OPTIONS]')
        sys.exit()


    fileType = filter(None,re.split('\.',fileName))[1]

    if fileType != 'oct':
        print ('Error: Wrong file type, use .oct file')
        sys.exit()


    searchAlgo = 'Exhaustive'
    CXX='g++'
    FLAGS = '-O3'
    OrioRun = False
    CUDA = '/usr/local/cuda'
    ARCH='64'
    REPS = '100'

    for i in sys.argv:
        if i == '-h':
            print_help()

        if '-search' in i:

            search = filter(None,re.split('=',i))
            if len(search) < 2:
                print ('Error: Search space prunning technique not specified')
                sys.exit()
            searchAlgo = search[1]


        if 'CXX' in i:
            comp = filter(None,re.split('=',i))
            if len(comp) < 2:
                print ('Error: C++ compiler not specified')
                sys.exit()
            CXX = comp[1]

        if 'CFLAGS' in i:
            comp = filter(None,re.split('=',i))
            if len(comp) < 2:
                print ('Warning: C++ compiler flags not specified. At least use an optimization flag.')
                FLAGS = ''
            else:
                FLAGS = comp[1]

        if 'CUDA' in i:

            comp = filter(None,re.split('=',i))
            if len(comp) < 2:
                print ('Warning: CUDA libraries not specified. Using default.')
            else:
                CUDA = comp[1]

                cudafiles = os.path.exists(CUDA+'/lib'+ARCH+'/libcudart.so')
                if cudafiles == False:
                    print "Error: libcudart.so not found. Make sure your CUDA files are configured correctly"
                    sys.exit()

        if '-arch' in i:

            arch = filter(None,re.split('=',i))
            if len(arch) < 2:
                print ('Warning: Architecture not specified. Using default.')

                
            else:
                
                if arch[1] == 'x86':
                    ARCH = ''
                elif arch[1] == 'x86_64':
                    ARCH = '64'
                else:
                    print "Error: Architecture specified wrong"
                    sys.exit()
            
        if '-reps' in i:

            amount = filter(None,re.split('=',i))
            if len(amount) < 2:
                print ("Error: Ammount of repetitions is empty")
                sys.exit()

            else:
                if amount[1].isdigit() == True:
                    REPS = amount[1]
                else:
                    print ("Error: Repetitions should be an integer")
                    sys.exit()

    
    main(fileName,CUDA,CXX,FLAGS,OrioRun,searchAlgo,ARCH,REPS)

