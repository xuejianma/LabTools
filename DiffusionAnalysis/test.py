"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.
"""
from readConductivities import im_img_all,re_img_all,conductivity_all
import matplotlib.pyplot as plt
plt.figure(figsize=(30,20))
plt.imshow(conductivity_all[-1])
plt.colorbar()
# plt.show()
plt.savefig("C:\Work\Xuejian Ma\Perovskite\imgs/test.png")