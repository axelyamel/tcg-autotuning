from cx_Freeze import setup, Executable
import sys, os
wdir = os.getcwd()
path2=os.path.dirname(os.path.realpath(__file__))
path = path2 + '/src'
sys.path.append(path)
from Decision import *


buildOptions = dict(
    includes=['os','sys','copy','re'],

)

executables = [
    Executable('tcr.py', base='Console', targetName = 'tcr')
]

setup(
    name='tcr',
    version = '0.625',
    description = 'Tensor contraction representation',
    author="Axel Y. Rivera",
    author_email="axel.rivera@utah.edu",
    url = "https://github.com/axelyamel/tcg-autotuning",
    options = dict(build_exe = buildOptions),
    executables = executables
)
