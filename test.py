import pyautogui

from publish.func.get_cover import get_random_image
cover_path="/run/media/kf/data/cover"

cover =get_random_image(cover_path)
print('cover:', cover)
pyautogui.typewrite(cover)
