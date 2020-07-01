"""
Created by Xuejian Ma at 6/19/2020.
All rights reserved.
"""
import numpy as np
import matplotlib.pyplot as plt
from config import unskewFlag,angleSteps
from utils import radialAverageByLinecuts
if unskewFlag == 0:
    from calibratedCoords import im_img_all_cropped, re_img_all_cropped, x_list_all_cropped, y_list_all_cropped, \
        conductivity_all_cropped
else:
    from calibratedUnskewedCoords import im_img_all_cropped, re_img_all_cropped, x_list_all_cropped, y_list_all_cropped, \
        conductivity_all_cropped

rList_all = []
zList_all = []
plt.figure()
for ind, graph in enumerate(conductivity_all_cropped):
    #    plt.figure(figsize = (5,5))
    xx, yy = np.meshgrid(x_list_all_cropped[ind], y_list_all_cropped[ind])
    #    plt.scatter(0,0,s=100)
    #    plt.pcolormesh(xx,yy,graph)
    #     rList,zList = radialAverage(graph,(0,0),xx,yy,radialSteps=300,threshold=1/6,angleSteps=2)
    #     rList,zList,rDict = radialAverageByLines(graph,(0,0),xx,yy,radialSteps=300,threshold=1/6*1,angleSteps=10)
    rList, zList, rDict = radialAverageByLinecuts(graph, (0, 0), xx, yy, radialSteps=300, threshold=1 / 6 * 1,
                                                  angleSteps=angleSteps)
    rList_all.append(rList)
    zList_all.append(zList)
    if ind == 0 :
        print('\n[NOTICE: you may see "RuntimeWarning: Mean of empty slice". It is due to the averaging mechanism I '
              'wrote in function radialAverageByLinecuts.\n I did not debug it as it works, and you can try if you '
              'want, as it could help you understand how radialAverageByLinecuts is implemented.]\n')
    print("Averaging Radial Linecuts Ongoing: ",ind+1,"/",len(conductivity_all_cropped))
#    plt.plot(rList,zList)
