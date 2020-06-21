# TR/opw00001
from pykiwoom.kiwoom import *

# 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

# 계좌번호는 11을 붙여서 10자리임
account_list = kiwoom.GetLoginInfo("ACCNO")
account = account_list[0]
print(account)

# opw00001 요청
df = kiwoom.block_request("opw00001",
                          계좌번호=account,
                          비밀번호="",
                          비밀번호입력매체구분="00",
                          조회구분=1,
                          output="예수금상세현황",
                          next=0)

# 예수금
#예수금 = int(df['예수금'][0])
#print(예수금)
#print(df)
for column in df.columns:
    print(column, df.loc[0][column])