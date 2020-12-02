    def measureEachTurn(self,i,laser_controller,oscilloscope,stepsDouble,waiting_time,timeBetweenTurns):
        if i<stepsDouble:

            getDS6_rawdata_run(oscilloscope)

            QTimer.singleShot(int(timeBetweenTurns * 1e3),
                              lambda: self.measureEachTurn(i+1, laser_controller,oscilloscope,stepsDouble,
                                                           waiting_time,timeBetweenTurns+waiting_time))
            if i >= 0:

                if i%2==0:
                    self.measureOn(laser_controller, oscilloscope,waiting_time=waiting_time)
                    # self.on_list.append(rawdata_on)
                    # print(i)
                    # print(self.on_list)
                else:
                    self.measureOff(laser_controller, oscilloscope,waiting_time=waiting_time)
                    # self.on_list.append(rawdata_off)
                    # print(i)
                    # print(self.off_list)
                    # currentDecay = np.asarray([item1 - item2 for item1, item2 in zip(self.on_list[-1], self.off_list[-1])])
                    # self.widget_currentDecay.plot(currentDecay)
                QTimer.singleShot(int(waiting_time * 1e3),lambda:self.progressBar.setValue(int((i + 1) / stepsDouble * 100)))


    def measureEachTurn1(self, i, laser_controller, oscilloscope, last_time, steps, waiting_time=6,
                         timeBetweenTurns=10):
        curr_time = time.time()

        print("Step: " + str(i + 1) + "/" + str(steps), end="\t")
        if last_time == None:
            print("Time left: Loading")
        else:
            print("Time left: " + str(timedelta(seconds=round((curr_time - last_time) * (steps - i)))))
        last_time = time.time()
        time.sleep(timeBetweenTurns)  # to make sure the controller does not turn on/off laser too frequently
        # QtTest.QTest.qWait(timeBetweenTurns*1e3)
        QThread.sleep(timeBetweenTurns)
        laser_controller.write("OUTP ON")
        # rawdata_on = getDS6_rawdata(oscilloscope, waiting_time=waiting_time)
        # time.sleep(timeBetweenTurns)  # to make sure the controller does not turn on/off laser too frequently
        # QtTest.QTest.qWait(timeBetweenTurns * 1e3)
        QThread.sleep(timeBetweenTurns)

        laser_controller.write("OUTP OFF")
        # rawdata_off = getDS6_rawdata(oscilloscope, waiting_time=waiting_time)
        # onoff_list.append([rawdata_on, rawdata_off])
        # return [rawdata_on, rawdata_off],last_time


    def measureOn(self, laser_controller, oscilloscope, waiting_time):
        # rawdata_on = []
        laser_controller.write("OUTP ON")
        # getDS6_rawdata_run(oscilloscope)
        # print(waiting_time)
        # time1 = time.time()
        QTimer.singleShot(int(waiting_time * 1e3), lambda: getDS6_rawdata_stop(oscilloscope, rawdata_list=self.on_list))
        # rawdata_on = getDS6_rawdata_stop(oscilloscope)
        # time2 = time.time()
        # print(time2-time1)
        # print(rawdata_on)
        # rawdata_on = getDS6_rawdata_stop(oscilloscope, waiting_time=waiting_time)
        # return rawdata_on


    def measureOff(self, laser_controller, oscilloscope, waiting_time):
        # rawdata_off = []
        laser_controller.write("OUTP OFF")
        # getDS6_rawdata_run(oscilloscope)
        QTimer.singleShot(int(waiting_time * 1e3),
                          lambda: getDS6_rawdata_stop(oscilloscope, rawdata_list=self.off_list))
        # rawdata_off = getDS6_rawdata_stop(oscilloscope)
        # rawdata_off = getDS6_rawdata(oscilloscope, waiting_time=waiting_time)
        # return rawdata_off

        QTimer.singleShot(int(waiting_time * 1e3) + int(0.5e3), self.plotDecay)


    def getDS6_rawdata_stop(self):
        return getDS6_rawdata_stop()





      # onoff_list = repeat(laser_controller, oscilloscope, steps = 10, waiting_time = 6)

        last_time = None
        onoff_list = []


    # for i in range(steps):
    #     [rawdata_on, rawdata_off],last_time = self.measureEachTurn1(i,laser_controller,oscilloscope,last_time,steps,waiting_time=waiting_time,timeBetweenTurns=timeBetweenTurns)
    #     currentDecay = np.asarray([item1-item2 for item1,item2 in zip(rawdata_on,rawdata_off)])
    #     self.widget_currentDecay.plot(currentDecay)