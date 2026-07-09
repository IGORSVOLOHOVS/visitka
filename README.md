# Visitka

Business card artwork for Igors Volohovs.

- `front.png` — front side: QR code, name, title, contacts, and skill tags.
- `back.png` — back side: blank.
- `generator/` — a small tool that renders `front.png`/`back.png` from a thin
  JSON config (name/title/contacts/tags/QR payload), so new cards can be
  produced without touching the design. See [`generator/README.md`](generator/README.md).
- **Contact file (vCard):**
  [`experiments/vcf/vcf_standard.vcf`](experiments/vcf/vcf_standard.vcf) — the
  official "add me to contacts" file (name, phone, email, title, portfolio
  URL, photo). Replaces the old Drive-hosted VCF; note the QR in the legacy
  `print.html`/`print_many.html` still encodes the old Drive link — see
  [`experiments/vcf/README.md`](experiments/vcf/README.md).

## Preview

**Front**

![front](front.png)

**Back**

![back](back.png)
