from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

tickers = kiwoom.GetThemeGroupCode('141')
print(tickers)
