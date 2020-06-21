from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)


kiwoom.GetConditionLoad()
conditions = kiwoom.GetConditionNameList()
condition_index, condition_name = conditions[0]
codes = kiwoom.SendCondition("0101", condition_name, condition_index, 0)
print(codes)