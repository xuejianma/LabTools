"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.
"""
from utils import mim2Conductivity
from config import fileNameIm,fileNameRe,folderPathList,diffusionCOMSOLCSV,diffusionCOMSOLScale,naiveScale

for ind,folderPath in enumerate(folderPathList):
    print("Ongoing Conversion: "+str(ind+1)+"/"+str(len(folderPathList)))
    mim2Conductivity(folderPath, fileNameIm, fileNameRe, csvFilePath=diffusionCOMSOLCSV, \
                     comsolScale=diffusionCOMSOLScale,naiveScale=naiveScale)
print("Conversion to conductivities DONE!")