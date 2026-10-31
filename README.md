# ISP-3A-Lab

影像信号处理（ISP）+ 3A + 画质（IQ）实验仓：从 RAW 走到可控制闭环。  
ISP pipeline + 3A + IQ lab, from RAW to a control loop.

对外名称写 **ISP-3A-Lab**（缩写全大写）。Git 路径仍是小写文件夹名，这是仓库惯例，不是把 ISP 写成 isp。  
The public name is **ISP-3A-Lab** (acronyms stay uppercase). Folder paths stay lowercase. That is git convention, not a claim that ISP is spelled “isp”.

本仓库是可复现实验，不是厂商固件。  
This is a reproducible lab, not vendor firmware.

---

## 岗位怎么看 / Job tracks

同一个仓库，四条投递路径。  
Same repo, four interview paths.

| 岗位 / Track | 先看这些 / Look at |
|---|---|
| 影像调试 / ISP tuning | `python/metrics`, `python/aaa/af.py`, `docs/principles` |
| 影像驱动 / Image-driven 3A | `python/isp`, `python/aaa`, `c/src` |
| 机器人影像 / Robot vision | `python/robot` |
| 具身智能 / Embodied AI | `python/embodied` |

目录 `python/aaa` 表示 3A。Python 包名不能以数字开头，所以不用 `3a`。对外说明一律写 3A（AE / AWB / AF）。  
The folder `python/aaa` means 3A. A Python package cannot start with a digit, so it is not named `3a`. In prose always write 3A (AE / AWB / AF).

细则见 `docs/job-mapping.md`。  
Details: `docs/job-mapping.md`.

---

## 规则 / Rules

每条都是中文在上、英文在下。这里的「语言」若出现，只指 Python / C，不指中文 / English。  
Chinese first, English second. If a rule says “language”, it means Python / C, not Chinese / English.

1. 这不是联发科 / 索尼 / 高通的 ISP 源码。  
   This is not MediaTek / Sony / Qualcomm ISP source.

2. Python 做实验、出图、面试演示；C 对齐产线写法。  
   Python is for experiments, plots, and interview demos. C is the vendor-style core.

3. 算法原理写在 `docs/principles/`，中英文都要有。先改文档，再改 Python，再改 C。原理与编程语言无关，不是与中文 / English 无关。  
   Write algorithm notes in `docs/principles/` in both Chinese and English. Change the note first, then Python, then C. “Language-agnostic” means Python vs C, not Chinese vs English.

4. 每个 `python/**/*.py` 都必须能单独运行，并完成自己的职能。  
   Every `python/**/*.py` file must run on its own and demonstrate its job.

5. 3A 改的是拍摄过程，IQ 评的是画面。两套代码分开放。  
   3A changes the capture. IQ metrics judge the picture. Keep them in different folders.

6. 通用文件保持通用。厂商逻辑（Sony、MTK、Qualcomm 等）只放 `platforms/`。不要把通用的 `ae.py` / `awb.py` / `af.py` 改成某家的实现。  
   Generic files stay generic. Vendor logic (Sony, MTK, Qualcomm, …) goes under `platforms/`. Do not rewrite the generic `ae.py` / `awb.py` / `af.py` into vendor code.

7. `platforms/` 只是扩展位。在有可公开的笔记之前，不建 `sony/` 等厂商目录。  
   `platforms/` is an extension point. Do not add `sony/` or other vendor folders until there are notes you can publish.

8. 不要提交客户图、产线 dump 或受 NDA 约束的 log。调试笔记用自己的话重写。  
   Do not commit customer images, factory dumps, or NDA logs. Rewrite debug notes in your own words.

9. 教学算法（灰世界、双线性 demosaic）是基线，不是可量产的 3A。  
   Teaching algorithms (gray world, bilinear demosaic) are baselines, not shippable 3A.

10. C 目前覆盖 Bayer、demosaic、AE、AWB、AF、SNR。机器人标定和具身闭环暂时只用 Python（OpenCV）。  
    C currently covers Bayer, demosaic, AE, AWB, AF, SNR. Robot calibration and the embodied loop stay Python (OpenCV) for now.

11. 第一版不要做 Python 调 C 的绑定。两套能读的实现，比一套 ABI 更适合面试。  
    Do not add Python↔C bindings in v1. Two readable implementations beat one ABI.

12. Demo 运行时合成数据。以后的真实 RAW / 图卡放 `data/`；敏感文件不要进 git。  
    Demos synthesize data at runtime. Real RAW / charts go in `data/` later. Keep sensitive files out of git.

13. 生成的图和报告放 `output/`（已加入 gitignore）。  
    Generated images and reports go to `output/` (gitignored).

---

## 目录 / Layout

```text
docs/principles/     算法原理（中英文，随时补）
                     algorithm notes (Chinese + English)
python/isp/          通用 ISP + platforms/ 厂商扩展位
                     generic ISP + vendor hooks
python/aaa/          通用 3A（AE / AWB / AF）+ platforms/
                     generic 3A + vendor hooks
python/metrics/      画质 IQ 测试，与 3A 分开
                     IQ tests, separate from 3A
python/robot/        标定、去畸变、运动曝光、时延
                     calibration, undistort, motion AE, latency
python/embodied/     感知 → 决策 → 动作
                     perceive → act loop
c/                   C99：ISP / 3A / SNR
                     C99 library + demos
data/                以后可放真实 RAW / 图卡
                     optional real RAW / charts
output/              生成结果（不入库）
                     generated images (gitignored)
```

---

## 运行 Python / Run Python

在仓库根目录下，每个 Python 文件都可以单独跑。  
From the repo root, every Python file can run alone.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 示例 / examples
python python/isp/demosaic.py
python python/aaa/awb.py
python python/metrics/report.py
python python/robot/calib.py
python python/embodied/loop.py
```

全量冒烟 / full smoke list:

```bash
bash scripts/smoke_python.sh
```

输出 / outputs: `output/<module>/`

---

## 编译 C / Build C

C 覆盖产线里通常用 C 写的模块：Bayer、demosaic、AE、AWB、AF、SNR。  
C covers the blocks production camera code usually ships in C: Bayer, demosaic, AE, AWB, AF, SNR.

```bash
make -C c
./c/bin/demo_pipeline
./c/bin/demo_ae
```

---

## 以后加厂商 / Add a vendor later（Sony / MTK / …）

不要把通用 3A 文件改成厂商代码。  
Do not edit the generic 3A files into vendor code.

1. 调试笔记放 `docs/principles/` 或 `python/aaa/platforms/<vendor>/NOTES.md`  
   Put debug notes in `docs/principles/` or `python/aaa/platforms/<vendor>/NOTES.md`

2. 新增 `python/aaa/platforms/<vendor>/ae.py`（AWB / AF 同理）  
   Add `python/aaa/platforms/<vendor>/ae.py` (same for AWB / AF)

3. 函数名与通用文件保持一致  
   Use the same function names as the generic files

4. 若有可公开的 C 代码，对应放到 `c/src/platforms/<vendor>/`  
   Mirror C under `c/src/platforms/<vendor>/` if you have a public C dump

详见 / see `docs/platforms.md`。
