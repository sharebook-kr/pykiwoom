import sys
from pykiwoom.kiwoom import *
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect(block=True)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    app.exec_()