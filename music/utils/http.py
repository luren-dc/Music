import requests

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Referer": "https://y.qq.com/",
}

session = None


def init_session():
    global session
    if not session:
        session = requests.Session()


def get(url, **kwargs) -> requests.Response | int:
    global session
    requests.packages.urllib3.disable_warnings()
    headers = {**DEFAULT_HEADERS, **kwargs.get("headers", {})}
    session.headers.update(headers)
    try:
        return session.get(url, **kwargs)
    except requests.exceptions.ConnectionError:
        return -1


def post(url, **kwargs) -> requests.Response | int:
    global session
    requests.packages.urllib3.disable_warnings()
    headers = {**DEFAULT_HEADERS, **kwargs.get("headers", {})}
    session.headers.update(headers)
    try:
        return session.post(url, **kwargs)
    except requests.exceptions.ConnectionError:
        return -1
