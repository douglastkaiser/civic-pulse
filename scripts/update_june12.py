#!/usr/bin/env python3
"""
June 12, 2026 updates for all issue and organization data files.
Key developments since June 11:
  - Austin AISD: ⚡ Deficit ballooned to $95M year-end ($76M worse than expected); reserves falling
    to 10% ($137M); board may DELAY June 18 vote to June 25; district needs another loan in September
    for payroll; $30M in property sales didn't materialize
  - OC: ⚡ DEMOCRATS PULL AHEAD in BOTH supervisor races (Voice of OC, June 10 evening count):
    D4: Traut (D) now leads Shaw (R) 33%+ vs 31%+; D5: Foley (D) 46.98% vs Dixon (R) 46.81%
    Only ~10,000 ballots remaining countywide. MAJOR REVERSAL from election night.
  - OC: GKN Aerospace donated $3M to United Way OC Community Resilience Fund + $1M for broader
    community initiatives (in addition to earlier $1M Red Cross). Extraction STILL delayed.
  - CA Governor: At 88% reporting — Becerra (D) ~28% vs Hilton (R) ~25%. Gap widening.
  - NYC: ADU deadline TODAY (June 12); early voting starts TOMORROW (June 13);
    registration + absentee ballot request deadline also June 13
  - NYC: CD-7 prediction markets: Valdez 77%, Reynoso 17% — DSA-backed candidate surging
  - HB: Housing vote June 16 (4 DAYS); $50K/month fines accruing
  - Madison: Plan Commission review June 15 (3 DAYS); council vote June 23 (11 DAYS)
  - Cambridge: ShotSpotter removal ~65 days remaining; 2400 Mass Ave social housing advancing
  - Brookline: Town Meeting concluded; no new developments
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
austin["last_scraped"] = "2026-06-12T12:00:00Z"

# AISD: deficit ballooned, vote may be delayed
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** ⚡ AISD's fiscal crisis deepened dramatically — the district now projects a $95M year-end deficit, $76M WORSE than previously expected. Reserves are projected to fall to just 10% ($137M), below the board's already-reduced 15% target. Key factors: $30M in expected property sales did not materialize, $26M in missed funding from declining enrollment/attendance, $15M in additional unspecified expenses. District leaders say they anticipate needing ANOTHER LOAN in September to meet payroll (following last year's $19M borrowing). Board members were caught off guard by the revised numbers — several questioned how they could vote on a budget days after receiving the proposal. Trustees discussed whether to DELAY the June 18 vote to June 25 or amend the budget in August. 280 proposed position cuts (90 currently filled). Central office cut $17M this week. Boundary realignment workshops June 16 (4 DAYS) and June 22-23 (virtual).")
    print("  Updated atx-aisd-budget-crisis")

# Pct 4: Morales first full day
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Morales's first full day as Pct 4 Commissioner — sworn in yesterday (June 11). His immediate priorities include road repairs, expanded Capital Metro bus service coordination, and affordable healthcare access through Central Health. 'There's so many services being gutted right now, but we need to find a way to bring those services back,' Morales told KUT. Raising Travis County virtual town hall June 16 at 6 PM (4 DAYS). CDBG public comment period opens June 17 (5 DAYS) through July 20, public hearing July 14. ⚡ AISD deficit ballooned to $95M — board may delay June 18 vote to June 25. Travis County offices closed June 18-19 for Juneteenth.")
    print("  Updated tc-pct4-runoff")

# Homelessness
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** AT-Home Initiative ($6.7M, 5-year) — city continues review/selection phase after proposals closed June 2. Up to three providers selected; contracts start September 2026. Navigation Center on track for late summer/early fall opening; 13-member Advisory Board formed. ⚡ AISD deficit ballooned to $95M — board may delay June 18 vote. School closures compound homelessness risk; district needs another loan in September for payroll. Bond final vote July 23 (41 DAYS) — shelter infrastructure NOT in ~$390M direction. Morales began first full day as Pct 4 commissioner.")
    print("  Updated atx-hso-plan-adopted")

# Bond: countdown
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Council on summer recess until July 23 — bond conversation resumes then. The ~$390M bond direction: Parks $250M, Transportation $92M, Community Facilities $48M — does NOT include housing. Bond community input survey open through June 23. Mayor Watson opposes the bond. Final vote July 23 (41 DAYS). Mid-August council vote to formally call November election. ⚡ AISD deficit ballooned to $95M; board may delay June 18 vote to June 25. District needs another loan in September — fiscal instability across Austin's public institutions complicates the bond narrative.")
    print("  Updated atx-2026-bond")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Filing period opens July 20 (38 DAYS). At least 8 candidates declared for D1. Semi-annual campaign finance filings due in July will reveal fundraising trajectories. Council on summer recess until July 23. Election Day November 3. Morales began first full day as Pct 4 commissioner. ⚡ AISD deficit ballooned to $95M — board may delay budget vote; fiscal crisis dominates local attention. Raising Travis County virtual town hall June 16 (4 DAYS).")
    print("  Updated atx-d1-election")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Legal status unchanged — trial remains halted per TX Supreme Court May 22 ruling sending the case back to Judge Shepperd to rule on AG Paxton's jurisdictional plea. If denied: automatic interlocutory appeal pauses everything. If granted: ATP's bond validation suit dismissed entirely. Project has shrunk to ~10 miles/$8.2B with 15 stations. ATP expects to award three major contracts in 2026. Morales began first full day as Pct 4 commissioner — his CapMetro coordination priorities could influence county-level transit investment. Council on recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Morales's first full day as Pct 4 commissioner — immediately begins voting on Raising Travis County childcare contracts. Program at record pace: 1,000+ scholarships funded (reaching October target months early), wait times dropped from 2 years to months, $2.6M gap funding to 150 providers, 2,650+ students in out-of-school time programs. Virtual town hall June 16 at 6 PM — 4 DAYS. CDBG public comment period opens June 17 (5 DAYS). ⚡ AISD deficit ballooned to $95M — school closures impact childcare and after-school access; district needs September loan for payroll. Travis County offices closed June 18-19 for Juneteenth.")
    print("  Updated tc-childcare-funding")

# APD Staffing
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** 157th cadet class mid-training — graduation scheduled September 18, 2026. APD has ~1,400+ sworn officers with 365 vacancies. Recent classes show 51-52% attrition rates. Interim Chief Henderson indicated next class roughly twice as large. Morales began first full day as Pct 4 commissioner — his law enforcement background (former constable) strengthens county-level public safety coordination. ⚡ AISD deficit ballooned to $95M — 280 position cuts proposed including campus police. Council on recess until July 23.")
    print("  Updated atx-apd-staffing-audit")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-12T12:00:00Z"

# Garden Grove: FBI aftermath, GKN donations
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 12 update:** Post-FBI raid fallout continues. GKN Aerospace has now committed $5M total in community support: $3M to United Way OC Community Resilience Fund, $1M for broader community initiatives, and an earlier $1M to the American Red Cross during the evacuation. OC BOS Chairman Chaffee called the $3M donation a 'drop in the bucket' and criticized GKN for failing to set up formal claims infrastructure. Garden Grove officials demanding company representatives attend next Tuesday's council meeting for continued accountability hearings. Chemical extraction STILL DELAYED — specialized sealed trucks have not arrived; no revised start date announced. The MMA remains in the compromised tank 22 days after the May 21 incident. 44+ lawsuits filed in OC Superior Court and US District Court. ⚡ Democrats pulled ahead in BOTH D4 and D5 supervisor races — new supervisors will shape county oversight of industrial safety.")
    print("  Updated Garden Grove chemical crisis")

# D4: DEMOCRATS PULL AHEAD
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** ⚡ REVERSAL: Traut (D) has pulled AHEAD of Shaw (R) — Traut now leads with 33%+ vs Shaw at 31%+, flipping from election night when Shaw led. Voice of OC headline: 'Democrats Pull Ahead in Orange County Supervisor Races.' Only ~10,000 ballots remaining countywide — the pool is nearly exhausted. Late-counted mail ballots skewing Democratic, consistent with California trends. OC Registrar posting another update today (June 12) at 5 PM. Additional updates: June 16, 18, 24, 26. Final certification July 10. Both candidates advance to November regardless — but Traut enters the general with momentum. FBI raided GKN Aerospace June 10 — federal probe adds urgency to D4 accountability. HB housing vote June 16 (4 DAYS).")
    print("  Updated oc-bos-district-4-open-seat")

# D5: FOLEY PULLS AHEAD
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** ⚡ REVERSAL: Foley (D) has pulled AHEAD of Dixon (R) — Foley leads 46.98% vs Dixon 46.81%, an extremely narrow margin after Dixon led since election night. Voice of OC: 'Democrats Pull Ahead in Orange County Supervisor Races.' Late mail ballots continuing to skew Democratic. Only ~10,000 ballots remaining countywide. OC Registrar posting update today at 5 PM. Certification July 10. This race determines the 3-2 board majority — if Foley holds the lead through certification, she enters November as the incumbent with momentum. If Dixon ultimately wins November, Republicans retake the board majority affecting the $10.5B budget, housing enforcement, and homelessness investment.")
    print("  Updated oc-bos-district-5-defense")

# Governor: gap widening
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** At 88% of expected votes counted: Becerra (D) ~28% vs Hilton (R) ~25% — gap has WIDENED from the initial 26.7%/26.4% margin. Becerra's lead solidifying as late mail ballots are processed. Steyer at ~23%, has not conceded. Both Becerra and Hilton confirmed advancing to November per AP, ABC7, NBC, CalMatters. County certification deadline July 3. The governor determines California's housing enforcement posture — RHNA, Builder's Remedy, AG referrals. ⚡ Democrats also pulling ahead in OC D4 and D5 supervisor races — statewide and local Democratic momentum in late mail ballot counting.")
    print("  Updated ca-governor-2026")

# HB: 4 DAYS to vote
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Huntington Beach housing element vote is June 16 — 4 DAYS AWAY. The court-ordered deadline to adopt a compliant housing element was May 28 — the city is now past deadline with $50K/month fines actively accruing. Total retroactive fines: $160K+ (at $10K/month since January 2025, escalating to $50K/month in June). The plan would zone for ~13,000 new units. Court ordered Builder's Remedy project approvals within 60-90 days. All legal avenues exhausted. ⚡ Democrats pulling ahead in both D4 and D5 supervisor races — county-level housing enforcement posture at stake. Governor race: Becerra (D) extending lead over Hilton (R) at 88% counted.")
    print("  Updated oc-newsom-housing-warning (HB)")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Revenue service date remains March 2027. The $649M project continues street testing on Santa Ana Boulevard. GKN chemical crisis aftermath continues to affect the Garden Grove corridor environment — MMA still in compromised tank 22 days post-incident. FBI raid fallout and 44+ lawsuits adding complexity to the area.")
    print("  Updated oc-streetcar-launch")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-12T12:00:00Z"

# Primary: early voting TOMORROW
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** ⚡ EARLY VOTING STARTS TOMORROW (June 13). June 13 is ALSO the last day to register to vote in person AND the last day to request an absentee/mail ballot by mail. Early voting runs June 13-21; polls open 6 AM - 9 PM. Primary Election Day June 23 (11 DAYS). CD-7 (Velázquez seat): prediction markets now show Valdez (DSA) at 77% vs Reynoso at 17% — a commanding lead driven by strong fundraising ($750K+ through March), Mayor Mamdani's endorsement, and DSA network mobilization. Emerson/PIX11 poll had Valdez 23%, Reynoso 21%, Won 13%, 43% undecided — but early vote dynamics may favor the candidate with the strongest ground operation. ADU deadline TODAY (see housing update).")
    print("  Updated nyc-june-primary-2026")

# Housing: ADU deadline TODAY
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** ⚡ City of Yes Plus One ADU Program intake survey deadline is TODAY (June 12). 3,100+ homeowners have applied since March reopening. Up to $395,000 per homeowner ($175K forgivable grant + $220K low-interest loan). Funding reviewed on rolling basis — early applicants have structural advantage as pipeline fills before funding is fully allocated. East 98th Street rezoning scoping session held yesterday (June 11) at 2 PM in East Flatbush — DEIS required; 786 dwelling units across six sites, 157-236 permanently affordable under MIH. Early voting starts TOMORROW (June 13) — Brooklyn council seats on the ballot will shape housing policy. Q1 2026 housing permits nearly doubled: 28,773 units filed vs 14,338/quarter average in 2025.")
    print("  Updated nyc-atlantic-ave-rezoning")

# COPA: early voting context
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** COPA bill language still being finalized — no hearing date yet. The 2026 version targets distressed buildings: those in the Alternative Enforcement Program, on the Certificate of No Harassment list, or about to lose subsidies. Timeline: 100 days total (45 days to express interest + 90 days to make offer). 26 sponsors (veto-proof). Backed by 200+ organizations. Mayor Mamdani supports. ⚡ Early voting starts TOMORROW (June 13) — Brooklyn council seats on the ballot will determine whether COPA has the votes to pass and override any future veto. Primary Election Day June 23 (11 DAYS).")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-12T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** ~65 days remaining in the 90-day ShotSpotter removal window (deadline mid-August 2026). Device removal/disabling underway per City Manager Huang's direction. The Cambridge Police Patrol Officers Association remains opposed, citing 11 gun violence incidents over 10 years flagged only by ShotSpotter. Councillors Nolan and McGovern maintain that after 10+ years of deployment, 'we have seen no proof of its effectiveness' — only 35% of notifications were confirmed as actual gunfire. No council revisitation of the order expected in the near term.")
    print("  Updated cam-shotspotter-banned")

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** All 13 task force members appointed. CRA advancing plans for 2400 Massachusetts Ave. in North Cambridge — 56 homes + retail — as a potential first social housing project. Listening sessions planned for this summer, plus a request for information from developers. The project aims for mixed-use with ground-floor retail, mixed-income homes, and an affordable homeownership component. CDD consultant hiring underway to support the task force's work. Barrett v. Cambridge inclusionary zoning lawsuit remains in discovery phase — AG Campbell intervened in April.")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-12T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Town Meeting concluded. Key outcomes: Chestnut Hill West rezoning APPROVED (May 28) — rezoning commercial area along Boylston Street/Route 9 for multi-use development with housing. Tax override overwhelmingly approved. Article 14 updated ADU rules. Article 15 restored cash-in-lieu payments for inclusionary units in sub-20-unit developments. Article 16 (26 Pleasant Street, 103 apartments including 15 affordable) POSTPONED to fall Special Town Meeting — this would have been the most significant new housing project. No further actions until fall session.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Brookline remains compliant — AG approved new zoning by-laws March 23, 2026. Not among the 9 towns sued in January 2026 for noncompliance. 165 of 177 communities have achieved compliance or conditional status. Results remain modest: only one known project in the rezoning corridor (childcare center + 3 housing units). Town Meeting approved Chestnut Hill West rezoning and updated ADU rules — both add density capacity. The 26 Pleasant Street rezoning (103 units) postponed to fall Special Town Meeting.")
    print("  Updated brk-mbta-communities-compliance")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-12T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Southeast and Southwest Area Plans adoption vote is June 23 — 11 DAYS AWAY. Plan Commission review is June 15 (3 DAYS) — the critical committee step before the full council vote. Both plans shape land use, housing density, and transportation in Madison's fastest-growing areas. Each committee meeting is open for public comment — agendas and registration instructions posted the Friday prior. BRT Route B federal funding ($118M) remains at HIGH risk — no signed FTA agreement.")
    print("  Updated mad-new-housing-developments")

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Route A continues 15-minute service. Route B: FTA says 'nothing has changed and funding is still in the pipeline,' but city characterizes risk as 'moderate to high' — no signed FTA agreement for the $118.1M Small Starts grant. Metro Transit developing alternate approaches if federal funding falls through — 'it may look different and come together in different ways.' Design work continuing through 2026; construction expected 2027, service 2028 if funded. SE/SW Area Plans: Plan Commission review June 15 (3 DAYS), council vote June 23 (11 DAYS) — transit-oriented development along BRT corridors central to both plans.")
    print("  Updated mad-east-west-brt-construction")

idx, issue = find_issue(madison["issues"], "mad-southeast-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Plan Commission review is June 15 — 3 DAYS AWAY. This is the critical committee step before the June 23 Common Council adoption vote (11 DAYS). Public comment registration opens with the agenda, posted the Friday prior to each meeting. The plan focuses on mixed-use and higher density along Milwaukee Street, Cottage Grove Road, Atwood Avenue, Monona Drive, and Stoughton Road.")
    print("  Updated mad-southeast-area-plan")

idx, issue = find_issue(madison["issues"], "mad-southwest-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 12 update:** Plan Commission review June 15 (3 DAYS), same pipeline as SE plan. Final adoption vote June 23 (11 DAYS). Public comment opportunities at each committee meeting. The plan includes mixed-use developments along Whitney Way, Raymond Road, Schroeder Road, and McKee Road — one of Madison's fastest-growing areas.")
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
        "\n\n**June 12 update:** ⚡ MAJOR REVERSAL: Democrats have pulled ahead in BOTH supervisor races. D4: Traut (D) now leads Shaw (R) with 33%+ vs 31%+ — flipped from election night. D5: Foley (D) leads Dixon (R) 46.98% to 46.81% — razor-thin margin after Dixon led since election night. Voice of OC headline: 'Democrats Pull Ahead in Orange County Supervisor Races.' Late mail ballots skewing Democratic, consistent with California trends. Only ~10,000 ballots remaining countywide. OC Registrar posting update today at 5 PM. Certification July 10. If these leads hold, Democrats maintain the 3-2 majority going into November with momentum. HB housing vote June 16 (4 DAYS). FBI raid fallout at GKN continues — GKN committed $5M total in community support."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 12 update:** Governor: Becerra (D) ~28% vs Hilton (R) ~25% at 88% of expected votes counted — gap WIDENING as late mail ballots are processed. Both confirmed advancing to November. County certification deadline July 3. ⚡ Democrats also pulling ahead in OC D4 and D5 — statewide Democratic momentum in late ballot counting. The governor determines California's housing enforcement posture for RHNA, Builder's Remedy, AG referrals."
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
        "\n\n**June 12 update:** Huntington Beach housing vote June 16 — 4 DAYS. City is now PAST the court-ordered May 28 deadline — $50K/month fines actively accruing. Total owed: $160K+. Court ordered Builder's Remedy project approvals within 60-90 days. ⚡ Democrats pulled ahead in BOTH D4 and D5 supervisor races — if leads hold through certification, the 3-2 Democratic majority is preserved going into November, maintaining county-level housing enforcement support. Governor: Becerra (D) extending lead over Hilton (R) at 88% counted — favorable for state housing enforcement posture. GKN committed $5M total in community support but chemical extraction still delayed."
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
        "\n\n**June 12 update:** GKN Aerospace committed $5M total in community support ($3M United Way OC Community Resilience Fund + $1M broader initiatives + $1M Red Cross), but BOS Chairman Chaffee called it a 'drop in the bucket' — no formal claims infrastructure established. Chemical extraction STILL delayed — MMA in compromised tank 22 days post-incident. 44+ lawsuits filed. ⚡ Democrats pulled ahead in BOTH D4 and D5 supervisor races — Traut (D) leads in D4, Foley (D) leads in D5. If leads hold, the 3-2 Democratic majority is preserved, protecting FY27 childcare and family services investments. HB housing vote June 16 (4 DAYS)."
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
        "\n\n**June 12 update:** Filing period opens July 20 (38 DAYS). At least 8 candidates for D1. Semi-annual campaign finance filings due in July. Morales began first full day as Pct 4 commissioner — priorities include roads, transit coordination, healthcare access. ⚡ AISD deficit ballooned to $95M ($76M worse than expected) — board may delay June 18 vote to June 25; district needs September loan for payroll. Fiscal instability across Austin's public institutions dominating local attention. Bond community input survey open through June 23. Council on recess until July 23."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 12 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 ruling. Project at ~10 miles/$8.2B with 15 stations. ATP expects three major contracts in 2026. Morales began first full day as Pct 4 commissioner — his CapMetro coordination priorities could influence county-level transit investment. Council on recess until July 23."
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
        "\n\n**June 12 update:** AT-Home Initiative — city continues review/selection phase. Navigation Center on track for late summer/early fall opening. Morales began first full day as Pct 4 commissioner. ⚡ AISD deficit ballooned to $95M — board may delay June 18 vote to June 25; district needs September loan for payroll. School closures compound homelessness risk. Bond final vote July 23 (41 DAYS) — shelter infrastructure NOT in ~$390M direction."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 12 update:** 157th cadet class mid-training — graduation September 18. APD has ~1,400+ sworn with 365 vacancies. Recent classes show 51-52% attrition rates. Interim Chief Henderson indicated next class roughly twice as large. Morales began first full day as Pct 4 commissioner — law enforcement background strengthens county-level public safety coordination. ⚡ AISD deficit ballooned to $95M — 280 position cuts proposed including campus police. Council on recess until July 23."
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
        "\n\n**June 12 update:** Morales's first full day as Pct 4 commissioner — immediately voting on Raising Travis County childcare contracts. His priorities include expanded bus service (CapMetro coordination) and affordable healthcare (Central Health). Program at record pace: 1,000+ scholarships, wait times dropped from 2 years to months. Virtual town hall June 16 at 6 PM (4 DAYS). CDBG public comment opens June 17 (5 DAYS). ⚡ AISD deficit ballooned to $95M — school closures impact childcare and after-school access; district needs September loan. Travis County offices closed June 18-19 for Juneteenth."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-12T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-12T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-12T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-12T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-12T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
