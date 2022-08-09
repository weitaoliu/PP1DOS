from lxml import etree  # to read xml files
import numpy as np
import matplotlib.pyplot as plt
from csv import writer  # to output data as a csv file
import timeit  # used to record the computational time used for the program/codes
from processingInterface import *  # used to incorporate external interface file
#  (https://stackoverflow.com/questions/924700/best-way-to-retrieve-variable-values-from-a-text-file)
import os  # imported here to change the working directory, .cvs and figures will be saved in that directory

codeStart = timeit.default_timer()


class xmlDataSet(object):

    def __init__(self, fileDataset):

        self.datasetPath = fileDataset
        # to read data from fileDataset, to get the data along the distance
        self.simResults = etree.parse(self.datasetPath)  # read xml files and then save as self.simResults variable
        self.profileAllInList = []
        self.getProfileData()  # it is used to fill in profileAllInList
        # the above function is used here to store post-processed data and to avoid repeated processing

        # ----Function1: getBasics()----
        self.basicVariable = None
        self.tempString = None  # used in getBasics(self, tagName) function
        self.basicStringContainer = None  # used in getBasics() function for storing strings (having ' ')
        self.sizeOfBasicAllInContainer = None  # getBasics(), used here to store all strings (without ' ')
        self.basicAllInContainer = None  # getBasics(), used here to store all strings (without ' ')
        self.sizeOfbasicVariable = None  # to get size of a tagName (the first element), ie, 11 for "additional" tag
        self.sizeOfbasicStringContainer = None  # to get the size of basic string container
        # -------------------------------

        # ----Function2: getBasics()----
        self.basic4NameContainer = None  # to get the name of variables and species, 11 in total
        self.basicIndexFromName = None  # to get the index for each variable and species, 0-10
        self.basic4IndexContainer = None  # to get the index x%3 == 2, the third one, index number
        self.basic4InfoContainer = None  # x%3 = 1, the middle information, ie, units
        self.basicsCombinedContainer = None  # all stored information, = 3 times size of info or name or index
        # ------------------------------

        # ----Function3: getNumOfGrids()
        #  in the profile-size tag, there are two numbers: gridNumber and numOfVariables
        self.profileSize = None  # accessing using tagName: profile-size
        self.emptyString = None  # used here to generate new string, appended from NULL
        self.tempList = None  # used to store a list
        self.profileSizeContainer = None
        self.numOfGrids = None  # representing the number of grids in results
        # ------------------------------

        # ----Function4: getProfileData()
        self.profileData = None  # crude profile data
        self.lenOfProfileData = None  # size of all dataset
        self.lenOfTempList = None  # the length all dataset
        self.lenOfTempList_x = None  # length for each element, separately by ' ' (ie, white space)
        # -------------------------------

    # ! this function can access variables in getProperties(self,index).
    # ! here note that tagName is pre-defined in the .xml file, so we need to read them get access data.(07.08.2022)
    # ! use xml online viewer to check /n or other characters in files. (https://jsonformatter.org/xml-viewer)
    def getBasics(self, tagName):
        self.basicVariable = self.simResults.find(tagName)
        self.sizeOfbasicVariable = len(self.basicVariable.text)

        self.tempString = ''  # the NULL character is used to avoid influencing accessing stored strings
        self.basicStringContainer = []  # initialize the string container
        for x in range(1, self.sizeOfbasicVariable):
            if self.basicVariable.text[x] != '\n':
                self.tempString += self.basicVariable.text[x]
            else:
                # print(self.tempString)
                self.basicStringContainer.append(self.tempString)
                self.tempString = ''

        # in a "XXX" tag (e.g., "additional"), the first element refers to the size, the following
        # codes aim to re-organized them into three parts: (1) variable (2) unit or MW (3) index
        self.sizeOfbasicStringContainer = int(self.basicStringContainer[0])
        # to delete the first element,ie, the size of container
        del self.basicStringContainer[0]

        self.basicAllInContainer = []  # initialize an empty container having all three information,
        # ie, name, unit, and index.

        # note the third line, ' ' is used since different strings ara separately by a white space and here the code
        # is used these to identify right name or strings for each group.
        for x in range(0, self.sizeOfbasicStringContainer):
            for y in range(len(self.basicStringContainer[x])):
                if self.basicStringContainer[x][y] != ' ' and y != len(self.basicStringContainer[x]) - 1:
                    self.tempString += self.basicStringContainer[x][y]
                elif y == len(self.basicStringContainer[x]) - 1:
                    self.tempString += self.basicStringContainer[x][y]
                    self.basicAllInContainer.append(self.tempString)
                    self.tempString = ''
                else:
                    self.basicAllInContainer.append(self.tempString)
                    self.tempString = ''
        self.sizeOfBasicAllInContainer = len(self.basicAllInContainer)

        return self.basicAllInContainer

    # ! NOTE: below three getBasics4XXXX use above getBasics() function
    # -------------------------------------------------------------------
    def getBasics4Name(self):
        self.basic4NameContainer = []
        self.basicsCombinedContainer = self.getBasics(
            'additional') + self.getBasics('mass-fractions')
        for x in range(0, len(self.basicsCombinedContainer)):
            if x % 3 == 0:
                self.basic4NameContainer.append(
                    self.basicsCombinedContainer[x])
        return self.basic4NameContainer

    # units information for variables, MW for species
    def getBasics4Info(self):
        self.basic4InfoContainer = []
        self.basicsCombinedContainer = self.getBasics(
            'additional') + self.getBasics('mass-fractions')
        for x in range(0, len(self.basicsCombinedContainer)):
            if x % 3 == 1:
                self.basic4InfoContainer.append(
                    self.basicsCombinedContainer[x])
        return self.basic4InfoContainer

    # to get the index for each variable and species
    def getBasics4Index(self):
        self.basic4IndexContainer = []
        self.basicsCombinedContainer = self.getBasics(
            'additional') + self.getBasics('mass-fractions')
        for x in range(0, len(self.basicsCombinedContainer)):
            if x % 3 == 2:
                self.basic4IndexContainer.append(
                    int(self.basicsCombinedContainer[x]))
        return self.basic4IndexContainer

    # NOTE: following codes is to find corresponding info between above three functions or containers
    def getBasicsIndexFromName(self, tagName):
        self.basicIndexFromName = -1
        for x in range(0, len(self.getBasics4Name())):
            if self.getBasics4Name()[x] == tagName:
                self.basicIndexFromName = x
        if self.basicIndexFromName == -1:
            print('Something wrong with the tag name, please check it again!')
            exit()
        return self.basicIndexFromName

    # -------------------------------------------------------------------

    def getNumOfGrids(self):
        self.profileSize = self.simResults.find('profiles-size')
        self.emptyString = ''
        self.tempList = []
        for x in range(1, len(self.profileSize.text)):
            # first step is to remove the '\n'
            if self.profileSize.text[x] != '\n':
                self.emptyString += self.profileSize.text[x]

            else:
                self.tempList.append(self.emptyString)
                self.emptyString = ''
        # print (self.tempList) # used for checking codes

        # NOTE: len(self.tempList) is used to detect how many lines (ie, \n)
        # while len(self.tempLists[x]) is used to calculate how many characters
        # in the x line. BUT here only one line exists, the first refers to number of
        # grids and the second one is the sum of basic variables and species.
        # There, here 0 is used for directly accessing the first line instead of detections.
        self.profileSizeContainer = []
        for x in range(len(self.tempList[0])):
            if self.tempList[0][x] != ' ':
                self.emptyString += self.tempList[0][x]
            else:
                self.profileSizeContainer.append(self.emptyString)
                break
        self.numOfGrids = int(self.profileSizeContainer[0])
        # print (self.numOfGrids) # used to check codes
        return self.numOfGrids

    # ----------------------------------------------------------------------------------------------#
    # !!! NOTE ----------------- the most important part, to get the profile data ----------------- #
    # ----------------------------------------------------------------------------------------------#
    def getProfileData(self):
        self.profileData = self.simResults.find('profiles')
        self.emptyString = ''
        self.tempList = []
        self.lenOfProfileData = len(self.profileData.text)
        for x in range(1, self.lenOfProfileData):
            if self.profileData.text[x] != '\n':
                self.emptyString += self.profileData.text[x]
            else:
                self.tempList.append(self.emptyString)
                self.emptyString = ''

        # NOTE: to create a container called tempAllInList, containing all data from profiles tag
        self.lenOfTempList = len(self.tempList)

        for x in range(0, self.lenOfTempList):
            self.lenOfTempList_x = len(self.tempList[x])
            for y in range(0, self.lenOfTempList_x):
                if self.tempList[x][y] != ' ' and y != self.lenOfTempList_x - 1:
                    self.emptyString += self.tempList[x][y]
                elif y == self.lenOfTempList_x - 1:
                    self.emptyString += self.tempList[x][y]
                    self.profileAllInList.append(float(self.emptyString))
                    self.emptyString = ''
                else:
                    self.profileAllInList.append(float(self.emptyString))
                    self.emptyString = ''
        # the value of the list has been stored in profileAllInList; it is now in __int__ function.

        #  -----------------------------------------------------------------------------------------#
        #  Below codes are commented since it is ineffective to postprocess all data, but just      |
        #  use only one of them via the tagName. This is because to get each variable's data, we    |
        #  need to call process all data, that is wasteful!!!                                       |
        #  A more wise way is to post-process once, store them to a big List, then use the List.    |
        # |----------------------------------Commented from-----------------------------------------|
        # | # NOTE: to convert string to float data                                                 |
        # | self.lenOftempAllInList = len(self.tempAllInList)                                       |
        # | for x in range (self.lenOftempAllInList):                                               |
        # |     self.tempAllInList[x] = float(self.tempAllInList[x])                                |
        # | # NOTE: to get number of variables (including temperature and species)                  |
        # | # the following function is based on:                                                   |
        # | #----$ size of profile data = num of grids x num of variables $------#                  |
        # | self.numOfVariables = int(self.lenOftempAllInList/self.getNumOfGrids())                 |
        # | self.targetList = []                                                                    |
        # | self.targetIndex = -1                                                                   |
        # | # NOTE: step 1. to get the targetName and its index                                     |
        # | for x in range(0, len(self.getBasics4Name())):                                          |
        # |     if self.getBasics4Name()[x] == targetVariable:                                      |
        # |         self.targetIndex = x                                                            |
        # |         break                                                                           |
        # | if self.targetIndex == -1:                                                              |
        # |     print ('Something wrong with the variable name, please check again!')               |
        # |     exit()                                                                              |
        # | # NOTE: step 2. to re-organize the self.tempAllInList                                   |
        # | for x in range (self.targetIndex,self.lenOftempAllInList, self.numOfVariables):         |
        # |     self.targetList.append(self.tempAllInList[x])                                       |
        # |                                                                                         |
        # | return self.targetList                                                                  |
        # ------------------------------------------------------------------------------------------#

    # -----------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------#
# ------------------------------a child class: basicData(xmlDataSet)--------------------------------#
# --------------------------------------------------------------------------------------------------#
# - create a child class which inherits from xmlDataSet; xmlDataSet is used to create a container   #
# - self.profileAllInList, which contains all profile (along distance) information of variables.    #
# - the child class, basicData(xmlDataSet) is used to extract basic information from the base class #
# ------------------------------------------------------------------------------------------------- #


class basicData(xmlDataSet):

    def __init__(self, fileDataset):
        super().__init__(fileDataset)
        self.pressure = None
        self.mixMW = None
        self.densityList = None
        self.temperatureList = None
        self.distanceList = None
        self.localMW = None
        self.tagIndex = None
        self.numOfVariables = None  # to know how many variables
        self.localIndex = None  # used to identify the first index for target data
        self.targetDataList = None  # used to contain the data of target variables

    def getTargetDataViaTagName(self, tagName):

        self.localIndex = -1
        self.targetDataList = []
        for x in range(len(self.getBasics4Name())):
            if self.getBasics4Name()[x] == tagName:
                self.localIndex = x
                break
            elif x == (len(self.getBasics4Name()) - 1) and self.getBasics4Name()[x] != tagName:
                print('Something wrong with the tagName, please check it again!')
                exit()
        # to get the num of variables
        self.numOfVariables = int(
            len(self.profileAllInList) / self.getNumOfGrids())
        for x in range(self.localIndex, len(self.profileAllInList), self.numOfVariables):
            self.targetDataList.append(self.profileAllInList[x])

        return self.targetDataList

    # below function is used to get the MW for each target species
    def getMW(self, tagName):

        self.localMW = -1
        self.tagIndex = -1
        for x in range(len(self.getBasics4Name())):
            if self.getBasics4Name()[x] == tagName:
                self.tagIndex = x
                break
            elif x == len(self.getBasics4Name()) - 1 and self.getBasics4Name()[x] == tagName:
                print('Something wrong with the input, please check it again!')
                exit()

        self.localMW = float(self.getBasics4Info()[self.tagIndex])

        return self.localMW

    # -------------------------------------------------------------------

    def getDistance(self, unit):

        self.distanceList = self.getTargetDataViaTagName(
            'axial-coordinate')

        if self.getBasics4Info()[self.getBasicsIndexFromName('axial-coordinate')] == '[cm]':
            if unit == 'mm':
                for x in range(len(self.distanceList)):
                    self.distanceList[x] *= 10

                self.getBasics4Info()[self.getBasicsIndexFromName(
                    'axial-coordinate')] = '[mm]'

            if unit == 'm':
                for x in range(len(self.distanceList)):
                    self.distanceList[x] /= 10

                self.getBasics4Info()[self.getBasicsIndexFromName(
                    'axial-coordinate')] = '[m]'

        elif self.getBasics4Info()[self.getBasicsIndexFromName('axial-coordinate')] == '[mm]':
            if unit == 'cm':
                for x in range(len(self.distanceList)):
                    self.distanceList[x] /= 10

                self.getBasics4Info()[self.getBasicsIndexFromName(
                    'axial-coordinate')] = '[cm]'

            if unit == 'm':
                for x in range(len(self.distanceList)):
                    self.distanceList[x] /= 100

                self.getBasics4Info()[self.getBasicsIndexFromName(
                    'axial-coordinate')] = '[mm]'

        return self.distanceList

    def getTemperature(self):
        self.temperatureList = self.getTargetDataViaTagName('temperature')

        return self.temperatureList

    def getDensity(self):
        self.densityList = self.getTargetDataViaTagName('density')

        return self.densityList

    def getMixMW(self):
        self.mixMW = self.getTargetDataViaTagName('mol-weight')

        return self.mixMW

    def getPressure(self):
        self.pressure = self.getTargetDataViaTagName('pressure')

        return self.pressure


# ------------------------------------------------------------------------------------------------- #
# -------------------------a child of child class: sootData(basicData)----------------------------- #
# ------------------------------------------------------------------------------------------------- #
# - the basicData class has generated basic data, like distance and temperature and created         #
# - accessing functions like getMW('tagName') and get getTargetDataViaTagName('tagName'). All these #
# - will be then used in sootData class to generate soot data based these basic info and functions  #
# ------------------------------------------------------------------------------------------------- #


class sootData(basicData):
    def __init__(self, fileDataset):
        super().__init__(fileDataset)
        # ----
        self.numOfBINs = -1  # used to identify the total num of BINs in the mechanism
        self.indexOfBINsList = []  # NOTE: here the calculating the index starts from 0
        self.nameOfBINsList = []

        self.nameOfBINsDetectList = []  # used to contain the name of BINs
        self.indexOfBINsDetectList = []  # used here to store the index (in getBasics4Name() ) of BINs

        self.getListOfBINs()  # used to update above variables

        self.localIndex4BIN = None  # local index for BINs
        self.localEffectNumOfBINs = None  # effective number after removing some small BINs
        self.localSVFBINDect = None
        self.SVFBINDectList = None
        self.localNumOfVariables = None
        self.localNumOfGrids = None
        self.BINData = None
        self.sootDensity = None
        self.BINDetectList = None
        self.localBINData = None
        self.localSootVFList = None
        self.localDensity = None
        self.localNameOfBINsList = None  # used to store the name for each BIN
        self.localIndexOfBINsList = None  # used to store the corresponding BIN index in the list
        # ----

    def getListOfBINs(self):

        self.localIndexOfBINsList = []
        self.localNameOfBINsList = []
        for x in range(len(self.getBasics4Name())):
            if 'BIN' in self.getBasics4Name()[x]:
                self.localIndexOfBINsList.append(x)
                self.localNameOfBINsList.append(self.getBasics4Name()[x])

        self.indexOfBINsList = self.localIndexOfBINsList
        self.nameOfBINsList = self.localNameOfBINsList
        self.numOfBINs = len(self.localIndexOfBINsList)

        for x in range(self.numOfBINs):
            self.nameOfBINsDetectList.append(self.nameOfBINsList[x])
            self.indexOfBINsDetectList.append(self.indexOfBINsList[x])

    def getSootVF(self):

        # the equation of soot volume fraction is based on following equation   #
        # soot volume fraction = sum of ((Y_BIN) * (rho_mixtures) / (rho_soot)) #
        self.localDensity = self.getDensity()  # to generate density dataset
        self.localSootVFList = [0] * self.getNumOfGrids()
        for x in range(self.numOfBINs):
            self.localBINData = self.getTargetDataViaTagName(self.nameOfBINsList[x])
            for y in range(self.getNumOfGrids()):
                self.localSootVFList[y] += self.localBINData[y] * self.localDensity[y] / 1800.0
            # self.localSootVFList += self.localSootVFList

        return self.localSootVFList

        # ----------------------NOTE: Aims of this function - 04.07.2022-----------------------------#
        # it is not efficient to call self.getTargetDataViaTagName() for each BIN, since the programme
        # needs to post-process the profileAllInList[] for each BIN. The cost becomes unaffordable 
        # when dealing with large number of BINs and grids. 
        # Therefore, the purpose of this function is to post-process profileAllInList[] for all BINs 
        # avoiding to over call the self.getTargetDataViaTagName() function. Meantime, the BINNum is
        # taken as an argument to consider the BIN cut effects on soot volume fraction. 
        # --------------------------------------------------------------------------------------------#

        # step1: to get list of BIN index and its corresponding name list
        # this has been done via class initialization ie, self.indexOfBINsList and self.nameOfBINsList

        # step2: to detect if considering the BINnum for post-processing SVF and the get a list for the 
        # BIN data (mass fraction) in "profile" tag. NOTE: Just one list for all desired BIN data

    def BINDetect(self, BINNum):

        self.BINDetectList = []
        if BINNum > 0:
            for x in range(0, BINNum):
                if x < 9:
                    self.BINDetectList.append('-0' + str(x + 1))
                else:
                    self.BINDetectList.append('-' + str(x + 1))

            for x in range(self.numOfBINs):
                for y in range(0, BINNum):
                    if self.BINDetectList[y] in self.nameOfBINsList[x]:
                        self.nameOfBINsDetectList.remove(self.nameOfBINsList[x])
                        self.indexOfBINsDetectList.remove(self.indexOfBINsList[x])

            # print(self.nameOfBINsDetectList)
            # print(self.indexOfBINsDetectList)

    def getSVFBINDect(self, sootDensity):
        self.sootDensity = sootDensity
        self.localDensity = self.getDensity()
        self.BINData = []
        self.localNumOfGrids = self.getNumOfGrids()
        self.localNumOfVariables = int(len(self.profileAllInList) / self.localNumOfGrids)
        for x in range(self.localNumOfGrids):
            for y in range(len(self.nameOfBINsDetectList)):
                self.localIndex4BIN = x * self.localNumOfVariables + self.indexOfBINsDetectList[y]
                self.BINData.append(self.profileAllInList[self.localIndex4BIN])

        self.SVFBINDectList = [0] * self.localNumOfGrids
        self.localSVFBINDect = 0
        self.localEffectNumOfBINs = int(len(self.BINData) / self.localNumOfGrids)
        for x in range(self.localNumOfGrids):
            for y in range(len(self.indexOfBINsDetectList)):
                self.localIndex4BIN = y + x * self.localEffectNumOfBINs
                self.SVFBINDectList[x] += (self.BINData[self.localIndex4BIN] * self.localDensity[x] / self.sootDensity)

        return self.SVFBINDectList


# TODO: add new classes for outputting the SVF or other variables when using CRECK mechanism


# TODO: should make the interface for above codes:

# ---- Here reading the interface file for above classes via processingInterface.py

os.chdir(workingDir)  # firstly, change to desired working directory

# ---- to create the object holding the dataset
if mechanismFormat == 'SYD':
    if not ifProcessSVF:
        dataObject = basicData(filePathway)
    if ifProcessSVF:
        dataObject = sootData(filePathway)
# elif mechanismFormat == 'CRECK':
#     if ifAlreadySVF:

# ---- finished, ! NOTE that a new class will be added for outputting CRECK soot dataset

# ---- to write the desired variables to .cvs file
# -- get the distance
if '[mm]' in basicOutputList[0]:
    distance = dataObject.getDistance('mm')
elif '[cm]' in basicOutputList[0]:
    distance = dataObject.getDistance('cm')
elif '[m]' in basicOutputList[0]:
    distance = dataObject.getDistance('m')
else:
    distance = []
    print('Something wrong with distance, please check again!')
    exit()

distance.insert(0, basicOutputList[0])  # set the header
# --

# -- get the temperature
temperature = dataObject.getTemperature()
temperature.insert(0, basicOutputList[1])
# --

# -- get the density
density = dataObject.getDensity()
density.insert(0, basicOutputList[2])
# --

# -- get the pressure
pressure = dataObject.getPressure()
pressure.insert(0, basicOutputList[3])
# --
basicVariables = [distance, temperature, density, pressure]
# -- to get the other variables' dataset (such as species)
otherVariables = []
for x in range(len(otherOutputList)):
    if otherOutputList[x] not in dataObject.getBasics4Name():
        print('Something wrong with the variable name, please check it again!')
        print('The problem comes from the name: ' + otherOutputList[x])
        exit()

    else:
        localData = dataObject.getTargetDataViaTagName(otherOutputList[x])
        localData.insert(0, otherOutputList[x])
        otherVariables.append(localData)
        localData = []
# --

# -- to get soot-related variables' dataset
dataObject.BINDetect(BINRemoveFrom)
sootVF = dataObject.getSVFBINDect(sootDensityUSD)
sootVF.insert(0, 'soot volume fraction')

if ifOutputVariables:
    with open(nameOfFile, 'w') as fd:
        csv_writer = writer(fd, delimiter=',')
        csv_writer.writerows(zip(*basicVariables, *otherVariables, sootVF))
        fd.write("\n")

# to use plot for preview the data
plt.plot(distance[1:], temperature[1:])
plt.show()


# plt.plot(test.getDistance('mm'),test.getSootVF())
# plt.show()

# print(text.getDistance('mm'))
# print(text.getTemperature())


# ---- END PART ----
codeStop = timeit.default_timer()
print('------------------------------------------------------------------')
print('  Computational time used for above codes: ', codeStop - codeStart, 's')
print('------------------------------------------------------------------')
