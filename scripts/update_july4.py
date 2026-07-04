#!/usr/bin/env python3
"""
July 4, 2026 updates for all issue and organization data files.
Key developments since July 3:
  - INDEPENDENCE DAY — all federal, state, county, and city offices CLOSED nationwide
  - Austin: July 4 holiday — city/county offices closed; fireworks at Auditorium Shores
  - Austin: Council recess continues (returns July 23 = 19 DAYS)
  - Austin: City Manager budget July 16 (12 DAYS); Filing period opens July 20 (16 DAYS)
  - Austin: Dog's Head TIRZ: Travis County vote July 14 (10 DAYS)
  - Austin: ERCOT heat wave continues — excessive heat warnings through weekend
  - OC: State certification July 10 (6 DAYS); AG HB penalties Day 4 at escalated rate
  - OC: GKN Phase 1 complete; Phase 2 timeline pending
  - OC: County faces $75M structural deficit + $400M Airport Fire liability
  - OC: BOS meetings cancelled through August
  - Brooklyn: NYC offices closed for July 4
  - Madison: City offices closed; heat wave continues; council meeting July 7 (3 DAYS)
  - Cambridge/Brookline: Offices closed; heat wave continues across Northeast
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
austin["last_scraped"] = "2026-07-04T12:00:00Z"

# Dog's Head
idx, issue = find_issue(austin["issues"], "atx-dogs-head-annexation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — all city/county offices closed. Travis County TIRZ vote July 14 (10 DAYS). City Council adoption vote July 23 (19 DAYS). Draft TIRZ plan expected next week after the holiday weekend. 2,600 acres; 12,000+ homes; projected $3.5B property tax revenue over 30 years.")
    print("  Updated atx-dogs-head-annexation")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — city offices closed. Rezoning continues for 445-acre site. Travis County TIRZ vote July 14 (10 DAYS). Council vote July 23 (19 DAYS). D1 filing opens July 20 (16 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Gas peaker plant
idx, issue = find_issue(austin["issues"], "atx-gas-peaker-plant")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — city offices closed. ERCOT excessive heat warnings continue through the weekend; 12% chance of rolling blackouts in August. Austin Energy over 70% carbon-free. Council on recess until July 23 (19 DAYS). City Manager budget July 16 (12 DAYS).")
    print("  Updated atx-gas-peaker-plant")

# HSO / homelessness
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — city offices closed. Cooling centers remain open for unhoused residents during holiday heat wave. SAHNC opening June 2027; Sunrise operator vote July 23 (19 DAYS). City Manager budget July 16 (12 DAYS). Council on recess until July 23 (19 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# AISD
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — AISD offices closed. Teacher Career Fair scheduled July 16 at Toney Burger Center (12 DAYS). Phase 1 boundary draft changes expected August 7 (34 DAYS); board vote September. Phase 2 pushed to 2028-29. City Manager budget July 16 (12 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — campaign activity paused. Filing opens July 20 (16 DAYS); deadline August 17. Semi-annual campaign finance filings due mid-July — will reveal fundraising trajectories for all declared candidates. At least 7 candidates have appointed treasurers. Election Day November 3. Council on recess until July 23 (19 DAYS).")
    print("  Updated atx-d1-election")

# Bond
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — city offices closed. Bond: ~$250M for parks and trails (largest share), remainder for transportation and community facilities. Housing ($200M) excluded. City Manager budget July 16 (12 DAYS). Final vote to place on November ballot: July 23 (19 DAYS).")
    print("  Updated atx-2026-bond")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day. DBC still zero applications after six weeks since approval. Council on recess until July 23 (19 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — courts closed. AG jurisdictional plea ruling still pending from Judge Shepperd. Legal challenge heading to Texas Supreme Court. Trump administration has not agreed to fund any new transit projects; Sen. Cornyn publicly opposes federal funding for Austin rail. Council on recess until July 23 (19 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — APD fully operational for July 4 events and fireworks security; administrative offices closed. City auditor found APD has no formal recruitment plan. City Manager budget July 16 (12 DAYS). Council on recess until July 23 (19 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — construction paused for holiday. Excavation continues through 2026. D-wall complete; first footings poured; structural steel positioning underway. Targeting LEED Gold and zero-carbon certification. On track for spring 2029 reopening — over 1 million total sq ft. Council on recess until July 23 (19 DAYS).")
    print("  Updated atx-convention-center")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — county offices closed. Travis County's $17.65M childcare contracts continue — fastest of its kind in the country. 150 childcare centers funded; 3,000 children in after-school/summer programs. City Manager budget July 16 (12 DAYS).")
    print("  Updated tc-childcare-funding")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day. DBC: zero applications in first six weeks. Minimum lot size reduced from 5,750 to 1,800 sq ft citywide — implementation ongoing. Council on recess until July 23 (19 DAYS).")
    print("  Updated atx-development-rules-overhaul")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-07-04T12:00:00Z"

# Garden Grove / GKN
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**July 4 update:** Independence Day — all offices closed. GKN Phase 1 cleanup completed July 2 — neutralized MMA removed from tanks #2 and #4. Original crisis began May 21 — 44 days ago. Phase 2 details still pending — includes remaining tank and facility remediation. Air monitoring continues with no exceedances. 44+ lawsuits filed. Three criminal investigations ongoing (FBI/EPA federal probe, OC DA Spitzer, Cal/OSHA). State certification July 10 (6 DAYS).")
    print("  Updated Garden Grove chemical crisis")

# D5
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — all offices closed. Becerra (D) vs Hilton (R) confirmed for November governor's race. Dixon (R) vs Foley (D) advancing to November general for D5; the 3-2 Democratic BOS majority hinges on this race. AG HB penalties Day 4 at escalated rate. State certification July 10 (6 DAYS). County faces $75M structural deficit + $400M Airport Fire liability. BOS cancelled through August.")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — all offices closed. Shaw (R) vs Traut (D) confirmed for November general. GKN Phase 1 cleanup completed July 2 — Phase 2 pending. State certification July 10 (6 DAYS). County faces $75M structural deficit + $400M Airport Fire liability; OCEA negotiations deadlocked. BOS cancelled through August.")
    print("  Updated oc-bos-district-4-open-seat")

# HB housing element
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — courts and government offices closed. AG HB penalties Day 4 at escalated rate ($150K/month combined — $100K AG + $50K court fines). HB has now lost 8 consecutive legal challenges to state housing mandates. State certification July 10 (6 DAYS). 120-day zoning deadline ~October 14.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — all offices closed. Governor county certification completed yesterday (July 3) — Becerra (D) vs Hilton (R) confirmed for November. Becerra ~28%, Hilton ~25% final primary results. First general election poll showed Becerra +21 points (52-31). State hasn't elected Republican governor in 20 years. State certification July 10 (6 DAYS).")
    print("  Updated ca-governor-2026")

# OC FY2027 Budget
idx, issue = find_issue(oc["issues"], "oc-fy2027-budget")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — county offices closed. County faces $75M structural deficit; tapping reserves for 4th consecutive year. OCEA labor negotiations deadlocked — supervisors took 25% pay raises while proposing zero wage increases for county workers. Teamsters Local 952 contract expired June 25. County also faces $400M estimated liability from Airport Fire. AG HB penalties Day 4 at $150K/month. BOS cancelled through August.")
    print("  Updated oc-fy2027-budget")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — testing paused for holiday. Project 95% complete per OCTA CEO Darrell Johnson. Testing phase continues — platform operations, control systems, street signal interface. Revenue service March 2027. 4.15-mile, 10-stop route. State certification July 10 (6 DAYS).")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**July 4 update:** Independence Day — all offices closed. Grand Jury response deadline passed June 30 — still no public reporting on county or city responses. County faces $75M structural deficit; OCEA negotiations deadlocked. BOS cancelled through August. State certification July 10 (6 DAYS).")
    print("  Updated OC Homelessness Grand Jury")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — all offices closed. NOFA remains open until closed, replaced, or all funds committed. State certification July 10 (6 DAYS). County faces $75M structural deficit. BOS cancelled through August.")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — all offices closed. General election confirmed: Valencia (D) vs Shader (R). Valencia dominated primary at 63% — heavy favorite given district's Democratic lean. State certification July 10 (6 DAYS).")
    print("  Updated oc-state-senate-sd34")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — all offices closed. Grand Jury response deadline passed — no public reporting on responses. County faces $75M structural deficit. GKN Phase 1 completed July 2. State certification July 10 (6 DAYS). BOS cancelled through August.")
    print("  Updated oc-homelessness-enforcement")

# Orange Housing Element
idx, issue = find_issue(oc["issues"], "oc-orange-housing-element")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — all offices closed. AG HB penalties Day 4 at escalated rate ($150K/month combined). HB has lost 8 consecutive legal challenges. State certification July 10 (6 DAYS).")
    print("  Updated oc-orange-housing-element")

# AD-68
idx, issue = find_issue(oc["issues"], "oc-ad68-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — all offices closed. State certification July 10 (6 DAYS). Valencia's move to SD-34 leaves this seat open.")
    print("  Updated oc-ad68-open-seat")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-07-04T12:00:00Z"

idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — city offices closed. NYC $125.8B FY2027 budget adopted June 30 — largest in Council history. Monitor Point must return to CPC for scope approval before full Council vote — no vote date confirmed yet. South of Prospect Plan: first neighborhood plan accounting for IBX; zoning concept map expected later 2026.")
    print("  Updated nyc-atlantic-ave-rezoning")

idx, issue = find_issue(brooklyn["issues"], "nyc-city-of-yes-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — city offices closed. ADUs now legal across all five boroughs; 3,100+ homeowner applications received. Q1 2026 housing permits nearly doubled: 28,773 units filed vs 14,338/quarter average in 2025. South of Prospect Plan: community engagement underway; zoning concept map expected later 2026.")
    print("  Updated nyc-city-of-yes-implementation")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-07-04T12:00:00Z"

idx, issue = find_issue(madison["issues"], "budget-rules-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — city offices closed. Heat wave continues across the Midwest; excessive heat warnings through the weekend. UW-Madison chilled water repairs ongoing — ~30 temporary chillers installed across 34 affected buildings. Christine Knapp starts as Madison Water Utility GM August 31 (pending Council approval). City faces $11M shortfall for 2027; agencies preparing 2% budget reductions. Next council meetings: July 7 (3 DAYS), July 21.")
    print("  Updated budget-rules-2026")

save_json(ISSUES_DIR / "madison-wi.json", madison)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-07-04T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-zoning-reform-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day — city offices closed. Doug Brown citizen petition remains de facto law until Council votes (earliest August 3). AHO changes could reduce housing production ~50% on some lots per developer warnings. Council summer recess continues.")
    print("  Updated cam-zoning-reform-implementation")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-07-04T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day. Heat emergency continues — temps forecast near 100°F through the weekend. Cooling centers remain open at Senior Center, Public Safety Building, libraries, and Evelyn Kirrane Aquatics Center. FY2027 budget maintaining existing services after override passed.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 4 update:** Independence Day. Chestnut Hill overlay approved 217-20 on May 28 — formal redevelopment application from City Realty expected later this summer; special permit review could take 9-12 months. Groundbreaking spring 2028 at earliest. 783 multifamily units + 200-room hotel. Heat emergency continues through the weekend.")
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
        "\n\n**July 4 update:** Independence Day — all offices closed. Governor county certification completed yesterday — Becerra (D) vs Hilton (R) confirmed. GKN Phase 1 complete. County faces $75M structural deficit + $400M Airport Fire liability. OCEA negotiations deadlocked. AG HB penalties Day 4 at escalated rate. State certification July 10 (6 DAYS). BOS cancelled through August."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 4 update:** Independence Day — all offices closed. Governor county certification completed yesterday — Becerra (D) vs Hilton (R) confirmed for November. Becerra +21 points in first general election poll (52-31). State certification July 10 (6 DAYS)."
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
        "\n\n**July 4 update:** Independence Day — courts and government offices closed. AG HB penalties Day 4 at escalated rate ($150K/month combined). HB has lost 8 consecutive legal challenges. State certification July 10 (6 DAYS). 120-day zoning deadline ~October 14."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 4 update:** Independence Day — all offices closed. GKN Phase 1 cleanup complete. County faces $75M structural deficit + $400M Airport Fire liability. State certification July 10 (6 DAYS). BOS cancelled through August."
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
        "\n\n**July 4 update:** Independence Day — all offices closed. GKN Phase 1 complete. County faces $75M structural deficit + $400M Airport Fire liability — threatens family services and childcare funding. State certification July 10 (6 DAYS). BOS cancelled through August."
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
        "\n\n**July 4 update:** Independence Day — campaign activity paused. Filing opens July 20 (16 DAYS); deadline August 17. Semi-annual campaign finance filings due mid-July. At least 7 candidates have appointed treasurers for D1. Bond final vote July 23 (19 DAYS). City Manager budget July 16 (12 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 4 update:** Independence Day — courts closed. AG jurisdictional plea ruling still pending from Judge Shepperd. Legal challenge heading to Texas Supreme Court. Federal funding uncertainty continues — Trump admin has not agreed to fund any new transit projects. Council on recess until July 23 (19 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**July 4 update:** Independence Day. Draft TIRZ plan expected next week after the holiday weekend. Travis County TIRZ vote July 14 (10 DAYS); council vote July 23 (19 DAYS)."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 4 update:** Independence Day. DBC still zero applications after six weeks. Council on recess until July 23 (19 DAYS)."
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
        "\n\n**July 4 update:** Independence Day — city offices closed. Cooling centers remain open for unhoused residents during heat wave. SAHNC operator vote July 23 (19 DAYS). City Manager budget July 16 (12 DAYS). Council on recess until July 23 (19 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 4 update:** Independence Day — APD fully operational for July 4 events and fireworks security; administrative offices closed. City auditor: APD has no formal recruitment plan. Heat wave continues — ERCOT warns 12% rolling blackout chance in August. City Manager budget July 16 (12 DAYS). Council on recess until July 23 (19 DAYS)."
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
        "\n\n**July 4 update:** Independence Day — county offices closed. Travis County's $17.65M childcare expansion continues — fastest of its kind in the country. 150 centers funded; 3,000 children in after-school/summer programs. City Manager budget July 16 (12 DAYS). Council on recess until July 23 (19 DAYS)."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**July 4 update:** Independence Day. City Manager budget July 16 (12 DAYS). D1 filing opens July 20 (16 DAYS). Council on recess until July 23 (19 DAYS)."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-07-04T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-07-04T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-07-04T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-07-04T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-07-04T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
