import pykiwoom

if __name__ == "__main__":
    km = pykiwoom.KiwoomManager()
    km.put_method(("GetMasterCodeName", "005930")) 
    data = km.get_method()
    print(data)


