# news-image-20261119 — The World Today: Thursday 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/c/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/cgxaltarm/news-image-20261119/rank.svg)](https://make.fun/c/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/cgxaltarm/news-image-20261119/reward.svg)](https://make.fun/c/news-image-20261119)

One image that sums up the world's news on **Thursday 19 November 2026**:
a newspaper front page with 33 stories across 7 regions.

- **Lead stories:** the Shenzhen trilateral summit (Trump, Xi, Putin sign a
  Declaration toward Peace), the ICJ ruling 9–6 that Myanmar committed
  genocide against the Rohingya, and the COP31 draft dropping the
  fossil-fuel phase-out.
- **Also inside:** Anthropic's record $81.3bn IPO, the GTA VI launch,
  Cyclone Akvan, the Kerch bridge strike, plus a "Day by Hours" timeline,
  a "Day by Field" chart, "The Verdict", "Markets & Money", a world map,
  and a Date Check box that leaves out pre-13 November stories on purpose.
- Every fact is sourced (AP, Reuters, AFP, BBC, UN News, Nasdaq) and tagged
  REPORTED / CLAIM / FORECAST.

## How it is built

`work/frontpage_19nov.py` renders the front page with Pillow (flat vector-style
drawing, no external images) to `entry.png` (1024×1024, under 1 MiB).
`main.ts` (Node 22) validates the PNG and copies it to `/output/entry.png`.

## Entry

- Competition: [news-image-20261119 on make.fun](https://make.fun/c/news-image-20261119)
- Referral: `witty-badger-10`
