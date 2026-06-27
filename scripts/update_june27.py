#!/usr/bin/env python3
"""
June 27, 2026 updates for all issue and organization data files.
Key developments since June 26:
  - Austin: ⚡ KUT investigation: Council has been voting in SECRET during executive sessions for years
    May 21 gas peaker plant vote (~$1B) tally never publicly released; TX Open Meetings Act §551.086
  - Austin: ⚡ AISD boundary realignment POSTPONED to 2028-29; split into Phase 1 (2027-28) and Phase 2 (2028-29)
    Phase 1 draft changes August 7; board vote September. More closures possible in Phase 2.
  - Austin: Dog's Head TIRZ presentation to Travis County June 26; 12,000 units, $26B projected value
    Environmental Commission July 1; county TIRZ vote July 14; city council adoption July 23
  - Austin: Convention center D-wall construction COMPLETE; first footings poured; structural steel positioning
  - Austin: APD 31+ homicides — 5 in 2 weeks in mid-to-late June; first net positive officer gain in years
  - Austin: SAHNC timeline slipped — opening now June 2027 (was late summer 2026)
  - Austin: City Manager budget presentation July 16 (19 DAYS)
  - OC: ⚡ HB ranked choice voting ORDERED by Judge Griffin (June 25) — first RCV in OC
  - OC: Grand Jury homelessness response deadline June 30 (3 DAYS) — BOS cancelled meetings through August
  - OC: AG seeking additional $100K/month HB penalties starting July 1 (4 DAYS)
  - OC: Governor county certification deadline July 3 (6 DAYS)
  - OC: GKN extraction STILL delayed — 37+ days post-incident
  - OC: OC Streetcar now 95% complete (was 92%)
  - OC: Interim CEO K.C. Roestenberg appointed (June 23-24); Aguirre last day June 28
  - OC: Final election certification July 10 (13 DAYS)
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
austin["last_scraped"] = "2026-06-27T12:00:00Z"

# AISD: boundary realignment POSTPONED
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** ⚡ AISD boundary realignment POSTPONED — Superintendent Segura split the process into two phases and delayed the districtwide overhaul to 2028-29. Phase 1 (2027-28): accommodates students from 10 closed schools, addresses over-enrolled campuses, defines Marshall MS attendance area. Draft changes to be shared August 7; board vote expected September 2026. Phase 2 (2028-29): districtwide modifications and feeder pattern changes — more school closures possible. Work begins January 2027. Comment card still open through July 31. Bond: staff to present ~$400M package when council returns July 23 (26 DAYS). CDBG public comment through July 20; hearing July 14 (17 DAYS). City Manager budget presentation July 16 (19 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Filing period opens July 19 (22 DAYS). First day to file in person July 20. Filing deadline August 17. At least 7 candidates have appointed campaign treasurers — the most competitive open D1 race since geographic representation began in 2014. Key candidates: Alexandria Anderson (retired athlete, MLK NA president), Steven Brown (Medtronic, ~$6K raised, Save Austin Now ties), Misael Ramos (2022 runner-up with 25.3%/6,065 votes, Democratic Socialist, Blackland CDC board president), Amber Goodwin (assistant DA, gun violence prevention, former Biden admin advisor — notably NOT agreed to comply with Fair Campaign Ordinance contribution limits), Kyra Lorena Rogers (small business owner), Michael David Nahas (pro-housing advocate, UT economics). Semi-annual campaign finance filings due in July will reveal fundraising trajectories. ⚡ KUT secret voting investigation (June 26) adds transparency as a campaign issue. Council on recess until July 23 (26 DAYS). Election Day November 3.")
    print("  Updated atx-d1-election")

# Bond
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Council on recess until July 23 (26 DAYS) — staff to present final ~$400M bond package. City Manager budget presentation July 16 (19 DAYS) — FY2027 budget context will inform bond debate. Working allocations: parks ($250M), active transportation ($92M), community facilities ($48M). Each $100M costs median homeowner ~$14/year. Housing ($200M) excluded — 2022 housing bond has ~80% of funds unspent. Staff had recommended delaying to 2028 (only ~65% of prior decade bonds spent, below 90% threshold); council majority overrode. Council must decide by mid-August whether to place on November ballot. ⚡ Dog's Head TIRZ: Travis County heard Endeavor presentation June 26 — 12,000 housing units, $26B projected value by 2061; Environmental Commission recommendation July 1 (4 DAYS); county TIRZ vote July 14 (17 DAYS); city council adoption July 23 (26 DAYS).")
    print("  Updated atx-2026-bond")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Legal status unchanged — Judge Shepperd has NOT YET ruled on AG Paxton's jurisdictional plea since receiving TX Supreme Court's May 22 mandate. If Shepperd grants the plea, ATP's bond validation suit is dismissed entirely; if denied, AG gets an automatic interlocutory appeal that pauses all proceedings. Meanwhile, ATP continues pre-construction: $60M design-build contract awarded to Austin Rail Constructors for utility testing and field work. Plans to award three major contracts in 2026: route/stations construction, O&M facility, and light rail vehicles. Groundbreaking planned early 2027 — ATP says it will proceed 'with or without federal dollars.' Federal funding ($4.1B sought, $0 received) remains at risk under current administration. Council on recess until July 23 (26 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# HSO
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** ⚡ SAHNC timeline slipped — facility now expected to open June 2027 (was late summer/early fall 2026). Construction underway through spring 2027 at 2401 S. I-35 ($4.3M purchase). Sunrise named tentative operator; city offering $250K/year for operations — Pastor Hilbelink indicated this may be a 'concern' since current Sunrise center is privately funded. Council vote July 23 (26 DAYS). Sunrise has rehoused 800 people in 2026. AT-Home Initiative ($6.7M, 5-year): proposals submitted June 2, under review — up to 3 providers selected, contracts begin September. ⚡ VOCAL-TX staging all-night vigil June 29 (2 DAYS) outside Cicero Institute protesting criminalization of homelessness. CDBG comment through July 20; hearing July 14 (17 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** ⚡ 31+ homicides in 2026 as of June 24 — 5 homicides in 2 weeks in mid-to-late June (APD says cases unconnected). Latest: June 24 stabbing on S. Lamar Blvd (self-defense claim, no charges); June 24 elderly male found dead on Lambs Lane (Austin's 31st homicide). APD has 330+ sworn officer vacancies (~1,819 of ~2,120 authorized). ⚡ POSITIVE SIGN: APD gained net 3 officers this year — first positive net gain in years after losing 60-90 annually for five years. Applications up 166%. Chief Davis projects full staffing by end of 2027. Next academy application deadline September 16 for January 2027 class. Council on recess until July 23 (26 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Raising Travis County: $75M voter-approved program scaling. $28M+ awarded total — $17.34M to Workforce Solutions for 1,000 annual scholarships (children up to age 3), $4.85M/year to AISD/Del Valle ISD/Manor ISD for extended pre-K and after-school, $4.16M for quality improvements across 150 providers. AISD opened 9 Apple Blossom Centers for extended after-school care (3-6 PM) for 3-year-old pre-K. Nearly 300 scholarships issued, target 1,000 by October. CDBG comment through July 20; hearing July 14 (17 DAYS).")
    print("  Updated tc-childcare-funding")

# Pct 4
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Morales serving as Pct 4 Commissioner. ⚡ Dog's Head TIRZ: Travis County heard Endeavor presentation June 26 — 12,000 housing units on 2,600 acres, $26B projected value. Commissioner Shea skeptical: 'This is a whole lot of trust me.' Environmental Commission recommendation July 1 (4 DAYS); county TIRZ vote July 14 (17 DAYS). CDBG comment through July 20; hearing July 14 (17 DAYS). Council on recess until July 23 (26 DAYS).")
    print("  Updated tc-pct4-runoff")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** ⚡ D-wall construction COMPLETE — reinforced concrete perimeter structure finished, providing earth retention and foundation support for below-grade facilities. First footings poured. Structural steel positioning underway. 80 steel trusses salvaged from demolished building (548,000 lbs/274 tons) — 10 for reuse in Neches Pavilion, 45 for new warehouse. Low-carbon structural steel and rebar sourced from Nucor Texas (Jewett, TX). Steel package purchased early as cost-saving measure — proved prescient given subsequent tariff threats. Excavation continues through August 2026. On track for spring 2029 reopening — first zero-carbon-certified convention center in the world; LEED v4 Gold (Platinum target). Council on recess until July 23 (26 DAYS).")
    print("  Updated atx-convention-center")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Rezoning process continues for 445-acre Jimmy Clay/Roy Kizer site (5,000-15,000 unit potential). Council resolution sponsored by Fuentes, Alter, Ellis, and Laine. ⚡ Dog's Head TIRZ presentation June 26 at Travis County — 12,000 housing units on 2,600 acres shows scale of development pipeline alongside golf course. Bond: housing ($200M) excluded from ~$400M direction. Council on recess until July 23 (26 DAYS). Filing period for D1 opens July 19 (22 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** DBC: still zero applications since June 1 launch — 27 days with no uptake. Market signal compounded by SB 840 impact: state law allows multifamily by-right in commercial zones, reducing developer incentive to use city density bonus programs. DDB400 (750 ft max downtown) accepting applications since June 8 — requires 7 of 14 menu standards; DDB850 (1,200 ft max) requires rezoning plus 10 of 14 menu standards. No early interest in DDB850 reported. Both require 5% affordable units. Council on recess until July 23 (26 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Development rules implementation continuing. DBC program active but zero applications in 27 days since launch — SB 840 by-right multifamily reduces developer incentive. DDB400/DDB850 downtown programs accepting applications. Missing middle housing draft ordinances due March 2027. Council on recess until July 23 (26 DAYS).")
    print("  Updated atx-development-rules-overhaul")

# Gas peaker plant
idx, issue = find_issue(austin["issues"], "atx-gas-peaker-plant")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** ⚡ KUT investigation (June 26): the May 21 executive session vote to purchase ~$1B in gas peaker capacity was conducted in SECRET — vote tally never publicly released. All current council members refused to disclose their individual votes. TX Open Meetings Act §551.086 (enacted 1999) allows city-owned utilities to vote secretly on 'competitive matters.' Former CM Kelly said such votes 'always' occurred publicly during her tenure (2021-2025). 400 MW of new capacity; estimated ~$2,500/kW. Plant not operational until 2030. 14 possible sites identified — 9 of 14 in East Austin (all 10 existing peaker units already there). May 29: council passed emissions guidelines capping CO2 and NOx below pre-plant levels with extreme grid exemptions. Council on recess until July 23 (26 DAYS).")
    print("  Updated atx-gas-peaker-plant")

# Dog's Head annexation
idx, issue = find_issue(austin["issues"], "atx-dogs-head-annexation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** ⚡ Travis County commissioners heard Endeavor Real Estate presentation June 26 on the Dog's Head development plan. Scale: 12,000 housing units, 3M sq ft retail, 1M sq ft industrial, 1M sq ft office. Current land value $17M; projected 2061 value $26B. Tax increment reinvestment zone (TIRZ) would reserve 80% of city tax revenue and 50% of county revenue for infrastructure. 20% affordable housing requirement, 260+ acres parkland, 6+ mile river trail. Commissioner Shea skeptical: 'This is a whole lot of trust me.' ⚡ KEY VOTES: Environmental Commission recommendation July 1 (4 DAYS); county TIRZ vote July 14 (17 DAYS); city council adoption July 23 (26 DAYS). If TIRZ not approved, Endeavor may disannex the property. Council on recess until July 23 (26 DAYS).")
    print("  Updated atx-dogs-head-annexation")

# May 17 shooting
idx, issue = find_issue(austin["issues"], "atx-may17-shooting-spree")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** 31+ homicides in 2026 as of June 24 — 5 homicides in 2 weeks in mid-to-late June (APD says unconnected). APD gained net 3 officers this year — first positive gain in years. Applications up 166%. Chief Davis projects full staffing by end of 2027. Council on recess until July 23 (26 DAYS).")
    print("  Updated atx-may17-shooting-spree")

# ICE policy
idx, issue = find_issue(austin["issues"], "atx-ice-grants-deadline")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Council on recess until July 23 (26 DAYS). City Manager budget presentation July 16 (19 DAYS) — federal funding impacts on city services remain a budget consideration.")
    print("  Updated atx-ice-grants-deadline")

# HOME initiative
idx, issue = find_issue(austin["issues"], "atx-home-initiative-results")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** DBC: zero applications in 27 days since launch — SB 840 by-right multifamily reduces developer incentive for city programs. Missing middle draft ordinances due March 2027. Council on recess until July 23 (26 DAYS).")
    print("  Updated atx-home-initiative-results")

# Light rail overlay
idx, issue = find_issue(austin["issues"], "atx-light-rail-overlay")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Judge Shepperd has not yet ruled on AG Paxton's jurisdictional plea. ATP awarded $60M design-build contract to Austin Rail Constructors for pre-construction. Groundbreaking planned early 2027. Council on recess until July 23 (26 DAYS).")
    print("  Updated atx-light-rail-overlay")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-27T12:00:00Z"

# D5
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** June 26 was the LAST SCHEDULED registrar count update — Dixon (R) held lead at ~48.5% vs Foley (D) ~45%. Ballot pool nearly exhausted. Both advance to November regardless. Final certification expected by July 10 (13 DAYS). ⚡ BOS cancelled meetings through August for summer recess — Grand Jury homelessness response deadline June 30 (3 DAYS) with no scheduled board meeting to formally respond. ⚡ Interim CEO K.C. Roestenberg appointed June 23-24 (Aguirre last day June 28) — new supervisors inherit leadership transition. Governor county certification July 3 (6 DAYS). If Dixon wins November, the board flips to Republican majority — affecting $10.8B budget, housing enforcement, homelessness investment.")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Shaw (R) ~33% vs Traut (D) ~31%; both advancing to November general. ~10,000 ballots remaining countywide — pool nearly exhausted. Final certification July 10 (13 DAYS). GKN chemical extraction STILL delayed — 37+ days post-incident; sealed trucks still haven't arrived. Three criminal investigations continue (FBI/EPA, DA Spitzer, Cal/OSHA). Grand Jury response deadline June 30 (3 DAYS). Governor county certification July 3 (6 DAYS).")
    print("  Updated oc-bos-district-4-open-seat")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** General election confirmed: Becerra (D) vs Hilton (R). Primary results nearly final. County certification deadline July 3 (6 DAYS) for governor, July 10 for local races. Grand Jury response deadline June 30 (3 DAYS).")
    print("  Updated ca-governor-2026")

# Also update oc-ca-governor-race if it exists
idx, issue = find_issue(oc["issues"], "oc-ca-governor-race")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** General election confirmed: Becerra (D) vs Hilton (R). County certification deadline July 3 (6 DAYS). Grand Jury response deadline June 30 (3 DAYS).")
    print("  Updated oc-ca-governor-race")

# HB housing
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** HB housing element adopted June 16 (6-1) — under 45-day HCD review (certification expected ~early August). Court-ordered fines: $10K/month (Jan 2025-May 2026) + $50K/month starting June = ~$220K+ accrued. ⚡ AG seeking additional $100,000/month penalties starting July 1 (4 DAYS) — could reach $150K/month combined. After 3 months, court may triple; after that, multiply by six and appoint receiver. 120-day zoning deadline from June 16 = ~October 14. ⚡ BREAKING (June 25): Judge Griffin ORDERED HB to switch to ranked choice voting — first RCV in OC — after finding at-large system violates CA Voting Rights Act by disenfranchising Latino voters. Implementation ordered by November 2026 (may push to 2028). Only 1,187 of 5,845 required units permitted. Four Builder's Remedy applications (696 units) in pipeline. Grand Jury deadline June 30 (3 DAYS).")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 27 update:** GKN chemical extraction STILL delayed — specialized sealed trucks have NOT arrived, 37+ days post-incident. OC Health Care Agency will give advance public notice once extraction rescheduled. Air monitoring continues with no exceedances detected. GKN preparing partial production restart in unaffected sections while under three parallel criminal investigations (FBI/EPA federal, OC DA Spitzer state, Cal/OSHA workplace safety). 44+ lawsuits filed. Company pledged $5M total. SBA Business Recovery Center open Mon-Fri. ⚡ Grand Jury response deadline June 30 (3 DAYS). AG HB penalties escalate July 1 (4 DAYS). Governor county certification July 3 (6 DAYS).")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Revenue service pushed to March 2027. ⚡ Construction now at 95% complete (up from 92%). Street testing continues on Santa Ana Boulevard since February 20 — covering platform operations, control systems, and traffic signal interfacing. Track complete along entire route. Fleet: eight Siemens S700 vehicles (each 90+ ft, 211 passenger capacity), six running daily. Expected 5,000 passengers/day across 10 stops. 4.15-mile route. $2 one-way/$5 day pass. 6 AM-11 PM daily. Grand Jury deadline June 30 (3 DAYS).")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 27 update:** ⚡ Grand Jury response deadline June 30 — 3 DAYS remaining. County must earmark sufficient discretionary funds toward homelessness prevention by deadline. ⚡ COMPLICATION: BOS cancelled meetings through August for summer recess — no scheduled board meeting to formally respond before deadline. County balanced current budget using $75M in one-time funds. Interim CEO Roestenberg appointed June 23-24. PIT Count: 6,321 (down 13.7%) — more sheltered (3,256) than unsheltered (3,065) for first time. OC completed 1,544 units with 1,811 more planned. Governor county certification July 3 (6 DAYS). Final election certification July 10 (13 DAYS).")
    print("  Updated OC Homelessness")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** ⚡ Grand Jury homelessness response deadline June 30 — 3 DAYS. $20.9M Supportive Housing NOFA + $35.1M HHAP continue. PIT Count: 6,321 (down 13.7%) — more sheltered than unsheltered for first time. D5 outcome determines board majority and enforcement vs. services balance. Final certification July 10 (13 DAYS).")
    print("  Updated oc-homelessness-enforcement")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** $20.9M Supportive Housing NOFA application period continues. Combined with $35.1M HHAP = $56M+ in housing funding. Grand Jury response deadline June 30 (3 DAYS). OC completed 1,544 units with 1,811 more planned. Governor county certification July 3 (6 DAYS). Final election certification July 10 (13 DAYS).")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** General election confirmed: Valencia (D) vs Shader (R). Valencia dominated primary at 63% vs Shader 37%. County certification deadline July 10 (13 DAYS). Grand Jury deadline June 30 (3 DAYS).")
    print("  Updated oc-state-senate-sd34")

# AD-68
idx, issue = find_issue(oc["issues"], "oc-ad68-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** Valencia's move to SD-34 leaves AD-68 open. County certification deadline July 10 (13 DAYS).")
    print("  Updated oc-ad68-open-seat")

# CD-40
idx, issue = find_issue(oc["issues"], "oc-cd40-kim-calvert")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** County certification deadline July 10 (13 DAYS). Grand Jury deadline June 30 (3 DAYS).")
    print("  Updated oc-cd40-kim-calvert")

# FY2027 budget
idx, issue = find_issue(oc["issues"], "oc-fy2027-budget")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 27 update:** $10.5B recommended budget under BOS review. Grand Jury homelessness response deadline June 30 (3 DAYS) — response will affect budget priorities. D5 primary results still being certified — board composition affects FY2027 spending. Final certification July 10 (13 DAYS).")
    print("  Updated oc-fy2027-budget")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ORGS — OC Purple Accountability
# ============================================================
print("\n=== Updating oc-purple-accountability.json ===")
oc_purple = load_json(ORGS_DIR / "oc-purple-accountability.json")

campaign = find_campaign(oc_purple, campaign_id="bos-majority-defense")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 27 update:** D5: Dixon (R) held lead at ~48.5% vs Foley (D) ~45% — June 26 was LAST SCHEDULED count; pool nearly exhausted. D4: Shaw (R) ~33% vs Traut (D) ~31%. Final certification July 10 (13 DAYS). ⚡ BOS cancelled meetings through August — Grand Jury deadline June 30 (3 DAYS) with no scheduled meeting to respond. Interim CEO Roestenberg appointed. GKN extraction STILL delayed — 37+ days. ⚡ HB: Judge Griffin ordered ranked choice voting (June 25); AG seeking additional $100K/month penalties July 1 (4 DAYS). Governor certification July 3 (6 DAYS)."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 27 update:** Becerra (D) vs Hilton (R) for governor — county certification July 3 (6 DAYS). Valencia (D) 63% vs Shader (R) 37% for SD-34 — certification July 10 (13 DAYS). Grand Jury deadline June 30 (3 DAYS)."
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
        "\n\n**June 27 update:** HB housing element adopted June 16 (6-1) — under 45-day HCD review. Fines: $10K/month (Jan 2025-May 2026) + $50K/month from June = ~$220K+ accrued. ⚡ AG seeking additional $100K/month penalties July 1 (4 DAYS). ⚡ Judge Griffin ordered HB to switch to ranked choice voting (June 25) — first RCV in OC; at-large system found to violate CA Voting Rights Act. 120-day zoning deadline ~October 14. Only 1,187 of 5,845 required units permitted. Builder's Remedy still in effect until HCD certifies. Grand Jury deadline June 30 (3 DAYS). Governor certification July 3 (6 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 27 update:** Oak Creek Golf Course conversion: environmental and traffic reviews underway; public hearings expected late 2026. Irvine Company revised plan: 50-acre nature park + ~3,000 housing units. November council elections (3 seats + mayor) critical for housing direction. Grand Jury deadline June 30 (3 DAYS). Governor certification July 3 (6 DAYS)."
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
        "\n\n**June 27 update:** GKN extraction STILL delayed — 37+ days post-incident; sealed trucks still haven't arrived. Three criminal investigations continue (FBI/EPA, DA Spitzer, Cal/OSHA). D5 supervisor race remains razor-thin — board composition controls county budget for childcare/family services. ⚡ Grand Jury response deadline June 30 (3 DAYS). Governor county certification July 3 (6 DAYS). Final election certification July 10 (13 DAYS)."
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
        "\n\n**June 27 update:** Filing period opens July 19 (22 DAYS). At least 7 candidates with appointed treasurers for D1 — most competitive open race since 2014. Key development: Amber Goodwin (assistant DA, gun violence prevention advocate) has NOT agreed to comply with Fair Campaign Ordinance contribution limits — potential fundraising advantage. Misael Ramos (2022 runner-up, 25.3%/6,065 votes) has campaign infrastructure. Semi-annual finance filings due July. ⚡ KUT secret voting investigation adds transparency as a campaign issue — May 21 peaker plant vote tally never released. ⚡ Dog's Head TIRZ: Environmental Commission July 1 (4 DAYS); county TIRZ vote July 14 (17 DAYS); city council adoption July 23 (26 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 27 update:** Judge Shepperd has NOT yet ruled on AG Paxton's jurisdictional plea since TX Supreme Court's May 22 mandate. ATP continues pre-construction: $60M design-build contract to Austin Rail Constructors. Plans to award three major contracts in 2026 (route/stations, O&M facility, vehicles). Groundbreaking planned early 2027. Federal funding ($4.1B sought, $0 received) at risk. ⚡ Convention center: D-wall construction COMPLETE; first footings poured; structural steel positioning underway. Council on recess until July 23 (26 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 27 update:** Rezoning continues for 445-acre site. ⚡ Dog's Head TIRZ: 12,000 housing units on 2,600 acres — county TIRZ vote July 14 (17 DAYS); council adoption July 23 (26 DAYS). Bond: housing ($200M) excluded from ~$400M direction. Council on recess until July 23 (26 DAYS)."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 27 update:** DBC: zero applications in 27 days since launch — SB 840 by-right multifamily reduces developer incentive. DDB400 requires 7 of 14 menu standards; DDB850 requires 10 of 14 plus rezoning — no early DDB850 interest reported. ⚡ Dog's Head TIRZ: 12,000 units, 20% affordable housing requirement, $26B projected value — county vote July 14 (17 DAYS). Missing middle draft ordinances due March 2027. Council on recess until July 23 (26 DAYS)."
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
        "\n\n**June 27 update:** ⚡ SAHNC timeline slipped — opening now June 2027 (was late summer 2026). Construction underway through spring 2027. City offering $250K/year for operations — Sunrise pastor indicated this may be a 'concern.' Council vote July 23 (26 DAYS). Sunrise rehoused 800 people in 2026. AT-Home Initiative: proposals submitted June 2, under review — contracts begin September. VOCAL-TX vigil June 29 (2 DAYS) outside Cicero Institute. CDBG comment through July 20; hearing July 14 (17 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="shelter-capacity-outcomes")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 27 update:** SAHNC opening delayed to June 2027. Marshalling Yard: up to 300 clients (Family Endeavors). Southbridge: new contract active since Feb 27 ($4M). HSO Director Gray acknowledged 'not enough shelter beds for everyone living unhoused in Austin.' 6 HEM teams (42 staff) being stood up for encampment management. Council on recess until July 23 (26 DAYS)."
    )
    print("  Updated shelter-capacity-outcomes")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 27 update:** ⚡ 31+ homicides — 5 in 2 weeks in mid-to-late June (APD says unconnected). 330+ sworn officer vacancies. POSITIVE: net 3 officers gained this year — first positive gain in years. Applications up 166%. Chief Davis projects full staffing by end of 2027. Next academy applications due September 16. ⚡ KUT investigation: council voted on ~$1B peaker plant in secret. Council on recess until July 23 (26 DAYS)."
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
        "\n\n**June 27 update:** Raising Travis County: $75M voter-approved program scaling — $28M+ awarded total. $17.34M to Workforce Solutions for 1,000 annual scholarships. AISD opened 9 Apple Blossom Centers for extended after-school care. Nearly 300 scholarships issued, target 1,000 by October. CDBG comment through July 20; hearing July 14 (17 DAYS). ⚡ AISD boundary realignment POSTPONED to 2028-29 — Phase 1 draft August 7, more closures possible in Phase 2."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 27 update:** City Manager budget presentation July 16 (19 DAYS). Bond: ~$400M package being developed; housing excluded. Council on recess until July 23 (26 DAYS). Filing period for council races opens July 19 (22 DAYS)."
    )
    print("  Updated parental-leave campaign")

campaign = find_campaign(atx_abundance, campaign_id="family-housing-campaign")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 27 update:** ⚡ Dog's Head TIRZ: 12,000 housing units, 20% affordable, 260+ acres parkland — county TIRZ vote July 14 (17 DAYS). DBC: zero applications in 27 days. Bond: housing ($200M) excluded. AISD boundary realignment POSTPONED to 2028-29 — school consolidation reshapes family housing demand. Council on recess until July 23 (26 DAYS)."
    )
    print("  Updated family-housing-campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-27T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-27T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-27T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-27T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-27T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
