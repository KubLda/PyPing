from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QTimer
from data.mainPyPing import MainWindow
from threading import Thread
import sys



class MainWindow(QtWidgets.QMainWindow, MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

def init():
    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        w = MainWindow()
        w.show()
        sys.exit(app.exec_())
    # sys.exit(thread1.join())
    # sys.exit(thread2.join())
    
thread1 = Thread(target=init)
thread1.start()