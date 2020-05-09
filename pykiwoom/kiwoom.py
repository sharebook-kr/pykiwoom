import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import pythoncom
import datetime
from pykiwoom import parser
import pandas as pd


class Kiwoom:
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.connected = False              # for login event
        self.received = False               # for tr event
        self.tr_items = None                # tr input/output items
        self.tr_data = None                 # tr output data
        self.tr_record = None
        self.tr_remained = False
        self.condition_loaded = False
        self._set_signals_slots()

    def _handler_login(self, err_code):
        if err_code == 0:
            self.connected = True

    def _handler_condition_load(self, ret, msg):
        if ret == 1:
            self.condition_loaded = True

    def _handler_tr_condition(self, screen_no, code_list, cond_name, cond_index, next):
        codes = code_list.split(';')[:-1]
        self.tr_condition_data = codes
        self.tr_condition_loaded= True

    def _handler_tr(self, screen, rqname, trcode, record, next):
        record = None
        items = None

        # remained data
        if next == '2':
            self.tr_remained = True
        else:
            self.tr_remained = False

        for output in self.tr_items['output']:
            record = list(output.keys())[0]
            items = list(output.values())[0]
            if record == self.tr_record:
                break

        rows = self.GetRepeatCnt(trcode, rqname)
        if rows == 0:
            rows = 1

        data_list = []
        for row in range(rows):
            row_data = []
            for item in items:
                data = self.GetCommData(trcode, rqname, row, item)
                row_data.append(data)
            data_list.append(row_data)

        # data to DataFrame
        df = pd.DataFrame(data=data_list, columns=items)
        self.tr_data = df
        self.received = True

    def _set_signals_slots(self):
        self.ocx.OnEventConnect.connect(self._handler_login)
        self.ocx.OnReceiveTrData.connect(self._handler_tr)
        self.ocx.OnReceiveConditionVer.connect(self._handler_condition_load)
        self.ocx.OnReceiveTrCondition.connect(self._handler_tr_condition)

    def CommConnect(self, block=True):
        self.ocx.dynamicCall("CommConnect()")
        if block:
            while not self.connected:
                pythoncom.PumpWaitingMessages()

    def GetConditionLoad(self, block=True):
        self.condition_loaded = False
        self.ocx.dynamicCall("GetConditionLoad()")
        if block:
            while not self.condition_loaded:
                pythoncom.PumpWaitingMessages()

    def GetLoginInfo(self, tag):
        data = self.ocx.dynamicCall("GetLoginInfo(QString)", tag)
        return data

    def GetCodeListByMarket(self, market):
        data = self.ocx.dynamicCall("GetCodeListByMarket(QString)", market)
        tokens = data.split(';')[:-1]
        return tokens

    def GetMasterCodeName(self, code):
        data = self.ocx.dynamicCall("GetMasterCodeName(QString)", code)
        return data

    def GetConnectState(self):
        state = self.ocx.dynamicCall("GetConnectState()")
        return state

    def GetMasterListedStockCnt(self, code):
        data = self.ocx.dynamicCall("GetMasterListedStockCnt(QString)", code)
        return data

    def GetMasterConstruction(self, code):
        data = self.ocx.dynamicCall("GetMasterConstruction(QString)", code)
        return data

    def GetMasterListedSTockDate(self, code):
        data = self.ocx.dynamicCall("GetMasterListedStockDate(QString)", code)
        return datetime.datetime.strptime(data, "%Y%m%d")

    def GetMasterLastPrice(self, code):
        data = self.ocx.dynamicCall("GetMasterLastPrice(QString)", code)
        return int(data)

    def GetMasterStockState(self, code):
        data = self.ocx.dynamicCall("GetMasterStockState(QString)", code)
        return data.split("|")

    def GetThemeGroupList(self, type):
        data = self.ocx.dynamicCall("GetThemeGroupList(int)", type)
        tokens = data.split(';')
        grp = {x.split('|')[1]:x.split('|')[0] for x in tokens}
        return grp

    def GetThemeGroupCode(self, theme_code):
        data = self.ocx.dynamicCall("GetThemeGroupCode(QString)", theme_code)
        data = data.split(';')
        return [x[1:] for x in data]

    def SetInputValue(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def GetDataCount(self, record):
        count = self.ocx.dynamicCall("GetDataCount(QString)", record)
        return count

    def GetRepeatCnt(self, trcode, rqname):
        count = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return count

    def CommRqData(self, rqname, trcode, next, screen):
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen)

    def GetCommData(self, trcode, rqname, index, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, item)
        return data.strip()

    def GetCommDataEx(self, trcode, record):
        data = self.ocx.dynamicCall("GetCommDataEx(QString, QString)", trcode, record)
        return data

    def block_request(self, *args, **kwargs):
        trcode = args[0].lower()
        lines = parser.read_enc(trcode)
        self.tr_items = parser.parse_dat(trcode, lines)
        self.tr_record = kwargs["output"]
        next = kwargs["next"]

        # set input
        for id in kwargs:
            if id.lower() is not "output" and id.lower() is not "next":
                self.SetInputValue(id, kwargs[id])

        # initialize
        self.received = False
        self.tr_remained = False

        # request
        self.CommRqData(trcode, trcode, next, "0101")
        while not self.received:
            pythoncom.PumpWaitingMessages()

        return self.tr_data

    def GetConditionNameList(self):
        data = self.ocx.dynamicCall("GetConditionNameList()")
        conditions = data.split(";")[:-1]

        # [('000', 'perpbr'), ('001', 'macd'), ...]
        result = []
        for condition in conditions:
            cond_index, cond_name = condition.split('^')
            result.append((cond_index, cond_name))

        return result

    def SendCondition(self, screen, cond_name, cond_index, search):
        self.tr_condition_loaded = False
        self.ocx.dynamicCall("SendCondition(QString, QString, int, int)", screen, cond_name, cond_index, search)

        while not self.tr_condition_loaded:
            pythoncom.PumpWaitingMessages()

        return self.tr_condition_data


if not QApplication.instance():
    app = QApplication(sys.argv)


if __name__ == "__main__":
    # 로그인
    kiwoom = Kiwoom()
    kiwoom.CommConnect(block=True)

    # 조건식 load
    kiwoom.GetConditionLoad()

    conditions = kiwoom.GetConditionNameList()

    # 0번 조건식에 해당하는 종목 리스트 출력
    condition_index = conditions[0][0]
    condition_name = conditions[0][1]
    codes = kiwoom.SendCondition("0101", condition_name, condition_index, 0)

    print(codes)