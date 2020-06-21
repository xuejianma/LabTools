"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.
"""
import numpy as np
from utils import calibrate_xlist,calibrate_ylist
from readConductivities import conductivity_all,im_img_all,re_img_all
from config import x_extra_shift_list,y_extra_shift_list

length = int(len(conductivity_all[0])/2)
conductivity_all_average_x = np.mean(np.array(conductivity_all)[:,length-10:length+10,:],axis=1)
conductivity_all_average_y = np.mean(conductivity_all,axis=2)

x_list = np.array(range(conductivity_all_average_x.shape[1]))
x_list_real = calibrate_xlist(x_list)
x_shift_max = x_list_real[int(np.mean([item.argmax() for item in conductivity_all_average_x]))]
x_list_all = [[x-x_shift_max+x_extra_shift for x in x_list_real] for x_extra_shift in x_extra_shift_list]

y_list = np.array(range(conductivity_all_average_y.shape[1]))
y_list_real = calibrate_ylist(y_list)
y_shift_max = y_list_real[int(np.mean([item.argmax() for item in conductivity_all_average_y]))]
y_list_all = [[y-y_shift_max+y_extra_shift for y in y_list_real] for y_extra_shift in y_extra_shift_list]
####################################
conductivity_all_cropped = np.copy(conductivity_all)
#here *_cropped and * are actually the same. The suffix is for skewing, which does not work
#very well. Details are in Im_Re_Phase_Diagram.ipynb
x_list_all_cropped = np.copy(x_list_all)
y_list_all_cropped = np.copy(y_list_all)
im_img_all_cropped = np.copy(im_img_all)
re_img_all_cropped = np.copy(re_img_all)

#
#
# import matplotlib.pyplot as plt
# from config import savePath
# X_shift = []
# Y_shift = []
#
# theta = 48 * np.pi / 180
# theta2 = theta
# affine_matrix = np.array([[np.cos(-theta2), -np.sin(-theta2)], [np.sin(-theta2), np.cos(-theta2)]]).dot(
#     np.array([[1, 0.0], [0.0, 1 / 1.16]])).dot(
#     np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]))
# X_all = [];
# Y_all = [];
# for ind in range(6):
#     X, Y = np.meshgrid(x_list_all[ind], y_list_all[ind]).copy()
#     for xi in range(len(X)):
#         for yi in range(len(X[0])):
#             # X[xi,yi]+=-x_shift_max+x_extra_shift_list[ind]
#             # Y[xi,yi]+=-y_shift_max+y_extra_shift_list[ind]
#             X[xi, yi], Y[xi, yi] = np.matmul(affine_matrix, np.asarray([X[xi, yi], Y[xi, yi]]))
#
#     X_all.append(X)
#     Y_all.append(Y)
#
# plt.figure(figsize=(5, 5))
# ind = 5
# img = conductivity_all[ind].copy()
# img = re_img_all[ind][:300, :300].copy()
#
# # for i in range(img.shape[0]):
# #    for j in range(img.shape[1]):
# #        if abs(np.linalg.norm([X[i,j],Y[i,j]])-5)<=0.1:
# #            img[i,j]=100
# plt.pcolormesh(X_all[ind], Y_all[ind], img, vmin=0, vmax=600, cmap="afmhot")
# plt.scatter([0], [0])
# plt.xlim(-15, 15)
# plt.ylim(-15, 15)
# plt.savefig(savePath+"./test.png")
#
