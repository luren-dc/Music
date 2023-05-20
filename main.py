import time
from music.uitls import login


def login_music():
    print("正在获取登录二维码")
    qq = login.QQLogin()
    img = qq.get_qrcode()
    if img == -1:
        return
    login.show_qrcode(img)
    print("\r等待扫码中", end="")
    while True:
        time.sleep(0.5)
        state = qq.check_state()
        print(state)
        if state == 4:
            print("\r二维码已失效")
            break
        elif state == 3:
            print("\r扫码成功，请确认登录", end="")
        elif state == 2:
            pass
        elif state == -1:
            print("获取二维码状态错误")
        elif state:
            print("\rQQ: %s 登录成功" % state)


def main():
    print(
        """\033[34m.___  ___.  __    __       _______. __    ______ 
|   \/   | |  |  |  |     /       ||  |  /      |
|  \  /  | |  |  |  |    |   (----`|  | |  ,----'
|  |\/|  | |  |  |  |     \   \    |  | |  |     
|  |  |  | |  `--'  | .----)   |   |  | |  `----.
|__|  |__|  \______/  |_______/    |__|  \______|\033[0m
    """
    )
    login_music()


if __name__ == "__main__":
    main()
