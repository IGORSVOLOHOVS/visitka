#!/usr/bin/env python
"""Renders all 10 business card design experiments to experiments/variant_NN_*/front.png.

Each variant is an independent, self-contained HTML/CSS design (templates/template_NN_*.html)
sharing the same content and rendering pipeline (Jinja2 -> Playwright screenshot) as the
production generator in ../generator, but exploring a different visual language per variant.
"""

from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

import qrcode
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from playwright.sync_api import sync_playwright
from qrcode.constants import ERROR_CORRECT_M

HERE = Path(__file__).resolve().parent
CARD_W, CARD_H = 1119, 615

DATA = {
    "name": "Igors Volohovs",
    "title": "Software Engineer",
    "phone": "+371 27572 829",
    "email": "igorsvolohovs@gmail.com",
    "url": "github.com/IGORSVOLOHOVS",
    "qr_target": "https://igorsvolohovs.github.io/",
    "tags": ["AI Integration", "Computer Vision", "Robotics"],
}


def make_qr_data_uri(data: str, fill: str = "#000000", back: str = "#ffffff", box_size: int = 9) -> str:
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=box_size, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=back).convert("RGB")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


# (slug, template filename, qr fill, qr back)
# Fill/back are kept at or near true black-on-white for every variant: a
# handful of themed color choices here (light-on-dark, tinted greens) were
# tried and failed to decode reliably (verified with OpenCV's QRCodeDetector)
# even at high contrast ratios and reasonable size - real phone scanners are
# more forgiving than that, but a business card QR that *sometimes* fails to
# scan is a real usability bug, not a style risk worth taking. Each template
# still frames the QR in a way that fits its own theme (dark IDE window,
# glowing panel, blueprint component box, etc).
VARIANTS = [
    ("variant_01_minimal", "template_01_minimal.html", "#161616", "#ffffff"),
    ("variant_02_geometric", "template_02_geometric.html", "#0d1b2a", "#ffffff"),
    ("variant_03_terminal", "template_03_terminal.html", "#000000", "#ffffff"),
    ("variant_04_neon_gradient", "template_04_neon_gradient.html", "#000000", "#ffffff"),
    ("variant_05_big_type", "template_05_big_type.html", "#000000", "#ffffff"),
    ("variant_06_qr_centerpiece", "template_06_qr_centerpiece.html", "#1c1c1c", "#f4f1ea"),
    ("variant_07_accent_color", "template_07_accent_color.html", "#141414", "#ffffff"),
    ("variant_08_corporate", "template_08_corporate.html", "#0b2545", "#ffffff"),
    ("variant_09_robotics", "template_09_robotics.html", "#000000", "#ffffff"),
    ("variant_10_blueprint", "template_10_blueprint.html", "#000000", "#ffffff"),
]


def main() -> None:
    env = Environment(loader=FileSystemLoader(str(HERE / "templates")))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": CARD_W, "height": CARD_H})
        for slug, tpl_name, qr_fill, qr_back in VARIANTS:
            template = env.get_template(tpl_name)
            qr_uri = make_qr_data_uri(DATA["qr_target"], qr_fill, qr_back)
            html = template.render(**DATA, qr_uri=qr_uri)

            out_dir = HERE / slug
            out_dir.mkdir(parents=True, exist_ok=True)

            page.set_content(html, wait_until="networkidle")
            page.locator("#card").screenshot(path=str(out_dir / "front.png"))
            Image.new("RGB", (CARD_W, CARD_H), color=(255, 255, 255)).save(out_dir / "back.png")
            print(f"Rendered {slug}")
        browser.close()


if __name__ == "__main__":
    main()
