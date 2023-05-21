import json
import time

import utils.http as requests
from music.utils.encrypt import get_sign

qq_number = 0
g_tk = 0

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
    def id(self, id: int) -> None:
        self.__id = id

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @artist.setter
    def artist(self, artist: list[str]) -> None:
        self.__artist = artist

    def __str__(self) -> str:
        return "mid: %s\n id: %s\n name: %s\n artist: %s" % (
            self.__mid,
            self.__id,
            self.__name,
            self.__artist,
        )

    __repr__ = __str__


QQMUSIC_API_URL = "https://u.y.qq.com/cgi-bin/musics.fcg"


def __request_api(data: dict) -> str | int:
    """
    请求 QQ音乐 API

    :param data: 数据
    :return: 请求结果
    """
    data = json.dumps(data, separators=(",", ":").encode("utf-8"))
    params = {"_": str(int(time.time() * 10000)), "sign": get_sign(data)}
    response = requests.post(QQMUSIC_API_URL, params=params, data=data)
    if response.status_code == 200:
        return response.text
    else:
        return -1


def get_songs(id: int) -> list[Song]:
    """
    获取 QQ音乐 歌单信息

    :param id: 歌单 id
    :return: 歌单信息
    """
    pass


def search(name: str, type: int) -> list[Song]:
    """
    搜索

    :param name: 搜索的关键词
    :param type: 搜索的类型 0: 歌曲 2: 专辑 3: 歌单 4: MV
    :return: 搜索的结果
    """
    data = {
        "comm": {
            "cv": 4747474,
            "ct": 24,
            "format": "json",
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "notice": 0,
            "platform": "yqq.json",
            "needNewCode": 1,
            "uin": 3308862290,
            "g_tk_new_20200303": 617682219,
            "g_tk": 617682219,
        },
        "req_1": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "remoteplace": "txt.yqq.song",
                "searchid": "56304152276655618",
                "search_type": 0,
                "query": name,
                "page_num": 1,
                "num_per_page": 10,
            },
        },
    }
