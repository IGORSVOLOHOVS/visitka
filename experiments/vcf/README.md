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

## The 4 new variants

All are vCard **3.0** (best importer compatibility across old and new
phones - 4.0 offers nothing useful here), correct CRLF line endings,
spec-compliant 75-octet line folding.

| File | Size | Contents | Use case |
|---|---|---|---|
| `vcf_minimal.vcf` | 150 B | name, phone, email | The absolute cleanest - nothing to be confused by |
| `vcf_standard.vcf` | 213 B | + Software Engineer, portfolio URL | Sensible default if one link is enough |
| `vcf_full.vcf` | 315 B | + GitHub as a second URL, both labeled "Portfolio"/"GitHub" (Apple `itemN.URL` + `X-ABLabel` convention - iOS shows named links, Android just sees two plain URLs) | **Recommended default** |
| `vcf_with_photo.vcf` | 12 KB | = full + embedded 240x240 JPEG avatar | For sending as a file (email/Telegram) where an avatar is nice; too big for a QR |

## Recommendation

**`vcf_full.vcf`** - it fixes the original complaint (2 labeled links
instead of 7 anonymous ones), keeps both links that actually matter
(portfolio + GitHub, same as the printed card), and at 315 bytes it fits
directly inside a QR code - so the QR can encode the vCard itself and the
phone offers "Add contact" instantly, no Google Drive middleman.
(Swapping the card's QR is a separate task, not done yet.)
