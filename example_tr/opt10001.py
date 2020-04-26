# opt10001: 주식 기본정보 요청
from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

df = kiwoom.block_request("opt10001", 종목코드="005930")
print(df)
