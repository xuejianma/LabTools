"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.

This file is for determining calibrating coefficients for 50Vx50V piezo stage distortion. It's not necessary to run it
if all coefficients are already determined. If you change any coefficient, remember to MANUALLY CHANGE it in config.py
as well. That is where coefficients really take effect. This here is only a playground which does NOT influence any
other files automatically.
"""
import numpy as np
import matplotlib.pyplot as plt
from readConductivities import conductivity_all
from config import saveFigPath
from utils import calibrate_xlist,calibrate_ylist

# https://stackoverflow.com/questions/45757280/solving-systems-of-equations-in-two-variables-python
def read_calibration_original_file(root_dir,calibration_original_file_name):
    with open(root_dir+calibration_original_file_name) as f:
        data = f.read()[:-1]
        lines = data.split("\n")
        conductivity_f = []
        #     print(lines)
        for line in lines:
            conductivity_f.append(np.array(line.split("\t")).astype(float)) #use space as splitter instead of /t
    return conductivity_f

def calculate_distortion(pair1,pair2):
    real1,appear1 = pair1
    real2,appear2 = pair2
    a = real1**2
    b = real1
    d = real2**2
    e = real2
    c = appear1
    f = appear2

    A = np.array([[a, b], [d, e]])
    B = np.array([[c], [f]])
    return(np.linalg.inv(A) @ B).reshape(1,2)[0]

def undistort_1D(appear,coeff1,coeff2):
    # coeff1*real**2 + coeff2*real - appear = 0
    return (-coeff2+np.sqrt(coeff2**2-4*coeff1*-appear))/(2*coeff1)


# read file
root_dir = '../../piezoCalibration/Al_on_silicon_commonly_used/2/'
calibration_original_file_name = 'Ch1 retrace.txt'
img = read_calibration_original_file(root_dir, calibration_original_file_name)
img_size_ij = np.shape(img)
# plt.imshow(img)

# overall configurations
unit = 30
extra_shift_x_real = 20
extra_shift_y_real = 0
extra_stretch_x_real = 1
extra_stretch_y_real = 1

# x-direction
pair1 = (unit, 87)
pair2 = (unit * 2, 199)
coeff1, coeff2 = calculate_distortion(pair1, pair2)
coeff1 *= 5
coeff2 *= 1
print("x coeff1: ",coeff1)
print("x coeff2: ",coeff2)

x_list_appear = list(range(img_size_ij[1]))
x_list_real = []

for x in x_list_appear:
    appear = img_size_ij[0] - x
    x_list_real.append(unit * 2 - undistort_1D(appear, coeff1, coeff2) + extra_shift_x_real)

# y-direction
# unit = 30
pair1 = (unit, 115)
pair2 = (unit * 2, 285)
coeff1, coeff2 = calculate_distortion(pair1, pair2)
coeff1 *= 1.5  # 0.5
coeff2 *= 1.2  # 1.8
print("y coeff1: ",coeff1)
print("y coeff2: ",coeff2)
print("!!!NOTICE!!!:")
print("Please remember to MANUALLY CHANGE the coeffs in config.py if you make any change for calibration. \n\
This file is only a playground and will not change other files or effective settings automatically.")

y_list_appear = list(range(img_size_ij[0]))
y_list_real = []
for y in y_list_appear:
    appear = y
    y_list_real.append(undistort_1D(appear, coeff1, coeff2) + extra_shift_y_real)

# img = conductivity_all[-1].copy()

X, Y = np.meshgrid(x_list_real[:-1], y_list_real)
Z = np.array(np.array(img))[:, :-1]

#Plot un-calibrated distorted raw Al figure
plt.figure(figsize=((np.max(x_list_real) - np.min(x_list_real)) / 8, (np.max(y_list_real) - np.min(y_list_real)) / 8))
plt.pcolormesh([np.max(Z) / 4 - (line - np.min(line)) for line in Z], vmin=0.0, vmax=1.2)
plt.title("un-calibrated distorted raw Al figure")
plt.savefig(saveFigPath+'/calibrations/calibrate0.png')



# Plot the density map using nearest-neighbor interpolation
plt.figure(figsize=((np.max(x_list_real) - np.min(x_list_real)) / 8, (np.max(y_list_real) - np.min(y_list_real)) / 8))
plt.title("CONVERTED without Distortion")
plt.pcolormesh(X, Y, [np.max(Z) / 4 - (line - np.min(line)) for line in Z], vmin=0.0, vmax=1.2)
# plt.pcolormesh(X,Y,Z)

# plt.colorbar()
# plt.show()
plt.savefig(saveFigPath+'/calibrations/calibrate1.png')

img = conductivity_all[-1].copy()

X, Y = np.meshgrid(x_list_real[:-1], y_list_real)
Z = np.array(np.array(img))[:, :-1]

# Plot un-calibrated distorted conductivity
plt.figure(figsize=((np.max(x_list_real) - np.min(x_list_real)) / 8, (np.max(y_list_real) - np.min(y_list_real)) / 8))
plt.pcolormesh(-Z, vmin=-3, vmax=-0, cmap="Blues")
plt.title("Calibrated Undistorted Conductivity")
plt.savefig(saveFigPath+'/calibrations/calibrate2.png')

# Plot the density map using nearest-neighbor interpolation
plt.figure(figsize=((np.max(x_list_real) - np.min(x_list_real)) / 8, (np.max(y_list_real) - np.min(y_list_real)) / 8))
plt.pcolormesh(X, Y, -Z, vmin=-3, vmax=-0, cmap="Blues")
# plt.pcolormesh(X,Y,Z)

# plt.colorbar()
# plt.show()
plt.title("Calibrated Undistorted Conductivity")
plt.savefig(saveFigPath+'/calibrations/calibrate3.png')

plt.figure()
plt.plot(y_list_real, np.mean(Z, axis=1), label='undistorted')
plt.plot(y_list_real, np.mean(Z, axis=1), label='undistorted2')

plt.legend()
plt.savefig(saveFigPath+'/calibrations/calibrate4.png')


plt.figure()
plt.plot(y_list_appear, np.mean(img, axis=1), label='distorted')
plt.legend()
plt.savefig(saveFigPath+'/calibrations/calibrate5.png')


ind = -1
img = conductivity_all[ind].copy()
img_shape = np.asarray(img).shape
x_list = list(range(img_shape[1]))
y_list = list(range(img_shape[0]))
x_list_real = calibrate_xlist(x_list)
y_list_real = calibrate_ylist(y_list)
X,Y = np.meshgrid(x_list_real,y_list_real)
Z = np.array(np.array(img))[:,:-1]
plt.figure(figsize=((np.max(X)-np.min(X))/12,(np.max(Y)-np.min(Y))/12))
#plt.subplot(121)
plt.title('Calibrated Image, Unskewed')
plt.pcolormesh(X,Y,-Z,vmin=-20,vmax=-0,cmap="Blues")

theta = np.pi/4
affine_matrix=np.array([[np.cos(-theta),-np.sin(-theta)],[np.sin(-theta),np.cos(-theta)]]).dot(
                        np.array([[1.1,0.0],[0.0,1]])).dot(
                        np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]]))
X,Y = np.meshgrid(x_list_real,y_list_real)
for xi in range(len(X)):
    for yi in range(len(X[0])):
        X[xi,yi],Y[xi,yi] = np.matmul(affine_matrix,np.asarray([X[xi,yi],Y[xi,yi]]))


# Plot the density map using nearest-neighbor interpolation
plt.figure(figsize=((np.max(X)-np.min(X))/12,(np.max(Y)-np.min(Y))/12))
#plt.subplot(122)
plt.title('Calibrated Image, Skewed')
plt.pcolormesh(X,Y,-Z,vmin=-3,vmax=-0,cmap="Blues")
plt.savefig(saveFigPath+'/calibrations/calibrate6.png')
