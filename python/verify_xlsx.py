# -*- coding: utf-8 -*-
"""端到端验证: 连跑两次 exe, 检查 Excel 是否新建 + 追加(两行), 并截屏看提示。

用法: python verify_xlsx.py
可用环境变量 MC_EXE 指定待测 exe。

注意: 会临时开启"检测记录"配置并在结束时还原; 原有的记录文件也会先备份、
验证完后恢复, 不会污染真实数据。
"""
import configparser
import os
import shutil
import subprocess
import time

from openpyxl import load_workbook
from PIL import ImageGrab

from _paths import BASE, find_exe, shot_path

EXE = find_exe()
XLSX = os.path.join(BASE, "显示器检测记录.xlsx")
BAK = XLSX + ".verify_bak"
CFG = os.path.join(os.environ.get("APPDATA") or os.path.expanduser("~"),
                   "MonitorCheck", "config.ini")


def set_record_config(flag):
    os.makedirs(os.path.dirname(CFG), exist_ok=True)
    with open(CFG, "w", encoding="utf-8") as f:
        f.write("[record]\nenabled = %s\n" % ("true" if flag else "false"))


def read_record_config():
    """返回 True/False, 文件不存在或损坏返回 None"""
    try:
        cp = configparser.ConfigParser()
        if cp.read(CFG, encoding="utf-8") and cp.has_option("record", "enabled"):
            return cp.getboolean("record", "enabled")
    except Exception:
        pass
    return None


def show(tag):
    if not os.path.exists(XLSX):
        print(tag, "-> xlsx 不存在")
        return
    ws = load_workbook(XLSX).active
    print(tag, "->", os.path.basename(XLSX), "行数(含表头):", ws.max_row)
    for r in ws.iter_rows(values_only=True):
        print("   ", r)


orig_cfg = read_record_config()
had_xlsx = os.path.exists(XLSX)
try:
    if had_xlsx:
        shutil.copy2(XLSX, BAK)
        os.remove(XLSX)
    set_record_config(True)          # v3.1 起记录默认关闭, 验证前临时打开

    print("测试目标:", EXE)

    # 第一次运行 -> 应新建文件
    p = subprocess.Popen([EXE])
    time.sleep(9.0)
    ImageGrab.grab().resize((960, 600)).save(shot_path("shot_x1.png"))
    p.kill()
    time.sleep(1.0)
    show("run1")

    # 第二次运行 -> 应追加
    time.sleep(2.0)
    p = subprocess.Popen([EXE])
    time.sleep(9.0)
    ImageGrab.grab().resize((960, 600)).save(shot_path("shot_x2.png"))
    p.kill()
    time.sleep(1.0)
    show("run2")
finally:
    # 还原现场
    if os.path.exists(XLSX):
        os.remove(XLSX)
    if had_xlsx and os.path.exists(BAK):
        shutil.move(BAK, XLSX)
    if orig_cfg is None:
        if os.path.exists(CFG):
            os.remove(CFG)
    else:
        set_record_config(orig_cfg)
    print("已还原配置与记录文件")
