#!/usr/bin/env python3
"""
June 11, 2026 updates for all issue and organization data files.
Key developments since June 10:
  - Garden Grove: ⚡ FBI/EPA served federal search warrant at GKN Aerospace on June 10 — seized records,
    chemical samples, equipment data; criminal probe now FEDERAL (in addition to DA Spitzer + Cal/OSHA)
  - Austin: George Morales formally appointed and sworn in TODAY (June 11) as Pct 4 Commissioner
  - Austin: AISD board vote June 18 (7 DAYS); boundary realignment workshops June 16 (5 DAYS)
  - OC: Registrar posting updated vote counts today at 5 PM; Shaw leads Traut by ~1,600 (D4);
    Dixon leads Foley by ~4,000 (D5)
  - OC: Huntington Beach housing vote confirmed for June 16 (5 DAYS); $50K/month fines accruing
  - NYC: East 98th Street scoping session TODAY at 2 PM; ADU deadline TOMORROW (June 12);
    early voting starts June 13 (2 DAYS); CD-7 poll: Valdez 23%, Reynoso 21%, 43% undecided
  - Madison: SE/SW Area Plans — Plan Commission review June 15 (4 DAYS), council vote June 23 (12 DAYS)
  - Cambridge: 2400 Mass Ave social housing project advancing; ShotSpotter removal ~66 days remaining
  - Brookline: Town Meeting concluded; Chestnut Hill West rezoning approved; 26 Pleasant St postponed to fall
  - Governor: Becerra (D) 26.7% vs Hilton (R) 26.4% — both advance to November, counting continues
  - Travis County CDBG: public comment period opens June 17; public hearing July 14
"""
import json
import os
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
austin["last_scraped"] = "2026-06-11T12:00:00Z"

# Pct 4: Morales sworn in TODAY
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** ⚡ George Morales was formally appointed and sworn in TODAY as Travis County Precinct 4 Commissioner — ending Margaret Gómez's 31-year tenure. He is the first new Pct 4 commissioner since 1995. Morales, a former Travis County constable who distributed 380,000 vaccines during COVID, immediately begins voting on county business. Key items before Commissioners Court: additional Raising Travis County childcare contracts, infrastructure investments, and FY2027 budget planning. CDBG public comment period opens June 17 (6 DAYS) through July 20, with a public hearing July 14. Raising Travis County virtual town hall June 16 at 6 PM (5 DAYS). Travis County offices closed June 18-19 for Juneteenth/Emancipation Day.")
    print("  Updated tc-pct4-runoff")

# AISD: 7 days to board vote
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Board final vote on the $181M deficit budget is June 18 — 7 DAYS AWAY. The full budget-cut plan details: 558 positions affected including 215 educator salaries cut (85 elementary, 51 middle, 79 high school), librarians at sub-400-student campuses reduced to part-time, middle/high school students moved to hub transportation model. $60M from selling/monetizing four AISD properties, $31M from campus-level changes (larger class sizes, reduced planning periods), $21M from 11 school closures. AISD has lost 3,000 students amid closures. Boundary realignment workshops: June 16 (South Austin, 5 DAYS) and June 22-23 (districtwide virtual). George Morales sworn in as Pct 4 commissioner TODAY.")
    print("  Updated atx-aisd-budget-crisis")

# Homelessness: AT-Home in review, Navigation Center update
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** AT-Home Initiative ($6.7M, 5-year) — city in review/selection phase after proposals closed June 2. Up to three providers selected; contracts start September 2026. Permanent supportive housing has 98% retention rate. South Austin Housing Navigation Center on track for late summer/early fall 2026 opening; 13-member Advisory Board formed. Morales sworn in as Pct 4 commissioner TODAY — his law enforcement background and county budget vote influence homelessness infrastructure. AISD board vote June 18 (7 DAYS) — school closures compound homelessness risk. Bond final vote July 23 (42 DAYS) — shelter infrastructure NOT in ~$390M direction.")
    print("  Updated atx-hso-plan-adopted")

# Bond: countdown
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Council on summer recess until July 23 — bond conversation resumes then. The ~$390M bond direction: Parks $250M, Transportation $92M, Community Facilities $48M — does NOT include housing. Austin Parks Foundation notes this is a 'summer standstill.' Mayor Watson opposes the bond, arguing the tax rate election defeat last fall makes it premature. Final vote July 23 (42 DAYS). Mid-August council vote to formally call November election. Morales sworn in as Pct 4 commissioner TODAY. AISD board vote June 18 (7 DAYS).")
    print("  Updated atx-2026-bond")

# D1 Election: filing countdown
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Filing period opens July 20 (39 DAYS). At least 8 candidates declared for D1 — the most competitive open-seat race since geographic representation began in 2014. First day to file in person is July 20; last day is August 17 at 5 PM. Semi-annual campaign finance filings for the first half of 2026 due in July — will reveal fundraising trajectory for all candidates. Council on summer recess until July 23. Election Day November 3. Key events this week: Morales sworn in TODAY. AISD board vote June 18 (7 DAYS). Raising Travis County virtual town hall June 16 (5 DAYS).")
    print("  Updated atx-d1-election")

# Project Connect: status unchanged
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Legal status unchanged — trial remains halted per TX Supreme Court May 22 ruling. Judge Shepperd must rule on AG Paxton's jurisdictional plea. Texas Tribune reported (May 21) project has shrunk to ~10 miles at $8.2B with 15 stations — per-mile cost 3x the 2020 estimate, land acquisition costs nearly quadrupled. ATP says 'on schedule' for 2027 construction start, expects to award three major contracts in 2026. Morales sworn in TODAY — his CapMetro coordination priorities could influence county-level transit investment. Council on recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# Childcare: Morales sworn in, town hall 5 days
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** ⚡ George Morales sworn in as Pct 4 commissioner TODAY — immediately begins voting on additional Raising Travis County childcare contracts before Commissioners Court. The program is at record pace: 1,000+ childcare scholarships funded (reaching October target months early), wait times dropped from 2 years to months, $2.6M in gap funding to 150 providers, 2,650+ students in out-of-school time programs. Virtual town hall June 16 at 6 PM — 5 DAYS AWAY. CDBG public comment period opens June 17 (6 DAYS) through July 20, public hearing July 14. Travis County offices closed June 18-19 for Juneteenth.")
    print("  Updated tc-childcare-funding")

# APD Staffing
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** 157th cadet class mid-training — graduation scheduled September 18, 2026. APD has ~1,400+ sworn officers with 365 vacancies. April 2025 audit: current pace of ~87 new officers/year inadequate to close gap by 2027. Recent cadet classes show 51-52% attrition rates — a significant training efficiency concern. Interim Chief Henderson indicated next class roughly twice as large. Morales sworn in TODAY — his law enforcement background (former constable) strengthens county-level public safety coordination. Council on recess until July 23.")
    print("  Updated atx-apd-staffing-audit")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-11T12:00:00Z"

# Garden Grove: FBI RAID
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 11 update:** ⚡ BREAKING: FBI and EPA served a federal search warrant at the GKN Aerospace facility on June 10 — agents seized documents, chemical samples, equipment records, risk analyses, employee complaints, and maintenance logs related to hazardous substances. The federal criminal probe targets potential violations of laws requiring companies to prevent accidental release of extremely hazardous substances. This is now a THREE-AGENCY criminal investigation: FBI/EPA (federal), OC DA Spitzer (state criminal), and Cal/OSHA (workplace safety). The warrant specifically sought samples of substances inside any container with methyl methacrylate and records on risk analyses of GKN's equipment. MMA chemical extraction STILL delayed — specialized sealed trucks have not arrived. The $500/address direct aid announced at the June 9 council meeting remains the only compensation. 44+ lawsuits filed in OC Superior Court and US District Court. Community continues demanding permanent facility closure.")
    print("  Updated Garden Grove chemical crisis")

# D4: vote count update expected today
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** OC Registrar posting updated vote count today at 5 PM. As of yesterday: Shaw (R) 26,264 (33.27%) vs Traut (D) 24,643 (31.22%) — margin ~1,600 votes. Mail ballot receipt deadline passed June 9 — all remaining counting is from the finite pool of already-received ballots. Additional count updates scheduled: June 12, 16, 18, 24, 26. Final certification July 10. The November general election — Shaw (R) vs. Traut (D) — is the decisive contest for the 3-2 Democratic BOS majority. ⚡ FBI raided GKN Aerospace yesterday (June 10) — federal criminal probe adds urgency to D4 industrial safety and accountability issues. Huntington Beach housing vote June 16 (5 DAYS).")
    print("  Updated oc-bos-district-4-open-seat")

# D5: Dixon lead
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** OC Registrar posting updated count today at 5 PM. Dixon (R) leads with 62,640 votes (48.5%) vs Foley (D) 58,654 (45.4%) — gap widened to ~4,000 votes. All remaining counting from already-received ballots (mail deadline passed June 9). Certification deadline July 10. If Dixon wins November, the board flips to Republican majority — affecting the $10.5B budget, housing enforcement, and homelessness investment. Voice of OC: 'Is an Incumbent on the OC Board of Supervisors Going to Lose Reelection?' FBI raided GKN Aerospace yesterday — federal probe adds weight to county oversight issues.")
    print("  Updated oc-bos-district-5-defense")

# Governor: counting continues
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Becerra (D) 26.7% vs Hilton (R) 26.4% — counting continues. AP, ABC7, NBC, CalMatters all project both advance to November. ABC7 confirmed: 'Democrat Xavier Becerra, Republican Steve Hilton advance to California governor face-off.' Steyer at ~21%, has not conceded. All precincts partially reporting; mail ballots continue to be processed. County certification deadline July 3. The governor determines California's housing enforcement posture — RHNA, Builder's Remedy, AG referrals.")
    print("  Updated ca-governor-2026")

# HB: 5 DAYS to vote
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Huntington Beach housing element vote is June 16 — 5 DAYS AWAY. The council postponed from a prior meeting by a 6-0 vote (Van Der Mark absent). $50K/month fines NOW ACCRUING — the city already owes $160,000+ in retroactive fines ($10K/month since January 2025, escalating to $50K/month in June). Fines go to California's Building Homes and Jobs Trust Fund. All legal avenues exhausted: US Supreme Court declined, state court ruled against, AG enforcement active. Court ordered Builder's Remedy project approvals within 60-90 days. The plan would zone for ~13,000 new units. HB residents previously voted to require public votes on major zoning changes — creating a political collision.")
    print("  Updated oc-newsom-housing-warning (HB)")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Revenue service date remains March 2027. The $649M project (funded with federal, state, local dollars including Measure M) continues street testing on Santa Ana Boulevard since February 2026. All Siemens S700 vehicles delivered. FBI raid at GKN Aerospace facility yesterday (June 10) adds complexity to the Garden Grove corridor environment.")
    print("  Updated oc-streetcar-launch")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-11T12:00:00Z"

# Primary: early voting 2 DAYS
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** ⚡ EARLY VOTING STARTS JUNE 13 — 2 DAYS AWAY. June 13 is ALSO the last day to register to vote AND the last day to request an absentee/mail ballot by mail. Early voting runs June 13-21 (varying hours by day). Primary Election Day June 23 (12 DAYS). CD-7 (Velázquez seat): Emerson/PIX11 poll shows Valdez (DSA) 23%, Reynoso 21%, Won 13%, 43% UNDECIDED — race wide open with early voting imminent. Key dynamic: voters under 40 favor Valdez 33%-15%, voters over 50 favor Reynoso 27%-13%. Reynoso has Velázquez, AG James, WFP, 32BJ SEIU, broad labor wall; Valdez has Mayor Mamdani, UAW, Sanders, NYC DSA. CBS described race as testing 'power of Mamdani's endorsement.' ADU deadline TOMORROW (June 12). East 98th Street scoping session TODAY at 2 PM.")
    print("  Updated nyc-june-primary-2026")

# Housing: ADU deadline TOMORROW, East 98th TODAY
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** ⚡ East 98th Street rezoning scoping session is TODAY at 2 PM. The project by Midyan Gate Realty (Bawabeh Holdings) would rezone six sites in East Flatbush from C8-2 to C4-4/C4-4D — enabling residential uses currently prohibited. Updated scope: 786 dwelling units across the project area (revised from earlier 972-unit figure), with 20-30% (157-236 units) permanently affordable under Mandatory Inclusionary Housing. City of Yes ADU application deadline is TOMORROW (June 12) — 3,100+ homeowners have applied since March reopening. Up to $395,000 per homeowner ($175K grant + $220K loan). Pre-Approved Plan Library with 11 DOB-reviewed designs available. Q1 2026 housing permits nearly doubled: 28,773 units filed vs 14,338/quarter average in 2025. Early voting starts June 13 (2 DAYS).")
    print("  Updated nyc-atlantic-ave-rezoning")

# COPA: bill language being finalized
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** COPA reintroduction advancing — Council Member Sandy Nurse rallied with tenants May 14 to announce the new version. Bill language still being finalized; Nurse stated 'We are in the process of finalizing the language... hoping to have something introduced very quickly.' The 2026 version targets distressed buildings — those in the Alternative Enforcement Program, on the Certificate of No Harassment list, or about to lose subsidies (421a, LIHTC). The bill gives qualified nonprofits or joint ventures a first opportunity to purchase before open market listing. Backed by 200+ organizations. Early voting starts June 13 (2 DAYS) — Brooklyn council seats on the ballot will shape the housing agenda.")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-11T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** ~66 days remaining in the 90-day ShotSpotter removal window (deadline mid-August 2026). The Cambridge Police Patrol Officers Association publicly expressed 'deep disappointment' with the council's 5-2-2 vote. Acting Commissioner Wells cited 11 gun violence incidents over 10 years flagged only by ShotSpotter. Councillors Nolan and McGovern responded that 'after more than 10 years of ShotSpotter's deployment, we have seen no proof of its effectiveness.' Device removal/disabling underway per City Manager Huang's direction. Discussions continue about whether the policy order language correctly invoked council's authority under the Surveillance Technology Ordinance.")
    print("  Updated cam-shotspotter-banned")

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** All 13 task force members appointed — notable members include Christopher Herbert (managing director, Harvard Joint Center for Housing Studies) and Sara Barcan (executive director, Homeowners Rehab Inc.). CRA advancing plans for 2400 Massachusetts Ave. in North Cambridge — 56 homes + retail — as a potential first social housing project. Listening sessions planned for this summer, plus a request for information from developers. The project aims for mixed-use with ground-floor retail, mixed-income homes, and an affordable homeownership component. FY27 operating budget of $1.033B (4.1% increase) adopted. Barrett v. Cambridge inclusionary zoning lawsuit in discovery phase.")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-11T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Town Meeting concluded — sessions ran May 26-28 and reserved June 2-4 if needed. Key outcomes: Chestnut Hill West rezoning APPROVED on May 28 (rezoning commercial area along Boylston Street/Route 9 near Newton border for multi-use development with housing). Tax override overwhelmingly approved. Article 14 updated Accessory Dwelling Unit rules. Article 15 amended zoning to restore cash-in-lieu payments for inclusionary units in sub-20-unit developments. Article 16 (26 Pleasant Street, 103 apartments including 15 affordable) POSTPONED to fall Special Town Meeting. The warrant contained 25 articles: Town budget, 10 bylaw/zoning amendments, and 6 resolutions.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Brookline remains compliant — AG approved new zoning by-laws March 23, 2026. Not among the 9 towns sued in January 2026. 165 of 177 communities have achieved compliance or conditional status. Results modest so far: only one known project in the rezoning corridor (childcare center + 3 housing units). Town Meeting approved Chestnut Hill West rezoning (May 28) and updated ADU rules (Article 14) — both add density capacity. The 26 Pleasant Street rezoning (103 units) postponed to fall, which would have been the most significant MBTA-corridor housing project to date.")
    print("  Updated brk-mbta-communities-compliance")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-11T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Southeast and Southwest Area Plans adoption vote is June 23 — 12 DAYS AWAY. Plan Commission review is June 15 (4 DAYS) — a critical step before the full council vote. Both plans were formally submitted May 5 and are cycling through Boards, Commissions, and Committees — each meeting open for public comment. The plans shape land use, housing density, and transportation in Madison's fastest-growing areas. Key corridors: Milwaukee Street, Cottage Grove Road, Atwood Avenue, Monona Drive (SE); Whitney Way, Raymond Road, Schroeder Road, McKee Road (SW). BRT Route B federal funding ($118M) remains at HIGH risk.")
    print("  Updated mad-new-housing-developments")

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Route A continues 15-minute service. Route B: FTA direction is that 'nothing has changed and funding is still in the pipeline,' but the city characterizes the risk as 'moderate to high' — no signed FTA agreement for the $118.1M Small Starts grant. Metro Transit developing alternate approaches to bring BRT to the north-south corridor if federal funding falls through — 'it may look different and come together in different ways.' Route B stretches 12.5 miles from Kennedy Road (north) to McKee Road in Fitchburg, sharing 3.5 miles with Route A through the Isthmus. Design work continuing through 2026; construction expected 2027, service 2028 if funded. SE/SW Area Plans vote June 23 (12 DAYS) — Plan Commission review June 15 (4 DAYS).")
    print("  Updated mad-east-west-brt-construction")

idx, issue = find_issue(madison["issues"], "mad-southeast-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Plan Commission review is June 15 — 4 DAYS AWAY. This is a critical committee step before the June 23 Common Council adoption vote (12 DAYS). The plan focuses on mixed-use and higher density along Milwaukee Street, Cottage Grove Road, Atwood Avenue, Monona Drive, and Stoughton Road. Each committee meeting is open for public comment.")
    print("  Updated mad-southeast-area-plan")

idx, issue = find_issue(madison["issues"], "mad-southwest-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 11 update:** Plan Commission review June 15 (4 DAYS), same pipeline as SE plan. Final adoption vote June 23 (12 DAYS). The plan includes mixed-use developments along Whitney Way, Raymond Road, Schroeder Road, and McKee Road — one of Madison's fastest-growing areas. Committee meetings open for public comment.")
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
        "\n\n**June 11 update:** OC Registrar posting updated vote counts today at 5 PM. D4: Shaw (R) leads 26,264 (33.27%) vs Traut (D) 24,643 (31.22%) — margin ~1,600. D5: Dixon (R) leads 62,640 (48.5%) vs Foley (D) 58,654 (45.4%) — gap ~4,000 votes. Mail ballot receipt deadline passed — all remaining counting from already-received ballots. ⚡ FBI/EPA served federal search warrant at GKN Aerospace yesterday (June 10) — the federal criminal probe adds a new dimension to D4 accountability issues. Next count updates: June 12, 16, 18, 24, 26. Certification July 10. November strategy for BOTH D4 and D5 is now the urgent priority. HB housing vote June 16 (5 DAYS)."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 11 update:** Governor: Becerra (D) 26.7% vs Hilton (R) 26.4% — AP, ABC7 confirm both advance to November. Counting continues; county certification deadline July 3. SD-34: Valencia (D) 63% vs Shader (R) 37% — Valencia heavy favorite in November. The governor determines California's housing enforcement posture for RHNA, Builder's Remedy, AG referrals."
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
        "\n\n**June 11 update:** Huntington Beach housing vote June 16 — 5 DAYS. Council previously postponed 6-0 (Van Der Mark absent). $50K/month fines NOW ACCRUING — $160K+ retroactive already owed. Court ordered Builder's Remedy project approvals within 60-90 days. ⚡ FBI/EPA raided GKN Aerospace yesterday — federal criminal probe escalates Garden Grove accountability, demonstrating consequences of inadequate corporate/government oversight. D4: Shaw (R) leads by ~1,600; D5: Dixon (R) leads by ~4,000 — both trending Republican. OC Streetcar remains at March 2027 launch."
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
        "\n\n**June 11 update:** ⚡ FBI/EPA served federal search warrant at GKN Aerospace yesterday (June 10) — agents seized records, chemical samples, and equipment data. Federal criminal probe now targets potential violations of hazardous substance release prevention laws. The crisis displaced thousands of families with young children in D4 territory. Direct aid remains just $500/address. Chemical extraction STILL delayed. 44+ lawsuits filed. D4: Shaw (R) leads by ~1,600; D5: Dixon (R) leads by ~4,000. The next supervisors shape FY27 childcare and family services budgets. HB housing vote June 16 (5 DAYS)."
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
        "\n\n**June 11 update:** Filing period opens July 20 (39 DAYS). At least 8 candidates for D1; semi-annual campaign finance filings due in July will reveal fundraising trajectories. George Morales sworn in as Pct 4 commissioner TODAY. AISD board vote on $181M deficit budget June 18 (7 DAYS) — 558 positions affected. Boundary realignment workshops June 16 (South Austin) and June 22-23 (virtual). Bond final vote July 23 (42 DAYS). Council on summer recess until July 23."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 11 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. Project has shrunk to ~10 miles/$8.2B with 15 stations (Texas Tribune, May 21). ATP expects to award three major contracts in 2026: full 9.8-mile buildout, O&M facility, train cars. Morales sworn in as Pct 4 commissioner TODAY — his CapMetro coordination priorities could influence county transit investment. Council on recess until July 23."
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
        "\n\n**June 11 update:** AT-Home Initiative — city in review/selection phase. Permanent supportive housing has 98% retention rate. Navigation Center on track for late summer/early fall opening; Advisory Board formed. Morales sworn in as Pct 4 commissioner TODAY — county budget votes influence homelessness infrastructure. AISD board vote June 18 (7 DAYS) — 558 positions, 11 school closures compound homelessness risk. Bond final vote July 23 (42 DAYS) — shelter infrastructure NOT in ~$390M direction."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 11 update:** 157th cadet class mid-training — graduation September 18. APD has ~1,400+ sworn with 365 vacancies. Recent classes show 51-52% attrition rates — efficiency concern beyond raw recruiting numbers. Interim Chief Henderson indicated next class roughly twice as large. Morales sworn in TODAY — his law enforcement background (former constable) strengthens county-level public safety coordination. Council on recess until July 23."
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
        "\n\n**June 11 update:** ⚡ George Morales sworn in as Pct 4 commissioner TODAY — immediately begins voting on Raising Travis County childcare contracts. Program at record pace: 1,000+ scholarships funded, wait times dropped from 2 years to months, $2.6M gap funding to 150 providers. Virtual town hall June 16 at 6 PM (5 DAYS). CDBG public comment period opens June 17 (6 DAYS) through July 20, public hearing July 14. AISD board vote June 18 (7 DAYS) — school closures impact family childcare and after-school access. Travis County offices closed June 18-19 for Juneteenth."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-11T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-11T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-11T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-11T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-11T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
