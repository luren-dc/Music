import os
import time
from multiprocessing import Process

import music
import music.utils.http as http
from music.utils import login


def login_music() -> int:
    qq = login.QQLogin()
    COOKIES_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "data", "cookies.txt"
    )
    if os.path.exists(COOKIES_FILE):
        print("正在验证 cookies 是否失效")
        http.get_cookies()
        state = qq.check_login()
        if state != -1:
            print("\rQQ: %s 登录成功" % state)
            return 1
        else:
            print("cookies 失效")
    print("正在获取登录二维码")
    img = qq.get_qrcode()
    if img == -1:
        return -1
    Process(target=login.show_qrcode, args=(img,)).start()
    count_error = 0
    while True:
        state = qq.check_state()
        print("\r" + " " * 20 + "\r", end="")
        if state == 4:
            print("\r二维码已失效")
            return -1
        elif state == 3:
            print("\r扫码成功，请确认登录", end="")
            count_error = 0
        elif state == 2:
            print("\r等待扫码中", end="")
            count_error = 0
        elif state == -1:
            count_error += 1
            print("\r获取错误 错误次数: %s" % count_error, end="")
        elif state:
            print("\r扫码已成功 登录验证中", end="")
            if qq.authorize() == -1:
                print("\r验证失败", end="")
                return -1
            print("\r登录验证成功 验证 skey 中", end="")
            if qq.check_state() == -1:
                print("\r验证失败", end="")
                return -1
            print("\rQQ: %s 登录成功" % state)
            http.save_cookies()
            return 1
        time.sleep(1)


def print_logo():
    """
    打印 Logo
    """
    print(
        "\033[34m.___  ___.  __    __       _______. __    ______ \n"
        "|   \\/   | |  |  |  |     /       ||  |  /      |\n"
        "|  \\  /  | |  |  |  |    |   (----`|  | |  ,----'\n"
        "|  |\\/|  | |  |  |  |     \\   \\    |  | |  |     \n"
        "|  |  |  | |  `--'  | .----)   |   |  | |  `----.\n"
        "|__|  |__|  \\______/  |_______/    |__|  \\______|\033[0m\n"
        "    "
    )


def song_search():
    """
    歌曲搜索
    """
    song = input("请输入要搜索的歌曲名: ")
    try:
        data = music.search(song, "song")
        print(f"共找到 {len(data)} 首歌曲：")
        for i, result in enumerate(data[:10], 1):
            print(f"{i}. {result.name} - {' & '.join(result.artist)}")
        index = int(input("请输入要下载的歌曲序号: ")) - 1
        data = music.get_download_url([data[index].mid])
        print(f"下载链接：{data}")
    except Exception as e:
        print("出现错误：", e)


def playlist_download():
    """
    歌单下载
    """
    songlist_id = input("请输入要下载的歌单 ID: ")
    try:
        data = music.get_playlist(int(songlist_id))
        mid = [data.mid for data in data]
        data = music.get_download_url(mid)
        print(f"下载链接：{data}")
    except Exception as e:
        print("出现错误：", e)


def main_menu():
    """主菜单"""
    print("=" * 40)
    print("    Music Downloader v1.0 by Luren")
    print("=" * 40)
    print("请选择要使用的功能：")
    print("[1] 歌曲搜索")
    print("[2] 歌单下载")
    print("[3] 下载历史")
    print("[4] 设置")
    print("[5] 关于")
    print("[!] 退出")

    print("=" * 40)


def main():
    """
    主函数
    """
    # 打印 Logo
    print_logo()

    # 登录
    is_login = login_music()

    while is_login:
        # 输出菜单
        main_menu()
        # 循环读取用户的输入
        while True:
            chose = input("请输入序号: ")
            break
        # 根据用户输入选择相应的功能
        if chose == "1":
            song_search()
        elif chose == "2":
            playlist_download()
        elif chose == "!":
            exit()
        else:
            print("请输入正确的序号！")


if __name__ == "__main__":
    main()
