# 시장의 종목코드 
from pykiwoom.kiwoom import *

if __name__ == "__main__":
    proxy = KiwoomProxy()
    
    data = proxy.fetch(func="GetCodeListByMarket", params=["0"])
    print(type(data), len(data))


