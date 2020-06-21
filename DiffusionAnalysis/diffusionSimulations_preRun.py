"""
Created by Xuejian Ma at 6/21/2020.
All rights reserved.
"""
import numpy as np
import pickle
import time
import matplotlib.pyplot as plt
from utils import diffusion_map
from config import savePath
from tqdm import tqdm
diffusion_simulation_database = {}
length_list=np.linspace(1,7,61)
t1 = time.time()
laser_r=2

plt.figure(figsize=(5,5))
xx,yy,z = diffusion_map(length_list[0],laser_r,pos_max =40,point_num=150)
plt.title("Diffusion example: laser_r="+str(laser_r)+", diffusion length="+str(length_list[0]))
plt.pcolormesh(xx,yy,z)
plt.savefig(savePath+"/diffusionSimulationExample.png")

for ind,length in enumerate(tqdm(length_list)):
#     xx,yy,z = diffusion_map(length,laser_r,pos_max =40,point_num=350)
    xx,yy,z = diffusion_map(length,laser_r,pos_max =40,point_num=150)

    diffusion_simulation_database[round(length,1)]=[xx,yy,z]
#     if ind == 0:
#         t2 = time.time()
#     print("length finished:",round(length,1),"time left:", (t2-t1)*(len(length_list)-ind-1)/60,"mins")
with open(savePath+"/diffusion_simulation_database.pickle","wb") as f:
    pickle.dump(diffusion_simulation_database,f)