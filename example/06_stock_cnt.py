from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

stock_cnt = kiwoom.GetMasterListedStockCnt("005690")
print("삼성전자 상장주식수: ", stock_cnt)
