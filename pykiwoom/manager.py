import time

class BaseManager:
    def __init__(self, kiwoom, ocx, cqueue, dqueue) -> None:
        self.kiwoom = kiwoom
        self.ocx = ocx
        self.cqueue = cqueue 
        self.dqueue = dqueue
        self.run()


class MethodManager(BaseManager):
    def __init__(self, kiwoom, ocx, cqueue, dqueue) -> None:
        super().__init__(kiwoom, ocx, cqueue, dqueue)

    def run(self):
        while True: 
            func_name, *params = self.cqueue.get()     # ["GetRepeatCnt", "opt1001", "req"]

            if hasattr(self.kiwoom, func_name):
                func = getattr(self.kiwoom, func_name)
                data = func(*params)
                self.dqueue.put(data)


class OrderManager(BaseManager):
    def __init__(self, kiwoom, ocx, cqueue, dqueue) -> None:
        super().__init__(kiwoom, ocx, cqueue, dqueue)

    def run(self):
        while True: 
            cmds, *params = self.cqueue.get()     # ["SendOrder", "rqname", "1000", "..."] 
            self.kiwoom.SendOrder(*params)
            time.sleep(0.2)


class TransactionManager(BaseManager):
    def __init__(self, kiwoom, ocx, cqueue, dqueue) -> None:
        super().__init__(kiwoom, ocx, cqueue, dqueue)

    def run(self):
        print("TransactionManager::run")
        while True: 
            # cmd = { 
            #   "func": "opt1001",
            #   "input" : {
            #       "종목코드" : "005930"
            #   }, 
            #   "output": [
            #       "종목코드",
            #       "종목명"
            #   ],
            #   "next": 0/2, 
            #   "screen": "1000"
            # } 
            cmd = self.cqueue.get()   
            print(cmd)

            trcode = cmd['func']
            next = cmd['next']
            screen = cmd['screen']
            input = cmd['input']
            output = cmd['output']

            for id, value in input.items():
                self.kiwoom.SetInputValue(id, value)
                print(id, value)

            self.kiwoom.CommRqData(trcode, trcode, next, screen)

            # 출력 중 가져올 아이템을 queue로 전달
            self.kiwoom.tr_item_queue.put(output)


