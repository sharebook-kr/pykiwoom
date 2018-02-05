import sys
from PyQt5.QtWidgets import *
from kiwoom import *


app = QApplication(sys.argv)
kiwoom = Kiwoom()
kiwoom.comm_connect()
code_list = kiwoom.get_code_list_by_market([0, 10])
print(code_list)
print(len(code_list))
