#!/usr/bin/env python3
"""Prune the keyword universe to vertical B2B topics only.
Adds in_library + exclude_reason columns; nothing is deleted."""
import csv, re

PATH = "/home/user/SEO/igaming/keyword-universe.csv"
rows = list(csv.DictReader(open(PATH)))

VERTICAL = re.compile(r"igaming|gambl|casino|bett|sportsbook|sport bet|gaming vertical")

# Casino/tool brands: navigational intent to someone else's program or product
BRANDS = re.compile(r"chumba|bitstarz|stake casino|888 casino|jackpot city|crown coins|high 5|zula|"
                    r"ignition|europa casino|hidden jack|vodds|peakycasino|gamdom|affnook|solitics|"
                    r"cellxpert|netrefer|income access|theaffiliateplatform|mobivion|twinred|"
                    r"alfaleads|exoclick|trafficjunky|automatentest|affter |after gambling affiliate|"
                    r"gambling craft|shuffle gambling|live casino affiliate")

# Generic adtech with no vertical token — different audience
GENERIC = re.compile(r"popunder|pushads|push ads|pop ads|push notification|onclick|"
                     r"native advertising platform|programmatic advertising|self serve|"
                     r"^ad networks?( for advertisers)?$|^best ad networks$|^advertising network$|"
                     r"taboola|adroll")

# Other BCA verticals (crypto library, not iGaming) — unless crypto casino/gambling
CRYPTO = re.compile(r"crypto|bitcoin")
CRYPTO_VERT = re.compile(r"crypto casino|crypto gambling|bitcoin casino")

# Land-based / local / physical
LAND = re.compile(r"traffic counter|traffic monitoring|rohnert|everett|scent|print ad|print market|"
                  r"direct mail|flyer|bus marketing|indian casino|tribal|native american|"
                  r"native casino marketing|las vegas|santa ana|maryland live|harrah|mgm|wynn|"
                  r"mandalay|flamingo|mirage|ncl |new york new york|washita|grand casino|sdg |"
                  r"mendez|seminole|casino resort|loyalty market")

# Jobs / careers / events
JOBS = re.compile(r"\bjobs?\b|salary|salaries|conference|bootcamp|training|hired|hiring|"
                  r"\bmanager\b|coordinator|director|executive|remote italy|warsaw|poland")

# Consumer traffic-camera games & consumer queries
CONSUMER = re.compile(r"^traffic (betting|gambling|casino|game)|betting on traffic|gambling on traffic|"
                      r"traffic cam|traffic camera|traffic light|rush hour|free casino games|"
                      r"high traffic casino demo|stake traffic|traffic for gambling$|"
                      r"why (are|do|am)|i hate|should be (illegal|banned)|ban gambling|ban sports|"
                      r"how to (stop|block)|anti gambling|so many gambling")

def judge(k):
    if BRANDS.search(k): return "brand-navigational"
    if CONSUMER.search(k): return "consumer/off-topic"
    if LAND.search(k): return "land-based/local"
    if JOBS.search(k): return "jobs/events"
    if CRYPTO.search(k) and not CRYPTO_VERT.search(k): return "crypto vertical (separate library)"
    if GENERIC.search(k) and not VERTICAL.search(k): return "generic adtech (non-vertical)"
    if not VERTICAL.search(k):
        # non-vertical leftovers that aren't platform-conquest for gambling-native networks
        if re.search(r"adsterra|propellerads|hilltopads|richads|clickadu", k): return None
        return "no vertical tie"
    return None

out = []
excluded = {}
for r in rows:
    reason = judge(r["keyword"])
    r["in_library"] = "no" if reason else "yes"
    r["exclude_reason"] = reason or ""
    if reason: excluded.setdefault(reason, []).append(r["keyword"])
    out.append(r)

fields = list(out[0].keys())
with open(PATH, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(out)

kept = sum(1 for r in out if r["in_library"]=="yes")
print(f"kept {kept} / {len(out)}")
for reason, kws in sorted(excluded.items()):
    print(f"\n[{reason}] ({len(kws)})")
    print("  " + ", ".join(sorted(kws)))
