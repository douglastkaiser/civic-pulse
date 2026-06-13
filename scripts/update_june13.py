#!/usr/bin/env python3
"""
June 13, 2026 updates for all issue and organization data files.
Key developments since June 12:
  - NYC: ⚡ EARLY VOTING STARTS TODAY (June 13) — polls open 9 AM - 5 PM; also LAST DAY to
    register in person and last day to request absentee ballot; CD-7 prediction markets:
    Valdez surges to 80% (up from 77%), Reynoso 19%
  - OC D5: ⚡ Dixon (R) appears to have RETAKEN lead from Foley (D) at ~48% vs ~46% in latest
    counts — reversing the brief Democratic lead reported June 10; race continues to seesaw
    with only ~10K ballots remaining; certification July 10
  - OC D4: Traut (D) maintains lead at 33%+ vs Shaw (R) 31%+; both advance to November
  - Austin AISD: Board vote June 18 (5 DAYS) — 558 positions affected by $181M shortfall;
    no delay announced; boundary realignment workshops June 16 (3 DAYS)
  - Austin Bond: Survey data in — top priorities: transportation (19.8%), housing (18.5%),
    parks (16.3%); ~70% support a tax increase; survey open through June 23 (10 DAYS)
  - Garden Grove: GKN SVP Carlin attended June 9 special council meeting — dodged reimbursement
    questions, promised community town hall; MMA extraction STILL delayed ~23 days post-incident
  - HB Housing: Vote June 16 (3 DAYS); revised draft posted June 8; $50K/month fines accruing
  - Madison: Plan Commission June 15 (2 DAYS); agendas posting TODAY; council vote June 23 (10 DAYS)
  - Cambridge: CRA finalized $9.375M loan for 2400 Mass Ave; ~64 days left in ShotSpotter removal
  - Brookline: No new developments; 26 Pleasant St postponed to fall Special Town Meeting
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
austin["last_scraped"] = "2026-06-13T12:00:00Z"

# AISD: vote in 5 days, $181M shortfall confirmed
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Board vote on $181M budget shortfall remains scheduled for June 18 — 5 DAYS. No delay announced despite earlier speculation. 558 positions affected districtwide: 215 teaching positions, 228 vacant roles, and 115 other staff. District has identified 73% of the $132M in required spending cuts so far ($85M central office + $25M campus cuts). Boundary realignment workshops June 16 (3 DAYS) and June 22-23. Teachers union urging district to use remaining time before the vote to minimize impacts to currently employed staff. Staff, students, and parents voiced concerns at June 9 public session. CDBG public comment opens June 17 (4 DAYS). Travis County offices closed June 18-19 for Juneteenth.")
    print("  Updated atx-aisd-budget-crisis")

# Pct 4: Morales serving, $17.65M childcare approved
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Morales now serving as Pct 4 Commissioner (sworn in June 11). Commissioners Court approved $17.65M expansion of Raising Travis County childcare and after-school programs — 1,000+ scholarships annually for children up to 3 years old, funding to Workforce Solutions Capital Area. Virtual town hall June 16 at 6 PM — 3 DAYS. CDBG public comment opens June 17 (4 DAYS) through July 20. Travis County offices closed June 18-19 for Juneteenth. ⚡ AISD board vote on $181M shortfall June 18 (5 DAYS) — 558 positions affected.")
    print("  Updated tc-pct4-runoff")

# Homelessness: navigation center operator solicitation
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** AT-Home Initiative ($6.7M, 5-year) — city in review/selection phase after proposals closed June 2. Navigation Center at 2401 S. I-35 Frontage Rd on track for late summer/early fall opening; city soliciting operator proposals (up to $250K in funding). 13-member Advisory Board formed from 69 applications. Bond final vote July 23 (40 DAYS) — shelter infrastructure NOT in ~$390M direction. AISD board vote June 18 (5 DAYS) — school closures compound homelessness risk. Morales now serving as Pct 4 commissioner.")
    print("  Updated atx-hso-plan-adopted")

# Bond: survey data incoming
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Bond community input survey open through June 23 — 10 DAYS remaining. Survey results emerging from 2,000+ responses: top priorities are transportation (19.8%), housing & homelessness (18.5%), and parks (16.3%). In open-ended responses, 34% named housing as Austin's most urgent issue, 22% cited transportation. ~70% of respondents support a property tax increase (most common: additional $10/month). Mayor Watson opposes the bond, but 6 council members voted to move forward with the $390M staff scenario. A bond task force earlier proposed a larger ~$770M package including housing. Council on recess until July 23 — final vote that day (40 DAYS). AISD board vote on $181M shortfall June 18 (5 DAYS).")
    print("  Updated atx-2026-bond")

# D1 Election: filing details
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Filing period opens July 19 (first day is Saturday; first in-person filing day Monday July 20 — 37 DAYS). Filing deadline August 17. Harper-Madison term-limited, not running — first open D1 seat in 8 years. At least 2 candidates have formally filed; semi-annual campaign finance reports due in July will reveal full fundraising landscape. Election Day November 3. Council on recess until July 23. Bond survey open through June 23 — transportation and housing top public priorities. AISD board vote June 18 (5 DAYS).")
    print("  Updated atx-d1-election")

# Project Connect: federal milestone context
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Legal status unchanged — trial halted per TX Supreme Court May 22 ruling; Judge Shepperd must rule on AG Paxton's jurisdictional plea. Project at ~10 miles/$8.2B with 15 stations. ATP achieved federal Record of Decision — a key NEPA milestone clearing the way for potential construction. ATP expects three major contracts in 2026. Council on recess until July 23. Morales now serving as Pct 4 commissioner — his CapMetro coordination priorities could influence county-level transit investment.")
    print("  Updated atx-project-connect-legal-update")

# Childcare: $17.65M approved
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Commissioners Court approved $17.65M expansion of Raising Travis County — childcare scholarships + after-school programs. 1,000+ scholarships funded annually for children up to 3, reaching October target months early. Wait times dropped from 2 years to months. 2,650+ students in out-of-school time programs. Virtual town hall June 16 at 6 PM — 3 DAYS. CDBG public comment opens June 17 (4 DAYS). AISD board vote on $181M shortfall June 18 (5 DAYS) — school closures directly impact childcare and after-school access. Travis County offices closed June 18-19 for Juneteenth.")
    print("  Updated tc-childcare-funding")

# APD Staffing
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** 157th cadet class mid-training — started January 26, graduation September 18, 2026. 156th class graduated May 1 (49 cadets started). 155th class had 33% attrition with 42 graduates. APD remains 300+ officers short of authorized strength. Morales now serving as Pct 4 commissioner — law enforcement background (former constable) supports county-level public safety coordination. AISD budget includes 280 position cuts including campus police — board vote June 18 (5 DAYS). Council on recess until July 23.")
    print("  Updated atx-apd-staffing-audit")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-13T12:00:00Z"

# Garden Grove: GKN council meeting update, extraction still delayed
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 13 update:** GKN SVP Steve Carlin attended June 9 special council meeting — promised a community town hall but DODGED ALL QUESTIONS about reimbursement for displaced residents. His refusal to answer direct questions was met with loud boos from the audience. GKN has committed $5M total ($3M United Way + $1M community + $1M Red Cross) but BOS Chairman Chaffee called it a 'drop in the bucket.' Chemical extraction STILL delayed — sealed trucks haven't arrived; no revised start date. MMA remains in compromised tank ~23 days after May 21 incident. FBI served search warrant June 10, collecting documents on MMA storage, cooling mechanisms, and employee complaints. 44+ lawsuits filed. Next regular council meeting June 16 (3 DAYS). ⚡ OC D5 race continues to seesaw — Dixon (R) appears to have retaken lead from Foley (D); new supervisors will shape industrial safety oversight.")
    print("  Updated Garden Grove chemical crisis")

# D4: Traut maintaining lead
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Traut (D) maintains lead at 33%+ vs Shaw (R) 31%+ per latest count. Only ~10,000 ballots remaining countywide — pool nearly exhausted. Both advance to November general regardless. OC Registrar posting updates at 5 PM weekdays; next scheduled updates June 16, 18, 24, 26. Final certification July 10. Late mail ballots have consistently skewed Democratic. GKN SVP attended June 9 council meeting — dodged reimbursement questions; FBI served search warrant June 10. HB housing vote June 16 (3 DAYS) — revised draft posted June 8.")
    print("  Updated oc-bos-district-4-open-seat")

# D5: Dixon RETAKES lead
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** ⚡ Race continues to SEESAW — after Foley (D) briefly pulled ahead around June 10, Dixon (R) appears to have retaken the lead in the latest counts at approximately 48% vs Foley's 46%. The race has been extremely volatile with leads changing hands multiple times since election night. Only ~10,000 ballots remaining countywide. OC Registrar updates at 5 PM weekdays; certification July 10. Both candidates head to November general regardless — but the primary result signals momentum and determines whether Foley enters the general as the 'trailing incumbent.' If Dixon wins November, Republicans retake the 3-2 board majority controlling the $10.5B budget, housing enforcement, and homelessness investment.")
    print("  Updated oc-bos-district-5-defense")

# Governor: Becerra lead solidifying
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Becerra (D) ~28% vs Hilton (R) ~25% at 88% of expected votes counted — gap continues to WIDEN as late mail ballots process. Hilton led on election night but Becerra overtook him as mail ballots were counted; AP confirmed both advancing to November. Steyer at ~23%, has not conceded. County certification deadline July 3. Governor determines California's housing enforcement posture — RHNA, Builder's Remedy, AG referrals. HB housing vote June 16 (3 DAYS). D5 supervisor race seesawing — Dixon (R) appears to have retaken lead from Foley (D).")
    print("  Updated ca-governor-2026")

# HB: 3 DAYS to vote, revised draft posted
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Huntington Beach housing element vote is June 16 — 3 DAYS AWAY. City posted a revised Draft Housing Element Update on June 8 — the plan would zone for ~13,000 new units. Council voted 6-0 on June 2 to postpone from that night to June 16 (Councilmember Van Der Mark absent). City is now PAST the court-ordered May 28 deadline — $50K/month fines actively accruing since June 1. Total retroactive fines: $210K+ ($10K/month Jan 2025 - May 2026 + $50K in June). Court ordered Builder's Remedy project approvals within 60-90 days. All legal avenues exhausted (US Supreme Court declined to hear challenge in February). Governor race: Becerra (D) extending lead — favorable for state housing enforcement.")
    print("  Updated oc-newsom-housing-warning (HB)")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Revenue service date remains March 2027. The $649M project continues street testing on Santa Ana Boulevard. GKN chemical crisis aftermath continues — MMA still in compromised tank ~23 days post-incident; extraction delayed; FBI investigation underway. GKN SVP attended June 9 council meeting, dodged reimbursement questions. Next Garden Grove council meeting June 16 (3 DAYS).")
    print("  Updated oc-streetcar-launch")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-13T12:00:00Z"

# Primary: EARLY VOTING STARTS TODAY
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** ⚡ EARLY VOTING STARTS TODAY — polls open 9 AM - 5 PM. TODAY is also the LAST DAY to register to vote in person AND the last day to request an absentee/mail ballot. Early voting runs through June 21. Primary Election Day June 23 (10 DAYS). You MUST go to your assigned early voting poll site — it may differ from your Election Day location (check vote.nyc). CD-7 (Velázquez seat): prediction markets now show Valdez (DSA) at 80% (up from 77%), Reynoso at 19%. Emerson/PIX11 poll: Valdez 23%, Reynoso 21%, Won 13% — but 43% undecided. Clear age divide: under-40 voters break for Valdez 33%-15%; over-50 break for Reynoso 27%-13%. Strong DSA ground operation may drive early vote turnout.")
    print("  Updated nyc-june-primary-2026")

# Housing: ADU deadline passed yesterday
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** City of Yes Plus One ADU Program intake survey deadline PASSED yesterday (June 12). 3,100+ homeowners applied since March reopening — up to $395,000 per homeowner ($175K forgivable grant + $220K low-interest loan). Funding reviewed on rolling basis. ⚡ EARLY VOTING STARTS TODAY — polls open 9 AM - 5 PM. Primary June 23 (10 DAYS). Brooklyn council seats on the ballot will shape housing policy. Q1 2026 housing permits nearly doubled: 28,773 units filed vs 14,338/quarter average in 2025. East 98th Street rezoning DEIS required — 786 units across six sites, 157-236 permanently affordable under MIH.")
    print("  Updated nyc-atlantic-ave-rezoning")

# COPA: early voting context
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** COPA bill language still being finalized — no hearing date yet. 26 sponsors (veto-proof). Targets distressed buildings: Alternative Enforcement Program, Certificate of No Harassment list, or expiring subsidies. ⚡ EARLY VOTING STARTS TODAY — polls open 9 AM - 5 PM. Brooklyn council seats on the ballot will determine whether COPA has the votes to pass. Last day to register in person. Primary June 23 (10 DAYS).")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-13T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** ~64 days remaining in the 90-day ShotSpotter removal window (deadline mid-August 2026). Device removal/disabling underway per City Manager Huang's direction. Cambridge Day reports (June 1) that officers 'aren't happy' — the Cambridge Police Patrol Officers Association continues to push back, criticizing the council's decision. The 5-2-2 vote on May 19 directed removal within 90 days. Councillors Nolan and McGovern maintain the system showed only 35% of notifications were confirmed gunfire. No council revisitation expected.")
    print("  Updated cam-shotspotter-banned")

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** CRA finalized $9.375M loan to North Cambridge Partners for the 2400 Massachusetts Ave. project — bought out the existing Leader Bank mortgage and replaced it with a 4.5% interest rate over two years. CRA initially invested $5M in January 2024, purchasing Class A membership shares. The project plans 56 homes + retail in North Cambridge as a potential first social housing project. All 13 task force members appointed (May). Listening sessions planned for this summer + RFI from developers. Barrett v. Cambridge inclusionary zoning lawsuit remains in discovery — AG Campbell intervened in April.")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-13T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Town Meeting concluded. No new developments. Article 16 (26 Pleasant Street — 103 apartments including 15 affordable) officially POSTPONED to fall Special Town Meeting (typically November). Developer and community expected to engage in interim discussions to refine the proposal before fall. Chestnut Hill West rezoning APPROVED. Tax override approved. Updated ADU rules (Article 14) and restored inclusionary payments (Article 15) in effect.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Brookline remains compliant — AG approved new zoning by-laws March 23, 2026. 165 of 177 communities statewide have achieved compliance. Town Meeting approved Chestnut Hill West rezoning and updated ADU rules — adding density capacity. 26 Pleasant Street (103 units) postponed to fall Special Town Meeting. No further actions until fall session.")
    print("  Updated brk-mbta-communities-compliance")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-13T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Plan Commission review is June 15 — 2 DAYS AWAY. Agendas are typically posted the Friday prior (TODAY). Council adoption vote June 23 (10 DAYS). Both SE and SW Area Plans shape land use, housing density, and transportation in Madison's fastest-growing areas. Public comment registration opens with the agenda. BRT Route B federal funding ($118M) remains at HIGH risk — no signed FTA agreement. SE/SW plans include transit-oriented development along BRT corridors.")
    print("  Updated mad-new-housing-developments")

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Route A continues 15-minute service. Route B: FTA says funding 'still in the pipeline' but city characterizes risk as 'moderate to high' — no signed FTA agreement for $118.1M Small Starts grant. Metro Transit developing alternate approaches if federal funding falls through. SE/SW Area Plans: Plan Commission review June 15 (2 DAYS), agendas posting TODAY; council vote June 23 (10 DAYS). Transit-oriented development along BRT corridors central to both plans.")
    print("  Updated mad-east-west-brt-construction")

idx, issue = find_issue(madison["issues"], "mad-southeast-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Plan Commission review is June 15 — 2 DAYS AWAY. Agendas posting TODAY (Friday prior). Council adoption vote June 23 (10 DAYS). Public comment registration opens with the agenda. The plan focuses on mixed-use and higher density along Milwaukee Street, Cottage Grove Road, Atwood Avenue, Monona Drive, and Stoughton Road. BRT Route B federal funding ($118M) remains at high risk.")
    print("  Updated mad-southeast-area-plan")

idx, issue = find_issue(madison["issues"], "mad-southwest-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 13 update:** Plan Commission review June 15 (2 DAYS), agendas posting TODAY. Council adoption vote June 23 (10 DAYS). Public comment opportunities at each committee meeting. The plan includes mixed-use developments along Whitney Way, Raymond Road, Schroeder Road, and McKee Road — one of Madison's fastest-growing areas. SE/SW plans were both introduced to the Common Council on May 5 and have been referred to relevant boards, commissions, and committees.")
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
        "\n\n**June 13 update:** ⚡ D5 race continues to SEESAW — Dixon (R) appears to have retaken the lead from Foley (D) at ~48% vs ~46% in the latest counts, reversing the brief Democratic lead reported June 10. The lead has changed hands multiple times since election night. Only ~10K ballots remaining countywide. D4: Traut (D) maintains lead at 33%+ vs Shaw (R) 31%+. Certification July 10. If Dixon holds through November, Republicans retake the 3-2 majority. OC Registrar updates at 5 PM weekdays; next scheduled updates June 16, 18, 24, 26. GKN SVP attended June 9 council meeting — dodged reimbursement questions; FBI served search warrant. HB housing vote June 16 (3 DAYS)."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 13 update:** Governor: Becerra (D) ~28% vs Hilton (R) ~25% at 88% counted — gap continues to widen. Hilton led on election night but was overtaken as mail ballots came in. County certification deadline July 3. D5 supervisor race seesawing — Dixon (R) appears to have retaken lead from Foley (D). HB housing vote June 16 (3 DAYS) — revised draft posted June 8; $50K/month fines accruing."
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
        "\n\n**June 13 update:** Huntington Beach housing vote June 16 — 3 DAYS. City posted revised Draft Housing Element Update on June 8. Council voted 6-0 on June 2 to postpone to June 16. $50K/month fines actively accruing since June 1 — total owed now $210K+. Court ordered Builder's Remedy project approvals within 60-90 days. US Supreme Court declined to hear HB's challenge in February — all legal avenues exhausted. D5 supervisor race seesawing — Dixon (R) appears to have retaken lead from Foley (D); county-level housing enforcement posture at stake. Governor: Becerra (D) extending lead, favorable for state housing enforcement."
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
        "\n\n**June 13 update:** GKN SVP Carlin attended June 9 special council meeting — dodged reimbursement questions, promised community town hall. $5M committed but no formal claims infrastructure. MMA extraction still delayed ~23 days post-incident. FBI search warrant served June 10 — collecting documents on storage, cooling, employee complaints. 44+ lawsuits filed. D5 supervisor race seesawing — Dixon (R) appears to have retaken lead from Foley (D); if Dixon wins November, Republicans retake 3-2 majority affecting FY27 childcare and family services investments. HB housing vote June 16 (3 DAYS)."
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
        "\n\n**June 13 update:** Filing period opens July 19 (first in-person day July 20 — 37 DAYS). Filing deadline August 17. At least 2 candidates have formally filed for D1 (Harper-Madison term-limited). Semi-annual campaign finance reports due July. Bond community survey results: transportation (19.8%), housing (18.5%), parks (16.3%) top priorities; ~70% support tax increase. AISD board vote on $181M shortfall June 18 (5 DAYS) — 558 positions affected. Council on recess until July 23."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 13 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. Project at ~10 miles/$8.2B with 15 stations. ATP achieved federal Record of Decision — key NEPA milestone for potential construction. ATP expects three major contracts in 2026. Morales now serving as Pct 4 commissioner — CapMetro coordination priorities could influence county transit investment. Council on recess until July 23."
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
        "\n\n**June 13 update:** AT-Home Initiative — city in review/selection phase. Navigation Center at 2401 S. I-35 on track for late summer/early fall; operator proposals solicited (up to $250K). 13-member Advisory Board formed from 69 applications. AISD board vote on $181M shortfall June 18 (5 DAYS) — school closures compound homelessness risk. Bond final vote July 23 (40 DAYS) — shelter infrastructure NOT in $390M direction."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 13 update:** 157th cadet class mid-training (started Jan 26) — graduation September 18. 156th class graduated May 1. 155th class: 33% attrition, 42 graduates. APD remains 300+ officers short. Morales now serving as Pct 4 commissioner — law enforcement background strengthens county public safety coordination. AISD $181M shortfall includes 280 position cuts including campus police — board vote June 18 (5 DAYS). Council on recess until July 23."
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
        "\n\n**June 13 update:** Commissioners Court approved $17.65M expansion of Raising Travis County childcare and after-school programs — 1,000+ scholarships annually for children up to 3. Morales now serving as Pct 4 commissioner, immediately voting on these contracts. Virtual town hall June 16 at 6 PM (3 DAYS). CDBG public comment opens June 17 (4 DAYS). AISD board vote on $181M shortfall June 18 (5 DAYS) — school closures impact childcare and after-school access. Travis County offices closed June 18-19 for Juneteenth."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-13T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-13T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-13T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-13T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-13T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
