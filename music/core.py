import os
import execjs


# MusicBean
class Song(object):
    __slots__ = ("__mid", "__id", "__name", "__artist", "__url")

    def __init__(self, mid: int, id: int, name: str, artist: list[str]):
        self.__mid = mid
        self.__id = id
        self.__name = name
        self.__artist = artist

    @property
    def mid(self) -> int:
        return self.__mid

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def artist(self) -> list[str]:
        return self.__artist

    @mid.setter
    def mid(self, mid: int) -> None:
        self.__mid = mid

    @id.setter
    def mid(self, id: int) -> None:
        self.__id = id

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @artist.setter
    def artist(self, artist: list[str]) -> None:
        self.__artist = artist

    def __str__(self) -> str:
        return "mid: %s\nid: %s\nname: %s\naritist: %s" % (
            self.__mid,
            self.__id,
            self.__name,
            self.__artist,
        )

    __repr__ = __str__


def get_js() -> None:
    js_path = os.path.dirname(os.path.realpath(__file__)) + "/sign.js"
    with open(js_path, "r", encoding="utf-8") as f:
        return f.read()


JSContext = None


# 初始化 JS 环境
def init_js_context():
    global JSContext
    JSContext = execjs.compile(get_js())


# Sign 计算方法
def get_sign(data: str) -> str:
    JSContext
    return JSContext.call("getSign", data)
