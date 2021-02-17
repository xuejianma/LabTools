# """
# Created by Xuejian Ma at 6/18/2020.
# All rights reserved.
# """
# from readConductivities import im_img_all,re_img_all,conductivity_all
# import matplotlib.pyplot as plt
# plt.figure(figsize=(30,20))
# plt.imshow(conductivity_all[-1])
# plt.colorbar()
# # plt.show()
# plt.savefig("C:\Work\Xuejian Ma\Perovskite\imgs/test.png")


import sys
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import QObject, QThread, pyqtSignal



class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.centralWidget.setLayout(layout)

    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        self.stepLabel.setText(f"Long-Running Step: {n}")

    # def runLongTask(self):
    #     """Long-running task in 5 steps."""
    #     for i in range(5):
    #         sleep(1)
    #         self.reportProgress(i + 1)
    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(



            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""
        for i in range(5):
            sleep(1)
            self.progress.emit(i + 1)
            print(i)
        self.finished.emit()

app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())




# from PyQt5 import QtWidgets, QtGui, QtCore
#
#
# class ImageScroller(QtWidgets.QWidget):
#     def __init__(self):
#         self.chosen_points = []
#         QtWidgets.QWidget.__init__(self)
#         self._image = QtGui.QPixmap("image.png")
#
#     def paintEvent2(self, paint_event):
#         super().paintEvent(paint_event)
#         painter = QtGui.QPainter(self)
#         painter.drawPixmap(self.rect(), self._image)
#         pen = QtGui.QPen()
#         pen.setWidth(20)
#         painter.setPen(pen)
#         painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
#         painter.drawPoint(300, 300)
#         painter.drawLine(100, 100, 400, 400)
#         print(123123)
#         for pos in self.chosen_points:
#             painter.drawPoint(pos)
#
#     def mouseReleaseEvent(self, cursor_event):
#         self.chosen_points.append(cursor_event.pos())
#         # self.chosen_points.append(self.mapFromGlobal(QtGui.QCursor.pos()))
#         self.update()
#
#
# if __name__ == '__main__':
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     w = ImageScroller()
#     w.paintEvent = w.paintEvent2
#     w.resize(640, 480)
#     w.show()
#     sys.exit(app.exec_())