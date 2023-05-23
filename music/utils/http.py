import json
import os

import requests

# 默认请求头
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Referer": "https://y.qq.com/",
}

session: requests.Session | None = None


def init_session():
    """
    初始化 session

    :return:
    """
    global session
    if not session:
        session = requests.Session()


def get(url, **kwargs) -> requests.Response | int:
    """
    发送 GET 请求

    :param url: 请求 URL
    :param kwargs: 请求参数
    :return:
    """
    global session
    requests.packages.urllib3.disable_warnings()
    headers = {**DEFAULT_HEADERS, **kwargs.get("headers", {})}
    session.headers.update(headers)
    try:
        return session.get(url, **kwargs)
    except requests.exceptions.ConnectionError:
        return -1


def post(url, **kwargs) -> requests.Response | int:
    """
    发送 POST 请求

    :param url: 请求 URL
    :param kwargs: 请求参数
    :return:
    """
    global session
    requests.packages.urllib3.disable_warnings()
    headers = {**DEFAULT_HEADERS, **kwargs.get("headers", {})}
    session.headers.update(headers)
    try:
        return session.post(url, **kwargs)
    except requests.exceptions.ConnectionError:
        return -1


def get_cookies() -> None:
    """
    获取 cookies

    :return:
    """
    filename = (
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        + "/data/cookies.txt"
    )
    with open(filename, "r") as f:
        cookies = json.loads(f.read())
        cookies = requests.utils.cookiejar_from_dict(cookies)
        session.cookies.update(cookies)


def save_cookies() -> None:
    """
    保存 cookies

    :return:
    """
    filename = (
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        + "/data/cookies.txt"
    )

    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(json.dumps(requests.utils.dict_from_cookiejar(session.cookies)))
