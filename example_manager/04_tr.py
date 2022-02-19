from pykiwoom.kiwoom import *

if __name__ == "__main__":
    km = KiwoomManager()

    tr_cmd = {
        'rqname': "opt10081",
        'trcode': 'opt10081',
        'next': '0',
        'screen': '1000',
        'input': {
            "종목코드": "005930",
            "기준일자": "20200424",
            "수정주가구분": "",
        },
        'output': ['종목코드', '종목명', "일자", "현재가"]
    }

    km.put_tr(tr_cmd)
    data = km.get_tr()
    print(data)


