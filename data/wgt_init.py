from PySide2 import QtWidgets
from data.widgetPyPing import PingForm
import sys


class MyWidget(QtWidgets.QWidget, PingForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())