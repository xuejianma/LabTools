"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.
"""
from utils import plotPhaseAndSimulatedCurves,readImRePhase,readSimulatedImReCSV,plotSimulatedImReCurves
saveFigPath = "../../Perovskite/imgs/"
diffusionCOMSOLCSV="../../Perovskite/simulation_Im_Re_curve/Untitled_R28_1degree.csv"
diffusionCOMSOLScale = 3.5*10
intensityListForPhaseDiagram = ["00000","00004","00013","00022","00044","00073"] #00007 is excluded due to a bad line
folderPath = '../../Perovskite/1.1/1.1_50Vx50V/201912/pos2/'
imFileName = 'Ch2 retrace.txt' # channel 2 for im signal for the perovskite experiment. Check it before set it.
reFileName = 'Ch1 retrace.txt' # same thing
filePathImList = [folderPath+intensity+'/'+imFileName for intensity in intensityListForPhaseDiagram]
filePathReList = [folderPath+intensity+'/'+reFileName for intensity in intensityListForPhaseDiagram]

im_all, re_all = readImRePhase(filePathImList,filePathReList,scale=1000)
cond_array, im_sim, re_sim = readSimulatedImReCSV(diffusionCOMSOLCSV,scale=diffusionCOMSOLScale)
plotPhaseAndSimulatedCurves(im_all,re_all,im_sim, re_sim,saveFigPath)
plotSimulatedImReCurves(diffusionCOMSOLCSV, saveFigPath,scale=diffusionCOMSOLScale)