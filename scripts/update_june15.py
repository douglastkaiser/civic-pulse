#!/usr/bin/env python3
"""
June 15, 2026 updates for all issue and organization data files.
Key developments since June 14:
  - NYC: ⚡ EARLY VOTING DAY 3 — Monday polls open 9 AM - 5 PM; Tue-Wed extended hours
    10 AM - 8 PM; primary June 23 (8 DAYS); CD-7 Valdez (DSA) still at 80% on prediction markets
  - OC D5: Dixon (R) lead steady at ~48.5% vs Foley (D) ~45.4%; OC Registrar next update
    TOMORROW (June 16) at 5 PM — first update since June 12
  - OC D4: Shaw (R) ~33% vs Traut (D) ~31%; both advance to November
  - Austin AISD: Board vote still scheduled June 18 (3 DAYS) — no formal postponement
    announced; delay to June 25 remains under discussion; boundary realignment workshops
    TOMORROW (June 16); deficit at $95M general fund
  - Austin Bond: Survey open through June 23 (8 DAYS)
  - HB Housing: Vote TOMORROW June 16 — $50K/month fines accruing; $310K+ total owed
  - Garden Grove: SBA Business Recovery Center opens TOMORROW at 12966 Euclid St;
    regular council meeting TOMORROW (June 16)
  - Madison: ⚡ Plan Commission reviewing SE & SW Area Plans TODAY; council vote June 23 (8 DAYS)
  - Travis County: Raising Travis County virtual town hall TOMORROW (June 16) at 6 PM
  - Cambridge: ~62 days remaining in ShotSpotter removal window
  - Brookline: No new developments
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
austin["last_scraped"] = "2026-06-15T12:00:00Z"

# AISD: vote in 3 days, workshops tomorrow
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Board vote on $181M budget shortfall remains on the June 18 agenda — 3 DAYS — no formal postponement announced, though board members discussed delaying to June 25 at the June 11 session. General fund deficit at $95M; 558 positions affected. Boundary realignment community workshops TOMORROW (June 16) and June 22-23 — these will shape the school consolidation map. CDBG public comment opens June 17 (2 DAYS). Raising Travis County virtual town hall TOMORROW (June 16) at 6 PM. Travis County offices closed June 18-19 for Juneteenth.")
    print("  Updated atx-aisd-budget-crisis")

# Pct 4: town hall TOMORROW
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Raising Travis County virtual town hall TOMORROW (June 16) at 6 PM — Morales expected to discuss the $17.65M childcare expansion. CDBG public comment opens June 17 (2 DAYS) through July 20. Travis County offices closed June 18-19 for Juneteenth. AISD board vote on $181M shortfall still scheduled June 18 (3 DAYS) — no formal delay announced.")
    print("  Updated tc-pct4-runoff")

# Bond: survey 8 DAYS remaining
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Bond community input survey open through June 23 — 8 DAYS remaining. Top priorities in 2,000+ responses: transportation (19.8%), housing & homelessness (18.5%), parks (16.3%); ~70% support a property tax increase. Council on recess until July 23 — final bond vote that day. AISD board vote on $181M shortfall June 18 (3 DAYS). Boundary realignment workshops TOMORROW (June 16).")
    print("  Updated atx-2026-bond")

# D1 Election: filing countdown
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Filing period opens July 19 (34 DAYS). Filing deadline August 17. First day to file in person is Monday, July 20. At least 2 candidates formally filed for the open D1 seat (Harper-Madison term-limited). Election Day November 3. Bond survey closes June 23 (8 DAYS). AISD board vote June 18 (3 DAYS) — the $95M general fund deficit and 558 position cuts are becoming a central campaign issue.")
    print("  Updated atx-d1-election")

# Homelessness: navigation center
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** AT-Home Initiative ($6.7M, 5-year) — city in review/selection phase. Navigation Center at 2401 S. I-35 Frontage Rd on track for late summer/early fall opening. Bond final vote July 23 — shelter infrastructure NOT in ~$390M direction. AISD board vote June 18 (3 DAYS). Travis County offices closed June 18-19 for Juneteenth.")
    print("  Updated atx-hso-plan-adopted")

# Project Connect: legal unchanged
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Legal status unchanged — trial halted per TX Supreme Court May 22 ruling; Judge Shepperd must rule on AG Paxton's jurisdictional plea. ATP achieved federal Record of Decision — key NEPA milestone. ATP expects three major contracts in 2026. Council on recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# Childcare: town hall TOMORROW
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Raising Travis County virtual town hall TOMORROW (June 16) at 6 PM. $17.65M expansion approved; 1,000+ scholarships funded annually; wait times dropped from 2 years to months. CDBG public comment opens June 17 (2 DAYS). AISD board vote on $181M shortfall June 18 (3 DAYS) — school closures directly impact childcare access. Travis County offices closed June 18-19 for Juneteenth.")
    print("  Updated tc-childcare-funding")

# APD Staffing
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** 157th cadet class mid-training — started January 26, graduation September 18. APD remains 300+ officers short of authorized strength. AISD budget includes campus police cuts — board vote June 18 (3 DAYS). Council on recess until July 23.")
    print("  Updated atx-apd-staffing-audit")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-15T12:00:00Z"

# Garden Grove: SBA center opens TOMORROW, council meeting TOMORROW
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 15 update:** SBA Business Recovery Center opens TOMORROW (June 16) at 12966 Euclid St, Suite 130, Garden Grove — walk-ins welcome Mon-Fri 8 AM - 7 PM (closed June 19 for Juneteenth). Low-interest federal disaster loans available. Chemical extraction STILL delayed ~25 days after May 21 incident — no revised start date. Three-agency criminal investigation continues (FBI/EPA, OC DA, Cal/OSHA). 44+ lawsuits filed. Regular Garden Grove council meeting TOMORROW (June 16). OC Registrar next ballot update TOMORROW at 5 PM — first since June 12.")
    print("  Updated Garden Grove chemical crisis")

# D4: Shaw leading
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Shaw (R) leads Traut (D) — Shaw at ~33.3% (26,264 votes) vs Traut at ~31.2% (24,643 votes). Only ~9,600 ballots remaining countywide. Both advance to November general regardless. OC Registrar next update TOMORROW (June 16) at 5 PM — first since June 12. Final certification July 10. HB housing vote TOMORROW (June 16). SBA Recovery Center opens TOMORROW.")
    print("  Updated oc-bos-district-4-open-seat")

# D5: Dixon consolidated lead
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Dixon (R) lead steady at ~48.5% vs Foley (D) ~45.4% — only ~9,600 ballots remaining countywide; pool nearly exhausted. OC Registrar next update TOMORROW (June 16) at 5 PM — first count since June 12; could narrow or widen the gap. Additional updates June 18, 24, 26. Certification July 10. Both advance to November regardless — but Dixon entering as primary winner signals Republican momentum for the 3-2 board majority.")
    print("  Updated oc-bos-district-5-defense")

# Governor: Becerra extending lead
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Becerra (D) maintaining lead — at 88% of expected votes counted, gap stands at ~28% vs Hilton (R) ~25%; Steyer (D) third at ~21%, has not conceded. AP confirmed both Becerra and Hilton advancing to November. County certification deadline July 3. OC Registrar next update TOMORROW (June 16) at 5 PM. HB housing vote TOMORROW.")
    print("  Updated ca-governor-2026")

# HB: TOMORROW
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** ⚡ Huntington Beach housing element vote is TOMORROW (June 16). Revised Draft Housing Element posted June 8 — zones for ~13,000 new units. $50K/month fines actively accruing since June 1 — total fines now ~$310K+ ($10K/month Jan 2025 - May 2026 = $170K, plus $50K × ~15 days in June prorated ~$25K, plus June monthly = $50K). Court ordered Builder's Remedy project approvals within 60-90 days. All legal avenues exhausted — US Supreme Court declined to hear the case in February. Governor race: Becerra (D) extending lead, favorable for continued state housing enforcement.")
    print("  Updated oc-newsom-housing-warning (HB)")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Revenue service date remains March 2027. The $649M project continues street testing. SBA Business Recovery Center for GKN crisis opens TOMORROW (June 16). Garden Grove council meeting TOMORROW. OC Registrar next update TOMORROW at 5 PM.")
    print("  Updated oc-streetcar-launch")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-15T12:00:00Z"

# Primary: EARLY VOTING DAY 3
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** ⚡ EARLY VOTING DAY 3 — Monday, polls open 9 AM - 5 PM. Go to your assigned early voting poll site (check vote.nyc — it may differ from your Election Day location). Tomorrow and Wednesday: extended hours 10 AM - 8 PM. Early voting continues through June 21. Primary Election Day June 23 (8 DAYS). CD-7 (Velázquez seat): prediction markets show Valdez (DSA) holding at 80%, Reynoso at 22%; Emerson/PIX11 poll had Valdez 23%, Reynoso 21%, Won 13% — but 43% undecided. Strong DSA ground operation targeting early vote turnout. Key endorsements for Valdez: Mayor Mamdani and Sen. Bernie Sanders.")
    print("  Updated nyc-june-primary-2026")

# Housing: early voting context
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** ⚡ EARLY VOTING DAY 3 — Monday, polls 9 AM - 5 PM; Tue-Wed extended 10 AM - 8 PM. Primary June 23 (8 DAYS). Brooklyn council seats on the ballot will shape housing policy implementation. City of Yes ADU Program: 3,100+ homeowner applications received (deadline was June 12). Q1 2026 housing permits nearly doubled vs 2025 average.")
    print("  Updated nyc-atlantic-ave-rezoning")

# COPA: early voting
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** COPA bill language still being finalized — no hearing date yet. 26 sponsors (veto-proof). ⚡ EARLY VOTING DAY 3 — Monday, polls 9 AM - 5 PM; Tue-Wed extended 10 AM - 8 PM. Brooklyn council seats on the ballot determine whether COPA has the votes. Primary June 23 (8 DAYS).")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-15T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** ~62 days remaining in the 90-day ShotSpotter removal window (deadline mid-August 2026). Device removal/disabling underway per City Manager Huang's direction. Cambridge Police Patrol Officers Association continues to push back publicly. No council revisitation expected.")
    print("  Updated cam-shotspotter-banned")

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** CRA advancing 2400 Massachusetts Ave. — $9.375M loan to North Cambridge Partners finalized, buying out Leader Bank mortgage at 4.5% over two years. CRA total investment ~$14.375M. The project plans 56 homes + retail. Task force listening sessions this summer; CDD consultant hiring underway. Barrett v. Cambridge inclusionary zoning lawsuit in discovery — AG Campbell intervened April.")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-15T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** No new developments. Article 16 (26 Pleasant Street — 103 apartments including 15 affordable) remains POSTPONED to fall Special Town Meeting (typically November). CHC Overlay District approved 217-20. Updated ADU rules and restored inclusionary payments in effect.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Brookline remains compliant. 165 of 177 communities statewide have achieved compliance. No further actions until fall Special Town Meeting.")
    print("  Updated brk-mbta-communities-compliance")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-15T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** ⚡ Plan Commission reviewing SE and SW Area Plans TODAY. Both plans shape land use, housing density, and transportation in Madison's fastest-growing areas. Council adoption vote June 23 (8 DAYS). Public comment opportunities at each committee meeting. BRT Route B federal funding ($118M) remains in the FTA pipeline — no signed agreement yet but FTA has indicated nothing has changed.")
    print("  Updated mad-new-housing-developments")

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** Route A continues 15-minute service. Route B: $118.1M Small Starts grant remains in the FTA pipeline — FTA has indicated nothing has changed but no signed agreement. Metro Transit developing alternate approaches if federal funding falls through. SE/SW Area Plans: Plan Commission reviewing TODAY; council vote June 23 (8 DAYS).")
    print("  Updated mad-east-west-brt-construction")

idx, issue = find_issue(madison["issues"], "mad-southeast-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** ⚡ Plan Commission reviewing the Southeast Area Plan TODAY. Register for public comment at cityofmadison.com. Council adoption vote June 23 (8 DAYS). The plan focuses on mixed-use and higher density along Milwaukee Street, Cottage Grove Road, Atwood Avenue, Monona Drive, and Stoughton Road. BRT Route B federal funding ($118M) remains in the FTA pipeline.")
    print("  Updated mad-southeast-area-plan")

idx, issue = find_issue(madison["issues"], "mad-southwest-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 15 update:** ⚡ Plan Commission reviewing the Southwest Area Plan TODAY. Register for public comment at cityofmadison.com. Council adoption vote June 23 (8 DAYS). The plan includes mixed-use developments along Whitney Way, Raymond Road, Schroeder Road, and McKee Road.")
    print("  Updated mad-southwest-area-plan")

save_json(ISSUES_DIR / "madison-wi.json", madison)

# ============================================================
# ORGS — OC Purple Accountability
# ============================================================
print("\n=== Updating oc-purple-accountability.json ===")
oc_purple = load_json(ORGS_DIR / "oc-purple-accountability.json")

campaign = find_campaign(oc_purple, campaign_id="bos-majority-defense")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 15 update:** D5: Dixon (R) lead steady at ~48.5% vs Foley (D) ~45.4% — ~9,600 ballots remaining. OC Registrar next update TOMORROW (June 16) at 5 PM — first count since June 12. D4: Shaw (R) at ~33.3% vs Traut (D) ~31.2%. Certification July 10. HB housing vote TOMORROW (June 16). SBA Business Recovery Center opens TOMORROW at 12966 Euclid St, Garden Grove."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 15 update:** Governor: Becerra (D) at ~28% vs Hilton (R) ~25% with 88% counted. County certification deadline July 3. OC Registrar next update TOMORROW (June 16) at 5 PM. HB housing vote TOMORROW — $50K/month fines accruing; total owed now ~$310K+."
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
        "\n\n**June 15 update:** ⚡ Huntington Beach housing vote TOMORROW (June 16). Revised Draft Housing Element posted June 8 — zones for ~13,000 new units. $50K/month fines actively accruing since June 1; total owed ~$310K+. US Supreme Court declined to hear in February — all legal avenues exhausted. Court ordered Builder's Remedy project approvals within 60-90 days. Governor: Becerra (D) extending lead, favorable for state housing enforcement."
    )
    print("  Updated orange-housing-element")

save_json(ORGS_DIR / "oc-housing-now.json", oc_housing)

# ============================================================
# ORGS — OC Abundance Project
# ============================================================
print("\n=== Updating oc-abundance-project.json ===")
oc_abundance = load_json(ORGS_DIR / "oc-abundance-project.json")

campaign = find_campaign(oc_abundance, campaign_id="oc-childcare-desert-mapping")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 15 update:** SBA Business Recovery Center opens TOMORROW (June 16) at 12966 Euclid St, Garden Grove — low-interest disaster loans for businesses affected by GKN evacuation. Chemical extraction still delayed ~25 days post-incident. Three-agency criminal investigation continues. D5: Dixon (R) steady at ~48.5% vs Foley (D) ~45.4% — OC Registrar update TOMORROW at 5 PM. HB housing vote TOMORROW."
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
        "\n\n**June 15 update:** Filing period opens July 19 (34 DAYS); first day to file in person July 20. Filing deadline August 17. At least 2 candidates formally filed for D1 (Harper-Madison term-limited). Bond survey closes June 23 (8 DAYS). AISD board vote on $181M shortfall June 18 (3 DAYS) — no formal delay announced; general fund deficit at $95M. Council on recess until July 23."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 15 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea following TX Supreme Court May 22 ruling. ATP achieved federal Record of Decision. Three major contracts expected in 2026. Council on recess until July 23."
    )
    print("  Updated defend-project-connect")

save_json(ORGS_DIR / "austin-yimby-action.json", atx_yimby)

# ============================================================
# ORGS — Austin Safe & Sound
# ============================================================
print("\n=== Updating austin-safe-and-sound.json ===")
atx_safe = load_json(ORGS_DIR / "austin-safe-and-sound.json")

campaign = find_campaign(atx_safe, campaign_id="hso-strategic-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 15 update:** AT-Home Initiative — city in review/selection phase. Navigation Center at 2401 S. I-35 on track for late summer/early fall. AISD board vote on $181M shortfall June 18 (3 DAYS) — school closures compound homelessness risk. Bond final vote July 23 — shelter infrastructure NOT in $390M direction."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 15 update:** 157th cadet class mid-training (started Jan 26) — graduation September 18. APD remains 300+ officers short. AISD $181M shortfall includes campus police cuts — board vote June 18 (3 DAYS). Council on recess until July 23."
    )
    print("  Updated apd-staffing-monitoring")

save_json(ORGS_DIR / "austin-safe-and-sound.json", atx_safe)

# ============================================================
# ORGS — Austin Abundance Project
# ============================================================
print("\n=== Updating austin-abundance-project.json ===")
atx_abundance = load_json(ORGS_DIR / "austin-abundance-project.json")

campaign = find_campaign(atx_abundance, campaign_id="childcare-desert-mapping")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 15 update:** Raising Travis County virtual town hall TOMORROW (June 16) at 6 PM. $17.65M expansion approved; 1,000+ scholarships annually; wait times down from 2 years to months. CDBG public comment opens June 17 (2 DAYS). AISD board vote on $181M shortfall June 18 (3 DAYS) — school closures impact childcare access. Travis County offices closed June 18-19 for Juneteenth."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-15T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-15T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-15T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-15T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-15T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
