# -*- coding: utf-8 -*-
"""验证脚本共用的路径解析。

不写死任何本机绝对路径: 项目克隆到任何目录都能直接运行。
- 待测 exe 默认取项目根目录下最新的 MonitorCheck*.exe
- 也可用环境变量 MC_EXE 显式指定
"""
import glob
import os

PY_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(PY_DIR)          # 项目根目录 (monitor-check/)


def find_exe():
    """定位待测 exe: 环境变量 MC_EXE 优先, 否则取最新的 MonitorCheck*.exe"""
    env = os.environ.get("MC_EXE")
    if env:
        if os.path.isfile(env):
            return env
        raise FileNotFoundError("环境变量 MC_EXE 指向的文件不存在: %s" % env)

    cands = glob.glob(os.path.join(BASE, "MonitorCheck*.exe"))
    if not cands:
        raise FileNotFoundError(
            "未找到 MonitorCheck*.exe, 请先运行 rebuild.bat 构建, "
            "或用环境变量 MC_EXE 指定 exe 路径")
    return max(cands, key=os.path.getmtime)


def shot_path(name):
    """截屏统一落在脚本所在目录"""
    return os.path.join(PY_DIR, name)
