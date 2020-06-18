"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.
"""
from utils import plotPhaseAndSimulatedCurves,readImRePhase,readSimulatedImReCSV,plotSimulatedImReCurves,\
                    plotSimulatedImReCurves_Linear
from config import diffusionCOMSOLScale,saveFigPath,diffusionCOMSOLCSV,trCOMSOLCSV,trCOMSOLScale,folderPathList,\
                    fileNameIm,fileNameRe


im_all, re_all = readImRePhase(folderPathList,fileNameIm,fileNameRe,scale=1000)
cond_array, im_sim, re_sim = readSimulatedImReCSV(diffusionCOMSOLCSV,scale=diffusionCOMSOLScale)
plotPhaseAndSimulatedCurves(im_all,re_all,im_sim, re_sim,saveFigPath)

plotSimulatedImReCurves(diffusionCOMSOLCSV, saveFigPath,scale=diffusionCOMSOLScale)#for iMIM diffusion

# plotSimulatedImReCurves(trCOMSOLCSV, saveFigPath,scale=trCOMSOLScale) #for TR-iMIM
# plotSimulatedImReCurves_Linear(trCOMSOLCSV, saveFigPath,trCOMSOLScale) #for TR-iMIM
