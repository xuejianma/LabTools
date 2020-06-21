"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.
"""
from utils import plotPhaseAndSimulatedCurves,readImRePhase,readSimulatedImReCSV,plotSimulatedImReCurves,\
                    plotSimulatedImReCurves_Linear
from config import naiveScale,diffusionCOMSOLScale,savePath,diffusionCOMSOLCSV,trCOMSOLCSV,trCOMSOLScale,folderPathList,\
                    fileNameIm,fileNameRe


im_all, re_all = readImRePhase(folderPathList,fileNameIm,fileNameRe,naiveScale=naiveScale)
cond_array, im_sim, re_sim = readSimulatedImReCSV(diffusionCOMSOLCSV,comsolScale=diffusionCOMSOLScale)
plotPhaseAndSimulatedCurves(im_all,re_all,im_sim, re_sim,savePath)

plotSimulatedImReCurves(diffusionCOMSOLCSV, savePath,comsolScale=diffusionCOMSOLScale)#for iMIM diffusion

# plotSimulatedImReCurves(trCOMSOLCSV, savePath,comsolScale=trCOMSOLScale) #for TR-iMIM
# plotSimulatedImReCurves_Linear(trCOMSOLCSV, savePath,comsolScale=trCOMSOLScale) #for TR-iMIM
