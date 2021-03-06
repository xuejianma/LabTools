"""
Created by Xuejian Ma at 6/21/2020.
All rights reserved.
"""
import numpy as np
import matplotlib.pyplot as plt
from averageRadialLinecuts import zList_all,rList_all
from utils import fit1,fit2
from config import savePath,power_list,power_label
from playground_plotMIMAndLaserLinecuts import select_index
import pickle

with open(savePath+"/diffusion_simulation_database.pickle","rb") as f:
    diffusion_simulation_database = pickle.load(f)
SMALL_SIZE = 8
MEDIUM_SIZE = 25
BIGGER_SIZE = 44    #35

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('axes', linewidth=2)
plt.rc('xtick.major',size=5,width=3)
plt.rc('ytick.major',size=5,width=3)

extra_shift_list = [0, 0, 0, 0, 0, 0]  # [-0.2,-0.2,0,0,0,0]


fig_x_range = 20
trial = False
extra_multiply_list = [1,1,1,1,1,1]#[0.95,0.95,0.95,0.95]#[0.994,0.994,0.95,0.994,0.994,0.994]

#no transport layer:[0.994]*6#[0.994,0.994,0.94,0.994,0.994,0.994]
#HTL: [0.96,0.97,0.98,0.97,0.97,0.97] wrong: [0.994]*6 #wrong HTL:[0.95,0.98,0.994,0.95,0.994,0.99]
#ETL: [0.95,0.994,0.94,0.994,0.994,0.994] wrong:[0.994,0.994,0.94,0.994,0.994,0.994]

#pvk "mixer":[0.994,0.994,0.95,0.994,0.994,0.994]   #[0.994]*6#[0.994,0.994,0.94,0.994,0.994,0.994]
#HTL "mixer": [0.94,0.98,0.98,0.97,0.97,0.97]
#ETL "mixer": [0.95,0.94,0.94,0.994,0.994,0.994] wrong:[0.994,0.994,0.94,0.994,0.994,0.994]

#wasted:
#[0.994] * 6  # [0.99,0.99,0.999,0.96,0.999,0.97]
#[0.994,0.994,0.95,0.994,0.994,0.994] for ETL

# power = [100,300,800,2000,5000,10000]
# power_label = ["1.0x10²", "3.0x10²", "8.0x10²", "20x10²", "50x10²", "100x10²"]
# power_list =[100,300,800,2000,5000,10000]
# error_list = [[4.5,5.5],[3.7,4.7],[3.1,4.1],[2.6,4.3],[2.6,4.8],[2.5,4.5]]
# diffusion_list_fit_list = [5,4.2,3.6,3.4,3.5,3.2]

# plot_ind = 5

error_list = []
diffusion_list_fit_list = []
colNum = 6
rowNum = int(np.ceil(len(zList_all)/colNum))
widthPerInset = 8
heightPerInset = 5
verbose = 0

plt.figure(figsize=(widthPerInset*colNum, heightPerInset*rowNum))

buffer_list = []
# for ind in range(len(power_label)):
for ind in range(len(zList_all)):
    buffer = []
    print()
    print("Diffusion Fitting Errorbar and Length "+str(ind+1)+"/"+str(len(zList_all)))
    # ind = 5
    x_axis = rList_all[ind] + extra_shift_list[ind]
    z_axis = ((zList_all[ind] - np.min(zList_all[ind])))
    fitrange = (-15,15)
    threshold=0.98
    if ind<=1 and trial==True:
        fitrange = (-15, 15)
        secondmin = sorted(zList_all[ind])[15]
        z_axis = ((zList_all[ind] - secondmin))

        if ind==0:
            # x_axis *= 0.8
            x_axis = np.asarray([x_axis[j] * (0.5 + np.abs(x_axis[j]) ** 2 / np.max(x_axis) ** 2) / 0.5 * 0.8 for j in
                                 range(len(x_axis))])
            fitrange = (4,8)
            threshold = 0.3
        elif ind==1:
            x_axis *= 0.85
            fitrange = (2,5)
            threshold = 0.85
        # x_axis = np.asarray([x_axis[j]/(1+np.abs(x_axis[j])**3/np.max(x_axis)**3)*1.0 for j in range(len(x_axis))])
        # x_axis = np.asarray([x_axis[j]*(0.5+np.abs(x_axis[j])**2/np.max(x_axis)**2)/0.5*0.8 for j in range(len(x_axis))])
        # x_axis = np.asarray([x_axis[j]*np.exp(-(np.max(x_axis)-np.abs(x_axis[j]))**5/np.max(x_axis)**5/5)*1.0 for j in range(len(x_axis))])

    try:
        lower_boundary, best_fit, upper_boundary, score_lower, score_best, score_upper = fit1(x_axis, z_axis,
                                                                                              diffusion_simulation_database,
                                                                                              extra_multiply=
                                                                                              extra_multiply_list[ind],
                                                                                              threshold = threshold,
                                                                                              fitrange=fitrange)
        print('threshold = {}'.format(threshold))

    except:
        lower_boundary, best_fit, upper_boundary, score_lower, score_best, score_upper = fit1(x_axis, z_axis,
                                                                                              diffusion_simulation_database,
                                                                                              extra_multiply=
                                                                                              extra_multiply_list[ind],
                                                                                              threshold=0.90,
                                                                                              fitrange=fitrange)#4 7
        print('threshold = 0.98')

    # temp = fit2(x_axis,z_axis,diffusion_simulation_database,extra_multiply=extra_multiply_list[ind])

    # diffusion_simulation_R2_score = dict.fromkeys(diffusion_simulation_database.keys(),None)
    #     temp = fit2(x_axis,z_axis,diffusion_simulation_database,extra_multiply=extra_multiply_list[ind])
    error_list.append([lower_boundary, upper_boundary])
    diffusion_list_fit_list.append(best_fit)
    #     if ind == plot_ind:
    if True:

        #         plt.figure(figsize=(6,3))
        plt.subplot(rowNum, colNum, ind + 1)
        plt.scatter(x_axis, z_axis, marker=(5, 1), color=[(32/255,160/255,255/255)], zorder=10, alpha=1, s=300)#alpha=0.7,color='royalblue'
        if trial == True and ind<=1:
            selected_indices = [kind for kind in range(len(x_axis)) if x_axis[kind]<30 and x_axis[kind]>-41]
            buffer.append(np.asarray(x_axis)[selected_indices])
            buffer.append(np.asarray(z_axis).astype(np.float)[selected_indices])
        else:
            buffer.append(x_axis)
            buffer.append(np.asarray(z_axis).astype(np.float))
        plt.tight_layout(pad=1)
        # laser_r = 2
        # length_list = [2.6,3.4,4.3]
        length_list = [lower_boundary, best_fit, upper_boundary]

        for index, length in enumerate(length_list):
            #     xx,yy,z = diffusion_map(length,laser_r,pos_max =40,point_num=100)
            xx, yy, _ = diffusion_simulation_database[length]
            z = diffusion_simulation_database[length][2]  # + 0.1*diffusion_simulation_database[2][2]
            x_axis_fit = xx[0]
            z_axis_fit = extra_multiply_list[ind] * z[round(z.shape[0] / 2)] / np.max(z) * (
                        np.max(zList_all[ind]) - np.min(zList_all[ind]))
            #             x_axis_clip = x_axis.clip(np.min(x_axis_fit),np.max(x_axis_fit))
            #             fit_func = interp1d(x_axis_fit,z_axis_fit)
            #             z_axis_fit_for_R2 = fit_func(x_axis_clip)
            # ax.xaxis.set_tick_params(width=5)
            # ax.yaxis.set_tick_params(width=5)
            if index == 0:

                plt.plot(x_axis_fit, z_axis_fit, linestyle='-.', label=str(round(length, 1)) + " µm", color="gray",
                         linewidth=3,zorder=99)  # , R²="+str(round(score_lower[0],3)) #,dashes=[5,4]
                buffer.append(x_axis_fit)
                buffer.append(z_axis_fit)
            elif index == 1:
                plt.plot(x_axis_fit, z_axis_fit, label=str(round(length, 1)) + " µm", color="black", linewidth=3,
                         zorder=99)  # , R²="+str(round(score_best[0],3))
                buffer.append(x_axis_fit)
                buffer.append(z_axis_fit)
            elif index == 2:
                plt.plot(x_axis_fit, z_axis_fit, linestyle='dashed', label=str(round(length, 1)) + " µm", color="gray",
                         linewidth=3,zorder=99)  # , R²="+str(round(score_upper[0],3))
                buffer.append(x_axis_fit)
                buffer.append(z_axis_fit)
        plt.xlim(-fig_x_range, fig_x_range)
        if verbose != 0:
            plt.legend(loc='upper right')
            # plt.xticks([])
            plt.title("$P_c$ = " + power_label[ind] + " mW/cm²")
            plt.xlabel("Position (µm)")
            plt.ylabel("Local σ (S/m)")
            handles, labels = plt.gca().get_legend_handles_labels()
            plt.legend(handles[::-1], labels[::-1], )  # loc='upper left')

        if ind == select_index:
            xtemp = x_axis
            ztemp = z_axis
        buffer_list.append(buffer)
plt.savefig(savePath+"/diffusionFittings.png")

# import pandas as pd
# conductivityLinecut_list = []
# for ind,buffer in enumerate(buffer_list):
#     df = pd.DataFrame(buffer).T
#     # df.to_csv(savePath+'/conductivityLinecut_'+str(ind+1)+'.csv')
#     df = df.rename(
#         columns={'0': 'x1', '1': 'y1(data)', '2': 'x2', '3': 'y2(lower)', '4': 'x3', '5': 'y3(best)', '6': 'x4',
#                  '7': 'y4(upper)'})
#     conductivityLinecut_list.append(df)
#
# headerintensities=np.asarray(np.asarray(range(len(buffer_list)))+1).astype(str)
# header = pd.MultiIndex.from_product([power_list,
#                                      ['x1', 'y1(data)', 'x2', 'y2(lower)', 'x3', 'y3(best)', 'x4', 'y4(upper)']],
#                                     names=['intensities', 'entries'])
# df = pd.DataFrame(pd.concat(conductivityLinecut_list, axis=1).values, columns=header)
# df.to_excel(savePath + 'diffusionLinecuts.xlsx')
#
#
#
# """
# diffusion length vs laser power curve
# """
# plt.figure(figsize=(8,5))
# SMALL_SIZE = 8
# MEDIUM_SIZE = 15
# BIGGER_SIZE = 20
#
# plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
# plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
# plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
# plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
# plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
# plt.rc('axes', linewidth=1.5)
# plt.rc('xtick.major',size=3,width=2)
# plt.rc('ytick.major',size=3,width=2)
# plt.rc('xtick.minor',size=2,width=1)
# plt.rc('ytick.minor',size=2,width=1)
#
# # power_list =[100,300,800,2000,5000,10000]
# # error_list = [[4.5,5.5],[3.7,4.7],[3.1,4.1],[2.6,4.3],[2.6,4.8],[2.5,4.5]]
# # diffusion_list_fit_list = [5,4.2,3.6,3.4,3.5,3.2]
# plt.scatter(power_list,diffusion_list_fit_list,marker='s',color='black',s=75,zorder=10)
# #plt.plot([100,800],[diffusion_list_fit_list[0]-0.2,diffusion_list_fit_list[2]-0.2],color='gray',linestyle='dashed')
# plt.plot(power_list,diffusion_list_fit_list,linestyle='dashed',color='gray',linewidth=3)
# for ind,power in enumerate(power_list):
#      plt.errorbar(power,error_list[ind],color = 'black',fmt='-_',linewidth=1,capsize=20)
# plt.yticks(np.arange(0, 10, step=1))
# plt.xscale('log')
# ymin = error_list[-1][0]-0.1-0.55
# ymax = error_list[0][1]+0.1+0.25
# plt.ylim(ymin,ymax)
# plt.xlabel("$P_c$ (mW/cm²)")
# plt.ylabel("Diffusion Length (µm)",labelpad=15)
# plt.tight_layout()
# plt.fill_between(power_list, np.array(error_list)[:,0],np.array(error_list)[:,1],color='oldlace')
# plt.savefig(savePath+"/diffusionLengthVSLaserPower.png")
#
# print(diffusion_list_fit_list,error_list)