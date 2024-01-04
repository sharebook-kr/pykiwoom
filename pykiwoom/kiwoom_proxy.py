import sys
from PyQt5.QtWidgets import QApplication
import pythoncom
from pykiwoom.kiwoom import Kiwoom


class KiwoomProxy:
    app = QApplication(sys.argv)

    def __init__(self,
                 method_cqueue, method_dqueue,
                 tr_cqueue, tr_dqueue,
                 order_cqueue,
                 real_cqueue, real_dqueues,
                 cond_cqueue, cond_dqueue,
                 tr_cond_dqueue, real_cond_dqueue,
                 chejan_dqueue):
        # method queue
        self.method_cqueue  = method_cqueue
        self.method_dqueue  = method_dqueue

        # tr queue
        self.tr_cqueue      = tr_cqueue
        self.tr_dqueue      = tr_dqueue

        # order queue
        self.order_cqueue   = order_cqueue

        # real queue
        self.real_cqueue    = real_cqueue
        self.real_dqueues   = real_dqueues

        # condition queue
        self.cond_cqueue      = cond_cqueue         # tr/real condition command queue
        self.cond_dqueue      = cond_dqueue         # condition name list queue
        self.tr_cond_dqueue   = tr_cond_dqueue      # tr condition data queue
        self.real_cond_dqueue = real_cond_dqueue    # real condition data queue

        # chejan
        self.chejan_dqueue    = chejan_dqueue

        # kiwoom instance
        self.kiwoom = Kiwoom(
            tr_dqueue           = self.tr_dqueue,
            real_dqueues        = self.real_dqueues,
            tr_cond_dqueue      = self.tr_cond_dqueue,
            real_cond_dqueue    = self.real_cond_dqueue,
            chejan_dqueue       = self.chejan_dqueue
        )

        # kiwoom login
        self.kiwoom.CommConnect()

        # condition load
        self.kiwoom.GetConditionLoad()

        # subprocess run
        self.run()

    def run(self):
        while True:
            # method
            if not self.method_cqueue.empty():
                func_name, *params = self.method_cqueue.get()

                if hasattr(self.kiwoom, func_name):
                    func = getattr(self.kiwoom, func_name)
                    result = func(*params)
                    self.method_dqueue.put(result)

            # tr
            if not self.tr_cqueue.empty():
                tr_cmd = self.tr_cqueue.get()

                # parameters
                trcode = tr_cmd['trcode']
                rqname = tr_cmd.get('rqname', trcode)
                next = tr_cmd.get('next', 0)
                screen = tr_cmd['screen']
                input  = tr_cmd['input']
                output = tr_cmd['output']

                for id, value in input.items():
                    self.kiwoom.SetInputValue(id, value)

                self.kiwoom.tr_output[trcode] = output
                self.kiwoom.CommRqData(rqname, trcode, next, screen)

            # order
            if not self.order_cqueue.empty():
                order_cmd = self.order_cqueue.get()
                # parameters
                rqname      = order_cmd['rqname']
                screen      = order_cmd['screen']
                acc_no      = order_cmd['acc_no']
                order_type  = order_cmd['order_type']
                code        = order_cmd['code']
                quantity    = order_cmd['quantity']
                if order_cmd['hoga_gb'] == "03":
                    price = ""
                else:
                    price = order_cmd['price']
                hoga_gb     = order_cmd['hoga_gb']
                order_no    = order_cmd['order_no']

                # request api
                self.kiwoom.SendOrder(rqname, screen, acc_no, order_type, code, quantity, price, hoga_gb, order_no)

            # real
            if not self.real_cqueue.empty():
                real_cmd  = self.real_cqueue.get()

                # parameters
                func_name = real_cmd['func_name']   # SetRealReg/DisConnectRealData
                screen    = real_cmd.get('screen', "7999")

                if func_name == "SetRealReg":
                    code_list = real_cmd['code_list']   # ["005930", "000660"]
                    fid_list  = real_cmd['fid_list']    # ["215", "20", "214"]
                    opt_type  = real_cmd['opt_type']

                    # register fid
                    for ticker in code_list:
                        if len(self.kiwoom.real_fid) == 0 or opt_type == 0:
                            self.kiwoom.real_fid[ticker] = fid_list
                        else:
                            prev_ticker = list(self.kiwoom.real_fid.keys())[0]
                            prev_fid_list = self.kiwoom.real_fid[prev_ticker]
                            self.kiwoom.real_fid[ticker] = \
                                list(set(prev_fid_list + fid_list))

                    self.kiwoom.SetRealReg(screen, ";".join(code_list),
                        ";".join(fid_list), str(opt_type))
                elif func_name == "DisConnectRealData":
                    self.kiwoom.DisconnectRealData(screen)

            # condition
            # cond_cmd = {
            #   'screen': 1000,
            #   'cond_name': 'pbr', (condition name)
            #   'index': 0, (condition index)
            #   'search': 0/1/2
            # }
            if not self.cond_cqueue.empty():
                cond_cmd  = self.cond_cqueue.get()
                func_name = cond_cmd['func_name']   # SendCondition/SendConditionStop
                if func_name == "GetConditionNameList":
                    cond_list = self.kiwoom.GetConditionNameList()
                    self.cond_dqueue.put(cond_list)
                else:
                # parameters
                    cond_name = cond_cmd['cond_name']
                    index     = cond_cmd['index']
                    screen = cond_cmd['screen']
                    if func_name == "SendCondition":
                        search = cond_cmd['search']
                        self.kiwoom.SendCondition(screen, cond_name, index, search, block=False)
                    elif func_name == "SendConditionStop":
                        self.kiwoom.SendConditionStop(screen, cond_name, index)

            pythoncom.PumpWaitingMessages()

