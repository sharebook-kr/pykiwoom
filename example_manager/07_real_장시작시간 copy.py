import pykiwoom


if __name__ == "__main__":
    km = pykiwoom.KiwoomManager()

    real_cmd = {
        'func_name': "SetRealReg",
        'real_type': '장시작시간',
        'screen': '2000',
        'code_list': "", 
        'fid_list': "215;20;214",
        "opt_type": 0
    }

    km.put_real(real_cmd)
    while True:
        data = km.get_real('장시작시간')
        print(data)


