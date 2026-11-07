# visitka

"Visitka" is Russian for "business card". This is the business card of Igors
Volohovs: the artwork, the small script that renders it, the design experiments
behind it, the contact files, and a one-page CV.

## What is here

- `front.png` and `back.png` are the card as it stands: the front carries the
  QR code, name, title, contacts and skill tags, and the back is blank.
- `generator/` renders those two images from `card.json`, a config that holds
  content only. `generate.py` fills the Jinja2 `template.html`, embeds a QR code
  and takes a screenshot with headless Chromium through Playwright.
  `generator/README.md` has the setup and the config fields. Its
  `requirements.txt` is the only dependency list, and nothing in this
  repository's checks runs the script.
- `experiments/` holds eleven other designs for the same content:
  `templates/` is their HTML, `variant_*/` the rendered sides, and
  `render_all.py` renders them all. `experiments/README.md` explains the layout.
- `experiments/vcf/` holds the vCard files. `vcf_standard.vcf` is the official
  contact file and `vcf_minimal.vcf` a shorter fallback.
- `print.html`, `print_many.html` and `print.css` are pages for printing cards at
  90 x 50 mm, using `QR code VCF.jpg` and `webpage qr code.png`. They are in
  Russian, and so is the name of the PDF printed from `print_many.html`.
- `cv.html` and `CV_Igors_Volohovs_OnePage.pdf` are the one-page CV. `cv.html`
  names an `image.png` that is not in this repository.
- `me.png` is a portrait.

## Working on it

This repository ships no program: it is documents, images and two small
scripts. `.\recipe.ps1` is still its whole interface: `.\recipe.ps1 test` runs
pytest and ruff over `.claude`, and `.\recipe.ps1 info` prints the metadata. The
other verbs print `nothing to <verb>`. `CLAUDE.md` holds the rules.

## License

MIT. See [LICENSE](LICENSE).
