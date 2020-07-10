"""
Created by Xuejian Ma at 6/19/2020.
All rights reserved.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from config import savePath,unskewFlag
if unskewFlag==0:
    from calibratedCoords import im_img_all_cropped,re_img_all_cropped,x_list_all_cropped,y_list_all_cropped,conductivity_all_cropped
else:
    from calibratedUnskewedCoords import im_img_all_cropped,re_img_all_cropped,x_list_all_cropped,y_list_all_cropped,conductivity_all_cropped


colors = [(0, 0, 0), (50 / 256, 100 / 256, 251 / 256), (72 / 256, 151 / 256, 247 / 256),
          (150 / 256, 241 / 256, 253 / 256), (1, 1, 1)]  # R -> G -> B
aqua = LinearSegmentedColormap.from_list(
    'aqua', colors, N=100)

fig, axs = plt.subplots(1, len(conductivity_all_cropped), figsize=(10*len(conductivity_all_cropped), 10))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.05, hspace=None)

# ind = 5
print()
maxscale_mim = 1.2
maxscale_cond = 1.75#maxscale_mim
for j in range(3):# 3 represents im,re and conductivity
    if j == 0:
        vmin = 0; vmax = int(maxscale_mim*1.041667*np.max(im_img_all_cropped)/10)*10;cmap = "afmhot"  #vmax=1000, imaginary images
        print("im range:",(vmin,vmax))
    elif j ==1:
        vmin = 0; vmax=int(0.95*maxscale_mim*1/1.04*np.max(re_img_all_cropped)/10)*10; cmap="afmhot"# real images
        #HTL vim = 40
        print("re range:", (vmin, vmax))
    elif j ==2:
        vmin = 0; vmax=int(0.8*maxscale_cond*1/2.009233*np.max(conductivity_all_cropped)); cmap=aqua #conductivity images
        print("conductivity range:", (vmin, vmax))
    for ind in range(len(conductivity_all_cropped)):
        if j == 0:
            img = im_img_all_cropped[ind].copy();
        elif j == 1:
            img = re_img_all_cropped[ind].copy();
        elif j == 2:
            img = conductivity_all_cropped[ind].copy();
        # ax = axs[ind//2,ind%2]
        ax = axs[ind]

        X, Y = np.meshgrid(x_list_all_cropped[ind], y_list_all_cropped[ind])
        # X = X_all[ind]
        # Y = Y_all[ind]

        Z = np.array(np.array(img))[:, :-1]

        # Plot the density map using nearest-neighbor interpolation

        # plt.figure(figsize=((np.max(x_list_real)-np.min(x_list_real))/8,(np.max(y_list_real)-np.min(y_list_real))/8))
        im = ax.pcolormesh(X, Y, Z, vmin=vmin, vmax=vmax, cmap=cmap)
        # ax.scatter([0],[0],color='red')
        ax.set_xlim(-15, 15)
        ax.set_ylim(-15, 15)
        # fontprops = fm.FontProperties(weight=1000,size=60,)
        fontprops = fm.FontProperties(size=60, )
        scalebar = AnchoredSizeBar(ax.transData,
                                   10, '10 $\mu m$', 'lower right',
                                   pad=0.2,
                                   sep=10,
                                   color='white',
                                   frameon=False,
                                   size_vertical=1,
                                   fontproperties=fontprops)

        # if ind ==0:
        #    ax.add_artist(scalebar)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect(1)

    plt.savefig(savePath+'/ImReConductivity'+str(j)+'.png')
# fig.colorbar(im) #You can uncomment the line to get an image with a COLOR BAR.

# plt.pcolormesh(X,Y,Z)