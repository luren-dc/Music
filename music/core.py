import json
import random
import time
from typing import Any, Callable

import music.utils.http as requests
from music.utils.encrypt import get_search_id, get_sign

qq_number = 0
g_tk = 0


# MusicBean
class Song(object):
    __slots__ = ("__mid", "__id", "__name", "__artist", "__url")

    def __init__(self, mid: int, song_id: int, name: str, artist: list[str]):
        self.__mid = mid
        self.__id = song_id
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
    def id(self, song_id: int) -> None:
        self.__id = song_id

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


def set_qq_info(qq_num: int, tk: int) -> None:
    """
    设置 QQ 音乐 API 信息
    :param qq_num: QQ 账号
    :param tk: g_tk
    :return:
    """
    global qq_number, g_tk
    qq_number = int(qq_num)
    g_tk = int(tk)


def __request_api(data: dict) -> Callable[[dict[str, Any]], Any] | int:
    """
    请求 QQ音乐 API

    :param data: 数据
    :return: 请求结果
    """
    data = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    params = {"_": str(int(time.time() * 1000)), "sign": get_sign(data.decode("utf-8"))}
    headers = {
        "Host": "u.y.qq.com",
        "origin": "https://y.qq.com",
        "accept": "application/json",
    }
    response = requests.post(QQMUSIC_API_URL, headers=headers, params=params, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return -1


def get_playlist(list_id: int) -> list[Song]:
    """
    获取 QQ音乐 歌单信息

    :param list_id: 歌单 id
    :return: 歌单信息
    """
    re = requests.get(
        url=f"https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid={list_id}&format=json&loginUin={qq_number}",
        headers={
            "Host": "u.y.qq.com",
            "origin": "https://y.qq.com",
            "accept": "application/json",
        },
    )
    data = re.json()
    if data["code"] == -1:
        return -1
    songs = []
    for data in data["cdlist"][0]["songlist"]:
        id = data["songid"]
        mid = data["songmid"]
        name = data["songname"]
        artist = []
        for singer in data["singer"]:
            artist.append(singer["name"])
        songs.append(Song(mid, id, name, artist))
    songs.reverse()
    return songs


SEARCH_TYPE = {"song": 0, "album": 2, "mv": 4, "playlist": 3, "user": 8, "lyric": 7}


def search(query: str, search_type: str, p: int = 1, num: int = 10) -> list[Song] | int:
    """
    搜索

    :param query: 搜索的关键词
    :param search_type: 搜索的类型 song: 0 album: 2 mv: 4 playlist: 3 user: 8 lyric: 7
    :param p: 页数
    :param num: 每页数量
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
            "uin": qq_number,
            "g_tk_new_20200303": g_tk,
            "g_tk": g_tk,
        },
        "req_1": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "remoteplace": "txt.yqq.song",
                "searchid": get_search_id(search_type),
                "search_type": SEARCH_TYPE[search_type],
                "query": query,
                "page_num": p,
                "num_per_page": num,
            },
        },
    }
    data = __request_api(data)
    if data == -1:
        return -1
    data = data["req_1"]["data"]["body"][search_type]
    if search_type == "song":
        data = data["list"]
        songs = []
        for song in data:
            artist = []
            for artist_ in song["singer"]:
                artist.append(artist_["name"])
            song = Song(song["mid"], song["id"], song["name"], artist)
            songs.append(song)
        songs.reverse()
        return songs


FILE_CONFIG = {
    "128k": {
        "s": "M500",
        "e": ".mp3",
        "bitrate": "128kbps",
    },
    "320k": {
        "s": "M800",
        "e": ".mp3",
        "bitrate": "320kbps",
    },
    "flac": {
        "s": "F000",
        "e": ".flac",
        "bitrate": "FLAC",
    },
}


def get_download_url(mid: list, song_type: str = "128k") -> str:
    def get_random(len):
        return "".join(str(random.choice(range(10))) for _ in range(len))

    file_info = FILE_CONFIG[song_type]
    n_data = {}
    mid = [mid[i : i + 100] for i in range(0, len(mid), 100)]
    for mid in mid:
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
                "uin": qq_number,
                "g_tk_new_20200303": g_tk,
                "g_tk": g_tk,
            },
            "req_1": {
                "module": "vkey.GetVkeyServer",
                "method": "CgiGetVkey",
                "param": {
                    "filename": []
                    if song_type == "flac"
                    else [f"{file_info['s']}{mid}{mid}{file_info['e']}" for mid in mid],
                    "guid": "788" + get_random(7),
                    "songmid": mid,
                    "songtype": [0 for i in range(len(mid))],
                    "uin": str(qq_number),
                    "loginflag": 1,
                    "platform": "20",
                },
            },
        }
        data = __request_api(data)
        if data != -1:
            sip = random.choice(data["req_1"]["data"]["sip"])
        for data in data["req_1"]["data"]["midurlinfo"]:
            n_data[data["songmid"]] = sip + data["purl"] if data["purl"] else -1
    return n_data
