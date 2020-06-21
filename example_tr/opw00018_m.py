# TR/opw00018
from pykiwoom.kiwoom import *

# 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

# 계좌번호는 11을 붙여서 10자리임
account_list = kiwoom.GetLoginInfo("ACCNO")
account = account_list[0]
print(account)

# opw00018 요청
df = kiwoom.block_request("opw00018",
                          계좌번호=account,
                          비밀번호="",
                          비밀번호입력매체구분="00",
                          조회구분=2,
                          output="계좌평가잔고개별합산",
                          next=0)

print(df)
df.to_excel("opw00018.xlsx")
