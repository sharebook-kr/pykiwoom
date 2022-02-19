# 시장의 종목코드 
from pykiwoom.kiwoom import *

if __name__ == "__main__":
    km = KiwoomManager()
    km.put_method(("GetCodeListByMarket", "0"))
    data = km.get_method() 
    print(data)


