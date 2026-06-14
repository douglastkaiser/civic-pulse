#!/usr/bin/env python3
"""
June 14, 2026 updates for all issue and organization data files.
Key developments since June 13:
  - NYC: ⚡ EARLY VOTING DAY 2 — polls open 9 AM - 5 PM (Sunday); primary June 23 (9 DAYS);
    CD-7 prediction markets: Valdez holds at 80%, Reynoso 22%; early voting runs through June 21
  - OC D5: Dixon (R) has CONSOLIDATED lead at ~48.5% vs Foley (D) ~45.4% — only ~9,600
    ballots remaining; OC Registrar next update Monday June 16; certification July 10
  - OC D4: Shaw (R) leads Traut (D) ~33% vs ~31% in latest counts; both advance to November
  - Austin AISD: Board vote scheduled June 18 (4 DAYS) but MAY DELAY TO JUNE 25 —
    board members questioned timeline at June 11 session; deficit swelled to $95M in general
    fund; 558 positions affected; boundary realignment workshops June 16 (2 DAYS)
  - Austin Bond: Survey open through June 23 (9 DAYS); results: transportation 19.8%,
    housing 18.5%, parks 16.3%; ~70% support tax increase
  - Garden Grove: SBA Business Recovery Center opening June 16 at 12966 Euclid St;
    MMA extraction STILL delayed ~24 days post-incident; next regular council meeting June 16
  - HB Housing: Vote June 16 (2 DAYS); $50K/month fines accruing; $260K+ total owed
  - Madison: Plan Commission review TOMORROW (June 15); council vote June 23 (9 DAYS)
  - Travis County: Raising Travis County virtual town hall June 16 at 6 PM (2 DAYS)
  - Cambridge: ~63 days remaining in ShotSpotter removal window; CRA $9.375M loan finalized
  - Brookline: No new developments; 26 Pleasant St postponed to fall
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
austin["last_scraped"] = "2026-06-14T12:00:00Z"

# AISD: vote in 4 days but may delay to June 25
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Board vote on $181M budget shortfall remains scheduled for June 18 — 4 DAYS — but board members discussed DELAYING TO JUNE 25 at the June 11 information session. Several trustees questioned how they could vote just days after receiving revised numbers that showed the general fund deficit swelling to $95M, with projected reserves falling below board policy minimums. 558 positions affected districtwide. Boundary realignment workshops June 16 (2 DAYS) and June 22-23. CDBG public comment opens June 17 (3 DAYS). Travis County offices closed June 18-19 for Juneteenth. Raising Travis County virtual town hall June 16 at 6 PM (2 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# Pct 4: Morales serving, town hall 2 DAYS
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Morales serving as Pct 4 Commissioner. Raising Travis County virtual town hall June 16 at 6 PM — 2 DAYS — Morales expected to discuss the $17.65M childcare and after-school expansion he voted on in his first week. CDBG public comment opens June 17 (3 DAYS) through July 20. Travis County offices closed June 18-19 for Juneteenth. AISD board vote on $181M shortfall scheduled June 18 (4 DAYS) but may delay to June 25 — general fund deficit swelled to $95M.")
    print("  Updated tc-pct4-runoff")

# Bond: survey 9 DAYS remaining
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Bond community input survey open through June 23 — 9 DAYS remaining. 2,000+ responses received; top priorities: transportation (19.8%), housing & homelessness (18.5%), parks (16.3%). In open-ended responses, 34% named housing as Austin's most urgent issue. ~70% support a property tax increase. Mayor Watson opposes the bond, but 6 council members voted to proceed with $390M staff scenario. Council on recess until July 23 — final bond vote that day. AISD board vote on $181M shortfall scheduled June 18 (4 DAYS) but may delay to June 25.")
    print("  Updated atx-2026-bond")

# D1 Election: filing countdown
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Filing period opens July 19 (35 DAYS). Filing deadline August 17. Harper-Madison term-limited — first open D1 seat in 8 years. At least 2 candidates have formally filed; semi-annual campaign finance reports due in July. Election Day November 3. Council on recess until July 23. Bond survey open through June 23 (9 DAYS). AISD board vote scheduled June 18 (4 DAYS) but may delay to June 25 — the fiscal crisis ($95M general fund deficit, 558 positions) is becoming a central campaign issue.")
    print("  Updated atx-d1-election")

# Homelessness: navigation center update
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** AT-Home Initiative ($6.7M, 5-year) — city in review/selection phase. Navigation Center at 2401 S. I-35 Frontage Rd on track for late summer/early fall opening. 13-member Advisory Board formed from 69 applications. Bond final vote July 23 — shelter infrastructure NOT in ~$390M direction. AISD board vote on $181M shortfall June 18 (4 DAYS) but may delay to June 25. Travis County offices closed June 18-19 for Juneteenth.")
    print("  Updated atx-hso-plan-adopted")

# Project Connect: legal unchanged
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Legal status unchanged — trial halted per TX Supreme Court May 22 ruling; Judge Shepperd must rule on AG Paxton's jurisdictional plea. Project at ~10 miles/$8.2B with 15 stations. ATP achieved federal Record of Decision — key NEPA milestone. ATP expects three major contracts in 2026. Council on recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# Childcare: town hall 2 DAYS
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Raising Travis County virtual town hall June 16 at 6 PM — 2 DAYS. $17.65M expansion approved; 1,000+ scholarships funded annually for children up to 3. Wait times dropped from 2 years to months. 2,650+ students in out-of-school time programs. CDBG public comment opens June 17 (3 DAYS). AISD board vote on $181M shortfall June 18 (4 DAYS) but may delay to June 25 — school closures directly impact childcare access. Travis County offices closed June 18-19 for Juneteenth.")
    print("  Updated tc-childcare-funding")

# APD Staffing
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** 157th cadet class mid-training — started January 26, graduation September 18. APD remains 300+ officers short of authorized strength. AISD budget includes campus police cuts — board vote June 18 (4 DAYS) but may delay to June 25. Council on recess until July 23.")
    print("  Updated atx-apd-staffing-audit")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-14T12:00:00Z"

# Garden Grove: SBA recovery center, extraction still delayed
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 14 update:** ⚡ SBA Business Recovery Center opening at 12966 Euclid St, Suite 130, Garden Grove on June 16 (2 DAYS) — low-interest federal disaster loans available to small businesses and nonprofits affected by the evacuation. Walk-ins welcome; Mon-Fri 8 AM - 7 PM (closed June 19). Chemical extraction STILL delayed ~24 days after May 21 incident — sealed trucks have not arrived; no revised start date. FBI/EPA federal criminal probe, OC DA criminal investigation, and Cal/OSHA workplace safety probe continue in parallel (three-agency investigation). 44+ lawsuits filed. Next regular Garden Grove council meeting June 16 (2 DAYS). D5 supervisor race: Dixon (R) has consolidated lead over Foley (D); new supervisors will shape industrial safety oversight.")
    print("  Updated Garden Grove chemical crisis")

# D4: Shaw leading, both advance
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Shaw (R) leads Traut (D) in latest counts — Shaw at ~33% vs Traut at ~31%. Only ~9,600 ballots remaining countywide. Both advance to November general regardless. OC Registrar next scheduled update Monday June 16 at 5 PM; additional updates June 18, 24, 26. Final certification July 10. SBA Business Recovery Center for Garden Grove crisis opens June 16 (2 DAYS). HB housing vote June 16 (2 DAYS).")
    print("  Updated oc-bos-district-4-open-seat")

# D5: Dixon consolidated lead
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Dixon (R) has CONSOLIDATED her lead — latest counts show Dixon at ~48.5% vs Foley (D) at ~45.4%. Only ~9,600 ballots remaining countywide — the pool is nearly exhausted. After leading briefly around June 10, Foley has fallen back as the remaining ballots proved more evenly split than the Democratic-leaning trend earlier in the canvass. OC Registrar next update Monday June 16 at 5 PM; additional updates June 18, 24, 26. Certification July 10. Both advance to November general regardless — but Dixon entering as the primary winner signals significant Republican momentum. If Dixon wins November, Republicans retake the 3-2 board majority controlling the $10.5B budget.")
    print("  Updated oc-bos-district-5-defense")

# Governor: Becerra gap widening
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Becerra (D) extending lead — latest SoS update shows Becerra at ~26.7% vs Hilton (R) at ~26.4% with 65% counted; at 88% of expected votes, gap was ~28% to ~25%. AP confirmed both advancing to November. Steyer (D) at ~23%, has not conceded. County certification deadline July 3. OC D5: Dixon (R) consolidated lead over Foley (D) at ~48.5% vs ~45.4%. HB housing vote June 16 (2 DAYS).")
    print("  Updated ca-governor-2026")

# HB: 2 DAYS to vote
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Huntington Beach housing element vote is June 16 — 2 DAYS AWAY. Revised Draft Housing Element Update posted June 8 — the plan would zone for ~13,000 new units. $50K/month fines actively accruing since June 1 — total retroactive fines now $260K+ ($10K/month Jan 2025 - May 2026 = $170K, plus $50K × 14 days in June prorated). Court ordered Builder's Remedy project approvals within 60-90 days. All legal avenues exhausted. Governor race: Becerra (D) extending lead over Hilton (R), favorable for continued state housing enforcement.")
    print("  Updated oc-newsom-housing-warning (HB)")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Revenue service date remains March 2027. The $649M project continues street testing. Garden Grove GKN aftermath: SBA Business Recovery Center opening June 16 (2 DAYS) at 12966 Euclid St. MMA still in compromised tank ~24 days post-incident. Next Garden Grove council meeting June 16 (2 DAYS).")
    print("  Updated oc-streetcar-launch")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-14T12:00:00Z"

# Primary: EARLY VOTING DAY 2
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** ⚡ EARLY VOTING DAY 2 — polls open 9 AM - 5 PM (Sunday). Go to your assigned early voting poll site — it may differ from your Election Day location (check vote.nyc). Early voting continues through June 21. Primary Election Day June 23 (9 DAYS). CD-7 (Velázquez seat): prediction markets show Valdez (DSA) holding at 80%, Reynoso at 22%. Emerson/PIX11 poll: Valdez 23%, Reynoso 21%, Won 13% — but 43% undecided. Strong DSA ground operation targeting early vote turnout. Tomorrow (Monday June 15): polls open 9 AM - 5 PM. Tuesday-Wednesday: extended hours 10 AM - 8 PM.")
    print("  Updated nyc-june-primary-2026")

# Housing: early voting context
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** ⚡ EARLY VOTING DAY 2 — polls open 9 AM - 5 PM (Sunday). Primary June 23 (9 DAYS). Early voting continues through June 21. Brooklyn council seats on the ballot will shape housing policy implementation. City of Yes ADU Program deadline passed June 12 — 3,100+ homeowners applied. Q1 2026 housing permits nearly doubled: 28,773 units filed vs 14,338/quarter average in 2025. East 98th Street rezoning DEIS required — 786 units across six sites.")
    print("  Updated nyc-atlantic-ave-rezoning")

# COPA: early voting
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** COPA bill language still being finalized — no hearing date yet. 26 sponsors (veto-proof). ⚡ EARLY VOTING DAY 2 — polls open 9 AM - 5 PM. Brooklyn council seats on the ballot will determine whether COPA has the votes to pass. Primary June 23 (9 DAYS). Early voting continues through June 21.")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-14T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** ~63 days remaining in the 90-day ShotSpotter removal window (deadline mid-August 2026). Device removal/disabling underway per City Manager Huang's direction. Cambridge Police Patrol Officers Association continues to push back. The 5-2-2 vote on May 19 directed removal within 90 days. No council revisitation expected.")
    print("  Updated cam-shotspotter-banned")

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** CRA advancing plans for 2400 Massachusetts Ave. — finalized $9.375M loan to North Cambridge Partners, buying out the Leader Bank mortgage at 4.5% interest over two years. CRA's total investment now ~$14.375M ($5M equity + $9.375M loan). The project plans 56 homes + retail as a potential first social housing project. Task force listening sessions planned for this summer + RFI from developers. CDD consultant hiring underway. Barrett v. Cambridge inclusionary zoning lawsuit remains in discovery — AG Campbell intervened in April.")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-14T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** No new developments. Article 16 (26 Pleasant Street — 103 apartments including 15 affordable) remains POSTPONED to fall Special Town Meeting (typically November). Developer and community expected to engage in interim discussions. CHC Overlay District (Chestnut Hill West rezoning) approved 217-20. Updated ADU rules and restored inclusionary payments in effect.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Brookline remains compliant — AG approved new zoning by-laws March 23. 165 of 177 communities statewide have achieved compliance. CHC Overlay District approved, ADU rules updated. 26 Pleasant Street (103 units) postponed to fall Special Town Meeting. No further actions until fall session.")
    print("  Updated brk-mbta-communities-compliance")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-14T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Plan Commission review is TOMORROW (June 15). Agendas should now be posted — check cityofmadison.com for agenda and public comment registration. Council adoption vote June 23 (9 DAYS). Both SE and SW Area Plans shape land use, housing density, and transportation in Madison's fastest-growing areas. BRT Route B federal funding ($118M) remains at moderate-to-high risk.")
    print("  Updated mad-new-housing-developments")

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Route A continues 15-minute service. Route B: federal funding ($118.1M Small Starts grant) remains at moderate-to-high risk — no signed FTA agreement. Metro Transit developing alternate approaches if federal funding falls through. SE/SW Area Plans: Plan Commission review TOMORROW (June 15); council vote June 23 (9 DAYS). Transit-oriented development along BRT corridors central to both plans.")
    print("  Updated mad-east-west-brt-construction")

idx, issue = find_issue(madison["issues"], "mad-southeast-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Plan Commission review is TOMORROW (June 15). Agendas should now be posted — register for public comment at cityofmadison.com. Council adoption vote June 23 (9 DAYS). The plan focuses on mixed-use and higher density along Milwaukee Street, Cottage Grove Road, Atwood Avenue, Monona Drive, and Stoughton Road. BRT Route B federal funding ($118M) remains at moderate-to-high risk.")
    print("  Updated mad-southeast-area-plan")

idx, issue = find_issue(madison["issues"], "mad-southwest-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 14 update:** Plan Commission review TOMORROW (June 15). Agendas should now be posted. Council adoption vote June 23 (9 DAYS). Public comment opportunities at each committee meeting. The plan includes mixed-use developments along Whitney Way, Raymond Road, Schroeder Road, and McKee Road — one of Madison's fastest-growing areas.")
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
        "\n\n**June 14 update:** D5: Dixon (R) has CONSOLIDATED lead at ~48.5% vs Foley (D) ~45.4% — only ~9,600 ballots remaining countywide. After Foley briefly led around June 10, the remaining ballots proved more evenly split. D4: Shaw (R) leads Traut (D) ~33% vs ~31%. OC Registrar next update Monday June 16 at 5 PM. Certification July 10. If Dixon holds through November, Republicans retake the 3-2 majority. SBA Business Recovery Center for GKN crisis opening June 16 at 12966 Euclid St, Garden Grove. HB housing vote June 16 (2 DAYS)."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 14 update:** Governor: Becerra (D) extending lead — latest SoS data shows ~26.7% vs Hilton (R) ~26.4% at 65% counted; at 88% counted gap was ~28% vs ~25%. County certification deadline July 3. D5: Dixon (R) consolidated lead at ~48.5% vs Foley (D) ~45.4%. HB housing vote June 16 (2 DAYS) — $50K/month fines accruing; total owed now $260K+."
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
        "\n\n**June 14 update:** Huntington Beach housing vote June 16 — 2 DAYS. Revised Draft Housing Element posted June 8 — zones for ~13,000 new units. $50K/month fines actively accruing since June 1 — total owed now $260K+. Court ordered Builder's Remedy project approvals within 60-90 days. All legal avenues exhausted. D5: Dixon (R) consolidated lead over Foley (D) — county-level housing enforcement posture at stake. Governor: Becerra (D) extending lead, favorable for state housing enforcement."
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
        "\n\n**June 14 update:** SBA Business Recovery Center opening June 16 at 12966 Euclid St, Suite 130, Garden Grove — low-interest disaster loans for businesses affected by GKN evacuation. MMA extraction still delayed ~24 days post-incident. Three-agency criminal investigation continues (FBI/EPA, OC DA, Cal/OSHA). 44+ lawsuits filed. D5: Dixon (R) consolidated lead at ~48.5% vs Foley (D) ~45.4% — if Dixon wins November, Republicans retake 3-2 majority affecting FY27 childcare investments. HB housing vote June 16 (2 DAYS)."
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
        "\n\n**June 14 update:** Filing period opens July 19 (35 DAYS). Filing deadline August 17. At least 2 candidates formally filed for D1 (Harper-Madison term-limited). Bond survey open through June 23 (9 DAYS) — top priorities: transportation (19.8%), housing (18.5%), parks (16.3%). AISD board vote on $181M shortfall June 18 (4 DAYS) but may delay to June 25 — general fund deficit swelled to $95M. Council on recess until July 23."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 14 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. Project at ~10 miles/$8.2B with 15 stations. ATP achieved federal Record of Decision — key NEPA milestone. ATP expects three major contracts in 2026. Council on recess until July 23."
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
        "\n\n**June 14 update:** AT-Home Initiative — city in review/selection phase. Navigation Center at 2401 S. I-35 on track for late summer/early fall; operator proposals solicited (up to $250K). AISD board vote on $181M shortfall June 18 (4 DAYS) but may delay to June 25 — school closures compound homelessness risk. Bond final vote July 23 — shelter infrastructure NOT in $390M direction."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 14 update:** 157th cadet class mid-training (started Jan 26) — graduation September 18. APD remains 300+ officers short. AISD $181M shortfall includes campus police cuts — board vote June 18 (4 DAYS) but may delay to June 25. Council on recess until July 23."
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
        "\n\n**June 14 update:** Raising Travis County virtual town hall June 16 at 6 PM — 2 DAYS. $17.65M expansion approved; 1,000+ scholarships annually for children up to 3. Morales serving as Pct 4 commissioner, voting on these contracts in his first week. CDBG public comment opens June 17 (3 DAYS). AISD board vote on $181M shortfall June 18 (4 DAYS) but may delay to June 25 — school closures impact childcare access. Travis County offices closed June 18-19 for Juneteenth."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-14T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-14T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-14T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-14T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-14T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
