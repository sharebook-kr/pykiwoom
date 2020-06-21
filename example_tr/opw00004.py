# TR/opw00004
from pykiwoom.kiwoom import *

# 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

# 계좌번호는 11을 붙여서 10자리임
account_list = kiwoom.GetLoginInfo("ACCNO")
account = account_list[0]
print(account)

# opw00001 요청
df = kiwoom.block_request("opw00004",
                          계좌번호=account,
                          비밀번호="",
                          상장폐지조회구분=0,
                          비밀번호입력매체구분="00",
                          output="계좌평가현황",
                          next=0)

print(df)
for column in df.columns:
    print(column, df.loc[0][column])
