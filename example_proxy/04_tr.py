from pykiwoom.kiwoom import *

if __name__ == "__main__":
    proxy = KiwoomProxy()
    
    proxy.request(
        func="opt10001",
        input={
            "종목코드": "005930"
        },
        output=['종목코드', '종목명'],
        next=0, 
        screen="1000"
    )

    data = proxy.tr_dqueue.get()
    print(data)