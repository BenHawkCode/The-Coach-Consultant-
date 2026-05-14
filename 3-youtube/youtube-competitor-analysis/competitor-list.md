# YouTube Competitor List

10 channels selected from the master 31-profile IG competitor list. All 10 also appear in `2-instagram/ig-competitor-analysis/competitor-list.md`, so the same competitor universe is tracked across both platforms — like-for-like comparisons stay clean and findings on one channel reinforce the other.

Filtered to channels with an active YouTube presence AND a content fit with the TCC ICP (Sam: open business owner, 35-50, £100K-£500K, founder-led service business). Channels with podcast / political / entertainment leanings (Steven Bartlett, Chris Williamson, Tony Robbins) excluded — they generate big numbers but on topics outside Sam's pain layers.

## Tier 1: Direct competitors (offer + hook density)

| # | Handle | Name | Why Study |
|---|--------|------|-----------|
| 1 | @AlexHormozi | Alex Hormozi | Master of direct-response hooks, metric-led storytelling, offer framing |
| 2 | @DanMartell | Dan Martell | SaaS + coaching, buyback principle framework, authority positioning |
| 3 | @ImanGadzhi | Iman Gadzhi | Agency education, aggressive hooks, proof-led creative |
| 4 | @RussellBrunson | Russell Brunson | Funnel-first content, marketing frameworks |
| 5 | @LeilaHormozi | Leila Hormozi | Operational + team-building hooks, female audience overlap |
| 6 | @myrongolden | Myron Golden | High-ticket offer positioning, bold hooks |
| 7 | @BrendonBurchard | Brendon Burchard | Polished creative with strong emotional hooks |

## Tier 2: Content-first entrepreneurs

| # | Handle | Name | Why Study |
|---|--------|------|-----------|
| 8 | @aliabdaal | Ali Abdaal | Course creator, clean educational hooks |
| 9 | @garyvee | Gary Vaynerchuk | Content volume king, repurpose patterns |

## Tier 5: UK-specific (closest market fit)

| # | Handle | Name | Why Study |
|---|--------|------|-----------|
| 10 | @JamesSinclairEntrepreneur | James Sinclair | UK business owner, down-to-earth interview format |

## Ben Idea Bank subset (5 channels for the weekly idea bank brief)

The full 10-channel pool feeds the competitor analysis intelligence brief (Antonio).
The Ben Video Idea Bank brief uses a 5-channel subset of the above, picked for ICP fit and Ben's preferred competitors:

- @AlexHormozi
- @DanMartell
- @ImanGadzhi
- @aliabdaal
- @JamesSinclairEntrepreneur

This subset lives in `scripts/_shared.py` under `IDEA_BANK_HANDLES`.

## Why this list, not a bigger one

We previously tried 20 channels. Seven failed scrape (handle mismatches between IG and YouTube — different platforms, different naming conventions). Three more (Steven Bartlett, Chris Williamson, Tony Robbins) produced high-volume hooks on politics, celebrity, and motivation that don't map to any TCC pain layer. They polluted the top-hook ranking without giving the intelligence brief anything actionable.

The 10 above are the channels where every top video maps to a Sam pain anchor and the framework / hook patterns are directly transferable to TCC content.

## Notes

- Channel handles verified before each run. yt-dlp will skip any handle it can't resolve.
- First-pass scrape pulls last 30 days of long-form videos plus last 30 Shorts per channel.
- Top 5 by engagement (views * like-rate) per channel go through Gemini multimodal for hook / framework / CTA / pain-anchor analysis. 10 channels x 5 = 50 videos per weekly run.
- The other ~250 videos sit in the raw JSON as metadata only.
