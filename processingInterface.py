# NOTE: this file is an essential part of postProcessSVF.py, which defines the
# variables necessary for codes.

# working directory
workingDir = '/home/itvwl/DocITV/'  # for storing figures and .cvs files

# xml file pathway
filePathway = '/home/itvwl/DocITV/Weekly Report/202206/OutputSYD_1D.xml'  # absolute pathway

# post-process SVF or not, and the mechanism format
ifProcessSVF = True
ifAlreadySVF = False
mechanismFormat = 'SYD'
BINRemoveFrom = 0
sootDensityUSD = 1800

# output variables
nameOfFile = 'SYDTest' + '.csv'
ifOutputVariables = True  # this judgement is used for otherOutputList
basicOutputList = ['distance [mm]', 'temperature [K]', 'density', 'pressure']  # written by default
otherOutputList = ['OH', 'CH3']  # used for outputting species




