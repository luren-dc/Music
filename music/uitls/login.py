import random
import re
import sys
import time
from io import BytesIO

from PIL import Image
from .http import (
    get,
    post,
    session,
)

# 获取二维码
QQMUSIC_QRSHOW = "https://ssl.ptlogin2.qq.com/ptqrshow"
# 检验二维码状态
QQMUSIC_PT = "https://xui.ptlogin2.qq.com/cgi-bin/xlogin"
# 验证
QQMUSIC_PTQR = "https://ssl.ptlogin2.qq.com/ptqrlogin"
LOGIN_AUTHORIZE = "https://graph.qq.com/oauth2.0/authorize"


def show_qrcode(img_data):
    """显示二维码"""
    img = Image.open(img_data).resize((90, 90))
    if sys.platform == "win32" or "darwin":
        img.show()
        img.close()
    else:
        width, height = img.size
        for y in range(0, height, 2):
            for x in range(width):
                r1 = img.getpixel((x, y))
                r2 = img.getpixel((x, y + 1)) if y + 1 < height else 255
                if r1 == 0:
                    if r2 == 0:
                        char = "█"
                    else:
                        char = "▀"
                else:
                    if r2 == 0:
                        char = "▄"
                    else:
                        char = " "
                print(char, end="")
            print()
        img.close()


def get_token(p_skey):
    """计算 g_tk"""
    h = 5381
    for c in p_skey:
        h += (h << 5) + ord(c)
    return 2147483647 & h


def get_uuid():
    """Generates a random UUID."""
    uuid_string = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'

    def callback(c):
        r = random.randint(0, 15)
        v = r if c == "x" else (r & 0x3 | 0x8)
        return hex(v)[2:]

    return "".join(
        [callback(c) if c in ["x", "y"] else c for c in uuid_string]
    ).upper()


def get_ptqrtoken(qrsig):
    """计算 ptqrtoken"""
    e = 0
    for c in qrsig:
        e += (e << 5) + ord(c)
    return 2147483647 & e


class QQLogin:
    def __init__(self):
        self.url_refresh = None
        self.qq_number = None
        self.g_tk = None
        self.ptqrtoken = None
        self.qrsig = None
        self.pt_login_sig = None
        self.uuid = None
        self.qqmusic_skey = None

    # 获取登录二维码
    def get_qrcode(self) -> int | BytesIO:
        self.uuid = get_uuid()
        params = {
            "appid": "716027609",
            "daid": "383",
            "style": "33",
            "login_text": "登录",
            "hide_title_bar": "1",
            "hide_border": "1",
            "target": "self",
            "s_url": "https://graph.qq.com/oauth2.0/login_jump",
            "pt_3rd_aid": "100497308",
            "pt_feedback_link": "https://support.qq.com/products/77942?customInfo=.appid100497308",
            "theme": "2",
            "verify_theme": "",
        }
        if get(QQMUSIC_PT, params=params) == -1:
            return -1
        self.pt_login_sig = session.cookies.get("pt_login_sig")
        # 获取二维码
        params = {
            "appid": "716027609",
            "e": "2",
            "l": "M",
            "s": "3",
            "d": "72",
            "v": "4",
            "t": str(random.random()),
            "daid": "383",
            "pt_3rd_aid": "100497308",
        }
        response = get(QQMUSIC_QRSHOW, params=params)
        if response == -1:
            return -1
        self.qrsig = session.cookies.get("qrsig")
        self.ptqrtoken = get_ptqrtoken(self.qrsig)
        from io import BytesIO

        return BytesIO(response.content)

    def check_state(self) -> int:
        if self.url_refresh:
            return self.qq_number
        params = {
            "u1": "https://graph.qq.com/oauth2.0/login_jump",
            "ptqrtoken": self.ptqrtoken,
            "ptredirect": "0",
            "h": "1",
            "t": "1",
            "g": "1",
            "from_ui": "1",
            "ptlang": "2052",
            "action": "0-0-%s" % int(time.time() * 1000),
            "js_ver": "20102616",
            "js_type": "1",
            "login_sig": self.pt_login_sig,
            "pt_uistyle": "40",
            "aid": "716027609",
            "daid": "383",
            "pt_3rd_aid": "100497308",
            "has_onekey": "1",
        }
        response = get(QQMUSIC_PTQR, params=params)
        if response == -1:
            return -1
        elif "二维码未失效" in response.text:
            return 2
        elif "二维码认证中" in response.text:
            return 3
        elif "二维码已失效" in response.text:
            return 4
        else:
            self.qq_number = re.findall(r"&uin=(.+?)&service", response.text)[0]
            self.url_refresh = re.findall(r"'(https:.*?)'", response.text)[0]
            self.g_tk = get_token(session.cookies.get("p_skey"))
            return self.qq_number

    def authorize(self):
        if self.url_refresh is not None:
            if get(self.url_refresh, allow_redirects=False, verify=False) == -1:
                return -1
            params = {
                "Referer": "https://graph.qq.com/oauth2.0/show?which=Login&display=pc&response_type=code&client_id"
                           "=100497308&redirect_uri=https://y.qq.com/portal/wx_redirect.html?login_type=1&surl=https"
                           "://y.qq.com/portal/profile.html#stat=y_new.top.user_pic&stat=y_new.top.pop.logout"
                           "&use_customer_cb=0&state=state&display=pc",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            data = {
                "response_type": "code",
                "client_id": "100497308",
                "redirect_uri": "https://y.qq.com/portal/wx_redirect.html?login_type=1&surl=https://y.qq.com"
                                "/#&use_customer_cb=0",
                "scope": "",
                "state": "state",
                "switch": "",
                "from_ptlogin": "1",
                "src": "1",
                "update_auth": "1",
                "openapi": "80901010",
                "g_tk": self.g_tk,
                "auth_time": str(int(time.time())),
                "ui": self.uuid,
            }
            if (
                    post(LOGIN_AUTHORIZE, data=data, allow_redirects=False, verify=False)
                    == -1
            ):
                return -1
            return 1
        else:
            return -1

    def getLoginInfo(self):
        pass