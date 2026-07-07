# Business card design experiments

10 visually distinct concepts for the same business card content (Igors
Volohovs, Software Engineer, AI Integration / Computer Vision / Robotics),
rendered with the same pipeline as `../generator` (Jinja2 + Playwright
screenshot at 1119x615). These are **explorations to choose from**, not a
replacement for the production card in `../generator` or the repo root
`front.png`/`back.png` - nothing there was touched.

Every QR code here actually encodes `https://igorsvolohovs.github.io/` and
was verified to decode correctly (OpenCV `QRCodeDetector`, script not
shipped - see git history). A few early color choices (green-on-dark,
white-on-dark) looked thematically nice but failed to decode reliably even
at high contrast, so every variant uses a plain black-on-white QR image,
framed to fit its own theme - a scan failure isn't a style worth risking on
an actual business card.

Run `python render_all.py` (from this directory, using `../generator/.venv`
or your own with `../generator/requirements.txt` installed) to regenerate
everything.

---

## 1. Minimal

![variant 1](variant_01_minimal/front.png)

Thin, airy, monochrome. Huge whitespace, a single hairline rule under the
name, small caps for the title, tags reduced to a quiet dotted list. No
color at all - the confidence is in the restraint.

## 2. Geometric / asymmetric

![variant 2](variant_02_geometric/front.png)

A diagonal cut replaces the usual straight panel divider, with a thin amber
sliver between navy and cream. Bold, angled tag chips and a QR card floating
mid-diagonal give it real motion instead of a static two-column layout.

## 3. Terminal

![variant 3](variant_03_terminal/front.png)

The whole card is a fake code editor window (title bar, traffic-light
dots, `~/contact.ts`), contact info rendered as a syntax-highlighted object
literal with line numbers and a blinking cursor. The most literal
"software engineer" concept of the ten, and probably the most memorable.

## 4. Neon gradient

![variant 4](variant_04_neon_gradient/front.png)

Dark background, a magenta-to-cyan gradient mesh, a subtle grid, and a
glowing name with neon text-shadow. Pill-shaped tags with soft outer glow
and a frosted-glass QR panel. AI-startup energy without going full cyberpunk
kitsch.

## 5. Big type

![variant 5](variant_05_big_type/front.png)

The name *is* the card - two lines of black display type bleeding off the
left edge at 130px, everything else (title, contacts, tags, QR) compressed
into a thin strip at the bottom. Maximum confidence, minimum decoration.

## 6. QR centerpiece

![variant 6](variant_06_qr_centerpiece/front.png)

No side panel at all - one continuous cream background, and the QR code
itself is the visual anchor of the composition (blend-mode multiply so it
sits flush with the background, a dashed orbit ring, and a "scan me" badge),
with the text arranged beside it rather than boxed away in its own zone.

## 7. Accent color

![variant 7](variant_07_accent_color/front.png)

White canvas, one bold accent color (orange) used sparingly: a corner
circle, the title badge, the tag labels. Swiss/Bauhaus-influenced,
everything else stays black text on white. The most contrast-y and
"designed" of the neutral-background variants.

## 8. Corporate

![variant 8](variant_08_corporate/front.png)

Centered, symmetric, formal: a monogram roundel, serif name, a thin gold
rule, letter-spaced title. Included deliberately as the conservative
counterpoint to the bolder variants - the one to hand to a board member.

## 9. Robotics / CV

![variant 9](variant_09_robotics/front.png)

Dark background with a faint circuit-trace pattern and PCB-style node
dots, monospace `> ` prompts for contact lines, and the three tags as
small badges with hand-drawn AI-chip / camera-lens / robot-arm icons. QR
sits inside a viewfinder-bracket frame, like a targeting reticle.

## 10. Blueprint

![variant 10](variant_10_blueprint/front.png)

An engineering technical-drawing pastiche: graph-paper grid, a dimension
line under the name, and the contact/tag info laid out as a real drafting
title block (CONTACT / REPOSITORY / DOMAIN 01-02 / DOMAIN 03 columns). The
QR is labeled like a schematic component ("QR-01"). Ties into
Robotics/CV without a single sci-fi cliche.
