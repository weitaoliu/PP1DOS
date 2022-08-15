# NOTE: this file is an essential part of postProcessSVF.py, which defines the
# variables necessary for codes.

# working directory
workingDir = '/home/itvwl/DocITV/'  # for storing figures and .cvs files

# xml file pathway
# filePathway = '/home/itvwl/DocITV/Weekly Report/202206/OutputSYD_1D.xml'  # absolute pathway
filePathway = '/home/itvwl/OpenFOAM/itvwl-5.x/run/SootTest/02_counterflow/sectionSootSims/1Dsims/C2H4Cases' \
              '/2016CnF_Wang/C2H4Cases/C2H4V30_327Species/Output-Soot_Radiaion_Diffusion_FineMesh/Solution.soot.out'  # absolute pathway

# post-process SVF or not, and the mechanism format
ifProcessSVF = False
ifAlreadySVF = True
mechanismFormat = 'CRECK'
BINRemoveFrom = 0
sootDensityUSD = 1800

# output variables
nameOfFile = 'CRECKTest' + '.csv'
ifOutputVariables = True  # this judgement is used for otherOutputList
basicOutputList = ['distance [mm]', 'temperature [K]', 'density', 'pressure']  # written by default
otherOutputList = ['OH', 'CH3']  # used for outputting species




