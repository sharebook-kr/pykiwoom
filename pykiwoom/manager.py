import multiprocessing as mp
from pykiwoom.kiwoom_proxy import KiwoomProxy


class KiwoomManager:
    def __init__(self, daemon=True):
        # SubProcess
        # method queue
        self.method_cqueue      = mp.Queue()
        self.method_dqueue      = mp.Queue()

        # tr queue
        self.tr_cqueue          = mp.Queue()
        self.tr_dqueue          = mp.Queue()

        # order queue
        self.order_cqueue       = mp.Queue()

        # real queue
        self.real_cqueue        = mp.Queue()
        self.real_dqueues       = mp.Queue()

        # condition queue
        self.cond_cqueue        = mp.Queue()
        self.cond_dqueue        = mp.Queue()
        self.tr_cond_dqueue     = mp.Queue()
        self.real_cond_dqueue   = mp.Queue()

        # chejan queue
        self.chejan_dqueue      = mp.Queue()

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
                self.real_dqueues,
                # condition queue
                self.cond_cqueue,
                self.cond_dqueue,
                self.tr_cond_dqueue,
                self.real_cond_dqueue,
                # chejan queue
                self.chejan_dqueue
            ),
            daemon=daemon
        )
        self.proxy.start()

    # method
    def put_method(self, cmd):
        self.method_cqueue.put(cmd)

    def get_method(self):
        return self.method_dqueue.get()

    # tr
    def put_tr(self, cmd):
        self.tr_cqueue.put(cmd)

    def get_tr(self):
        return self.tr_dqueue.get()

    # order
    def put_order(self, cmd):
        self.order_cqueue.put(cmd)

    # real
    def put_real(self, cmd):
        self.real_cqueue.put(cmd)

    def get_real(self):
        return self.real_dqueues.get()

    # condition
    def put_cond(self, cmd):
        self.cond_cqueue.put(cmd)

    def get_cond(self, real=False, method=False):
        if method is True:
            return self.cond_dqueue.get()
        elif real is True:
            return self.real_cond_dqueue.get()
        else:
            return self.tr_cond_dqueue.get()

    def get_chejan(self):
        return self.chejan_dqueue.get()