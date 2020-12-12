"""
Created by Xuejian Ma at 11/30/2020.
All rights reserved.
"""
import time
import numpy as np
from datetime import timedelta



def getDS6_rawdata_run(inst):
    try:
        inst.write(":RUN")
    except:
        print("Error Running Oscilloscope")

def getDS6_rawdata_stop(inst, start=1, points=70000000, waiting_time=6,rawdata_list=None):
    try:
        wt = 0;
        inst.write(":STOP")
        inst.write(":WAV:MODE NORM")  # RAW means deeper raw data. NORM means displayed data
        time.sleep(wt)
        inst.write(":WAV:STAR " + str(start))
        time.sleep(wt)
        inst.write(":WAV:STOP " + str(points + start))
        time.sleep(wt)
        inst.write(":WAV:POIN " + str(points))
        time.sleep(wt)
        inst.write(":WAV:SOUR CHAN1")
        time.sleep(wt)
        inst.write(":WAV:RES")
        time.sleep(wt)
        inst.write(":WAV:BEG")
        time.sleep(wt)
        rawdata = inst.query_binary_values(':WAV:DATA?', datatype='B', is_big_endian=False)
        #         print("Memory depth is: %s"%inst.query(":ACQ:MDEP?"))
        #         print("Real number of data: %d"%len(rawdata))
        #         plt.plot(rawdata)
        #         plt.show()
        if rawdata_list!=None:
            # rawdata_list[:] = rawdata
            rawdata_list.append(rawdata)
        return rawdata
    except:
        print("Error getting rawdata")

def getDS6_rawdata(inst, start=1, points=70000000, waiting_time=6):
    try:
        wt = 0;
        inst.write(":RUN")
        time.sleep(waiting_time)
        inst.write(":STOP")
        inst.write(":WAV:MODE NORM")  # RAW means deeper raw data. NORM means displayed data
        time.sleep(wt)
        inst.write(":WAV:STAR " + str(start))
        time.sleep(wt)
        inst.write(":WAV:STOP " + str(points + start))
        time.sleep(wt)
        inst.write(":WAV:POIN " + str(points))
        time.sleep(wt)
        inst.write(":WAV:SOUR CHAN1")
        time.sleep(wt)
        inst.write(":WAV:RES")
        time.sleep(wt)
        inst.write(":WAV:BEG")
        time.sleep(wt)
        rawdata = inst.query_binary_values(':WAV:DATA?', datatype='B', is_big_endian=False)
        #         print("Memory depth is: %s"%inst.query(":ACQ:MDEP?"))
        #         print("Real number of data: %d"%len(rawdata))
        #         plt.plot(rawdata)
        #         plt.show()
        return rawdata
    except:
        print("Error getting rawdata")


def repeat(laser_controller, oscilloscope, steps=10, waiting_time=6,timeBetweenTurns=10):
    last_time = None
    onoff_list = []
    for i in range(steps):
        curr_time = time.time()

        print("Step: " + str(i + 1) + "/" + str(steps), end="\t")
        if last_time == None:
            print("Time left: Loading")
        else:
            print("Time left: " + str(timedelta(seconds=round((curr_time - last_time) * (steps - i)))))
        last_time = time.time()
        time.sleep(timeBetweenTurns)  # to make sure the controller does not turn on/off laser too frequently
        laser_controller.write("OUTP ON")
        rawdata_on = getDS6_rawdata(oscilloscope, waiting_time=waiting_time)
        time.sleep(timeBetweenTurns)  # to make sure the controller does not turn on/off laser too frequently
        laser_controller.write("OUTP OFF")
        rawdata_off = getDS6_rawdata(oscilloscope, waiting_time=waiting_time)
        onoff_list.append([rawdata_on, rawdata_off])
    print("Measurement Done")
    return onoff_list


def averager(onoff_list):
    on_mean = np.mean(np.array(onoff_list)[:, 0], axis=0)
    off_mean = np.mean(np.array(onoff_list)[:, 1], axis=0)
    result_mean = np.array([item1 - item2 for item1, item2 in zip(on_mean, off_mean)])
    return result_mean, on_mean, off_mean

def normalize(data):
    return (data-np.min(data))/(np.max(data)-np.min(data))*10 # factor of 10 prevents weird incapability to fit normally with x from 0 to 1

def denormalize(newData,data):
    return newData*(np.max(data)-np.min(data))/10+np.min(data) # factor of 10 prevents weird incapability to fit normally with x from 0 to 1

def decay1(t,A,tau,y0):
    return A*np.exp(-t/tau)+y0

def decay2(t,A1,A2,tau1,tau2,y0):
    return A1*np.exp(-t/tau1)+A2*np.exp(-t/tau2)+y0

def decay3(t,A1,A2,A3,tau1,tau2,tau3,y0):
    return A1*np.exp(-t/tau1)+A2*np.exp(-t/tau2)+A3*np.exp(-t/tau3)+y0