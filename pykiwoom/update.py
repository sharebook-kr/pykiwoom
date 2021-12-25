import os 
import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import pythoncom
import win32gui
import win32con
import win32api
import time
import multiprocessing as mp


#--------------------------------------------------------------------
# 자동 로그인 해제 및 설정
#--------------------------------------------------------------------
LOGIN_FILE     = "C:/OpenAPI/system/Autologin.dat"
LOGIN_FILE_TMP = "C:/OpenAPI/system/Autologin.tmp"


def turn_off_auto():
    if os.path.isfile(LOGIN_FILE):
        os.rename(LOGIN_FILE, LOGIN_FILE_TMP) 

def turn_on_auto():
    if os.path.isfile(LOGIN_FILE_TMP):
        os.rename(LOGIN_FILE_TMP, LOGIN_FILE)


#--------------------------------------------------------------------
# 수동 로그인 관련 함수
#--------------------------------------------------------------------
def window_enumeration_handler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def enum_windows():
    windows = []
    win32gui.EnumWindows(window_enumeration_handler, windows)
    return windows


def find_window(caption):
    hwnd = win32gui.FindWindow(None, caption)
    if hwnd == 0:
        windows = enum_windows()
        for handle, title in windows:
            if caption in title:
                hwnd = handle
                break
    return hwnd


def enter_keys(hwnd, data, interval=500):
    win32api.SendMessage(hwnd, win32con.EM_SETSEL, 0, -1)
    win32api.SendMessage(hwnd, win32con.EM_REPLACESEL, 0, data)
    win32api.Sleep(interval)


def click_button(btn_hwnd):
    win32api.PostMessage(btn_hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
    win32api.Sleep(100)
    win32api.PostMessage(btn_hwnd, win32con.WM_LBUTTONUP, 0, 0)
    win32api.Sleep(300)


def left_click(x, y, hwnd):
    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)


def double_click(x, y, hwnd):
    left_click(x, y, hwnd)
    left_click(x, y, hwnd)
    win32api.Sleep(300)


#--------------------------------------------------------------------
# 로그인창
#--------------------------------------------------------------------
class MyWindow(QWidget):
    app = QApplication(sys.argv)

    def __init__(self, q):
        super().__init__()
        self.login_status = False
        self.q = q
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.slot_login)
        self.login()

    def login(self):
        self.ocx.dynamicCall("CommConnect()")
        while not self.login_status: 
            pythoncom.PumpWaitingMessages()
            time.sleep(0.001)

    def slot_login(self, err_code):
        self.login_status = True
        self.q.put('complete')


def version(user_id, user_pass, user_cert=None):
    q = mp.Queue()

    # 자동 로그인 해제
    turn_off_auto()

    sub_proc = mp.Process(target=MyWindow, name="Sub Process", args=(q,), daemon=True)
    sub_proc.start()

    while True:
        caption = "Open API Login"
        hwnd = find_window(caption)

        if hwnd == 0:
            print("로그인 창 대기 ...")
            time.sleep(1)
            continue
        else:
            break

    time.sleep(2)
    edit_id   = win32gui.GetDlgItem(hwnd, 0x3E8)
    edit_pass = win32gui.GetDlgItem(hwnd, 0x3E9)
    edit_cert = win32gui.GetDlgItem(hwnd, 0x3EA)
    btn_login = win32gui.GetDlgItem(hwnd, 0x1)

    if user_cert is None:
        if win32gui.IsWindowEnabled(win32gui.GetDlgItem(hwnd, 0x3EA)):
            click_button(win32gui.GetDlgItem(hwnd, 0x3ED))
    else:
        if not win32gui.IsWindowEnabled(win32gui.GetDlgItem(hwnd, 0x3EA)):
            click_button(win32gui.GetDlgItem(hwnd, 0x3ED))

    double_click(15, 15, edit_id)
    enter_keys(edit_id, user_id) 
    time.sleep(0.5)

    double_click(15, 15, edit_pass)
    enter_keys(edit_pass, user_pass) 
    time.sleep(0.5)

    if user_cert is not None:
        double_click(15, 15, edit_cert)
        enter_keys(edit_cert, user_cert) 
        time.sleep(0.5)

    double_click(15, 15, edit_id)
    enter_keys(edit_id, user_id) 
    time.sleep(1)
    click_button(btn_login)   

    secs_cnt = 0
    while True:
        time.sleep(1)
        remain_secs = 120 - secs_cnt
        print(f"로그인 대기: {remain_secs}")

        # 버전처리 경고창 확인
        hwnd = find_window("opstarter")
        if hwnd != 0:
            try:
                static_hwnd = win32gui.GetDlgItem(hwnd, 0xFFFF)
                text = win32gui.GetWindowText(static_hwnd)
                if '버전처리' in text:
                    while sub_proc.is_alive():
                        sub_proc.kill()
                        time.sleep(1)

                    click_button(win32gui.GetDlgItem(hwnd, 0x2))
                    secs_cnt = 90      # 버전처리이면 30초 후 종료
            except:
                pass

        # 업그레이드 확인창
        hwnd = find_window("업그레이드 확인")
        if hwnd != 0:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

        # 버전처리가 있는 경우의 종료
        if secs_cnt > 120:
            break

        # 버전처리가 없는 경우의 종료
        if not q.empty():
            data = q.get()
            break

        secs_cnt += 1
    
    print("버전처리 완료")

    # 자동 로그인 재설정
    turn_on_auto()


if __name__ == "__main__":
    version("아이디", "비밀번호", "공인인증서비밀번호")
