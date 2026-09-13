# Museum Stamp Print · 套色印章 Skill

**Turn any travel photo into a museum-style multi-layer registration stamp (套色印章) — plus an authentic printmaker's step-by-step proof sheet.**

把一张旅行照片变成博物馆文创风格的多层套色印章，并附一张符合真实套版印刷逻辑的「分版步骤图」。

| Finished stamp 成品 | Step-by-step proof sheet 步骤图 |
|---|---|
| ![Finished stamp](examples/naha-master.png) | ![Step sheet](examples/naha-steps.png) |

*Example: a bingata kimono street scene from Naha, Okinawa. 示例：那霸红型和服街景。*

## What it does / 它做什么

Given one photo, the skill generates:

1. **A finished multi-block stamp print** — the scene reduced to flat geometric ink layers in the photo's own color families, slightly misregistered like real block printing, with a vintage postal-cancellation text strip (`PLACE · YYYY.MM.DD`).
2. **A 4-step stamping diagram (2×2)** — each cell = previous cell + exactly one carved block, ending in the finished print. Real overprint physics throughout:
   - **Translucent inks**: a shape crossing an earlier layer shows a darker mixed tone (multiply-like) — overlap and non-overlap of one shape can never share one color.
   - **Knockout voids**: big foreground blocks (a figure, a garment) are stamped into silhouette-shaped voids carved in the earlier blocks — pure color on bare paper, never "pasted over" the layers below.
   - **One block = one step**: a block's fill and texture appear together; within one pull, colors butt or knock out with thin white gaps, never mix.
   - **Detail-block finale**: the anchor's pattern (e.g. bingata motifs) + keyline + text all land in the final step, so the last transition is a big visible jump.

Face rules: back views have no face; front views get minimal generalized ink-mark features (two dashes for eyes, one stroke for a mouth) — never beautified, never black silhouettes.

## Install / 安装

Works with any agent runtime that supports `SKILL.md`-style skills and an image-generation tool with image-to-image (in WorkBuddy/CodeBuddy that's `ImageGen` with `image1`/`image2`).

**WorkBuddy / CodeBuddy**

```bash
git clone https://github.com/Guzi2005/layered-stamp-skill.git
cp -r layered-stamp-skill ~/.workbuddy/skills/museum-stamp-print
```

**Claude Code (skills directory)**

```bash
git clone https://github.com/Guzi2005/layered-stamp-skill.git
cp -r layered-stamp-skill ~/.claude/skills/museum-stamp-print
```

Requirements: an image-generation tool with image-to-image; Python 3 + Pillow for the final layout step (`pip install Pillow`). No other dependencies.

## Usage / 用法

Just mention the trigger words and hand over a photo:

- 套色印章 / 套版印刷 / 博物馆印章 / 纪念章 / 分版
- stamp print / block-print seal / registration stamp

Orientation: square, portrait and landscape are all supported. By default the skill rolls randomly per run — 70% square, 30% non-square (following the photo's orientation). **If you explicitly ask for 竖版 / 横版 / 方形, your choice always wins.**

## How it works / 工作原理

Whole-sheet generation kept violating step logic (subjects stamped too early, same-pull colors mixing, the finished print copied into every cell), so the skill uses a **deterministic chain route**:

1. **Stage A — master**: generate the finished single stamp from the photo (image-to-image traces contours far better than text alone).
2. **Stage B — chain**: cell 1 = "show only the base block"; each next cell = edit of the previous, stamping exactly one more block. Cross-step overprint rules are restated in every prompt.
3. **Stage C — compose**: Pillow script crops each cell to its print region, normalizes scale, and pastes the 2×2 sheet with numerals and registration crosses — printing is real generation, only layout is code.

Hard-won lessons are baked into the skill (with verification notes): anti-paper-cut NOT-lists, per-row paper-color sampling for watermark removal, over-erase recovery passes for region edits, reverse-closing to keep steps and finished print in sync, and the knockout-void carving logic.

## Author / 作者

**Guzi2005** — 最好是能帮到你 (Hope it helps.)

## License / 许可证

[MIT](LICENSE) — examples included. Case images were generated from the author's own travel photos.
