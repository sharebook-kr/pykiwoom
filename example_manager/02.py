# 시장의 종목코드 
import pykiwoom

if __name__ == "__main__":
    km = pykiwoom.KiwoomManager()
    km.put_method(("GetCodeListByMarket", "0"))
    km.put_method(("GetCodeListByMarket", "10"))
    kospi = km.get_method() 
    kosdaq = km.get_method() 
    all = kospi + kosdaq
    print(len(all))
    


