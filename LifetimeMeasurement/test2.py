import sys
from PyQt5 import QtCore, QtWidgets


class ProcessThread(QtCore.QThread):
    def run(self):
        # while True:
        #     self.optimize()
        for _ in range(3):
            QtCore.QThread.sleep(1)
            self.measure_property()

    def optimize(self):
        print("optimize")

    def measure_property(self):
        print("measure_property")


class MyForm():
    def __init__(self):
        self.ui = QtWidgets.QDialog()
        self.thread = ProcessThread(self.ui)
        self.button = QtWidgets.QPushButton("Press me")
        self.button.clicked.connect(self.thread.start)
        self.waiting_interval = 10000
        lay = QtWidgets.QVBoxLayout(self.ui)
        lay.addWidget(self.button)
        self.ui.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w=MyForm()
    sys.exit(app.exec_())