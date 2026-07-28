# Why Refreshes Haven't Moved Rankings — And The Fix

**Date:** 2026-07-28 | Companion to STRATEGY.md

## The diagnosis (data-verified)

**It is NOT an authority problem:**
- blockchain-ads.com: 3,558 referring domains (1,647 dofollow), DR-strong homepage (UR 9.0).
- The page ranking **#1** for "igaming marketing agency" (luvkaizen) has **0 backlinks**. Vizibl's platform page at #13: **0 backlinks**. HilltopAds' post at #7: 1 referring domain.
- Conclusion: we massively out-muscle every SERP winner. Links are not the bottleneck.

**It IS a cannibalization + focus problem — 202 queries with multiple BCA pages competing (GSC, 28d):**

| Query cluster | Competing BCA pages | Effect |
|---|---|---|
| casino/gambling affiliate (~8,000 impr/mo) | /post/casino-affiliate-marketing + /post/gambling-affiliate-program | Both stuck pos 15–80, ~0 clicks |
| casino advertising | /post/casino-advertising-examples + /post/gambling-advertising + /post/igaming-ad-examples (3-way) | All stuck pos 18–50 |
| igaming/gambling ad network, buy gambling traffic | /igaming-advertising + /post/top-gambling-ad-networks + /post/igaming-marketing-agency | Money page pos 46–60; post pos 14 |
| casino marketing (agency) | /post/casino-marketing-strategies + /post/igaming-marketing-agency | Split pos 17–37 |
| crypto ad network family | Homepage + /crypto-advertising + /post/best-web3-ad-networks + /publishers (4-way) | All pos 17–26 |
| Money-page level | **/igaming-advertising (594 internal links) vs /crypto-gambling-betting (994 internal links)** | Two nav-level pages, same vertical |
| Locales | /ru/ and /ko/ versions ranking in EN SERPs (e.g. "igaming" → /ru/post/igaming-vertical, 1,020 impr) | hreflang misconfiguration |

**Secondary finding:** /igaming-advertising has 135 refdomains but only **3 dofollow** — and ranks for ~0 keywords. It's invisible to Google despite sitewide nav links (nav links pass little topical relevance; contextual in-content links do).

**Why refreshing failed:** a refresh improves one page's content, but Google's problem was never content quality — it can't pick WHICH page deserves the query. Relevance stays split, every page stays capped at pos 12–25. No refresh fixes that.

---

## The fix: consolidate → differentiate → funnel

### Step 1 — One query, one page (the assignment map)

| Intent | Canonical page | Action on competitors |
|---|---|---|
| iGaming advertising platform / ad network / buy igaming+gambling traffic | **/igaming-advertising** | Becomes THE hub. All iGaming posts add contextual in-content links with anchors "iGaming ad network", "buy gambling traffic", "iGaming advertising platform". |
| Crypto casino / crypto gambling advertising | /crypto-gambling-betting | **Differentiate, don't compete**: reposition as the crypto-casino wedge page (title: "Crypto Casino & Gambling Advertising"). Remove generic iGaming keywords from title/H1/meta. Link up to /igaming-advertising as parent. |
| casino/gambling affiliate programs + marketing | /post/casino-affiliate-marketing (188 refdomains, best positions) | **301 /post/gambling-affiliate-program → it.** Merge any unique content first. Kills the biggest split (~8,000 impr/mo). |
| best gambling/igaming ad networks (+ buy gambling traffic listicle intent) | /post/top-gambling-ad-networks (already pos 3.65 for "best igaming ads networks") | Put Blockchain-Ads at #1. Add comparison table. Link to /igaming-advertising. |
| casino ads examples | /post/casino-advertising-examples | Retitle to own "casino ads/advertising examples" ONLY. Cut gambling-generic sections. |
| gambling ads/advertising (regulation + overview) | /post/gambling-advertising | Retitle to own "gambling advertising" ONLY. Cut casino-example sections (link to examples post instead). |
| igaming ads examples | /post/igaming-ad-examples | Own "iGaming ads" ONLY. |
| casino marketing strategies | /post/casino-marketing-strategies | Keep strategies intent; remove "agency" targeting. |
| igaming marketing agency | /post/igaming-marketing-agency | Keep the listicle; reframe intro: "need a platform instead of an agency?" → /igaming-advertising. BCA platform gets the #1 spot. |
| crypto ad network | /crypto-advertising | De-optimize homepage/publishers for this term; /post/best-web3-ad-networks links to /crypto-advertising as #1. |

### Step 2 — /igaming-advertising hub — ✅ MOSTLY DONE (redesigned 2026-07-26)
Verified live 2026-07-28: platform positioning ("Advertising Platform for iGaming"), case studies with hard numbers (BC.Game, 1win, Stake $250 CPA, Roobet $23 CPA, Dafabet), 17-question FAQ, channel links, 3.5–4k words. This satisfies the hub requirement — do NOT rebuild again.

Remaining on-page nits only:
- Two H1s detected ("Advertising Platform for iGaming" + "Drive user acquisition...") — keep exactly one H1.
- Query coverage gap: page targets "igaming advertising platform" but demand clusters around **"igaming ad network"** and **"igaming traffic" / "buy gambling traffic"** (the surging terms). Work these phrases into H2s/FAQ copy naturally (e.g. FAQ: "Is Blockchain-Ads an iGaming ad network or a DSP?", "Can I buy gambling traffic on a CPA basis?").
- Add FAQPage schema markup if not present (17 FAQs already written — free win).
- IMPORTANT: two days post-redesign is too early for ranking movement; Google needs 2–6 weeks. Judge the redesign no earlier than week 4 — but its effect stays capped until cannibalization (Steps 1, 3, 4) is resolved.

### Step 3 — Contextual internal linking (the relevance funnel)
- Every iGaming post: 1–2 in-content links to /igaming-advertising with commercial anchors (vary them), placed in the first half of the article.
- Hub links down to each cluster post ("iGaming ad examples", "casino affiliate marketing guide") — hub-and-spoke.
- Case studies (betpanda, casino-punkz, low-cpa-casino) link to /igaming-advertising.

### Step 4 — hreflang hygiene
- /ru/post/igaming-vertical is taking 1,020 EN-market impressions; /ko/ and /es/ versions leak into EN SERPs. Verify hreflang + x-default on all locale variants (Webflow localization settings). EN pages must be canonical for EN queries.

### Step 5 — Targeted authority (small, surgical)
- Only 3 dofollow refdomains on the money page. Get 5–10 contextual dofollow links to /igaming-advertising: inclusion in ranking listicles ("best gambling ad networks" posts by HilltopAds-style blogs), iGaming trade press (SBC, EGR), affiliate forums (STM, affLIFT).
- This is polish, not the fix — competitors rank with 0 links.

### Step 6 — Measure the right way
- Tracking set: igaming advertising / ads / ad network / traffic, buy gambling traffic, casino advertising, gambling ads, casino affiliate programs, best gambling ad networks, igaming marketing agency.
- Expect: 2–3 weeks for consolidation signals (301s recrawled), movement weeks 3–6. If a merged query cluster doesn't improve by week 6, the merge target was wrong — revisit.

## Sequence (revised — hub redesign already shipped)
1. Week 1: 301 gambling-affiliate-program merge; retitle/de-overlap the casino/gambling/igaming ads trio; differentiate /crypto-gambling-betting from /igaming-advertising; contextual in-content links from all iGaming posts → hub.
2. Week 2: top-gambling-ad-networks BCA-first rework; hreflang audit; hub on-page nits (single H1, ad-network/traffic phrasing, FAQ schema).
3. Weeks 3–6: watch tracking set weekly, then start conquest content (STRATEGY.md Phase 3) once the foundation stops leaking. Do not judge the redesign before week 4.

## Live SERP verification (2026-07-28, US desktop)

Checked live: igaming marketing agency, igaming advertising, igaming ad network, casino advertising, buy gambling traffic, casino affiliate programs.

**Confirmed:**
- **"igaming ad network" is our best commercial SERP.** Fully commercial: ReachEffect's dedicated LP at #2, Match2One DSP page #5, adsnetwork.io industry page #14, TrafficStars product page #18 — product pages win here. **Our /post/top-gambling-ad-networks sits at #9 live** (better than GSC 28d averages suggested — likely already benefiting from recent changes). The hub page targeting "igaming ad network" is the right move.
- **"buy gambling traffic" is a pure platform SERP**: TrafficNomads homepage #1, RichAds #2, HilltopAds' dedicated /igaming-traffic LP #15, TrafficStars /product/gambling-traffic #17. Our listicle is #22. Competitors win with **dedicated traffic LPs** — gap: we have no /gambling-traffic or buy-traffic-targeted section. Fold "buy gambling/igaming traffic" into the hub or ship a dedicated LP.
- Cannibalization diagnosis unchanged — it's structural, not SERP-specific.

**Corrected assumptions:**
1. **"casino advertising" (head term) — DEPRIORITIZE as a primary target.** Live SERP is fragmented: Google's ads policy #1, Pinterest, Reddit, Wikipedia, YouTube, and **land-based** casino agencies (LT Agency, Good Giant). No online-platform page in top 20. The B2B-online intent we serve is a minority of this SERP; ceiling is low regardless of what we do. Target "casino ad network" / "casino traffic" phrasings instead; keep the examples post for the examples-intent slice only.
2. **"casino affiliate programs" — consolidation alone won't win it; the format is wrong.** Live SERP = affiliate program operators (N1 Partners #6, Alpha Affiliates #8, LivePartners #10) and program directories/listicles (StatsDrone #3, 15m, affcatalog, GPWA). Searchers are affiliates choosing programs to join. Our #22 page is a "what is casino affiliate marketing" guide — intent mismatch. Fix: still do the 301 merge, but ALSO reformat the surviving page as "Best Casino Affiliate Programs (2026)" — a real program listicle with payout models (CPA/RevShare/hybrid) — with a "where to buy traffic for these offers" bridge to the hub. These searchers are media buyers, i.e. our actual ICP.
3. **"igaming advertising" (head term) is mixed intent** — regulation bodies (AdStandards, AGCO, Meta policy) share the SERP with platforms (Vizibl's platform page holds #4). A platform page CAN rank (Vizibl proves it), but the hub's realistic primary wins are "igaming ad network" + "igaming advertising platform" + traffic terms, with "igaming advertising" as secondary.

## Flag (separate from iGaming, but urgent)
"blockchain-ads.com is a scam" gets 1,991 impressions/28d across 20 pages. /reviews ranks pos 3.4 — decent defense, but this reputation SERP deserves its own workstream.
