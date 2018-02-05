from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slot()

    def _create_kiwoom_instance(self):
        """
        키움 ocx 객체 생성
        :return: None
        """
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slot(self):
        """
        시그널(이벤트)과 슬롯(이벤트 처리 메서드)를 연결
        :return:
        """
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        """
        로그인
        :return: None
        """
        self.dynamicCall("CommConnect()")
        self.login_loop = QEventLoop()
        self.login_loop.exec_()

    def _event_connect(self, err):
        """
        로그인 이벤트를 처리하는 메서드
        :param err: 0: 로그인 성공, 1: 로그인 실패
        :return: None
        """
        if err == 0:
            print("로그인 성공")
        else:
            print("로그인 실패")

        self.login_loop.exit()

    def get_code_list_by_market(self, market_list):
        """
        시장 구분에 따라 종목 코드를 얻어오는 메서드
        :param market: list e.g. [0, 10]
        :return: list 코드 리스트
        """
        code_list = []

        for market in market_list:
            ret = self.dynamicCall("GetCodeListByMarket(QString)", market)
            codes = ret.split(';')[:-1]
            code_list.extend(codes)

        return code_list

    def get_master_code_name(self, code):
        """
        종목 코드의 한글명을 반환하는 메서드
        :param code: str e.g. "000660"
        :return: str
        """
        ret = self.dynamicCall("GetMasterCodeName(QString)", code)
        return ret

    def get_master_listed_stock_date(self, code):
        """
        종목 코드의 상장일을 반환
        :param code:
        :return:
        """
        ret = self.dynamicCall("GetMasterListedStockDate(QString)", code)
        return ret

    def get_master_construction(self, code):
        """
        종목 코드의 감리 구분을 반환하는 메서드 (정상/투자주의/투자경고/투자위험/투자주의환기종목)
        :param code:
        :return:
        """
        ret = self.dynamicCall("GetMasterConstruction(QString)", code)
        return ret

    def set_input_value(self, id, value):
        """
        Transaction 입력 값을 설정하는 메서드
        :param id: str, e.g. "종목코드"
        :param value: str, e.g. "000660"
        :return: None
        """
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        """
        Transaction을 서버로 송신하는 메서드
        :param rqname:
        :param trcode:
        :param next:
        :param screen_no:
        :return:
        """
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no);
        self.tr_loop = QEventLoop()
        self.tr_loop.exec_()

    def get_comm_data(self, trcode, rqname, index, item_name):
        """
        서버로부터 수신 데이터를 반환하는 메서드
        :param trcode:
        :param rqname:
        :param index:
        :param item_name:
        :return:
        """
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, item_name)
        return ret.strip()

    def _receive_tr_data(self, screen_no, rqname, trcode, recode_name, next, unused1, unused2, unused3, unused4):
        if rqname == "opt10001_req":
            self.pbr = self.get_comm_data(trcode, rqname, 0, "PBR")
            self.per = self.get_comm_data(trcode, rqname, 0, "PER")

        try:
            self.tr_loop.exit()
        except:
            pass