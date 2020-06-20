"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.

This file defines global setting parameters and useful folder/file paths.
50Vx50V scan window, 300x300 resolution by default.
"""
import numpy as np
naiveScale = 1000 # The original data in txt files are in unit V. We need to convert them to mV here for convenience.

"""
comsolScale = 3.5*10 for diffusion. 3.5 is the default calibrated coefficient,
    10 is multiplied to fit the signal amplification of lock-in.
comsolScale=  3.5/1000*125 for TR-iMIM signals. 3.5 is still default calibrated coefficient, factor of 125/1000 is
    multiplied since 3.5 is for a 1000x DC amplifier, while TR-iMIM uses the amplifier with 125x instead.
"""

trCOMSOLScale = 3.5/1000*125
diffusionCOMSOLScale = 3.5*10

saveFigPath = "../../Perovskite/imgs/"
diffusionCOMSOLCSV="../../Perovskite/simulation_Im_Re_curve/Untitled_R28_1degree.csv"
trCOMSOLCSV="../../Perovskite/simulation_Im_Re_curve/tr2.csv"

intensityListForPhaseDiagram = ["00004","00007","00013","00022","00044","00073"] #00007 is excluded due to a bad line

rootPath = '../../Perovskite/1.1/1.1_50Vx50V/201912/pos2/'

# rootPath = '../../Perovskite\HTL_ETL\HTL_firstBatchAfterStayAtHome/20200617/'
# intensityListForPhaseDiagram = ["00004","00044","00073"]

fileNameIm = 'Ch2 retrace.txt' # channel 2 for im signal for the perovskite experiment. Check it before set it.
fileNameRe = 'Ch1 retrace.txt' # same thing
folderPathList = [rootPath+intensity for intensity in intensityListForPhaseDiagram]

"""
x_extra_shift_list and y_extra_shift_list are for manually determining centers for diffusions.
You may adjust them for different measurements accordingly.
"""
x_extra_shift_list = np.array([0.27,0.09,-0.2,-0.3,0.0-0.45,-0.75-0.45])
y_extra_shift_list = np.array([-0.55,0.75,0.4,0.5,0.0+0.25,-0.25-0.05])
