# Auto Master Drive — YouTube Production System

Public production system for the **Auto Master Drive** YouTube channel:
https://youtube.com/@automasterdrive

Niche: future EV / EREV head-to-head comparisons (model years 2026–2030),
trucks, Scout Motors, Tesla — US audience. 4 long videos a week
(Tue / Thu / Fri 01:00 PKT + Sun 01:00 PKT fast-trending) + 2 Shorts a day.

## What lives here

| Path | What it is |
|---|---|
| `titles/title-bank.md` | All published long-video titles + the title patterns that work (model + year + "vs" + number/price/range). No puzzle titles. |
| `scripts/script-template.md` | Blank long-video script template (hook, sections, scoreboard, verdict, open question, subscribe CTA). |
| `scripts/hook-checker.py` | Checks a script's first ~30 seconds for a number, a shock claim, and an open question/promise. `python3 scripts/hook-checker.py script.md` — exit 0 = pass, 1 = fail. |
| `.github/workflows/daily-stats.yml` | Daily GitHub Action: fetches public channel stats with yt-dlp (no API key) and appends one JSON line to `stats/history.jsonl`. |
| `docs/index.html` + `docs/stats.json` | Static dashboard (GitHub Pages, served from `/docs`): subscribers, views, videos, next uploads, monetization target. |
| `stats/history.jsonl` | One JSON line per day of public channel stats (grows via the daily Action). |

## Rules the whole system follows

- **Titles** = search phrases US viewers type: model + year + "vs" + number /
  price / range. Clever / puzzle titles are banned.
- **Honesty first:** every figure is labelled claim vs tested vs official.
  Never fake specs, designs, prices, staged results, or a winner in the
  thumbnail. Rumours are always framed as "reports say".
- **"Auto Master Drive" appears exactly 2×** in every long-video narration.
- **Upload disclosure:** YouTube Studio's "Altered or synthetic content" =
  **YES** for every video (AI images + AI voiceover).
- **Voice:** one locked voice for all voiceovers.
- **Thumbnails:** 2 per video (Test & Compare). Winner is NEVER in the thumbnail.
- **Every video** ends with an open question that becomes the next video's topic.

## Monetization sprint

Target: **1,000 subscribers + 4,000 watch hours by 31 Jan 2027**
(apply at the old YPP bar before it doubles on 1 Feb 2027).
Status as of 9 Nov 2026: 51 subscribers, 29,169 total views, 102 videos.
