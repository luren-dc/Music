from multiprocessing import Process
import time

import music
from music.utils import login


def login_music() -> int:
    print("正在获取登录二维码")
    qq = login.QQLogin()
    img = qq.get_qrcode()
    if img == -1:
        return -1
    Process(target=login.show_qrcode, args=(img,)).start()
    count_error = 0
    while True:
        time.sleep(1)
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
            return 1


def main():
    print(
        "\033[34m.___  ___.  __    __       _______. __    ______ \n"
        "|   \/   | |  |  |  |     /       ||  |  /      |\n"
        "|  \  /  | |  |  |  |    |   (----`|  | |  ,----'\n"
        "|  |\/|  | |  |  |  |     \   \    |  | |  |     \n"
        "|  |  |  | |  `--'  | .----)   |   |  | |  `----.\n"
        "|__|  |__|  \______/  |_______/    |__|  \______|\033[0m\n"
        "    "
    )
    while True:
        if login_music() == -1:
            user_input = input("登陆失败 是否重新登陆?(Y/回车) ")
            if user_input == "" or user_input.lower() == "y":
                continue
            else:
                break
        time.sleep(3)
        song = input("要搜索的歌曲")
        music.search(song, "song")
        break


if __name__ == "__main__":
    main()
