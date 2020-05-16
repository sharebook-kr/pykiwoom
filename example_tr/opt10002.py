# opt10002: 주식 거래원 요청
from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

df = kiwoom.block_request("opt10002",
                          종목코드="005930",
                          output="주식거래원",
                          next=0)
print(df)
