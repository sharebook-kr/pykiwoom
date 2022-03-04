# 시장의 종목코드 
import pykiwoom

if __name__ == "__main__":
    km = pykiwoom.KiwoomManager()
    km.put_method(("GetCodeListByMarket", "0"))
    data = km.get_method() 
    print(data)


