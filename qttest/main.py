# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QFileDialog
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap,QMouseEvent


class qttest(QWidget):
    def __init__(self):
        super(qttest, self).__init__()
        self.load_ui()
        self.showImage()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def showImage(self,file='img.jpg'):
        pixmap = QPixmap(file)
        pixmap1 = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        self.ui.label_2.setPixmap(pixmap1)
        self.ui.label_2.mousePressEvent = self.getPos


    def getPos(self,event):
        x = event.pos().x()
        y = event.pos().y()
        print(x,y)


if __name__ == "__main__":
    app = QApplication([])
    widget = qttest()
    widget.show()
    sys.exit(app.exec_())











# # This Python file uses the following encoding: utf-8
# import sys
# import os
#
#
# from PySide2.QtWidgets import QApplication, QWidget, QFileDialog
# from PySide2.QtCore import QFile, Qt
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtGui import QPixmap,QMouseEvent
#
#
# class qttest(QWidget):
#     def __init__(self):
#         super(qttest, self).__init__()
#         self.load_ui()
#         self.showImage()
#         self.pressButton1()
#         self.pressButton_2()
#         # self.ui.label_2.mousePressEvent(self)
#         # self.setCentralWidget(self.ui.label_4)
#
#
#     def load_ui(self):
#         loader = QUiLoader()
#         path = os.path.join(os.path.dirname(__file__), "form.ui")
#         ui_file = QFile(path)
#         ui_file.open(QFile.ReadOnly)
#         self.ui = loader.load(ui_file, self)
#         ui_file.close()
#
#     def pressButton1(self):
#         self.ui.pushButton.clicked.connect(self.clicked)
#     def clicked(self):
#         self.ui.label.setText('pressed!')
#     def showImage(self,file='img.jpg'):
#         pixmap = QPixmap(file)
#         pixmap1 = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
#
#         self.ui.label_2.setPixmap(pixmap1)
#         self.ui.label_2.mousePressEvent  = self.getPos
#
#         # self.ui.label_2.mousePressEvent(QMouseEvent)
#         # self.ui.label_2.clicked.connect(self.clicked)
#
#
#     def pressButton_2(self):
#
#         self.ui.pushButton_2.clicked.connect(self.selectFile)
#         # print(self.ui.pushButton_2.__dict__)
#
#     def selectFile(self):
#         filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.',
#                                                              )
#         self.showImage(file=filename)
#         self.ui.label_3.setText(filename)
#     def getPos(self,event):
#         # event.accept()
#         x = event.pos().x()
#         y = event.pos().y()
#         print(x,y)
#         # raise ValueError(1234)
#         self.ui.label_4.setText(str(x)+','+str(y))
#         # self.ui.label_2.mousePressEvent(event)
#
# if __name__ == "__main__":
#     app = QApplication([])
#     widget = qttest()
#     widget.show()
#     sys.exit(app.exec_())
