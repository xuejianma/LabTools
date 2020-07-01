"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
from calibratedCoords import conductivity_all_cropped,x_list_all,y_list_all,conductivity_all_average_y
from config import savePath

width_num = 2
heigh_num = int(np.ceil(len(conductivity_all_cropped)/width_num))
fig, axs = plt.subplots(heigh_num, width_num, figsize=(20, 30))

# ind = 5
for ind in range(len(conductivity_all_cropped)):
    if len(conductivity_all_cropped) == 1:
        ax = axs[0]
    else:
        ax = axs[ind // width_num, ind % width_num]
    img = conductivity_all_cropped[ind].copy()
    X, Y = np.meshgrid(x_list_all[ind], y_list_all[ind])
    # X = X_all[ind]
    # Y = Y_all[ind]

    Z = np.array(np.array(img))[:, :-1]

    # Plot the density map using nearest-neighbor interpolation
    zlim = np.max(np.array(img))/1.1
    # plt.figure(figsize=((np.max(x_list_real)-np.min(x_list_real))/8,(np.max(y_list_real)-np.min(y_list_real))/8))
    ax.pcolormesh(X, Y, -Z, vmin=-zlim, vmax=-0, cmap="Blues")
    ax.scatter([0], [0], color='red',s=500)
    ax.set(adjustable='box', aspect='equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    fontprops = fm.FontProperties(size=30)
    scalebar = AnchoredSizeBar(ax.transData,
                               10, '10 $\mu m$', 'lower right',
                               pad=1,
                               sep=7,
                               color='white',
                               frameon=False,
                               size_vertical=0.5,
                               fontproperties=fontprops)

    # axs[ind % heigh_num, ind // heigh_num].add_artist(scalebar)
    ax.add_artist(scalebar)
plt.savefig(savePath+"/checkCenterPoints0.png")

plt.figure(figsize=(10, 5))
for ind, conductivity_average in enumerate(conductivity_all_average_y):
    if True:#ind in [0, 1, 2, 3, 4, 5]:
        y_axis = np.array(y_list_all[ind])
        #         z_axis = (conductivity_average-conductivity_average.min())/(conductivity_average.max()-conductivity_average.min())
        z_axis = conductivity_average / conductivity_average.max()

        plt.plot(y_axis, z_axis)
#        plt.plot(np.linspace(-30,30,301),z_axis)
plt.title("Normalized averaging over axis=2. Doesn't reflect the real diffusion at all! Only for center and shape "
          "checking.")
plt.legend(list(range(len(conductivity_all_average_y))))
plt.plot((0, 0), (0, 1.1))
plt.savefig(savePath+"/checkCenterPoints1.png")
