"""
Created by Xuejian Ma at 11/30/2020.
All rights reserved.
"""
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication

#def num(self, i):
def num(i):
    print(i)
    i += 1
    if i < 999:
        # run again after 2000ms with argument
        QtCore.QTimer.singleShot(2000, lambda: num(i))
        #QtCore.QTimer.singleShot(2000, lambda:self.num(i))

app = QApplication(sys.argv)

# run first time with start argument
num(1)
#QtCore.QTimer.singleShot(2000, lambda:num(1))

sys.exit(app.exec_())