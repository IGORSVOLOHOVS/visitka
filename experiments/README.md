# Business card design experiments

10 visually distinct concepts for the same business card content (Igors
Volohovs, Software Engineer, AI Integration / Computer Vision / Robotics),
rendered with the same pipeline as `../generator` (Jinja2 + Playwright
screenshot at 1119x615). These are **explorations to choose from**, not a
replacement for the production card in `../generator` or the repo root
`front.png`/`back.png` - nothing there was touched.

Every QR code here actually encodes `https://igorsvolohovs.github.io/` and
was verified to decode correctly (OpenCV `QRCodeDetector`). A few early
color choices (green-on-dark, white-on-dark) looked thematically nice but
failed to decode reliably even at high contrast, so every variant uses a
plain black-on-white QR image, framed to fit its own theme - a scan failure
isn't a style worth risking on an actual business card.

**Print-size check.** A QR that decodes fine on a full-resolution digital
screenshot can still be too small to scan on an actual printed card held at
arm's length (~15-30cm) - phones need roughly 15-20mm of QR width and
~0.3-0.4mm per module at that distance, and a first pass at all 10 variants
had 9 of them sitting at 5.5-9.6mm (the QR was a small secondary detail in
most layouts, not sized for real-world scanning). All 9 were reworked -
not just a bigger CSS number, but a real layout pass per template so the
QR could grow into a proper focal element while keeping each concept
recognizable - and re-verified. Assuming the card prints at 90x50mm (the
size already used in this repo's `print.css`, 1119x615px -> 12.43px/mm):

| Variant | QR size (print) | Module size |
|---|---|---|
| 1 Minimal | 20.6mm | 0.56mm |
| 2 Geometric | 20.6mm | 0.56mm |
| 3 Terminal | 20.6mm | 0.56mm |
| 4 Neon gradient | 20.6mm | 0.56mm |
| 5 Big type | 20.6mm | 0.56mm |
| 6 QR centerpiece | 24.1mm | 0.65mm |
| 7 Accent color | 20.6mm | 0.56mm |
| 8 Corporate | 20.6mm | 0.56mm |
| 9 Robotics | 20.6mm | 0.56mm |
| 10 Blueprint | 20.6mm | 0.56mm |

All ten are now comfortably above the safe thresholds.

Run `python render_all.py` (from this directory, using `../generator/.venv`
or your own with `../generator/requirements.txt` installed) to regenerate
everything.

---

## 1. Minimal

![variant 1](variant_01_minimal/front.png)

Thin, airy, monochrome. Huge whitespace, a single hairline rule under the
name, small caps for the title, tags reduced to a quiet dotted list. No
color at all - the confidence is in the restraint. The QR moved from a
small corner afterthought to a full-height anchor on the right, which
suits the minimal layout well: one strong secondary shape instead of a
label-and-icon footer.

## 2. Geometric / asymmetric

![variant 2](variant_02_geometric/front.png)

A diagonal cut replaces the usual straight panel divider, with a thin amber
sliver between navy and cream. Bold, angled tag chips give it real motion
instead of a static two-column layout. The QR card now sits low in the
widest part of the cream triangle (it doubled in size and the diagonal
geometry meant the old mid-height position no longer had room for it).

## 3. Terminal

![variant 3](variant_03_terminal/front.png)

The whole card is a fake code editor window (title bar, traffic-light
dots, `~/contact.ts`), contact info rendered as a syntax-highlighted object
literal with line numbers and a blinking cursor. The most literal
"software engineer" concept of the ten, and probably the most memorable.
The QR panel on the right grew to a real "preview pane" size; the code
font shrank slightly to keep every line on one row next to it.

## 4. Neon gradient

![variant 4](variant_04_neon_gradient/front.png)

Dark background, a magenta-to-cyan gradient mesh, a subtle grid, and a
glowing name with neon text-shadow. Pill-shaped tags with soft outer glow
and a frosted-glass QR panel, now sized to actually be scannable off a
printed card rather than just decorative. AI-startup energy without going
full cyberpunk kitsch.

## 5. Big type

![variant 5](variant_05_big_type/front.png)

The name *is* the card - two lines of black display type bleeding off the
left edge, a small stamped title badge underneath. Reworked the bottom
strip to give the QR a real square block instead of a token corner icon:
name size came down a little (168px -> 122px) to free the vertical room,
which if anything reads cleaner. Maximum confidence, minimum decoration.

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
"designed" of the neutral-background variants. The framed QR in the
bottom-right corner more than doubled in size and still clears the accent
circle with room to spare.

## 8. Corporate

![variant 8](variant_08_corporate/front.png)

Formal: a monogram roundel, serif name, a thin gold rule, letter-spaced
title. Included deliberately as the conservative counterpoint to the
bolder variants - the one to hand to a board member. Originally a fully
centered, symmetric layout with a small QR tucked into a horizontal
footer; a QR that size couldn't grow to a safe scanning size without
either overflowing the card or squeezing the text block too tight, so it's
now a two-column layout (content left, QR right, thin rule between) - a
common formal-letterhead pattern rather than a compromise.

## 9. Robotics / CV

![variant 9](variant_09_robotics/front.png)

Dark background with a faint circuit-trace pattern and PCB-style node
dots, monospace `> ` prompts for contact lines, and the three tags as
small badges with hand-drawn AI-chip / camera-lens / robot-arm icons. QR
sits inside a viewfinder-bracket frame, like a targeting reticle - scaled
up along with the QR itself so the brackets still read as a frame rather
than a decoration dwarfed by the code inside it.

## 10. Blueprint

![variant 10](variant_10_blueprint/front.png)

An engineering technical-drawing pastiche: graph-paper grid, a dimension
line under the name, and the contact/tag info laid out as a real drafting
title block (CONTACT / REPOSITORY / DOMAIN 01-02 / DOMAIN 03 columns). The
QR - grown to a proper component size - is labeled like a schematic part
("QR-01"). Ties into Robotics/CV without a single sci-fi cliche.

Along the way, growing this QR surfaced a real rendering bug worth noting:
the background grid pattern was painting *on top of* the QR image (both
were `position: absolute` with no explicit stacking order), which silently
corrupted part of the printed code. Fixed by giving the QR component an
explicit `z-index` - a good reminder that a QR that looks fine at a glance
can still have broken modules hiding on close inspection.
