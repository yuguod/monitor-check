# -*- coding: utf-8 -*-
"""启动 MonitorCheck.exe 并在白色/红色画面阶段各截屏一张, 用于可视化验证"""
import subprocess
import sys
import time

from PIL import ImageGrab

BASE = r"C:\Users\yuguo\WorkBuddy\2026-09-03-20-07-00\monitor-check"
exe = BASE + r"\MonitorCheck.exe"

p = subprocess.Popen([exe])
time.sleep(4.0)  # 信息页 1.2s -> idx0 黑 -> ~3.2s 白
img = ImageGrab.grab()
img.resize((img.width // 3, img.height // 3)).save(BASE + r"\python\shot_white.png")
time.sleep(2.0)  # ~5.2s -> idx2 红
img = ImageGrab.grab()
img.resize((img.width // 3, img.height // 3)).save(BASE + r"\python\shot_red.png")
p.kill()
print("done, was_alive =", p.poll() is None)
