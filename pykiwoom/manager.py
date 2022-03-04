import multiprocessing as mp
from .kiwoom import *
from .real_type import *

REAL_TYPE_NUM = len(real_index) 

class KiwoomManager:
    def __init__(self, daemon=True):
        # SubProcess
        # queue
        self.method_cqueue  = mp.Queue()
        self.method_dqueue  = mp.Queue()
        self.tr_cqueue      = mp.Queue()
        self.tr_dqueue      = mp.Queue()
        self.order_cqueue   = mp.Queue()

        # real queue
        self.real_cqueue    = mp.Queue()
        self.real_dqueues   = [
            mp.Queue() for x in range(REAL_TYPE_NUM)
        ]

        self.proxy = mp.Process(
            target=KiwoomProxy, 
            args=(
                # method queue
                self.method_cqueue, 
                self.method_dqueue,
                # tr queue
                self.tr_cqueue, 
                self.tr_dqueue,
                # order queue
                self.order_cqueue,
                # real queue 
                self.real_cqueue, 
                self.real_dqueues
            ),
            daemon=daemon 
        )
        self.proxy.start()

    def put_method(self, cmd):
        self.method_cqueue.put(cmd)

    def get_method(self):
        return self.method_dqueue.get()

    def put_tr(self, cmd):
        self.tr_cqueue.put(cmd)

    def get_tr(self):
        return self.tr_dqueue.get()

    def put_real(self, cmd):
        self.real_cqueue.put(cmd)

    def get_real(self, name):
        index = real_index.get(name)
        return self.real_dqueues[index].get()
