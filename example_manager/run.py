import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.dynamicCall("CommConnect()")
        self.ocx.OnEventConnect.connect(self.OnEventConnect)

    def OnEventConnect(self, err_code):
        print(err_code)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()