[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/7tomars/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/7tomars/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# News Image — Saturday 21 November 2026

One newspaper-poster image summing up the world news of Saturday 21 November 2026: Mexico captures cartel boss "El Chapo Isidro"; the COP31 climate talks in Antalya run into overtime with no deal; a Russian "double-tap" strike hits Kryvyi Rih; Wall Street plunges as the AI sell-off deepens; a magnitude 6.9 earthquake shakes Peru; a Wolbachia mosquito trial cuts dengue and chikungunya by about 69% among schoolchildren in Brazil; BepiColombo enters orbit around Mercury; and two tankers are hit by projectiles near the Strait of Hormuz.

## How to run

Requires Python 3.12+ and nothing else — standard library only, no network, no external fonts or image libraries. The bitmap font and the PNG encoder are written from scratch in `main.py`.

```sh
python3 main.py
```

This writes `entry.png` (1024×1024, under 1 MiB) into `$MAKEFUN_OUTPUT_DIR` when that variable is set, otherwise into `/output`. Runs are deterministic: two runs produce byte-identical output.

## Date discipline

Every story on the poster is news of Saturday 21 November 2026, verified against at least two real news sources published that day. These near-misses were checked and kept out:

- The ICJ Myanmar/Rohingya genocide ruling was 19 November, not 21 November.
- Anthropic's $2 trillion IPO debut was Thursday 19 November.
- The New York Times report that Trump was weighing new Iran strikes ran 18 November — the 21 November news was Trump delaying any decision until after the new year.
- The Russian strikes on Kyiv that killed 3 were Friday 20 November.
- The Russian missiles and drone that entered Polish airspace were 19–20 November.
- Voyager 1 crossed one light-day from Earth on 18 November and NASA confirmed it 19 November — widely reported 21 November but not 21 November news.
- The COP31 draft deal stripping fossil-fuel references was Thursday 19 November.

## Sources

Each of the eight stories was verified in at least two outlets:

1. Mexico captures "El Chapo Isidro" — Reuters / AP
2. COP31 talks run into overtime — Reuters / AP
3. Russian strike hits Kryvyi Rih — AP / AAP
4. Wall Street plunges in AI sell-off — Le Monde / AP
5. Magnitude 6.9 quake shakes Peru — AP / TBS News
6. Wolbachia mosquito trial cuts dengue by 69% — AP / Gulf News
7. BepiColombo enters orbit at Mercury — Nature / EarthSky
8. Two tankers hit near Strait of Hormuz — Reuters / NY Post

## License

MIT — see [LICENSE](LICENSE).
