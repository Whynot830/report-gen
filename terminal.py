"""Скриншоты терминала в стиле Ghostty для вставки в отчёты.

    python3 -m reportgen.terminal --title /Users/whynot -o shot.png <<'EOF'
    whynot@MBP14 ~ % ls
    EOF
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Палитра по скриншоту Ghostty: окно #121212, светофор macOS, жёлтый курсор.
BG = (18, 18, 18, 255)
FG = (214, 214, 212, 255)
DIM = (122, 122, 120, 255)
TITLE = (154, 154, 152, 255)
COMMENT = (108, 108, 106, 255)
USER = (166, 218, 149, 255)
PATH_C = (137, 180, 250, 255)
ERROR = (238, 105, 123, 255)
CURSOR = (232, 196, 104, 255)
LIGHTS = ((255, 95, 87), (254, 188, 46), (40, 200, 64))

FONT_CANDIDATES = (
    ("/System/Library/Fonts/SFNSMono.ttf", 0),
    ("/Library/Fonts/SFNSMono.ttf", 0),
    ("/System/Library/Fonts/Menlo.ttc", 0),
    ("/System/Library/Fonts/Supplemental/Courier New.ttf", 0),
)

FONT_SIZE = 26
TITLE_SIZE = 17
LINE = 34
PAD_X = 28
TITLE_H = 48
PAD_BOTTOM = 28
RADIUS = 20
LIGHT_Y = 16
LIGHT_D = 14

ZSH_RE = re.compile(
    r"^(?P<user>[^\s@]+)@(?P<host>\S+)\s+(?P<path>\S+)\s+(?P<mark>%|#)\s?(?P<cmd>.*)$"
)
PSQL_RE = re.compile(r"^(?P<db>[^\s=*]+)(?P<star>\*)?=#\s?(?P<cmd>.*)$")
PSQL_CONT_RE = re.compile(r"^(?P<db>[^\s-]+)-#\s?(?P<cmd>.*)$")
MONGO_RE = re.compile(r"^(?P<db>\S+)>\s?(?P<cmd>.*)$")
DOLLAR_RE = re.compile(r"^(?P<path>\S+\$)\s?(?P<cmd>.*)$")


def _font(size: int) -> ImageFont.FreeTypeFont:
    for path, index in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size, index=index)
        except OSError:
            continue
    return ImageFont.load_default()


def _text_width(font: ImageFont.ImageFont, text: str) -> int:
    bbox = font.getbbox(text if text else " ")
    return bbox[2] - bbox[0]


def _draw_segments(draw: ImageDraw.ImageDraw, x: int, y: int, font, parts: list[tuple[str, tuple]]) -> None:
    for text, color in parts:
        if not text:
            continue
        draw.text((x, y), text, font=font, fill=color)
        x += _text_width(font, text)


def _line_parts(line: str) -> list[tuple[str, tuple]]:
    stripped = line.lstrip()
    if (
        stripped.startswith("ERROR")
        or "SQLSTATE" in line
        or "NOT_FOUND" in line
        or "NOT_ALLOWED" in line
        or "UnroutableError" in line
        or "ProbableAccessDeniedError" in line
    ):
        return [(line, ERROR)]
    if stripped.startswith("--") or stripped.startswith("Сессия") or stripped.startswith("# "):
        return [(line, COMMENT)]
    if stripped.startswith("Last login:") or stripped.startswith("zsh:"):
        return [(line, DIM)]

    m = ZSH_RE.match(line)
    if m:
        return [
            (m["user"], USER),
            ("@", DIM),
            (m["host"], USER),
            (" ", FG),
            (m["path"], PATH_C),
            (" ", FG),
            (m["mark"], FG),
            ((" " + m["cmd"]) if m["cmd"] else "", FG),
        ]
    m = PSQL_RE.match(line)
    if m:
        prompt = m["db"] + ("*" if m["star"] else "") + "=#"
        return [(prompt, PATH_C), ((" " + m["cmd"]) if m["cmd"] else "", FG)]
    m = PSQL_CONT_RE.match(line)
    if m:
        return [(m["db"] + "-#", DIM), ((" " + m["cmd"]) if m["cmd"] else "", FG)]
    m = MONGO_RE.match(line)
    if m:
        return [(m["db"] + ">", PATH_C), ((" " + m["cmd"]) if m["cmd"] else "", FG)]
    m = DOLLAR_RE.match(line)
    if m:
        return [(m["path"], PATH_C), ((" " + m["cmd"]) if m["cmd"] else "", FG)]
    return [(line if line else " ", FG)]


def render_terminal(
    text: str,
    *,
    title: str = "/Users/whynot",
    cursor: bool = False,
    min_width: int = 980,
) -> Image.Image:
    """Вернуть RGBA-изображение окна Ghostty с текстом сессии."""
    font = _font(FONT_SIZE)
    title_font = _font(TITLE_SIZE)
    lines = text.replace("\t", "    ").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if not lines:
        lines = [""]

    text_w = max(_text_width(font, line) for line in lines)
    title_w = _text_width(title_font, title)
    width = max(min_width, text_w + PAD_X * 2, title_w + 120)
    height = TITLE_H + 16 + len(lines) * LINE + PAD_BOTTOM

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=RADIUS, fill=BG)

    for i, color in enumerate(LIGHTS):
        x = 18 + i * 22
        draw.ellipse((x, LIGHT_Y, x + LIGHT_D, LIGHT_Y + LIGHT_D), fill=color)

    draw.text((88, 14), title, font=title_font, fill=TITLE)

    y = TITLE_H + 12
    for line in lines:
        _draw_segments(draw, PAD_X, y, font, _line_parts(line))
        y += LINE

    if cursor:
        cx = PAD_X + _text_width(font, lines[-1] + " ")
        cy = TITLE_H + 12 + (len(lines) - 1) * LINE + 4
        cw = max(14, _text_width(font, " ") - 2)
        draw.rectangle((cx, cy, cx + cw, cy + LINE - 10), fill=CURSOR)

    return img


def save_terminal(
    text: str,
    path: str | Path,
    *,
    title: str = "/Users/whynot",
    cursor: bool = False,
    min_width: int = 980,
) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img = render_terminal(text, title=title, cursor=cursor, min_width=min_width)
    img.save(path, "PNG")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Скриншот терминала в стиле Ghostty")
    parser.add_argument("-o", "--output", required=True, help="Путь к PNG")
    parser.add_argument("--title", default="/Users/whynot", help="Заголовок окна")
    parser.add_argument("--cursor", action="store_true", help="Жёлтый курсор в конце")
    parser.add_argument("--min-width", type=int, default=980)
    parser.add_argument("text", nargs="?", help="Текст; иначе stdin")
    args = parser.parse_args(argv)
    text = args.text if args.text is not None else sys.stdin.read()
    out = save_terminal(
        text,
        args.output,
        title=args.title,
        cursor=args.cursor,
        min_width=args.min_width,
    )
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
