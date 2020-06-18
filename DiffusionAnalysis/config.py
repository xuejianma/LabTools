"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.

This file defines global setting parameters and useful folder/file paths.
"""

"""
scale = 3.5*10 for diffusion. 3.5 is the default calibrated coefficient,
    10 is multiplied to fit the signal amplification of lock-in.
scale=  3.5/1000*125 for TR-iMIM signals. 3.5 is still default calibrated coefficient, factor of 125/1000 is
    multiplied since 3.5 is for a 1000x DC amplifier, while TR-iMIM uses the amplifier with 125x instead.
"""
trCOMSOLScale = 3.5/1000*125
diffusionCOMSOLScale = 3.5*10

saveFigPath = "../../Perovskite/imgs/"
diffusionCOMSOLCSV="../../Perovskite/simulation_Im_Re_curve/Untitled_R28_1degree.csv"
trCOMSOLCSV="../../Perovskite/simulation_Im_Re_curve/tr2.csv"

intensityListForPhaseDiagram = ["00000","00004","00013","00022","00044","00073"] #00007 is excluded due to a bad line
rootPath = '../../Perovskite/1.1/1.1_50Vx50V/201912/pos2/'
fileNameIm = 'Ch2 retrace.txt' # channel 2 for im signal for the perovskite experiment. Check it before set it.
fileNameRe = 'Ch1 retrace.txt' # same thing
folderPathList = [rootPath+intensity for intensity in intensityListForPhaseDiagram]