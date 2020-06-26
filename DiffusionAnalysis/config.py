"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.

This file defines global setting parameters and useful folder/file paths.
50Vx50V scan window, 300x300 resolution by default.
This project was initially written with jupyter notebook. Please check Im_Re_Phase_Diagram.ipynb for any information
and extra (mostly useless) functions.
IMPORTANT: PLEASE RUN THE FILES WITH SUFFIX "_preRun.py" FOR THE FIRST TIME!!! (convert2Unskewed_preRun.py is not
compulsory if you set unskewFlag = 0 in this file. Check it for more information)
"""
import os
import numpy as np

"""
rootPath records:
'../../Perovskite/1.1/1.1_50Vx50V/201912/pos2/'
'../../Perovskite/HTL_ETL/HTL_firstBatchAfterStayAtHome/20200617'
"""
rootPath = '../../Perovskite/1.1/1.1_50Vx50V/201912/pos2/'
savePath = rootPath+"/processFiles/"
if not os.path.exists(savePath):
    os.mkdir(savePath)
# if not os.path.exists(savePath+"/diffusion_simulation_database.pickle"):
#     print("\n[WARNING: You may run diffusionSimulations_preRun.py for the first time to get diffusion_simulation_database.pickle.]")

naiveScale = 2300 # The original data in txt files are in unit V. We need to convert them to mV here for convenience.

"""
comsolScale = 3.5*10 for diffusion. 3.5 is the default calibrated coefficient,
    10 is multiplied to fit the signal amplification of lock-in.
comsolScale=  3.5/1000*125 for TR-iMIM signals. 3.5 is still default calibrated coefficient, factor of 125/1000 is
    multiplied since 3.5 is for a 1000x DC amplifier, while TR-iMIM uses the amplifier with 125x instead.
"""

trCOMSOLScale = 3.5/1000*125
diffusionCOMSOLScale = 3.5*10

diffusionCOMSOLCSV="../../Perovskite/simulation_Im_Re_curve/Untitled_R28_1degree.csv"
trCOMSOLCSV="../../Perovskite/simulation_Im_Re_curve/tr2.csv"

intensityListForPhaseDiagram = ["00004","00007","00013","00022","00044","00073"] #00007 is excluded due to a bad line
power_label = ["1.0x10² mW/cm²","3.0x10² mW/cm²","8.0x10² mW/cm²","20x10² mW/cm²","50x10² mW/cm²","100x10² mW/cm²"]
power_list =[100,300,800,2000,5000,10000]


# rootPath = '../../Perovskite\HTL_ETL\HTL_firstBatchAfterStayAtHome/20200617/'
# intensityListForPhaseDiagram = ["00004","00044","00073"]

fileNameIm = 'Ch2 retrace.txt' # channel 2 for im signal for the perovskite experiment. Check it before set it.
fileNameRe = 'Ch1 retrace.txt' # same thing
folderPathList = [rootPath+'/'+intensity for intensity in intensityListForPhaseDiagram]

"""
x_extra_shift_list and y_extra_shift_list are for manually determining centers for diffusions.
You may adjust them for different measurements accordingly.
x:-value~right; +value~left
y:-value~up; +value~down
Hisotry records:
    Perovskite Sample in '../../Perovskite/1.1/1.1_50Vx50V/201912/pos2/':
        x_extra_shift_list = np.array([0.27,0.09,-0.2,-0.3,0.0-0.45,-0.75-0.45])+np.asarray([-0.76276169,-0.45913387,-0.15354331,-0.15354331, 0.,2.36675187])
        y_extra_shift_list = np.array([-0.55,0.75,0.4,0.5,0.0+0.25,-0.25-0.05])+np.asarray([ 1.05682016,-0.45771987,-0.91839836,-0.15224807,-0.6109478,1.05682016])
    HTL Sample
        x_extra_shift_list = np.array([0.75,0,0.75,0,0,0.5])
        y_extra_shift_list = np.array([0,0.5,0.5,0,-0.25,0.5])
"""
x_extra_shift_list = np.array([0.27, 0.09, -0.2, -0.3, 0.0 - 0.45, -0.75 - 0.45]) + np.asarray(
    [-0.76276169, -0.45913387, -0.15354331, -0.15354331, 0., 2.36675187])
y_extra_shift_list = np.array([-0.55, 0.75, 0.4, 0.5, 0.0 + 0.25, -0.25 - 0.05]) + np.asarray(
    [1.05682016, -0.45771987, -0.91839836, -0.15224807, -0.6109478, 1.05682016])

"""
Usually we set unskewFlag = 0. If you consider yourself a perfectionist, try set unskewFlag = 1, and change skew 
parameters in convert2Unskewed_preRun.py. Run it first. It takes a while. Then the program will extract unskewed coordinates with 
calibratedUnskewedCoords.py. The parameters in convert2Unskewed_preRun.py could be changed by test and error in playground_skew.py. 
Remember, that is just a playground to test influcences of different parameters. Eventually you should change them in 
convert2Unskewed_preRun.py and rerun the file, which again, takes a while.
"""
unskewFlag = 0