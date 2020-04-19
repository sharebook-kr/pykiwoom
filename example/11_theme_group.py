from pykiwoom.kiwoom import *
import pprint

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

group = kiwoom.GetThemeGroupList(1)
pprint.pprint(group)

