# -*- coding: utf-8 -*-
"""验证 v4: 信息栏每 10 秒自动刷新(两次截屏时间戳应不同), 且不打断画面循环"""
import ctypes
import subprocess
import time

from PIL import Image, ImageGrab

BASE = r"C:\Users\yuguo\WorkBuddy\2026-09-03-20-07-00\monitor-check"
exe = BASE + r"\MonitorCheck.exe"

u = ctypes.windll.user32
p = subprocess.Popen([exe])
time.sleep(5.0)
u.keybd_event(0x20, 0, 0, 0)
u.keybd_event(0x20, 0, 2, 0)
time.sleep(1.5)
ImageGrab.grab().resize((960, 600)).save(BASE + r"\python\shot_r1.png")
time.sleep(12.0)   # 跨过一次 10 秒刷新
ImageGrab.grab().resize((960, 600)).save(BASE + r"\python\shot_r2.png")
p.kill()
print("refresh shots ok, was_alive =", p.poll() is None)
