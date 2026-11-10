# Thumbnails — locked template

`amd_thumbnail.py` renders every Auto Master Drive thumbnail in one locked style (PIL, no paid tools):

- Canvas 1920×1080, headline at the BOTTOM (top quarter empty)
- Optional big YELLOW number line above the headline (range / price / hp)
- Optional small subline at the TOP-LEFT (top-right is the logo's corner)
- Real AMD logo top-right on a white rounded backing
- Dark gradient over the bottom band so text stays readable on any base

The base image must NOT already contain headline text — the template renders all text itself. Use a clean scene still as `--base`.

Usage:

```bash
python3 amd_thumbnail.py --base scene.jpg --headline "ENDS IN 2027" \
    --number "420 VS 320" --subline "CYBERTRUCK vs RIVIAN R1T" \
    --out thumbnail.png
```

Tested 9 Nov 2026 on the Cybertruck vs Rivian R1T long (template-main/alt in that video's folder). Adopted as the pipeline standard from the Thursday 12 Nov Scout long. Works under PIL 13.
