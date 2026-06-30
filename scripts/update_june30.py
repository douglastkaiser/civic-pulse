#!/usr/bin/env python3
"""
June 30, 2026 updates for all issue and organization data files.
Key developments since June 29:
  - Austin: Council recess continues (returns July 23, 23 DAYS); City Manager budget July 16 (16 DAYS)
  - Austin: Dog's Head Environmental Commission TOMORROW (July 1); county TIRZ vote July 14 (14 DAYS)
  - Austin: D1 filing opens July 19 (19 DAYS); first in-person filing July 20
  - Austin: Homicide count at 30+ for 2026; tracking below 2025 pace (55 total last year)
  - Austin: SAHNC opening June 2027; Sunrise tentative operator; council vote July 23
  - Austin: Convention center: June 18 court ruling permanently secured bond funding
  - Austin: DBC still zero applications after first month in commercial zones
  - OC: ⚡ Grand Jury homelessness response deadline TODAY (June 30) — county must earmark prevention funds
  - OC: ⚡ AG seeking additional $100K/month HB penalties starting TOMORROW (July 1)
  - OC: ⚡ OC CERTIFIED primary results June 26 — D5: Foley (D) vs Dixon (R), razor-thin; both to November
  - OC: GKN extraction FINALLY STARTED — ~14,000 gallons MMA removed; cleanup through Thursday
  - OC: OC Streetcar powered testing started June 25; service March 2027
  - OC: Interim CEO Roestenberg in role ($430K salary, $657K total comp); BOS cancelled through August
  - OC: Governor county certification July 3 (3 DAYS)
  - Brooklyn: Monitor Point rezoning committee-approved June 25 — 1,324 units, 50% affordable (up from 25%)
  - Brooklyn: South of Prospect Plan announced — rezoning Coney Island Ave & McDonald Ave corridors
  - Madison: Door Creek Watershed Study extended through Jan 2027; Christine Knapp appointed Water Utility GM
  - Cambridge: Joint roundtable with School Committee TODAY (June 30); FY27 budget adopted
  - Brookline: Chestnut Hill overlay approved 217-20 at town meeting; buildings up to 175 ft allowed
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
austin["last_scraped"] = "2026-06-30T12:00:00Z"

# AISD
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** AISD boundary realignment remains split into Phase 1 (2027-28) and Phase 2 (2028-29). Phase 1 draft changes August 7 (38 DAYS); board vote September. Additional closures possible in Phase 2. 10 schools closed end of 2025-26. Superintendent suspended additional closures to focus on boundary work. Bond: staff to present ~$390M package when council returns July 23 (23 DAYS). City Manager budget presentation July 16 (16 DAYS). CDBG public comment through July 20; hearing July 14 (14 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** Filing period opens July 19 (19 DAYS). First day to file in person July 20. Filing deadline August 17. At least 3 candidates declared: Alexandria Anderson, Steven Brown, Kyra Lorena Rogers. Financial activity filings due July. Harper-Madison term-limited — first open D1 race since geographic representation began 2014. Council on recess until July 23 (23 DAYS). Election Day November 3.")
    print("  Updated atx-d1-election")

# Bond
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** Council on recess until July 23 (23 DAYS) — staff to present final ~$390M bond package. City Manager budget presentation July 16 (16 DAYS). Community survey closed with 53,000+ responses. Bond Election Advisory Task Force proposed two options: $766.53M and $436M — council majority directed ~$390M focused on parks ($250-260M), active transportation ($75-80M), community facilities/cultural arts ($50-60M). Mayor Watson opposes. Housing ($200M) excluded. Council decides in August whether to place on November ballot.")
    print("  Updated atx-2026-bond")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 order. Federal Record of Decision secured. Bait-and-switch lawsuit combined with ATP bond authorization case. Phase 1: 9.8-mile surface line, 15 stations, all-electric trains every 5 min. Target completion 2033. ATP continues design and property acquisition. Council on recess until July 23 (23 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# HSO
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** SAHNC opening June 2027. Construction and building improvements at 2401 S. I-35 through spring 2027. Sunrise tentative operator — council vote July 23 (23 DAYS). Sunrise rehoused 800 people in 2026. AT-Home Initiative ($6.7M, 5-year) proposals under review — awards September. Raising Travis County: $17.34M to WSCA for 1,000 childcare scholarships; $4.16M for provider quality improvements. CDBG comment through July 20; hearing July 14 (14 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** 30+ homicides in 2026 — tracking below 2025 pace (55 total last year, down from 72 in 2024). APD has 300+ sworn officer vacancies. Chief Davis reports first net positive officer gain in years. 157th cadet class mid-training. City Manager budget presentation July 16 (16 DAYS). Council on recess until July 23 (23 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** Raising Travis County expansion: $17.34M to WSCA for 1,000 childcare scholarships annually for children up to age 3. $4.16M for quality improvements at 150 providers (teacher raises, curriculum). Families pay ≤7% of income; scholarship continues to age 13. Future: reserved slots model RFS expected November 2026, contracts April 2027. Nontraditional-hours and infant/toddler gaps remain. CDBG comment through July 20; hearing July 14 (14 DAYS). City Manager budget July 16 (16 DAYS).")
    print("  Updated tc-childcare-funding")

# Pct 4
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** Morales serving as Pct 4 Commissioner. CDBG public comment through July 20; hearing July 14 (14 DAYS). City Manager budget presentation July 16 (16 DAYS). Council on recess until July 23 (23 DAYS).")
    print("  Updated tc-pct4-runoff")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** June 18 court ruling: Judge Sherine Thomas ruled Austin's financial plan lawful — permanently secured $1.35B bond funding via hotel occupancy tax. D-wall complete; first footings poured; structural steel positioning in progress. Excavation continuing through August 2026. Targeting LEED Gold certification. On track for spring 2029 reopening — nearly doubling rentable space to ~620,000 sq ft. Council on recess until July 23 (23 DAYS).")
    print("  Updated atx-convention-center")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** Rezoning continues for 445-acre site. Bond: housing ($200M) excluded from ~$390M direction. Dog's Head Environmental Commission TOMORROW (July 1). Council on recess until July 23 (23 DAYS). D1 filing opens July 19 (19 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** DBC in effect since June 1 — still zero applications after first month in commercial areas citywide. Cautious real estate conditions. DDB400 (750 ft max downtown) accepting applications since June 8; DDB850 (1,200 ft max) requires rezoning. Both require 5% affordable units. SB 840 multifamily by-right in commercial zones. Council on recess until July 23 (23 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** SB 840 compliance continuing: multifamily by-right in CS, GR, LO, GO districts at 36 units/acre and 45 ft. DBC zero applications in first month. DDB400/DDB850 downtown programs accepting applications. Missing middle housing draft ordinances due March 2027. Council on recess until July 23 (23 DAYS).")
    print("  Updated atx-development-rules-overhaul")

# Dog's Head
idx, issue = find_issue(austin["issues"], "atx-dogs-head-annexation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** ⚡ Environmental Commission review TOMORROW (July 1) — June 17 commission meeting saw nearly 4 hours of public comment; environmental activists described TIRZ deal as 'dystopian.' Draft TIRZ plan expected after July 4 weekend. Travis County TIRZ vote July 14 (14 DAYS). City council adoption vote July 23 (23 DAYS). 2,600 acres; 12,000+ homes projected; 20% affordable. Environmental remediation alongside new construction on former industrial mining land.")
    print("  Updated atx-dogs-head-annexation")

# Gas peaker plant
idx, issue = find_issue(austin["issues"], "atx-gas-peaker-plant")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** KUT June 26 investigation: Austin City Council has been voting in SECRET during executive sessions on Austin Energy matters for years — TX Open Meetings Act §551.086 carve-out allows secret votes on utility 'competitive matters.' ~$1B peaker plant vote tally never publicly released. Council approved emissions limits May 29 after secret plant vote. Austin Energy estimates peaker units operational by 2030. Public Citizen: 'struggling to understand' why gas peaker secret but wind/solar/battery contracts public. Council on recess until July 23 (23 DAYS).")
    print("  Updated atx-gas-peaker-plant")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-30T12:00:00Z"

# D5
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** ⚡ OC CERTIFIED primary results June 26 — D5 final: Foley (D) vs Dixon (R), razor-thin margin. Both advance to November. State certification deadline July 10 (10 DAYS). ⚡ Grand Jury homelessness response deadline TODAY — county must earmark prevention funds. BOS cancelled meetings through August — governance gap during critical deadlines. Interim CEO Roestenberg in role ($430K salary, $657K total comp); contract 'indefinite term.' 42% voter turnout (809,000+ ballots). Governor county certification July 3 (3 DAYS).")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** OC certified primary results June 26. Shaw (R) ~33% vs Traut (D) ~31%; both advancing to November. State certification deadline July 10 (10 DAYS). ⚡ GKN extraction FINALLY STARTED — ~14,000 gallons MMA removed; cleanup continuing through Thursday. Three criminal investigations ongoing (FBI/EPA, OC DA Spitzer, Cal/OSHA). ⚡ Grand Jury response deadline TODAY. BOS cancelled through August. Interim CEO Roestenberg in role.")
    print("  Updated oc-bos-district-4-open-seat")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** General election confirmed: Becerra (D) vs Hilton (R). OC certified results June 26. Governor county certification deadline July 3 (3 DAYS). State certification July 10 (10 DAYS). 42% turnout in OC (809,000+ ballots). Grand Jury deadline TODAY.")
    print("  Updated ca-governor-2026")

# HB housing element
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** ⚡ AG seeking additional $100K/month HB penalties starting TOMORROW (July 1) — could reach $150K/month combined with existing $50K/month fines. After 3 months at escalated rate, court may triple; after that, multiply by six and appoint receiver. Total accrued fines ~$500K+. HB housing element adopted June 16 (6-1) — HCD certification pending. Judge Griffin ORDERED ranked choice voting — first RCV in OC; to be implemented by November 2026 or 2028 depending on registrar capacity. 120-day zoning deadline ~October 14. Only 1,187 of 5,845 required very-low/low-income units permitted.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 30 update:** ⚡ GKN chemical extraction FINALLY STARTED — ~14,000 gallons of neutralized methyl methacrylate (MMA) removed from two storage tanks. Cleanup continuing through Thursday under unified command (OC Health Care Agency, South Coast AQMD, GKN). Air quality continuously monitored. Incident began May 21 — 40 days ago; forced evacuation of ~50,000 residents across Garden Grove, Anaheim, Stanton, Westminster, Cypress, Buena Park. 44+ lawsuits filed. Three criminal investigations (FBI/EPA, OC DA Spitzer, Cal/OSHA). GKN preparing partial production restart in unaffected sections. Grand Jury deadline TODAY. Company pledged $5M — council criticized as insufficient.")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** ⚡ Powered testing milestone: streetcar vehicles began testing on energized overhead wires June 25 — first overnight test 9pm-3am. Construction 95% complete. Revenue service March 2027. Fleet: eight Siemens S700 vehicles (90+ ft each, 211 passenger capacity). Expected 5,000 passengers/day across 10 stops. 4.15-mile route Santa Ana to Garden Grove. Testing phase 6-12 months.")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury: TODAY
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 30 update:** ⚡ Grand Jury response deadline TODAY — county must earmark sufficient discretionary funds toward homelessness prevention by end of day. Grand Jury report emphasized shift from reactive (shelters, encampment clearances) to preventative approaches (rental assistance, early intervention). BOS cancelled meetings through August — unclear how county will formally respond. PIT Count: 6,321 (down 13.7%); for first time, more people sheltered than unsheltered (3,256 sheltered vs 3,065 unsheltered). Since 2024: 898 supportive/affordable units created, 841 individuals placed into permanent homes. Interim CEO Roestenberg in role. Governor certification July 3 (3 DAYS).")
    print("  Updated OC Homelessness Grand Jury")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** ⚡ Grand Jury homelessness response deadline TODAY. BOS cancelled through August. $20.9M Supportive Housing NOFA + $35.1M HHAP continue. PIT Count: 6,321 (down 13.7%); first time more sheltered than unsheltered. D5 certified: Foley (D) vs Dixon (R), razor-thin — November outcome determines enforcement vs. services balance on board.")
    print("  Updated oc-homelessness-enforcement")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** $20.9M Supportive Housing NOFA application period continues. Combined with $35.1M HHAP = $56M+ in housing funding. Grand Jury response deadline TODAY. PIT Count: first time more sheltered than unsheltered. Since 2024: 898 units created, 841 placed into permanent homes. Governor certification July 3 (3 DAYS). State certification July 10 (10 DAYS).")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** General election confirmed: Valencia (D) vs Shader (R). Valencia dominated primary 63% vs 37%. OC certified results June 26. State certification deadline July 10 (10 DAYS).")
    print("  Updated oc-state-senate-sd34")

# OC FY2027 Budget
idx, issue = find_issue(oc["issues"], "oc-fy2027-budget")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** Interim CEO Roestenberg in role since June 26 ($430K salary, $657K total comp); contract 'indefinite term' — unclear when BOS will search for permanent CEO. BOS cancelled through August. Grand Jury deadline TODAY. Grand Jury criticized unchecked spending. Three largest OC cities grappling with budget deficits. GKN extraction finally started — cleanup costs mounting.")
    print("  Updated oc-fy2027-budget")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-30T12:00:00Z"

idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** ⚡ Monitor Point rezoning committee-approved June 25 — 1,324 total units with 50% affordable (662 units), up from original 25%. Includes supportive housing, deeply affordable senior units, 100+ units for formerly homeless. Council secured commitment to complete Bushwick Inlet Park. Returns to City Planning Commission before full Council vote. South of Prospect Plan announced: Mayor Mamdani advancing rezoning of Coney Island Ave and McDonald Ave corridors south of Prospect Park — transit-oriented mixed-use development tied to future IBX (Interborough Express). East New York rezoning confirmed producing results with less gentrification. Citywide zoning reform estimated 82,000+ new homes with $5B City for All housing plan.")
    print("  Updated nyc-atlantic-ave-rezoning")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-30T12:00:00Z"

idx, issue = find_issue(madison["issues"], "budget-rules-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** SW/SE Area Plans adopted June 23. 200-acre Burke parkland purchase authorized ($6M Park Land Acquisition Funds; city/county cost-sharing). Area joins city in 2036; park planning begins after annexation. Door Creek Watershed Study contract extended through January 2027. Christine Knapp appointed General Manager of Madison Water Utility. Extreme heat warning issued — city resources deployed. Budget engagement sessions continuing.")
    print("  Updated budget-rules-2026")

save_json(ISSUES_DIR / "madison-wi.json", madison)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-30T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-zoning-reform-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** ⚡ Joint roundtable City Council Working Meeting with School Committee TODAY — discussing Cambridge Preschool Program including means testing and program expansion. FY27 budget adopted. Affordable Housing Overlay five-year review underway — Council reviewing impact on housing production since AHO adoption. Council approved $625K for nonprofits including Transition House. Zero Waste Master Plan changes proposed.")
    print("  Updated cam-zoning-reform-implementation")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-30T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** Chestnut Hill Commercial Overlay District approved 217-20 at town meeting (May 28). MoA and tax certainty agreement with City Realty also approved 230-6-6. Overlay covers 27.8 acres over six blocks along Route 9 between Hammond St and Hammond Pond Pkwy. Buildings up to 150-175 ft (12-14 stories) allowed; tapering near Newton boundary. Enables mixed-use transformation of older commercial parcels and parking lots. Route 9 transportation working group with Newton and MassDOT continuing.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 30 update:** Chestnut Hill overlay approved 217-20 — supports mixed-use zoning aligned with MBTA Communities Act compliance. Overlay covers 27.8 acres with buildings up to 175 ft. Fall 2023 MBTA-CA zoning amendments entered into eCode. Affordability guidelines being developed by Housing Advisory Board and Planning Board.")
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
        "\n\n**June 30 update:** ⚡ OC CERTIFIED primary results June 26 — D5 final: Foley (D) vs Dixon (R), razor-thin. Both to November. 42% turnout (809,000+ ballots). ⚡ Grand Jury homelessness response deadline TODAY. ⚡ AG penalties escalate TOMORROW (July 1) — $100K/month additional for HB. GKN extraction FINALLY STARTED — ~14,000 gallons MMA removed. BOS cancelled through August. Interim CEO Roestenberg ($430K, indefinite term). HB: Judge Griffin ordered RCV — first in OC. Governor certification July 3 (3 DAYS)."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 30 update:** OC certified results June 26. Becerra (D) vs Hilton (R) for governor — county certification July 3 (3 DAYS). Valencia (D) 63% vs Shader (R) 37% for SD-34 — state certification July 10 (10 DAYS). Grand Jury deadline TODAY. 42% turnout. BOS cancelled through August."
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
        "\n\n**June 30 update:** ⚡ AG penalties escalate TOMORROW (July 1) — additional $100K/month on top of $50K/month = $150K/month combined. After 3 months: court may triple; then multiply by six and appoint receiver. Total accrued ~$500K+. HB housing element adopted June 16 — HCD certification pending. Judge Griffin ordered RCV — to be implemented November 2026 or 2028. 120-day zoning deadline ~October 14. D5 certified: Foley vs Dixon, razor-thin. Grand Jury deadline TODAY. Governor certification July 3 (3 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 30 update:** Oak Creek Golf Course conversion: environmental and traffic reviews underway; public hearings expected late 2026. November council elections critical for housing direction. Grand Jury deadline TODAY. GKN extraction finally started — 14,000 gallons MMA removed. BOS cancelled through August."
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
        "\n\n**June 30 update:** ⚡ GKN extraction FINALLY STARTED — ~14,000 gallons MMA removed; cleanup through Thursday. Grand Jury deadline TODAY. D5 certified: Foley vs Dixon, razor-thin — supervisor races control county budget for childcare/family services. BOS cancelled through August. Interim CEO Roestenberg in role ($430K, indefinite term). Three largest OC cities grappling with budget deficits. Governor certification July 3 (3 DAYS)."
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
        "\n\n**June 30 update:** D1 filing opens July 19 (19 DAYS). At least 3 candidates declared (Anderson, Brown, Rogers). Financial activity filings due July. Bond shapes race — council directed ~$390M; BEATF proposed $766M and $436M options; Mayor Watson opposes. City Manager budget presentation July 16 (16 DAYS). Staff presents bond package July 23. Council on recess until July 23 (23 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 30 update:** Federal Record of Decision secured. Legal: Judge Shepperd ruling pending on AG Paxton jurisdictional plea. Bait-and-switch lawsuit combined with ATP bond case. Convention center: June 18 court ruling permanently secured $1.35B bond funding. D-wall complete; structural steel in progress. Dog's Head Environmental Commission TOMORROW (July 1). Council on recess until July 23 (23 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 30 update:** Rezoning continues for 445-acre site. Bond: housing ($200M) excluded from ~$390M direction. ⚡ Dog's Head TIRZ: Environmental Commission TOMORROW (July 1); county vote July 14 (14 DAYS); council July 23. Environmental activists pushed back hard at June 17 commission meeting. Council on recess until July 23 (23 DAYS)."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 30 update:** DBC still zero applications after first month — cautious market. DDB400 accepting applications; DDB850 requires rezoning. SB 840 by-right in commercial zones. Missing middle drafts due March 2027. ⚡ Dog's Head: Environmental Commission TOMORROW (July 1); 12,000+ homes, 20% affordable. Former industrial mining land — remediation alongside construction. Bond: housing excluded from ~$390M direction. Council on recess until July 23 (23 DAYS)."
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
        "\n\n**June 30 update:** SAHNC opening June 2027. Construction at 2401 S. I-35 through spring 2027. Sunrise tentative operator — council vote July 23 (23 DAYS). Sunrise rehoused 800 in 2026. AT-Home Initiative awards September. Raising Travis County: $17.34M for 1,000 childcare scholarships + $4.16M provider quality improvements. Bond: shelter NOT in ~$390M direction. CDBG comment through July 20; hearing July 14 (14 DAYS). City Manager budget July 16 (16 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 30 update:** 30+ homicides in 2026 — tracking below 2025 pace (55 total, vs 72 in 2024). 300+ sworn vacancies. First net positive officer gain in years. Chief Davis: staffing stabilizes in 2-3 years. City Manager budget presentation July 16 (16 DAYS). Council on recess until July 23 (23 DAYS)."
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
        "\n\n**June 30 update:** Raising Travis County: $17.34M to WSCA for 1,000 annual scholarships (children up to 3); $4.16M for 150 provider quality improvements. Families pay ≤7% income; scholarship to age 13. Reserved slots model RFS November 2026, contracts April 2027. Infant/toddler and nontraditional-hours gaps remain. CDBG comment through July 20; hearing July 14 (14 DAYS). City Manager budget July 16 (16 DAYS)."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 30 update:** City Manager budget presentation July 16 (16 DAYS). Council on recess until July 23 (23 DAYS). D1 filing opens July 19 (19 DAYS)."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-30T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868", "brooklyn-ny", "madison-wi", "cambridge-ma", "brookline-ma"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-30T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-30T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-30T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-30T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
