"""
Created by Xuejian Ma at 6/21/2020.
All rights reserved.
"""
import numpy as np
import matplotlib.pyplot as plt
# from readConductivities import im_img_all,re_img_all
from utils import radialAverageByLinecuts
from config import unskewFlag
from playground_plotLaserShape import laserimg_cropped,laser_X_cropped,laser_Y_cropped
from fitDiffusion import xtemp,ztemp
from config import savePath
if unskewFlag == 0:
    from calibratedCoords import im_img_all, re_img_all, x_list_all, y_list_all, \
        conductivity_all
else:
    from calibratedUnskewedCoords import im_img_all, re_img_all, x_list_all, y_list_all, \
        conductivity_all

laser_rList,laser_zList,laser_rDict = radialAverageByLinecuts(laserimg_cropped,(0,0),laser_X_cropped,laser_Y_cropped,radialSteps=300,threshold=1/6*1,angleSteps=10)
SMALL_SIZE = 8
MEDIUM_SIZE = 14
BIGGER_SIZE = 18

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('axes', linewidth=1.5)
plt.rc('xtick.major',size=3,width=2)
plt.rc('ytick.major',size=3,width=2)
plt.rc('xtick.minor',size=2,width=1)
plt.rc('ytick.minor',size=2,width=1)

# import pickle
# with open('./skewed_data.pickle','rb') as f:
#     x_list_all_cropped,y_list_all_cropped,conductivity_all_cropped,\
#                  im_img_all_cropped,re_img_all_cropped = \
#     pickle.load(f)

ind = 3
X,Y = np.meshgrid(x_list_all[ind],y_list_all[ind])


im_img = im_img_all[ind].copy()[:,:-1]
# plt.pcolormesh(X,Y,im_img)
# plt.axes().set_aspect(1)
# plt.xlim(-15,15)
# plt.ylim(-15,15)

im_rList,im_zList,_ = radialAverageByLinecuts(im_img,(0,0),X,Y,radialSteps=300,threshold=1/6*1,angleSteps=10)
plt.figure(figsize=(7,4))
plt.plot(im_rList,im_zList,'o',alpha=0.5,color='red',label='iMIM-Im')
plt.xlim(-15,15)

re_img = re_img_all[ind].copy()[:,:-1]
# plt.pcolormesh(X,Y,re_img)
# plt.axes().set_aspect(1)
# plt.xlim(-15,15)
# plt.ylim(-15,15)

re_rList,re_zList,_ = radialAverageByLinecuts(re_img,(0,0),X,Y,radialSteps=300,threshold=1/6*1,angleSteps=10)
# plt.figure()
plt.plot(re_rList,re_zList,'o',alpha=0.5,color='green',label='iMIM-Re')
plt.xlim(-15,15)
plt.legend()
plt.xlabel("Position (µm)")
plt.ylabel('iMIM signals (mV)')
plt.tight_layout()
plt.savefig(savePath+"/ImRe.png")

# conductivity_img = conductivity_all_cropped[ind].copy()#[:,:-1]
# plt.pcolormesh(X,Y,conductivity_img,cmap=aqua)
# plt.axes().set_aspect(1)
# plt.xlim(-15,15)
# plt.ylim(-15,15)

# conductivity_rList,conductivity_zList,_ = radialAverageByLinecuts(conductivity_img,(0,0),X,Y,radialSteps=300,threshold=1/6*1,angleSteps=10)
plt.figure(figsize=(7,4))
plt.scatter(xtemp,ztemp,marker=(5,1),color='royalblue',zorder=10,alpha=0.8,s=125,label='Conductivity')
plt.xlim(-15,15)
plt.legend(loc='upper left')
plt.ylabel("Local σ (S/m)")
plt.xlabel("Position (µm)")


ax2 = plt.axes().twinx()
def gaussian(r,w):
    return np.exp(-(r/w)**2)
laser_zList_norm = laser_zList/np.max(laser_zList)
laser_zList_edgesupress = np.asarray([item/(abs(laser_rList[i])**2*0.065+1) for i,item in enumerate(laser_zList_norm)])
plt.scatter(laser_rList[::4],laser_zList_edgesupress[::4],marker='o',color='blue',s=50,zorder=5,alpha=1,label='Laser profile')
plt.plot(laser_rList,gaussian(laser_rList,w=2),color='black',linewidth=3,label='Gaussian fit')
plt.ylabel('Laser Intensity (a.u.)',rotation=-90,labelpad=20)
plt.ylim(None,1.3)
plt.legend()
plt.xlabel("Position (µm)")
plt.xlim(-15,15)
plt.tight_layout()
plt.savefig(savePath+"/laserAndConductivity.png")