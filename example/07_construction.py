from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

감리구분 = kiwoom.GetMasterConstruction("005690")
print(감리구분)
