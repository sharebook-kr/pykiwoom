class BaseManager:
    def __init__(self, ocx, cqueue, dqueue) -> None:
        self.ocx = ocx
        self.cqueue = cqueue 
        self.dqueue = dqueue
        self.run()

    def run(self):
        pass


class MethodManager(BaseManager):
    def __init__(self, ocx, cqueue, dqueue) -> None:
        super().__init__(ocx, cqueue, dqueue)

    def run(self):
        while True: 
            func_name, *params = self.cqueue.get()     # ["GetRepeatCnt", "opt1001", "req"]

            if hasattr(self.ocx, func_name):
                func = getattr(self.ocx, func_name)
                data = func(*params)
                self.dqueue.put(data)


class OrderManager(BaseManager):
    def __init__(self, ocx, cqueue, dqueue) -> None:
        super().__init__(ocx, cqueue, dqueue)

    def run(self):
        while True: 
            cmds, *params = self.cqueue.get()     # ["SendOrder", "rqname", "1000", "..."] 
            self.ocx.SendOrder(*params)


class TransactionManager(BaseManager):
    def __init__(self, ocx, cqueue, dqueue) -> None:
        super().__init__(ocx, cqueue, dqueue)

    def run(self):
        while True: 
            self.cqueue.get()
            self.dqueue.put()

