# Museum Stamp Print · 套色印章 Skill

**把一张旅行照片变成博物馆文创风格的多层套色印章 + 真实套版印刷分版步骤图。**  
*Turn a travel photo into a museum-style multi-layer registration stamp + an authentic printmaker's step-by-step proof sheet.*

| 原片 Source | 中性成品 Neutral | 步骤图 Steps |
|---|---|---|
| ![source](examples/naha-source.jpg) | ![neutral](examples/naha-master.png) | ![steps](examples/naha-steps.png) |
| 2025年夏那霸琉球装束体验 | 默认：真实橡皮章墨质感 | 2×2 分版过程 |

## 三种风格 Three styles

| 中性 Neutral | 干性 Dry | 油性 Oily |
|---|---|---|
| ![neutral](examples/naha-master.png) | ![dry](examples/naha-style-dry.png) | ![oily](examples/naha-style-oily.png) |
| **默认**。半透明橡皮章墨、硬边、轻微叠印、颗粒纹理。Default translucent rubber-stamp ink, hard edges, light overprint, grain. | **更干**。网点/丝网网格、明显缺墨、干辊留白、边缘枯涩，像快没墨时的真实印刷。Halftone dots + screen mesh, ink-starved streaks, broken edges. | **更油**。强覆盖力、边缘有水彩晕染、带 1-2 处未干时抹开的真实湿墨拖痕。Dense coverage, wet-ink halos, 1-2 accidental smudge marks. |

三种风格都支持：直接说「我要干性/中性/油性」即可指定；不说的话，每次按 **2 : 6 : 2（干/中/油）** 随机抽签决定。风格也可以与横竖方方向参数同时指定。

## 它做什么 / What it does

给一张照片，生成两件东西：

1. **一枚成品套色印章**——把画面压成 5-6 个几何色块，保持原片构图、人物比例和主体轮廓；边缘有真实套版错位（1-3 mm），底部带邮戳风文字 `地点 · YYYY.MM.DD`。
2. **一张 2×2 分版步骤图**——每一格 = 前一格 + 正好一个新色版，最后一格就是成品。逻辑严格遵守真实套色印章：
   - **半透明叠印**：色块压在前一色上会出现更深的混色，同一形状在纸面和压墨处的颜色一定不同；
   - **挖空留白**：大块前景（如人物/琉球装束）不会「盖住」下层，而是前一版提前刻出空白、后续直接盖在纸上，边缘硬接；
   - **一版一步**：一块版的所有颜色同一步盖完，版内颜色只并置或白缝隔开，不互相透混；
   - **收官跳变**：最后一格同时盖「纹样细节版 + 轮廓线 + 文字」，变化最大，绝不只是加一行字。

人物规则：背影无脸；正面只给极简概括五官（两点眼 + 一笔嘴），不美颜、不黑影。

## 安装 / Install

支持任何使用 `SKILL.md` 风格 skill 且带 image-to-image 生图工具的 Agent 环境（WorkBuddy/CodeBuddy 里是 `ImageGen` 的 `image1`/`image2`，其他环境按本地参数名适配）。

```bash
git clone https://github.com/Guzi2005/layered-stamp-skill.git

# WorkBuddy / CodeBuddy
cp -r layered-stamp-skill ~/.workbuddy/skills/museum-stamp-print

# Claude Code
cp -r layered-stamp-skill ~/.claude/skills/museum-stamp-print
```

只需要 Python 3 + Pillow 做最后的拼版（`pip install Pillow`），其余全靠生图模型完成。

## 用法 / Usage

上传照片，直接说触发词即可：

- 套色印章 / 套版印刷 / 博物馆印章 / 纪念章 / 分版 / stamp print / block-print seal / registration stamp
- 加风格：「做一套干性套色印章」「油性的」「要方图」「横版，油性」

风格：默认随机掷签——**干性 : 中性 : 油性 = 2 : 6 : 2**；你一旦点名「干性/中性/油性」，你的选择直接覆盖随机。

方向：默认随机掷签——70% 方形、30% 非方形（竖图出竖版、横图出横版、方图按构图选）；你一旦说「方形/竖版/横版」，你的选择直接覆盖随机。

## 工作原理 / How it works

整图一次生成 4 格容易违反步骤逻辑（人物提前出现、同一版颜色互混、成品被复制到每格），所以用**链式确定性流程**：

1. **Stage A 母版**：用原片 image-to-image 生成最终成品，轮廓最稳。
2. **Stage B 链式分格**：第 1 格 = 从母版删除到只剩底色版；后面每格 = 以上一格为底，只盖一个新色版。每次 prompt 都重申跨步叠印规则。
3. **Stage C 拼版**：用 Pillow 统一裁切、归一化比例、去水印、画序号和套准十字，只有排版是代码，印刷本身全是生图。

这个流程里还固定了几条实战经验：防剪纸漂移的 NOT 列表、水印按行采样纸色、区域编辑过擦后的恢复 pass、反向收官保证步骤与成品对号、挖空留白逻辑、无人物外轮廓虚线。

## 作者 / Author

**Guzi2005** — 最好是能帮到你

## 许可证 / License

[MIT](LICENSE) · 示例图片均来自作者本人的旅行照片。
