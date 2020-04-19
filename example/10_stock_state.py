from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

종목상태 = kiwoom.GetMasterStockState("005930")
print(종목상태)
