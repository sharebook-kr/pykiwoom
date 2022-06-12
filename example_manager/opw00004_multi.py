import pykiwoom


if __name__ == "__main__":
    km = pykiwoom.KiwoomManager()

    tr_cmd = {
        'rqname': "opw00004",
        'trcode': 'opw00004',
        'next': '0',
        'screen': '1000',
        'input': {
            "계좌번호": "5469578910",
            "비밀번호": "8117",
            "상장폐지조회구분": 0,
            "비밀번호입력매체구분": "00"
        },
        'output': ["종목코드", "종목명", "현재가"]
    }

    km.put_tr(tr_cmd)
    data = km.get_tr()
    print(data)