#!/usr/bin/env python3
"""
July 1, 2026 updates for all issue and organization data files.
Key developments since June 30:
  - Austin: Dog's Head Environmental Commission review TODAY (July 1); council recess continues (returns July 23, 22 DAYS)
  - Austin: City Manager budget July 16 (15 DAYS); D1 filing opens July 20 (19 DAYS); at least 7 candidates declared
  - Austin: AISD halting most boundary realignment — pushing comprehensive changes to 2028-29 (KUT June 26)
  - Austin: DBC still zero applications; new affordable housing incentives launched June 25
  - OC: AG $100K/month additional HB penalties START TODAY (July 1) — could reach $150K/month combined
  - OC: GKN Phase 1 cleanup actively underway — removal through July 2; neutralized MMA trucked to Ohio for incineration
  - OC: Grand Jury homelessness response deadline passed (June 30) — no public reporting on whether county responded
  - OC: D5 correction: Dixon (R) OVERTOOK Foley (D) during mail ballot counting — both to November
  - OC: Remote public comment requirement effective TODAY for all OC cities
  - OC: County labor crisis — no raises for workers in FY2027 budget while supervisors took 25% raise last year
  - Brooklyn: NYC Council adopted $115.9B FY2026 budget June 30 — includes $4B capital + $1B expense for City for All housing
  - Brooklyn: Monitor Point full Council vote expected early July
  - Madison: Excessive Heat Warning through July 1 7PM — heat index up to 106; UW-Madison closed 23 buildings (broken chilled water line)
  - Madison: Christine Knapp confirmation vote expected July 7 or July 21
  - Cambridge: FY27 budget takes effect TODAY ($1.03B, first to exceed $1B)
  - Cambridge: AHO — CDD recommended 3 changes to Multifamily Housing Ordinance June 29; resident petition to reduce max from 9 to 6 stories
  - Brookline: FY2027 budget takes effect TODAY ($481M with $23.25M override); heat emergency declared July 1-4
"""
import json
from pathlib import Path

ISSUES_DIR = Path(__file__).resolve().parent.parent / "public" / "data" / "issues"
ORGS_DIR = Path(__file__).resolve().parent.parent / "public" / "data" / "orgs"
META_DIR = Path(__file__).resolve().parent.parent / "public" / "data" / "meta"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Saved {path.name}")


def find_issue(issues, issue_id=None, title_keyword=None):
    for i, issue in enumerate(issues):
        if issue_id and issue.get("id") == issue_id:
            return i, issue
        if title_keyword and title_keyword.lower() in issue.get("title", "").lower():
            return i, issue
    return None, None


def find_campaign(data, campaign_id=None, keywords=None):
    for campaign in data.get("active_campaigns", []):
        if campaign_id and campaign.get("id") == campaign_id:
            return campaign
    if keywords:
        for campaign in data.get("active_campaigns", []):
            text = (campaign.get("title", "") + " " + campaign.get("summary", "")).lower()
            if all(kw.lower() in text for kw in keywords):
                return campaign
    return None


def append_to_field(issue, field, text):
    if field in issue:
        issue[field] += text
    else:
        issue[field] = text


def append_to_summary(campaign, text):
    campaign["summary"] = campaign["summary"] + text


# ============================================================
# ISSUES — AUSTIN
# ============================================================
print("=== Updating austin-78702.json ===")
austin = load_json(ISSUES_DIR / "austin-78702.json")
austin["last_scraped"] = "2026-07-01T12:00:00Z"

# AISD
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** ⚡ KUT (June 26): AISD halting most districtwide boundary realignment — comprehensive changes pushed to 2028-29 instead of 2027-28. Phase 1 draft changes still expected August 7 (37 DAYS); board vote September. Additional closures remain possible in Phase 2. 10 schools closed end of 2025-26; 580+ positions affected. Superintendent suspended additional closures to focus on boundary work. City Manager budget presentation July 16 (15 DAYS). Council on recess until July 23 (22 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Filing period opens July 20 (19 DAYS). Filing deadline August 17. At least 7 candidates declared — including Alexandria Anderson (39, personal trainer, Austin Neighborhoods Council), Steven Brown (41, clinical specialist, East Austin native). Candidates raised ~$140K collectively heading into 2026. Harper-Madison term-limited — first open D1 race since geographic representation began 2014. Council on recess until July 23 (22 DAYS). Election Day November 3.")
    print("  Updated atx-d1-election")

# Bond
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Bond in summer standstill. Staff Alternative Scenario breakdown: $200M parks (including $65M aquatics, $50M parkland acquisition), $92M transit (sidewalks, trails, bike paths), $23M library/animal center, $25M homeless shelter. Mayor Watson staunchly opposes 2026 bond; staff recommend delay to 2028. Final up-or-down vote on whether to place bond on November ballot: July 23 (22 DAYS). City Manager budget presentation July 16 (15 DAYS).")
    print("  Updated atx-2026-bond")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 order. Core question: whether ATP has authority to issue bonds using property-tax revenue. Federal Record of Decision secured. ATP continues design, property acquisition ($230M for 18 parcels). Phase 1: 9.8-mile surface line, 15 stations, all-electric trains every 5 min. Target completion 2033. Council on recess until July 23 (22 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# HSO
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** SAHNC opening June 2027. Construction at 2401 S. I-35 through spring 2027. Sunrise selected as operator — council vote July 23 (22 DAYS). Sunrise rehoused 800 people in 2026. $25M homeless shelter included in proposed $390M bond package. AT-Home Initiative ($6.7M, 5-year) proposals under review — awards September. CDBG comment through July 20; hearing July 14 (13 DAYS). City Manager budget July 16 (15 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** 2025 homicides: 55 (down from 66 in 2024), lowest since before 2020. Overall violent and property crime also decreased. Downtown area command at only 65% staffing (vs 85-90% historically). 300+ sworn officer vacancies. Chief Davis reports first net positive officer gain in years. City Manager budget presentation July 16 (15 DAYS). Council on recess until July 23 (22 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Raising Travis County serving 5,200+ children through 13 community partners, supporting 180 childcare providers. Wait times dropped from ~2 years to months. Eligibility: families earning up to 85% SMI (~$92,041 for family of four). Reserved slots model RFS expected November 2026, contracts April 2027. CDBG comment through July 20; hearing July 14 (13 DAYS). City Manager budget July 16 (15 DAYS).")
    print("  Updated tc-childcare-funding")

# Pct 4
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Morales serving as Pct 4 Commissioner. City Manager budget presentation July 16 (15 DAYS). Council on recess until July 23 (22 DAYS).")
    print("  Updated tc-pct4-runoff")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Structural demolition 100% complete. D-wall complete; first footings poured; excavation continues through 2026. Targeting LEED Gold and zero-carbon certification. June 18 court ruling permanently secured $1.35B bond funding via hotel occupancy tax. On track for spring 2029 reopening — nearly doubling rentable space from 365,000 to ~620,000 sq ft. Council on recess until July 23 (22 DAYS).")
    print("  Updated atx-convention-center")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Rezoning continues for 445-acre site (Resolution No. 20260312-027). Dog's Head Environmental Commission review TODAY (July 1). Travis County TIRZ vote July 14 (13 DAYS). Bond: housing ($200M) excluded from ~$390M direction. Council on recess until July 23 (22 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** DBC still zero applications after first month in commercial zones. ⚡ New: Austin launched additional affordable housing incentives June 25 for mixed-use construction and downtown towers. DDB400 (750 ft max downtown) accepting applications since June 8; DDB850 (1,200 ft max) requires rezoning. Both require 5% affordable units. SB 840 multifamily by-right in commercial zones. Council on recess until July 23 (22 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** SB 840 compliance continuing. DBC zero applications in first month. New affordable housing incentives launched June 25 for mixed-use and downtown. Missing middle housing draft ordinances due March 2027. Council on recess until July 23 (22 DAYS).")
    print("  Updated atx-development-rules-overhaul")

# Dog's Head
idx, issue = find_issue(austin["issues"], "atx-dogs-head-annexation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** ⚡ Environmental Commission review TODAY (July 1) — formal recommendation to Council on environmental protections. June 26: Travis County commissioners scrutinized the deal at a hearing ahead of TIRZ votes; intense opposition continues. Draft TIRZ plan expected after July 4 weekend. Travis County TIRZ vote July 14 (13 DAYS). City council adoption vote July 23 (22 DAYS). 2,600 acres; 12,000+ homes projected; 20% affordable.")
    print("  Updated atx-dogs-head-annexation")

# Gas peaker plant
idx, issue = find_issue(austin["issues"], "atx-gas-peaker-plant")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Austin Energy estimates peaker units operational by 2030. 400-megawatt plant at ~$1B cost. Austin Energy cites 30-50 reliability risk hours annually that could rise to 575 without new gas generation. Council approved emissions limits May 29 after secret plant vote. Council on recess until July 23 (22 DAYS).")
    print("  Updated atx-gas-peaker-plant")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-07-01T12:00:00Z"

# D5
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** ⚡ CORRECTION: Dixon (R) OVERTOOK Foley (D) during mail ballot counting after Foley led on election night (48.4% to 45.8%). Neither hit 50% — both advance to November. Third candidate Vellema received ~5.7%. ⚡ AG penalties escalate TODAY — additional $100K/month for HB on top of $50K/month = $150K/month combined. Grand Jury response deadline passed yesterday (June 30) — no public reporting on county response. ⚡ Remote public comment now required for ALL OC city councils (effective today). BOS cancelled through August. Governor county certification July 3 (2 DAYS). State certification July 10 (9 DAYS).")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** OC certified: Shaw (R) 33.27% (26,264 votes) vs Traut (D) 31.22% (24,643 votes) — Fullerton Mayor Fred Jung and La Habra Mayor Rose Espinoza eliminated. Both to November. GKN Phase 1 cleanup actively underway — neutralized MMA being pumped into temperature-controlled containers, trucked to Ohio for incineration. Removal through July 2. Three criminal investigations ongoing (FBI/EPA, OC DA, Cal/OSHA). ⚡ AG penalties escalate TODAY. Grand Jury deadline passed yesterday. Remote public comment now required. BOS cancelled through August.")
    print("  Updated oc-bos-district-4-open-seat")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** General election confirmed: Becerra (D) vs Hilton (R). OC certification complete. Governor county certification deadline July 3 (2 DAYS). State certification July 10 (9 DAYS). ⚡ AG HB penalties escalate TODAY. Remote public comment effective today for all OC cities.")
    print("  Updated ca-governor-2026")

# HB housing element
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** ⚡ AG penalties ESCALATE TODAY — additional $100K/month starting July 1 on top of existing $50K/month = $150K/month combined. Prior fines: $10K/month from Jan 2025 through May 2026 ($160K accrued). After 3 months at escalated rate, court may triple; after that, multiply by six and appoint receiver. Total accrued fines mounting. HB housing element adopted June 16 (6-1) — HCD certification pending. Judge Griffin ordered ranked choice voting — first in OC. 120-day zoning deadline ~October 14. Only 1,187 of 5,845 required very-low/low-income units permitted. D5 certified: Dixon overtook Foley during mail counting. State certification July 10 (9 DAYS).")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**July 1 update:** GKN Phase 1 cleanup actively underway — neutralized MMA being pumped from tanks #2 and #4 into specialized temperature-controlled containers. Removal started June 29 after a 3-week delay; scheduled through July 2. Material transported in refrigerated trucks to Ohio disposal site for incineration. Continuous air monitoring in place; operations daylight hours only. Residents warned of temporary fruity/plastic-like odors. Incident began May 21 — 41 days ago. 44+ lawsuits filed. Three criminal investigations (FBI/EPA, OC DA Spitzer, Cal/OSHA). ⚡ AG HB penalties escalate TODAY.")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Powered testing continues — first overnight test June 25 (9pm-3am) on energized overhead catenary wires. Prior: unpowered testing since October 2025; street testing on Santa Ana Boulevard since February 20. Construction 95% complete. Revenue service March 2027. Testing phase 6-12 months. Fleet: eight Siemens S700 vehicles. 4.15-mile route Santa Ana to Garden Grove.")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**July 1 update:** Grand Jury response deadline PASSED yesterday (June 30) — no public reporting on whether county or cities formally filed responses. Grand Jury report recommended shift from shelter-first to prevention-first (rental assistance, early intervention, identifying people on edge of homelessness). Commission to Address Homelessness (renamed from 'End Homelessness') was supposed to submit prevention strategies by Dec 31, 2025 — status unclear. BOS cancelled through August — governance gap during critical accountability period. PIT Count: 6,321 (down 13.7%); more sheltered (3,256) than unsheltered (3,065) for first time. Remote public comment now required for all OC cities (effective today).")
    print("  Updated OC Homelessness Grand Jury")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Grand Jury response deadline passed yesterday. BOS cancelled through August. PIT Count: 6,321 (down 13.7%); first time more sheltered than unsheltered. D5 certified: Dixon (R) overtook Foley (D) during mail counting — November outcome determines enforcement vs. services balance on board. Remote public comment now required for all OC cities (effective today).")
    print("  Updated oc-homelessness-enforcement")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** $20.9M Supportive Housing NOFA open until all funds committed. Up to 100 Project-Based Vouchers (Housing Choice, Mainstream, VASH) for extremely low-income homeless households. Combined with $35.1M HHAP = $56M+ in housing funding. Grand Jury deadline passed yesterday. PIT Count: first time more sheltered than unsheltered. Governor certification July 3 (2 DAYS). State certification July 10 (9 DAYS).")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** General election confirmed: Valencia (D) ~63% vs Shader (R) ~37%. Valencia strong favorite. OC certified. State certification deadline July 10 (9 DAYS). Governor county certification July 3 (2 DAYS).")
    print("  Updated oc-state-senate-sd34")

# OC FY2027 Budget
idx, issue = find_issue(oc["issues"], "oc-fy2027-budget")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** ⚡ $10.5B FY2026-27 budget adopted — $5.2B General Fund, $1.3B General Purpose Revenue. MAJOR CONTROVERSY: No raises for general county workers while supervisors gave themselves 25% raise last year. OCEA, Teamsters Local 952, and AOCDS in deadlocked labor negotiations. Workers protested at July 4 event. OC DA lambasted supervisors for silencing public debate on budget. Interim CEO Roestenberg in role ($430K, indefinite term). BOS cancelled through August. GKN cleanup costs mounting. ⚡ AG HB penalties escalate TODAY.")
    print("  Updated oc-fy2027-budget")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-07-01T12:00:00Z"

idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Monitor Point: Land Use Committee approved 9-0 on June 25 — full Council vote expected early July. Negotiated affordability up from 25% to 50%: 662 permanently affordable units (329 at 40-60% AMI, 172 at 80-125% AMI, 161 senior units at 30-50% AMI, ~110 supportive housing). Community benefits include Bushwick Inlet Park completion ($300K/year maintenance), new Greenpoint Monitor Museum, Nassau G train ADA upgrade (~$60M), 1+ acre waterfront open space. ⚡ NYC Council adopted $115.9B FY2026 budget June 30 — includes $4B capital + $1B expense for City for All housing commitments. South of Prospect Plan: community engagement via neighborhood survey underway; draft zoning proposal expected 2027.")
    print("  Updated nyc-atlantic-ave-rezoning")

# City of Yes
idx, issue = find_issue(brooklyn["issues"], "nyc-city-of-yes-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** ⚡ NYC Council adopted $115.9B FY2026 budget unanimously on June 30 — includes $4B capital + $1B expense for City for All housing. Mayor Mamdani's 'Block by Block' plan (May 2026) targets 200,000 new affordable + 200,000 preserved over 10 years. City of Yes (enacted December 2024) projected to enable 82,000+ homes over 15 years. Monitor Point full Council vote expected early July — test case for implementation. IBX Draft EIS expected fall/winter 2026.")
    print("  Updated nyc-city-of-yes-implementation")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-07-01T12:00:00Z"

idx, issue = find_issue(madison["issues"], "budget-rules-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** ⚡ Excessive Heat Warning through TODAY 7PM — heat index up to 106°F. ⚡ UW-Madison broken chilled water line forced closure of 23 buildings plus partial closure of 11 more (June 30); repairs expected to take at least one month; summer classes relocated. Cooling centers open (Veterans Memorial Coliseum, Madison College shelter, all Madison Public Libraries); Metro Transit providing free rides to cooling centers. City faces $11M shortfall for 2027 ($472.1M revenue vs $483.2M expenditures); Mayor Rhodes-Conway directed all agencies to prepare up to 2% budget reductions (~$9M). Next budget engagement session July 26. Christine Knapp confirmation vote expected July 7 or July 21. Next council meetings: July 7, July 21.")
    print("  Updated budget-rules-2026")

save_json(ISSUES_DIR / "madison-wi.json", madison)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-07-01T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-zoning-reform-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** ⚡ FY27 budget takes effect TODAY — $1.03B operating budget (Cambridge's first to exceed $1B), adopted 8-0-0-1. Over $51M for affordable housing (including social housing), ~$16M homelessness/housing stability, $5M early childcare exploration. Capital budget: $155.1M. Property taxes now 70% of revenue (up from 64% FY2022). ⚡ AHO developments (June 29): CDD recommended 3 'modest' changes to Multifamily Housing Ordinance — increased setbacks, enhanced ground-level permeable open space, limiting large-unit buildings to 3 stories. Doug Brown resident petition (13 signatures) proposes reducing AHO max heights from 9 to 6 stories + adding setback/parking requirements — Council cannot vote until August 3. Council divided: McGovern and Sobrinho-Wheeler oppose restrictions; Flaherty and Zusy support refinements. AHO progress: ~1,000 affordable units in development across 16 buildings; first AHO project (106 units, 52 New Street) opened spring 2026. Joint roundtable with School Committee held June 30 — Cambridge Preschool Program means testing discussed.")
    print("  Updated cam-zoning-reform-implementation")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-07-01T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** ⚡ FY2027 budget takes effect TODAY — $481M with $23.25M in override funding (approved May 5: 8,675 yes / 5,732 no). Override allocates $17.94M to schools, $5.31M to town departments over three fiscal years, increasing total tax levy by 18%. New Select Board: David Pearlman (Chair), Michael Rubenstein (Vice Chair), Bernard Greene, Amanda Zimmerman (new), Anthony Buono (new) — Zimmerman and Buono defeated incumbent VanScoyoc May 5. ⚡ Heat emergency declared July 1-4 — temperatures in 90s, heat index potentially 105-110°F. Cooling centers open at Senior Center, Public Safety Building, libraries, and Evelyn Kirrane Aquatics Center (free pool access). Chestnut Hill overlay: formal redevelopment application from City Realty expected later this summer; special permit review could take 9-12 months. Town News Portal retiring today — content moves to brooklinema.gov.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 1 update:** Chestnut Hill overlay supporting compliance — 27.8 acres with buildings up to 175 ft. Formal redevelopment application expected later this summer. FY2027 budget takes effect today ($481M). Heat emergency declared July 1-4.")
    print("  Updated brk-mbta-communities-compliance")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ORGS — OC Purple Accountability
# ============================================================
print("\n=== Updating oc-purple-accountability.json ===")
oc_purple = load_json(ORGS_DIR / "oc-purple-accountability.json")

campaign = find_campaign(oc_purple, campaign_id="bos-majority-defense")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** ⚡ CORRECTION: Dixon (R) overtook Foley (D) during mail ballot counting — both to November but dynamics shifted. D4: Shaw (R) 33% vs Traut (D) 31%, both to November. ⚡ AG HB penalties escalate TODAY — $150K/month combined. Grand Jury response deadline passed yesterday — no public reporting on county response. ⚡ FY2027 budget controversy: no worker raises while supervisors took 25% last year; OCEA, Teamsters, AOCDS in deadlocked negotiations. OC DA lambasted supervisors for silencing budget debate. GKN Phase 1 cleanup underway through July 2. ⚡ Remote public comment now required for ALL OC city councils (effective today). BOS cancelled through August. Governor certification July 3 (2 DAYS)."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** OC certified. Becerra (D) vs Hilton (R) for governor — county certification July 3 (2 DAYS). Valencia (D) 63% vs Shader (R) 37% for SD-34 — state certification July 10 (9 DAYS). ⚡ AG HB penalties escalate TODAY. Remote public comment required starting today. BOS cancelled through August."
    )
    print("  Updated state-legislative-tracking")

save_json(ORGS_DIR / "oc-purple-accountability.json", oc_purple)

# ============================================================
# ORGS — OC Housing Now
# ============================================================
print("\n=== Updating oc-housing-now.json ===")
oc_housing = load_json(ORGS_DIR / "oc-housing-now.json")

campaign = find_campaign(oc_housing, campaign_id="orange-housing-element")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** ⚡ AG penalties ESCALATE TODAY — $100K/month additional on top of $50K/month = $150K/month combined. Prior: $10K/month Jan 2025-May 2026 ($160K accrued). After 3 months at escalated rate: court may triple; then multiply by six and appoint receiver. HB housing element adopted June 16 — HCD certification pending. Judge Griffin ordered RCV. 120-day zoning deadline ~October 14. D5 certified: Dixon overtook Foley during mail counting. Remote public comment required starting today. Governor certification July 3 (2 DAYS). State certification July 10 (9 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** Oak Creek Golf Course conversion environmental/traffic reviews underway; public hearings expected late 2026. GKN Phase 1 cleanup underway through July 2 — neutralized MMA trucked to Ohio for incineration. ⚡ AG HB penalties escalate TODAY. Grand Jury deadline passed yesterday. Remote public comment now required. BOS cancelled through August."
    )
    print("  Updated irvine-general-plan")

save_json(ORGS_DIR / "oc-housing-now.json", oc_housing)

# ============================================================
# ORGS — OC Abundance Project
# ============================================================
print("\n=== Updating oc-abundance-project.json ===")
oc_abundance = load_json(ORGS_DIR / "oc-abundance-project.json")

campaign = find_campaign(oc_abundance, campaign_id="oc-childcare-desert-mapping")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** GKN Phase 1 cleanup underway through July 2. ⚡ FY2027 budget controversy: no worker raises; county labor crisis with OCEA, Teamsters, AOCDS deadlocked. Grand Jury deadline passed yesterday. D5 certified: Dixon overtook Foley — supervisor races control county budget for childcare/family services. ⚡ AG HB penalties escalate TODAY. Remote public comment now required for all OC cities. BOS cancelled through August. Governor certification July 3 (2 DAYS)."
    )
    print("  Updated oc-childcare-desert-mapping")

save_json(ORGS_DIR / "oc-abundance-project.json", oc_abundance)

# ============================================================
# ORGS — Austin YIMBY Action
# ============================================================
print("\n=== Updating austin-yimby-action.json ===")
atx_yimby = load_json(ORGS_DIR / "austin-yimby-action.json")

campaign = find_campaign(atx_yimby, campaign_id="council-elections-2026")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** D1 filing opens July 20 (19 DAYS). At least 7 candidates declared. Candidates raised ~$140K collectively heading into 2026. Bond shapes race — final vote on $390M bond July 23 (22 DAYS); Mayor Watson opposes. City Manager budget presentation July 16 (15 DAYS). Council on recess until July 23 (22 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. Core question: ATP authority to issue bonds using property-tax revenue. Federal Record of Decision secured. ATP continues design, property acquisition ($230M for 18 parcels). Convention center: structural demolition 100% complete; D-wall complete; excavation continuing. Dog's Head Environmental Commission review TODAY (July 1). Council on recess until July 23 (22 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** Rezoning continues for 445-acre site. ⚡ Dog's Head Environmental Commission review TODAY (July 1); Travis County commissioners scrutinized deal at June 26 hearing. TIRZ vote July 14 (13 DAYS); council vote July 23 (22 DAYS). Bond: housing ($200M) excluded from ~$390M direction. Council on recess until July 23 (22 DAYS)."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** DBC still zero applications after first month. ⚡ New affordable housing incentives launched June 25 for mixed-use construction and downtown towers. DDB400 accepting applications; DDB850 requires rezoning. SB 840 by-right in commercial zones. Missing middle drafts due March 2027. ⚡ AISD halting most boundary realignment — pushed to 2028-29 (KUT June 26). Dog's Head Environmental Commission TODAY (July 1). Council on recess until July 23 (22 DAYS)."
    )
    print("  Updated ongoing-housing-advocacy campaign")

save_json(ORGS_DIR / "austin-yimby-action.json", atx_yimby)

# ============================================================
# ORGS — Austin Safe & Sound
# ============================================================
print("\n=== Updating austin-safe-and-sound.json ===")
atx_safe = load_json(ORGS_DIR / "austin-safe-and-sound.json")

campaign = find_campaign(atx_safe, campaign_id="hso-strategic-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** SAHNC opening June 2027. Sunrise selected as operator — council vote July 23 (22 DAYS). $25M homeless shelter in proposed $390M bond. AT-Home Initiative awards September. Raising Travis County serving 5,200+ children through 13 partners. CDBG comment through July 20; hearing July 14 (13 DAYS). City Manager budget July 16 (15 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** 2025 homicides: 55 (down from 66 in 2024), lowest since before 2020. Downtown area command at only 65% staffing (vs 85-90% historically). 300+ sworn vacancies but first net positive officer gain in years. City Manager budget presentation July 16 (15 DAYS). Council on recess until July 23 (22 DAYS)."
    )
    print("  Updated apd-staffing-response campaign")

save_json(ORGS_DIR / "austin-safe-and-sound.json", atx_safe)

# ============================================================
# ORGS — Austin Abundance Project
# ============================================================
print("\n=== Updating austin-abundance-project.json ===")
atx_abundance = load_json(ORGS_DIR / "austin-abundance-project.json")

campaign = find_campaign(atx_abundance, campaign_id="childcare-desert-mapping")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** Raising Travis County now serving 5,200+ children through 13 community partners, supporting 180 providers. Wait times dropped from ~2 years to months. Eligibility: up to 85% SMI (~$92,041 family of four). Reserved slots model RFS November 2026, contracts April 2027. CDBG comment through July 20; hearing July 14 (13 DAYS). City Manager budget July 16 (15 DAYS)."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**July 1 update:** City Manager budget presentation July 16 (15 DAYS). Council on recess until July 23 (22 DAYS). D1 filing opens July 20 (19 DAYS)."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-07-01T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868", "brooklyn-ny", "madison-wi", "cambridge-ma", "brookline-ma"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-07-01T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-07-01T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-07-01T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-07-01T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
