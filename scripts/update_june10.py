#!/usr/bin/env python3
"""
June 10, 2026 updates for all issue and organization data files.
Key developments since June 9:
  - OC: Mail ballot receipt deadline PASSED yesterday (June 9) — remaining count is finite
  - OC: Garden Grove special council meeting held June 9 — GKN VP Steve Carlin attended for FIRST TIME,
         chaos erupted, hours of testimony, direct aid increased $250→$500/address
  - OC: MMA chemical extraction STILL delayed — ~50 gal stormwater overflow entered storm drain, being tested
  - OC D4: Shaw 33.27% vs Traut 31.22% — margin ~1,600, both advance to November
  - OC D5: Dixon 48.5% vs Foley 45.4% — Dixon leads by ~4,000 votes, both advance to November
  - Governor: Becerra (D) 26.7% vs Hilton (R) 26.4% — ~65% counted, both advance
  - HB housing vote June 16 (6 DAYS); $50K/month fines now accruing; $160K retroactive owed
  - Austin: Morales appointment TOMORROW June 11 (1 DAY); AISD board vote June 18 (8 DAYS)
  - Austin: AISD full cut plan released June 3, teacher/parent protest June 5, boundary workshops scheduled
  - NYC: Early voting June 13 (3 DAYS); ADU deadline June 12 (2 DAYS); scoping June 11 (TOMORROW)
  - NYC: ADU program has 3,100+ applications (up from 98 previously); CD-7 poll: Valdez 23%, Reynoso 21%
  - NYC: Q1 2026 housing permits nearly doubled from 2025 quarterly average
  - Madison: SE/SW Area Plans vote June 23 (13 DAYS)
  - Cambridge: June 8 council met — Affordable Housing Overlay 5-year review; potential first social housing
    project at 2400 Mass Ave (56 homes + retail)
  - Brookline: Chestnut Hill West rezoning approved May 28; tax override overwhelmingly approved
  - OC Streetcar: launch pushed to March 2027 (from spring 2026)
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
austin["last_scraped"] = "2026-06-10T12:00:00Z"

# AISD: protest, cut plan details, boundary workshops
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Board final vote on the $181M deficit budget is June 18 — 8 DAYS AWAY. The full budget-cut plan released June 3 details: 215 full-time educator salary cuts (85 elementary, 51 middle, 79 high school), $60M from selling/monetizing four AISD properties, $31M from campus-level changes (larger class sizes, reduced planning periods, cutting librarians), $21M from 11 school closures. Teachers and parents held a protest rally on June 5. AISD has lost 3,000 students amid closures. Superintendent Segura suspended further school closures until the district stabilizes — boundary realignment workshops scheduled: June 16 (South Austin) and June 22-23 (districtwide virtual). George Morales appointed Pct 4 commissioner TOMORROW (June 11).")
    print("  Updated atx-aisd-budget-crisis")

# Pct 4: Morales TOMORROW
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** ⚡ George Morales will be formally appointed and sworn in as Pct 4 Commissioner TOMORROW (June 11) — ending Margaret Gómez's 31-year tenure. He is the first new Pct 4 commissioner in over 30 years. KUT covered Gómez's farewell on June 3. Morales, a former Travis County constable, immediately begins voting on county business: Raising Travis County childcare contracts ($17.65M awarded, additional contracts before Commissioners Court), infrastructure investments, and FY2027 budget planning. CDBG public comment period opens June 17 through July 20 with a public hearing July 14. Travis County offices closed June 18-19 for Juneteenth/Emancipation Day. Raising Travis County virtual town hall June 16 at 6 PM (6 DAYS).")
    print("  Updated tc-pct4-runoff")

# Homelessness: AT-Home proposals closed, in review
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** AT-Home Initiative ($6.7M, 5-year) proposals closed June 2 — the city is now in the review and selection phase. Up to three providers will be selected; contracts start September 2026. South Austin Housing Navigation Center — the city's FIRST city-owned facility — on track for late summer/early fall 2026 opening. The 13-member Center Advisory Board has been formed. AISD board vote June 18 (8 DAYS) — school closures compound homelessness risk; 3,000 students already lost. Bond final vote July 23 (43 DAYS) — shelter infrastructure still NOT in ~$390M direction. Morales sworn in TOMORROW (June 11).")
    print("  Updated atx-hso-plan-adopted")

# Bond: countdown
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Council on summer recess until July 23 — bond conversation resumes then. The ~$390M bond direction: Parks $250M, Transportation $92M, Community Facilities $48M — does NOT include housing. Mayor Watson opposes the bond, arguing the tax rate election defeat last fall makes it premature. Final vote July 23 (43 DAYS). Mid-August council vote to formally call November election. AISD board vote on $181M deficit budget June 18 (8 DAYS). Morales appointed Pct 4 commissioner TOMORROW (June 11).")
    print("  Updated atx-2026-bond")

# D1 Election: filing countdown
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Filing period opens July 20 (40 DAYS). At least 8 candidates declared for D1 — the most competitive open-seat race since geographic representation began in 2014. Known candidates include Alexandria Anderson (retired athlete), Steven Brown (Medtronic clinical specialist, raised ~$6K). Council on summer recess until July 23. Election Day November 3. Key countdown: Morales appointed Pct 4 commissioner TOMORROW (June 11). AISD board vote June 18 (8 DAYS). Bond final vote July 23 (43 DAYS).")
    print("  Updated atx-d1-election")

# Project Connect: status unchanged
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Legal status unchanged — trial remains halted per TX Supreme Court May 22 ruling. Judge Shepperd must now rule on AG Paxton's jurisdictional plea — if denied, AG gets automatic interlocutory appeal that pauses everything; if granted, ATP's bond validation suit is dismissed entirely. ATP says it is 'on schedule' to begin construction in 2027 and expects to award three major contracts in 2026: full 9.8-mile buildout, operations/maintenance facility, and train cars. FTA signed off on key environmental review January 16. Council on recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# Childcare: countdown updates
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Raising Travis County continues at record pace — 1,000 childcare scholarships funded, reaching the October target months early. Wait times for affordable childcare dropped from 2 years to months. Over 2,650 students in out-of-school time programs. $2.6M in gap funding to 150 providers. Virtual town hall June 16 at 6 PM — 6 DAYS AWAY. George Morales sworn in as Pct 4 commissioner TOMORROW (June 11) — immediately begins voting on additional childcare contracts before Commissioners Court. CDBG public comment period opens June 17.")
    print("  Updated tc-childcare-funding")

# APD Staffing: 156th class detail + 157th update
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** 157th cadet class mid-training — graduation scheduled September 18, 2026. The 156th class graduated May 1 with 25 cadets of 49 who started (51% completion rate). APD has ~1,400+ sworn officers with 365 vacancies — an April 2025 audit found the current pace of ~87 new officers/year is inadequate to close the gap by 2027. Interim Chief Robin Henderson indicated the next class would be roughly twice as large. Council on recess until July 23. Morales sworn in TOMORROW (June 11).")
    print("  Updated atx-apd-staffing-audit")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-10T12:00:00Z"

# D4: post-ballot-deadline, November focus
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Mail ballot receipt deadline PASSED yesterday — remaining count is from the finite pool of already-received ballots. Shaw leads with 26,264 votes (33.27%) vs Traut at 24,643 (31.22%) — margin ~1,600. Neither candidate near 50%, so a November general election runoff is all but certain: Shaw (R) vs. Traut (D). OC Registrar posting daily updates at 5 PM — next batch today at 5 PM. Additional updates scheduled June 11, 12, 16, 18, 24, 26. Final certification July 10. The November general election is now the decisive contest for the 3-2 Democratic BOS majority. Huntington Beach housing vote June 16 (6 DAYS).")
    print("  Updated oc-bos-district-4-open-seat")

# D5: Dixon lead stable
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Mail ballot deadline PASSED yesterday. Dixon leads with 62,640 votes (48.5%) vs Foley at 58,654 (45.4%) — Dixon's lead has widened to ~4,000 votes. Both advance to November regardless. Voice of OC headline asks: 'Is an Incumbent on the OC Board of Supervisors Going to Lose Reelection?' Dixon overtook Foley on election night and has held the lead since. OC Registrar daily updates at 5 PM. Certification deadline July 10. If Dixon wins November, the board flips to Republican majority — affecting the $10.5B budget, housing enforcement, and homelessness investment.")
    print("  Updated oc-bos-district-5-defense")

# Governor: both advance, counting continues
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Becerra (D) leads Hilton (R) 26.7% to 26.4% with ~65% of expected votes counted. Both officially advance to November — AP, ABC7, NBC, CalMatters all project both in the general. Steyer at ~21%, has not conceded. Mail ballot receipt deadline passed yesterday. County officials have until July 3 to certify results to Secretary of State. The governor determines California's housing enforcement posture — RHNA, Builder's Remedy, AG referrals. First successful Builder's Remedy court case won in La Cañada Flintridge (80-unit project) — sets precedent for noncompliant OC cities.")
    print("  Updated ca-governor-2026")

# HB: 6 DAYS to vote, fines accruing
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Huntington Beach housing element vote is June 16 — 6 DAYS AWAY. $50K/month fines are NOW ACCRUING as of June — the city already owes $160,000 in retroactive fines ($10K/month since January 2025). Fines go to California's Building Homes and Jobs Trust Fund. All legal avenues exhausted (US Supreme Court declined, state court ruled against, AG enforcement active). Court has ordered the city to approve Builder's Remedy projects within 60-90 days. The plan would zone for ~13,000 new units. Complicating factor: HB residents previously voted to require public votes on major zoning changes.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove: BREAKING — June 9 meeting aftermath
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 10 update:** ⚡ BREAKING: Garden Grove special council meeting held yesterday (June 9) — chaos erupted during hours of heated testimony from displaced residents. GKN Aerospace Senior VP Steve Carlin attended for the FIRST TIME since the May 21 emergency. Carlin stated 500+ people work at the plant, most living locally. Key outcomes: direct aid increased from $250 to $500 per address — residents called it a 'drop in the bucket.' Mayor Klopfenstein: 'GKN must be held accountable and I will not stop until everyone that has been impacted by this incident is made whole.' MMA chemical extraction STILL delayed — no revised start date. NEW CONCERN: ~50 gallons of stormwater overflowed from a disposal tote and entered a storm drain — officials say contamination risk is low but water is being tested. 44+ lawsuits filed. Cal/OSHA investigation and DA Spitzer's criminal probe continue.")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar: launch pushed to 2027
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** OC Streetcar revenue service date pushed to March 2027 — from the originally hoped spring 2026 launch. The 4.15-mile electric route through Santa Ana and Garden Grove (10 stops each direction) continues street testing on Santa Ana Boulevard since February 2026. The Garden Grove chemical crisis may complicate the operational environment along the route.")
    print("  Updated oc-streetcar-launch")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-10T12:00:00Z"

# Primary: early voting 3 DAYS, registration deadline
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** ⚡ EARLY VOTING STARTS JUNE 13 — 3 DAYS AWAY. June 13 is ALSO the last day to register to vote AND the last day to request an absentee/mail ballot by mail. Early voting runs June 13-21 (Sat/Sun 9-5, Mon 9-5, Tue/Wed 10-8, Thu 9-5, Fri/Juneteenth 8-4). Primary Election Day June 23 (13 DAYS). CD-7 (Velázquez seat) latest polling: Valdez (DSA) 23%, Reynoso 21%, Won 13%, 43% UNDECIDED — this race is wide open with early voting days away. Key endorsements: Reynoso has Velázquez, AG James, WFP, 32BJ SEIU; Valdez has Mayor Mamdani, UAW, Sanders, NYC DSA. East 98th Street scoping TOMORROW (June 11) at 2 PM. ADU deadline June 12 (2 DAYS).")
    print("  Updated nyc-june-primary-2026")

# Housing: ADU 3,100+ applications, Q1 permits doubled, East 98th details
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** City of Yes ADU application deadline June 12 — 2 DAYS AWAY. ⚡ 3,100+ homeowners have applied since March reopening (up dramatically from 98 when previously tracked). Up to $395,000 per homeowner ($175K grant + $220K loan). Pre-Approved Plan Library with 11 DOB-reviewed designs launched — though only ~12% of residential lots actually meet zoning/size requirements. East 98th Street rezoning scoping session TOMORROW (June 11) at 2 PM in East Flatbush — 972 apartments across 9 buildings (14-15 stories), 194-292 affordable units under MIH. Q1 2026 housing permits nearly DOUBLED: 28,773 units filed vs 14,338/quarter average in 2025 — Manhattan up 289%. City of Yes is accelerating production citywide.")
    print("  Updated nyc-atlantic-ave-rezoning")

# COPA: narrower version details
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** COPA (Intro. 905) has 26 sponsors — veto-proof majority. The 2026 version is narrower and 'stronger': targets distressed buildings with an average of 3+ open hazardous violations per year. Timeline shortened to 100 days total (45 days to express interest + 90 days to make offer, down from the vetoed version's 180 days). Backed by 200+ organizations including CLTs, tenant associations, affordable housing developers, labor unions. Mayor Mamdani supports — unlike Adams who vetoed it. Bill language still being finalized; no hearing date yet. Early voting starts June 13 (3 DAYS) — Brooklyn council seats on the ballot will shape the housing agenda.")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-10T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** ~67 days remaining in the 90-day ShotSpotter removal window (deadline mid-August 2026). Cambridge Day reported June 1 that police officers are unhappy with the mandate — Acting Commissioner Pauline Wells cited 11 gun violence incidents over 10 years that were flagged only by ShotSpotter. The June 8 council meeting did not revisit the ShotSpotter order. Device removal/disabling process underway per City Manager Huang's direction.")
    print("  Updated cam-shotspotter-banned")

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** All 13 task force members appointed in May — notable members include Christopher Herbert (managing director, Harvard Joint Center for Housing Studies) and Sara Barcan (executive director, Homeowners Rehab Inc.). CDD consultant hiring underway. ⚡ Cambridge's first social housing project may already be identified: the Cambridge Redevelopment Authority is advancing plans for 2400 Massachusetts Ave. in North Cambridge — 56 homes + retail — even before the task force completes its work. June 8 council meeting featured a five-year progress review of the Affordable Housing Overlay. FY27 operating budget of $1.033B (4.1% increase) adopted. Barrett v. Cambridge inclusionary zoning lawsuit in discovery phase — AG Campbell intervened in April, warning a ruling for the developer could affect 141+ municipalities.")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-10T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Brookline is NOT among the 9 towns the AG sued in January 2026 for MBTA Communities noncompliance — 165 of 177 communities have achieved compliance or conditional status. However, results so far are modest: only one known project in the MBTA Communities rezoning corridor (a childcare center plus 3 housing units). The AG approved Brookline's new zoning by-laws on March 23, 2026. A Housing Advisory Board subcommittee drafted a warrant article for Spring 2026 Town Meeting to address additional compliance measures.")
    print("  Updated brk-mbta-communities-compliance")

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Town Meeting underway — Chestnut Hill West rezoning APPROVED on May 28, rezoning the commercial area along Boylston Street/Route 9 near the Newton border for multi-use development with housing. Voters overwhelmingly approved a tax override to stave off cuts to schools and town departments. Continuation sessions were reserved for June 2-4 if needed. The warrant contained 25 articles including the Town budget, 10 bylaw/zoning amendments, and 6 resolutions.")
    print("  Updated brk-annual-town-meeting-2026")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-10T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Southeast and Southwest Area Plans adoption vote is June 23 — 13 DAYS AWAY. Both plans were formally submitted and introduced to the Common Council on May 5. Currently cycling through Boards, Commissions, and Committees — each meeting is open for public comment. The plans shape land use, housing density, and transportation in two of Madison's fastest-growing areas. Property assessment appeals in hearing phase (Board of Assessors meeting weekly through summer). BRT Route B federal funding ($118M) remains at HIGH risk — no signed FTA agreement, city developing alternate strategies for scaled-back improvements.")
    print("  Updated mad-new-housing-developments")

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Route A continues 15-minute service. Route B: transportation director publicly characterized the city as at 'high' risk of not receiving the $118.1M FTA Small Starts grant — FTA recommended the funding in May 2024 but no contract signed. Trump administration and congressional spending cuts placing the grant in jeopardy. Metro Transit developing alternate strategies to deliver 'some of the BRT improvements' without federal funding. Design work continuing through 2026; construction expected 2027, service 2028 if funding secured. SE/SW Area Plans vote June 23 (13 DAYS) — transit-oriented development along BRT corridors is central to both plans.")
    print("  Updated mad-east-west-brt-construction")

# SE Area Plan: committee review underway
idx, issue = find_issue(madison["issues"], "mad-southeast-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Southeast Area Plan currently in committee review — Boards, Commissions, and Committees may propose amendments before the June 23 Common Council vote (13 DAYS). Each committee meeting is open for public comment. The plan was formally introduced May 5. Advocates for more housing along major corridors with existing transit infrastructure.")
    print("  Updated mad-southeast-area-plan")

idx, issue = find_issue(madison["issues"], "mad-southwest-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 10 update:** Southwest Area Plan in the same committee review pipeline as the SE plan — final adoption vote June 23 (13 DAYS). Both plans submitted together May 5. Committee meetings open for public comment. The plan shapes development in one of Madison's fastest-growing areas.")
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
        "\n\n**June 10 update:** Mail ballot deadline PASSED yesterday — remaining count is from finite pool of already-received ballots. D4: Shaw (R) leads 26,264 (33.27%) vs Traut (D) 24,643 (31.22%) — margin ~1,600, November runoff certain. D5: Dixon (R) leads 62,640 (48.5%) vs Foley (D) 58,654 (45.4%) — gap widened to ~4,000 votes. Voice of OC: 'Is an Incumbent Going to Lose Reelection?' Both seats trending Republican heading into November. OC Registrar posting daily 5 PM updates through June 26. Certification July 10. Developing November strategy for BOTH D4 and D5 is now the urgent priority. Governor: Becerra (D) 26.7% vs Hilton (R) 26.4%, both advance."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 10 update:** Governor: Becerra (D) 26.7% vs Hilton (R) 26.4% — ~65% of expected votes counted. AP, ABC7, NBC, CalMatters all project both advance to November. Mail ballot deadline passed yesterday. Steyer at ~21%. County certification deadline July 3. SD-34: Valencia (D) 63% vs Shader (R) 37% remains unchanged. First successful Builder's Remedy court case won in La Cañada Flintridge (80 units) — sets precedent for OC cities."
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
        "\n\n**June 10 update:** Huntington Beach housing element vote June 16 — 6 DAYS. $50K/month fines NOW ACCRUING as of June — $160K retroactive already owed. Court ordered Builder's Remedy project approvals within 60-90 days. First successful Builder's Remedy court case won in La Cañada Flintridge (80 units) — OC cities on notice. Mail ballot deadline passed yesterday. Governor: Becerra (D) leads Hilton (R) 26.7% to 26.4%. D4: Shaw (R) leads by ~1,600; D5: Dixon (R) leads by ~4,000. If both Republicans win November, county-level housing enforcement support seriously at risk. OC Streetcar launch pushed to March 2027."
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
        "\n\n**June 10 update:** ⚡ Garden Grove special council meeting held yesterday (June 9) — GKN VP Steve Carlin attended for the FIRST TIME. Chaos erupted during hours of testimony. Direct aid increased $250→$500/address — residents called it a 'drop in the bucket.' MMA extraction STILL delayed. NEW: ~50 gallons stormwater overflowed to storm drain, being tested. 44+ lawsuits filed. The crisis displaced thousands of families with young children. Mail ballot deadline passed yesterday — D4 Shaw (R) leads, D5 Dixon (R) leads. The next supervisors shape FY27 childcare and family services budgets. HB housing vote June 16 (6 DAYS)."
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
        "\n\n**June 10 update:** Filing period opens July 20 (40 DAYS). At least 8 candidates with 7 appointed treasurers for D1. Known candidates include Alexandria Anderson (retired athlete) and Steven Brown (Medtronic, raised ~$6K). George Morales sworn in as Pct 4 commissioner TOMORROW (June 11). AISD full cut plan released June 3 — 215 educator salaries, protest rally June 5. Board vote June 18 (8 DAYS). Bond final vote July 23 (43 DAYS). Mayor Watson opposes bond. Council on summer recess until July 23."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 10 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. If denied: automatic interlocutory appeal pauses everything. If granted: ATP's bond validation suit dismissed. ATP says 'on schedule' for 2027 construction. FTA signed off on key environmental review January 16. Three major contracts expected in 2026: full 9.8-mile buildout, operations/maintenance facility, train cars. Council on recess until July 23."
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
        "\n\n**June 10 update:** AT-Home Initiative ($6.7M, 5-year) proposals closed June 2 — city in review/selection phase. Up to 3 providers selected; contracts start September 2026. Navigation Center on track for late summer/early fall opening. 13-member Advisory Board formed. AISD full cut plan released June 3: 215 educator salaries cut, 3,000 students lost, protest rally June 5. Board vote June 18 (8 DAYS) — school closures compound homelessness risk. Bond final vote July 23 (43 DAYS) — shelter infrastructure NOT in ~$390M direction. Morales sworn in TOMORROW (June 11)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 10 update:** 157th cadet class mid-training — graduation September 18. 156th class graduated May 1 with 25 of 49 (51% completion). APD has ~1,400+ sworn officers with 365 vacancies. April 2025 audit: current pace of ~87 new officers/year inadequate to close gap by 2027. Interim Chief Henderson indicated next class roughly twice as large. Council on recess until July 23. Morales sworn in TOMORROW (June 11) — his law enforcement background (former constable) may influence county-level public safety coordination."
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
        "\n\n**June 10 update:** Raising Travis County at record pace — 1,000 scholarships funded, October target reached months early. Wait times dropped from 2 years to months. $2.6M gap funding to 150 providers. Virtual town hall June 16 at 6 PM (6 DAYS). George Morales sworn in as Pct 4 commissioner TOMORROW (June 11) — immediately begins voting on additional childcare contracts. CDBG public comment period opens June 17. AISD full cut plan released June 3: 215 educator salaries, school closures impacting family childcare and after-school access. Board vote June 18 (8 DAYS)."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-10T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-10T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-10T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-10T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-10T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
