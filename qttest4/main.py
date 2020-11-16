# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QMainWindow,QWidget,QVBoxLayout
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class qttest4(QMainWindow):
    def __init__(self):
        super(qttest4, self).__init__()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

if __name__ == "__main__":
    app = QApplication([])
    widget = qttest4()
    widget.show()
    sys.exit(app.exec_())
