#!/usr/bin/env python3
"""Arrange clusters into a semantic library: pillars -> entries, with entries
ordered by information gain (greedy marginal SERP-territory coverage,
value-weighted). Outputs library.json + LIBRARY.md + library.csv."""
import csv, json, glob, re
from collections import defaultdict

SCRATCH = "/tmp/claude-0/-home-user-SEO/902ba0b1-362e-51aa-be60-e911903115d7/scratchpad"
clusters = json.load(open(f"{SCRATCH}/serp/clusters.json"))

# SERP url sets per keyword
def norm_url(u):
    u = u.split("#")[0].split("?")[0].rstrip("/")
    return u.replace("https://","").replace("http://","").replace("www.","").lower()
serp_urls = {}
for f in glob.glob(f"{SCRATCH}/serp/slice*.jsonl"):
    for line in open(f):
        line = line.strip()
        if not line: continue
        try: rec = json.loads(line)
        except json.JSONDecodeError: continue
        if rec.get("serp"):
            serp_urls[rec["kw"]] = {norm_url(i["url"]) for i in rec["serp"][:10] if i.get("url")}

meta = {r["keyword"]: r for r in csv.DictReader(open("/home/user/SEO/igaming/keyword-universe.csv"))}

PILLARS = {
 "Ad network / platform":      ("P1", "Platform, Ad Network & Traffic"),
 "Traffic buying":             ("P1", "Platform, Ad Network & Traffic"),
 "Competitor alternatives":    ("P1", "Platform, Ad Network & Traffic"),
 "Advertising (general)":      ("P2", "Vertical Advertising Playbooks"),
 "Ad examples & creatives":    ("P2", "Vertical Advertising Playbooks"),
 "Compliance & platform policy":("P3", "Compliance & Ad Policies"),
 "Affiliate programs & marketing":("P4", "Affiliate Economy"),
 "Agency-intent capture":      ("P5", "Growth & Marketing Strategy"),
 "Marketing strategy & guides":("P5", "Growth & Marketing Strategy"),
 "Operator setup":             ("P6", "Operator & Industry Resources"),
 "Vertical general":           ("P6", "Operator & Industry Resources"),
 "Affiliate B2B software":     ("P6", "Operator & Industry Resources"),
}
FITW = {"Core":1.0, "High":0.7, "Medium":0.4, "Low":0.15}

def slugify(k):
    return re.sub(r"[^a-z0-9]+","-",k.lower()).strip("-")

# cluster-level url universe + value
for c in clusters:
    urls = set()
    for k in c["members"]:
        urls |= serp_urls.get(k, set())
    c["urls"] = urls
    weak_factor = 1 + min(c["fruits"], 30)/30.0          # up to 2x for very weak SERPs
    strike = 1.5 if (c["bca_best_pos"] and c["bca_best_pos"] <= 20) else 1.0
    c["value"] = max(c["total_volume"],10) * FITW[c["best_fit"]] * weak_factor * strike

# greedy information-gain ordering (global)
covered = set()
order = []
remaining = clusters[:]
while remaining:
    best, best_score, best_nov = None, -1, 0
    for c in remaining:
        new = len(c["urls"] - covered)
        nov = new / max(len(c["urls"]), 1)               # novelty share 0..1
        score = c["value"] * (0.35 + 0.65*nov)           # value damped by redundancy
        if score > best_score:
            best, best_score, best_nov = c, score, nov
    order.append((best, best_nov, len(best["urls"] - covered)))
    covered |= best["urls"]
    remaining.remove(best)

# assemble library
lib = []
for rank, (c, nov, new_urls) in enumerate(order, start=1):
    pid, pname = PILLARS.get(c["theme"], ("P6","Operator & Industry Resources"))
    url = c["bca_url"]
    status = "existing"
    if not url:
        status = "new"
        url = "/post/" + slugify(c["parent"])
    lib.append({
        "ig_rank": rank, "pillar_id": pid, "pillar": pname,
        "entry": c["parent"], "size": c["size"], "volume": c["total_volume"],
        "fruits": c["fruits"], "bca_pos": c["bca_best_pos"], "fit": c["best_fit"],
        "novelty_pct": round(nov*100), "new_urls": new_urls,
        "status": status, "url": url, "members": c["members"],
    })

json.dump(lib, open(f"{SCRATCH}/serp/library.json","w"), indent=1)

# CSV
with open("/home/user/SEO/igaming/library.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["ig_rank","pillar","entry","keywords","volume","fruits","bca_pos","fit",
                "novelty_pct","status","target_url","members"])
    for e in lib:
        w.writerow([e["ig_rank"],e["pillar"],e["entry"],e["size"],e["volume"],e["fruits"],
                    e["bca_pos"],e["fit"],e["novelty_pct"],e["status"],e["url"]," | ".join(e["members"])])

# Markdown
by_pillar = defaultdict(list)
for e in lib: by_pillar[(e["pillar_id"], e["pillar"])].append(e)
md = ["# iGaming Advertising Content Library — Semantic Hierarchy & Publish Order",
"",
"**Built 2026-07-28.** Entries = SERP-cluster parents. Order inside each pillar and the global",
"IG rank both come from greedy information-gain selection: each next entry is the one adding the",
"most NEW top-10 SERP territory (URLs not covered by any earlier entry), weighted by",
"volume x fit x SERP weakness x strike-zone bonus. Novelty % = share of an entry's SERP",
"territory that was new when it was selected — low novelty means the topic is largely covered",
"by entries above it (write it later, or fold it into the earlier page).",
"",
"**Hub:** `/igaming-advertising` sits above every pillar as the commercial center; every entry links up to it.",
""]
for (pid, pname) in sorted(by_pillar):
    entries = sorted(by_pillar[(pid,pname)], key=lambda e: e["ig_rank"])
    tv = sum(e["volume"] for e in entries)
    md.append(f"## {pid} — {pname}  ({len(entries)} entries · {tv:,} combined volume)")
    md.append("")
    md.append("| IG# | Entry (head term) | Kws | Vol | 🍎 | BCA | Novelty | Status | Target URL |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for e in entries:
        md.append(f"| {e['ig_rank']} | **{e['entry']}** | {e['size']} | {e['volume']:,} | {e['fruits']} | "
                  f"{'#'+str(e['bca_pos']) if e['bca_pos'] else '—'} | {e['novelty_pct']}% | {e['status']} | `{e['url']}` |")
    md.append("")
top20 = sorted(lib, key=lambda e: e["ig_rank"])[:20]
md.append("## Global publish order — first 20 entries")
md.append("")
for e in top20:
    md.append(f"{e['ig_rank']}. **{e['entry']}** ({e['pillar_id']}, {e['size']} kws, {e['volume']:,} vol, "
              f"{e['novelty_pct']}% novel, {e['status']}) → `{e['url']}`")
open("/home/user/SEO/igaming/LIBRARY.md","w").write("\n".join(md))

print("entries:", len(lib))
for (pid,pname) in sorted(by_pillar):
    es = by_pillar[(pid,pname)]
    print(f"{pid} {pname}: {len(es)} entries, vol {sum(e['volume'] for e in es):,}")
print("\nGlobal IG order (top 15):")
for e in sorted(lib, key=lambda x:x['ig_rank'])[:15]:
    print(f"{e['ig_rank']:>3}. [{e['pillar_id']}] {e['entry']}  (vol {e['volume']:,}, nov {e['novelty_pct']}%, {e['status']}, {e['size']} kws)")
