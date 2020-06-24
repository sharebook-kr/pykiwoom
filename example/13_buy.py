from pykiwoom.kiwoom import *
import time

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

# 주식계좌
accounts = kiwoom.GetLoginInfo("ACCNO")
stock_account = accounts[0]

# 삼성전자, 10주, 시장가주문 매수
for i in range(10):
    kiwoom.SendOrder("시장가매수", "0101", stock_account, 1, "005930", 10, 0, "03", "")
    time.sleep(0.2)
    print(i, "매수 완료")


