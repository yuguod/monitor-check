# -*- coding: utf-8 -*-
"""启动 exe 并在白色/红色画面阶段各截屏一张, 用于可视化验证。

用法: python screenshot_test.py
可用环境变量 MC_EXE 指定待测 exe。
"""
import subprocess
import time

from PIL import ImageGrab

from _paths import find_exe, shot_path

exe = find_exe()
print("测试目标:", exe)

p = subprocess.Popen([exe])
time.sleep(4.0)  # 信息页 -> 黑 -> 白
img = ImageGrab.grab()
img.resize((img.width // 3, img.height // 3)).save(shot_path("shot_white.png"))
time.sleep(2.0)  # -> 红
img = ImageGrab.grab()
img.resize((img.width // 3, img.height // 3)).save(shot_path("shot_red.png"))
p.kill()
print("done, was_alive =", p.poll() is None)
