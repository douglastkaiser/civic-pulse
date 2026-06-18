#!/usr/bin/env python3
"""
June 18, 2026 updates for all issue and organization data files.
Key developments since June 17:
  - Austin AISD: Board vote TODAY June 18 on $181M budget shortfall —
    558 positions, 10 school closures; written comments due by 5 PM
  - Austin: Travis County offices CLOSED today & tomorrow for Juneteenth;
    37th Annual Juneteenth celebration 11 AM-2 PM at 800 Lavaca
  - OC: ⚡ HUNTINGTON BEACH HOUSING ELEMENT APPROVED 6-1 on June 16;
    Chad Williams sole dissent; city zones for 13,000+ residences;
    judge to rule next month on increasing fines to $150K/month
  - OC D5: Foley (D) 47.0% vs Dixon (R) 46.8% — registrar count TODAY ~5 PM;
    ~9,500 ballots remaining; both advance to November regardless
  - OC Streetcar: now 95% complete (up from 92%); testing underway;
    revenue service pushed to early 2027
  - Garden Grove: GKN donated $3M to OC Community Resilience Fund + $1M
    pledge; chemical extraction still delayed ~28 days post-incident
  - NYC: EARLY VOTING DAY 6 — polls 8 AM - 4 PM; 77,000+ voted through
    Day 5 citywide; Brooklyn 21,675; CD-7 Valdez 79% on prediction markets
  - Madison: SE & SW Area Plans council vote June 23 (5 DAYS)
  - Cambridge: ~59 days in ShotSpotter 90-day removal window
  - Brookline: Community Housing funding review happened yesterday
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
austin["last_scraped"] = "2026-06-18T12:00:00Z"

# AISD: vote TODAY
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** ⚡ BOARD VOTE TODAY — Trustees voting on $181M budget shortfall for 2026-27. Written public comments accepted through 5 PM at www.austinisd.org. 558 positions eliminated including teachers, librarians, counselors, campus police, and part-time assistant principals. Key strategies: $60M from selling/monetizing four AISD properties, $31M from larger class sizes and cutting librarians, $17M from central office cuts, $31M through attrition. 10 campus closures already approved in November save ~$21M. Budget must pass by end of June. Travis County offices CLOSED today and tomorrow for Juneteenth — 37th Annual celebration at 800 Lavaca 11 AM-2 PM. CDBG public comment open through July 20.")
    print("  Updated atx-aisd-budget-crisis")

# Pct 4: Juneteenth; CDBG continues
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Travis County offices CLOSED today and tomorrow (June 18-19) for Juneteenth. 37th Annual Juneteenth celebration TODAY 11 AM-2 PM at 800 Lavaca. CDBG public comment period continues through July 20; public hearing July 14 at 9 AM. Draft PY26 Action Plan and ConPlan/PY24-25 amendments all open for comment. AISD board voting TODAY on $181M budget shortfall. Bond survey closes June 23 (5 DAYS).")
    print("  Updated tc-pct4-runoff")

# Bond: survey 5 DAYS remaining
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Bond community input survey closes June 23 — 5 DAYS remaining. 53,000+ individual responses so far. Top priorities: transportation (19.8%), housing & homelessness (18.5%), parks (16.3%); ~70% support a property tax increase; 81% say sustainability/climate should factor into project selection. AISD board voting TODAY on $181M shortfall. Council on recess until July 23 — final bond vote that day. Travis County offices CLOSED for Juneteenth.")
    print("  Updated atx-2026-bond")

# D1 Election: filing countdown
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Filing period opens July 19 (31 DAYS). First day to file in person July 20. Filing deadline August 17. 5 open council seats (D1, D3, D5, D8, D9) — D1 open as Harper-Madison term-limited; D8 Ellis seeking petition for third term vs. challenger Selena Xie. 20+ candidates have appointed campaign treasurers. Bond survey closes June 23 (5 DAYS). AISD board vote TODAY — school closures and $181M deficit are defining campaign issues. Semi-annual campaign finance filings due in July. Election Day November 3.")
    print("  Updated atx-d1-election")

# Homelessness: navigation center RFP
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** South Austin Navigation Center at 2401 S. I-35 Frontage Rd — RFP open for operator; up to $250K in funding; 13-member Center Advisory Board formed from 69 applicants. HSO expects the first City-owned navigation center to open late summer/early fall 2026. AT-Home Initiative ($6.7M, 5-year) — proposals due June 2; city in review/selection phase; contracts for up to 3 providers, 12-month term beginning September 2026. AISD board voting TODAY on $181M shortfall — school closures compound homelessness risk. Travis County offices CLOSED for Juneteenth.")
    print("  Updated atx-hso-plan-adopted")

# Project Connect: legal unchanged
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Legal status unchanged — trial halted per TX Supreme Court May 22 ruling; Judge Shepperd must rule on AG Paxton's jurisdictional plea. ATP achieved federal Record of Decision — key NEPA milestone allowing property acquisition, utility relocation, and contract awards. Three major contracts expected in 2026: light rail infrastructure design-build, operations & maintenance facility, and vehicle procurement. Project Connect property tax rate expected to generate ~$185M in 2026. Council on recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# Childcare: Juneteenth closure
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Travis County offices CLOSED today and tomorrow for Juneteenth. 37th Annual Juneteenth celebration TODAY at 800 Lavaca 11 AM-2 PM. $17.65M childcare expansion on track; nearly 300 kids have received scholarships, target 1,000 by October. CDBG public comment continues through July 20 — draft PY26 Action Plan and ConPlan amendments open for comment. Public hearing July 14 at 9 AM. AISD board voting TODAY on $181M shortfall — school closures directly impact childcare access and family stability.")
    print("  Updated tc-childcare-funding")

# APD Staffing
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** 157th cadet class mid-training — started January 26, graduation September 18. APD remains 300+ officers short of authorized strength (~1,819 of ~2,120 authorized). Annual budget $527.9M. AISD board voting TODAY on $181M shortfall — includes campus police cuts. Council on recess until July 23. Travis County offices CLOSED for Juneteenth.")
    print("  Updated atx-apd-staffing-audit")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-18T12:00:00Z"

# Garden Grove: GKN $3M donation, extraction still delayed
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 18 update:** GKN Aerospace donated $3M to United Way OC Community Resilience Fund + pledged additional $1M for community initiatives. Board Chairman Doug Chaffee called the donation a \"drop in the bucket.\" Chemical extraction STILL delayed — ~28 days post-incident; specialized sealed trucks needed for MMA transport have not yet arrived. No revised start date announced. Three-agency criminal investigation continues (FBI/EPA, OC DA, Cal/OSHA). FBI search warrant June 10 authorized seizure of chemical samples, training logs, safety complaints, and communications. 44+ lawsuits filed including class-action. 50,000+ residents were evacuated. Next regular Garden Grove council meeting June 23. OC Registrar count TODAY ~5 PM.")
    print("  Updated Garden Grove chemical crisis")

# D4: both advance
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Shaw (R) at ~33.3% vs Traut (D) at ~31.2%. ~9,500 ballots remaining countywide — pool nearly exhausted. Both advance to November general. OC Registrar count TODAY ~5 PM. Additional updates June 24, 26. Final certification July 10. ⚡ Huntington Beach housing element APPROVED 6-1 on June 16 — Garden Grove council meeting June 23.")
    print("  Updated oc-bos-district-4-open-seat")

# D5: registrar count TODAY
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Foley (D) 47.0% vs Dixon (R) 46.8% — margin 327 votes as of last count. OC Registrar releasing updated count TODAY (~5 PM). ~9,500 ballots remaining countywide; all outstanding ballots awaiting voter response and signature verification. Neither candidate will reach 50% — both advance to November runoff. Final certification July 10. Additional counts June 24, 26. Becerra (D) vs Hilton (R) advance to November governor's race — first poll shows Becerra +21 points, which could boost Democratic turnout for Foley.")
    print("  Updated oc-bos-district-5-defense")

# Governor: primary confirmed, general shaping up
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Primary confirmed: Becerra (D) 28% vs Hilton (R) 25% advance to November general election (with 88% counted). First general election poll: Becerra 52% vs Hilton 31% — commanding 21-point lead among likely voters. Steyer (D) finished third at ~23% and is eliminated. Registered Democrats outnumber Republicans nearly 2-to-1 statewide. OC county certification deadline July 3. OC Registrar count TODAY ~5 PM. ⚡ Huntington Beach housing element APPROVED 6-1 — Becerra win would maintain aggressive state housing enforcement.")
    print("  Updated ca-governor-2026")

# HB: HOUSING ELEMENT APPROVED
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** ⚡ HUNTINGTON BEACH HOUSING ELEMENT APPROVED — City Council voted 6-1 on Tuesday June 16 to adopt the housing element. Councilmember Chad Williams was the sole dissent, offering multiple substitute motions that all failed. City now zones for 13,000+ new residences. Mayor Casey McKeon cited mounting fines (~$100K+ accrued) but said the fight for local control may continue at the ballot box. Several councilmembers said they disapproved but couldn't justify six-figure monthly fines. Judge scheduled to rule next month on whether to increase fines from $50K to $150K/month — adoption may reduce or eliminate future penalties. HB was the ONLY noncompliant city in all of Orange County, 4.5+ years behind schedule. Becerra (D) 52% vs Hilton (R) 31% in first general poll — Becerra would maintain aggressive enforcement.")
    print("  Updated oc-newsom-housing-warning (HB)")

# OC Streetcar: 95% complete
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Construction now 95% complete on the $649M project (up from 92%). Street testing and systems integration underway — testing phase expected 6-12 months. Revenue service date pushed to early 2027 (OCTA hoping for August launch but extended timeline to March 2027 in May). Service will run 6 AM-11 PM daily with extended weekend hours; $2 one-way/$5 day pass; expected 5,000 daily riders across 10 stops connecting Garden Grove and Santa Ana. OC Registrar count TODAY ~5 PM.")
    print("  Updated oc-streetcar-launch")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-18T12:00:00Z"

# Primary: EARLY VOTING DAY 6
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** ⚡ EARLY VOTING DAY 6 — polls 8 AM - 4 PM (Wednesday). Through Day 5: 77,000+ total voters citywide (+14,756 from Day 4); Brooklyn: 21,675 check-ins (+4,913 from Day 4). Manhattan leads at 32,738, Queens 14,530, Bronx 7,262, Staten Island 1,625. Turnout down 50%+ compared to last year. Early voting continues through June 21. Primary Election Day June 23 (5 DAYS). CD-7 (Velázquez seat): prediction markets show Valdez at 79% (down from 83%), Reynoso at 21%. Emerson poll: Valdez 23%, Reynoso 21%, Won 13%, 43% undecided. Strong age divide persists: under-40 voters favor Valdez 33-15%, over-50 break for Reynoso 27-13%.")
    print("  Updated nyc-june-primary-2026")

# Housing: early voting context
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** ⚡ EARLY VOTING DAY 6 — polls 8 AM - 4 PM. 77,000+ voted citywide through Day 5; Brooklyn: 21,675 check-ins. Primary June 23 (5 DAYS). Brooklyn council seats on the ballot will shape housing policy. City of Yes ADU Program: 3,100+ homeowner applications received. Q1 2026 housing permits nearly doubled vs 2025 — 28,773 units filed.")
    print("  Updated nyc-atlantic-ave-rezoning")

# COPA: early voting
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** COPA bill language still being finalized — no hearing date yet. 26 sponsors (veto-proof). ⚡ EARLY VOTING DAY 6 — 77,000+ voted citywide through Day 5; Brooklyn: 21,675 check-ins. Turnout down 50%+ vs last year. Brooklyn council seats on the ballot determine whether COPA has the votes. Primary June 23 (5 DAYS).")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-18T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** ~59 days remaining in the 90-day ShotSpotter removal window (deadline mid-August 2026). Council voted 5-2-2 on May 19 to end the program. Device removal/disabling underway per City Manager Huang's direction. Cambridge Police Patrol Officers Association (~200 officers) continues public opposition, calling the decision a threat to emergency response times. Critics cite ICE access concerns through SoundThinking's CrimeTracer database. No council revisitation expected.")
    print("  Updated cam-shotspotter-banned")

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** CRA $9.375M loan to North Cambridge Partners finalized for 2400 Mass Ave — replaced Leader Bank mortgage at reduced 4.5% rate over two years. CRA total investment ~$14.375M ($5M equity + $9.375M loan). Project plans 56 homes + ground-floor retail with mixed-income component including affordable homeownership. 13-member Social Housing Task Force appointed by council — evaluating financing, governance, and expansion of permanently affordable, publicly owned, mixed-income developments. Task force listening sessions this summer; CDD consultant hiring underway. Barrett v. Cambridge inclusionary zoning lawsuit in discovery — AG Campbell intervened April; fact discovery deadline November 13.")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-18T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Community Housing funding review held yesterday (June 17) at 2 PM on Zoom — Community Preservation Act funding allocations discussed. Article 16 (26 Pleasant Street — 103 apartments including 15 affordable) remains POSTPONED to fall Special Town Meeting (typically November). CHC Overlay District approved 217-20. Updated ADU rules and restored inclusionary payments in effect. Annual Town Meeting concluded June 4.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Brookline remains compliant. 165 of 177 communities statewide have achieved compliance. No further actions until fall Special Town Meeting. Community Housing funding review held yesterday (June 17).")
    print("  Updated brk-mbta-communities-compliance")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-18T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** SE and SW Area Plans council adoption vote June 23 (5 DAYS). Both plans promote mixed-use development, higher density along major corridors, and increased transit connectivity. Transportation Commission reviewed June 3; Plan Commission reviewed June 15. Public comment opportunity at council meeting. BRT Route B: $118.1M federal funding remains in FTA pipeline — FTA confirms \"nothing has changed\"; design work continuing through 2026, construction 2027, launch 2028.")
    print("  Updated mad-new-housing-developments")

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Route A continues 15-minute service. Route B: $118.1M Small Starts grant remains in FTA pipeline — FTA confirms direction unchanged. ~78% federally funded, remainder from local communities. Route B runs from Madison's Northside through downtown to South Madison/Fitchburg, serving 53,000 people and 40,000 jobs. Design work continuing through 2026, construction 2027, launch 2028. SE/SW Area Plans: council vote June 23 (5 DAYS).")
    print("  Updated mad-east-west-brt-construction")

idx, issue = find_issue(madison["issues"], "mad-southeast-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Council adoption vote June 23 (5 DAYS). Plan Commission reviewed June 15; Transportation Commission reviewed June 3. The plan focuses on mixed-use and higher density along Milwaukee Street, Cottage Grove Road, Atwood Avenue, Monona Drive, and Stoughton Road. Public comment opportunity at council meeting.")
    print("  Updated mad-southeast-area-plan")

idx, issue = find_issue(madison["issues"], "mad-southwest-area-plan")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 18 update:** Council adoption vote June 23 (5 DAYS). Plan Commission reviewed June 15; Transportation Commission reviewed June 3. The plan includes mixed-use developments along Whitney Way, Raymond Road, Schroeder Road, and McKee Road. Public comment opportunity at council meeting.")
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
        "\n\n**June 18 update:** D5: Foley (D) 47.0% vs Dixon (R) 46.8% — margin 327 votes. OC Registrar count TODAY ~5 PM; ~9,500 ballots remaining. Both advance to November. D4: Shaw (R) ~33% vs Traut (D) ~31% — both advance. ⚡ Huntington Beach housing element APPROVED 6-1 on June 16 — city finally zones for 13,000+ residences after years of defiance. Certification deadline July 10. Garden Grove council meeting June 23."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 18 update:** CA Governor primary confirmed: Becerra (D) 28% vs Hilton (R) 25% advance to November. First general poll: Becerra +21 points. ⚡ Huntington Beach housing element APPROVED 6-1 on June 16 — Councilmember Chad Williams sole dissent. City zones for 13,000+ residences. Judge to rule next month on increasing fines from $50K to $150K/month; adoption may reduce future penalties. HB was the ONLY noncompliant city in OC. OC Registrar count TODAY ~5 PM."
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
        "\n\n**June 18 update:** ⚡ MAJOR VICTORY — Huntington Beach City Council voted 6-1 on June 16 to adopt the housing element after years of legal resistance. Chad Williams sole dissent. City now zones for 13,000+ new residences — was the ONLY noncompliant city in all of Orange County, 4.5+ years behind schedule. Mayor McKeon cited mounting fines (~$100K+ accrued) but signaled the fight may continue at the ballot box. Judge to rule next month on increasing fines from $50K to $150K/month — adoption may reduce or eliminate future penalties. Several councilmembers described the vote as being \"beaten into submission.\" Becerra (D) +21 over Hilton (R) in first general poll — Becerra win maintains aggressive state enforcement. D5: Foley (D) 47.0% vs Dixon (R) 46.8% — registrar count TODAY."
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
        "\n\n**June 18 update:** GKN donated $3M to United Way OC Community Resilience Fund + pledged $1M for community initiatives — Board Chairman Chaffee called it a \"drop in the bucket.\" Chemical extraction still delayed ~28 days post-incident; specialized sealed trucks not yet arrived. FBI search warrant June 10 authorized seizure of chemical samples, training logs, safety complaints. 44+ lawsuits filed. OC Streetcar now 95% complete — testing underway, revenue service early 2027. D5: Foley (D) 47.0% vs Dixon (R) 46.8% — registrar count TODAY ~5 PM. ⚡ HB housing element APPROVED 6-1."
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
        "\n\n**June 18 update:** Filing period opens July 19 (31 DAYS). 5 open seats: D1 (Harper-Madison term-limited), D3, D5, D8 (Ellis seeking third-term petition vs. Xie), D9. 20+ candidates have appointed treasurers. Bond survey closes June 23 (5 DAYS). ⚡ AISD board voting TODAY on $181M shortfall — 558 positions, 10 school closures. CDBG public comment continues through July 20. Travis County offices CLOSED for Juneteenth. Semi-annual campaign finance filings due in July. Council on recess until July 23."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 18 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. ATP achieved federal Record of Decision — enables property acquisition, utility relocation, and contract awards. Property tax rate generating ~$185M in 2026 for early design and utility work. Three major contracts expected in 2026. Council on recess until July 23."
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
        "\n\n**June 18 update:** South Austin Navigation Center RFP open — 13-member Advisory Board formed from 69 applicants. HSO expects opening late summer/early fall 2026. AT-Home Initiative ($6.7M, 5-year) — proposals due June 2, city in review; contracts for up to 3 providers, September 2026 start. ⚡ AISD board voting TODAY on $181M shortfall — school closures compound homelessness risk. Bond final vote July 23 — shelter infrastructure NOT in $390M direction. Travis County offices CLOSED for Juneteenth."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if not campaign:
    campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 18 update:** 157th cadet class mid-training (started Jan 26) — graduation September 18. APD remains 300+ officers short (~1,819 of ~2,120 authorized); annual budget $527.9M. AISD board voting TODAY on $181M shortfall — includes campus police cuts. Council on recess until July 23. Travis County offices CLOSED for Juneteenth."
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
        "\n\n**June 18 update:** Travis County offices CLOSED today and tomorrow for Juneteenth — 37th Annual celebration at 800 Lavaca 11 AM-2 PM. $17.65M childcare expansion on track; nearly 300 kids have received scholarships, target 1,000 by October. CDBG public comment continues through July 20 — draft PY26 Action Plan and ConPlan/PY24-25 amendments all open for comment. Public hearing July 14 at 9 AM. ⚡ AISD board voting TODAY on $181M shortfall — school closures directly impact childcare access and family stability."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-18T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-18T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-18T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-18T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-18T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
