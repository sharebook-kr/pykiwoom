from pykiwoom.kiwoom import *

if __name__ == "__main__":
    proxy = KiwoomProxy()
    
    data = proxy.call(func="GetLoginInfo", params=["USER_NAME"])
    print(data)



