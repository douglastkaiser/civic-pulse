#!/usr/bin/env python3
"""
July 7, 2026 updates for all issue and organization data files.
Key developments since July 5-6:
  - Austin: Monday — offices reopen after extended July 4 weekend
  - Austin: City Manager FY2027 budget due July 16 (9 DAYS)
  - Austin: Travis County TIRZ vote July 14 (7 DAYS); commissioners questioning SpaceX connection
  - Austin: DBC still zero applications after 7+ weeks; no DBC submissions confirmed by Austin Planning
  - Austin: D1 filing opens July 20 (13 DAYS); semi-annual campaign finance filings due mid-July
  - Austin: Convention center diaphragm wall complete, first footings poured, excavation >50 ft deep
  - Austin: Triple-digit heat continues; ERCOT 0.21% July grid emergency probability
  - OC: State certification July 10 (3 DAYS)
  - OC: AG HB penalties Day 7 at escalated rate ($150K/month); hearing July 17 (10 DAYS)
  - OC: Streetcar 95% complete; overnight powered testing began June 25-26
  - OC: Supportive Housing NOFA confirmed at $20.9M + up to 100 PBVs
  - Brooklyn: NYC offices reopen today; $125.8B FY2027 budget in effect
  - Brooklyn: New $300M rental assistance program (Intro 966); Comptroller flags $2.8B one-time measures
  - Brooklyn: City of Yes housing production up 23% in first 10 months; ADU intake closed June 12
  - Brooklyn: Monitor Point approved — 1,324 units, 50% deeply affordable
  - Madison: Common Council meeting TONIGHT (July 7) at 6:30 PM
  - Madison: $11M shortfall — alder analysis shows ~$7.2M problem after reserves; depts proposing 2% cuts
  - Madison: Budget requests due July 17 (10 DAYS)
  - Cambridge: Doug Brown petition confirmed active — cuts AHO from 9 to 6 stories
  - Cambridge: 680+ affordable units across 10 AHO developments in progress
  - Cambridge: Cambridge Public Works member killed July 4; community meeting July 8
  - Brookline: City Realty acquired Chestnut Hill site for $41M; 1.2M SF mixed-use proposed
  - Brookline: Override passed 60-40% ($23.25M); Select Board turnover
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
austin["last_scraped"] = "2026-07-07T12:00:00Z"

# Dog's Head
idx, issue = find_issue(austin["issues"], "atx-dogs-head-annexation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen after extended holiday weekend. Travis County commissioners scrutinizing TIRZ deal — Commissioner Shea called it 'a whole lot of trust me'; Austin Current reporting questions whether Fortune 100 tenant ('Project Toaster') is SpaceX. Environmental Commission unanimously recommended delaying TIRZ vote to January 2027. Travis County TIRZ vote July 14 (7 DAYS). Council vote July 23 (16 DAYS) if not delayed. City Manager budget July 16 (9 DAYS).")
    print("  Updated atx-dogs-head-annexation")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. Travis County TIRZ vote July 14 (7 DAYS) — commissioners questioning deal terms and potential SpaceX connection. Environmental Commission's TIRZ delay recommendation could affect broader development timeline. Council vote July 23 (16 DAYS). D1 filing opens July 20 (13 DAYS). City Manager budget July 16 (9 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Gas peaker plant
idx, issue = find_issue(austin["issues"], "atx-gas-peaker-plant")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. Triple-digit heat continues across central Texas. ERCOT grid emergency probability 0.21% for July — peak demand could exceed 92.2 GW (10% above last year), driven by data centers and population growth. No conservation appeals or grid emergencies reported. Austin Energy over 70% carbon-free. City Manager budget July 16 (9 DAYS). Council returns July 23 (16 DAYS).")
    print("  Updated atx-gas-peaker-plant")

# HSO / homelessness
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. Sunrise selected as tentative SAHNC operator through competitive process — has rehoused 800 people in 2026, connected 1,880 to housing in 2025. Council approval vote July 23 (16 DAYS). SAHNC at 2401 S. I-35 — construction continues, opening June 2027. 13-member Advisory Board formed from 69 applicants. AT-Home Initiative ($6.7M, 5-year) contract awards expected September 2026 — 98% retention rate in permanent supportive housing. City Manager budget July 16 (9 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# AISD
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. $181M deficit stands: 558 positions affected, 10 school closures approved. Boundary realignment Phase 1 draft August 7 (31 DAYS) covers schools receiving students from closed campuses. Phase 2 postponed to 2028-29 — additional closures possible. Two draft scenarios ('Oak' and 'Elm') in community review; online comment card open through July 31. AISD lost 3,000+ students in 2025-26. Board vote on Phase 1 in September. City Manager budget July 16 (9 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen — campaign activity resumes. Harper-Madison term-limited; seat open for first time in 8 years. Filing opens July 20 (13 DAYS); deadline August 17. Seven candidates emerging: Amber Karessa Goodwin (assistant DA), Misael Daguan Ramos (2022 runner-up), Steven Brown, Alexandria Anderson, and others. Semi-annual campaign finance filings due mid-July — January reports showed ~$140K raised collectively across all council races. City Manager budget July 16 (9 DAYS). Election Day November 3. Council returns July 23 (16 DAYS).")
    print("  Updated atx-d1-election")

# Bond
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. ~$390M bond (parks, transportation, community facilities) — housing ($200M) and stormwater/flood mitigation excluded. Staff directed to explore alternative funding for excluded categories. Final vote July 23 (16 DAYS) to place on November ballot. Mayor Watson remains opposed. Bond survey received 53,000+ responses; transportation and housing tied as top priorities among respondents. City Manager budget July 16 (9 DAYS).")
    print("  Updated atx-2026-bond")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. DBC approaching 7+ weeks since approval with still zero applications — Austin Planning confirmed no DBC submissions. Pre-application meeting with Housing staff required before submitting. Stark contrast to DB90's immediate uptake in 2024. Downtown DDB400/DDB850 (towers up to 1,200 ft) also seeing no activity. Program offers 15-60 ft extra height across 5 tiers in multifamily/commercial zones. Council returns July 23 (16 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen — courts resume normal operations. Judge Shepperd still has not ruled on AG Paxton's jurisdictional plea since TX Supreme Court's May 22 mandate. Core question: whether ATP qualifies as a bond 'issuer' under the EDJA. If plea denied → automatic interlocutory appeal; if granted → ATP's bond validation suit dismissed. Either path means months of additional delay. Federal funding uncertain — Trump admin has not agreed to any new transit projects; Sen. Cornyn publicly opposes federal funding for Austin rail. ATP continues design, property acquisition ($230M for 18 parcels), and contract advancement. FTA environmental clearance secured January 2026. Council returns July 23 (16 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen — APD normal operations. ~1,819 officers, still ~700 short but gained net +3 officers last year — first positive year in recent memory. Chief Davis projects full staffing by end of 2027. 28% pay raise over 5 years improving retention. $3.7M recruitment budget (highest in 5 years). City auditor found no formal long-term recruitment plan. APD receives ~$540M (36.2% of general fund). Proposed FY2027: $544M ($26M increase). City Manager budget July 16 (9 DAYS). Council returns July 23 (16 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen — construction resumes normal pace. $1.6B 'Unconventional ATX' project advancing on schedule: demolition 100% complete, diaphragm wall finished, first footings poured, excavation exceeding 50 ft depth continuing through August. Travis County court ruled June 18 that $1.35B bond financing plan is lawful. Targeting world's first Net Zero Carbon Certified convention center — mass timber roof, low-carbon concrete/steel. Spring 2029 reopening. Council returns July 23 (16 DAYS).")
    print("  Updated atx-convention-center")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. Raising Travis County: $75M voter-approved initiative (Nov 2024, 59%) — fastest implementation nationally, first in Texas. Over $28M awarded total; $17.65M in contracts with ~180 providers and 13 community partners serving 5,200+ children. Eligibility up to 85% SMI ($92K for family of 4); families pay no more than 7% of income. Wait times dropped from 2 years to months; children 3 and under no longer waiting by end of summer. CDBG public hearing July 14 at 9 AM (7 DAYS). City Manager budget July 16 (9 DAYS). Council returns July 23 (16 DAYS).")
    print("  Updated tc-childcare-funding")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. DBC: zero applications in 7+ weeks — Austin Planning confirmed no submissions. Minimum lot size 1,800 sq ft citywide — implementation ongoing. Council returns July 23 (16 DAYS).")
    print("  Updated atx-development-rules-overhaul")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-07-07T12:00:00Z"

# Garden Grove / GKN
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**July 7 update:** Offices reopen. Crisis Day 47. Phase 1 complete — ~14,000 gallons MMA neutralized and removed from tanks #2 and #4 (June 29-July 2). No evacuations needed during Phase 1. Phase 2 timeline (remaining tank and facility remediation) still pending from DTSC/OC HCA — no schedule posted. Air monitoring continues with no exceedances. Three criminal investigations ongoing: FBI/EPA (search warrant executed June 10 under 42 U.S.C. 7412(r)), OC DA Spitzer (opened May 22, 'not getting satisfactory answers'), Cal/OSHA. 44+ lawsuits filed. Wikipedia article actively maintained. State certification July 10 (3 DAYS).")
    print("  Updated Garden Grove chemical crisis")

# D5
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. State certification July 10 (3 DAYS) — official results to be finalized. D5 primary final: Foley (D) 48.4% vs Dixon (R) 45.8% — November runoff confirmed. 3-2 Democratic BOS majority hinges on this race. OCEA labor crisis deepening — county has $204M above reserve target per forensic audit while proposing zero wage increases. AG HB penalties Day 7 at escalated rate ($150K/month). BOS cancelled through August — governance gap with interim CEO Roestenberg ($430K).")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. State certification July 10 (3 DAYS). Shaw (R) 33.27% vs Traut (D) 31.22% confirmed for November. GKN Phase 1 complete; Phase 2 pending — industrial safety remains defining D4 issue. OCEA forensic audit: county $204M above reserve target; $252M reserve increase since 2019. BOS cancelled through August.")
    print("  Updated oc-bos-district-4-open-seat")

# HB housing element
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen — courts resume. AG HB penalties Day 7 at escalated rate ($150K/month combined). HB has now lost 8 consecutive legal challenges. July 2 anti-SLAPP ruling struck cross-complaint; state entitled to recover attorney's fees. Governor Newsom: 'Hey, NIMBY Huntington Beach...you tired of losing yet?' Only 1,187 of 5,845 required very-low/low-income units permitted so far. Hearing July 17 for additional penalties (10 DAYS). 120-day zoning deadline ~October 14. State certification July 10 (3 DAYS).")
    print("  Updated oc-newsom-housing-warning (HB)")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. County certifications complete — Hilton (R) ~28% vs Becerra (D) ~26% confirmed for November. First general election poll: Becerra (D) 52% vs Hilton (R) 31% — significant Democratic advantage. State hasn't elected Republican governor in 20 years. CA's 2:1 Democratic registration advantage makes Hilton a significant underdog. Secretary of State certification July 10 (3 DAYS). General election November 3.")
    print("  Updated ca-governor-2026")

# OC FY2027 Budget
idx, issue = find_issue(oc["issues"], "oc-fy2027-budget")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. FY2026-27 recommended budget released. OCEA labor crisis deepening — no new sessions announced beyond July 1. County faces $75M structural deficit + $400M Airport Fire liability. OCEA forensic auditor (HMR) confirmed county has significant unrestricted funds for labor costs. Supervisors took 25% pay raises + $715K executive comp while proposing hiring freezes and zero wage increases. Teamsters Local 952 contract expired June 25. AG HB penalties Day 7. State certification July 10 (3 DAYS). BOS cancelled through August.")
    print("  Updated oc-fy2027-budget")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. Project 95% complete. Overnight powered testing began June 25-26 on the Raitt Street to Santa Ana RTC segment using newly energized overhead wire system. Testing phase estimated 6-12 months. Revenue service pushed to March 2027. Expected to carry 5,000 daily riders across 10 stops on 4.15-mile all-electric route between Santa Ana and Garden Grove. State certification July 10 (3 DAYS).")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**July 7 update:** Offices reopen. Grand Jury response deadline passed June 30 — Supervisor Foley issued a statement but no formal BOS responses confirmed publicly. Grand Jury report titled 'Is Orange County Moving in the Right Direction?' recommended earmarking discretionary funds for homelessness prevention. Common Good workforce reentry campus (4.6 acres in City of Orange) broke ground June 24 — vocational training, education, retail, and short-term housing for 52 participants. OCEA forensic audit: county $204M above reserve target. BOS cancelled through August. State certification July 10 (3 DAYS).")
    print("  Updated OC Homelessness Grand Jury")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. NOFA confirmed at $20.9M available (HOME, HOME-ARP, MHSA/BHSA, 15G Reserves, HSA funds) for acquisition, new construction, or rehabilitation of supportive housing. Up to 100 Project Based Vouchers also available. Small-scale housing eligible. NOFA remains open until closed, replaced, or all funds committed. State certification July 10 (3 DAYS). BOS cancelled through August.")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. Valencia (D) ~63% vs Shader (R) ~37% — heavy favorite for November given district's Democratic lean. State certification July 10 (3 DAYS). General election November 3.")
    print("  Updated oc-state-senate-sd34")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. Grand Jury response deadline passed — Supervisor Foley issued statement but no formal BOS response confirmed. Common Good workforce reentry campus (4.6 acres, City of Orange) broke ground June 24 — first publicly owned facility of its kind in SoCal; vocational training, education, short-term housing for 52 justice-involved participants. State certification July 10 (3 DAYS). BOS cancelled through August.")
    print("  Updated oc-homelessness-enforcement")

# Orange Housing Element
idx, issue = find_issue(oc["issues"], "oc-orange-housing-element")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. HB anti-SLAPP ruling (July 2) strengthens precedent for all noncompliant cities — court found cities can't sue state for enforcing housing law. HB has lost 8 consecutive legal challenges. AG HB penalties Day 7 at escalated rate. Four pending Builder's Remedy applications in City of Orange (696 units) remain in pipeline. State certification July 10 (3 DAYS).")
    print("  Updated oc-orange-housing-element")

# AD-68
idx, issue = find_issue(oc["issues"], "oc-ad68-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. State certification July 10 (3 DAYS). Valencia's move to SD-34 leaves seat open. General election November 3.")
    print("  Updated oc-ad68-open-seat")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-07-07T12:00:00Z"

idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** NYC offices reopen today after extended holiday weekend. $125.8B FY2027 budget now in effect — includes new $300M rental assistance program (Intro 966) targeting up to 30,000 New Yorkers, Fair Fares expansion, $350M added to reserves. Comptroller Levine flagged concerns about reliance on $2.8B in one-time measures. Atlantic Ave rezoning in post-approval implementation — developers already acquiring sites in the 21-block corridor (Vanderbilt to Nostrand Ave); projects 4,600 units (~40% affordable). Monitor Point approved: 1,324 units (50% deeply affordable) plus Bushwick Inlet Park completion. Atlantic Yards: $5B proposal for 5,600 apartments over Vanderbilt rail tracks — groundbreaking targeted 2028.")
    print("  Updated nyc-atlantic-ave-rezoning")

idx, issue = find_issue(brooklyn["issues"], "nyc-city-of-yes-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** NYC offices reopen today. Housing production rose 23% in the first 10 months after City of Yes passage. Plus One ADU Program intake closed June 12 after receiving thousands of responses — HPD now analyzing site eligibility. 'ADU for You' free resource center launched March 2026 with pre-approved plans and budgeting calculator. Mayor Mamdani's 'Block by Block' housing plan (May 2026) seeks to extend City of Yes frameworks to medium/high-density areas. Columbia Commons affordable housing lottery launched for 369 units at 498 Columbia Street in Red Hook.")
    print("  Updated nyc-city-of-yes-implementation")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-07-07T12:00:00Z"

idx, issue = find_issue(madison["issues"], "budget-rules-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Common Council meeting TONIGHT at 6:30 PM in Room 201 of City-County Building. City faces $11M shortfall for 2027 — District 19 alder analysis frames as ~$7.2M problem after ~$4M covered from reserves. Binding constraint is state expenditure restraint program (ERIP) cap. Mayor directed all departments to propose 2% reductions (~$9M). No new positions or supplemental programs allowed. Initial budget requests due July 17 (10 DAYS); Executive Budget in October. Christine Knapp (Cedar Rapids Water Division, 9 years) confirmed as Madison Water Utility GM — starts August 31, pending Council contract approval. Seven major development proposals up for summer 2026 approval.")
    print("  Updated budget-rules-2026")

save_json(ISSUES_DIR / "madison-wi.json", madison)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-07-07T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-zoning-reform-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. Doug Brown citizen petition (filed June 3, 13 signatures from West Cambridge/Neighborhood Nine) remains de facto law until Council votes — earliest August 3. Petition cuts maximum AHO heights from nine to six stories, blocks inclusionary projects from building to six stories unless adjacent buildings are 3+ stories, and adds setback and parking requirements. City spokesperson confirmed several developments will likely be unable to move forward as planned. Over 680 affordable units across 10 AHO developments currently in progress or review. Councilors Zusy and Flaherty have separately proposed amendments to open space, setback, and parking rules. Council in summer recess. A Cambridge Public Works Department member was shot and killed off-duty on July 4 near Broadway and Norfolk Street — community meeting scheduled July 8 at Fletcher Maynard Academy.")
    print("  Updated cam-zoning-reform-implementation")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-07-07T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. FY2027 total budget at $481M after voters approved $23.25M property tax override on May 5 (60-40%, highest local election turnout ever recorded). Override phased over 3 years: $17.94M to schools, $5.31M to town departments — without it, ~240 FTE positions would have been cut. Select Board turnover: incumbent VanScoyoc defeated; Amanda Zimmerman and Anthony Buono won two open seats. Town Meeting also adopted 10-year Climate Action and Resiliency Plan (May 19) with 45 strategies and 178 actions targeting net-zero emissions, plus civil immigration enforcement prohibition and Pleasant Street Multi-Family Overlay District.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 7 update:** Offices reopen. Chestnut Hill overlay approved 217-20 on May 28 — covers ~27.8 acres along Route 9, allows buildings up to 12-14 stories in highest-intensity subdistrict. City Realty acquired 5.34-acre Chestnut Hill Office Park site (1280-1330 Boylston St) for $41M — proposing 1.2M SF mixed-use project: hotel, 245 housing units, medical office, retail. Projected $9M/year in property taxes. Special permit review expected 9-12 months once formal application filed. Town Meeting also authorized Memorandum of Agreement and tax certainty agreement with City Realty. MBTA Communities bylaw passed November 2023 (207-33) with capacity for ~6,990 units (~800 expected to be built).")
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
        "\n\n**July 7 update:** Offices reopen. State certification July 10 (3 DAYS) — official primary results to be finalized. D5: Foley (D) 48.4% vs Dixon (R) 45.8%. D4: Shaw (R) 33.27% vs Traut (D) 31.22%. 3-2 Democratic BOS majority hinges on BOTH seats. OCEA labor crisis deepening — no new sessions announced beyond July 1; forensic audit shows $204M above reserve target. AG HB penalties Day 7 at $150K/month. Governor: first general poll Becerra (D) 52% vs Hilton (R) 31% — strong Democratic headwinds for November. GKN Phase 1 complete; three criminal investigations ongoing. BOS cancelled through August."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 7 update:** Offices reopen. State certification July 10 (3 DAYS). Governor: Hilton (R) ~28% vs Becerra (D) ~26% — first general poll shows Becerra +21 (52-31), significant Democratic advantage. SD-34: Valencia (D) dominant at ~63%. AD-68: open seat, certification pending. General election November 3."
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
        "\n\n**July 7 update:** Offices reopen. AG HB penalties Day 7 at escalated rate ($150K/month combined). HB has lost 8 consecutive legal challenges — Governor Newsom: 'Hey, NIMBY Huntington Beach...you tired of losing yet?' Anti-SLAPP ruling struck cross-complaint; state entitled to fee recovery. Only 1,187 of 5,845 required very-low/low-income units permitted. Hearing July 17 for additional penalties (10 DAYS). 120-day zoning deadline ~October 14. Supportive Housing NOFA confirmed at $20.9M + up to 100 PBVs. State certification July 10 (3 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 7 update:** Offices reopen. ⚡ Irvine Company proposing 3,100-unit Oak Creek Golf Course conversion (235 acres near Spectrum) — could be approved summer 2026, advancing Irvine's 23,610-unit RHNA requirement. OCEA forensic audit: county $204M above reserve target despite deficit narrative. OC Streetcar 95% complete — powered testing underway, March 2027 launch. State certification July 10 (3 DAYS). BOS cancelled through August."
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
        "\n\n**July 7 update:** Offices reopen. GKN Phase 1 complete — childcare facilities in Garden Grove/Stanton corridor have resumed normal operations after 50,000-person evacuation. Three criminal investigations ongoing (FBI/EPA, DA Spitzer, Cal/OSHA). County faces $75M structural deficit + $400M Airport Fire liability — threatens family services. OCEA labor crisis: no new sessions beyond July 1; supervisors took 25% raises while proposing zero for workers. Supportive Housing NOFA confirmed at $20.9M. State certification July 10 (3 DAYS). BOS cancelled through August."
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
        "\n\n**July 7 update:** Offices reopen — campaign activity resumes. D1: 7 candidates emerging including Amber Karessa Goodwin (assistant DA), Misael Daguan Ramos (2022 runner-up), Steven Brown, and Alexandria Anderson. Filing opens July 20 (13 DAYS); deadline August 17. Semi-annual campaign finance filings due mid-July — January reports showed ~$140K raised collectively. Bond survey received 53,000+ responses. City Manager budget July 16 (9 DAYS). Election Day November 3. Council returns July 23 (16 DAYS)."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 7 update:** Offices reopen — courts resume. Judge Shepperd still has not ruled on AG Paxton's jurisdictional plea. Core question: whether ATP qualifies as bond 'issuer' under EDJA. Either path (plea denied → interlocutory appeal; plea granted → suit dismissed) means months of delay. Federal funding uncertain — Trump admin has not agreed to any new transit projects; Sen. Cornyn publicly opposes. ATP continues design, property acquisition ($230M for 18 parcels). Convention center: diaphragm wall complete, first footings poured, June 18 court ruling affirmed $1.35B bond plan — positive precedent. Council returns July 23 (16 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 7 update:** Offices reopen. Travis County commissioners scrutinizing TIRZ — Shea called it 'a whole lot of trust me'; Austin Current reports questions about whether 'Project Toaster' (Fortune 100 tenant) is SpaceX. Environmental Commission unanimously recommended delaying TIRZ vote to Jan 2027. Travis County TIRZ vote July 14 (7 DAYS). Council vote July 23 (16 DAYS) if not delayed."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 7 update:** Offices reopen. DBC zero applications after 7+ weeks — Austin Planning confirmed no submissions. Pre-application meeting with Housing staff required. Downtown DDB400/DDB850 also no activity. Stark contrast to DB90's immediate uptake in 2024. Council returns July 23 (16 DAYS)."
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
        "\n\n**July 7 update:** Offices reopen. Sunrise selected as tentative SAHNC operator through competitive process — 800 rehoused in 2026, 1,880 connected to housing in 2025. Council approval vote July 23 (16 DAYS). SAHNC at 2401 S. I-35 — construction continues, opening June 2027. 13-member Advisory Board formed from 69 applicants. AT-Home Initiative ($6.7M, 5-year) contract awards expected September — 98% retention rate. Cooling centers remain open for unhoused during triple-digit heat. City Manager budget July 16 (9 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 7 update:** Offices reopen — APD normal operations. ~1,819 officers, still ~700 short. Net +3 officers last year — first positive year in recent memory. Chief Davis: full staffing by end of 2027. 28% pay raise over 5 years. Proposed FY2027 APD budget: $544M ($26M increase, 36.2% of general fund). City auditor: no formal long-term recruitment plan. City Manager budget July 16 (9 DAYS). Council returns July 23 (16 DAYS)."
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
        "\n\n**July 7 update:** Offices reopen. Raising Travis County: over $28M awarded total — $17.34M to Workforce Solutions for 1,000 annual scholarships, $4.16M for quality improvements at 150 providers. 13 community partners serving 5,200+ children. Children 3 and under no longer waiting for scholarships by end of summer. Families pay no more than 7% of income (down from 15%+). CDBG public hearing July 14 at 9 AM (7 DAYS) — comment period through July 20. AISD boundary realignment Phase 1 draft August 7 (31 DAYS); Phase 2 postponed to 2028-29. City Manager budget July 16 (9 DAYS). Council returns July 23 (16 DAYS) — bond final vote ($390M, housing excluded)."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**July 7 update:** Offices reopen. City Manager budget July 16 (9 DAYS) — FY2027 budget context for workforce benefit advocacy. Proposed FY2027 APD budget $544M ($26M increase); city-wide $6.3B with $33M deficit addressed through cuts and reserve draws. D1 filing opens July 20 (13 DAYS). Council returns July 23 (16 DAYS)."
    )
    print("  Updated parental-leave campaign")

campaign = find_campaign(atx_abundance, campaign_id="employer-index")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 7 update:** Offices reopen. Campaign in planning phase. City Manager budget July 16 (9 DAYS) — FY2027 budget provides employer benefit policy context. D1 filing opens July 20 (13 DAYS). Council returns July 23 (16 DAYS)."
    )
    print("  Updated employer-index campaign")

campaign = find_campaign(atx_abundance, campaign_id="family-housing-campaign")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 7 update:** Offices reopen. DBC zero applications after 7+ weeks — Austin Planning confirmed no submissions. Developer uptake remains the key indicator. Dog's Head TIRZ: Travis County commissioners scrutinizing deal; county TIRZ vote July 14 (7 DAYS). Environmental Commission unanimously recommended delay to Jan 2027. AISD boundary realignment Phase 1 draft August 7 (31 DAYS). Bond: housing ($200M) excluded from ~$390M direction; final vote July 23 (16 DAYS). Council returns July 23 (16 DAYS)."
    )
    print("  Updated family-housing-campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-07-07T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868", "brooklyn-ny", "madison-wi", "cambridge-ma", "brookline-ma"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-07-07T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-07-07T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-07-07T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-07-07T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
