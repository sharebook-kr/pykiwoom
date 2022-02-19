# pykiwoom
Python Wrapper for Kiwoom Open API+

# Books 

https://wikidocs.net/book/1173


# Examples

## 로그인 

```
from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
```


# 서브 프로세스로 사용하기 

키움 클래스를 별도의 서브 프로세스로 사용하려면 KiwoomManager를 사용하면 됩니다. 이를 통해 사용자 프로그램과 키움 클래스를 완전히 분리할 수 있습니다. 

## 메서드

```
from pykiwoom.kiwoom import *

if __name__ == "__main__":
    km = KiwoomManager()
    km.put_method(("GetMasterCodeName", "005930")) 
    data = km.get_method()
    print(data)
```

## TR 

```
from pykiwoom.kiwoom import *

if __name__ == "__main__":
    km = KiwoomManager()

    tr_cmd = {
        'rqname': "opt10001",
        'trcode': 'opt10001',
        'next': '0',
        'screen': '1000',
        'input': {
            "종목코드": "005930"
        },
        'output': ['종목코드', '종목명', 'PER', 'PBR']
    }

    km.put_tr(tr_cmd)
    data = km.get_tr()
    print(data)
```

## TR 연속 조회

TR 연속 조회의 경우 이전 TR 데이터를 가져간 후 다시 요청해야합니다. 

```
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
        'output': ["일자", "시가", "고가", "저가", "현재가"]
    }

    for i in range(2):
        if i != 0:
            tr_cmd['next'] = '2'
        
        km.put_tr(tr_cmd)
        data = km.get_tr()
        print(data)
```
