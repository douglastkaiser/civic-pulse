#!/usr/bin/env python3
"""
June 24, 2026 updates for all issue and organization data files.
Key developments since June 23:
  - Austin: Bond survey closed June 23 — 53,000+ responses; city staff compiling for July 23
  - Austin: AISD boundary workshops completed June 22-23; comment card open through July 31
  - Austin: D1 filing period opens July 19 (25 DAYS); council recess until July 23 (29 DAYS)
  - Austin: Project Connect legal status unchanged; convention center D-wall continues
  - Austin: Raising Travis County at $51.7M+; CDBG comment through July 20
  - OC: OC Registrar ballot count TODAY (June 24) — D5 razor-thin: Foley (D) ~47.0% vs Dixon (R) ~46.8%
  - OC: Garden Grove council met June 23 — GKN accountability hearings; chemical extraction
    trucks reported finally arriving, extraction expected to begin within days
  - OC: Grand Jury homelessness response deadline June 30 (6 DAYS)
  - OC: HB housing element — HCD certification pending; $50K/month fines accruing
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
austin["last_scraped"] = "2026-06-24T12:00:00Z"

# AISD: Boundary workshops completed
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** AISD boundary realignment workshops completed June 22-23 — two virtual sessions presented 'Oak' and 'Elm' draft maps showing different elementary-to-middle-to-high pathways after 10 school closures. Online comment card open through July 31. Revised draft map to trustees in August; board vote expected September; implementation August 2027. Bond survey closed June 23 — staff compiling 53,000+ responses for council return July 23 (29 DAYS). CDBG public comment continues through July 20; hearing July 14 (20 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Filing period opens July 19 (25 DAYS). First day to file in person July 20. Filing deadline August 17. At least 8 candidates declared — most competitive open D1 race since geographic representation began in 2014. Semi-annual campaign finance filings due in July will reveal fundraising trajectories. AISD boundary workshops completed June 22-23 — comment card open through July 31. Bond survey closed — staff compiling 53,000+ responses for council return July 23 (29 DAYS). Election Day November 3.")
    print("  Updated atx-d1-election")

# Bond: survey closed
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Bond community input survey CLOSED June 23 — 53,000+ individual responses from 2,000+ participants. Top priorities: transportation (19.8%), housing & homelessness (18.5%), parks (16.3%); ~70% support a property tax increase; 70%+ rated climate/sustainability 'very or somewhat important.' City staff now compiling results for presentation to council when they return from recess July 23 (29 DAYS). City Manager Broadnax to present final ~$390M bond package at that meeting. Housing ($200M) remains excluded from the current bond direction.")
    print("  Updated atx-2026-bond")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 order. No new court filings. Phase 1: 9.8-mile surface line. ATP continues design work, property acquisition ($230M for 18 parcels), and contract advancement under federal Record of Decision. Three major contracts expected in 2026. Target completion 2033. Council on recess until July 23 (29 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# HSO
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Sunrise Navigation Center tentative operator selection for South Austin Housing Navigation Center at 2401 S. I-35 — council approval vote July 23 (29 DAYS). AT-Home Initiative ($6.7M, 5-year) proposals under review — contract awards for up to 3 providers expected September 2026. AISD boundary workshops completed — school closures compound homelessness risk. CDBG public comment through July 20; hearing July 14 (20 DAYS). Bond survey closed — shelter infrastructure NOT in ~$390M bond direction.")
    print("  Updated atx-hso-plan-adopted")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** 157th cadet class mid-training — graduation September 18. APD remains 300+ officers short of authorized strength (~1,819 of ~2,120 authorized). 156th cadet class graduated May 1. Council on recess until July 23 (29 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Raising Travis County at $51.7M+ distributed — 25 contracts serving 9,402 children/youth across Travis County. Nearly 300 scholarships issued, target 1,000 by October. Families pay ≤7% of income; eligible up to 85% SMI (~$92K for family of four). AISD boundary workshops completed June 22-23 — school closures reshape childcare access patterns. CDBG public comment through July 20; hearing July 14 at 9 AM (20 DAYS). Bond survey closed — housing ($200M) excluded from ~$390M direction.")
    print("  Updated tc-childcare-funding")

# Pct 4
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Morales serving as Pct 4 Commissioner. $51.7M+ distributed through Raising Travis County initiative serving 9,402 children/youth. CDBG public comment through July 20; hearing July 14 at 9 AM (20 DAYS). Bond survey closed — staff compiling results. Council on recess until July 23 (29 DAYS).")
    print("  Updated tc-pct4-runoff")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** D-wall construction continues in Area E — trenching between 2nd & 3rd Streets, concrete pours and rebar cages being installed. Judge Thomas's June 18 ruling affirmed the $1.35B bond funding plan as lawful. On track for spring 2029 reopening, nearly doubling rentable space to ~620,000 sq ft. Austin United PAC organizing new petition for November 2026 ballot. Council on recess until July 23 (29 DAYS).")
    print("  Updated atx-convention-center")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Rezoning process continues for 445-acre Jimmy Clay/Roy Kizer site (5,000-15,000 unit potential). Council resolution sponsored by Fuentes, Alter, Ellis, and Laine. AISD boundary workshops completed — south Austin school consolidation reshapes housing demand for this site. Bond survey closed — staff compiling results. Council on recess until July 23 (29 DAYS). Filing period for D1 opens July 19 (25 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Citywide DBC in effect since May 22 — five tiers adding 0-60 feet of extra height. Rental projects reserve units at ≤50% MFI; homeownership at ≤80% MFI. Monitoring DBC uptake as key indicator of whether framework produces actual housing. SB 840 allows multifamily by-right in commercial zones — Austin code still updating. Council on recess until July 23 (29 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Development rules implementation continuing. SB 840 compliance: multifamily by-right in CS, GR, LO, GO districts at 36 units/acre and 45 ft. Missing middle housing draft ordinances due March 2027. Council on recess until July 23 (29 DAYS).")
    print("  Updated atx-development-rules-overhaul")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-24T12:00:00Z"

# D5: Ballot count TODAY
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** ⚡ OC Registrar ballot count TODAY (June 24) at 5 PM — D5 remains razor-thin: Foley (D) ~47.0% vs Dixon (R) ~46.8%. Lead has changed hands multiple times during canvass. ~9,500 ballots remaining countywide. Both advance to November regardless. Next count June 26. Final certification July 10 (16 DAYS). Grand Jury homelessness response deadline June 30 (6 DAYS). Becerra (D) +21 over Hilton (R) in first general governor poll may boost Democratic turnout in November. If Dixon wins November, the board flips to Republican majority — affecting $10.8B budget, housing enforcement, and homelessness investment.")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Shaw (R) and Traut (D) both advancing to November general. OC Registrar ballot count TODAY at 5 PM. Next count June 26. Final certification July 10 (16 DAYS). ⚡ Garden Grove council met June 23 — GKN accountability hearings continued; chemical extraction trucks reported finally arriving; extraction expected to begin within days (~34 days post-incident). Three-agency criminal investigation ongoing (FBI/EPA, DA Spitzer, Cal/OSHA). Grand Jury response deadline June 30 (6 DAYS).")
    print("  Updated oc-bos-district-4-open-seat")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** General election confirmed: Becerra (D) vs Hilton (R). Becerra +21 in first general poll (52-31 among likely voters). Democrats outnumber Republicans nearly 2-to-1 statewide. County certification deadline July 3 for governor, July 10 for local races. ⚡ D5 remains razor-thin — Foley (D) ~47.0% vs Dixon (R) ~46.8%; registrar count TODAY.")
    print("  Updated ca-governor-2026")

# HB: fines accruing
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** HB housing element adopted June 16 (6-1) — HCD review and certification still pending. $50,000/month fines accruing since June 2026. Total owed now ~$385K+. Judge ruling next month on further increase to $150,000/month — could reach $900K/month and receivership. Only 1,187 of 5,845 required very-low/low-income units permitted so far. Becerra (D) +21 in first general poll — Becerra win maintains aggressive state enforcement.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove: council met June 23; extraction trucks arriving
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 24 update:** ⚡ Garden Grove City Council met June 23 — continued GKN accountability hearings. Chemical extraction specialized sealed trucks reported finally arriving after ~34 days of delay since May 21 incident; extraction operation expected to begin within days. GKN employees returning to facility for safety checks as company prepares partial production restart — while under three parallel criminal investigations (FBI/EPA federal, OC DA Spitzer state, Cal/OSHA workplace safety). 6,000+ assistance applications to United Way OC. 44+ lawsuits filed. OC Registrar ballot count TODAY — D5 race directly affects county industrial safety oversight. SBA Business Recovery Center continues open Mon-Fri 8 AM-7 PM. Grand Jury response deadline June 30 (6 DAYS).")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Construction at 95%. Safety testing underway since June 3 — verifying train operations, control systems, and street signal interface. Revenue service target March 2027. Fleet: eight Siemens S700 vehicles. Expected 5,000 passengers/day across 10 stops. $2 one-way/$5 day pass. 6 AM-11 PM daily.")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury: 6 DAYS
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 24 update:** Grand Jury response deadline June 30 — 6 DAYS remaining. Recommended county earmark sufficient discretionary funds toward homelessness prevention by June 30. OC completed 1,544 permanent supportive housing units with 1,811 more planned. PIT Count: 6,321 (down 13.7%). OC Registrar count TODAY — D5 race affects homelessness policy direction. Grand Jury deadline is the nearest critical action item.")
    print("  Updated OC Homelessness")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** Grand Jury homelessness response deadline June 30 — 6 DAYS. $20.9M Supportive Housing NOFA + $35.1M HHAP continue. PIT Count: 6,321 (down 13.7%). OC Registrar count TODAY — D5 outcome determines board majority and enforcement vs. services balance in November.")
    print("  Updated oc-homelessness-enforcement")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** $20.9M Supportive Housing NOFA application period continues. Combined with $35.1M HHAP = $56M+ in housing funding. Grand Jury response deadline June 30 (6 DAYS). OC completed 1,544 units with 1,811 more planned. OC Registrar count TODAY — supervisor race affects housing funding priorities.")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 24 update:** General election confirmed: Valencia (D) vs Shader (R). Valencia dominated primary at 63%. County certification deadline July 10 (16 DAYS). OC Registrar count TODAY.")
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
        "\n\n**June 24 update:** ⚡ OC Registrar ballot count TODAY at 5 PM — D5 remains razor-thin: Foley (D) ~47.0% vs Dixon (R) ~46.8%. Lead has changed hands multiple times. ~9,500 ballots remaining. Next count June 26. Final certification July 10 (16 DAYS). D4: Shaw (R) and Traut (D) both advancing. Grand Jury response deadline June 30 (6 DAYS). Garden Grove council met June 23 — GKN chemical extraction trucks finally arriving. Becerra (D) +21 over Hilton (R) in first general poll."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 24 update:** Becerra (D) vs Hilton (R) for governor — Becerra +21 in first general poll. Valencia (D) vs Shader (R) for SD-34 — Valencia at 63%. County certification July 3 (governor), July 10 (local). OC Registrar count TODAY — D5 razor-thin."
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
        "\n\n**June 24 update:** HB housing element adopted June 16 (6-1) — HCD certification pending. $50K/month fines accruing; total owed ~$385K+. Judge ruling next month on $150K/month increase. Only 1,187 of 5,845 required very-low/low-income units permitted so far — adoption is step one, implementation is the fight. Four Builder's Remedy applications in Orange (696 units) remain in pipeline. OC Registrar count TODAY — D5 razor-thin; board majority affects housing enforcement posture. Grand Jury deadline June 30 (6 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 24 update:** Oak Creek Golf Course conversion: environmental and traffic reviews underway; public hearings expected late 2026. Irvine Company revised plan: 50-acre nature park + ~3,000 housing units. November council elections (3 seats + mayor) critical. OC Registrar count TODAY — D5 razor-thin; countywide housing coordination affected by supervisor race."
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
        "\n\n**June 24 update:** Garden Grove council met June 23 — GKN accountability hearings continued; chemical extraction trucks finally arriving after ~34 days; extraction expected within days. GKN preparing partial production restart while under three criminal investigations. 6,000+ assistance applications to United Way OC. SBA Business Recovery Center open. OC Registrar count TODAY — D5 razor-thin; supervisor race controls county budget and childcare/family services investment. Grand Jury response deadline June 30 (6 DAYS)."
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
        "\n\n**June 24 update:** Filing period opens July 19 (25 DAYS). At least 8 candidates declared for D1. AISD boundary workshops completed June 22-23 — comment card open through July 31. Semi-annual campaign finance filings due in July. Bond survey closed — staff compiling 53,000+ responses. Council on recess until July 23 (29 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 24 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. Phase 1: 9.8-mile surface line. ATP continues design, property acquisition ($230M for 18 parcels), contract advancement. Three major contracts expected in 2026. Target completion 2033. Convention center D-wall construction continuing — June 18 bond ruling provides positive precedent. Council on recess until July 23 (29 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 24 update:** Rezoning continues for 445-acre site. AISD boundary workshops completed — south Austin school consolidation reshapes housing demand. Bond survey closed — staff compiling results. Council on recess until July 23 (29 DAYS)."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 24 update:** DBC in effect since May 22 — monitoring uptake as key indicator. SB 840 allows multifamily by-right in commercial zones — Austin code still updating. Missing middle draft ordinances due March 2027. Bond survey closed — 53,000+ responses; housing/homelessness tied as top priority (18.5%) but housing ($200M) excluded from ~$390M direction. Council on recess until July 23 (29 DAYS)."
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
        "\n\n**June 24 update:** Sunrise Navigation Center tentative operator selection — council vote July 23 (29 DAYS). AT-Home Initiative ($6.7M, 5-year) proposals under review — contract awards September 2026. AISD boundary workshops completed — school closures compound homelessness risk. Bond survey closed — shelter infrastructure NOT in ~$390M bond direction; housing/homelessness tied as top priority among respondents (18.5%). CDBG public comment through July 20; hearing July 14 (20 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 24 update:** 157th cadet class mid-training — graduation September 18. APD remains 300+ officers short (~1,819 of ~2,120 authorized). Council on recess until July 23 (29 DAYS)."
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
        "\n\n**June 24 update:** Raising Travis County at $51.7M+ distributed — 25 contracts serving 9,402 children/youth. Nearly 300 scholarships issued, target 1,000 by October. Families pay ≤7% of income. AISD boundary workshops completed June 22-23 — school closures reshape childcare access patterns; comment card open through July 31. CDBG public comment through July 20; hearing July 14 at 9 AM (20 DAYS). Bond survey closed — housing ($200M) excluded."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 24 update:** AISD budget approved at $205M — 558 positions eliminated; impacts AISD employees as public employer. Raising Travis County at $51.7M+ distributed. Council on recess until July 23 (29 DAYS). Filing period for council races opens July 19 (25 DAYS)."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-24T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-24T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-24T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-24T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-24T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
