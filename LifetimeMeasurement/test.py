"""
Created by Xuejian Ma at 11/30/2020.
All rights reserved.
"""
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication
import time

#def num(self, i):
def num(i):
    # print(i)
    # i += 1
    print(i)

    if i < 1:
        QtCore.QTimer.singleShot(1000, lambda: num(i + 1))
        # run again after 2000ms with argument
        pass

        #QtCore.QTimer.singleShot(2000, lambda:self.num(i))
    return i

def happy():
    print('happy')
    print('happy in',time.time())

app = QApplication(sys.argv)

# run first time with start argument
# num(1)
# time1 = time.time()
# print(time1)
# QtCore.QTimer.singleShot(1000,lambda:happy)
# print(time.time())
# happy()
# print(time2-time1)
#QtCore.QTimer.singleShot(2000, lambda:num(1))

def output():
    print('in',time.time())

class testclass():
    def test(self):
        self.x = 1
        print(time.time())
        QtCore.QTimer.singleShot(2000, lambda: output(self.x))
        print(time.time())
        self.x = 0
        happy()

    def output(self):
        print('in', time.time())

    def test2(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(output)
        # time.sleep(5)
        self.timer.start(5000)#,QtCore.pyqtSlot("output()"))
        # time.sleep(5)
        print(1234)

    def test3(self):
        print(3333)





a = testclass()
a.test2()
# for _ in range(3):
#     QtCore.QThread.sleep(1)
#     a.test3()


# test2()

sys.exit(app.exec_())
# app.exec_()
# sys.exit()
