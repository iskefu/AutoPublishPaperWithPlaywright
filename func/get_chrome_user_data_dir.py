import os
from pathlib import Path

def get_chrome_user_data_dir():
    # 根据操作系统获取用户目录
    user_home = Path.home()
    if os.name == "nt":  # Windows
        path = user_home / "AppData" / "Local" / "Google" / "Chrome" / "User Data"
    elif os.name == "posix":
        path = user_home / ".config" / "google-chrome"/"Default"
    else:
        raise Exception("Unsupported operating system")

    return path
if __name__ == '__main__':
    chrome_data_dir = get_chrome_user_data_dir()
    print(chrome_data_dir)
