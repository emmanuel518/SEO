#!/usr/bin/env python3
"""Build the iGaming advertising keyword universe workbook for Blockchain-Ads.
Data pulled 2026-07-28 from Ahrefs (matching terms + competitor organic), DataForSEO
(Google Ads volumes, live SERPs) and GSC (last 28 days). CPCs in USD.
"""
import csv, re, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------- raw data
# (keyword, ahrefs_volume, cpc_usd_or_None, difficulty_or_None, source)
A = []  # ahrefs matching-terms + competitor rows

def add(rows, src):
    for r in rows:
        kw, vol, cpc, diff = r
        A.append((kw.strip().lower(), vol, cpc, diff, src))

# --- Ahrefs matching terms: iGaming vertical (junk rows dropped: jobs, salaries, conference logistics)
add([
("igaming marketing",700,7.00,15),("igaming affiliate marketing platform",500,None,47),
("igaming affiliate software",400,8.00,48),("igaming affiliate marketing software",350,None,50),
("igaming affiliate marketing system",300,None,35),("igaming marketing agency",300,12.00,0),
("igaming affiliate marketing",300,16.00,19),("igaming affiliate system",250,None,51),
("igaming affiliate management software",250,None,29),("igaming affiliate platform",250,None,51),
("igaming affiliate management service",200,None,38),("igaming digital marketing",200,None,21),
("igaming ads",200,None,12),("igaming content marketing",200,None,1),
("igaming crm marketing solutions",150,None,None),("igaming affiliate program",150,1.50,41),
("igaming crm marketing tools",150,None,None),("igaming traffic provider",150,None,None),
("igaming affiliate",150,1.00,10),("igaming affiliate programs",150,1.50,54),
("affiliate igaming",150,None,None),("igaming affiliate news",150,None,12),
("igaming affiliate network",150,None,None),("igaming affiliate list",150,None,None),
("best igaming affiliate software",150,None,9),("affiliate marketing software for igaming",150,None,39),
("affiliate marketing igaming",150,None,20),("igaming digital marketing agency",100,None,24),
("personalized marketing for igaming",100,None,None),("igaming advertising",100,None,None),
("igaming affiliate program software",100,None,23),("crm marketing for igaming",100,None,None),
("igaming affiliate marketing programs",90,None,None),("affiliate tracking software for igaming",90,None,24),
("igaming affiliate management",90,None,37),("marketing automation igaming",90,None,None),
("marketing igaming",80,None,None),("igaming marketing automation",70,None,None),
("igaming traffic purchase online advertising",70,None,None),("igaming marketing services",70,None,28),
("best igaming affiliate programs",60,None,58),("igaming affiliate management platform",60,None,39),
("best practices for igaming ads",60,None,None),("igaming affiliate marketing agency",60,None,None),
("igaming marketing software",60,None,None),("igaming ads networks",50,None,None),
("igaming affiliate management system",50,None,None),("best igaming ads networks",50,None,None),
("igaming google ads",40,None,None),("igaming marketing company",40,None,40),
("igaming affiliate companies",40,None,None),("igaming affiliate networks",40,None,61),
("igaming marketing strategies",40,None,0),("buy igaming traffic",40,None,None),
("what is igaming affiliate marketing",30,None,21),("igaming influencer marketing",30,None,0),
("igaming growth marketing agency",30,None,0),("igaming affiliate management agency",30,None,44),
("igaming traffic for affiliates",30,None,None),("igaming marketing guide",30,None,0),
("igaming content marketing agency",30,None,0),("igaming ad network",30,None,None),
("igaming affiliate roas benchmarks",30,None,None),("igaming affiliate marketing consulting",30,None,None),
("top traffic sources igaming",20,None,None),("revshare for igaming affiliate programs",20,None,None),
("igaming marketing agencies",20,None,None),("igaming digital marketing services",20,None,14),
("igaming social media marketing",20,None,0),("igaming affiliate cpa rates",10,None,None),
("igaming affiliate revenue share commission rates",10,None,None),("quality traffic igaming offers",10,None,None),
("best igaming affiliate programs 2026",10,None,None),("igaming affiliate fraud",10,None,4),
("performance marketing igaming",10,None,6),("igaming traffic sources",10,None,22),
("media buying igaming",10,None,None),("igaming affiliate cpa per ftd range",10,None,None),
("igaming affiliate networks list",10,None,None),("igaming advertising trends 2026",10,None,None),
("igaming online advertising",10,None,None),("white label igaming affiliate platform",10,None,11),
("igaming affiliate tracking platforms",10,None,None),("igaming marketing crm",10,None,None),
("igaming marketing attribution platform",10,None,None),("igaming event marketing agency",10,None,None),
], "ahrefs_mt_igaming")

# --- Ahrefs matching terms: gambling vertical (consumer/anti-gambling + block-ads rows dropped)
add([
("gambling advertising",250,4.50,58),("gambling ads",250,9.00,53),
("google ads gambling policy news",200,None,None),("gambling affiliate program",200,None,65),
("online gambling affiliate marketing",200,None,51),("gambling advertising news",200,None,None),
("gambling marketing",150,None,45),("gambling affiliate marketing platform",150,None,60),
("gambling affiliate marketing",150,None,51),("affiliate marketing gambling",150,None,48),
("gambling affiliate marketing software",150,None,61),("buy gambling traffic",150,None,None),
("gambling marketing agency",150,None,52),("google ads gambling",100,None,32),
("gambling advertising regulations",100,None,61),("gambling affiliate marketing system",100,None,59),
("sports gambling ads",90,None,None),("online gambling ads",90,4.00,None),
("google ads gambling policy",90,None,60),("sports gambling advertising",90,None,None),
("affiliate gambling program",80,None,None),("ads for gambling",80,None,None),
("google ads gambling policy update",70,None,None),("meta ads policy gambling news",70,None,None),
("best gambling affiliate program",60,None,None),("affiliate program gambling",60,None,None),
("can you advertise gambling on google",60,None,None),("gambling traffic sources",60,None,None),
("google ads gambling and games policy",50,None,None),("online gambling marketing",50,None,56),
("traffic gambling",50,None,None),("gambling ads traffic",50,None,None),
("advertising for gambling",40,None,None),("gambling influencer marketing",40,None,None),
("tiktok advertising policy gambling",40,None,None),("advertise gambling",40,None,None),
("email marketing for casino and gambling industry",40,None,42),("revshare gambling affiliate program",40,None,25),
("affiliate gambling marketing",40,None,None),("gambling ad network",40,None,None),
("responsible gambling advertising",40,None,None),("affiliate marketing for gambling",30,None,None),
("gambling affiliate traffic",30,None,None),("gambling advertising network",30,None,29),
("gambling digital ads",30,None,None),("affiliate marketing software for gambling",30,None,58),
("email marketing for gambling",30,None,54),("gambling advertising regulations united states",30,None,None),
("google ads gambling certification",30,None,None),("gambling digital marketing agency",30,None,62),
("gambling and casino marketing agencies",30,None,None),("social media marketing for gambling",30,None,None),
("online gambling advertising",30,1.60,53),("facebook gambling ads",20,None,52),
("how to advertise gambling",20,None,None),("creative gambling ads",20,None,None),
("gambling traffic",20,None,11),("gambling push ads",20,None,None),
("sports gambling affiliate marketing",20,None,None),("online gambling marketing solution",20,None,None),
("best gambling ads",20,None,None),("gambling digital marketing",20,None,None),
("gambling creatives",20,None,None),("online gambling certificate google ads",20,None,None),
("compliant gambling advertising",20,None,None),("facebook gambling ads policy",20,None,None),
("gambling advertising examples",20,None,None),("advertise gambling pop sources online",20,None,None),
("gambling advertising rules",10,None,None),("online gambling affiliate program",10,1.60,None),
("guide to compliant gambling advertising",10,None,None),("google ads gambling certification apply",10,None,None),
("online gambling marketing strategy",10,None,None),("google ads gambling license",10,None,None),
("gambling ads examples",10,None,None),("microsoft advertising gambling policy",10,None,None),
("taboola advertising policy gambling",10,None,None),("google ads online gambling allowed countries",10,None,None),
], "ahrefs_mt_gambling")

# --- Ahrefs matching terms: casino vertical (land-based brand/phone/job rows dropped)
add([
("casino marketing",350,None,47),("casino affiliate program",300,3.50,61),
("casino marketing ideas",200,None,55),("casino affiliate marketing software",200,None,62),
("casino advertising strategies",200,None,53),("casino advertising",200,4.50,39),
("affiliate casino program",200,3.50,68),("casino affiliate marketing system",200,None,48),
("casino digital marketing",150,None,47),("online casino affiliate marketing",150,4.00,44),
("online casino marketing strategy",150,None,55),("casino marketing agency",150,None,53),
("casino marketing plan",150,None,60),("casino affiliate marketing platform",150,None,66),
("casino affiliate marketing",150,None,35),("online casino ads",150,4.00,38),
("casino ads",150,5.00,39),("casino advertising campaign",150,None,56),
("casino digital marketing agency",150,None,53),("online casino marketing",150,None,57),
("online casino affiliate program",100,7.00,67),("affiliate program casino",100,2.50,60),
("affiliate marketing software for casino",100,None,55),("promote online casino",100,4.00,None),
("online casino advertising",100,4.00,61),("casino traffic",100,19.00,32),
("casino marketing software",100,None,71),("promote casino",100,None,None),
("affiliate marketing casino",90,None,None),("online casino marketing agency",90,None,61),
("top casino affiliate program",90,None,None),("seo casino marketing",90,None,65),
("chumba casino affiliate program",80,2.50,60),("how to promote a casino website",80,None,None),
("casino marketing strategy",80,None,59),("how to promote online casino",80,None,None),
("best casino ads",70,None,None),("best casino affiliate marketing software",60,None,None),
("crypto casino affiliate program",60,None,None),("online casino digital marketing",50,None,None),
("casino advertising agency",50,None,58),("live casino affiliate program",50,None,None),
("affiliate program online casino",50,None,None),("crypto casino traffic",50,None,24),
("best casino affiliate program",50,None,55),("casino affiliate program software",50,None,None),
("casino seo marketing services",50,None,None),("casino advertising examples",50,None,39),
("bitcoin casino affiliate program",40,None,None),("online casino marketing strategies",40,None,None),
("online casino advertising networks for publishers",40,None,None),("casino loyalty marketing",40,None,None),
("performance marketing casino",40,None,None),("best online casino affiliate program",40,1.90,None),
("casino player acquisition",40,None,None),("buy casino traffic",30,None,49),
("crypto casino marketing",30,None,None),("casino marketing services",30,None,39),
("casino media buying",30,None,0),("casino affiliate advertising",30,None,49),
("casino influencer marketing",30,None,None),("casino marketing strategies",30,None,None),
("bitstarz casino affiliate program",30,None,0),("best practices for casino ads",30,None,None),
("crypto casino ads",30,None,None),("sweepstakes casino marketing",30,None,24),
("affiliate casino traffic tools",30,None,42),("social casino google ads",20,None,None),
("casino marketing consulting",20,None,41),("white label casino affiliate program",20,None,61),
("casino advertising channels",20,None,None),("casino affiliate marketing tools",20,None,None),
("stake casino affiliate program",20,None,None),("google ads casino policy",20,None,None),
("sweepstakes casino affiliate program",20,None,None),("casino ads examples",20,None,None),
("best practices for casino player acquisition",20,None,36),("casino email marketing",20,None,None),
("casino push ads",20,None,None),("casino facebook ads",20,None,None),
("casino content marketing",20,None,None),("casino pay per click marketing",20,None,None),
("converting casino traffic into players",20,None,12),("casino game ads",20,None,None),
("casino ads traffic",20,None,None),("online casino traffic",10,None,None),
("casino affiliate program cpa",10,None,None),("crypto casino marketing agency",10,None,24),
("crypto casino marketing strategies",10,None,None),("guide to casino affiliate marketing",10,None,None),
("casino google ads",10,None,None),("facebook casino ads",10,None,None),
("social casino certificate google ads",10,None,None),("creative casino ads",10,None,None),
("casino ads on facebook",10,None,None),("online casino marketing funnel",10,None,0),
("social casino affiliate program",10,None,None),("casino online marketing",10,None,None),
("888 casino affiliate program",10,None,None),("casino sms marketing",10,None,None),
], "ahrefs_mt_casino")

# --- Ahrefs matching terms: betting/sportsbook vertical (traffic-camera game rows dropped)
add([
("sports betting advertising",250,12.00,22),("sportsbook marketing services",250,None,4),
("sports betting marketing strategies",200,None,56),("online sportsbook marketing",200,None,16),
("sports betting ads",200,6.00,13),("betting ads",150,6.00,33),
("sports betting marketing",150,None,45),("sports betting affiliate marketing",100,None,46),
("betting company marketing agency",100,None,60),("betting affiliate program",100,None,53),
("sports betting affiliate program",100,7.00,51),("online betting marketing agency",100,None,57),
("affiliate marketing sports betting",80,None,43),("sportsbook marketing",70,None,38),
("sports betting advertising regulation",70,None,24),("online betting marketing strategy",70,None,59),
("betting traffic",70,None,None),("sportsbook digital marketing",70,None,5),
("sportsbook advertising",60,5.00,19),("sports betting marketing agency",60,None,39),
("sport betting affiliate program",60,3.50,None),("online betting ads",50,None,None),
("betting marketing agency",50,None,61),("betting affiliate marketing software",40,None,54),
("affiliate marketing software for sportsbook",40,None,1),("affiliate marketing software for betting",40,None,45),
("betting marketing",30,None,50),("sportsbook marketing solutions",30,None,None),
("sports betting ads examples",30,None,None),("betting affiliate marketing system",30,None,46),
("advertising sports betting",30,None,None),("betting digital marketing",30,None,None),
("sports betting traffic",20,None,None),("betting traffic sources",20,None,17),
("sports betting affiliate traffic",20,None,None),("marketing agency for sports betting",20,None,None),
("social media marketing for betting",20,None,None),("online betting affiliate program",20,1.60,None),
("sportsbook digital marketing agency",20,None,None),("esports betting marketing",20,None,None),
("how to run ads for betting app",20,None,None),("betting affiliate marketing",10,None,57),
("pop-under traffic for betting campaigns",10,None,None),("sportsbook marketing agency",10,None,None),
("betting push ads",10,None,None),("digital marketing for betting sites",10,None,None),
("betting ad network",10,None,21),("betting email marketing services",10,None,None),
("sports betting traffic sources",10,None,None),("sports betting email marketing",10,None,None),
("us sports betting advertising spend 2023",10,None,None),
], "ahrefs_mt_betting")

# --- Ahrefs competitor organic: richads.com (consumer casino-shopping rows dropped)
add([
("best casino affiliate programs",3100,4.34,67),("igaming affiliate marketing platform",600,None,47),
("igaming marketing",500,12.25,15),("igaming affiliate software",450,7.52,48),
("igaming affiliate platform",350,None,51),("how to start a online casino business",350,1.43,56),
("how to start an online casino",300,10.62,56),("casino affiliate programs",300,0.09,66),
("gambling ads",200,9.26,53),("casino affiliate programme",200,None,58),
("affiliate casino programs",200,None,68),("gambling affiliate programs",200,None,52),
("casino advertising",200,4.49,39),("casino affiliate",200,4.75,68),
("online gambling affiliate marketing",200,None,51),("online casino affiliates",200,4.06,64),
("best gambling affiliate programs",150,None,47),("sports betting affiliate programs",150,6.98,54),
("casino affiliates",150,5.85,56),("betting affiliate program",150,None,53),
("online casino ads",150,2.86,38),("igaming definition",150,None,61),
("betting affiliate",150,None,0),("casino advertising campaign",150,None,56),
("igaming affiliate",150,1.03,21),("casino ads",150,5.07,39),
("how to start an online gambling business",100,1.58,48),("igaming affiliate marketing",100,16.39,20),
("gambling affiliate",100,8.19,53),("online casino affiliate marketing",100,3.85,43),
("best casino affiliate program",100,None,55),("affiliate gambling",100,None,60),
("casino affiliate system",100,None,62),("casino affiliate marketing",100,None,41),
("sportsbook affiliate program",100,2.24,34),("gambling affiliate program",100,None,65),
("sportsbook affiliate programs",100,1.17,42),("igaming trends",90,None,7),
("gambling affiliate marketing",90,None,51),("sports betting affiliate marketing",90,None,47),
("sports betting affiliates",90,5.70,53),("casino ad",90,7.46,21),
("online casino advertising",90,3.86,61),("online casino affiliate",80,3.85,66),
("online casino affiliate programs",80,4.02,61),("online gambling affiliate",80,None,35),
("white label igaming",70,None,None),("igaming meaning",200,None,51),
], "ahrefs_comp_richads")

# --- Ahrefs competitor organic: hilltopads.com
add([
("igaming seo agency",1000,4.50,40),("igaming marketing agency",400,12.48,0),
("igaming digital marketing",300,None,21),("igaming digital agency",150,None,13),
("igaming digital marketing agency",150,None,24),("igaming agency",100,None,16),
], "ahrefs_comp_hilltopads")

# --- DataForSEO Google Ads volumes (separate volume column on merge)
G = [
("sportsbook marketing",6600,21.85),("popunder ads",2900,33.15),
("programmatic advertising platform",1300,53.06),("ad networks for advertisers",1000,24.50),
("sports betting advertising",1000,None),("native advertising platform",880,27.45),
("gambling ads",720,17.94),("gambling advertising",720,17.94),
("self serve ad platform",720,314.98),("casino advertising",390,45.28),
("casino ads",390,45.28),("igaming seo",390,7.69),
("best ad networks",260,4.31),("igaming traffic",260,53.68),
("buy gambling traffic",110,None),("crypto ad network",110,None),
("self serve dsp",110,258.51),("betting advertising",90,20.04),
("betting ads",90,20.04),("igaming marketing",70,9.90),
("online casino advertising",70,3.87),("igaming affiliate marketing",70,13.46),
("gambling traffic",70,None),("push notification ads",50,83.26),
("igaming marketing agency",50,15.10),("casino marketing agency",50,None),
("casino marketing strategies",50,None),("push ads network",50,None),
("igaming advertising",40,None),("casino affiliate marketing",40,None),
("crypto advertising platform",40,None),("adsterra alternative",30,16.60),
("best crypto ad network",30,None),("gambling marketing agency",30,None),
("casino digital marketing",30,None),("online gambling advertising",30,None),
("gambling ad network",20,None),("igaming ppc",20,None),
("pop ads network",20,None),("promote online casino",20,None),
("taboola alternatives",10,105.99),("adroll alternatives",10,58.78),
("hilltopads alternative",10,48.43),("propellerads alternative",10,None),
("buy casino traffic",10,None),
]

# --- Blockchain-Ads current best known position (GSC 28d avg or DFS index or live SERP)
BCA = {
"sports betting ads":(11,"/post/igaming-ad-examples","DFS index"),
"casino advertisements":(11,"/post/gambling-advertising","DFS index"),
"gaming verticals":(12,"/post/igaming-vertical","DFS index"),
"gambling advert":(13,"/post/igaming-ad-examples","DFS index"),
"casino ads on facebook":(13,"/post/advertising-online-gambling-on-facebook","DFS index"),
"affiliate program casino":(13,"/post/casino-affiliate-marketing","DFS index"),
"ads for gambling":(14,"/post/igaming-ad-examples","DFS index"),
"igaming marketing agency":(14,"/post/igaming-marketing-agency","live SERP 07-28"),
"buy casino traffic":(14,"/post/top-gambling-ad-networks","GSC 28d"),
"online casino marketing agency":(15,"/post/igaming-marketing-agency","GSC 28d"),
"casino affiliate programs":(16,"/post/casino-affiliate-marketing","GSC 28d"),
"a d casino":(16,"/post/top-gambling-ad-networks","DFS index"),
"igaming ads":(16,"/post/igaming-ad-examples","GSC 28d"),
"betting marketing agency":(16,"/post/igaming-marketing-agency","GSC 28d"),
"gambling ad network":(17,"/post/top-gambling-ad-networks","GSC 28d"),
"casino ad":(18,"/post/casino-advertising-examples","DFS index"),
"casino advertising":(19,"/post/casino-advertising-examples","GSC 28d"),
"igaming ad network":(9,"/post/top-gambling-ad-networks","live SERP 07-28"),
"best igaming ads networks":(4,"/post/top-gambling-ad-networks","GSC 28d"),
"casino affiliate marketing":(20,"/post/casino-affiliate-marketing","GSC 28d"),
"casino digital marketing agency":(20,"/post/igaming-marketing-agency","GSC 28d"),
"casino marketing agency":(22,"/post/igaming-marketing-agency","GSC 28d"),
"buy gambling traffic":(22,"/post/top-gambling-ad-networks","live SERP 07-28"),
"gambling ad networks":(24,"/post/top-gambling-ad-networks","GSC 28d"),
"gambling ads":(25,"/post/igaming-ad-examples","DFS index"),
"casino ads":(26,"/post/igaming-ad-examples","DFS index"),
"casino affiliate program":(26,"/post/casino-affiliate-marketing","DFS index"),
"buy igaming traffic":(47,"/post/top-gambling-ad-networks","GSC 28d"),
"igaming business":(27,"/post/igaming-vertical","DFS index"),
"what is igaming":(30,"/post/igaming-vertical","DFS index"),
"how to monetize website":(30,"/post/monetize-website","DFS index"),
"casino marketing":(18,"/post/casino-marketing-strategies","GSC 28d"),
"casino digital marketing":(26,"/post/casino-marketing-strategies","GSC 28d"),
"affiliate marketing gambling":(13,"/post/casino-affiliate-marketing","GSC 28d"),
"google ads gambling policy":(7,"/post/gambling-ads-google-policy","GSC 28d"),
"sports betting advertising":(43,"/post/igaming-ad-examples","DFS index"),
"gambling advertising":(42,"/post/igaming-ad-examples","DFS index"),
"casino advert":(42,"/post/casino-advertising-examples","DFS index"),
"casino marketing strategies":(18,"/post/casino-marketing-strategies","GSC 28d"),
"igaming":(26,"/post/igaming-vertical","GSC 28d"),
"crypto casino affiliate program":(13,"/post/casino-affiliate-marketing","GSC 28d"),
"gambling advertising examples":(10,"/post/gambling-advertising","GSC 28d"),
"igaming advertising":(13,"/post/igaming-ad-examples","live SERP 07-28"),
}

# ---------------------------------------------------------------- merge & classify
merged = {}
for kw, vol, cpc, diff, src in A:
    e = merged.setdefault(kw, {"kw":kw,"vol_a":None,"vol_g":None,"cpc":None,"diff":None,"src":set()})
    e["vol_a"] = max(e["vol_a"] or 0, vol or 0)
    if cpc: e["cpc"] = max(e["cpc"] or 0, cpc)
    if diff is not None: e["diff"] = diff if e["diff"] is None else max(e["diff"], diff)
    e["src"].add(src)
for kw, vol, cpc in G:
    e = merged.setdefault(kw, {"kw":kw,"vol_a":None,"vol_g":None,"cpc":None,"diff":None,"src":set()})
    e["vol_g"] = vol
    if cpc: e["cpc"] = max(e["cpc"] or 0, cpc)
    e["src"].add("dfs_googleads")

def classify(kw):
    k = kw
    def any_in(*words): return any(w in k for w in words)
    # cluster
    if any_in("policy","certification","certificate","regulation","rules","compliant","license",
              "can you advertise","is it legal","allowed countries","responsible"):
        cl = "Compliance & platform policy"
    elif any_in("alternative"):
        cl = "Competitor alternatives"
    elif any_in("ad network","ads networks","advertising network","dsp","self serve","programmatic",
                "native advertising platform","push ads","push notification","pop ads","popunder",
                "pop-under","ad networks"):
        cl = "Ad network / platform"
    elif any_in("traffic","media buying"):
        cl = "Traffic buying"
    elif any_in("affiliate software","affiliate platform","affiliate management","affiliate tracking",
                "tracking software","affiliate program software","affiliate marketing software",
                "affiliate marketing platform","affiliate marketing system","affiliate system",
                "white label","affiliate app","affiliate script","affiliate crm"):
        cl = "Affiliate B2B software"
    elif any_in("affiliate"):
        cl = "Affiliate programs & marketing"
    elif any_in("agency","agencies","consulting","services","company","companies","specialists","solutions"):
        cl = "Agency-intent capture"
    elif any_in("examples","creative","best casino ads","best gambling ads","best betting ads"):
        cl = "Ad examples & creatives"
    elif any_in("how to start","start a","start an","start online","open a","create online","create an"):
        cl = "Operator setup"
    elif any_in("advertis","ads","promote","promotion"):
        cl = "Advertising (general)"
    elif any_in("marketing","seo","ppc","acquisition","crm","email","influencer","automation","attribution"):
        cl = "Marketing strategy & guides"
    else:
        cl = "Vertical general"
    # audience
    if cl in ("Ad network / platform","Traffic buying","Competitor alternatives","Ad examples & creatives",
              "Advertising (general)","Compliance & platform policy","Agency-intent capture"):
        aud = "Advertiser / media buyer"
    elif cl == "Affiliate programs & marketing":
        aud = "Affiliate (media buyer)"
    elif cl == "Affiliate B2B software":
        aud = "Operator (B2B tooling)"
    elif cl in ("Operator setup","Marketing strategy & guides","Vertical general"):
        aud = "Operator"
    else:
        aud = "Mixed"
    # BCA fit
    fit = {"Ad network / platform":"Core","Traffic buying":"Core","Competitor alternatives":"Core",
           "Advertising (general)":"Core","Agency-intent capture":"High","Compliance & platform policy":"High",
           "Ad examples & creatives":"High","Affiliate programs & marketing":"Medium",
           "Marketing strategy & guides":"Medium","Operator setup":"Medium",
           "Vertical general":"Low","Affiliate B2B software":"Low"}[cl]
    return cl, aud, fit

def vertical(kw):
    for v, words in [("iGaming",("igaming",)),("Casino",("casino",)),
                     ("Betting",("betting","sportsbook","sport betting")),
                     ("Gambling",("gambling",))]:
        if any(w in kw for w in words): return v
    return "Cross-vertical"

rows = []
for e in merged.values():
    cl, aud, fit = classify(e["kw"])
    pos, url, psrc = BCA.get(e["kw"], (None,None,None))
    rows.append({"kw":e["kw"],"vertical":vertical(e["kw"]),"cluster":cl,"aud":aud,"fit":fit,
                 "vol_a":e["vol_a"],"vol_g":e["vol_g"],"cpc":e["cpc"],"diff":e["diff"],
                 "pos":pos,"url":url,"psrc":psrc,"src":", ".join(sorted(e["src"]))})

fit_rank = {"Core":0,"High":1,"Medium":2,"Low":3}
rows.sort(key=lambda r:(fit_rank[r["fit"]], -max(r["vol_a"] or 0, r["vol_g"] or 0)))

# ---------------------------------------------------------------- workbook
wb = Workbook()
F = "Arial"
def style_header(ws, ncols, row=1):
    for c in range(1, ncols+1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(name=F, bold=True, color="FFFFFF", size=10)
        cell.fill = PatternFill("solid", fgColor="1F3864")
        cell.alignment = Alignment(vertical="center", wrap_text=True)

# --- README
ws = wb.active; ws.title = "README"
readme = [
["Blockchain-Ads — iGaming Advertising Keyword Universe"],
["Built: 2026-07-28 | Market: US | Sources: Ahrefs Keywords Explorer (matching terms, 4 vertical sweeps), Ahrefs competitor organic keywords (richads.com, hilltopads.com), DataForSEO Google Ads volumes, GSC last 28 days, live SERP checks."],
[""],
["How to read this workbook"],
["Universe tab = every deduplicated keyword in the iGaming/gambling/casino/betting advertising ecosystem, classified. Sorted by BCA Fit then volume."],
["Priority Score (column L) = MAX(Ahrefs vol, Google Ads vol) x Fit weight (table below). Live formula - opens computed in Excel/Google Sheets; edit weights to re-score."],
["Clusters tab = formula-driven rollup by cluster. Page Map tab = which BCA URL should own each cluster."],
[""],
["Fit weights (edit to re-score)"],
["Fit","Weight","Meaning"],
["Core",1.0,"Buyer looking for a place to spend ad budget - our product SERPs"],
["High",0.7,"Adjacent commercial/compliance intent that converts to platform demand"],
["Medium",0.4,"ICP-adjacent (affiliates & operators researching) - content play"],
["Low",0.1,"Ecosystem context, B2B tooling we don't sell, or thin relevance"],
[""],
["Notes"],
["CPC in USD. Ahrefs difficulty 0-100. Volumes differ by source; both kept. BCA position = best known (GSC 28d avg, DFS index, or live SERP 2026-07-28)."],
["Excluded during collection: consumer casino-shopping queries, anti-gambling sentiment, block-ads queries, traffic-camera betting games, jobs/salaries, land-based casino brand queries."],
["Google Ads volumes for niche B2B terms often read low (10-110) while spiking months hit 590-2400 (igaming traffic, buy gambling traffic, self serve ad platform). Check trend before dismissing a keyword."],
]
for r in readme: ws.append(r)
for row in (1,4,9,16):
    ws.cell(row=row, column=1).font = Font(name=F, bold=True, size=12 if row==1 else 11)
style_header(ws, 3, row=10)
for r in range(11,15):
    for c in range(1,4): ws.cell(row=r, column=c).font = Font(name=F, size=10)
    ws.cell(row=r, column=2).font = Font(name=F, size=10, color="0000FF")
ws.column_dimensions["A"].width = 28; ws.column_dimensions["B"].width = 10; ws.column_dimensions["C"].width = 70
for r in (2,5,6,7,17,18,19):
    ws.cell(row=r, column=1).font = Font(name=F, size=9)
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)

# --- Universe
ws = wb.create_sheet("Universe")
hdr = ["Keyword","Vertical","Cluster","Audience","BCA Fit","Vol (Ahrefs)","Vol (Google Ads)",
       "CPC $","KD","BCA Pos","BCA URL","Priority Score","Pos Source","Data Sources"]
ws.append(hdr); style_header(ws, len(hdr))
for i, r in enumerate(rows, start=2):
    ws.append([r["kw"],r["vertical"],r["cluster"],r["aud"],r["fit"],r["vol_a"],r["vol_g"],
               r["cpc"],r["diff"],r["pos"],r["url"],
               f'=ROUND(MAX(0,F{i},G{i})*INDEX(README!$B$11:$B$14,MATCH(E{i},README!$A$11:$A$14,0)),0)',
               r["psrc"],r["src"]])
for i in range(2, len(rows)+2):
    for c in range(1, len(hdr)+1):
        cell = ws.cell(row=i, column=c); cell.font = Font(name=F, size=9)
    ws.cell(row=i, column=8).number_format = '0.00'
    fitcell = ws.cell(row=i, column=5)
    fill = {"Core":"C6EFCE","High":"FFEB9C","Medium":"DDEBF7","Low":"F2F2F2"}[fitcell.value]
    fitcell.fill = PatternFill("solid", fgColor=fill)
widths = [42,12,26,22,9,11,14,8,6,9,42,12,16,30]
for c,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(c)].width = w
ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:N{len(rows)+1}"
NL = len(rows)+1

# --- Clusters rollup (values computed in Python from Universe data; static because
# the source data in this workbook is static. Priority Score on Universe stays formula-driven.)
ws = wb.create_sheet("Clusters")
hdr = ["Cluster","Keywords","Sum best volume","Avg KD","BCA ranks top-20 (count)"]
ws.append(hdr); style_header(ws, len(hdr))
from collections import defaultdict
agg = defaultdict(lambda: {"n":0,"vol":0,"kd":[],"top20":0})
for r in rows:
    a = agg[r["cluster"]]
    a["n"] += 1
    a["vol"] += max(r["vol_a"] or 0, r["vol_g"] or 0)
    if r["diff"] is not None: a["kd"].append(r["diff"])
    if r["pos"] is not None and r["pos"] <= 20: a["top20"] += 1
for i, cl in enumerate(sorted(agg, key=lambda c: -agg[c]["vol"]), start=2):
    a = agg[cl]
    kd = round(sum(a["kd"])/len(a["kd"])) if a["kd"] else None
    ws.append([cl, a["n"], a["vol"], kd, a["top20"]])
    for c in range(1,6): ws.cell(row=i, column=c).font = Font(name=F, size=10)
note_row = len(agg)+3
ws.cell(row=note_row, column=1, value="Values computed from Universe tab data at build time (2026-07-28). Best volume = MAX(Ahrefs, Google Ads) per keyword.").font = Font(name=F, size=8, italic=True)
for c,w in zip(range(1,6),[30,10,16,8,24]): ws.column_dimensions[get_column_letter(c)].width = w

# --- Page Map
ws = wb.create_sheet("Page Map")
hdr = ["Cluster","Owning BCA page","Status","Action"]
ws.append(hdr); style_header(ws, len(hdr))
pm = [
["Ad network / platform","/igaming-advertising (hub)","Live, redesigned 07-26","Add 'iGaming ad network' + 'buy traffic' phrasing to H2s/FAQ; single H1; FAQ schema"],
["Traffic buying","/igaming-advertising (hub) or dedicated /gambling-traffic LP","Gap","Competitors win with dedicated traffic LPs (HilltopAds, TrafficStars). Ship LP or hub section"],
["Competitor alternatives","New: /post/<network>-alternatives + reviews","Gap (Taboola/A-Ads reviews exist)","Extend proven review playbook to RichAds, Adsterra, PropellerAds, HilltopAds, ClickAdu"],
["Advertising (general)","/post/gambling-advertising + vertical posts","Live, cannibalized","De-overlap titles per playbook; each post owns one term"],
["Ad examples & creatives","/post/igaming-ad-examples, /post/casino-advertising-examples","Live, pos 11-19","CTR title rewrites; internal links to hub"],
["Agency-intent capture","/post/igaming-marketing-agency","Live, pos 14","Reframe: 'need a platform instead?' -> BCA #1, then agency list"],
["Compliance & platform policy","/post/advertising-online-gambling-on-facebook + Google policy posts","Partial (pos 7 on google ads gambling policy)","Build policy hub: Google/Meta/TikTok gambling ads guides -> 'compliant alternative' CTA"],
["Affiliate programs & marketing","/post/casino-affiliate-marketing (after 301 merge)","Live, wrong format","301 gambling-affiliate-program into it; reformat as 'Best Casino Affiliate Programs 2026' listicle (3,100/mo head term); bridge to traffic buying"],
["Affiliate B2B software","None","Not our product","Skip or one comparison post for topical authority only"],
["Marketing strategy & guides","/post/igaming-marketing-strategies, /post/casino-marketing-strategies","Live","Refresh + internal links to hub; keep one strategy post per vertical"],
["Operator setup","/post/how-to-start-an-online-casino","Live","Refresh; natural advertiser-onboarding CTA (operators launching = future ad buyers)"],
["Vertical general","/post/igaming-vertical","Live, pos 26-44","Keep as glossary/authority; fix hreflang leakage (RU/KO versions rank in EN)"],
]
for r in pm: ws.append(r)
for i in range(2, len(pm)+2):
    for c in range(1,5):
        cell = ws.cell(row=i, column=c); cell.font = Font(name=F, size=9)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
for c,w in zip(range(1,5),[26,40,26,70]): ws.column_dimensions[get_column_letter(c)].width = w
ws.freeze_panes = "A2"

os.makedirs("/home/user/SEO/igaming", exist_ok=True)
# CSV export of universe
with open("/home/user/SEO/igaming/keyword-universe.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["keyword","vertical","cluster","audience","bca_fit","vol_ahrefs","vol_googleads","cpc_usd","kd","bca_pos","bca_url","pos_source","sources"])
    for r in rows:
        w.writerow([r["kw"],r["vertical"],r["cluster"],r["aud"],r["fit"],r["vol_a"],r["vol_g"],r["cpc"],r["diff"],r["pos"],r["url"],r["psrc"],r["src"]])

wb.save("/home/user/SEO/igaming/keyword-universe.xlsx")
print("rows:", len(rows))
from collections import Counter
print(Counter([r["fit"] for r in rows]))
print(Counter([r["cluster"] for r in rows]).most_common())
