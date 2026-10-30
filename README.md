# MonitorCheck 显示器检测工具

Windows 平台单文件显示器检测工具，用于快速查看显示器信息并输出各类测试画面，排查坏点、亮斑、色彩异常、拖影等问题。

基于 **Python + tkinter** 原生实现，不依赖 IE / mshta，运行全程无 ActiveX、无安全提示。

当前版本：**v3.1**

## 功能特性

- **显示器信息读取**：品牌、型号、序列号、出厂年月、当前分辨率、刷新率、显卡型号
  - WMI（`WmiMonitorID` / `Win32_VideoController`）主通道
  - 注册表 EDID 解析作为回退：面板名（0xFE）、序列号（0xFF）、生产周/年
- **19 种测试画面**：8 种纯色、灰阶、横竖彩条、SMPTE 彩条、双向渐变、棋盘格、网格、十字准星、暗点检测等，支持自动循环
- **常驻信息栏**：测试画面中上部实时显示显示器信息，每 10 秒增量刷新（不重绘测试画面，不闪屏、不打断循环计时）
- **防休眠**：运行期间阻止系统休眠与屏幕熄灭
- **检测记录（可选）**：按 `R` 开启后，自动把检测结果追加写入同目录的 `显示器检测记录.xlsx`（品牌 / 型号 / 序列号 / 出厂年月 / 分辨率 / 刷新率 / 检测时间），文件已存在则追加；文件被 Excel 占用时自动改写到副本，不丢数据
- **单文件运行**：打包为单个 exe，无需安装 Python 或任何依赖

## 操作方法

| 操作 | 功能 |
| --- | --- |
| 空格 / 鼠标左键 | 下一画面（信息页为开始测试） |
| 鼠标右键双击 | 退出程序 |
| ESC | 退出程序 |
| ← / → | 上一画面 / 下一画面 |
| P | 暂停 / 恢复自动循环 |
| R | 开启 / 关闭检测记录（选择会被记住） |

> 右键单击不会退出，只会在屏幕底部提示「再按一次右键 = 退出程序」，避免测试过程中误触。

## 下载

前往 [Releases](../../releases) 下载最新的 `MonitorCheck_v3.1.exe`，双击即可运行。

## 从源码运行 / 构建

环境要求：Windows + Python 3.12（需自带 tkinter）+ PyInstaller + openpyxl。

```bat
pip install pyinstaller openpyxl
python python\monitor_check.py
```

打包为单文件 exe：

```bat
cd python
pyinstaller --onefile --noconsole --clean --icon icon.ico ^
  --version-file version_info.txt ^
  --exclude-module PIL --exclude-module numpy --exclude-module pandas ^
  --name MonitorCheckPy monitor_check.py
```

> `--exclude-module PIL` 必须保留：openpyxl 会条件性导入 Pillow，不排除会让 exe 多出约 7MB。
> 也可以直接运行 `python\rebuild.bat`：它优先使用 PATH 中的 `pyinstaller`，找不到时回退到常见虚拟环境路径，无需改脚本。

## 项目结构

```
monitor-check/
├── python/
│   ├── monitor_check.py     # 主程序（tkinter GUI）
│   ├── version_info.txt     # exe 版本资源（v3.1）
│   ├── icon.ico             # 应用图标
│   ├── rebuild.bat          # 一键重打包脚本
│   ├── _paths.py            # 验证脚本共用的路径解析（无硬编码路径）
│   └── verify_*.py          # 自动化验证脚本（截屏 / Excel）
└── README.md
```

## 验证脚本（可选）

`python/` 下的脚本用于回归验证，**不含任何硬编码绝对路径**，克隆到任意目录都能运行；待测 exe 默认取项目根目录下最新的 `MonitorCheck*.exe`，也可用环境变量指定。

| 脚本 | 用途 |
| --- | --- |
| `screenshot_test.py` | 启动 exe，在黑 / 白画面阶段各截屏一张 |
| `verify_v4.py` | 验证信息栏每 10 秒刷新，且不打断画面循环 |
| `verify_xlsx.py` | 连跑两次，验证 Excel 新建 + 追加（临时开启记录，结束后自动还原配置与原有记录文件） |

```bat
rem 默认用最新的 MonitorCheck*.exe
python python\verify_v4.py

rem 或显式指定待测 exe
set MC_EXE=D:\tools\MonitorCheck_v3.1.exe
python python\verify_xlsx.py
```

## 版本历史

- **v3.1**（2026-10-30）：右键改为双击退出（单击仅提示）；检测记录改为可选开关（默认关闭，`R` 切换，选择持久化）；修正高 DPI 下信息页行距挤压
- **v3.0**（2026-09-15）：新增 Excel 检测记录导出
- **v2.1**（2026-09-10）：信息栏 10 秒增量刷新，改用 ctypes 轻量枚举
- **v2.0**（2026-09-04）：由 HTA/IExpress 方案重写为 Python + tkinter 原生实现，彻底消除 IE 安全提示
