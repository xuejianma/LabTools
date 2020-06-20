"""
Created by Xuejian Ma at 6/19/2020.
All rights reserved.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from calibratedCoords50V import im_img_all_cropped,re_img_all_cropped,x_list_all_cropped,y_list_all_cropped
from config import saveFigPath


colors = [(0, 0, 0), (50 / 256, 100 / 256, 251 / 256), (72 / 256, 151 / 256, 247 / 256),
          (150 / 256, 241 / 256, 253 / 256), (1, 1, 1)]  # R -> G -> B
aqua = LinearSegmentedColormap.from_list(
    'aqua', colors, N=100)

fig, axs = plt.subplots(1, 6, figsize=(60, 10))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.05, hspace=None)

# ind = 5
for ind in range(6):
    # ax = axs[ind//2,ind%2]
    ax = axs[ind]
    # img = conductivity_all_cropped[ind].copy(); vmin = 0; vmax=10; cmap=aqua #conductivity images
    img = im_img_all_cropped[ind].copy();
    vmin = 0;
    vmax = 1100;
    cmap = "afmhot"  # imaginary images
    # img = re_img_all_cropped[ind].copy(); vmin = 0; vmax=600; cmap="afmhot"# real images

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

plt.savefig(saveFigPath+'/im.png')
# fig.colorbar(im) #You can uncomment the line to get an image with a COLOR BAR.

# plt.pcolormesh(X,Y,Z)