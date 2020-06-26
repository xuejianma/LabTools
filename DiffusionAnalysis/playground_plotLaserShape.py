"""
Created by Xuejian Ma at 6/21/2020.
All rights reserved.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from config import savePath
colors = [(0, 0, 0),(25/256, 50/256, 251/256),(36/256, 75/256, 247/256), (75/256, 120/256, 253/256),(0.8, 0.8, 1)]  # R -> G -> B
aqua_blue = LinearSegmentedColormap.from_list(
        'aqua_blue', colors, N=100)
laserimg = plt.imread('../../Perovskite/laserSpot.png')[:,:,2]
laser_x = np.linspace(0,385.8175354250646,laserimg.shape[1])-249.8
laser_y = np.linspace(0,385.8175354250646/laserimg.shape[1]*laserimg.shape[0],laserimg.shape[0])-170.15
sr = [np.where(laser_y<-15)[0][-1],np.where(laser_y>15)[0][0],np.where(laser_x<-15)[0][-1],np.where(laser_x>15)[0][0]]

laser_X,laser_Y = np.meshgrid(laser_x,laser_y)
laser_X_cropped = laser_X[sr[0]:sr[1],sr[2]:sr[3]]
laser_Y_cropped = laser_Y[sr[0]:sr[1],sr[2]:sr[3]]

laserimg_cropped = laserimg[sr[0]:sr[1],sr[2]:sr[3]]
# plt.figure(figsize=(10,10))
# plt.pcolormesh(laser_X_cropped,laser_Y_cropped,laserimg_cropped,cmap=aqua)#[450:490,250:500])
# plt.axes().set_aspect(1)
# plt.scatter([0],[0],color='red',s=10)

plt.figure()
laserimg_cropped_edgesupress = laserimg_cropped.copy()
for i in range(laserimg_cropped_edgesupress.shape[0]):
    for j in range(laserimg_cropped_edgesupress.shape[1]):
        laserimg_cropped_edgesupress[i,j]/=((np.linalg.norm([laser_X_cropped[i,j],laser_Y_cropped[i,j]]))**2*0.065+1)
plt.pcolormesh(laser_X_cropped,laser_Y_cropped,laserimg_cropped_edgesupress,cmap=aqua_blue)#[450:490,250:500])
plt.axes().set_aspect(1)
plt.xticks([])
plt.yticks([])

# plt.scatter([0],[0],color='red',s=10)
plt.title("Laser spot, 30um x 30um")
plt.savefig(savePath+"/laserSpotCropped.png")