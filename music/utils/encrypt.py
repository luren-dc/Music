import os
import random
import execjs

# JS 环境上下文
JSContext = None


def __get_js() -> str:
    js_path = os.path.dirname(os.path.realpath(__file__)) + "/sign.js"
    with open(js_path, "r", encoding="utf-8") as f:
        return f.read()


# 初始化 JS 环境
def init_js_context():
    global JSContext
    JSContext = execjs.compile(__get_js())


# Sign 计算方法
def get_sign(data: str) -> str:
    global JSContext
    return JSContext.call("getSign", data)


def get_token(p_skey):
    """计算 g_tk"""
    h = 5381
    for c in p_skey:
        h += (h << 5) + ord(c)
    return 2147483647 & h


def get_uuid():
    """生成随机 UUID."""
    uuid_string = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"

    def callback(c):
        r = random.randint(0, 15)
        v = r if c == "x" else (r & 0x3 | 0x8)
        return hex(v)[2:]

    return "".join([callback(c) if c in ["x", "y"] else c for c in uuid_string]).upper()


def get_ptqrtoken(qrsig):
    """计算 ptqrtoken"""
    e = 0
    for c in qrsig:
        e += (e << 5) + ord(c)
    return 2147483647 & e
