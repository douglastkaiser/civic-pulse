#!/usr/bin/env python3
"""
June 29, 2026 updates for all issue and organization data files.
Key developments since June 28:
  - Austin: Council on recess until July 23 (24 DAYS); city manager budget presentation July 16 (17 DAYS)
  - Austin: SAHNC timeline slipped — opening now June 2027 (was late summer 2026); council vote July 23
  - Austin: Dog's Head TIRZ: Environmental Commission July 1 (2 DAYS); county vote July 14; council July 23
  - Austin: 30+ homicides in 2026; South Lamar stabbing is Austin's 30th of year
  - Austin: D1 filing opens July 19 (20 DAYS); at least 3 candidates declared
  - Austin: AISD boundary postponed to 2028-29; Phase 1 draft Aug 7; more closures possible
  - Austin: Convention center D-wall COMPLETE; first footings poured; structural steel in progress
  - Austin: KUT: secret executive session voting on Austin Energy — ~$1B peaker plant vote tally never released
  - OC: ⚡ Grand Jury homelessness response deadline TOMORROW (June 30) — 1 DAY
  - OC: AG seeking additional $100K/month HB penalties starting July 1 (2 DAYS)
  - OC: D5 razor-thin: Foley 46.98% vs Dixon 46.81% — certification July 10 (11 DAYS)
  - OC: GKN extraction STILL delayed — 38+ days post-incident
  - OC: Interim CEO Roestenberg officially in role since June 26; Aguirre last day June 28
  - OC: OC Streetcar 95% complete; service pushed to March 2027
  - OC: Governor county certification July 3 (4 DAYS)
  - OC: HB ranked choice voting ORDERED by Judge Griffin — first RCV in OC history
  - OC: BOS cancelled meetings through August — governance gap during critical deadlines
  - Brooklyn: East New York rezoning producing results; 840-ft tower (1,263 units) approved; waterfront advancing
  - Madison: SW/SE Area Plans adopted June 23; 200-acre Burke parkland purchase authorized
  - Cambridge: FY27 budget adopted; AHO five-year review; joint roundtable with School Committee June 30
  - Brookline: Chestnut Hill Commercial Overlay District approved at annual town meeting
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
austin["last_scraped"] = "2026-06-29T12:00:00Z"

# AISD
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** AISD boundary realignment POSTPONED to 2028-29 — split into Phase 1 (2027-28) and Phase 2 (2028-29). Phase 1 draft changes August 7 (39 DAYS); board vote September. More closures possible in Phase 2 — unclear which campuses. 10 schools closed at end of 2025-26 school year. Enrollment declined 3,000+ students last year. Bond: staff to present ~$390M package when council returns July 23 (24 DAYS). CDBG public comment through July 20; hearing July 14 (15 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** Filing period opens July 19 (20 DAYS). First day to file in person July 20. Filing deadline August 17. At least 3 candidates declared: Alexandria Anderson, Steven Brown, Kyra Lorena Rogers. Most competitive open D1 race since geographic representation began 2014 — Harper-Madison term-limited. Council on recess until July 23 (24 DAYS). Election Day November 3.")
    print("  Updated atx-d1-election")

# Bond
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** Council on recess until July 23 (24 DAYS) — staff to present final ~$390M bond package. City Manager budget presentation July 16 (17 DAYS). Community survey closed with 53,000+ responses. Council majority directed ~$390M: parks ($250-260M), active transportation ($75-80M), community facilities/cultural arts ($50-60M). Mayor Watson opposes. Housing ($200M) excluded. Council decides in August whether to place on November ballot.")
    print("  Updated atx-2026-bond")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 order. Federal Record of Decision secured — environmental review formally complete. Bait-and-switch lawsuit combined with ATP bond authorization case. Phase 1: 9.8-mile surface line, 15 stations, all-electric trains every 5 min. Full cost $8B+ including interest. ATP continues design, property acquisition ($230M for 18 parcels). Target completion 2033. Council on recess until July 23 (24 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# HSO
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** ⚡ SAHNC timeline slipped — opening now June 2027 (was late summer 2026). Construction and building improvements underway at 2401 S. I-35; work expected through spring 2027. Sunrise Navigation Center named tentative operator — council approval vote July 23 (24 DAYS). Sunrise has rehoused 800 people in 2026. AT-Home Initiative ($6.7M, 5-year) proposals under review — awards September. Bond: shelter infrastructure NOT in ~$390M direction. CDBG comment through July 20; hearing July 14 (15 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** 30+ homicides in 2026 — South Lamar stabbing is Austin's 30th of the year. 5 homicides in 2 weeks mid-to-late June. Tracking slightly below 2025 pace. APD has 300+ sworn officer vacancies. Chief Davis says first net positive officer gain in years. 157th cadet class mid-training. City Manager budget presentation July 16 (17 DAYS). Council on recess until July 23 (24 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** $17.65M expansion continuing — 25 contracts serving 5,200+ children, 180 providers. Nearly 300 scholarships issued, target 1,000 by October. Families pay ≤7% of income. Infant/toddler care and nontraditional-hours coverage remain key gaps. CDBG comment through July 20; hearing July 14 (15 DAYS). City Manager budget presentation July 16 (17 DAYS).")
    print("  Updated tc-childcare-funding")

# Pct 4
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** Morales serving as Pct 4 Commissioner. CDBG public comment through July 20; hearing July 14 (15 DAYS). City Manager budget presentation July 16 (17 DAYS). Council on recess until July 23 (24 DAYS).")
    print("  Updated tc-pct4-runoff")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** D-wall construction COMPLETE — first footings poured. Structural steel positioning in progress. Structural demolition 100% complete. Excavation in full force, continuing through August 2026; 293,000+ cubic yards removed. TX Supreme Court denied Austin United petition April 2; June 18 bond ruling permanently enjoins future legal challenges. Targeting LEED Gold certification. On track for spring 2029 reopening — nearly doubling rentable space to ~620,000 sq ft. Council on recess until July 23 (24 DAYS).")
    print("  Updated atx-convention-center")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** Rezoning continues for 445-acre site. Bond: housing ($200M) excluded from ~$390M direction. Council on recess until July 23 (24 DAYS). D1 filing opens July 19 (20 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** DBC in effect since June 1 in commercial areas citywide — five tiers (0-60 extra ft). Market uptake slow; zero applications in first month reflects cautious real estate conditions. DDB400 (750 ft max downtown) accepting applications since June 8; DDB850 (1,200 ft max) requires rezoning. Both require 5% affordable units. SB 840 multifamily by-right in commercial zones. Council on recess until July 23 (24 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** SB 840 compliance continuing: multifamily by-right in CS, GR, LO, GO districts at 36 units/acre and 45 ft. DBC zero applications in first month. DDB400/DDB850 downtown programs accepting applications. Missing middle housing draft ordinances due March 2027. Council on recess until July 23 (24 DAYS).")
    print("  Updated atx-development-rules-overhaul")

# Dog's Head
idx, issue = find_issue(austin["issues"], "atx-dogs-head-annexation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** ⚡ Environmental Commission review July 1 (2 DAYS). Travis County scrutinizing TIRZ deal — commissioners questioned projections at June 26 presentation; county TIRZ vote July 14 (15 DAYS). City council adoption vote July 23 (24 DAYS). 2,600 acres; 12,000+ homes projected; 20% affordable (10% Endeavor, 10% city+others). $26B projected value by 2061. 6.5-mile public trail planned — initial 2-mile portion within 2 years of TIRZ adoption.")
    print("  Updated atx-dogs-head-annexation")

# Gas peaker plant
idx, issue = find_issue(austin["issues"], "atx-gas-peaker-plant")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** KUT investigation revealed Austin City Council has been voting in SECRET during executive sessions on Austin Energy matters for years — ~$1B peaker plant vote tally never publicly released. TX Open Meetings Act §551.086 carve-out allows secret votes on utility 'competitive matters.' City says secret votes may have been occurring since 1999. Council approved emissions limits May 29 after secret plant vote. Council on recess until July 23 (24 DAYS).")
    print("  Updated atx-gas-peaker-plant")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-29T12:00:00Z"

# D5
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** ⚡ D5 razor-thin: Foley (D) 46.98% vs Dixon (R) 46.81% — separated by less than 0.2%. Lead has changed hands multiple times during canvass. Certification July 10 (11 DAYS). Both advance to November regardless. ⚡ Grand Jury homelessness response deadline TOMORROW (June 30). BOS cancelled meetings through August — governance gap during critical deadlines. Interim CEO Roestenberg officially in role since June 26; Aguirre's last day June 28. Governor county certification July 3 (4 DAYS).")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** Shaw (R) ~33% vs Traut (D) ~31%; both advancing to November. Certification July 10 (11 DAYS). GKN extraction STILL delayed — 38+ days post-incident; sealed trucks still haven't arrived. GKN preparing partial production restart while under three criminal investigations. ⚡ Grand Jury response deadline TOMORROW (June 30). BOS cancelled meetings through August. Interim CEO Roestenberg in role.")
    print("  Updated oc-bos-district-4-open-seat")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** General election confirmed: Becerra (D) vs Hilton (R). County certification deadline July 3 (4 DAYS) for governor; July 10 for local races (11 DAYS). Hilton enters general as significant underdog — Democrats outnumber Republicans nearly 2-to-1 in CA. Grand Jury deadline TOMORROW (June 30).")
    print("  Updated ca-governor-2026")

# HB housing element
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** HB housing element adopted June 16 (6-1) — HCD review and certification pending. Court-ordered $50K/month fines accruing; total now ~$500K+. ⚡ AG seeking additional $100K/month penalties starting July 1 (2 DAYS) — could reach $150K/month combined. After 3 months, court may triple fines; after that, multiply by six and appoint receiver. ⚡ Judge Griffin ORDERED ranked choice voting for HB — first RCV in OC history. 120-day zoning deadline from June 16 = ~October 14. Only 1,187 of 5,845 required very-low/low-income units permitted.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 29 update:** GKN chemical extraction STILL delayed — 38+ days post-incident (May 21). Specialized sealed trucks still have NOT arrived; no revised start date announced. Air monitoring continues with no exceedances. GKN preparing partial production restart in unaffected sections while under three criminal investigations (FBI/EPA, OC DA Spitzer, Cal/OSHA). 44+ lawsuits filed. Company pledged $5M total — Garden Grove council criticized as insufficient. Grand Jury deadline TOMORROW (June 30). BOS cancelled meetings through August.")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** Construction 95% complete. Revenue service pushed to March 2027. Street testing continues on Santa Ana Boulevard since February 20. Track complete along entire route. Fleet: eight Siemens S700 vehicles. Expected 5,000 passengers/day across 10 stops. 4.15-mile route. Testing phase could take 6-12 months.")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury: TOMORROW
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 29 update:** ⚡ Grand Jury response deadline TOMORROW (June 30) — county must earmark sufficient discretionary funds toward homelessness prevention by deadline. Grand Jury report emphasized shift from reactive (shelters, encampment clearances) to preventative approaches (rental assistance, early intervention, identifying people on edge of homelessness). BOS cancelled meetings through August — unclear how county will meet deadline. OC completed 1,544 permanent supportive housing units with 1,811 more planned. PIT Count: 6,321 (down 13.7%). Interim CEO Roestenberg in role. Governor certification July 3 (4 DAYS).")
    print("  Updated OC Homelessness Grand Jury")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** ⚡ Grand Jury homelessness response deadline TOMORROW (June 30). BOS cancelled meetings through August. $20.9M Supportive Housing NOFA + $35.1M HHAP continue. PIT Count: 6,321 (down 13.7%). D5 razor-thin: Foley 46.98% vs Dixon 46.81% — November outcome determines board majority and enforcement vs. services balance.")
    print("  Updated oc-homelessness-enforcement")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** $20.9M Supportive Housing NOFA application period continues. Combined with $35.1M HHAP = $56M+ in housing funding. Grand Jury response deadline TOMORROW (June 30). OC completed 1,544 units with 1,811 more planned. Governor certification July 3 (4 DAYS). Certification July 10 (11 DAYS).")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** General election confirmed: Valencia (D) vs Shader (R). Valencia dominated primary 63% vs 37%. County certification July 10 (11 DAYS).")
    print("  Updated oc-state-senate-sd34")

# OC FY2027 Budget
idx, issue = find_issue(oc["issues"], "oc-fy2027-budget")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** Interim CEO Roestenberg officially in role since June 26 — Aguirre's last day June 28. BOS cancelled meetings through August. Grand Jury criticized unchecked spending. Three largest OC cities (Anaheim, Santa Ana, Irvine) grappling with budget deficits. Anaheim's $120M Disneyland Resort bond payoff next year expected to cut new revenue in half.")
    print("  Updated oc-fy2027-budget")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-29T12:00:00Z"

idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** East New York rezoning producing results — research confirms new housing lessens rent increases and slows gentrification. Mandatory Inclusionary Housing producing affordable units as designed. 840-ft tower (1,263 units including 325 affordable under MIH) approved. Brooklyn waterfront towers in Greenpoint advancing — developer committed to 662 affordable of 1,150 total units. Citywide zoning reform estimated to create 82,000+ new homes with $5B City for All housing plan.")
    print("  Updated nyc-atlantic-ave-rezoning")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-29T12:00:00Z"

idx, issue = find_issue(madison["issues"], "budget-rules-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** Common Council adopted Southwest and Southeast Area Plans on June 23. Council authorized purchase of 200 acres in Burke for future parkland ($6M Park Land Acquisition Funds) — area joins city in 2036. Door Creek Watershed Study contract extended through January 2027. Christine Knapp appointed General Manager of Madison Water Utility. Budget engagement sessions continuing.")
    print("  Updated budget-rules-2026")

save_json(ISSUES_DIR / "madison-wi.json", madison)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-29T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-zoning-reform-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** FY27 budget adopted. Affordable Housing Overlay five-year progress review underway — Council reviewing impact on housing production since AHO adoption. Joint roundtable City Council Working Meeting with School Committee scheduled for June 30 (TOMORROW). Council approved $625K for nonprofits including Transition House. Zero Waste Master Plan changes proposed.")
    print("  Updated cam-zoning-reform-implementation")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-29T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** ⚡ Town Meeting approved Chestnut Hill Commercial Overlay District — new zoning overlay for 1280-1330 Boylston St (Chestnut Hill Office Park). Enables mixed-use transformation: new housing, commercial activity, public space. Route 9 transportation working group with Newton and MassDOT. Housing Advisory Board and Planning Board developing affordability guidelines for overlay incentives. Annual Town Meeting concluded.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 29 update:** Chestnut Hill Commercial Overlay District approved at annual town meeting — supports mixed-use zoning aligned with MBTA Communities Act compliance goals. Affordability guidelines being developed by Housing Advisory Board and Planning Board.")
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
        "\n\n**June 29 update:** ⚡ D5 razor-thin: Foley (D) 46.98% vs Dixon (R) 46.81% — less than 0.2% separating candidates. Both advance to November regardless. Certification July 10 (11 DAYS). ⚡ Grand Jury homelessness response deadline TOMORROW (June 30). BOS cancelled meetings through August — governance gap. Interim CEO Roestenberg in role since June 26; Aguirre departed June 28. HB: AG seeking additional $100K/month penalties starting July 1 (2 DAYS). Judge Griffin ordered ranked choice voting for HB — first RCV in OC. GKN extraction STILL delayed — 38+ days."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 29 update:** Becerra (D) vs Hilton (R) for governor — county certification July 3 (4 DAYS). Valencia (D) 63% vs Shader (R) 37% for SD-34 — certification July 10 (11 DAYS). Grand Jury deadline TOMORROW (June 30). BOS cancelled meetings through August."
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
        "\n\n**June 29 update:** HB housing element adopted June 16 — HCD certification pending. $50K/month fines accruing; ~$500K+ total. ⚡ AG seeking additional $100K/month starting July 1 (2 DAYS). After 3 months, court may triple; then multiply by six and appoint receiver. ⚡ Judge Griffin ORDERED ranked choice voting for HB — first RCV in OC. 120-day zoning deadline ~October 14. D5 razor-thin: Foley 46.98% vs Dixon 46.81%. Grand Jury deadline TOMORROW (June 30). Governor certification July 3 (4 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 29 update:** Oak Creek Golf Course conversion: environmental and traffic reviews underway; public hearings expected late 2026. November council elections critical for housing direction. Grand Jury deadline TOMORROW (June 30). BOS cancelled meetings through August."
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
        "\n\n**June 29 update:** GKN extraction STILL delayed — 38+ days. Air monitoring no exceedances. Grand Jury deadline TOMORROW (June 30). D5 razor-thin: Foley 46.98% vs Dixon 46.81% — supervisor races control county budget for childcare/family services. BOS cancelled meetings through August. Interim CEO Roestenberg in role. Governor certification July 3 (4 DAYS). Three largest OC cities grappling with budget deficits."
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
        "\n\n**June 29 update:** D1 filing opens July 19 (20 DAYS). At least 3 candidates declared (Anderson, Brown, Rogers). Bond shapes race — council directed ~$390M; Mayor Watson opposes. City Manager budget presentation July 16 (17 DAYS). Staff presents bond package July 23. Council on recess until July 23 (24 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 29 update:** Federal Record of Decision secured — environmental review formally complete. Legal: Judge Shepperd ruling pending on AG Paxton jurisdictional plea. Bait-and-switch lawsuit combined with ATP bond case. Convention center: D-wall COMPLETE; first footings poured; structural steel in progress. Council on recess until July 23 (24 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 29 update:** Rezoning continues for 445-acre site. Bond: housing ($200M) excluded from ~$390M direction. Dog's Head TIRZ: Environmental Commission July 1 (2 DAYS); county vote July 14 (15 DAYS). Council on recess until July 23 (24 DAYS)."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 29 update:** DBC zero applications in first month — cautious market conditions. DDB400 accepting applications; DDB850 requires rezoning. SB 840 by-right in commercial zones. Missing middle drafts due March 2027. Dog's Head TIRZ: Environmental Commission July 1 (2 DAYS); 12,000+ homes, 20% affordable. Bond: housing excluded from ~$390M direction. Council on recess until July 23 (24 DAYS)."
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
        "\n\n**June 29 update:** ⚡ SAHNC timeline slipped — opening now June 2027 (was late summer 2026). Construction/improvements at 2401 S. I-35 through spring 2027. Sunrise tentative operator — council vote July 23 (24 DAYS). Sunrise rehoused 800 in 2026. AT-Home Initiative awards September. Bond: shelter NOT in ~$390M direction. CDBG comment through July 20; hearing July 14 (15 DAYS). City Manager budget July 16 (17 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 29 update:** 30+ homicides in 2026 — 5 in 2 weeks in late June; tracking slightly below 2025 pace. 300+ sworn vacancies. First net positive officer gain in years. Chief Davis: staffing stabilizes in 2-3 years. City Manager budget presentation July 16 (17 DAYS). Council on recess until July 23 (24 DAYS)."
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
        "\n\n**June 29 update:** $17.65M expansion continuing — 5,200+ children, 180 providers, ~300 scholarships (target 1,000 by October). Infant/toddler and nontraditional-hours gaps remain. CDBG comment through July 20; hearing July 14 (15 DAYS). City Manager budget July 16 (17 DAYS). Bond: housing excluded from ~$390M direction."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 29 update:** City Manager budget presentation July 16 (17 DAYS). Council on recess until July 23 (24 DAYS). D1 filing opens July 19 (20 DAYS)."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-29T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868", "brooklyn-ny", "madison-wi", "cambridge-ma", "brookline-ma"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-29T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-29T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-29T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-29T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
