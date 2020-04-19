from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

상장일 = kiwoom.GetMasterListedSTockDate("005690")
print(상장일)
print(type(상장일))        # datetime.datetime 객체
