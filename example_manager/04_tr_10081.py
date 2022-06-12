import pykiwoom

if __name__ == "__main__":
    km = pykiwoom.KiwoomManager()

    tr_cmd = {
        'rqname': "opt10081",
        'trcode': 'opt10081',
        'next': '0',
        'screen': '1000',
        'input': {
            "종목코드": "005930",
            "기준일자": "20220612",
            "수정주가구분": "0",
        },
        'output': ['종목코드', "일자", "시가", "고가", "저가", "현재가"]
    }

    km.put_tr(tr_cmd)
    data, remain = km.get_tr()
    print(data)


