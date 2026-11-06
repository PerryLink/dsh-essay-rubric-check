#!/usr/bin/env python3
"""README visuals for dsh-essay-rubric-check, derived from the shipped pipeline.

Two figures, both read off the material the repository actually ships rather
than a generic template:

  hero 1440x576 (Pillow, four files: zh/en x light/dark)
      A rubric sheet as a scorecard. The header carries the student, rubric
      version and totals; each of three criteria is one bar whose end is that
      criterion's `maxScore`. Row 2 scores 22 against a max of 20 (the value in
      tests/fixtures/ER-002/ER-002-unsafe.json), row 3 carries a score with an
      empty `evidenceQuote` column (tests/fixtures/ER-004/ER-004-unsafe.json).
      Two finding lines below name the rule, the row and the field — the
      locator the plugin actually returns — and the strip keeps issues and
      skipped apart, with the verdict left to the reviewer.

  flow 1100x660 (hand-written SVG, two files: light/dark)
      A margin-annotation sheet, not a node row: the rubric sheet on the left
      is pinned 1-6 in the margin of the cell each finding is about (missing
      `student`, a repeated `criterionNo`, score 22 against 20, a blank
      `criterion`/`levelDesc`, a blank `evidenceQuote`, and the sheet total).
      Every pin opens exactly one card on the right that carries the rule id,
      severity, scope (header / row / total) and the locator as
      `row N · column <field>`. Pin 6 sits on the rule pack: ER-003's
      expression still points at the placeholder `dimensionRef`, so nothing is
      summed and the rule reports itself in `skipped`. The report band keeps
      `issues[]` and `skipped[]` in separate cells and sends the conclusion to
      the reviewer.

Text values come from the repository's own fixtures and rule pack, not from
imagination:
  tests/fixtures/ER-002/ER-002-unsafe.json  (score 22, maxScore 20)
  tests/fixtures/ER-004/ER-004-unsafe.json  (score 18, evidenceQuote "")
  tests/fixtures/ER-005/ER-005-unsafe.json  (two rows with criterionNo 1)
  tests/fixtures/ER-006/ER-006-unsafe.json  (no header student)
  rules/essay-rubric-check.yaml             (ER-001..ER-006, 2026.1)
  src/shared/render.ts                      (locator wording: row / column)

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow + Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf.
"""
from __future__ import annotations

import math
import os
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

FONT_CJK = r"C:\Windows\Fonts\msyh.ttc"
FONT_CJK_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"
for _p in (FONT_CJK, FONT_CJK_BOLD, FONT_MONO, FONT_MONO_BOLD):
    if not os.path.exists(_p):
        raise SystemExit(f"FATAL: font missing: {_p}")

FONT_FILES = {"cjk": FONT_CJK, "cjk_bold": FONT_CJK_BOLD,
              "mono": FONT_MONO, "mono_bold": FONT_MONO_BOLD}

RADIUS = 20
SHADOW = 24

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", card_edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent2="#16a34a",
        pill="#ece7f9", band="#f5f2fb", band_alt="#faf8fe",
        grid="#e7e4f0", rule="#dcd8ea",
        mark="#b45309", mark_bg="#fdf3e9", on_accent="#ffffff",
        shadow=(32, 26, 64), glow2="#7a68c9", shadow_alpha=0.10,
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", card_edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent2="#3fb950",
        pill="#242d42", band="#202839", band_alt="#1e2534",
        grid="#262f42", rule="#2b3348",
        mark="#d9a441", mark_bg="#2a2216", on_accent="#0c1016",
        shadow=(0, 0, 0), glow2="#8496f5", shadow_alpha=0.45,
    ),
}


def font(size: int, kind: str = "cjk_bold") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], size)


def hx(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(base)
    a, b = hx(c1), hx(c2)
    for y in range(h):
        t = 0.15 * (y / h) + 0.85 * (y / h) ** 1.35
        d.line([(0, y), (w, y)],
               fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: tuple,
         alpha: int = 40) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(9, 0, -1):
        rr = r * i / 9
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=color + (int(alpha * (1 - i / 10)),))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def card(img: Image.Image, box: tuple, s: dict, radius: int = RADIUS,
         shadow: int = SHADOW, fill: str | None = None,
         edge: str | None = None) -> Image.Image:
    """A soft-shadowed rounded card on the gradient background."""
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(shadow, 0, -3):
        sd.rounded_rectangle([x0 - i // 5, y0 + i // 2, x1 + i // 5, y1 + i],
                             radius=radius + i // 5,
                             fill=s["shadow"] + (int(9 * (1 - i / shadow)),))
    base = Image.alpha_composite(img.convert("RGBA"),
                                 sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                        outline=hx(edge or s["card_edge"]), width=2)
    return base.convert("RGB")


_SCRATCH = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: int, kind: str) -> float:
    return _SCRATCH.textlength(text, font=font(size, kind))


def require_w(text: str, size: int, kind: str, max_w: float, what: str) -> None:
    """Fail loudly instead of shipping a clipped label."""
    w = measure(text, size, kind)
    if w > max_w + 0.4:
        raise SystemExit(
            f"FATAL: {what} overflows: {text!r} needs {w:.1f}px > {max_w}px")


def fit(text: str, kind: str, max_w: float, start: int, minimum: int) -> int:
    size = start
    while size > minimum:
        if measure(text, size, kind) <= max_w:
            return size
        size -= 1
    if measure(text, size, kind) <= max_w:
        return size
    raise SystemExit(
        f"FATAL: text does not fit {max_w}px at >= {minimum}px: {text!r}")


def fit_lines(lines: list[str], kind: str, max_w: float, start: int,
              minimum: int) -> int:
    return min(fit(t, kind, max_w, start, minimum) for t in lines)


def pill(img: Image.Image, xy: tuple[int, int], text: str, s: dict,
         size: int = 16, fg: str | None = None, bg: str | None = None,
         kind: str = "cjk_bold") -> tuple[int, int]:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    h = size + 20
    d.rounded_rectangle([x, y, x + w + 30, y + h], radius=h // 2,
                        fill=hx(bg or s["pill"]))
    d.text((x + 15, y + h / 2), text, font=f, fill=hx(fg or s["accent"]),
           anchor="lm")
    return int(x + w + 30), int(y + h)


def chip(img: Image.Image, xy: tuple[int, int], text: str, fg: str, bg: str,
         size: int = 11, kind: str = "cjk_bold", padx: int = 9,
         height: int = 20) -> int:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    d.rounded_rectangle([x, y, x + w + padx * 2, y + height],
                        radius=height // 2, fill=hx(bg))
    d.text((x + padx, y + height / 2), text, font=f, fill=hx(fg), anchor="lm")
    return int(w + padx * 2)


def dash_rect(d: ImageDraw.ImageDraw, box: tuple[float, float, float, float],
              color: str, width: int = 2, dash: int = 7, gap: int = 4) -> None:
    x0, y0, x1, y1 = box
    for a, b in (((x0, y0), (x1, y0)), ((x0, y1), (x1, y1)),
                 ((x0, y0), (x0, y1)), ((x1, y0), (x1, y1))):
        dist = math.hypot(b[0] - a[0], b[1] - a[1])
        n = int(dist // (dash + gap)) + 1
        for i in range(n):
            t0 = i * (dash + gap) / dist
            t1 = min((i * (dash + gap) + dash) / dist, 1.0)
            if t0 >= 1:
                break
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                    (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                   fill=hx(color), width=width)


# --------------------------------------------------------------------------- hero
# Every value below is an excerpt of a fixture in this repository; see the
# module docstring for the mapping.
HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 核查器",
        value=["六条规则，只核对一张表", "差异落到行号与栏名"],
        sub=["读一份评分表：表头加每项一行，核齐备、分值、合计、",
             "定位栏、序号与表头归属；不判作文好坏，不改原件。"],
        meta="ER-001..ER-006 · 规则包即数据 · skipped 逐条说明",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        sheet_title="作文评分表 · rows[]",
        sheet_chip="只读原件",
        sheet_head="某某考生 · 某某作文题 · 2026 版 · 满分 20",
        dims=["内容", "语言", "结构"],
        scores=[(18, 20), (22, 20), (18, 20)],
        quotes=["原文 ¶4", "原文 ¶4", "— 空"],
        sheet_note="刻度终点 = 该项分值；列名忽略大小写、空格与下划线",
        f1=dict(rule="ER-002", sev="warn", loc="第 2 行 · 字段 score",
                text="得分 22 超过该项分值 20——只比较两个数，不判断分数与作文是否相称"),
        f2=dict(rule="ER-004", sev="warn", loc="第 3 行 · 字段 evidenceQuote",
                text="给了分，却没有原文定位——只核对栏目是否为空，不核对引文真伪"),
        strip_l="issues[] 2 条 · skipped[] 1 条",
        strip_r="结论留给阅卷人",
        strip_sub="summary { error 0 · warn 2 · info 0 } · ER-003 合计未配置 → skipped",
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · checker",
        value=["Six rules read one rubric sheet", "differences land on row + column"],
        sub=["Header plus one row per criterion, six checks,",
             "no verdict and no rewriting of the original."],
        meta="ER-001..ER-006 · rules are data · skipped explained",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        sheet_title="Rubric sheet · rows[]",
        sheet_chip="read-only",
        sheet_head="Some student · Some essay prompt · 2026 · full score 20",
        dims=["Content", "Language", "Structure"],
        scores=[(18, 20), (22, 20), (18, 20)],
        quotes=["¶4 quoted", "¶4 quoted", "— blank"],
        sheet_note="bar end = that criterion's maxScore; column names ignore case and spaces",
        f1=dict(rule="ER-002", sev="warn", loc="row 2 · column score",
                text="score 22 against maxScore 20 — compares two numbers, not the essay"),
        f2=dict(rule="ER-004", sev="warn", loc="row 3 · column evidenceQuote",
                text="scored with no quote — checks the column is filled, not that the quote is real"),
        strip_l="issues[] 2 · skipped[] 1",
        strip_r="the reviewer decides",
        strip_sub="summary { error 0 · warn 2 · info 0 } · ER-003 total not configured → skipped",
    ),
}


def hero(lang: str, skin: str) -> None:
    s = SKIN[skin]
    H = HERO[lang]
    W, HT = 1440, 576
    img = gradient(W, HT, s["bg_from"], s["bg_to"])
    img = glow(img, 1180, 30, 420, hx(s["accent"]),
               24 if skin == "light" else 38)
    img = glow(img, 90, 580, 300, hx(s["glow2"]),
               10 if skin == "light" else 16)

    d = ImageDraw.Draw(img)
    m = 64
    col_w = 596

    # ---- left column: kicker / title / value / sub / meta / footer -----------
    pill(img, (m, 56), H["kicker"], s, size=17)
    d = ImageDraw.Draw(img)

    title_size = fit("dsh-essay-rubric-check", "mono_bold", col_w, 58, 48)
    d.text((m - 2, 118), "dsh-essay-rubric-check",
           font=font(title_size, "mono_bold"), fill=hx(s["text"]))

    vf = fit_lines(H["value"], "cjk_bold", col_w, 42, 34)
    for i, line in enumerate(H["value"]):
        d.text((m, 204 + i * 56), line, font=font(vf, "cjk_bold"),
               fill=hx(s["text"]))

    sf = font(22, "cjk")
    for i, line in enumerate(H["sub"]):
        require_w(line, 22, "cjk", col_w, "hero sub")
        d.text((m + 1, 334 + i * 34), line, font=sf, fill=hx(s["sub"]))

    require_w(H["meta"], 19, "cjk", col_w, "hero meta")
    require_w(H["foot"], 16, "cjk", col_w, "hero footer")
    d.text((m + 1, 428), H["meta"], font=font(19, "cjk"), fill=hx(s["faint"]))
    d.line([m + 1, 480, m + col_w - 4, 480], fill=hx(s["grid"]), width=2)
    d.text((m + 1, 494), H["foot"], font=font(16, "cjk"), fill=hx(s["faint"]))

    # ---- right: the rubric sheet as a scorecard -----------------------------
    img = card(img, (700, 40, 1376, 338), s, radius=RADIUS, shadow=SHADOW)
    d = ImageDraw.Draw(img)
    d.text((724, 58), H["sheet_title"], font=font(17, "cjk_bold"),
           fill=hx(s["accent"]))
    cw = measure(H["sheet_chip"], 11, "cjk")
    chip(img, (1352 - int(cw) - 18, 54), H["sheet_chip"], s["accent"],
         s["pill"], size=11)
    d = ImageDraw.Draw(img)
    d.text((724, 88), H["sheet_head"], font=font(13, "cjk"), fill=hx(s["sub"]))
    require_w(H["sheet_head"], 13, "cjk", 620, "sheet header")

    bar_x0, bar_x1 = 752, 1070          # bar end = maxScore
    tick_lo, tick_hi = 32, 55
    for r, (score, max_score) in enumerate(H["scores"]):
        ry = 112 + r * 62
        over = score > max_score
        d.text((724, ry + 8), f"{r + 1:02d}", font=font(10, "mono"),
               fill=hx(s["faint"]))
        d.text((752, ry + 2), H["dims"][r], font=font(16, "cjk_bold"),
               fill=hx(s["text"]))

        # the score against the criterion's maximum, right-aligned
        value = f"{score} / {max_score}"
        vf2 = font(14, "mono_bold" if over else "mono")
        vcol = s["mark"] if over else s["text"]
        d.text((1188, ry + 6), value, font=vf2, fill=hx(vcol), anchor="ra")
        require_w(value, 14, "mono_bold" if over else "mono", 64,
                  "score value")

        # the quote column: filled, or visibly empty
        empty = H["quotes"][r].startswith("—")
        qbox = (1204, ry + 5, 1352, ry + 33)
        d.rounded_rectangle(qbox, radius=8,
                            fill=hx(s["mark_bg"] if empty else s["band"]))
        if empty:
            dash_rect(d, qbox, s["mark"], width=2, dash=6, gap=3)
        d.text((1278, ry + 19), H["quotes"][r], font=font(10.5, "cjk"),
               fill=hx(s["mark"] if empty else s["sub"]), anchor="mm")
        require_w(H["quotes"][r], 10.5, "cjk", 132, "quote slot")

        # bar: track = maxScore, fill = score, overshoot marked past the tick
        d.rounded_rectangle([bar_x0, ry + 39, bar_x1, ry + 48], radius=5,
                            fill=hx(s["grid"]))
        ratio = min(score / max_score, 1.0)
        fill_w = int((bar_x1 - bar_x0) * ratio)
        d.rounded_rectangle([bar_x0, ry + 39, bar_x0 + fill_w, ry + 48],
                            radius=5, fill=hx(s["accent"]))
        if over:
            extra = int((bar_x1 - bar_x0) * (score / max_score - 1))
            seg = (bar_x1, ry + 39, bar_x1 + extra, ry + 48)
            d.rounded_rectangle(seg, radius=5, fill=hx(s["mark"]))
            d.ellipse([bar_x1 + extra - 4, ry + 39, bar_x1 + extra + 6,
                       ry + 48], fill=hx(s["mark"]))
        d.line([(bar_x1, ry + tick_lo), (bar_x1, ry + tick_hi)],
               fill=hx(s["faint"]), width=2)

    d.text((724, 312), H["sheet_note"], font=font(11.5, "cjk"),
           fill=hx(s["faint"]))
    require_w(H["sheet_note"], 11.5, "cjk", 628, "sheet note")

    # ---- right: two located findings ----------------------------------------
    img = card(img, (700, 352, 1376, 470), s, radius=18, shadow=20)
    d = ImageDraw.Draw(img)
    for row, key in ((0, "f1"), (1, "f2")):
        A = H[key]
        y = 366 + row * 58
        d.text((724, y), A["rule"], font=font(12.5, "mono_bold"),
               fill=hx(s["accent"]))
        rw = measure(A["rule"], 12.5, "mono_bold")
        chip(img, (724 + int(rw) + 10, y - 4), A["sev"], s["accent"],
             s["pill"], size=10, padx=8, height=18)
        d = ImageDraw.Draw(img)
        lk = "cjk" if lang == "zh" else "mono"
        d.text((1352, y + 1), A["loc"], font=font(11, lk),
               fill=hx(s["sub"]), anchor="ra")
        require_w(A["loc"], 11, lk, 300, "finding locator")
        d.text((724, y + 25), A["text"],
               font=font(13 if row == 0 else 12.5, "cjk"),
               fill=hx(s["text"]))
        require_w(A["text"], 13 if row == 0 else 12.5, "cjk", 628,
                  "finding text")

    # ---- right: report strip, issues and skipped kept apart ------------------
    img = card(img, (700, 486, 1376, 546), s, radius=18, shadow=16)
    d = ImageDraw.Draw(img)
    d.text((724, 500), H["strip_l"], font=font(13, "cjk"),
           fill=hx(s["text"]))
    d.text((1352, 499), H["strip_r"], font=font(13.5, "cjk_bold"),
           fill=hx(s["accent2"]), anchor="ra")
    d.text((724, 522), H["strip_sub"], font=font(11, "cjk"),
           fill=hx(s["faint"]))
    rw = measure(H["strip_r"], 13.5, "cjk_bold")
    total = measure(H["strip_l"], 13, "cjk") + rw + 56
    if total > 628:
        raise SystemExit(f"FATAL: hero report strip overflows ({total:.1f}px)")
    require_w(H["strip_sub"], 11, "cjk", 628, "hero report sub")
    name = f"dsh-essay-rubric-check-hero-{lang}-{skin}.webp"
    img.save(os.path.join(OUT, name), "WEBP", quality=92, method=6)
    print(f"wrote {name} ({W}×{HT})")


# --------------------------------------------------------------------------- flow
FLOW = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        panel="#ffffff", card="#ffffff", edge="#e6e2ef", band="#f5f2fb",
        band_alt="#faf8fe",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent2="#16a34a", rule="#dcd8ea",
        mark="#b45309", mark_bg="#fdf3e9", on_accent="#ffffff",
        shadow="0.10",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        panel="#1b2231", card="#1b2231", edge="#2e374b", band="#202839",
        band_alt="#1e2534",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent2="#3fb950", rule="#2b3348",
        mark="#d9a441", mark_bg="#2a2216", on_accent="#0c1016",
        shadow="0.45",
    ),
}

FONT_CSS_CJK = ("'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',"
                "'Source Han Sans SC',sans-serif")
FONT_CSS_MONO = ("'Consolas','SFMono-Regular','Menlo',ui-monospace,monospace")

# pin, rule, severity, scope, found, locator
CARDS = [
    ("1", "ER-006", "warn", "header",
     "the sheet names no student", "header · column student"),
    ("2", "ER-005", "warn", "row",
     "criterionNo “1” repeats", "row 1 · column criterionNo"),
    ("3", "ER-002", "warn", "row",
     "score 22 > maxScore 20", "row 2 · column score"),
    ("4", "ER-001", "warn", "row",
     "criterion and levelDesc both empty", "row 3 · column criterion"),
    ("5", "ER-004", "warn", "row",
     "scored, but no evidenceQuote", "row 3 · column evidenceQuote"),
    ("6", "ER-003", "skip", "total",
     "expression sums a placeholder only", "skipped · nothing was summed"),
]


class Svg:
    """Tiny SVG writer that measures every label before it is emitted."""

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.overflows: list[str] = []

    def add(self, markup: str) -> None:
        self.parts.append(markup)

    def text(self, x: float, y: float, content: str, size: float, fill: str, *,
             anchor: str = "start", weight: int | None = None,
             mono: bool = False, max_w: float | None = None,
             opacity: float | None = None) -> None:
        kind = ("mono" if mono else "cjk") + ("_bold" if weight else "")
        if max_w is not None:
            w = measure(content, size, kind)
            if w > max_w + 0.4:
                self.overflows.append(
                    f"{content!r} needs {w:.1f}px > {max_w}px")
        family = FONT_CSS_MONO if mono else FONT_CSS_CJK
        attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"',
                 f'font-family="{family}"', f'font-size="{size}"']
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<text {" ".join(attrs)}>{escape(content)}</text>')

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str,
             rx: float = 0, stroke: str | None = None, sw: float = 1.5,
             shadow: bool = False, dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"']
        if rx:
            attrs.append(f'rx="{rx}"')
        attrs.append(f'fill="{fill}"')
        if opacity is not None:
            attrs.append(f'fill-opacity="{opacity}"')
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if shadow:
            attrs.append('filter="url(#soft)"')
        self.add(f'<rect {" ".join(attrs)}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, *, stroke: str,
             sw: float = 1.5, dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
                 f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<line {" ".join(attrs)}/>')

    def circle(self, cx: float, cy: float, r: float, *, fill: str,
               stroke: str | None = None, sw: float = 1.5,
               dash: str | None = None) -> None:
        attrs = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{fill}"']
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        self.add(f'<circle {" ".join(attrs)}/>')

    def chip(self, x: float, y: float, label: str, fg: str, bg: str, *,
             size: float = 10.5, pad: float = 9, height: float = 20,
             mono: bool = False, weight: int | None = None,
             anchor: str = "start") -> float:
        """A pill; returns its left edge when anchored right, else its width."""
        kind = ("mono" if mono else "cjk") + ("_bold" if weight else "")
        w = measure(label, size, kind) + pad * 2
        left = x - w if anchor == "end" else x
        self.rect(left, y, w, height, fill=bg, rx=height / 2)
        self.text(left + pad, y + height / 2 + size * 0.34, label, size, fg,
                  weight=weight, mono=mono)
        if anchor == "end":
            return left
        return w

    def svg(self, w: int, h: int, label: str) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" '
                f'height="{h}" viewBox="0 0 {w} {h}" role="img" '
                f'aria-label="{escape(label)}">')
        return "\n".join([head, *self.parts, "</svg>"]) + "\n"


def flow_svg(skin: str) -> str:
    s = FLOW[skin]
    W, H = 1100, 660
    v = Svg()

    v.add("<defs>")
    v.add(f'<linearGradient id="bg" x1="0" y1="0" x2="0.3" y2="1">'
          f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
          f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    v.add(f'<filter id="soft" x="-30%" y="-30%" width="160%" height="170%">'
          f'<feDropShadow dx="0" dy="7" stdDeviation="9" '
          f'flood-color="#16122c" flood-opacity="{s["shadow"]}"/></filter>')
    v.add("</defs>")
    v.add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

    def pin(cx: float, cy: float, label: str) -> None:
        if label == "6":
            v.circle(cx, cy, 8.6, fill=s["panel"], stroke=s["mark"], sw=1.6,
                     dash="3 2")
            v.text(cx, cy + 3.7, label, 10, s["mark"], anchor="middle",
                   weight=700, mono=True)
        else:
            v.circle(cx, cy, 8.6, fill=s["accent"])
            v.text(cx, cy + 3.7, label, 10, s["on_accent"], anchor="middle",
                   weight=700, mono=True)

    # ---- header -------------------------------------------------------------
    v.text(44, 58, "dsh-essay-rubric-check", 28, s["text"], weight=700, mono=True,
           max_w=640)
    v.text(44, 86,
           "essay_rubric_check: one rubric sheet in, a located finding list out "
           "— every numbered pin opens one finding card.",
           15, s["sub"], max_w=850)
    v.chip(1056, 36, "rule pack 2026.1 · 6 rules", s["accent"], s["band"],
           size=12, pad=12, height=26, anchor="end")

    # ---- left: the rubric sheet, pinned in the margin -----------------------
    v.rect(44, 106, 604, 394, fill=s["panel"], rx=20, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.text(62, 132, "MATERIAL · rubric sheet", 11.5, s["faint"], mono=True,
           max_w=240)
    v.chip(630, 120, "read-only", s["accent"], s["band"], size=10.5, pad=10,
           height=20, anchor="end")
    v.text(62, 154, "file · material → parseMaterial() → header + rows[]",
           11.5, s["accent"], mono=True, max_w=520)

    # header band: the sheet-level fields ER-006 reads
    v.rect(56, 166, 580, 42, fill=s["band"], rx=10)
    fields = [("student", "—", "1"), ("rubricVersion", "2026", None),
              ("totalScore", "18", None), ("fullScore", "20", None)]
    fx = [70, 208, 346, 484]
    for i, (key, value, num) in enumerate(fields):
        x = fx[i]
        if num is not None:
            pin(x + 12, 190, num)
            tx = x + 26
        else:
            tx = x
        v.text(tx, 183, key, 11, s["faint"], mono=True, max_w=100)
        v.text(tx, 203, value, 12.5,
               s["mark"] if key == "student" else s["text"], mono=True,
               weight=700 if key == "student" else None, max_w=95)

    # table head
    v.rect(56, 216, 580, 28, fill=s["band"], rx=8)
    v.text(68, 235, "No.", 11, s["sub"], max_w=52)
    v.text(128, 235, "Criterion · level", 11, s["sub"], max_w=196)
    v.text(392, 235, "Max", 11, s["sub"], anchor="end", max_w=60)
    v.text(468, 235, "Score", 11, s["sub"], anchor="end", max_w=62)
    v.text(484, 235, "Quote", 11, s["sub"], max_w=120)

    rows = [
        dict(sid="1", crit="Content · clear focus", score="18", quote="¶4 · quoted",
             crit_pin=None, no_pin=None, score_pin=None, quote_pin=None),
        dict(sid="1", crit="Language · fluent", score="22", quote="¶4 · quoted",
             crit_pin=None, no_pin="2", score_pin="3", quote_pin=None),
        dict(sid="2", crit="— · —", score="18", quote="—",
             crit_pin="4", no_pin=None, score_pin=None, quote_pin="5"),
    ]
    for r, row in enumerate(rows):
        top = 244 + r * 43
        cy = top + 21
        if r < len(rows) - 1:
            v.line(62, top + 43, 630, top + 43, stroke=s["rule"], sw=1)

        # No. cell — the repeated criterion number on row 2
        if row["no_pin"]:
            v.rect(68, top + 8, 60, 26, fill=s["mark_bg"], rx=6,
                   stroke=s["mark"], sw=1.4, dash="4 3")
            pin(86, cy, row["no_pin"])
            v.text(100, cy + 4, row["sid"], 11.5, s["text"], mono=True,
                   max_w=20)
        else:
            v.text(76, cy + 4, row["sid"], 11.5, s["text"], mono=True,
                   max_w=20)

        # Criterion / level cell
        if row["crit_pin"]:
            v.rect(128, top + 8, 200, 26, fill=s["mark_bg"], rx=6,
                   stroke=s["mark"], sw=1.4, dash="4 3")
            pin(146, cy, row["crit_pin"])
            v.text(162, cy + 4, row["crit"], 11.5, s["mark"], max_w=156)
        else:
            v.text(136, cy + 4, row["crit"], 11.5, s["text"], max_w=184)

        # Max / Score cells — 22 is read against the 20 this row declares
        v.text(404, cy + 4, "20", 11.5, s["sub"], mono=True, anchor="end",
               max_w=40)
        if row["score_pin"]:
            v.rect(400, top + 8, 76, 26, fill=s["mark_bg"], rx=6,
                   stroke=s["mark"], sw=1.4, dash="4 3")
            pin(416, cy, row["score_pin"])
            v.text(468, cy + 4, row["score"], 11.5, s["mark"], mono=True,
                   weight=700, anchor="end", max_w=40)
        else:
            v.text(468, cy + 4, row["score"], 11.5, s["text"], mono=True,
                   anchor="end", max_w=40)

        # Quote cell
        if row["quote_pin"]:
            v.rect(476, top + 8, 148, 26, fill=s["mark_bg"], rx=6,
                   stroke=s["mark"], sw=1.4, dash="4 3")
            pin(494, cy, row["quote_pin"])
            v.text(510, cy + 4, row["quote"], 11.5, s["mark"], max_w=108)
        else:
            v.text(484, cy + 4, row["quote"], 11.5, s["text"], max_w=136)

    # columns the pack reads, then the rule pack itself (pin 6 lives here)
    v.text(56, 392,
           "columns read: criterionNo · criterion · levelDesc · maxScore · "
           "score · evidenceQuote", 11, s["faint"], mono=True, max_w=580)

    v.rect(56, 404, 580, 84, fill=s["band_alt"], rx=12, stroke=s["accent"],
           sw=1.4, dash="5 4")
    v.text(72, 428, "rules/essay-rubric-check.yaml", 11.5, s["text"],
           mono=True, weight=700, max_w=330)
    v.chip(620, 414, "2026.1", s["accent"], s["band"], size=10.5, pad=10,
           height=20, anchor="end")
    v.text(72, 448,
           "validated on load, not trusted · excerpt ≥ 8 chars · kind caps severity",
           11, s["faint"], max_w=540)
    pin(88, 466, "6")
    v.text(106, 470,
           "ER-003 expression → dimensionRef — a placeholder, so nothing is summed",
           11, s["mark"], max_w=510)

    # ---- right: one card per pin, carrying rule · severity · scope · locator
    v.rect(664, 106, 392, 394, fill=s["panel"], rx=20, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.text(682, 132, "runCheck() → findings", 11.5, s["faint"], mono=True,
           max_w=260)
    v.text(682, 152, "rule · severity · scope · locator (row + column)",
           11, s["faint"], max_w=350)

    for i, (num, rid, sev, scope, found, loc) in enumerate(CARDS):
        cy = 160 + i * 56
        skip = rid == "ER-003"
        v.rect(676, cy, 368, 53, fill=s["card"], rx=12,
               stroke=s["mark"] if skip else s["edge"],
               sw=1.2 if skip else 1.5,
               dash="5 4" if skip else None, shadow=True)
        pin(694, cy + 26, num)
        v.text(712, cy + 16, rid, 13, s["accent"] if not skip else s["sub"],
               mono=True, weight=700, max_w=80)
        v.chip(992, cy + 8, sev, s["mark"] if skip else s["accent"],
               s["band"], size=9.5, pad=7, height=17, weight=700,
               anchor="end")
        v.text(1032, cy + 16, scope, 11, s["faint"], anchor="end", max_w=90)
        v.text(712, cy + 31, found, 11.5, s["text"], max_w=316)
        v.text(712, cy + 45, loc, 11, s["accent"] if not skip else s["mark"],
               mono=True, max_w=316)

    # ---- report band: issues and skipped stay in separate cells --------------
    v.rect(44, 514, 1012, 70, fill=s["panel"], rx=18, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.line(384, 528, 384, 570, stroke=s["rule"], sw=1)
    v.line(700, 528, 700, 570, stroke=s["rule"], sw=1)

    v.text(64, 544, "issues[] 5", 13, s["accent"], mono=True, weight=700,
           max_w=170)
    v.text(64, 566, "summary { error 0 · warn 5 · info 0 }", 11, s["faint"],
           max_w=290)
    v.text(404, 544, "skipped[] 1", 13, s["mark"], mono=True, weight=700,
           max_w=170)
    v.text(404, 566, "ER-003 · nothing was summed", 11, s["faint"], max_w=280)
    v.text(720, 544, "buildView() → markdown + reportJson", 12.5, s["accent"],
           mono=True, weight=700, max_w=330)
    v.text(720, 566, "the verdict stays with the reviewer", 11, s["accent2"],
           max_w=300)

    # ---- footer -------------------------------------------------------------
    v.line(44, 600, 1056, 600, stroke=s["rule"], sw=1)
    v.text(44, 622,
           "Every card is an observation: what the sheet says, what the rule "
           "asks for, and where to look — no compliance verdict.",
           11.5, s["sub"], max_w=1010)
    v.text(44, 644,
           "config: rulesFile · disabledRules · onlyRules · skipNotes · "
           "timeoutMs ｜ read-only · no network · no model call",
           11.5, s["faint"], max_w=1010)

    if v.overflows:
        raise SystemExit("FATAL: SVG label overflow:\n  " + "\n  ".join(v.overflows))
    return v.svg(W, H,
                 "dsh-essay-rubric-check structure: a rubric sheet whose student "
                 "cell and two criterion rows carry five numbered pins, and whose "
                 "rule pack carries the sixth; each pin opens one finding card with "
                 "rule, severity, scope and a row + column locator; the report band "
                 "keeps issues and skipped apart and leaves the verdict to the "
                 "reviewer")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            hero(lang, skin)
        name = f"dsh-essay-rubric-check-flow-v5-{skin}.svg"
        with open(os.path.join(OUT, name), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(flow_svg(skin))
        print(f"wrote {name} (1100×660)")


if __name__ == "__main__":
    main()
