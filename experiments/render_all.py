#!/usr/bin/env python
"""Renders all 10 business card design experiments.

Front: name/title/contacts/tags/photo + a short "portfolio on the back" CTA
(no printed URL - that would be redundant with the QR).
Back: QR code (encoding https://igorsvolohovs.github.io/) + "github.com"
caption, centered, styled per-variant via templates/template_back_shared.html.
"""

from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

import qrcode
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright
from qrcode.constants import ERROR_CORRECT_M

HERE = Path(__file__).resolve().parent
CARD_W, CARD_H = 1119, 615

DATA = {
    "name": "Igors Volohovs",
    "title": "Software Engineer",
    "phone": "+371 27572 829",
    "email": "igorsvolohovs@gmail.com",
    "tags": ["AI Integration", "Computer Vision", "Robotics"],
}
QR_TARGET = "https://igorsvolohovs.github.io/"


def file_to_data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def make_qr_data_uri(data: str, fill: str = "#000000", back: str = "#ffffff", box_size: int = 9) -> str:
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=box_size, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=back).convert("RGB")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


# Each front template gets: DATA + photo_uri + cta (the on-brand "portfolio is
# on the back" line replacing the old printed URL).
FRONT_VARIANTS = {
    "variant_01_minimal": ("template_01_minimal.html", "PORTFOLIO ON THE BACK"),
    "variant_02_geometric": ("template_02_geometric.html", "PORTFOLIO ON THE BACK →"),
    "variant_03_terminal": ("template_03_terminal.html", "portfolio -> flip card"),
    "variant_04_neon_gradient": ("template_04_neon_gradient.html", "PORTFOLIO ↓ FLIP CARD"),
    "variant_05_big_type": ("template_05_big_type.html", "PORTFOLIO ON REVERSE"),
    "variant_06_qr_centerpiece": ("template_06_qr_centerpiece.html", "Flip for portfolio"),
    "variant_07_accent_color": ("template_07_accent_color.html", "PORTFOLIO ON REVERSE"),
    "variant_08_corporate": ("template_08_corporate.html", "Portfolio — see reverse"),
    "variant_09_robotics": ("template_09_robotics.html", "see_reverse --portfolio"),
    "variant_10_blueprint": ("template_10_blueprint.html", "SEE SHEET 2 / PORTFOLIO"),
}

# Back side: shared template, themed per variant to match its front.
GOOGLE_FONTS = {
    "manrope": "https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;500;700&display=swap",
    "sora": "https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&display=swap",
    "jetbrains": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap",
    "archivo": "https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@500;700&display=swap",
    "space_grotesk": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap",
    "plex_serif": "https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@600&display=swap",
    "plex_mono": "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap",
}

BACK_STYLES = {
    "variant_01_minimal": dict(
        bg="#161616", font_family="'Manrope', sans-serif", font_href=GOOGLE_FONTS["manrope"],
        caption_weight="300", caption_tracking="6px", caption_transform="lowercase",
    ),
    "variant_02_geometric": dict(
        bg="#0d1b2a", font_family="'Sora', sans-serif", font_href=GOOGLE_FONTS["sora"],
        caption_weight="700", caption_tracking="2px",
        frame_extra="box-shadow: 0 0 0 3px #ffb703;",
    ),
    "variant_03_terminal": dict(
        bg="#282c34", font_family="'JetBrains Mono', monospace", font_href=GOOGLE_FONTS["jetbrains"],
        caption_weight="500", caption_tracking="0px",
        extra_html='<div style="position:absolute;top:40px;left:50px;color:#5c6370;font-size:22px;">~/contact.ts</div>',
        frame_extra="border: 2px solid #3a3f4b;",
    ),
    "variant_04_neon_gradient": dict(
        bg=(
            "radial-gradient(circle at 12% 15%, rgba(255,0,200,0.35), transparent 42%),"
            "radial-gradient(circle at 85% 20%, rgba(0,229,255,0.30), transparent 45%),"
            "radial-gradient(circle at 70% 90%, rgba(130,0,255,0.35), transparent 50%), #120019"
        ),
        font_family="'Sora', sans-serif", font_href=GOOGLE_FONTS["sora"],
        caption_weight="700", caption_tracking="3px",
        frame_extra="box-shadow: 0 0 40px rgba(255,46,196,0.45), 0 0 70px rgba(76,233,255,0.3);",
    ),
    "variant_05_big_type": dict(
        bg="#000000", font_family="'Archivo', sans-serif", font_href=GOOGLE_FONTS["archivo"],
        caption_weight="700", caption_tracking="1px",
    ),
    "variant_06_qr_centerpiece": dict(
        bg="#1c1c1c", font_family="'Space Grotesk', sans-serif", font_href=GOOGLE_FONTS["space_grotesk"],
        caption_weight="500", caption_tracking="1px",
    ),
    "variant_07_accent_color": dict(
        bg="#141414", font_family="'Space Grotesk', sans-serif", font_href=GOOGLE_FONTS["space_grotesk"],
        caption_weight="700", caption_tracking="1px",
        frame_extra="border: 3px solid #ff4d1c;",
    ),
    "variant_08_corporate": dict(
        bg="#0b2545", font_family="'IBM Plex Serif', serif", font_href=GOOGLE_FONTS["plex_serif"],
        caption_weight="600", caption_tracking="3px",
        extra_html='<div style="position:relative;z-index:2;width:80px;height:1px;background:#c9a24b;margin-bottom:6px;"></div>',
    ),
    "variant_09_robotics": dict(
        bg="#081018", font_family="'Sora', sans-serif", font_href=GOOGLE_FONTS["sora"],
        caption_weight="600", caption_tracking="1px",
        extra_css=(
            ".circuit{position:absolute;inset:0;opacity:.35;"
            "background-image:linear-gradient(#1a2c36 1px,transparent 1px),"
            "linear-gradient(90deg,#1a2c36 1px,transparent 1px);background-size:46px 46px;}"
        ),
        extra_html='<div class="circuit"></div>',
        frame_extra="border: 2px solid #39ffc7;",
    ),
    "variant_10_blueprint": dict(
        bg="#0e2a47", font_family="'IBM Plex Mono', monospace", font_href=GOOGLE_FONTS["plex_mono"],
        caption_weight="500", caption_tracking="2px",
        extra_css=(
            ".gridbg{position:absolute;inset:0;"
            "background-image:linear-gradient(rgba(234,242,251,0.08) 1px,transparent 1px),"
            "linear-gradient(90deg,rgba(234,242,251,0.08) 1px,transparent 1px);background-size:28px 28px;}"
        ),
        extra_html='<div class="gridbg"></div>',
        frame_extra="border: 1.5px solid #7fa4c9;",
    ),
}


def main() -> None:
    env = Environment(loader=FileSystemLoader(str(HERE / "templates")))
    photo_uri = file_to_data_uri(HERE / "assets" / "photo.png", "image/png")
    qr_uri = make_qr_data_uri(QR_TARGET, "#000000", "#ffffff")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": CARD_W, "height": CARD_H})

        for slug, (tpl_name, cta) in FRONT_VARIANTS.items():
            template = env.get_template(tpl_name)
            html = template.render(**DATA, photo_uri=photo_uri, cta=cta)
            out_dir = HERE / slug
            out_dir.mkdir(parents=True, exist_ok=True)
            page.set_content(html, wait_until="networkidle")
            page.locator("#card").screenshot(path=str(out_dir / "front.png"))
            print(f"Rendered {slug}/front.png")

        back_template = env.get_template("template_back_shared.html")
        for slug, style in BACK_STYLES.items():
            context = dict(qr_uri=qr_uri, caption="github.com")
            context.update(style)
            html = back_template.render(**context)
            out_dir = HERE / slug
            page.set_content(html, wait_until="networkidle")
            page.locator("#card").screenshot(path=str(out_dir / "back.png"))
            print(f"Rendered {slug}/back.png")

        browser.close()


if __name__ == "__main__":
    main()
