from pykiwoom.kiwoom import *

if __name__ == "__main__":
    km = KiwoomManager()
    km.put_method(("GetMasterCodeName", "005930")) 
    data = km.get_method()
    print(data)


