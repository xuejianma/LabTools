"""
Created by Xuejian Ma at 6/21/2020.
All rights reserved.
"""
import numpy as np
import matplotlib.pyplot as plt
from averageRadialLinecuts import zList_all,rList_all
from config import savePath,power_label,power_list



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


plt.figure(figsize = (8,6))
colors=plt.cm.rainbow(np.linspace(0,0.5,2*len(rList_all)))
signal_center_list = []
signal_center_error_list = []

for ind in range(len(rList_all)):
#     rList_sym = np.concatenate((-rList_all[ind][::-1],rList_all[ind]))
#     zList_sym = np.concatenate((zList_all[ind][::-1],zList_all[ind]))
#     plt.plot(rList_sym,zList_sym/np.max(zList_all[ind]))
    r_list = rList_all[ind]
    z_list = (zList_all[ind]-np.min(zList_all[ind]))#/(np.max(zList_all[ind])-np.min(zList_all[ind]))
    #center_pos = int(len(zList_all[ind])/2)
    center_pos = np.where(rList_all[ind]==0)[0][0]
    center_cluster = [z_list[i] for i in range(center_pos-15,center_pos+15)]
    signal_center_error_list.append([np.min(center_cluster),np.max(center_cluster)])
#     plt.scatter(r_list,z_list,s=5)
    plt.plot(r_list,z_list,color=colors[ind])
    signal_center_list.append(zList_all[ind][center_pos]-np.min(zList_all[ind]))
# power_label = ["1.0x10² mW/cm²","3.0x10² mW/cm²","8.0x10² mW/cm²","20x10² mW/cm²","50x10² mW/cm²","100x10² mW/cm²"]
# power_list =[100,300,800,2000,5000,10000]
plt.legend(power_label)
plt.xlabel("Position (µm)")
plt.ylabel("Local σ (nS)")
# plt.xlim(-15,15)
plt.tight_layout()
plt.title("Averaged Radial Linecuts")
plt.savefig(savePath+"/averagedLinecuts.png")

plt.figure(figsize=(8,5))
plt.scatter(power_list,signal_center_list,marker='o',s = 75,color='blue',zorder=10)
m,b = np.polyfit(np.log(power_list), np.log(signal_center_list), 1)
print("m,b:",m,b)
k = np.exp(b)
print('y=e^b*x^^m,k-e^b,k:',k)
k2 = ((np.exp(m*np.log(power_list[-1])+b))-(np.exp(m*np.log(power_list[0])+b)))/(power_list[-1]-power_list[0])
print('red k2:',k2)
ml,bl = np.polyfit(power_list, signal_center_list, 1)
print("orange ml,bl:",ml,bl)
print('y/x:',[item2/item1 for item1,item2 in zip(power_list,signal_center_list)])

#plt.plot([100,10000],[signal_center_list[0],signal_center_list[-1]],color="black",linestyle="dashed")
plt.plot([power_list[0],power_list[-1]],[np.exp(m*np.log(power_list[0])+b),np.exp(m*np.log(power_list[-1])+b)],color="gray",linestyle="dashed",linewidth=4)
plt.plot([power_list[0],power_list[-1]],[ml*power_list[0]+bl,ml*power_list[-1]+bl],color="orange",linestyle="dashed",linewidth=4)
plt.plot([power_list[0],power_list[-1]],[k2*power_list[0],k2*power_list[-1]],color="red",linestyle="dashed",linewidth=4)

for ind,power in enumerate(power_list):
    plt.errorbar(power,signal_center_error_list[ind],fmt='-_',color='blue',linewidth=2,markersize=15,markeredgewidth=2)
# plt.xscale('log')
# plt.yscale('log')
plt.xlabel("$P_c$ (mW/cm²)")
plt.ylabel("Center σ (S/m)")
# plt.xlim(8e1,1.2e4)
# plt.ylim(2e-1,2e1)
plt.tight_layout()

plt.savefig(savePath+"/centerConductivitiesCurve.png")
print("powers:",list(power_list))
print("center conductivities: ",list(np.array(signal_center_list)[:,0]))