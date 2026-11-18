# visitka - software requirements specification

Reverse-engineered from commit `0e235cf` on 2026-11-18. It describes what the
files do, not what they should do. Hub: [docs/README.md](docs/README.md).

## 1. Purpose and scope

The repository produces and stores one person's business card and related
contact material (`README.md:3-5`).

In scope:

- `generator/`: a CLI that renders the card front and back as PNG from a JSON
  content config.
- `experiments/`: a script and templates that render eleven alternative
  designs, and two vCard files in `experiments/vcf/`.
- `print.html`, `print_many.html`, `print.css`: browser pages for printing
  cards at 90 x 50 mm.
- `cv.html` and the committed PDFs and images, as content.
- `recipe.ps1` as the repository's command interface (FR-20 only).

Out of scope: the hooks, workflows and rules of the lab tooling (described by
repo-quality-template); the personal site that the QR codes point to (another
repository); the tools used to produce `CV_Igors_Volohovs_OnePage.pdf`, the
QR images at the root and the original artwork (not in this repository).

## 2. Context

| Actor or system | Role | Source |
| --- | --- | --- |
| Card owner / maintainer | Edits `card.json` and templates, runs the scripts, prints cards | `generator/README.md`, `experiments/README.md` |
| Person receiving the card | Scans the QR code or imports a vCard | `experiments/vcf/README.md:7-10` |
| Playwright + headless Chromium | Renders HTML and takes the screenshot | `generate.py:93-99`, `render_all.py:152-184` |
| Google Fonts CDN | Supplies Poppins, the variant fonts, and Inter for the print pages and the CV | `template.html:5-6`, `render_all.py:68-76`, `print.html:9`, `print_many.html:9`, `cv.html:10` |
| cdnjs, Tailwind CDN | Font Awesome and Tailwind for the print pages and the CV | `print.html:6`, `cv.html:6,8` |
| Personal site | Target of the QR codes (`QR_TARGET`, `qr_data`) | `render_all.py:33`, `generator/card.json:7` |
| Web browser | Displays and prints the print pages and the CV | `print.html:15-17` |

Runtime: Python with the packages in `generator/requirements.txt`; the
documented setup is Windows PowerShell with `py -3.12` (`generator/README.md:21-26`).
`recipe.ps1` is a PowerShell script; CI runs on a runner labelled `windows`
(`.gitea/workflows/test.yaml:16`).

## 3. Functional requirements

### 3.1 Card generator (`generator/generate.py`)

**FR-1.** The system shall require the command-line options `--config` and `--out-dir`.
Source: `generator/generate.py:107-110`. Verification: no test.

**FR-2.** The system shall read the config as UTF-8 JSON, require the keys `name`, `title`, `phone`, `email`, `url`, `qr_data`, and treat `tags` as optional with an empty list as default.
Source: `generator/generate.py:80-86,112`. Verification: no test.

**FR-3.** The system shall encode `qr_data` as a QR code with error correction level M, box size 9, a 4-module border and automatic version selection, black on white, and embed it as a base64 PNG data URI.
Source: `generator/generate.py:59-72`. Verification: no test.

**FR-4.** The system shall render `generator/template.html` with Jinja2, passing every `DESIGN` constant and the config values; colours, fonts, sizes and proportions shall not be taken from the config.
Source: `generator/generate.py:32-56,75-88`, `generator/README.md:71-74`. Verification: no test.

**FR-5.** The system shall lay out the front as a dark panel of 43.80 % of the card width holding the QR image at 72 % of the panel width, and a light panel with the name, the title, three contact lines in the order phone, email, url, and a wrapping row of tags.
Source: `generator/generate.py:35,55`, `generator/template.html:29-109`. Verification: no test.

**FR-6.** The system shall render the HTML in headless Chromium at a 1119 x 615 viewport, wait for network idle, and save a screenshot of the element `#card` as `<out-dir>/front.png`.
Source: `generator/generate.py:91-99,116`, `generator/template.html:94`. Verification: no test.

**FR-7.** The system shall write `<out-dir>/back.png` as a white 1119 x 615 RGB image.
Source: `generator/generate.py:102-103,117`. Verification: no test.

**FR-8.** The system shall create the output directory with its parents if missing, print the path of each written file, and exit with code 0.
Source: `generator/generate.py:113-114,122-124,128`. Verification: no test.

### 3.2 Design experiments (`experiments/render_all.py`)

**FR-9.** The system shall render a front image for each of the 11 entries of `FRONT_VARIANTS` from its template, with the hard-coded `DATA`, the photo `experiments/assets/photo.png` as a data URI and the variant's call-to-action string, into `experiments/<variant>/front.png`.
Source: `experiments/render_all.py:26-32,53-65,147-163`. Verification: no test.

**FR-10.** The system shall render the backs of variants 1-10 from `template_back_shared.html` with the per-variant `BACK_STYLES` (background, font, caption weight, tracking and case, extra CSS or HTML, frame style), and the back of variant 11 from `template_11_split_panel_back.html`.
Source: `experiments/render_all.py:78-144,165-182`. Verification: no test.

**FR-11.** The system shall put the same QR code on every back: `QR_TARGET` encoded with error correction M, box size 9, border 4, black on white, with the caption `portfolio`.
Source: `experiments/render_all.py:33-34,41-48,150,167,178`. Verification: no test.

**FR-12.** The system shall render, on the variant 6 front, a `|` divider and the plain label `C++ / Python` after the first tag.
Source: `experiments/templates/template_06_qr_centerpiece.html:109`. Verification: no test.

### 3.3 Print pages

**FR-13.** `print.html` shall show one front and one back card of 90 x 50 mm and a button that calls `window.print()`; the instruction block shall be hidden when printing.
Source: `print.html:14-49`, `print.css:10-11,39-47,175-177`. Verification: no test.

**FR-14.** `print_many.html` shall build 12 front cards and 12 back cards in script, place each set in a 3 x 4 grid, and break the page between the two grids, for A4 landscape with zero margin.
Source: `print_many.html:58,89-103`, `print.css:159-163,178-196`. Verification: no test.

**FR-15.** The back of the print pages shall show `QR code VCF.jpg` captioned "Scan to Add VCF" and `webpage qr code.png` captioned with the site's domain; the front shall show the name, a job title and skill chips without contacts.
Source: `print.html:22-48`, `print_many.html:61-84`. Verification: no test.

### 3.4 Content files

**FR-16.** `experiments/vcf/vcf_standard.vcf` shall be a vCard 3.0 with the properties N, FN, TEL, EMAIL, TITLE, URL and an inline base64 JPEG PHOTO.
Source: `experiments/vcf/vcf_standard.vcf:1-9,244`. Verification: no test.

**FR-17.** `experiments/vcf/vcf_minimal.vcf` shall be a vCard 3.0 with N, FN, TEL, EMAIL and an inline base64 JPEG PHOTO, without TITLE and URL.
Source: `experiments/vcf/vcf_minimal.vcf:1-7,242`, `experiments/vcf/README.md:26-27`. Verification: no test.

**FR-18.** `cv.html` shall present a sidebar with the sections Contacts, Links, Skills, Languages and Hobbies, and a main column with About Me, Work Experience and Education.
Source: `cv.html:51,70,89,118,137,164,174,256`. Verification: no test.

**FR-19.** The committed card `front.png` and `back.png` shall be 1119 x 615 px, the front being generator output and the back plain white.
Source: commit `bbb6840` message, `README.md:9-10`; size read from the PNG headers. Verification: no test.

### 3.5 Repository interface

**FR-20.** `recipe.ps1` shall follow the repo-quality-template verb set; here `test` runs pytest, `ruff check` and `ruff format` over `.claude`, `info` prints name, code, version and summary, `clean` removes cache folders, and the other verbs print `nothing to <verb>`.
Source: `recipe.ps1:1-74`. Verification: no test; `.\recipe.ps1 info` run on 2026-11-18, exit 0.

### 3.6 Declared but not implemented

| Statement | Where declared | State in the repository |
| --- | --- | --- |
| Pixel and SSIM comparison with the original artwork | `generator/README.md:76-94` | `compare.py` "is not shipped" (line 80); the table predates the text enlargement in `bbb6840` |
| Every QR decodes correctly (OpenCV) | `experiments/README.md:69-70` | No decoding script or test in the repository |
| vCards use CRLF line endings | `experiments/vcf/README.md:33-34` | Files are LF (`git ls-files --eol`), and no commit since they were added in `84e7ba3` holds a CR byte in them; `.gitattributes:1` keeps them LF on checkout |
| A QR that carries a vCard directly | `experiments/vcf/README.md:45-49`, `generator/README.md:61-65` | Left as "separate decision"; a photo-less revision exists only in commit `84e7ba3` |
| CV portrait | `cv.html:46` | `image.png` is not in the repository (`README.md:25-26`) |
| CV PDF built from `cv.html` | implied by the pair in `README.md:25` | Commit `de6d49a`: "nothing in this repository builds it"; the PDF was edited directly |

## 4. Interfaces

### 4.1 Command line

| Command | Arguments | Output | Source |
| --- | --- | --- | --- |
| `python generate.py` | `--config PATH` (required), `--out-dir DIR` (required) | `DIR/front.png`, `DIR/back.png`, two `Wrote ...` lines | `generate.py:106-124` |
| `python render_all.py` | none | 22 PNGs under `experiments/variant_*/`, one `Rendered ...` line each | `render_all.py:147-184` |
| `.\recipe.ps1 <verb>` | `build`, `install`, `uninstall`, `clean`, `run`, `publish`, `info`, `test` | see FR-20 | `recipe.ps1:1-7,40-74` |

### 4.2 Template contexts (Jinja2)

| Template | Variables | Source |
| --- | --- | --- |
| `generator/template.html` | all `DESIGN` keys, `name`, `title`, `phone`, `email`, `url`, `tags`, `qr_data_uri`; also reads `tag_bg`, `tag_text`, which are never passed and render empty | `generate.py:78-87`, `template.html:9-25` |
| `experiments/templates/template_01..11_*.html` | `name`, `title`, `phone`, `email`, `tags`, `photo_uri`, `cta` | `render_all.py:158` |
| `template_back_shared.html` | `qr_uri`, `caption`, `bg`, `font_family`, `font_href`, `caption_weight`, `caption_tracking`, `caption_transform`, `extra_css`, `extra_html`, `frame_extra`; defaults in the template for `caption_weight` (`600`), `caption_tracking` (`2px`), `caption_transform` (`none`), `radius` (`10px`), `text_color` (`#ffffff`) | `template_back_shared.html:6-47`, `render_all.py:167-169` |
| `template_11_split_panel_back.html` | `qr_uri`, `caption` | `render_all.py:178` |

### 4.3 File formats

| File | Format | Source |
| --- | --- | --- |
| `generator/card.json` | JSON object, keys per FR-2 | `generator/card.json:1-9` |
| Rendered sides | PNG, 1119 x 615 px | `generate.py:33-34`, `render_all.py:24` |
| `experiments/vcf/*.vcf` | vCard 3.0, lines folded at 75 characters, LF line endings | `vcf_standard.vcf:2`; measured |
| Print layout | CSS mm units, card 90 x 50 mm, A4 landscape page | `print.css:10-11,160-163` |

## 5. Data

| Entity | Storage | Notes |
| --- | --- | --- |
| Card content | `generator/card.json`; separately hard-coded in `render_all.py:26-34`, `print.html:25-48`, `print_many.html:61-84`, `cv.html`, the two vCards | Repeated per file and not synchronised by code; the values already differ (job title, tag spelling, phone formatting) |
| Design constants | `DESIGN`, `QR_*` in `generate.py:32-61`; CSS in each template | Not part of the config |
| Photos | `experiments/assets/photo.png` (560 x 560), `photo_old.png` (640 x 640), `me.png` (2560 x 2560) | Read by `render_all.py:149` (`photo.png` only) |
| Rendered images | `front.png`, `back.png`, `experiments/variant_*/*.png` | Committed; `previews/*.png` of variant 6 are produced by no script in the repository |
| Contact files | `experiments/vcf/*.vcf`, about 18 KB each (18 048 and 17 987 bytes) | Contain phone and email; too large for a QR code (`experiments/vcf/README.md:45-47`) |
| Binary storage | Git LFS for `*.png`, `*.jpg`, `*.pdf` | `.gitattributes:8-10` |

## 6. Non-functional requirements

**NFR-1.** Rendered card sides shall be 1119 x 615 px. Source: `generate.py:33-34`, `render_all.py:24`.

**NFR-2.** QR codes shall use error correction level M and a 4-module quiet zone. Source: `generate.py:59-61`, `render_all.py:42`.

**NFR-3.** Printed cards shall be 90 x 50 mm, with colours printed as specified (`print-color-adjust: exact`). Source: `print.css:10-11,18-19`.

**NFR-4.** Text files shall be checked out with LF line endings, PowerShell scripts with CRLF. Source: `.gitattributes:1-2`.

**NFR-5.** No key shall be committed: `.claude/.env` and the root `.env` are ignored. Source: `.gitignore:24,27`, `CLAUDE.md` rule 4.

**NFR-6.** The code shall be distributed under the MIT licence. Source: `LICENSE:1-3`.

## 7. Constraints and dependencies

| Dependency | Version | Source |
| --- | --- | --- |
| Python | 3.12 for the documented venv; not enforced in code | `generator/README.md:22` |
| jinja2 | `>=3.1,<4` | `generator/requirements.txt:1` |
| qrcode | `>=8.0,<9` | `generator/requirements.txt:2` |
| pillow | `>=10.0,<12` | `generator/requirements.txt:3` |
| playwright | `>=1.45,<2`, plus `playwright install chromium` | `generator/requirements.txt:4`, `generator/README.md:25` |
| ruff (tooling) | `==0.16.1` | `.claude/ruff.toml:2` |
| Font Awesome (CDN) | 6.4.0 | `print.html:6`, `cv.html:8` |
| Tailwind (inlined CSS) | v3.4.17 | `cv.html:36` |

There is no lock file. `render_all.py` uses the generator's requirements
(`experiments/README.md:101-103`).

## 8. Acceptance

1. In `generator/`, set up per `generator/README.md:21-26` and run
   `python generate.py --config card.json --out-dir output/`. Expect two
   `Wrote` lines, `output/front.png` and `output/back.png` of 1119 x 615 px,
   and a white back (FR-1 to FR-8). Compare `output/front.png` with the root
   `front.png` by eye; exact equality is not expected (font antialiasing,
   `generator/README.md:92-94`).
2. Decode the QR in `output/front.png` with any reader; expect the `qr_data`
   value (FR-3).
3. In `experiments/`, run `python render_all.py`; expect 22 `Rendered` lines and
   `git status` listing only PNGs under `experiments/variant_*/` (FR-9 to FR-12).
4. Open `print.html` and `print_many.html`, print to PDF: one card pair, then
   two A4 landscape pages of 12 cards (FR-13 to FR-15).
5. Import both vCards on a phone; check the fields of FR-16 and FR-17. Check
   `git ls-files --eol experiments/vcf` for the line endings.
6. Run `.\recipe.ps1 test`; expect `$LASTEXITCODE` 0 (FR-20).

## 9. Open questions

- Which design is the current card: the root `front.png` ("the card as it
  stands", `README.md:9`) or variant 6 ("the final, print-ready design",
  `experiments/README.md:184-186`)? Were the 50 copies printed?
- Are `print.html` and `print_many.html` still in use? Commit `7a0aa02` calls
  them "legacy", and their title differs from the card's.
- Is "5+ years experience" on variant 11 correct (`experiments/README.md:261-263`)?
- Should `card.json` keep the "AI Intergation" typo now that the root
  `front.png` is generator output rather than the original artwork?
- Were CRLF line endings intended for the vCards (`experiments/vcf/README.md:34`)
  despite `.gitattributes:1`? Measured: every committed version of the
  vCards since `84e7ba3` is LF; what working trees showed before
  `.gitattributes` existed depends on `core.autocrlf` and is not recorded.
- Answered: `contacts.vcf` in the personal site's repository
  (IGORSVOLOHOVS.github.io, branches `main`, `test` and `release`, read from a
  local clone on 2026-11-18) is the same git blob as `vcf_standard.vcf`
  (18 048 bytes), as commit `7a0aa02` says. The copy the live site serves was
  not fetched.
- What do `QR code VCF.jpg` and `webpage qr code.png` encode? Commit `7a0aa02`
  says the first encodes the site's `contacts.vcf`; neither was decoded here.
  `QR code VCF.jpg` is the same Git LFS object as `vcf.jpg` in the personal
  site's repository.
- Where are `cv.html`'s `image.png` and the tool that produced the CV PDF?
  Partly answered: the personal site's repository has an `image.png` that is
  the same Git LFS object as `experiments/assets/photo_old.png`; whether
  `cv.html` means that file is not recorded. The PDF tool is unknown.
- What do the README's exceptions R-37, R-41 and R-42 cover? They point to
  issues #9-#11 on a Gitea instance that was not read.
- Who besides the owner is meant to use the generator, and is there a target
  printer or print shop whose requirements apply?
