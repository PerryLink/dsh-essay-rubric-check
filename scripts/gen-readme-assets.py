#!/usr/bin/env python3
"""Generate README image assets for dsh-essay-rubric-check (docs/assets/).

Outputs (idempotent overwrite):
  dsh-essay-rubric-check-flow-light.svg
  dsh-essay-rubric-check-flow-dark.svg
      Hero workflow diagram. Two hand-written SVG files (vector - never
      rasterized to webp). Text inside is command-surface tokens only
      (essay_rubric_check, parseMaterial, runCheck, buildView, ...), so all
      five README languages share the same pair. The plugin has no UI and
      ships no benchmark data, so there is no screenshot and no evidence
      chart: the flow diagram is the whole image set.

The old single-theme docs/assets/dsh-essay-rubric-check-flow.svg and the
quickstart screenshots are deliberately left in place (external links must
not 404); the READMEs reference only the new light/dark pair.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow (the CJK probe below is shared with the family template;
           this particular diagram has no CJK text, but the probe stays so a
           future localized variant cannot silently render tofu boxes).
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont  # noqa: F401  (family template parity)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

# --- palette: PerryLink family (accent) + GitHub page backgrounds ----------
FAMILY = "#4B67B4"   # family accent (badges labelColor family uses #2B3245)
GREEN = {"light": "#16a34a", "dark": "#3fb950"}
SKIN = {
    "light": dict(bg="#ffffff", box="#f6f8fa", border="#d0d7de",
                  text="#1f2328", sub="#57606a", track="#eaeef2"),
    "dark": dict(bg="#0d1117", box="#161b22", border="#30363d",
                 text="#f0f6fc", sub="#8b949e", track="#21262d"),
}

# --- CJK font probe: Chinese must never render as tofu boxes ----------------
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",      # Microsoft YaHei
    r"C:\Windows\Fonts\simhei.ttf",    # SimHei
    r"C:\Windows\Fonts\Deng.ttf",      # DengXian
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
]
FONT_PATH = next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)
if FONT_PATH is None:
    sys.exit("FATAL: no CJK font found (looked for msyh.ttc, simhei.ttf, "
             "Deng.ttf, Noto Sans CJK, PingFang). Refusing to render Chinese "
             "as tofu boxes; install one of the probed fonts and re-run.")


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


# ---------------------------------------------------------------------------
# Hero workflow SVG (light + dark)
# ---------------------------------------------------------------------------
FLOW_NODES = [
    ("file / material", "JSON / YAML"),
    ("parseMaterial", "header + rows"),
    ("runCheck", "ER-001…ER-006"),
    ("issues[]", "found · expected · fix"),
    ("buildView", "markdown + reportJson"),
]


def arrow(x1: int, y: int, x2: int, color: str) -> list[str]:
    return [
        f'<path d="M{x1} {y}h{x2 - x1 - 10}" stroke="{color}" '
        f'stroke-width="3" stroke-linecap="round"/>',
        f'<path d="M{x2 - 14} {y - 7}l10 7-10 7" fill="none" '
        f'stroke="{color}" stroke-width="3" stroke-linecap="round" '
        f'stroke-linejoin="round"/>',
    ]


def flow_svg(skin: str) -> str:
    s = SKIN[skin]
    w, h = 1280, 440
    x0, nw, nh, gap, y0 = 56, 208, 110, 30, 150
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="dsh-essay-rubric-check workflow: file or material to '
        f'parseMaterial to runCheck to issues to buildView">',
        '<title>dsh-essay-rubric-check workflow</title>',
        f'<rect width="{w}" height="{h}" rx="18" fill="{s["bg"]}"/>',
        f'<text x="56" y="58" fill="{s["text"]}" font-family="ui-sans-serif,'
        f'system-ui,sans-serif" font-size="30" font-weight="700">'
        f'dsh-essay-rubric-check</text>',
        f'<text x="56" y="92" fill="{s["sub"]}" font-family="ui-monospace,'
        f'monospace" font-size="15">essay_rubric_check · '
        f'rules/essay-rubric-check.yaml · ER-001…ER-006</text>',
        f'<line x1="56" y1="116" x2="1224" y2="116" stroke="{s["border"]}"/>',
    ]

    for i, (label, sub) in enumerate(FLOW_NODES):
        x = x0 + i * (nw + gap)
        if i == len(FLOW_NODES) - 1:
            accent = GREEN[skin]
        elif i == 2:
            accent = FAMILY
        else:
            accent = s["border"]
        parts.append(
            f'<rect x="{x}" y="{y0}" width="{nw}" height="{nh}" rx="14" '
            f'fill="{s["box"]}" stroke="{accent}" stroke-width="2"/>')
        parts.append(
            f'<text x="{x + nw // 2}" y="{y0 + 46}" fill="{s["text"]}" '
            f'text-anchor="middle" font-family="ui-monospace,monospace" '
            f'font-size="17" font-weight="700">{label}</text>')
        parts.append(
            f'<text x="{x + nw // 2}" y="{y0 + 76}" fill="{s["sub"]}" '
            f'text-anchor="middle" font-family="ui-monospace,monospace" '
            f'font-size="12.5">{sub}</text>')
        if i < len(FLOW_NODES) - 1:
            parts.extend(arrow(x + nw + 4, y0 + nh // 2, x + nw + gap - 4,
                               s["sub"]))

    # rule-pack rail: the pack feeds runCheck (node 3) and is validated on load.
    cx3 = x0 + 2 * (nw + gap) + nw // 2
    parts.append(
        f'<path d="M{cx3} {y0 + nh}v38" stroke="{FAMILY}" stroke-width="2" '
        f'stroke-dasharray="5 5"/>')
    bw, bh, bx, by = 560, 76, cx3 - 280, 298
    parts.append(
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" '
        f'fill="{s["box"]}" stroke="{FAMILY}" stroke-width="2" '
        f'stroke-dasharray="5 5"/>')
    parts.append(
        f'<text x="{bx + bw // 2}" y="{by + 32}" fill="{s["text"]}" '
        f'text-anchor="middle" font-family="ui-monospace,monospace" '
        f'font-size="14" font-weight="700">'
        f'rules/essay-rubric-check.yaml</text>')
    parts.append(
        f'<text x="{bx + bw // 2}" y="{by + 56}" fill="{s["sub"]}" '
        f'text-anchor="middle" font-family="ui-monospace,monospace" '
        f'font-size="12.5">loadRulesetFile · excerpt ≥ 8 · kind → severity'
        f'</text>')
    parts.append(
        f'<text x="56" y="416" fill="{s["sub"]}" font-family="ui-monospace,'
        f'monospace" font-size="13">skipped[] · '
        f'summary {{ error, warn, info }} · issueCount · reportJson</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for skin in ("light", "dark"):
        path = os.path.join(OUT, f"dsh-essay-rubric-check-flow-{skin}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin))
    print("wrote 2 SVG assets to docs/assets/ "
          "(dsh-essay-rubric-check-flow-{light,dark}.svg)")


if __name__ == "__main__":
    main()
