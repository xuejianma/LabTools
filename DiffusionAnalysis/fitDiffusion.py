"""
Created by Xuejian Ma at 6/21/2020.
All rights reserved.
"""
import numpy as np
import matplotlib.pyplot as plt
from averageRadialLinecuts import zList_all,rList_all
from utils import fit1,fit2
from config import savePath,power_list,power_label
import pickle

with open(savePath+"/diffusion_simulation_database.pickle","rb") as f:
    diffusion_simulation_database = pickle.load(f)
SMALL_SIZE = 8
MEDIUM_SIZE = 25
BIGGER_SIZE = 35

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
extra_multiply_list = [0.994]*6#[0.994,0.994,0.94,0.994,0.994,0.994]#HTL: [0.95,0.98,0.994,0.95,0.994,0.99]
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


# for ind in range(len(power_label)):
for ind in range(len(zList_all)):
    print()
    print("Diffusion Fitting Errorbar and Length "+str(ind+1)+"/"+str(len(zList_all)))
    # ind = 5
    x_axis = rList_all[ind] + extra_shift_list[ind]
    z_axis = ((zList_all[ind] - np.min(zList_all[ind])))
    try:
        lower_boundary, best_fit, upper_boundary, score_lower, score_best, score_upper = fit1(x_axis, z_axis,
                                                                                              diffusion_simulation_database,
                                                                                              extra_multiply=
                                                                                              extra_multiply_list[ind],
                                                                                              threshold = 0.98)
        print('threshold = 0.98')
    except:
        lower_boundary, best_fit, upper_boundary, score_lower, score_best, score_upper = fit1(x_axis, z_axis,
                                                                                              diffusion_simulation_database,
                                                                                              extra_multiply=
                                                                                              extra_multiply_list[ind],
                                                                                              threshold=0.94)
        print('threshold = 0.94')
    # temp = fit2(x_axis,z_axis,diffusion_simulation_database,extra_multiply=extra_multiply_list[ind])

    # diffusion_simulation_R2_score = dict.fromkeys(diffusion_simulation_database.keys(),None)
    #     temp = fit2(x_axis,z_axis,diffusion_simulation_database,extra_multiply=extra_multiply_list[ind])
    error_list.append([lower_boundary, upper_boundary])
    diffusion_list_fit_list.append(best_fit)
    #     if ind == plot_ind:
    if True:

        #         plt.figure(figsize=(6,3))
        plt.subplot(rowNum, colNum, ind + 1)
        plt.scatter(x_axis, z_axis, marker=(5, 1), color='royalblue', zorder=10, alpha=0.7, s=200)
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
                         linewidth=5)  # , R²="+str(round(score_lower[0],3)) #,dashes=[5,4]
            elif index == 1:
                plt.plot(x_axis_fit, z_axis_fit, label=str(round(length, 1)) + " µm", color="black", linewidth=6,
                         zorder=9)  # , R²="+str(round(score_best[0],3))
            elif index == 2:
                plt.plot(x_axis_fit, z_axis_fit, linestyle='dashed', label=str(round(length, 1)) + " µm", color="gray",
                         linewidth=5)  # , R²="+str(round(score_upper[0],3))
        plt.xlim(-15, 15)
        if verbose != 0:
            plt.legend(loc='upper right')
            # plt.xticks([])
            plt.title("$P_c$ = " + power_label[ind] + " mW/cm²")
            plt.xlabel("Position (µm)")
            plt.ylabel("Local σ (nS)")
            handles, labels = plt.gca().get_legend_handles_labels()
            plt.legend(handles[::-1], labels[::-1], )  # loc='upper left')

        if ind == 3:
            xtemp = x_axis
            ztemp = z_axis
plt.savefig(savePath+"/diffusionFittings.png")

"""
diffusion length vs laser power curve
"""
plt.figure(figsize=(8,5))
SMALL_SIZE = 8
MEDIUM_SIZE = 15
BIGGER_SIZE = 20

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

# power_list =[100,300,800,2000,5000,10000]
# error_list = [[4.5,5.5],[3.7,4.7],[3.1,4.1],[2.6,4.3],[2.6,4.8],[2.5,4.5]]
# diffusion_list_fit_list = [5,4.2,3.6,3.4,3.5,3.2]
plt.scatter(power_list,diffusion_list_fit_list,marker='s',color='black',s=75,zorder=10)
#plt.plot([100,800],[diffusion_list_fit_list[0]-0.2,diffusion_list_fit_list[2]-0.2],color='gray',linestyle='dashed')
plt.plot(power_list,diffusion_list_fit_list,linestyle='dashed',color='gray',linewidth=3)
for ind,power in enumerate(power_list):
     plt.errorbar(power,error_list[ind],color = 'black',fmt='-_',linewidth=1,capsize=20)
plt.yticks(np.arange(0, 10, step=1))
plt.xscale('log')
ymin = error_list[-1][0]-0.1-0.55
ymax = error_list[0][1]+0.1+0.25
plt.ylim(ymin,ymax)
plt.xlabel("$P_c$ (mW/cm²)")
plt.ylabel("Diffusion Length (µm)",labelpad=15)
plt.tight_layout()
plt.fill_between(power_list, np.array(error_list)[:,0],np.array(error_list)[:,1],color='oldlace')
plt.savefig(savePath+"/diffusionLengthVSLaserPower.png")

print(diffusion_list_fit_list,error_list)