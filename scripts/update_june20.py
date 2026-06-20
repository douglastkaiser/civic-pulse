#!/usr/bin/env python3
"""
June 20, 2026 updates for all issue and organization data files.
Key developments since June 19:
  - Austin: Offices reopen after Juneteenth; AISD budget fallout continues
  - Austin: ⚡ Sunrise Homeless Navigation Center selected as tentative operator
    for South Austin facility — council vote July 23
  - Austin: Bond survey closes June 23 (3 DAYS); final vote July 23 (33 DAYS)
  - Austin: D1 filing period opens July 19 (29 DAYS)
  - OC: No registrar update today — next count June 24
  - OC: Dixon (R) leads Foley (D) in D5; Shaw (R) vs Traut (D) in D4
  - OC: Garden Grove GKN chemical extraction ~30 days delayed; council June 23
  - OC: HB housing element adopted June 16 — HCD review pending
  - OC: Grand Jury homelessness response deadline June 30 (10 DAYS)
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
austin["last_scraped"] = "2026-06-20T12:00:00Z"

# AISD: Post-vote fallout
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** AISD offices reopen after Juneteenth. Budget approved 7-1 on June 18 at $205M — now being filed with TEA by end of June. 558 positions eliminated; impacted non-certified staff receiving formal notifications this week. Last-minute amendment preserved full-time librarians (~$1M from fund balance). Boundary realignment virtual workshops June 22-23 — will shape school consolidation map for affected campuses. The $205M in cuts (up from original $181M) reflects declining property values and enrollment losses (~3,000 students). District anticipates needing another loan in September for payroll. Bond survey closes June 23 (3 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** Filing period opens July 19 (29 DAYS). First day to file in person July 20. Filing deadline August 17. At least 8 candidates declared — the most competitive open D1 race since geographic representation began in 2014. Semi-annual campaign finance filings due in July will reveal fundraising trajectories. Bond survey closes June 23 (3 DAYS). AISD boundary realignment workshops June 22-23. Council on recess until July 23. Election Day November 3.")
    print("  Updated atx-d1-election")

# Bond: survey 3 DAYS
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** Bond community input survey closes June 23 — 3 DAYS remaining. 53,000+ individual responses so far; top priorities: transportation (19.8%), housing & homelessness (18.5%), parks (16.3%); ~70% support a property tax increase. The ~$390M bond direction (parks, transportation, community facilities) does NOT include housing. Council on recess until July 23 — final bond vote that day (33 DAYS). City Manager Broadnax to present bond proposal at July 23 meeting.")
    print("  Updated atx-2026-bond")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 order. No new court filings. ATP continues design work, property acquisition ($230M for 18 parcels), and contract advancement under federal Record of Decision. Three major contracts expected in 2026: light rail infrastructure, O&M facility, and vehicle procurement. Council on recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# HSO: ⚡ Sunrise selected as operator
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** ⚡ BREAKING: Sunrise Homeless Navigation Center selected as tentative operator for the South Austin Housing Navigation Center at 2401 S. I-35 — the city's FIRST city-owned navigation center. Sunrise, the largest homelessness services provider in central Texas (800+ people rehoused in 2026), was chosen through competitive evaluation. Council must approve the recommendation on July 23 — the same meeting as the bond final vote. The 13-member Center Advisory Board (formed from 69 applicants) will help shape operations. Up to $250K in city funding for initial 12-month term. AT-Home Initiative ($6.7M, 5-year) proposals still under review — contracts for up to 3 providers starting September 2026. AISD boundary realignment workshops June 22-23. Bond survey closes June 23 (3 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** 157th cadet class mid-training — graduation September 18. APD remains 300+ officers short of authorized strength (~1,819 of ~2,120 authorized). AISD budget approved at $205M including campus police cuts — reduced school police could increase demand on APD patrol resources near affected campuses. Council on recess until July 23.")
    print("  Updated atx-apd-staffing-audit")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** $17.65M Raising Travis County childcare expansion continues on track — nearly 300 scholarships issued, target 1,000 by October. Wait times dropped from 2 years to months. AISD boundary realignment workshops June 22-23 — school closures directly impact childcare access patterns. CDBG public comment continues through July 20; public hearing July 14 at 9 AM. Grand Jury homelessness response deadline June 30 (10 DAYS).")
    print("  Updated tc-childcare-funding")

# Pct 4
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** Morales serving as Pct 4 Commissioner — voted on additional Raising Travis County childcare contracts in his first week. CDBG public comment continues through July 20; public hearing July 14 at 9 AM. Bond survey closes June 23 (3 DAYS). AISD boundary realignment workshops June 22-23.")
    print("  Updated tc-pct4-runoff")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** Rezoning process continues for 445-acre Jimmy Clay/Roy Kizer site (5,000-15,000 unit potential). Council on recess until July 23. AISD budget approved at $205M — south Austin school closures and boundary realignment (workshops June 22-23) could reshape demand patterns for family housing on this site.")
    print("  Updated atx-golf-course-rezone")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** Citywide density bonus program in effect since May 22 approval. Developers can seek 15-60 feet of additional height in exchange for affordable housing. The Real Deal monitoring DBC uptake — early applications being tracked as the key indicator of whether the framework produces actual housing. Council on recess until July 23.")
    print("  Updated atx-density-bonus-approved")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** Development rules overhaul implementation continuing — minimum lot sizes reduced to 1,800 sq ft citywide, missing middle zoning districts created. SB 840 compliance driving additional changes. Council on recess until July 23.")
    print("  Updated atx-development-rules-overhaul")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** Construction continues on the $1.6B convention center — on track for late 2028 opening with ~620,000 sq ft of rentable space (70% increase). TX Supreme Court denied Austin United PAC's appeal April 2, exhausting legal options. PAC organizing new petition for November 2026 ballot. Council on recess until July 23.")
    print("  Updated atx-convention-center")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-20T12:00:00Z"

# D5: no registrar update today
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** No OC Registrar update today — next scheduled count June 24 at 5 PM. Dixon (R) leads Foley (D) ~48.96% to ~45.08% in latest count. Remaining ballots are cure-period and signature-verification returns — pool nearly exhausted. Both advance to November regardless. Additional counts June 24, 26. Final certification July 10. Becerra (D) +21 over Hilton (R) in first general poll may boost Democratic turnout in November. If Dixon wins November, the board flips to Republican majority — affecting $10.8B budget, housing enforcement, and homelessness investment.")
    print("  Updated oc-bos-district-5-defense")

# D4: no update today
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** No OC Registrar update today — next count June 24 at 5 PM. Shaw (R) and Traut (D) both advancing to November general. Additional counts June 24, 26. Final certification July 10. Garden Grove GKN chemical extraction still delayed ~30 days post-incident; next council meeting June 23 (3 DAYS). SBA Business Recovery Center open.")
    print("  Updated oc-bos-district-4-open-seat")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** General election confirmed: Becerra (D) vs Hilton (R). First general poll: Becerra +21 points among likely voters (52% to 31%). Democrats outnumber Republicans nearly 2-to-1 statewide. Hilton has vowed to cut income taxes, slash environmental regulations, and boost oil drilling — a Hilton win could weaken state housing enforcement (RHNA, Builder's Remedy, AG referrals). County certification deadline July 3 for governor, July 10 for local races.")
    print("  Updated ca-governor-2026")

# HB: HCD review pending
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** HB housing element adopted June 16 (6-1) — now awaiting CA HCD review and certification. Several councilmembers signaled continued resistance via future ballot measures. Mayor McKeon cited mounting fines (~$100K+ accrued) as the primary motivator. Judge scheduled to rule next month on increasing fines from $50K to $150K/month — adoption may reduce or eliminate future penalties. HB was the ONLY noncompliant city in all of Orange County, 4.5+ years behind schedule. Becerra (D) win would maintain aggressive state housing enforcement.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove: ~30 days
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 20 update:** Chemical extraction remains delayed — ~30 days post-incident (May 21). Specialized sealed trucks for MMA transport still have not arrived; no revised start date announced. Three-agency criminal investigation continues (FBI/EPA federal, OC DA Spitzer state criminal, Cal/OSHA workplace safety). GKN pledged $5M total ($3M United Way OC Resilience Fund + $1M Red Cross + $1M community) — criticized as insufficient by Board Chairman Chaffee. 44+ lawsuits filed in OC Superior Court and US District Court. SBA Business Recovery Center open at 12966 Euclid St, Suite 130 (Mon-Fri 8 AM-7 PM). Next Garden Grove council meeting June 23 (3 DAYS) — continued accountability hearings expected.")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** Construction at 95%. Safety testing commenced June 3 — 6-12 month testing phase verifying train operations and street signal interface. Revenue service date pushed to early 2027 (OCTA targeting March 2027). $649M project funded by federal, state, and local dollars including Measure M. Eight Siemens S700 vehicles delivered; six planned for daily service. $2 one-way/$5 day pass. 6 AM-11 PM daily with extended weekend hours.")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury
idx, issue = find_issue(oc["issues"], title_keyword="Homelessness")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 20 update:** Grand Jury response deadline June 30 — 10 DAYS remaining. OC FY2026-27 budget hearings continuing. PIT Count: 6,321 (down 13.7%), more sheltered than unsheltered for first time. D5: Dixon (R) leads Foley (D) — supervisor race outcome directly affects homelessness policy and the $10.8B county budget.")
    print("  Updated OC Homelessness")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** Grand Jury homelessness response deadline June 30 — 10 DAYS. $20.9M Supportive Housing NOFA + $35.1M HHAP funding continue flowing. PIT Count: 6,321 (down 13.7%), more sheltered (3,256) than unsheltered (3,065) for first time. D5: Dixon (R) leads Foley (D) — November outcome determines board majority and whether enforcement is paired with adequate services investment.")
    print("  Updated oc-homelessness-enforcement")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** $20.9M Supportive Housing NOFA application period continues. Combined with $35.1M HHAP = $56M+ in housing funding for OC's most vulnerable. D5 supervisor race outcome affects housing funding priorities and board majority. Grand Jury response deadline June 30 (10 DAYS).")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 20 update:** General election confirmed: Valencia (D) vs Shader (R). Valencia dominated primary at 63% vs Shader 37% — heavy favorite given district's Democratic lean. His Assembly record on housing and governance remains the key evaluation. County certification deadline July 10.")
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
        "\n\n**June 20 update:** No OC Registrar update today — next count June 24. D5: Dixon (R) leads Foley (D) ~48.96% to ~45.08%. D4: Shaw (R) vs Traut (D) — both advancing. Remaining ballots nearly exhausted. Certification July 10. Grand Jury homelessness response deadline June 30 (10 DAYS). Becerra (D) +21 over Hilton (R) in first general poll could boost November Democratic turnout."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 20 update:** General election confirmed: Becerra (D) vs Hilton (R) for governor; Valencia (D) vs Shader (R) for SD-34. HB housing element adopted June 16 — HCD review pending; councilmembers signaling continued resistance via ballot measures. D5: Dixon (R) leads Foley (D) — November race determines board majority."
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
        "\n\n**June 20 update:** HB housing element adopted June 16 (6-1) — HCD review and certification pending. Several HB councilmembers signaled continued resistance via ballot measures despite mounting fines (~$100K+ accrued). Judge ruling next month on increasing fines to $150K/month. Becerra (D) +21 over Hilton (R) in first general poll — Becerra win would maintain aggressive state housing enforcement. Grand Jury response deadline June 30 (10 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 20 update:** Oak Creek Golf Course conversion: environmental and traffic reviews underway; formal public hearings expected late 2026. Irvine Company's revised plan includes 50-acre nature park + ~3,000 housing units. Former mayors gathering signatures for citizen's initiative challenging the 1988 open space designation. November council elections (3 seats + mayor) remain critical for implementation. D5 supervisor race outcome affects countywide housing coordination."
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
        "\n\n**June 20 update:** Garden Grove GKN chemical extraction still delayed ~30 days post-incident; sealed trucks not arrived. SBA Business Recovery Center open at 12966 Euclid St (Mon-Fri 8 AM-7 PM). Next Garden Grove council meeting June 23 (3 DAYS) — continued accountability hearings. Grand Jury response deadline June 30 (10 DAYS). D5: Dixon (R) leads Foley (D) — supervisor race controls county budget and childcare/family services investment."
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
        "\n\n**June 20 update:** Filing period opens July 19 (29 DAYS). First day to file in person July 20. Filing deadline August 17. At least 8 candidates declared for D1 — most competitive open-seat race since 2014. Semi-annual campaign finance filings due July will reveal fundraising landscape. AISD boundary realignment workshops June 22-23. Bond survey closes June 23 (3 DAYS). Council on recess until July 23. Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 20 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. ATP continues design work, property acquisition ($230M for 18 parcels), and contract advancement. Three major contracts expected in 2026. Council on recess until July 23."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezoning")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 20 update:** Rezoning process continues for 445-acre site. AISD boundary realignment workshops June 22-23 — south Austin school consolidation could reshape housing demand patterns. Bond survey closes June 23 (3 DAYS). Council on recess until July 23."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, keywords=["density", "bonus"])
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["housing", "advocacy"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 20 update:** Citywide density bonus program in effect since May 22 — monitoring DBC uptake as key indicator of whether framework produces actual housing. HOME Initiative implementation continuing. Bond survey closes June 23 (3 DAYS). Council on recess until July 23."
    )
    print("  Updated housing advocacy campaign")

save_json(ORGS_DIR / "austin-yimby-action.json", atx_yimby)

# ============================================================
# ORGS — Austin Safe & Sound
# ============================================================
print("\n=== Updating austin-safe-and-sound.json ===")
atx_safe = load_json(ORGS_DIR / "austin-safe-and-sound.json")

campaign = find_campaign(atx_safe, campaign_id="hso-strategic-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 20 update:** ⚡ Sunrise Homeless Navigation Center selected as tentative operator for the South Austin Housing Navigation Center at 2401 S. I-35 — the city's FIRST city-owned navigation center. Sunrise has rehoused 800+ people in 2026. Council must approve the recommendation on July 23. 13-member Advisory Board formed from 69 applicants. AT-Home Initiative ($6.7M, 5-year) proposals under review — contracts for up to 3 providers starting September 2026. AISD budget approved at $205M — 10 school closures compound homelessness risk. Bond final vote July 23 — shelter infrastructure NOT in ~$390M direction."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if not campaign:
    campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 20 update:** 157th cadet class mid-training — graduation September 18. APD remains 300+ officers short (~1,819 of ~2,120 authorized). AISD campus police cuts could increase demand on APD patrol resources. Council on recess until July 23."
    )
    print("  Updated apd-staffing campaign")

save_json(ORGS_DIR / "austin-safe-and-sound.json", atx_safe)

# ============================================================
# ORGS — Austin Abundance Project
# ============================================================
print("\n=== Updating austin-abundance-project.json ===")
atx_abundance = load_json(ORGS_DIR / "austin-abundance-project.json")

campaign = find_campaign(atx_abundance, campaign_id="childcare-desert-mapping")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 20 update:** $17.65M Raising Travis County expansion on track — nearly 300 scholarships issued, target 1,000 by October. Wait times dropped from 2 years to months. AISD boundary realignment workshops June 22-23 — school closures directly impact childcare access patterns across affected neighborhoods. CDBG public comment through July 20; hearing July 14 at 9 AM."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 20 update:** AISD budget approved at $205M — impacts AISD employees as public employer; 558 positions eliminated. City and county parental leave policies under research. Council on recess until July 23."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-20T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-20T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-20T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-20T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-20T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
