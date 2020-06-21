"""
Created by Xuejian Ma at 6/19/2020.
All rights reserved.
"""
import pickle
from config import folderPathList

x_list_all_cropped = []
y_list_all_cropped = []
conductivity_all_cropped = []
im_img_all_cropped = []
re_img_all_cropped = []
try:
    for ind, folderPath in enumerate(folderPathList):
        with open(folderPath + '/skewed_data.pickle', 'rb') as f:
            x_list, y_list, new_conductivity_img, new_im_img, new_re_img = pickle.load(f)
        x_list_all_cropped.append(x_list)
        y_list_all_cropped.append(y_list)
        conductivity_all_cropped.append(new_conductivity_img)
        im_img_all_cropped.append(new_im_img)
        re_img_all_cropped.append(new_re_img)
except:
    raise IOError(
        'skewed_data.pickle file not found. Did you run convert2Unskewed_preRun.py before? That is a must for unskewing')
