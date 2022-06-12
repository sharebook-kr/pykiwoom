import sys 
from PyQt5.QtWidgets import *
import pykiwoom

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.km = pykiwoom.KiwoomManager()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()