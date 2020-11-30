"""
Created by Xuejian Ma at 6/18/2020.
All rights reserved.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm.auto import tqdm
from scipy import interpolate
from collections import defaultdict
from scipy.interpolate import interp1d
from PyParkTiff import SaveParkTiff



def readTXT(filePath):
    """
    Read diffusion data in default txt file to a 2d numpy array.
    :param filePath: txt file generated by Labview diffusion measurement GUI. Default name is "Ch1 retrace.txt" etc.
    :return: 2d array of the diffusion data in the txt file
    """
    f1 = open(filePath)
    data = f1.read()[:-1]
    lines = data.split("\n")
    matrix = []
    for line in lines:
        try:
            matrix.append(np.array(line.split("\t")).astype(float))
        except:
            matrix.append(np.array(line.split(" ")).astype(float))
    return np.asarray(matrix)


def readImRePhase(folderPathList, fileNameIm, fileNameRe, naiveScale):
    """
    Read im and re diffusion files into 1d arrays for phase diagram. Phase diagram is for comparison with simulated
    Im and Re curves by COMSOL.
    :param filePathImList: must have the same length with filePathReList correspondingly.
    :param filePathReList: must have the same length with filePathImList correspondingly.
    :param naiveScale: naiveScale to the raw data. Usually the raw data are in V. To convert them to mV, we need scale=1000.
    :return: 1d array im_all, and 1d array re_all, with only voltage information (no coordinates information)
    """
    im_all = []
    re_all = []
    for folderPath in folderPathList:
        im = readTXT(folderPath + '/' + fileNameIm)
        im_all += list(np.array(im).reshape(1, -1)[0] * naiveScale)
        re = readTXT(folderPath + '/' + fileNameRe)
        re_all += list(np.array(re).reshape(1, -1)[0] * naiveScale)
    return im_all, re_all


def plotImRePhase(filePathImList, filePathReList, savePath):
    """
    Read and Plot im and re diffusion files into 1d arrays for phase diagram. Phase diagram is for comparison with simulated
    Im and Re curves by COMSOL.
    :param filePathImList: must have the same length with filePathReList correspondingly.
    :param filePathReList: must have the same length with filePathImList correspondingly.
    :param savePath: path to save the phase diagram.
    :return: None
    """
    im_all, re_all = readImRePhase(filePathImList, filePathReList)
    plt.plot(np.array(im_all), np.array(re_all), ".")
    plt.savefig(savePath + '/imRePhase.png')
    return None


def readSimulatedImReCSV(filePath, comsolScale):
    '''
    Read the simulated im re curves generated by COMSOL.
    :param filePath: csv file from COMSOL, which contains columns of conductivity, im and re signals.
    :param comsolScale: convert from COMSOL unit to mV.
        comsolScale = 3.5*10 for diffusion. 3.5 is the default calibrated coefficient,
            10 is multiplied to fit the signal amplification of lock-in.
        comsolScale=  3.5/1000*125 for TR-iMIM signals. 3.5 is still default calibrated coefficient, factor of 125/1000 is
            multiplied since 3.5 is for a 1000x DC amplifier, while TR-iMIM uses the amplifier with 125x instead.
    :return: cond_array as x-axis, im_sim, re_sim as y-values
    '''
    df = pd.read_csv(filePath, error_bad_lines=False, skiprows=4)  # Untitled_632
    # diffusion simulation file chosen: Untitled_R28_1degree.csv
    # Tr simulation file chosen: tr2.csv
    cond_array = df.iloc[:, 0]
    # im_sim_raw = df.iloc[:,1]*3.5*10
    # re_sim_raw = df.iloc[:,2]*3.5*10
    im_sim_raw = df.iloc[:, 1] * comsolScale  # * 3.5 / 1000 * 125
    re_sim_raw = df.iloc[:, 2] * comsolScale  # * 3.5 / 1000 * 125
    im_sim = im_sim_raw - np.min(im_sim_raw)
    re_sim = re_sim_raw - np.min(re_sim_raw)
    return cond_array, im_sim, re_sim


def plotSimulatedImReCurves(filePath, savePath, comsolScale):
    '''
    Plot the simulated im re curves generated by COMSOL.
    :param filePath: csv file from COMSOL, which contains columns of conductivity, im and re signals.
    :param savePath: path to save the curves.
    :param comsolScale: see readSimulatedImReCSV().
    :return: None
    '''
    SMALL_SIZE = 8
    MEDIUM_SIZE = 20
    BIGGER_SIZE = 22
    plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=BIGGER_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=MEDIUM_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    plt.rc('axes', linewidth=2)
    plt.rc('xtick.major', size=5, width=3)
    plt.rc('ytick.major', size=5, width=3)
    cond_array, im_sim, re_sim = readSimulatedImReCSV(filePath, comsolScale)
    plt.figure()
    plt.xscale('log')
    # plt.xlim(1e-7,7e6)
    # plt.plot(cond_array,im_sim,'.')
    # plt.plot(cond_array,re_sim,'.')
    plt.plot(cond_array, im_sim, color='red', linewidth=6, label="iMIM-Im")
    plt.plot(cond_array, re_sim, color='green', linewidth=6, label="iMIM-Re")
    plt.xlabel("Local σ (S/m)")
    plt.ylabel("Simulated Signals (mV)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(savePath + "/simulatedImReCurves.png")
    return None


def plotSimulatedImReCurves_Linear(filePath, savePath, comsolScale, maxPos=107, maxTick=12, tickStep=2):
    '''
    Plot the simulated im re curves generated by COMSOL in the LINEAR SCOPE.
    :param filePath: csv file from COMSOL, which contains columns of conductivity, im and re signals.
    :param savePath: path to save the curves.
    :param comsolScale: see readSimulatedImReCSV().
    :param maxPos: see below for details.
    :param maxTick: see below for details.
    :param tickStep: see below for details.
    :return: None
    '''
    SMALL_SIZE = 8
    MEDIUM_SIZE = 25
    BIGGER_SIZE = 35

    plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=BIGGER_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=MEDIUM_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    plt.rc('axes', linewidth=4)
    plt.rc('xtick.major', size=5, width=3)
    plt.rc('ytick.major', size=5, width=3)
    cond_array, im_sim, re_sim = readSimulatedImReCSV(filePath, comsolScale)
    rc = list(range(0, maxPos))
    plt.figure()
    plt.plot(cond_array[rc], im_sim[rc], color='red', linewidth=10, label="iMIM-Im")
    plt.plot(cond_array[rc], re_sim[rc], color='green', linewidth=10, label="iMIM-Re")
    plt.xticks(list(range(0, maxTick, tickStep)))
    plt.savefig(savePath + "/simulatedImReCurves_Linear.png")
    return None


def plotPhaseAndSimulatedCurves(im_all, re_all, im_sim, re_sim, savePath):
    """
    Plot both phase diagram and simulated im re curves in one figure, in order to see the quality of simulation.
    :param im_all: from readImRePhase()
    :param re_all: from readImRePhase()
    :param im_sim: from readSimulatedImReCSV()
    :param re_sim: from readSimulatedImReCSV()
    :param savePath: path to save the figure.
    :return: None
    """
    plt.figure()
    plt.plot(np.array(im_all), np.array(re_all), ".")
    plt.plot(im_sim, re_sim)
    plt.savefig(savePath + "/phaseAndSimulatedCurves.png")
    return None


def distance(pt1, pt2):
    return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)


def nearestIndex(pt, array_with_conductivity):
    # pt: (x,y)
    # array_with_conductivity: [((x,y),conductivity),...]
    distance_list = []
    for item in array_with_conductivity:
        distance_list.append(distance(pt, item[0]))
    return distance_list.index(np.min(distance_list))


def readImRe(folderPath, fileNameIm, fileNameRe, naiveScale):
    filePathIm = folderPath + '/' + fileNameIm
    filePathRe = folderPath + '/' + fileNameRe
    im_img_array = []
    with open(filePathIm) as f:
        data = f.read()[:-1]
        lines = data.split("\n")
        for line in lines:
            try:
                im_img_array.append(np.array(line.split("\t")).astype(float) * naiveScale)
            except:
                im_img_array.append(np.array(line.split(" ")).astype(float) * naiveScale)
    re_img_array = []
    with open(filePathRe) as f:
        data = f.read()[:-1]
        lines = data.split("\n")
        for line in lines:
            try:
                re_img_array.append(np.array(line.split("\t")).astype(float) * naiveScale)
            except:
                re_img_array.append(np.array(line.split(" ")).astype(float) * naiveScale)
    return np.asarray(im_img_array), np.asarray(re_img_array)


def mim2Conductivity(folderPath, fileNameIm, fileNameRe, csvFilePath, comsolScale, naiveScale):
    im_img_array, re_img_array = readImRe(folderPath, fileNameIm, fileNameRe, naiveScale)
    cond_array, im_sim, re_sim = readSimulatedImReCSV(csvFilePath, comsolScale)
    array_with_conductivity = []
    for im, re, conductivity in zip(im_sim, re_sim, cond_array):
        array_with_conductivity.append(((im, re), conductivity))

    conductivity_img_array = []
    for i in tqdm(range(len(im_img_array))):
        #         print(i/len(im_img_array))
        img_line = []
        for j in range(len(re_img_array)):
            pt = (im_img_array[i][j], re_img_array[i][j])
            conductivity_index = nearestIndex(pt, array_with_conductivity)
            # print(conductivity_index)
            img_line.append(array_with_conductivity[conductivity_index][1])
        conductivity_img_array.append(img_line)

    np.savetxt(folderPath + "/conductivity.txt", conductivity_img_array)
    data = np.loadtxt(folderPath + "/conductivity.txt")
    SaveParkTiff(data, data.shape[1], data.shape[0], folderPath+'/conductivity.tiff')
    return None


def readConductivity(folderPath):
    with open(folderPath + "/conductivity.txt") as f:
        data = f.read()[:-1]
        lines = data.split("\n")
        conductivity_f = []
        #     print(lines)
        for line in lines:
            conductivity_f.append(np.array(line.split(" ")).astype(float))  # use space as splitter instead of /t
    return conductivity_f

def undistort_1D(appear,coeff1,coeff2):
    # appear = coeff1*real^2 + coeff2*real
    # coeff1*real**2 + coeff2*real - appear = 0
    return (-coeff2+np.sqrt(coeff2**2-4*coeff1*-appear))/(2*coeff1)

def calibrate_xlist(xList,coeff1 = 0.06944444444444448, coeff2 = 2.4833333333333334, extra_scale_x = 1.0):
    new_xList = []
    for x in xList:
        new_xList.append(-undistort_1D(np.max(xList)-x,coeff1,coeff2)*extra_scale_x)
    return new_xList

# def calibrate_ylist(yList,coeff1 = 0.0152777777777777793, coeff2 = 5.250000000000001, extra_scale_y = 1.0):
def calibrate_ylist(yList,coeff1 = 0.04583333333333334, coeff2 = 3.5000000000000004, extra_scale_y = 1.0):
    new_yList = []
    for y in yList:
        new_yList.append(undistort_1D(y,coeff1,coeff2)*extra_scale_y)
    return new_yList


def resampleTraditionalMethod(img,X,Y,xmin,xmax,ymin,ymax,size):
    x_list = np.linspace(xmin,xmax,size)
    y_list = np.linspace(ymin,ymax,size)
    new_X,new_Y = np.meshgrid(x_list,y_list)
    new_img = np.zeros(new_X.shape)
    for i in tqdm(range(new_img.shape[0])):
        for j in range(new_img.shape[1]):
            min_list = []
            for ii in range(img.shape[0]):
                for jj in range(img.shape[1]):
                    if xmin<=X[ii][jj]<=xmax and ymin<=Y[ii][jj]<=ymax:
                        min_list.append([np.linalg.norm([new_X[i][j]-X[ii][jj],new_Y[i][j]-Y[ii][jj]]),[ii,jj]])
            target_ii,target_jj = sorted(min_list)[0][1]
            new_img[i,j] = img[target_ii,target_jj]
    return new_img,x_list,y_list

def resample(img,X,Y,xmin,xmax,ymin,ymax,size=None):
    if size==None:
        size=0
        for item in X[0]:
            if xmin<=item<=xmax:
                size+=1
    #print(size)
    x_list = np.linspace(xmin,xmax,size)
    y_list = np.linspace(ymin,ymax,size)
    new_X,new_Y = np.meshgrid(x_list,y_list)
    new_img = np.zeros(new_X.shape)
    new_img[:]=np.nan
    for ii in tqdm(range(img.shape[0])):
        for jj in range(img.shape[1]):
            xmin_list = []
            ymin_list = []
            if xmin<=X[ii][jj]<=xmax and ymin<=Y[ii][jj]<=ymax:
                for i in range(len(x_list)):
                    xmin_list.append([abs(X[ii][jj]-x_list[i]),i])
                for j in range(len(y_list)):
                    ymin_list.append([abs(Y[ii][jj]-y_list[j]),j])
                target_i = sorted(xmin_list)[0][1]
                target_j = sorted(ymin_list)[0][1]
                new_img[target_j,target_i] = img[ii,jj]
    for i in range(new_img.shape[0]):
        for j in range(new_img.shape[1]):
            if np.isnan(new_img[i,j]):
                new_img[i,j]=np.nanmean([new_img[(i-1)%size,j],new_img[(i+1)%size,j],new_img[i,(j-1)%size],new_img[i,(j+1)%size],
                                        new_img[(i-1)%size,(j-1)%size],new_img[(i+1)%size,(j+1)%size],new_img[(i+1)%size,(j-1)%size],new_img[(i-1)%size,(j+1)%size]])
                #print(new_img[i,j])
                # new_img=np.nan_to_num(new_img)
    return new_img,x_list,y_list

def radialAverageByLinecuts(graph,center,xAxis_or_xMeshgrid,yAxis_or_yMeshgrid,radialSteps=100,threshold=1.0,angleSteps = None,angleThreshold=0.01):
    graph = np.asarray(graph)
    graphShape = np.shape(graph)
    xShape = np.shape(xAxis_or_xMeshgrid)
    yShape = np.shape(yAxis_or_yMeshgrid)
    if len(xShape)==1 and len(yShape)==1:
        xx,yy = np.meshgrid(xAxis_or_xMeshgrid,yAxis_or_yMeshgrid)
        x_list = xAxis_or_xMeshgrid
        y_list = yAxis_or_yMeshgrid
    else:
        xx,yy = xAxis_or_xMeshgrid,yAxis_or_yMeshgrid
        x_list = xAxis_or_xMeshgrid[0]
        y_list = yAxis_or_yMeshgrid[:,0]
#     print(np.shape(xx),np.shape(yy),graphShape)
    if not np.shape(xx)==np.shape(yy)==graphShape:
        raise ValueError("image size is not equal to x size times y size")
    #print(y_list)
    graph_interpolated = interpolate.RectBivariateSpline(y_list, x_list, graph) #RectBivariateSpline: y before x. interp2d: x before y. (for both function before and function usage)
    #graph_interpolated = interpolate.interp2d(xAxis_or_xMeshgrid, yAxis_or_yMeshgrid, graph)
    bottomLeftPoint = np.array((xx[0][0],yy[0][0]))
    bottomRightPoint = np.array((xx[0][-1],yy[0][-1]))
    topLeftPoint = np.array((xx[-1][0],yy[-1][0]))
    topRightPoint = np.array((xx[-1][-1],yy[-1][-1]))
    radialMax = np.max([np.linalg.norm(center-bottomLeftPoint),np.linalg.norm(center-bottomRightPoint),\
                       np.linalg.norm(center-topLeftPoint),np.linalg.norm(center-topRightPoint)])
    rListPos = np.linspace(0,radialMax,radialSteps)
    rListNeg = (-rListPos[1:])[::-1]
    rList = np.concatenate([rListNeg,rListPos])
    rDict = defaultdict(list)
    for r in rList:
        rDict[r]=[]
#     rDictNeg = defaultdict(list)
#     for r in rListNeg:
#         rDictNeg[r]=[]
    angle_unit = None
    angle_list = None
    if angleSteps is None:
        raise ValueError("angleSteps should not be None")
    else:
        angleUnit = np.pi/angleSteps # changed to 2*np.pi instead of np.pi for radialAverageByLinecuts. Different from radialAverageByLines with opposite lists sperately.
        angleArray = np.array([angleUnit*ind for ind in range(angleSteps)])
#     print(angleArray)
    radialAverageByLinecuts.selectxy = []
    for angle in angleArray:
        tilted_rList_coords = [(r*np.cos(angle),r*np.sin(angle)) for r in rList]
        radialAverageByLinecuts.selectxy.append(tilted_rList_coords)
        for ind,(tilted_x,tilted_y) in enumerate(tilted_rList_coords):
            if np.min(xx) <= tilted_x <= np.max(xx) and np.min(yy) <= tilted_y <=np.max(yy):
                #rDict[rList[ind]].append(graph_interpolated(tilted_y,tilted_x)[0][0]) #RectBivariateSpline: y before x. interp2d: x before y. (for both function before and function usage)
                #print(graph_interpolated(tilted_x,tilted_y))
                rDict[rList[ind]].append(graph_interpolated(tilted_x,tilted_y)[0])
            else:
                rDict[rList[ind]].append(np.nan)
    zList = [np.nanmean(rDict[key]) for key in rList]
    nan_list = [ind for ind in range(len(zList)) if np.isnan(zList[ind])]
    rList = np.delete(rList,nan_list)
    zList = np.delete(zList,nan_list)
    return rList,zList,rDict


def diffusion_map(L,w0,pos_max=25,point_num=100,A=1):
    """
    By Zhaodong Chu via Matlab
    """
    l = np.linspace(-pos_max,pos_max,point_num);
    unit_length = 2*pos_max/point_num
    # l = (-0.1:0.1:0.1);
    num = len(l);  # number of pixels in one dimension

    [xx, yy] = np.meshgrid(l,l);
    R = np.sqrt(xx**2 + yy**2);  # distance matrix
    N = A * np.exp(-2*R**2/w0**2);  # Gaussian beam Nin

    z = np.zeros((num, num));   # initialize sum resuot
    middle = round(num/2);

    for  i in range(middle):
#         print(i/middle)
        for j in range(middle):

            x = xx[i,j];
            y = yy[i,j];
            # Nin = A * np.exp(-2*R(i,j)^2/w0^2);
            Nin = N[i,j];

            r = np.sqrt((xx - x)**2 + (yy - y)**2);

            Nr3 = Nin * unit_length **2 / (2 * np.pi * L**2) * np.exp(-r / L);   # Quadrant III
            Nr1 = Nr3[::-1,::-1];  # Quadrant I
            Nr2 = Nr3[::-1,:];  # Quadrnat III
            Nr4 = Nr3[:,::-1];

            if x == 0 and  y == 0:
                z = z + Nr3;
            elif x == 0:
                z = z + Nr3 + Nr2;
            elif y == 0:
                z = z + Nr3 + Nr4;
            else:
                z = z + Nr1 + Nr2 + Nr3 + Nr4;
    return xx,yy,z

def R2(y_real_list,y_fit_list):
    y_mean = np.mean(y_real_list)
    SS_tot = sum([(y_real - y_mean)**2 for y_real in y_real_list])
    SS_res = sum([(y_fit - y_real)**2 for y_real,y_fit in zip(y_real_list,y_fit_list)])
    R2 = 1 - SS_res/SS_tot
    return R2

def fit1(x_axis,z_axis,diffusion_simulation_database,extra_multiply,threshold = 0.97,fitrange=None):
    z_axis_norm = (np.array(z_axis)-np.min(z_axis))/(np.max(z_axis)-np.min(z_axis))/extra_multiply
    R2_score_list = []
    if fitrange != None:
        index_list1 = [item for item in range(len(x_axis)) if x_axis[item] >= fitrange[0] and x_axis[item] <= fitrange[1]]
        z_axis_norm = z_axis_norm[index_list1]
    for length in diffusion_simulation_database:
        xx,yy,z = diffusion_simulation_database[length]
        x_axis_fit = xx[0]
#         z_axis_fit = extra_multiply*z[round(z.shape[0]/2)]/np.max(z)*(np.max(zList_all[ind])-np.min(zList_all[ind]))
        z_axis_fit = (z[round(z.shape[0]/2)]-np.min(z[round(z.shape[0]/2)]))/(np.max(z[round(z.shape[0]/2)])-np.min(z[round(z.shape[0]/2)]))
        fit_func = interp1d(x_axis_fit,z_axis_fit)
#         print(x_axis)
        x_axis_clip = x_axis.clip(np.min(x_axis_fit),np.max(x_axis_fit))
#         print(x_axis_clip)
        z_axis_fit_for_R2 = fit_func(x_axis_clip)
        if fitrange!= None:
            index_list2 = [item for item in range(len(x_axis_clip)) if x_axis_clip[item]>=fitrange[0] and x_axis_clip[item]<=fitrange[1]]
        # print(len(x_axis),len(x_axis_clip),len(z_axis_norm),len(z_axis_fit_for_R2))
        # print(z_axis_norm[len(z_axis_norm)-1])
        # z_axis_norm = z_axis_norm[index_list1]
            z_axis_fit_for_R2 = z_axis_fit_for_R2[index_list2]
        R2_score = R2(z_axis_norm,z_axis_fit_for_R2)
#         diffusion_simulation_R2_score[length] = R2_score
#         print((z_axis_fit_for_R2))
        R2_score_list.append((R2_score,length))

    #threshold = 0.97 # you could adjust the threshold here to control the fitting range.
    R2_score_list_selected = []
    for R2_score,length in R2_score_list:
        if R2_score>threshold:
            R2_score_list_selected.append((R2_score,length))
    print(R2_score_list)
    print(R2_score_list_selected)
#     print(R2_score_list_selected,23333)
    score_lower,lower_boundary = R2_score_list_selected[0]
    score_upper,upper_boundary = R2_score_list_selected[-1]
    score_best,best_fit = max(R2_score_list_selected)
    print([lower_boundary,upper_boundary])
    print(best_fit)
#     error_list.append([lower_boundary,upper_boundary])
#     diffusion_list_fit_list.append(best_fit)
    return lower_boundary,best_fit,upper_boundary,score_lower,score_best,score_upper

def fit2(x_axis,z_axis,diffusion_simulation_database,extra_multiply):
    z_axis_norm = np.array(z_axis)/(np.max(z_axis)-np.min(z_axis))/extra_multiply
    R2_score_list = []
    diffusion_simulation_database_with_coeff = {}
    for c1 in np.round(np.linspace(0,1,11),2):
        print(c1)
        c2 = np.round(1.0-c1,2)
        for L1 in diffusion_simulation_database:
            for L2 in diffusion_simulation_database:
                xx,yy,_ = diffusion_simulation_database[L1] # either L1 or L2. Should be the same for xx and yy
                z1 = diffusion_simulation_database[L1][2]
                z1_axis_fit = (z1[round(z1.shape[0]/2)]-np.min(z1[round(z1.shape[0]/2)]))/(np.max(z1[round(z1.shape[0]/2)])-np.min(z1[round(z1.shape[0]/2)]))
                z2 = diffusion_simulation_database[L2][2]
                z2_axis_fit = (z2[round(z2.shape[0]/2)]-np.min(z2[round(z2.shape[0]/2)]))/(np.max(z2[round(z2.shape[0]/2)])-np.min(z2[round(z2.shape[0]/2)]))
                z_axis_fit = c1*z1_axis_fit+c2*z2_axis_fit
                #plt.plot(z_axis_fit)
                x_axis_fit = xx[0]
#                 z_axis_fit = z[round(z.shape[0]/2)]#(z[round(z.shape[0]/2)]-np.min(z[round(z.shape[0]/2)]))/(np.max(z[round(z.shape[0]/2)])-np.min(z[round(z.shape[0]/2)]))
                fit_func = interp1d(x_axis_fit,z_axis_fit)
                x_axis_clip = x_axis.clip(np.min(x_axis_fit),np.max(x_axis_fit))
                z_axis_fit_for_R2 = fit_func(x_axis_clip)
                R2_score = R2(z_axis_norm,z_axis_fit_for_R2)
                R2_score_list.append((R2_score,(c1,L1,c2,L2)))
    return R2_score_list