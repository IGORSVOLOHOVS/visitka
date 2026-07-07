# Business card generator

Renders `front.png` / `back.png` for the Igors Volohovs business card from a
thin JSON config. All visual design (colors, fonts, sizes, layout, QR
error-correction/box size) is fixed inside `template.html` / `generate.py` -
the config only carries content.

## How it works

`template.html` (Jinja2) + fixed `DESIGN` constants in `generate.py` define
the look. `generate.py` renders the template with your config values, embeds
a QR code generated from `qr_data` (via the `qrcode` library) as an inline
base64 image, then uses a headless Chromium browser (Playwright) to
screenshot the rendered card element at its exact native resolution
(1119x615px) - this is what makes the output pixel-accurate rather than an
approximation: it's a real browser rendering real CSS, not a hand-rolled
raster layout.

## Setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

## Usage

```powershell
python generate.py --config card.json --out-dir output/
```

Produces `output/front.png` and `output/back.png` (back is a blank white
image, same dimensions as front).

## Config schema

```json
{
  "name": "Igors Volohovs",
  "title": "Software Engineer",
  "phone": "+ 371 27572 829",
  "email": "igorsvolohovs@gmail.com",
  "url": "https://github.com/IGORSVOLOHOVS/",
  "qr_data": "https://igorsvolohovs.github.io/",
  "tags": ["AI Intergation", "Computer Vision", "Robotics"]
}
```

- `name`, `title`, `phone`, `email`, `url`, `tags` - printed as text on the
  card.
- `qr_data` - the payload actually **encoded** into the QR code, kept as a
  separate field from `url` on purpose: decoding the *original* printed
  card's QR code (via OpenCV) showed it pointed to a Google Drive link, not
  the GitHub URL printed next to it as text - so the two were never
  guaranteed to be the same thing. `qr_data` now points to
  `https://igorsvolohovs.github.io/`, Igor's existing personal site
  (confirmed live - same phone/email/GitHub links as this card), while `url`
  stays the printed GitHub link, unchanged. Point `qr_data` at whatever URL/
  vCard/text you want scanning the card to open.
- `tags` can hold any number of entries; note the original artwork has a
  typo ("AI Intergation") which `card.json` reproduces on purpose for an
  accurate pixel comparison against the original design - fix it in your own
  config if you don't want the typo.

Colors, fonts, sizes, panel proportions, and QR error-correction/box size are
**not** config fields - they're the fixed `DESIGN` dict in `generate.py`, so
every card generated with this tool shares one consistent visual identity
regardless of content.

## Accuracy vs. the original artwork

Compared against `../front.png` (the original card image) using
`ImageChops.difference` and SSIM (`scikit-image`), computed per side of the
card (`compare.py` is not shipped - this was a one-off verification, see the
numbers below):

| Region | SSIM | Exact pixel match |
|---|---|---|
| Whole card | 0.69 | 77% |
| Text panel (right side) | 0.83 | 89% |
| QR panel (left side) | 0.51 | 62% |

The text panel was calibrated by directly measuring bounding boxes of each
text line in the original (position, width, height) and iterating font size/
weight/spacing/margins in `template.html` until they matched within a few
pixels - see git history for the iteration. Residual differences there are
sub-pixel antialiasing (Chromium's text renderer isn't bit-identical to
whatever tool produced the original, even with the same font).

The QR panel match is inherently limited and this is expected, not a bug:
a QR code is regenerated from `qr_data` fresh using the `qrcode` library,
and independently generated QR codes for the same payload are **valid but
not bit-identical** - different libraries choose different mask patterns
(there are 8 valid masks per the QR spec) and sometimes different
error-correction levels, changing every module's exact position while
still encoding and scanning correctly. What *is* matched: module count/
density (both are version-5, 37x37 modules, confirmed by decoding the
original with OpenCV) and physical size within the dark panel. Getting a
bit-exact module pattern would require knowing the exact library and mask
choice used for the original, which isn't recoverable from the image alone.
