# VCF (vCard) variants

Replacement candidates for the old "Scan to Add VCF" contact card.

## What was wrong with the old one

- **The QR didn't contain a vCard at all** - it pointed to a Google Drive
  link (`drive.google.com/file/d/1KZ-9Bd...`). Scanning landed people on a
  Drive page where they still had to download and open the file, instead of
  the phone immediately offering "Add contact?".
- **42 KB of noise.** The Drive-hosted file packed in NICKNAME, a work
  address, LANG x3, CATEGORIES, GEO coordinates, BDAY, a NOTE, and a ~40 KB
  embedded photo.
- **Up to 7 link-ish entries**: 4x URL (Telegram, GitHub, LinkedIn,
  portfolio) + 2x X-SOCIALPROFILE duplicating GitHub/LinkedIn + the
  portfolio URL repeated a third time inside NOTE. This is the "too many
  links, confusing" complaint.
- **Stale data**: ORG "Additive Lab" and TITLE "C++ Developer" (now
  Software Engineer).
- Format nit: lines were LF-separated; the vCard spec requires CRLF.

## The 4 variants (current revision)

All are vCard **3.0** (best importer compatibility across old and new
phones - 4.0 offers nothing useful here), correct CRLF line endings,
spec-compliant 75-octet line folding.

Per Igor's revision: **every variant now embeds his photo** (new selfie,
face-centered square crop, 240x240 JPEG avatar), and there is only **one
link** - the portfolio; the GitHub URL and the `itemN.`/`X-ABLabel`
grouping from the previous revision are gone.

| File | Size | Contents |
|---|---|---|
| `vcf_minimal.vcf` | ~17 KB | name, phone, email, photo |
| `vcf_standard.vcf` | ~17 KB | + Software Engineer, portfolio URL |
| `vcf_full.vcf` | ~17 KB | same as standard (see note) |
| `vcf_with_photo.vcf` | ~17 KB | same as standard (see note) |

**Note:** after this revision `vcf_standard.vcf`, `vcf_full.vcf` and
`vcf_with_photo.vcf` are byte-identical - the photo is in all variants
now and dropping GitHub removed the only other thing that set them
apart. Practically there are two real choices: minimal (no title/link)
and standard (title + portfolio). The duplicate files are kept for now
so the set of names Igor is reviewing stays stable; prune them once he
settles on one.

**Heads-up on QR use:** at ~17 KB none of these fit in a QR code anymore
(practical vCard-in-QR limit is roughly 1-2 KB). These files are for
sending directly (email/Telegram/AirDrop) or hosting behind a short
link. If a scan-to-add-contact QR is wanted, it needs a photo-less
vCard (the previous 315-byte revision fit comfortably) - that's a
separate decision.
