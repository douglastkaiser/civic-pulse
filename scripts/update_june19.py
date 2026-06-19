#!/usr/bin/env python3
"""
June 19, 2026 updates for all issue and organization data files.
Key developments since June 18:
  - Austin AISD: ⚡ BUDGET APPROVED 7-1 — $205M in cuts (up from $181M);
    last-minute amendment restored full-time librarians at all campuses
    (~$1M from fund balance); 558 positions eliminated
  - Austin: Juneteenth — City, Travis County, AISD offices all CLOSED
  - OC D5: ⚡ LEAD CHANGE — Dixon (R) takes lead over Foley (D) ~48.96%
    to ~45.08% in latest registrar count; threatens 3-2 Democratic majority
  - OC D4: Shaw (R) vs Traut (D) — both advancing to November
  - NYC: Early voting Day 6 complete — 92,000+ voted citywide;
    Brooklyn 26,464; early voting through June 21; Primary Day June 23 (4 DAYS)
  - Madison: SE & SW Area Plans council vote June 23 (4 DAYS)
  - Cambridge: ~58 days in ShotSpotter 90-day removal window
  - Governor race: Becerra (D) vs Hilton (R) confirmed for November
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
austin["last_scraped"] = "2026-06-19T12:00:00Z"

# AISD: BUDGET APPROVED
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** ⚡ AISD BUDGET APPROVED 7-1 — Board passed $205M in cuts last night (up from $181M originally planned). Last-minute amendment restored full-time librarians at all campuses (~$1M investment from the district's fund balance). One trustee abstained. 558 positions eliminated including teachers, counselors, campus police, part-time assistant principals. Key strategies: $60M from selling/monetizing four AISD properties, $31M from larger class sizes, $17M from central office cuts, $31M through attrition, ~$21M from 10 campus closures approved in November. Budget must be filed with TEA by end of June. Juneteenth — AISD offices CLOSED today.")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election: AISD fallout context
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Juneteenth — city offices CLOSED. ⚡ AISD budget approved 7-1 last night at $205M in cuts (up from $181M) — school closures and budget pain are defining campaign issues for all 5 open seats. Filing period opens July 19 (30 DAYS). Bond survey closes June 23 (4 DAYS). Council on recess until July 23.")
    print("  Updated atx-d1-election")

# Bond: survey 4 DAYS remaining
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Juneteenth — city offices CLOSED. Bond community input survey closes June 23 — 4 DAYS remaining. ⚡ AISD budget approved 7-1 at $205M in cuts — property tax burden conversation intensifies as bond election approaches. Council on recess until July 23 — final bond vote that day. City Manager Broadnax to present bond proposal at July 23 meeting; latest draft includes up to $700M across city services.")
    print("  Updated atx-2026-bond")

# Project Connect: unchanged, context
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Juneteenth — offices CLOSED. Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 order. No new court filings. ATP continues design work and property acquisition under federal Record of Decision. Council on recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# HSO: Juneteenth
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Juneteenth — city and county offices CLOSED. ⚡ AISD budget approved 7-1 at $205M — 10 school closures and 558 position cuts will compound homelessness pressure on families. South Austin Navigation Center on track for late summer/early fall opening. AT-Home Initiative proposals under review — contracts for up to 3 providers starting September 2026.")
    print("  Updated atx-hso-plan-adopted")

# APD: Juneteenth
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Juneteenth — city offices CLOSED. ⚡ AISD budget approved 7-1 at $205M — includes campus police position cuts. APD remains 300+ officers short. 157th cadet class mid-training — graduation September 18. Council on recess until July 23.")
    print("  Updated atx-apd-staffing-audit")

# Childcare: AISD impact
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Juneteenth — Travis County offices CLOSED. ⚡ AISD budget approved 7-1 at $205M in cuts — 10 school closures directly impact childcare access and family stability across affected neighborhoods. $17.65M Raising Travis County childcare expansion continues; nearly 300 kids have received scholarships. CDBG public comment through July 20; hearing July 14.")
    print("  Updated tc-childcare-funding")

# Pct 4: Juneteenth
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Juneteenth — Travis County offices CLOSED. ⚡ AISD budget approved 7-1 at $205M. CDBG public comment continues through July 20; hearing July 14. Bond survey closes June 23 (4 DAYS).")
    print("  Updated tc-pct4-runoff")

# Golf course: no change
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Juneteenth — city offices CLOSED. Rezoning process continues for 445-acre Jimmy Clay/Roy Kizer site (5,000-15,000 unit potential). Council on recess until July 23. ⚡ AISD budget approved 7-1 at $205M — school closures in south Austin could accelerate demand for family housing on this site.")
    print("  Updated atx-golf-course-rezone")

# Development rules / density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Juneteenth — city offices CLOSED. Citywide density bonus program in effect since May 22 approval. New rules allow additional 15-60 feet of height depending on zoning and proximity to residential uses. Council on recess until July 23.")
    print("  Updated atx-density-bonus-approved")

idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Juneteenth — city offices CLOSED. Development rules overhaul implementation continuing. SB 840 compliance driving changes to floor-area ratio regulations. Council on recess until July 23.")
    print("  Updated atx-development-rules-overhaul")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-19T12:00:00Z"

# D5: LEAD CHANGE — Dixon takes lead
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** ⚡ LEAD CHANGE — Dixon (R) has pulled ahead to ~48.96% vs Foley (D) at ~45.08% in the latest OC Registrar count, reversing Foley's earlier slim lead. This threatens the 3-2 Democratic majority on the Board of Supervisors. Remaining ballots are signature-verification and cure-period returns — pool nearly exhausted. Both advance to November runoff regardless. Additional registrar counts June 24, 26. Final certification July 10. Becerra (D) +21 over Hilton (R) in first general poll may help Foley in November but the primary margin sets the narrative.")
    print("  Updated oc-bos-district-5-defense")

# D4: both advance
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Shaw (R) and Traut (D) both advancing to November general. Ballot pool nearly exhausted — additional counts June 24, 26. Final certification July 10. ⚡ D5: Dixon (R) has taken lead over Foley (D) ~48.96% to ~45.08% — threatens Democratic majority.")
    print("  Updated oc-bos-district-4-open-seat")

# Governor: general election taking shape
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** General election confirmed: Becerra (D) vs Hilton (R). First general poll shows Becerra +21 points among likely voters. Democrats outnumber Republicans nearly 2-to-1 statewide. Steyer (D) eliminated after finishing third. ⚡ D5: Dixon (R) takes lead over Foley (D) — if Hilton loses badly in November, could drag down Dixon. Certification deadline July 10.")
    print("  Updated ca-governor-2026")

# HB: state review pending
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Huntington Beach housing element adopted June 16 (6-1 vote) — but CA Housing and Community Development (HCD) must still review and certify the plan. Several councilmembers said they may continue challenging state mandates through ballot measures. Judge scheduled to rule next month on increasing fines from $50K to $150K/month — adoption strengthens city's defense. Becerra (D) win in November would maintain aggressive state housing enforcement posture.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove: cleanup still delayed
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 19 update:** Chemical extraction remains delayed — ~29 days post-incident. Specialized sealed trucks for MMA transport still have not arrived; no revised start date announced. Three-agency criminal investigation continues (FBI/EPA, OC DA, Cal/OSHA). GKN $3M donation to United Way OC Resilience Fund + $1M pledge criticized as insufficient by Board Chairman Chaffee. 44+ lawsuits filed. Next Garden Grove council meeting June 23 (4 DAYS). SBA Business Recovery Center open at 12866 Main St.")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar: unchanged
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Construction at 95%. Street testing and systems integration underway. Revenue service date pushed to early 2027 (OCTA targeting March 2027). $649M project. ⚡ D5: Dixon (R) takes lead over Foley (D) — supervisor race outcome affects OCTA board composition and transit funding priorities.")
    print("  Updated oc-streetcar-launch")

# Homelessness: no change
idx, issue = find_issue(oc["issues"], title_keyword="Homelessness")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 19 update:** ⚡ D5: Dixon (R) takes lead over Foley (D) — supervisor race outcome directly affects homelessness policy and budget priorities. Grand Jury criticism of county homelessness response remains unaddressed. OC FY2026-27 budget hearings continuing.")
    print("  Updated OC Homelessness")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** $20.9M Supportive Housing NOFA application period underway. ⚡ D5: Dixon (R) takes lead over Foley (D) — supervisor race outcome affects housing funding priorities and Board majority.")
    print("  Updated oc-supportive-housing-nofa")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-19T12:00:00Z"

# Primary: Day 6 results, Day 7 Juneteenth hours
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** ⚡ EARLY VOTING DAY 7 (Juneteenth) — polls open with extended hours. Through Day 6 (June 18): 92,000+ total voters citywide; Brooklyn: 26,464 check-ins (+4,789 from Day 5). Manhattan 38,413, Queens 17,265, Bronx 8,323, Staten Island 1,882. Early voting continues through Saturday June 21. Primary Day June 23 (4 DAYS). CD-7 (Velázquez seat): Valdez still favored on prediction markets. Emerson poll: Valdez 23%, Reynoso 21%, Won 13%, 43% undecided — race remains fluid with high undecideds.")
    print("  Updated nyc-june-primary-2026")

# Housing: early voting context
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Early voting Day 7 (Juneteenth). 92,000+ voted citywide through Day 6; Brooklyn 26,464. Primary June 23 (4 DAYS). Brooklyn council seats on the ballot shape housing policy going forward.")
    print("  Updated nyc-atlantic-ave-rezoning")

# COPA
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Early voting Day 7 (Juneteenth). 92,000+ voted citywide through Day 6; Brooklyn 26,464. COPA bill — no hearing date set yet; 26 sponsors (veto-proof). Primary June 23 (4 DAYS) — council composition determines COPA's path.")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-19T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** ~58 days remaining in the 90-day ShotSpotter removal window (deadline mid-August 2026). Device removal/disabling underway. Cambridge Police Patrol Officers Association continues public opposition. No council revisitation expected.")
    print("  Updated cam-shotspotter-banned")

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Social Housing Task Force listening sessions scheduled for this summer. CDD consultant hiring underway. CRA $9.375M loan to North Cambridge Partners finalized for 2400 Mass Ave (56 homes + retail). Barrett v. Cambridge inclusionary zoning lawsuit in discovery — fact discovery deadline November 13.")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-19T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Annual Town Meeting concluded June 4. Article 16 (26 Pleasant Street — 103 apartments including 15 affordable) remains POSTPONED to fall Special Town Meeting. CHC Overlay District approved 217-20. Updated ADU rules and restored inclusionary payments in effect. No further action until fall.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Brookline remains compliant. 165 of 177 communities statewide have achieved compliance. No further actions until fall Special Town Meeting.")
    print("  Updated brk-mbta-communities-compliance")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-19T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** SE and SW Area Plans council adoption vote June 23 (4 DAYS). Both plans promote mixed-use development, higher density along major corridors. Public comment opportunity at council meeting. BRT Route B: $118.1M federal funding remains in FTA pipeline; design work continuing through 2026, construction 2027, launch 2028.")
    print("  Updated mad-new-housing-developments")

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Route A continues 15-minute service. Route B $118.1M Small Starts grant in FTA pipeline — direction unchanged. SE/SW Area Plans council vote June 23 (4 DAYS) — plans support transit-oriented density along BRT corridors.")
    print("  Updated mad-east-west-brt-construction")

idx, issue = find_issue(madison["issues"], "mad-southeast-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Council adoption vote June 23 (4 DAYS). Plan and committee input reviewed — ready for final Common Council action. Public comment opportunity at council meeting.")
    print("  Updated mad-southeast-area-plan")

idx, issue = find_issue(madison["issues"], "mad-southwest-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 19 update:** Council adoption vote June 23 (4 DAYS). Plan and committee input reviewed — ready for final Common Council action. Public comment opportunity at council meeting.")
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
        "\n\n**June 19 update:** ⚡ ALERT: LEAD CHANGE IN D5 — Dixon (R) has pulled ahead to ~48.96% vs Foley (D) at ~45.08% in latest OC Registrar count. This reverses Foley's earlier slim lead and threatens the 3-2 Democratic majority. Remaining ballots are cure-period and signature-verification returns — pool nearly exhausted. Both advance to November regardless. Additional counts June 24, 26. Certification July 10. D4: Shaw (R) vs Traut (D) — both advancing. Becerra (D) +21 over Hilton (R) in first general poll could boost Democratic turnout in November, but primary margin sets the narrative."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 19 update:** General election confirmed: Becerra (D) vs Hilton (R). First poll: Becerra +21 points among likely voters. Democrats outnumber Republicans nearly 2-to-1 statewide. HB housing element adopted June 16 — HCD review pending. ⚡ D5: Dixon (R) takes lead over Foley (D) — could shift Board dynamics on state housing mandate enforcement."
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
        "\n\n**June 19 update:** HB housing element adopted June 16 but CA HCD must still review and certify the plan — more back-and-forth likely. Several HB councilmembers signaled continued resistance via ballot measures. Judge ruling next month on increasing fines to $150K/month. ⚡ D5: Dixon (R) takes lead over Foley (D) ~48.96% to ~45.08% — if Dixon wins in November, could shift Board posture on state housing mandates."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 19 update:** ⚡ D5: Dixon (R) takes lead over Foley (D) in latest count — supervisor race affects countywide housing policy coordination. Irvine General Plan implementation continuing; Oak Creek Golf Course conversion council vote still pending.")
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
        "\n\n**June 19 update:** Garden Grove GKN chemical extraction still delayed — ~29 days post-incident; specialized trucks not arrived. FBI/EPA investigation continues. GKN $3M donation + $1M pledge criticized as insufficient. Next Garden Grove council meeting June 23 (4 DAYS). ⚡ D5: Dixon (R) takes lead over Foley (D) — supervisor race controls county budget and childcare investment priorities. SBA Business Recovery Center open."
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
        "\n\n**June 19 update:** Juneteenth — offices CLOSED. ⚡ AISD budget approved 7-1 last night at $205M in cuts (up from $181M) — 558 positions, 10 school closures. Last-minute amendment restored full-time librarians (~$1M from fund balance). School closures and budget pain are defining D1 campaign issues. Filing opens July 19 (30 DAYS). Bond survey closes June 23 (4 DAYS). Council on recess until July 23."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 19 update:** Juneteenth — offices CLOSED. Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. ATP continuing design work and property acquisition under federal Record of Decision. Council on recess until July 23."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezoning")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 19 update:** Juneteenth — offices CLOSED. Rezoning process continues for 445-acre site. ⚡ AISD budget approved 7-1 at $205M — south Austin school closures could accelerate demand for family housing on this site. Council on recess until July 23."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, keywords=["density", "bonus"])
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["housing", "advocacy"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 19 update:** Juneteenth — offices CLOSED. Citywide density bonus program in effect since May 22. ⚡ AISD budget approved 7-1 at $205M — affordability crisis deepens as school system contracts. HOME Initiative implementation continuing. Council on recess until July 23."
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
        "\n\n**June 19 update:** Juneteenth — offices CLOSED. ⚡ AISD budget approved 7-1 at $205M — 10 school closures and 558 position cuts compound homelessness risk for families. South Austin Navigation Center on track for late summer/early fall opening. AT-Home Initiative proposals under review — contracts for up to 3 providers, September 2026 start."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if not campaign:
    campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 19 update:** Juneteenth — offices CLOSED. ⚡ AISD budget approved 7-1 at $205M — includes campus police cuts. APD remains 300+ officers short (~1,819 of ~2,120 authorized). 157th cadet class graduation September 18. Council on recess until July 23."
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
        "\n\n**June 19 update:** Juneteenth — Travis County offices CLOSED. ⚡ AISD budget approved 7-1 at $205M — 10 school closures directly impact childcare access and family stability. Last-minute amendment preserved full-time librarians at all campuses. $17.65M Raising Travis County expansion on track; nearly 300 scholarships issued, target 1,000 by October. CDBG public comment through July 20."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 19 update:** Juneteenth — city offices CLOSED. ⚡ AISD budget approved 7-1 at $205M — impacts AISD employees as a public employer. City and county parental leave policies under research."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-19T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-19T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-19T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-19T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-19T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
