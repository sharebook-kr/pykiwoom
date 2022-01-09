from pykiwoom.kiwoom import *

if __name__ == "__main__":
    proxy = KiwoomProxy()
    
    data = proxy.fetch(func="GetLoginInfo", params=["USER_NAME"])
    print(data)



