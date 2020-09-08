"""
Created by Xuejian Ma at 6/19/2020.
All rights reserved.

This file generates the unskewed coordinates and data points. Unskeweing in skewPlaygound.py is just a visual
unskewing, which does not take much extra running time. This file unskew the images by resampling all pixels to squares.
It takes significant amount of time of it, but you only need to run it once for one set of skewing parameters. Those
parameters could be determined by test and error in skewPlaygound.py quickly. skewPlaygound.py is a playgound, and only
a playgound. One must come back to this file here to really change the parameters for the whole program to read.
"""
import numpy as np
import pickle
from readConductivities import conductivity_all,im_img_all,re_img_all
from calibratedCoords import x_list_all,y_list_all
from utils import resample
from config import folderPathList
from PyParkTiff import SaveParkTiff

X_shift = []
Y_shift = []

# sample w/o transport layers
# theta = 48*np.pi/180
# theta2=theta
# affine_matrix=np.array([[np.cos(-theta2),-np.sin(-theta2)],[np.sin(-theta2),np.cos(-theta2)]]).dot(
#                         np.array([[1,0.0],[0.0,1/1.16]])).dot(
#                         np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]]))

#sample with HTL/ETL
theta = 0*np.pi/180
theta2=theta
affine_matrix=np.array([[np.cos(-theta2),-np.sin(-theta2)],[np.sin(-theta2),np.cos(-theta2)]]).dot(
                       np.array([[1,0.0],[0.0,1]])).dot(
                       np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]]))


X_all = []; Y_all = [];
for ind in range(len(conductivity_all)):
    X,Y = np.meshgrid(x_list_all[ind],y_list_all[ind]).copy()
    for xi in range(len(X)):
        for yi in range(len(X[0])):
            #X[xi,yi]+=-x_shift_max+x_extra_shift_list[ind]
            #Y[xi,yi]+=-y_shift_max+y_extra_shift_list[ind]
            X[xi,yi],Y[xi,yi] = np.matmul(affine_matrix,np.asarray([X[xi,yi],Y[xi,yi]]))

    X_all.append(X)
    Y_all.append(Y)


x_list_all_cropped = []
y_list_all_cropped = []
im_img_all_cropped = []
re_img_all_cropped = []
conductivity_all_cropped = []
length = int(len(conductivity_all[0]) / 2)
xmin, xmax, ymin, ymax = [-25, 25, -25, 25]

size_list = []
for ind in range(len(conductivity_all)):
    X = X_all[ind].astype(np.float32)
    Y = Y_all[ind].astype(np.float32)
    size = 0
    for item in X[0]:
        if xmin <= item <= xmax:
            size += 1
    size_list.append(size)
size = np.min(size_list)
print('size:', size)

for ind,folderPath in enumerate(folderPathList):
# for ind in range(len(conductivity_all)):
#     ind=5

    print()
    print("Ongoing Resampling Conversion: ",ind + 1, '/', len(conductivity_all))
    X = X_all[ind].astype(np.float32)
    Y = Y_all[ind].astype(np.float32)
    img = conductivity_all[ind][:300, :300].astype(np.float32)
    img_im = im_img_all[ind][:300, :300].astype(np.float32)
    img_re = re_img_all[ind][:300, :300].astype(np.float32)
    print("\t---- resamping conductivity image (Sub-task 1/3)")
    new_conductivity_img, x_list, y_list = resample(img, X, Y, xmin, xmax, ymin, ymax, size)
    print("\t---- resamping im coordinates (Sub-task 2/3)")
    new_im_img, _, _ = resample(img_im, X, Y, xmin, xmax, ymin, ymax, size)
    print("\t---- resamping re coordinates (Sub-task 3/3)")
    new_re_img, _, _ = resample(img_re, X, Y, xmin, xmax, ymin, ymax, size)
    conductivity_all_cropped.append(new_conductivity_img)
    im_img_all_cropped.append(new_im_img)
    re_img_all_cropped.append(new_re_img)
    x_list_all_cropped.append(x_list)
    y_list_all_cropped.append(y_list)
    with open(folderPath+'/skewed_data.pickle', 'wb') as f:
        pickle.dump([x_list, y_list, new_conductivity_img, \
                     new_im_img, new_re_img], f)

    with open(folderPath + '/skewed_data.pickle', 'rb') as f:
        [x_list, y_list, new_conductivity_img,new_im_img, new_re_img]=pickle.load(f)
    new_conductivity_img = np.nan_to_num(new_conductivity_img)
    new_re_img = np.nan_to_num(new_re_img)
    new_im_img = np.nan_to_num(new_im_img)
    txtsave_cond = folderPath+'/new_conductivity_img_50um.txt'
    txtsave_re = folderPath+'/new_re_img_50um.txt'
    txtsave_im = folderPath+'/new_im_img_50um.txt'
    np.savetxt(txtsave_cond,new_conductivity_img)
    np.savetxt(txtsave_re,new_re_img)
    np.savetxt(txtsave_im,new_im_img)
    data = np.loadtxt(txtsave_cond)
    SaveParkTiff(data, xmax-xmin, ymax-ymin, folderPath+'/new_conductivity_img_50um.tiff')
    data = np.loadtxt(txtsave_re)
    SaveParkTiff(data, xmax-xmin, ymax-ymin, folderPath+'/new_re_img_50um.tiff')
    data = np.loadtxt(txtsave_im)
    SaveParkTiff(data, xmax-xmin, ymax-ymin, folderPath+'/new_im_img_50um.tiff')

# conductivity_all_average_x = np.mean(np.array(conductivity_all_cropped)[:,length-10:length+10,:],axis=1)
# conductivity_all_average_y = np.mean(conductivity_all_cropped,axis=2)

import pickle

# with open(savePath+'/skewed_data.pickle', 'wb') as f:
#     pickle.dump([x_list_all_cropped, y_list_all_cropped, conductivity_all_cropped, \
#                  im_img_all_cropped, re_img_all_cropped], f)