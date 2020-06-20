"""
Created by Xuejian Ma at 6/19/2020.
All rights reserved.
"""
import numpy as np
import matplotlib.pyplot as plt
from readConductivities import conductivity_all,im_img_all,re_img_all
from calibratedCoords50V import x_list_all,y_list_all

X_shift = []
Y_shift = []

theta = 48 * np.pi / 180
theta2 = theta
affine_matrix = np.array([[np.cos(-theta2), -np.sin(-theta2)], [np.sin(-theta2), np.cos(-theta2)]]).dot(
    np.array([[1, 0.0], [0.0, 1 / 1.16]])).dot(
    np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]))
X_all = [];
Y_all = [];
for ind in range(len(conductivity_all)):
    X, Y = np.meshgrid(x_list_all[ind], y_list_all[ind]).copy()
    for xi in range(len(X)):
        for yi in range(len(X[0])):
            # X[xi,yi]+=-x_shift_max+x_extra_shift_list[ind]
            # Y[xi,yi]+=-y_shift_max+y_extra_shift_list[ind]
            X[xi, yi], Y[xi, yi] = np.matmul(affine_matrix, np.asarray([X[xi, yi], Y[xi, yi]]))

    X_all.append(X)
    Y_all.append(Y)

plt.figure(figsize=(5, 5))
ind = 5
img = conductivity_all[ind].copy()
img = re_img_all[ind][:300, :300].copy()

# for i in range(img.shape[0]):
#    for j in range(img.shape[1]):
#        if abs(np.linalg.norm([X[i,j],Y[i,j]])-5)<=0.1:
#            img[i,j]=100
plt.pcolormesh(X_all[ind], Y_all[ind], img, vmin=0, vmax=600, cmap="afmhot")
plt.scatter([0], [0])
plt.xlim(-15, 15)
plt.ylim(-15, 15)
plt.show()