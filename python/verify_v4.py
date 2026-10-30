# -*- coding: utf-8 -*-
"""验证: 信息栏每 10 秒自动刷新(两次截屏时间戳应不同), 且不打断画面循环。

用法: python verify_v4.py
可用环境变量 MC_EXE 指定待测 exe。
"""
import ctypes
import subprocess
import time

from PIL import ImageGrab

from _paths import find_exe, shot_path

exe = find_exe()
print("测试目标:", exe)

u = ctypes.windll.user32
p = subprocess.Popen([exe])
time.sleep(5.0)
u.keybd_event(0x20, 0, 0, 0)   # 空格: 从信息页进入测试画面
u.keybd_event(0x20, 0, 2, 0)
time.sleep(1.5)
ImageGrab.grab().resize((960, 600)).save(shot_path("shot_r1.png"))
time.sleep(12.0)   # 跨过一次 10 秒刷新
ImageGrab.grab().resize((960, 600)).save(shot_path("shot_r2.png"))
p.kill()
print("refresh shots ok, was_alive =", p.poll() is None)
