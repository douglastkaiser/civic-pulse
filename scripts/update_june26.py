#!/usr/bin/env python3
"""
June 26, 2026 updates for all issue and organization data files.
Key developments since June 25:
  - Austin: Council on recess until July 23 (27 DAYS); staff to present ~$400M bond package
  - Austin: DBC program: ZERO applications submitted since June 1 launch — market signal
  - Austin: DDB400 now accepting applications (since June 8); DDB850 requires rezoning
  - Austin: Convention center structural steel positioning beginning this month
  - Austin: D1 filing opens July 19 (23 DAYS); at least 3 candidates declared
  - Austin: $17.65M childcare expansion approved; 5,200+ children served
  - OC: Registrar ballot count TODAY (June 26) — Dixon (R) has retaken lead over Foley (D)
    in recent counts; D5 remains too close to call; ~10,000 ballots remaining countywide
  - OC: GKN extraction STILL delayed — 36+ days post-incident; trucks still haven't arrived
  - OC: Grand Jury homelessness response deadline June 30 (4 DAYS)
  - OC: AG seeking additional $100K/month HB penalties starting July 1 (5 DAYS)
  - OC: Governor county certification deadline July 3 (7 DAYS)
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
austin["last_scraped"] = "2026-06-26T12:00:00Z"

# AISD: boundary comment card still open
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** AISD boundary realignment comment card open through July 31. Virtual workshop completed June 23. Revised draft map to trustees in August; board vote September; implementation August 2027. 10 campuses closing this summer. Bond: staff to present ~$400M package when council returns July 23 (27 DAYS). Task force produced two options ($766.5M and $436M); community survey drew 53,000+ responses. CDBG public comment through July 20; hearing July 14 (18 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** Filing period opens July 19 (23 DAYS). First day to file in person July 20. Filing deadline August 17. At least 3 candidates declared: Alexandria Anderson (retired track athlete/personal trainer), Steven Brown (Medtronic clinical specialist, East Austin native), Kyra Lorena Rogers (small business owner). Most competitive open D1 race since geographic representation began in 2014 — Harper-Madison term-limited. Bond debate shapes D1 dynamics. Council on recess until July 23 (27 DAYS). Election Day November 3.")
    print("  Updated atx-d1-election")

# Bond: council divided
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** Council on recess until July 23 (27 DAYS) — staff to present final ~$400M bond package. Resident-led task force produced two options: $766.5M full package and $436M narrowed proposal. Community survey closed June 23 with 53,000+ responses — top priorities: transportation and housing/homelessness tied, followed by parks, public safety, flood protection, climate. 70%+ said climate considerations 'very or somewhat important' for all projects. Council majority (Alter, Ellis, Siegel, Vela, Qadri, Velásquez) directed staff toward ~$400M: parks ($250-260M), active transportation ($75-80M), community facilities/cultural arts ($50-60M). Mayor Watson and CM Duchen oppose. Housing ($200M) excluded. Council decides in August whether to place on November ballot.")
    print("  Updated atx-2026-bond")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 order. TX Supreme Court denied Austin United's convention center petition April 2 — provides legal precedent for public infrastructure projects. Phase 1: 9.8-mile surface line, 15 stations, all-electric trains every 5 minutes. Full cost $8B+ including interest. ATP continues design, property acquisition ($230M for 18 parcels). Target completion 2033. Council on recess until July 23 (27 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# HSO
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** Sunrise Navigation Center named tentative operator for South Austin Housing Navigation Center at 2401 S. I-35 ($4.3M purchase). Sunrise has already rehoused 800 people in 2026. Council approval vote July 23 (27 DAYS). Facility expected to open late summer/early fall 2026. AT-Home Initiative ($6.7M, 5-year) proposals under review — contract awards September. Bond: shelter infrastructure NOT in ~$400M direction; housing ($200M) excluded. CDBG public comment through July 20; hearing July 14 (18 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** 30+ homicides in 2026 — tracking slightly below 2025 pace (31 by same date last year). APD has 330+ sworn officer vacancies (~1,819 of ~2,120 authorized). Chief Lisa Davis says staffing will stabilize in 2-3 years. 157th cadet class mid-training. Council on recess until July 23 (27 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** ⚡ Raising Travis County: $17.65M expansion approved — 25 contracts serving 5,200+ children, 180 childcare providers supported. Nearly 300 scholarships issued, target 1,000 by October. Families pay ≤7% of income; eligible up to 85% SMI (~$92K for family of four). Wait times cut from 2 years to months. Infant/toddler care and nontraditional-hours coverage remain key gaps. CDBG public comment through July 20; hearing July 14 (18 DAYS).")
    print("  Updated tc-childcare-funding")

# Pct 4
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** Morales serving as Pct 4 Commissioner. $17.65M childcare expansion approved — 5,200+ children served through Raising Travis County. CDBG public comment through July 20; hearing July 14 (18 DAYS). Council on recess until July 23 (27 DAYS).")
    print("  Updated tc-pct4-runoff")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** ⚡ Structural steel positioning beginning this month — major construction milestone. D-wall construction progressing between 2nd & 3rd Streets. Excavation continues through August 2026; 293,000+ cubic yards removed. TX Supreme Court denied Austin United petition April 2; June 18 bond ruling permanently enjoins future legal challenges to $1.35B bond funding. On track for spring 2029 reopening — nearly doubling rentable space to ~620,000 sq ft. Council on recess until July 23 (27 DAYS).")
    print("  Updated atx-convention-center")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** Rezoning process continues for 445-acre Jimmy Clay/Roy Kizer site (5,000-15,000 unit potential). Council resolution sponsored by Fuentes, Alter, Ellis, and Laine. Bond: housing ($200M) excluded from ~$400M direction — broader infrastructure landscape shifting. Council on recess until July 23 (27 DAYS). Filing period for D1 opens July 19 (23 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** ⚡ MARKET SIGNAL: Zero DBC applications submitted since program launched June 1 — reflecting cautious real estate market conditions despite strong policy framework. DBC offers five tiers (0-60 extra feet); rental projects reserve 10% at ≤50% MFI, for-sale 10% at ≤80% MFI. ⚡ Downtown towers: DDB400 (750 ft max) accepting applications since June 8; DDB850 (1,200 ft max) requires rezoning. Both require 5% affordable units. SB 840 multifamily by-right in commercial zones. Council on recess until July 23 (27 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** Development rules implementation continuing. SB 840 compliance: multifamily by-right in CS, GR, LO, GO districts at 36 units/acre and 45 ft. DBC program active but zero applications filed since June 1 launch. DDB400/DDB850 downtown programs now accepting applications. Missing middle housing draft ordinances due March 2027. Council on recess until July 23 (27 DAYS).")
    print("  Updated atx-development-rules-overhaul")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-26T12:00:00Z"

# D5: count TODAY
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** ⚡ OC Registrar ballot count TODAY (June 26) — scheduled ~5 PM update. Dixon (R) retook lead in recent counts at ~48.5% vs Foley (D) ~45%; lead has changed hands multiple times during canvass. ~10,000 ballots remaining countywide — pool nearly exhausted. Both advance to November regardless. Final certification July 10 (14 DAYS). Grand Jury homelessness response deadline June 30 (4 DAYS). Governor county certification July 3 (7 DAYS). If Dixon wins November, the board flips to Republican majority — affecting $10.8B budget, housing enforcement, and homelessness investment.")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** OC Registrar count TODAY — Shaw (R) ~33% vs Traut (D) ~31%; both advancing to November general. ~10,000 ballots remaining countywide. Final certification July 10 (14 DAYS). GKN chemical extraction STILL delayed — 36+ days post-incident; sealed trucks still haven't arrived. GKN preparing partial production restart in unaffected sections while under three criminal investigations (FBI/EPA, DA Spitzer, Cal/OSHA). Grand Jury response deadline June 30 (4 DAYS).")
    print("  Updated oc-bos-district-4-open-seat")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** General election confirmed: Becerra (D) vs Hilton (R). Primary results nearly final — Becerra 28%, Hilton 25% with 88% counted. County certification deadline July 3 (7 DAYS) for governor, July 10 for local races. OC Registrar count TODAY. Grand Jury response deadline June 30 (4 DAYS). Hilton enters general as significant underdog — Democrats outnumber Republicans nearly 2-to-1 in CA; no Republican governor elected in 20 years.")
    print("  Updated ca-governor-2026")

# HB: fines accruing, AG penalties imminent
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** HB housing element adopted June 16 (6-1) — HCD review and certification pending. Court-ordered $50,000/month fines accruing since June 2026; total owed now ~$450K+. ⚡ AG seeking additional $100,000/month penalties starting July 1 (5 DAYS) — could reach $150K/month combined. After 3 months, court may triple fines; after that, multiply by six and appoint receiver. 120-day zoning deadline from June 16 = ~October 14. Only 1,187 of 5,845 required very-low/low-income units permitted. Four Builder's Remedy applications (696 units) in pipeline.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove: extraction STILL delayed
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 26 update:** GKN chemical extraction STILL delayed — specialized sealed trucks have NOT arrived, 36+ days post-incident. OC Health Care Agency will give advance public notice once extraction rescheduled; warns pumping may release distinctive fruity/plastic-like odor. Air monitoring continues with no exceedances detected. GKN preparing partial production restart in unaffected sections while under three parallel criminal investigations (FBI/EPA, OC DA Spitzer, Cal/OSHA). 44+ lawsuits filed. Company pledged $5M total. SBA Business Recovery Center open Mon-Fri. OC Registrar count TODAY. Grand Jury response deadline June 30 (4 DAYS).")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** Revenue service pushed to March 2027. Construction at ~92%. Street testing continues on Santa Ana Boulevard since February 20. Track complete along entire route. Fleet: eight Siemens S700 vehicles manufactured in Sacramento. Expected 5,000 passengers/day across 10 stops. 4.15-mile route. $2 one-way/$5 day pass. 6 AM-11 PM daily.")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury: 4 DAYS
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 26 update:** Grand Jury response deadline June 30 — 4 DAYS remaining. County must earmark sufficient discretionary funds toward homelessness prevention by deadline. Grand Jury report emphasized shift from reactive (shelters, encampment clearances) to preventative approaches (rental assistance, early intervention). OC completed 1,544 permanent supportive housing units with 1,811 more planned. PIT Count: 6,321 (down 13.7%) — for the first time, more sheltered (3,256) than unsheltered (3,065). OC Registrar count TODAY. Governor county certification July 3 (7 DAYS).")
    print("  Updated OC Homelessness")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** Grand Jury homelessness response deadline June 30 — 4 DAYS. $20.9M Supportive Housing NOFA + $35.1M HHAP continue. PIT Count: 6,321 (down 13.7%) — more sheltered than unsheltered for first time. OC Registrar count TODAY — D5 outcome determines board majority and enforcement vs. services balance.")
    print("  Updated oc-homelessness-enforcement")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** $20.9M Supportive Housing NOFA application period continues. Combined with $35.1M HHAP = $56M+ in housing funding. Grand Jury response deadline June 30 (4 DAYS). OC completed 1,544 units with 1,811 more planned. OC Registrar count TODAY — supervisor races affect housing funding priorities. Governor county certification July 3 (7 DAYS).")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 26 update:** General election confirmed: Valencia (D) vs Shader (R). Valencia dominated primary at 63% vs Shader 37% — only two candidates on ballot, both advance. County certification deadline July 10 (14 DAYS). OC Registrar count TODAY.")
    print("  Updated oc-state-senate-sd34")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ORGS — OC Purple Accountability
# ============================================================
print("\n=== Updating oc-purple-accountability.json ===")
oc_purple = load_json(ORGS_DIR / "oc-purple-accountability.json")

campaign = find_campaign(oc_purple, campaign_id="bos-majority-defense")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 26 update:** ⚡ OC Registrar count TODAY (June 26). D5: Dixon (R) has retaken lead at ~48.5% vs Foley (D) ~45% — lead has changed hands multiple times; ~10,000 ballots remaining. D4: Shaw (R) ~33% vs Traut (D) ~31%. Final certification July 10 (14 DAYS). Grand Jury response deadline June 30 (4 DAYS). GKN extraction STILL delayed — 36+ days; sealed trucks still haven't arrived. HB: AG seeking additional $100K/month penalties starting July 1 (5 DAYS) — on top of $50K/month already accruing. 120-day zoning deadline ~Oct 14."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 26 update:** Becerra (D) vs Hilton (R) for governor — primary results nearly final (Becerra 28%, Hilton 25%). Hilton enters as significant underdog; Democrats outnumber Republicans 2-to-1 in CA. Valencia (D) 63% vs Shader (R) 37% for SD-34. County certification July 3 (7 DAYS) for governor, July 10 (14 DAYS) for local. OC Registrar count TODAY."
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
        "\n\n**June 26 update:** HB housing element adopted June 16 (6-1) — HCD certification pending. Court-ordered $50K/month fines accruing; total ~$450K+. ⚡ AG seeking additional $100K/month penalties starting July 1 (5 DAYS) — after 3 months, court may triple; after that, multiply by six and appoint receiver. 120-day zoning deadline = ~October 14. Only 1,187 of 5,845 required units permitted. Four Builder's Remedy applications (696 units) in pipeline. OC Registrar count TODAY — D5 razor-thin; board majority affects housing enforcement. Grand Jury deadline June 30 (4 DAYS). Governor certification July 3 (7 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 26 update:** Oak Creek Golf Course conversion: environmental and traffic reviews underway; public hearings expected late 2026. Irvine Company revised plan: 50-acre nature park + ~3,000 housing units. November council elections (3 seats + mayor) critical for housing direction. OC Registrar count TODAY. Grand Jury deadline June 30 (4 DAYS)."
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
        "\n\n**June 26 update:** GKN extraction STILL delayed — 36+ days post-incident; sealed trucks still haven't arrived. Air monitoring continues with no exceedances. GKN preparing partial production restart while under three criminal investigations. 44+ lawsuits filed. OC Registrar count TODAY — D5 razor-thin; supervisor races control county budget for childcare/family services. Grand Jury response deadline June 30 (4 DAYS). Governor county certification July 3 (7 DAYS)."
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
        "\n\n**June 26 update:** Filing period opens July 19 (23 DAYS). At least 3 candidates declared for D1 (Anderson, Brown, Rogers) — most competitive open race since 2014. Bond shapes race dynamics — council majority directed ~$400M package; Mayor Watson opposes; task force proposed up to $766.5M. Staff presents July 23. Community survey drew 53,000+ responses. Council on recess until July 23 (27 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 26 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. TX Supreme Court denied Austin United convention center petition April 2 — legal precedent for infrastructure projects. Phase 1: 9.8-mile surface line, 15 stations, trains every 5 min. Full cost $8B+. ATP continues design, property acquisition ($230M for 18 parcels). Convention center: structural steel positioning beginning this month; excavation through August. Council on recess until July 23 (27 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 26 update:** Rezoning continues for 445-acre site. Bond: housing ($200M) excluded from ~$400M direction. Council on recess until July 23 (27 DAYS)."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 26 update:** ⚡ DBC: zero applications submitted since June 1 launch — market conditions cautious despite strong policy framework. DDB400 (750 ft max downtown) accepting applications since June 8; DDB850 (1,200 ft max) requires rezoning — both require 5% affordable units. SB 840 multifamily by-right in commercial zones. Missing middle draft ordinances due March 2027. Bond: housing ($200M) excluded from ~$400M direction. Council on recess until July 23 (27 DAYS)."
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
        "\n\n**June 26 update:** Sunrise Navigation Center named tentative operator — council vote July 23 (27 DAYS). Sunrise has rehoused 800 people in 2026. Facility at 2401 S. I-35 ($4.3M) expected to open late summer/early fall 2026. AT-Home Initiative ($6.7M, 5-year) proposals under review — awards September. Bond: shelter infrastructure NOT in ~$400M direction. CDBG comment through July 20; hearing July 14 (18 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 26 update:** 30+ homicides in 2026 — tracking slightly below 2025 pace. APD has 330+ sworn officer vacancies (~1,819 of ~2,120 authorized). Chief Davis says staffing will stabilize in 2-3 years. 157th cadet class mid-training. Council on recess until July 23 (27 DAYS)."
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
        "\n\n**June 26 update:** ⚡ $17.65M childcare expansion approved — 25 contracts serving 5,200+ children, 180 providers supported. Nearly 300 scholarships issued, target 1,000 by October. Wait times cut from 2 years to months. Families pay ≤7% of income. Infant/toddler care and nontraditional-hours coverage remain key gaps. CDBG comment through July 20; hearing July 14 (18 DAYS). Bond: housing ($200M) excluded from ~$400M direction."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 26 update:** $17.65M childcare expansion approved. Bond: task force proposed up to $766.5M; council majority directed ~$400M. Council on recess until July 23 (27 DAYS). Filing period for council races opens July 19 (23 DAYS)."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-26T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-26T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-26T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-26T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-26T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
