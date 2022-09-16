from pykiwoom import KiwoomManager

if __name__ == "__main__":
    km = KiwoomManager()
    cmd = {
        'func_name': 'GetConditionNameList'
    }
    km.put_cond(cmd)
    data = km.get_cond(method=True)
    print(data)

    cmd = {
        'func_name': 'SendCondition',
        'screen': '1010',                   # screen
        'cond_name': 'golden',              # condition name
        'index': 0,                         # condition index
        'search': 1
    }

    km.put_cond(cmd)
    while True:
        data = km.get_cond(real=True)
        print(data)