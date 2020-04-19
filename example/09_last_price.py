from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

전일가 = kiwoom.GetMasterLastPrice("005930")
print(int(전일가))
print(type(전일가))
