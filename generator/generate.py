#!/usr/bin/env python
"""Business card generator.

Renders front.png and back.png for the Igors Volohovs business card design
from a thin JSON config (content only - name/title/contacts/tags/QR payload).
All visual design decisions (colors, fonts, sizes, layout, QR error
correction/box size) are fixed constants below, not part of the config, so
every card produced by this tool shares one consistent look.

Usage:
    python generate.py --config card.json --out-dir output/
"""

from __future__ import annotations

import argparse
import base64
import json
from io import BytesIO
from pathlib import Path

import qrcode
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from playwright.sync_api import sync_playwright
from qrcode.constants import ERROR_CORRECT_M

HERE = Path(__file__).resolve().parent

# ---- Design constants: everything that is fixed by the card design itself,
# measured from the original artwork, and NOT duplicated per-config. ----
DESIGN = {
    "card_w": 1119,
    "card_h": 615,
    "dark_panel_frac": 0.4380,
    "dark_bg": "#171917",
    "light_bg": "#e8e6e8",
    "text_strong": "#232423",
    "text_muted": "#4a4a4a",
    "name_size": 61,
    "name_weight": 500,
    "title_size": 17,
    "title_weight": 700,
    "title_tracking": 0.42,
    "contact_size": 21,
    "contact_gap": 11,
    "tag_size": 19,
    "tag_weight": 700,
    "tag_gap": 30,
    "light_pad_x": 74,
    "light_pad_top": 94,
    "title_margin_top": 20,
    "contacts_margin_top": 79,
    "tags_margin_top": 100,
    "qr_display_frac": "72%",
}

# QR generation constants (fixed - not per-config)
QR_ERROR_CORRECTION = ERROR_CORRECT_M
QR_BOX_SIZE = 9
QR_BORDER = 4  # standard quiet zone, in modules


def make_qr_data_uri(data: str) -> str:
    qr = qrcode.QRCode(error_correction=QR_ERROR_CORRECTION, box_size=QR_BOX_SIZE, border=QR_BORDER)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def render_html(config: dict) -> str:
    env = Environment(loader=FileSystemLoader(str(HERE)))
    template = env.get_template("template.html")
    context = {
        **DESIGN,
        "name": config["name"],
        "title": config["title"],
        "phone": config["phone"],
        "email": config["email"],
        "url": config["url"],
        "tags": config.get("tags", []),
        "qr_data_uri": make_qr_data_uri(config["qr_data"]),
    }
    return template.render(**context)


def render_front_png(config: dict, out_path: Path) -> None:
    html = render_html(config)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": DESIGN["card_w"], "height": DESIGN["card_h"]})
        page.set_content(html, wait_until="networkidle")
        card = page.locator("#card")
        card.screenshot(path=str(out_path))
        browser.close()


def render_back_png(out_path: Path) -> None:
    Image.new("RGB", (DESIGN["card_w"], DESIGN["card_h"]), color=(255, 255, 255)).save(out_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate front.png/back.png for the business card")
    parser.add_argument("--config", required=True, help="Path to a thin JSON config (see card.json)")
    parser.add_argument("--out-dir", required=True, help="Directory to write front.png/back.png into")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    front_path = out_dir / "front.png"
    back_path = out_dir / "back.png"

    render_front_png(config, front_path)
    render_back_png(back_path)

    print(f"Wrote {front_path}")
    print(f"Wrote {back_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
