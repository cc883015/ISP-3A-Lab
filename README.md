# isp-3a-lab

**EN** ISP pipeline + 3A + IQ lab, from RAW to a control loop.  
**中文** 影像信号处理（ISP）+ 3A + 画质（IQ）实验仓：从 RAW 走到可控制闭环。

ISP / 3A / IQ are the words camera people already use. This repo is a lab, not vendor firmware.  
ISP、3A、IQ 是影像同行的常用词。本仓库是可复现实验，不是厂商固件。

---

## Job tracks / 岗位怎么看

Same repo, four interview paths. / 同一个仓库，四条投递路径。

| Track / 岗位 | Look at / 先看这些 |
|---|---|
| ISP tuning / 影像调试 | `python/metrics`, `python/aaa/af.py`, `docs/principles` |
| Image-driven / 3A / 影像驱动 | `python/isp`, `python/aaa`, `c/src` |
| Robot vision / 机器人影像 | `python/robot` |
| Embodied AI / 具身智能 | `python/embodied` |

Details: `docs/job-mapping.md`  
细则见 `docs/job-mapping.md`

---

## Rules / 规则

These rules stay in Chinese and English so an interviewer or an ISP engineer can read either column.  
以下规则中英对照，方便面试官或做过 ISP 的人直接读。

1. **EN** This is not MediaTek / Sony / Qualcomm ISP source.  
   **中文** 这不是联发科 / 索尼 / 高通的 ISP 源码。

2. **EN** Python is for experiments, plots, and interview demos. C is the vendor-style core.  
   **中文** Python 做实验、出图、面试演示；C 对齐产线写法。

3. **EN** Algorithm notes live in `docs/principles/` and stay language-agnostic. Change the note first, then Python, then C.  
   **中文** 算法原理只写在 `docs/principles/`，和语言无关。先改文档，再改 Python，再改 C。

4. **EN** Every `python/**/*.py` file must run on its own and demonstrate its job.  
   **中文** 每个 `python/**/*.py` 都必须能单独运行，并完成自己的职能。

5. **EN** 3A changes the capture. IQ metrics judge the picture. Keep them in different folders.  
   **中文** 3A 改的是拍摄过程，IQ 评的是画面。两套代码分开放。

6. **EN** Generic files stay generic. Vendor logic (Sony, MTK, Qualcomm, …) goes under `platforms/`. Do not rewrite `ae.py` / `awb.py` / `af.py` into vendor code.  
   **中文** 通用文件保持通用。厂商逻辑（Sony、MTK、Qualcomm 等）只放 `platforms/`。不要把 `ae.py` / `awb.py` / `af.py` 改成某家的实现。

7. **EN** `platforms/` is an extension point. Sony (and others) are not added until there are notes you can publish.  
   **中文** `platforms/` 只是扩展位。在有可公开的笔记之前，不建 `sony/` 等厂商目录。

8. **EN** Do not commit customer images, factory dumps, or NDA logs. Rewrite debug notes in your own words.  
   **中文** 不要提交客户图、产线 dump 或受 NDA 约束的 log。调试笔记用自己的话重写。

9. **EN** Teaching algorithms (gray world, bilinear demosaic) are baselines, not shippable 3A.  
   **中文** 教学算法（灰世界、双线性 demosaic）是基线，不是可量产的 3A。

10. **EN** C currently covers Bayer, demosaic, AE, AWB, AF, SNR. Robot calib and the embodied loop stay Python (OpenCV) for now.  
    **中文** C 目前覆盖 Bayer、demosaic、AE、AWB、AF、SNR。机器人标定和具身闭环暂时只用 Python（OpenCV）。

11. **EN** Do not add Python↔C bindings in v1. Two readable implementations beat one ABI.  
    **中文** 第一版不要做 Python 调 C 的绑定。两套能读的实现，比一套 ABI 更适合面试。

12. **EN** Demos synthesize data at runtime. Real RAW / charts go in `data/` later and stay out of git if they are sensitive.  
    **中文** Demo 运行时合成数据。以后的真实 RAW / 图卡放 `data/`；敏感文件不要进 git。

13. **EN** Generated images and reports go to `output/` (gitignored).  
    **中文** 生成的图和报告放 `output/`（已加入 gitignore）。

---

## Layout / 目录

```text
docs/principles/     algorithm notes / 算法原理（随时补）
python/isp/          generic ISP + platforms/ vendor hooks
                     通用 ISP + 厂商扩展位
python/aaa/          generic AE / AWB / AF + platforms/
                     通用 3A + 厂商扩展位
python/metrics/      IQ tests, separate from 3A
                     画质测试，与 3A 分开
python/robot/        calibration, undistort, motion AE, latency
                     标定、去畸变、运动曝光、时延
python/embodied/     perceive → act loop
                     感知 → 决策 → 动作
c/                   C99 library + demos for ISP / 3A / SNR
                     C99 库与演示
data/                optional real RAW / charts
                     以后可放真实 RAW / 图卡
output/              generated images (gitignored)
                     生成结果（不入库）
```

---

## Run Python / 运行 Python

From the repo root, every Python file can run alone.  
在仓库根目录下，每个 Python 文件都可以单独跑。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# examples / 示例
python python/isp/demosaic.py
python python/aaa/awb.py
python python/metrics/report.py
python python/robot/calib.py
python python/embodied/loop.py
```

Full smoke list / 全量冒烟：

```bash
bash scripts/smoke_python.sh
```

Outputs / 输出：`output/<module>/`

---

## Build C / 编译 C

C covers the blocks production camera code usually ships in C: Bayer, demosaic, AE, AWB, AF, SNR.  
C 覆盖产线里通常用 C 写的模块：Bayer、demosaic、AE、AWB、AF、SNR。

```bash
make -C c
./c/bin/demo_pipeline
./c/bin/demo_ae
```

---

## Add a vendor later / 以后加厂商（Sony / MTK / …）

**EN** Do not edit the generic 3A files into vendor code.  
**中文** 不要把通用 3A 文件改成厂商代码。

1. **EN** Put debug notes in `docs/principles/` or `python/aaa/platforms/<vendor>/NOTES.md`  
   **中文** 调试笔记放 `docs/principles/` 或 `python/aaa/platforms/<vendor>/NOTES.md`

2. **EN** Add `python/aaa/platforms/<vendor>/ae.py` (same for AWB / AF)  
   **中文** 新增 `python/aaa/platforms/<vendor>/ae.py`（AWB / AF 同理）

3. **EN** Use the same function names as the generic files  
   **中文** 函数名与通用文件保持一致

4. **EN** Mirror C under `c/src/platforms/<vendor>/` if you have a public C dump  
   **中文** 若有可公开的 C 代码，对应放到 `c/src/platforms/<vendor>/`

See / 详见 `docs/platforms.md`。
