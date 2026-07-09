# VCF (vCard) variants

Replacement candidates for the old "Scan to Add VCF" contact card.

## What was wrong with the old one

- **The QR didn't contain a vCard at all** - it pointed to a Google Drive
  link (`drive.google.com/file/d/1KZ-9Bd...`). Scanning landed people on a
  Drive page where they still had to download and open the file, instead of
  the phone immediately offering "Add contact?".
- **42 KB of noise.** The Drive-hosted file packed in NICKNAME, a work
  address, LANG x3, CATEGORIES, GEO coordinates, BDAY, a NOTE, and a ~30 KB
  embedded photo.
- **Up to 7 link-ish entries**: 4x URL (Telegram, GitHub, LinkedIn,
  portfolio) + 2x X-SOCIALPROFILE duplicating GitHub/LinkedIn + the
  portfolio URL repeated a third time inside NOTE. This is the "too many
  links, confusing" complaint.
- **Stale data**: ORG "Additive Lab" and TITLE "C++ Developer" (now
  Software Engineer).
- Format nit: lines were LF-separated; the vCard spec requires CRLF.

## The final set: 2 files

Earlier revisions had 4 files, but after Igor's changes (photo in every
variant, GitHub link dropped) three of them became byte-identical, so the
set is now two honest variants instead of four duplicated names.

Both are vCard **3.0** (best importer compatibility across old and new
phones - 4.0 offers nothing useful here), correct CRLF line endings,
spec-compliant 75-octet line folding. The photo is the one from Igor's
old VCF - the exhibition shot with the Yaskawa robot - kept uncropped
(it's already square) and downscaled from 480x480/30 KB to a 240x240
JPEG avatar.

| File | Size | Fields |
|---|---|---|
| `vcf_minimal.vcf` | ~18 KB | name, phone, email, photo |
| `vcf_standard.vcf` | ~18 KB | + Software Engineer, portfolio URL |

**Heads-up on QR use:** at ~18 KB neither fits in a QR code (practical
vCard-in-QR limit is roughly 1-2 KB). These files are for sending
directly (email/Telegram/AirDrop) or hosting behind a short link. If a
scan-to-add-contact QR is wanted, it needs a photo-less vCard (the
315-byte revision at commit 84e7ba3 fit comfortably) - separate decision.
