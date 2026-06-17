#!/usr/bin/env python3
"""
June 17, 2026 updates for all issue and organization data files.
Key developments since June 16:
  - NYC: ⚡ EARLY VOTING DAY 5 — polls 10 AM - 8 PM (Tue);
    62,244 voters through Day 4 citywide; Brooklyn 16,762 check-ins;
    CD-7 Valdez now at 83% on prediction markets (up from 80%); primary June 23 (6 DAYS)
  - OC D5: Foley (D) reclaims narrow lead 47.0% (85,104) vs Dixon (R) 46.8% (84,777);
    ~9,600 ballots remaining; next registrar count June 18
  - OC D4: Shaw (R) ~33% vs Traut (D) ~31%; both advance to November
  - CA Governor: First general election poll: Becerra (D) 52% vs Hilton (R) 31%
  - Austin AISD: Board vote TOMORROW June 18 — written comments due by 5 PM;
    $181M deficit, 558 positions, 11 school closures
  - Austin: CDBG public comment period OPENS TODAY (June 17) through July 20;
    Travis County offices CLOSED June 18-19 for Juneteenth
  - HB Housing: June 16 vote result not yet confirmed — fines ~$385K+ and climbing;
    $100K/month penalty possible starting July; receivership risk if noncompliant
  - Garden Grove: SBA Business Recovery Center open; next council meeting June 23;
    FBI search warrant served June 10
  - Madison: SE & SW Area Plans — council vote June 23 (6 DAYS)
  - Cambridge: ~60 days remaining in ShotSpotter removal window
  - Brookline: Community Housing funding review TODAY at 2 PM on Zoom
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
austin["last_scraped"] = "2026-06-17T12:00:00Z"

# AISD: vote TOMORROW
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Board vote on $181M budget shortfall is TOMORROW (June 18). Written public comments accepted through June 18 at 5 PM at www.austinisd.org. 558 positions affected including teachers, librarians, and campus police. Key strategies: $60M from selling/monetizing four AISD properties, $31M from increasing student-to-teacher ratios and cutting librarians, $17M from central office cuts, $31M through attrition. Budget must pass by end of June. CDBG public comment period opens TODAY (June 17) through July 20. Travis County offices CLOSED June 18-19 for Juneteenth.")
    print("  Updated atx-aisd-budget-crisis")

# Pct 4: town hall happened yesterday; CDBG opens today
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Raising Travis County virtual town hall held yesterday (June 16) — Morales discussed the $17.65M childcare expansion; nearly 300 kids have received scholarships, target 1,000 by October. CDBG public comment period opens TODAY (June 17) through July 20; public hearing July 14 at 9 AM. Draft PY26 Action Plan available for download at traviscountytx.gov. Travis County offices CLOSED June 18-19 for Juneteenth. AISD board vote TOMORROW (June 18).")
    print("  Updated tc-pct4-runoff")

# Bond: survey 6 DAYS remaining
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Bond community input survey open through June 23 — 6 DAYS remaining. 53,000+ individual responses so far. Top priorities: transportation (19.8%), housing & homelessness (18.5%), parks (16.3%); ~70% support a property tax increase. AISD board vote on $181M shortfall TOMORROW (June 18). Council on recess until July 23 — final bond vote that day.")
    print("  Updated atx-2026-bond")

# D1 Election: filing countdown
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Filing period opens July 19 (32 DAYS). First day to file in person July 20. Filing deadline August 17. At least 20 candidates have appointed campaign treasurers across the 5 open council seats (D1, D3, D5, D8, D9). Election Day November 3. Bond survey closes June 23 (6 DAYS). AISD board vote TOMORROW (June 18) — the $181M deficit and school closures are a defining campaign issue. Semi-annual campaign finance filings due in July.")
    print("  Updated atx-d1-election")

# Homelessness: navigation center RFP
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** South Austin Navigation Center at 2401 S. I-35 Frontage Rd — RFP open; up to $250K in funding available for operator. City and Travis County anticipate awarding contracts to up to 3 providers for initial 12-month term beginning September 2026. AT-Home Initiative ($6.7M, 5-year) — proposals were due June 2; city in review/selection phase. AISD board vote TOMORROW (June 18). Travis County offices CLOSED June 18-19 for Juneteenth.")
    print("  Updated atx-hso-plan-adopted")

# Project Connect: legal unchanged
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Legal status unchanged — trial halted per TX Supreme Court May 22 ruling; Judge Shepperd must rule on AG Paxton's jurisdictional plea. Moody's issued tentative credit rating (straight-A grades) but based on two false assumptions: that all lawsuits had been dismissed and that Paxton had validated ATP's bond authority. ATP achieved federal Record of Decision — key NEPA milestone. Three major contracts expected in 2026. Council on recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# Childcare: CDBG opens today
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Raising Travis County town hall held yesterday (June 16 at 6 PM). $17.65M expansion approved; nearly 300 kids have received scholarships, target 1,000 by October; wait times down from 2 years to months. CDBG public comment period opens TODAY (June 17) through July 20 — draft PY26 Action Plan available at traviscountytx.gov. Public hearing July 14 at 9 AM. AISD board vote on $181M shortfall TOMORROW (June 18) — school closures directly impact childcare access. Travis County offices CLOSED June 18-19 for Juneteenth.")
    print("  Updated tc-childcare-funding")

# APD Staffing
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** 157th cadet class mid-training — started January 26, graduation September 18. APD remains 300+ officers short of authorized strength. AISD $181M shortfall includes campus police cuts — board vote TOMORROW (June 18). Council on recess until July 23.")
    print("  Updated atx-apd-staffing-audit")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-17T12:00:00Z"

# Garden Grove: SBA center open, FBI search warrant
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 17 update:** SBA Business Recovery Center now open at 12966 Euclid St, Suite 130, Garden Grove — walk-ins Mon-Fri 8 AM - 7 PM (closed June 19 for Juneteenth). FBI/EPA served search warrant at GKN facility on June 10 — seized documents on chemical storage, cooling mechanisms, and employee complaints. GKN Senior VP Steve Carlin promised community town hall at June 9 special council meeting but dodged reimbursement questions. Chemical extraction STILL delayed ~27 days post-incident. Three-agency criminal investigation continues (FBI/EPA, OC DA, Cal/OSHA). 44+ lawsuits filed including class-action. 50,000+ residents were evacuated. Next regular Garden Grove council meeting June 23.")
    print("  Updated Garden Grove chemical crisis")

# D4: Shaw leading, next count June 18
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Shaw (R) at ~33.3% vs Traut (D) at ~31.2%. Only ~9,600 ballots remaining countywide — pool nearly exhausted. Both advance to November general regardless. Next OC Registrar count June 18. Additional updates June 24, 26. Final certification July 10. Garden Grove council meeting June 23. SBA Recovery Center open.")
    print("  Updated oc-bos-district-4-open-seat")

# D5: Foley reclaims lead
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** ⚡ Foley (D) has reclaimed a narrow lead — 47.0% (85,104 votes) vs Dixon (R) 46.8% (84,777 votes). Margin: 327 votes. Only ~9,600 ballots remaining countywide — every batch matters. Neither candidate will reach 50%, so both advance to November runoff. Next OC Registrar count June 18. Final certification July 10. First general election poll shows Becerra (D) leading Hilton (R) 52-31 for governor — Democratic turnout strength could help Foley in November.")
    print("  Updated oc-bos-district-5-defense")

# Governor: first general election poll
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** ⚡ First general election poll: Becerra (D) 52% vs Hilton (R) 31% — Becerra holds a commanding 21-point lead among likely voters. Registered Democrats outnumber Republicans nearly 2-to-1 statewide. Final primary tallies (88% counted): Becerra ~28%, Hilton ~25%, Steyer ~23%. OC county certification deadline July 3. OC Registrar next count June 18. Hilton has vowed to cut income taxes, slash environmental regulations, and boost oil drilling.")
    print("  Updated ca-governor-2026")

# HB: June 16 vote result unclear
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Huntington Beach council met yesterday (June 16) for the housing element vote — result not yet confirmed in public reporting. $50K/month fines continue accruing; total owed now ~$385K+. Fines could escalate to $100K/month starting in July if still noncompliant. If noncompliance persists further, fines could reach $900K/month and the city faces receivership — meaning local officials would lose zoning control. Every single city in OC has a compliant housing element except Huntington Beach — now 4.5+ years behind schedule. First general election poll: Becerra (D) 52% vs Hilton (R) 31% — Becerra win would maintain aggressive state housing enforcement.")
    print("  Updated oc-newsom-housing-warning (HB)")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Construction 92% complete on the $649M project. Revenue service date remains spring 2027. Street testing continues. SBA Business Recovery Center open in Garden Grove. Next Garden Grove council meeting June 23. OC Registrar next count June 18.")
    print("  Updated oc-streetcar-launch")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-17T12:00:00Z"

# Primary: EARLY VOTING DAY 5
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** ⚡ EARLY VOTING DAY 5 — polls 10 AM - 8 PM (Tuesday). Through Day 4: 62,244 total voters citywide (+18,167 from Day 3); Brooklyn: 16,762 check-ins (+5,324 from Day 3). Manhattan leads at 26,607, Queens 11,755, Bronx 5,774, Staten Island 1,346. Early voting continues through June 21. Primary Election Day June 23 (6 DAYS). CD-7 (Velázquez seat): prediction markets now show Valdez (DSA) at 83% (up from 80%), Reynoso at 19%. Strong age divide persists: voters under 40 favor Valdez 33-15%, over 50 break for Reynoso 27-13%. Key endorsements for Valdez: Mayor Mamdani and Sen. Bernie Sanders. 43% of voters still undecided in Emerson poll.")
    print("  Updated nyc-june-primary-2026")

# Housing: early voting context
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** ⚡ EARLY VOTING DAY 5 — polls 10 AM - 8 PM. 62,244 voted citywide through Day 4; Brooklyn: 16,762 check-ins. Primary June 23 (6 DAYS). Brooklyn council seats on the ballot will shape housing policy implementation. City of Yes ADU Program: 3,100+ homeowner applications received. Q1 2026 housing permits nearly doubled vs 2025 average — 28,773 units filed.")
    print("  Updated nyc-atlantic-ave-rezoning")

# COPA: early voting
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** COPA bill language still being finalized — no hearing date yet. 26 sponsors (veto-proof). ⚡ EARLY VOTING DAY 5 — 62,244 voted citywide through Day 4; Brooklyn: 16,762 check-ins. Brooklyn council seats on the ballot determine whether COPA has the votes. Primary June 23 (6 DAYS).")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-17T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** ~60 days remaining in the 90-day ShotSpotter removal window (deadline mid-August 2026). Council voted 5-2 (two abstaining) to end the program on May 19. Device removal/disabling underway per City Manager Huang's direction. Cambridge Police Patrol Officers Association continues public opposition. No council revisitation expected.")
    print("  Updated cam-shotspotter-banned")

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** CRA advancing 2400 Massachusetts Ave — $9.375M loan to North Cambridge Partners finalized after project failed to attract sufficient outside financing. CRA total investment ~$14.375M ($5M equity + $9.375M loan). CRA purchased 4,000 sq ft to be permanently affordable to middle-income buyers. Project plans 56 homes + retail — could be Cambridge's first social housing project. Task force listening sessions this summer; CDD consultant hiring underway. Barrett v. Cambridge inclusionary zoning lawsuit in discovery — AG Campbell intervened April; fact discovery deadline November 13.")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-17T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** ⚡ Community Housing funding review TODAY (June 17) at 2 PM on Zoom — Community Preservation Act funding allocations under discussion. Article 16 (26 Pleasant Street — 103 apartments including 15 affordable) remains POSTPONED to fall Special Town Meeting (typically November). CHC Overlay District approved 217-20. Updated ADU rules and restored inclusionary payments in effect. Annual Town Meeting concluded June 4.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Brookline remains compliant. 165 of 177 communities statewide have achieved compliance. No further actions until fall Special Town Meeting. Community Housing funding review TODAY at 2 PM on Zoom.")
    print("  Updated brk-mbta-communities-compliance")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-17T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Plan Commission reviewed SE and SW Area Plans on June 15. Both plans shape land use, housing density, and transportation in Madison's fastest-growing areas. Council adoption vote June 23 (6 DAYS). Public comment opportunities at each committee meeting. BRT Route B: $118.1M federal funding remains in FTA pipeline; design work continuing through 2026, construction start planned for 2027.")
    print("  Updated mad-new-housing-developments")

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Route A continues 15-minute service. Route B: $118.1M Small Starts grant remains in FTA pipeline — design work continuing through 2026, construction planned 2027, launch planned 2028. Route B will run from Madison's Northside through downtown to South Madison/Fitchburg. SE/SW Area Plans: council vote June 23 (6 DAYS).")
    print("  Updated mad-east-west-brt-construction")

idx, issue = find_issue(madison["issues"], "mad-southeast-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Plan Commission reviewed the Southeast Area Plan on June 15. Council adoption vote June 23 (6 DAYS). The plan focuses on mixed-use and higher density along Milwaukee Street, Cottage Grove Road, Atwood Avenue, Monona Drive, and Stoughton Road. Public comment opportunity at council meeting.")
    print("  Updated mad-southeast-area-plan")

idx, issue = find_issue(madison["issues"], "mad-southwest-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 17 update:** Plan Commission reviewed the Southwest Area Plan on June 15. Council adoption vote June 23 (6 DAYS). The plan includes mixed-use developments along Whitney Way, Raymond Road, Schroeder Road, and McKee Road. Public comment opportunity at council meeting.")
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
        "\n\n**June 17 update:** ⚡ D5: Foley (D) reclaims narrow lead — 47.0% (85,104) vs Dixon (R) 46.8% (84,777). Margin: 327 votes with ~9,600 ballots remaining. D4: Shaw (R) ~33% vs Traut (D) ~31% — both advance. Next OC Registrar count June 18. Certification July 10. First general election poll: Becerra (D) 52% vs Hilton (R) 31% — Democratic strength could boost Foley in November. Garden Grove council meeting June 23."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 17 update:** First general election poll: Becerra (D) 52% vs Hilton (R) 31% — commanding 21-point lead. Registered Democrats outnumber Republicans nearly 2-to-1 statewide. Final primary tallies (88% counted): Becerra ~28%, Hilton ~25%, Steyer ~23%. OC county certification deadline July 3. Next registrar count June 18. HB housing element: June 16 vote result not yet confirmed; fines ~$385K+ and climbing; could escalate to $100K/month in July."
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
        "\n\n**June 17 update:** Huntington Beach council met yesterday (June 16) for the housing element vote — result not yet confirmed. $50K/month fines continue; total owed ~$385K+. Could escalate to $100K/month in July, and up to $900K/month with receivership risk. HB is 4.5+ years behind schedule and the only noncompliant city in OC. First general election poll: Becerra (D) 52% vs Hilton (R) 31% — a Becerra win maintains aggressive state housing enforcement. D5: Foley (D) reclaims narrow lead over Dixon (R), 47.0% vs 46.8%."
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
        "\n\n**June 17 update:** SBA Business Recovery Center open at 12966 Euclid St, Garden Grove — low-interest disaster loans for businesses affected by GKN evacuation. FBI/EPA served search warrant on GKN facility June 10 — seized documents on chemical storage and employee complaints. 50,000+ residents evacuated; chemical extraction still delayed ~27 days post-incident. 44+ lawsuits filed. D5: Foley (D) reclaims narrow lead 47.0% vs Dixon (R) 46.8% — next count June 18. Garden Grove council meeting June 23."
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
        "\n\n**June 17 update:** Filing period opens July 19 (32 DAYS). 20 candidates have already appointed campaign treasurers across the 5 open seats (D1, D3, D5, D8, D9). Bond survey closes June 23 (6 DAYS). AISD board vote on $181M shortfall TOMORROW (June 18) — 558 positions, campus police cuts, 11 school closures. CDBG public comment opens TODAY (June 17). Semi-annual campaign finance filings due in July. Council on recess until July 23."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 17 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. Moody's tentative credit rating based on two false assumptions (all lawsuits dismissed; Paxton validated bonds). ATP achieved federal Record of Decision. Three major contracts expected in 2026. Council on recess until July 23."
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
        "\n\n**June 17 update:** South Austin Navigation Center at 2401 S. I-35 — RFP open for operator, up to $250K; contracts for up to 3 providers, 12-month term beginning September 2026. AT-Home Initiative ($6.7M, 5-year) — proposals due June 2, city in review. AISD board vote TOMORROW (June 18) — school closures compound homelessness risk. Bond final vote July 23 — shelter infrastructure NOT in $390M direction."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if not campaign:
    campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 17 update:** 157th cadet class mid-training (started Jan 26) — graduation September 18. APD remains 300+ officers short. AISD $181M shortfall includes campus police cuts — board vote TOMORROW (June 18). Council on recess until July 23."
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
        "\n\n**June 17 update:** Raising Travis County virtual town hall held yesterday (June 16). $17.65M expansion; nearly 300 kids have received scholarships, target 1,000 by October; wait times down from 2 years to months. CDBG public comment period opens TODAY (June 17) through July 20 — draft PY26 Action Plan available at traviscountytx.gov. Public hearing July 14 at 9 AM. AISD board vote TOMORROW (June 18) — school closures directly impact childcare access. Travis County offices CLOSED June 18-19 for Juneteenth."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-17T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-17T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-17T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-17T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-17T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
