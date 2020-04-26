from pykiwoom.kiwoom import *
import time
import pandas as pd

# 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

# TR 요청
#dfs = []
df = kiwoom.block_request("opt10081",
                          종목코드="005930",
                          기준일자="20200424",
                          수정주가구분=1,
                          output="주식일봉차트조회",
                          next=0)
print(df.head())
#dfs.append(df)

#while kiwoom.tr_remained:
#    df = kiwoom.block_request("opt10081",
#                              종목코드="005930",
#                              기준일자="20200424",
#                              수정주가구분=1,
#                              output="주식일봉차트조회",
#                              next=2)
#    dfs.append(df)
#    time.sleep(1)
#
#df = pd.concat(dfs)
#df.to_excel("005930.xlsx")
