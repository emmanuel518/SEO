#!/usr/bin/env python3
"""LowFruits-style SERP clustering for the BCA iGaming keyword universe.
Clusters = keywords whose top-10 SERPs share >= SHARED_MIN URLs (union-find).
Weak spots = forum/UGC/social results or low-DR domains in the top 10.
"""
import csv, json, glob, sys
from collections import defaultdict

SCRATCH = "/tmp/claude-0/-home-user-SEO/902ba0b1-362e-51aa-be60-e911903115d7/scratchpad"
SHARED_MIN = 3

# UGC / forum / social domains = automatic weak spots (LowFruits' "fruits")
UGC = ("reddit.com","quora.com","youtube.com","linkedin.com","medium.com","x.com","twitter.com",
       "facebook.com","instagram.com","pinterest.com","blackhatworld.com","stackexchange.com",
       "afflift.com","stmforum.com","warriorforum.com","tiktok.com","wikipedia.org")

def norm_url(u):
    u = u.split("#")[0].split("?")[0].rstrip("/")
    return u.replace("https://","").replace("http://","").replace("www.","").lower()

def root_domain(d):
    d = d.replace("www.","").lower()
    parts = d.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else d

# ---- load SERPs
serps = {}
for f in glob.glob(f"{SCRATCH}/serp/slice*.jsonl"):
    for line in open(f):
        line = line.strip()
        if not line: continue
        try: rec = json.loads(line)
        except json.JSONDecodeError: continue
        if rec.get("serp"):
            serps[rec["kw"]] = [{"pos":i.get("pos"),"url":norm_url(i["url"]),"domain":root_domain(i.get("domain") or i["url"].split("/")[2])}
                                for i in rec["serp"][:10] if i.get("url")]
print(f"SERPs loaded: {len(serps)}", file=sys.stderr)

# ---- load universe metadata
meta = {}
for r in csv.DictReader(open("/home/user/SEO/igaming/keyword-universe.csv")):
    bv = max(int(float(r["vol_ahrefs"] or 0)), int(float(r["vol_googleads"] or 0)))
    meta[r["keyword"]] = {"bv":bv,"cluster_t":r["cluster"],"fit":r["bca_fit"],"vertical":r["vertical"],
                          "cpc":float(r["cpc_usd"]) if r["cpc_usd"] else None,
                          "kd":int(float(r["kd"])) if r["kd"] else None,
                          "pos":round(float(r["bca_pos"])) if r["bca_pos"] else None,
                          "url":r["bca_url"] or None}

# ---- DR map (filled by enrichment step; optional on first pass)
try:
    DR = json.load(open(f"{SCRATCH}/serp/domain_dr.json"))
except FileNotFoundError:
    DR = {}

# ---- parent-anchored clustering (soft mode): a keyword joins the cluster whose
# PARENT shares >= SHARED_MIN top-10 URLs with it; best overlap wins. No chaining.
kws = sorted([k for k in serps if k in meta], key=lambda k: -meta[k]["bv"])
urlsets = {k:{i["url"] for i in serps[k]} for k in kws}
parents = []          # cluster parents in volume order
assign = {}           # kw -> parent
for k in kws:
    best, best_ov = None, 0
    for p in parents:
        ov = len(urlsets[k] & urlsets[p])
        if ov >= SHARED_MIN and ov > best_ov:
            best, best_ov = p, ov
    if best is None:
        parents.append(k); assign[k] = k
    else:
        assign[k] = best

groups = defaultdict(list)
for k in kws: groups[assign[k]].append(k)

# ---- weak-spot scoring per keyword
def weakness(k):
    fruits, notes = 0, []
    for item in serps[k]:
        d = item["domain"]
        if any(d == u or d.endswith("."+u) for u in UGC):
            fruits += 1; notes.append(f"{d}@{item['pos']}")
        elif d in DR and DR[d] is not None and DR[d] <= 25:
            fruits += 1; notes.append(f"{d}(DR{DR[d]})@{item['pos']}")
    return fruits, notes

# ---- build cluster records
clusters = []
for members in groups.values():
    members.sort(key=lambda k: -meta[k]["bv"])
    par = members[0]
    vol = sum(meta[k]["bv"] for k in members)
    fr_total = 0; fruit_notes = []
    bca_best = None; bca_url = None
    kds = [meta[k]["kd"] for k in members if meta[k]["kd"] is not None]
    for k in members:
        fr, notes = weakness(k)
        fr_total += fr
        fruit_notes += notes
        p = meta[k]["pos"]
        if p is not None and (bca_best is None or p < bca_best):
            bca_best, bca_url = p, meta[k]["url"]
    # dominant thematic cluster label
    from collections import Counter
    theme = Counter(meta[k]["cluster_t"] for k in members).most_common(1)[0][0]
    fit = min(members, key=lambda k: {"Core":0,"High":1,"Medium":2,"Low":3}[meta[k]["fit"]])
    clusters.append({
        "parent": par, "size": len(members), "members": members,
        "total_volume": vol, "avg_kd": round(sum(kds)/len(kds)) if kds else None,
        "fruits": fr_total, "fruit_notes": sorted(set(fruit_notes))[:8],
        "theme": theme, "best_fit": meta[fit]["fit"],
        "bca_best_pos": bca_best, "bca_url": bca_url,
    })
clusters.sort(key=lambda c: (-c["total_volume"], -c["size"]))

json.dump(clusters, open(f"{SCRATCH}/serp/clusters.json","w"), indent=1)
print(f"clusters: {len(clusters)} | multi-keyword: {sum(1 for c in clusters if c['size']>1)} "
      f"| singletons: {sum(1 for c in clusters if c['size']==1)}", file=sys.stderr)
for c in clusters[:15]:
    print(f"[{c['size']:>2} kws | vol {c['total_volume']:>5} | fruits {c['fruits']:>2} | "
          f"BCA {('#'+str(c['bca_best_pos'])) if c['bca_best_pos'] else '—':>4}] {c['parent']}"
          + (f"  (+ {', '.join(c['members'][1:4])}…)" if c['size']>1 else ""), file=sys.stderr)

# unique domains needing DR (for enrichment step)
doms = sorted({i["domain"] for k in kws for i in serps[k] if not any(i["domain"]==u or i["domain"].endswith("."+u) for u in UGC)})
open(f"{SCRATCH}/serp/domains_needed.json","w").write(json.dumps(doms))
print(f"unique non-UGC domains: {len(doms)} (DR known: {sum(1 for d in doms if d in DR)})", file=sys.stderr)
