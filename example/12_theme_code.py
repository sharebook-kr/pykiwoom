from pykiwoom.kiwoom import *
import pprint

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

tickers = kiwoom.GetThemeGroupCode('141')
print(tickers)
