from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

name = kiwoom.GetMasterCodeName("005930")
print(name)
