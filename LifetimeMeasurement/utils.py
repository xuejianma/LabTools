"""
Created by Xuejian Ma at 11/30/2020.
All rights reserved.
"""
import time
import numpy as np
from datetime import timedelta



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