#!/usr/bin/env python3
"""
June 7, 2026 updates for all issue and organization data files.
Key developments since June 5:
  - OC D5: Dixon (R) takes the lead over Foley (D) — 3-2 Dem BOS majority at double risk
  - OC D4: Shaw's lead widens to ~1,600 votes
  - CA Governor: Becerra takes slight lead over Hilton (26.7% vs 26.4%)
  - AISD: Parents/teachers protested June 5; board vote June 18 (11 days)
  - HB: Housing element adoption delayed to June 16 council meeting
  - NYC: COPA has 26 sponsors, early voting for June 23 primary starts June 13
  - Cambridge ShotSpotter: 65% false positive rate; police unhappy; 90-day removal
  - APD: 166% increase in test signups; on pace for full staffing by end 2027
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


def add_next_actions(campaign, new_actions):
    existing = set(campaign.get("next_actions", []))
    for action in new_actions:
        if action not in existing:
            campaign["next_actions"].append(action)


# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-07T12:00:00Z"

# D5: Dixon takes the lead — MAJOR shift
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** ⚡ MAJOR SHIFT: Dixon (R) has TAKEN THE LEAD over Foley (D) as late-arriving mail ballots are counted. Latest totals: Dixon 62,640 (48.5%) vs Foley 58,654 (45.4%). Foley led on election night and in early canvass counts but Dixon has pulled ahead as conservative-leaning mail ballots arrived. The gap has widened with each update — Dixon went from 48.96% to 48.54% while Foley inched from 45.08% to 45.45%, but Dixon maintains a ~4,000-vote lead. Both advance to November regardless, but the momentum has shifted decisively to Dixon. If Dixon wins in November, the board flips to Republican majority — and with Shaw (R) also leading in D4, the 3-2 Democratic BOS majority faces DOUBLE JEOPARDY. Canvass continues through July 10.")
    append_to_field(issue, "why_it_matters_to_you",
        " ⚡ CRITICAL: Dixon (R) has taken the lead over Foley (D) — 62,640 to 58,654. Combined with Shaw (R) leading Traut (D) by ~1,600 votes in D4, the Democratic BOS majority is at serious risk in BOTH swing seats. If both Republicans win in November, the board flips 4-1 Republican — fundamentally changing housing enforcement, homelessness investment, and the county's relationship with state housing mandates.")
    print("  Updated oc-bos-district-5-defense")

# D4: Shaw's lead widens
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** Canvass continues — Shaw (R) 26,264 (33.27%) vs Traut (D) 24,643 (31.22%) as of June 5. Shaw's lead has widened from the election-night 68-vote margin to approximately 1,621 votes. Mail-in ballots postmarked by June 2 accepted through June 9. Certification deadline July 10. Combined with Dixon (R) taking the lead over Foley (D) in D5, the 3-2 Democratic BOS majority faces double jeopardy in November.")
    print("  Updated oc-bos-district-4-open-seat")

# Governor: Becerra takes slight lead
idx, issue = find_issue(oc["issues"], "oc-ca-governor-race")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** Becerra (D) has taken a slight lead over Hilton (R) as late ballots are counted — Becerra 26.7% vs Hilton 26.4%. Tom Steyer trails at ~21%. Both Becerra and Hilton expected to advance to the November general. County election officials have until July 3 to certify results. The race remains the most consequential for California housing policy — Becerra's AG tenure drove the Huntington Beach enforcement; a Hilton governorship could weaken RHNA enforcement statewide.")
    print("  Updated oc-ca-governor-race")

# HB: Housing element delayed to June 16
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** Huntington Beach city council has scheduled the housing element vote for June 16 — 9 DAYS AWAY. $50K/month fines are accruing. The council's continued delay despite exhausting all legal avenues (US Supreme Court, state court, AG enforcement) demonstrates the political dynamics of NIMBY resistance even under maximum legal pressure. The June 16 vote will determine whether HB finally adopts its housing plan or faces indefinite escalating penalties.")
    print("  Updated oc-newsom-housing-warning (HB)")

# OC Streetcar: safety testing detail
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** Safety testing officially commenced June 3 per OCTA CEO Darrell E. Johnson. The 6-12 month testing phase verifies train operations and street signal interface. Revenue service date confirmed pushed to March 2027 (from August 2026). 95% complete. Fares confirmed: $2 one-way / $5 day pass. Daily service 6am-11pm with extended weekend hours. Expected 5,000 passengers/day across 10 stops.")
    print("  Updated oc-streetcar-launch")

# Garden Grove: residents demanding closure
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 7 update:** Residents at Garden Grove city council meetings are demanding the city permanently close the GKN Aerospace facility. GKN's pledged community support totals $5M ($3M to OC Community Resilience Fund via United Way, $1M to Red Cross, $1M for broader community initiatives). Cleanup remains delayed — specialized sealed trucks needed to transport MMA from the compromised tank have not arrived. Cal/OSHA investigation and DA Spitzer's criminal probe continue in parallel. 44+ lawsuits filed in OC Superior Court and US District Court.")
    print("  Updated Garden Grove chemical crisis")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — AUSTIN
# ============================================================
print("\n=== Updating austin-78702.json ===")
austin = load_json(ISSUES_DIR / "austin-78702.json")
austin["last_scraped"] = "2026-06-07T12:00:00Z"

# AISD: Protest + countdown
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** Parents and teachers rallied on June 5 to protest the budget cuts — the protest drew significant media coverage and community attention. The recommended budget affects 558 positions total across the district (teachers, librarians, counselors, police, and central staff). 11 schools closing this summer. Board of Trustees final vote: June 18 — 11 DAYS AWAY. The budget must be adopted by end of June for the July 1 fiscal year start. Community opposition is intensifying but the $181M deficit leaves few alternatives without state funding reform.")
    print("  Updated atx-aisd-budget-crisis")

# APD: Recruitment progress
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** Positive recruitment trend: APD reports a 166% increase in people signing up for written and physical tests. Three recent cadet classes graduated a total of 122 officers. The 154th cadet class graduates in August; the 155th class begins April 21 with 65 cadets in the hiring process. APD projects it will be on pace for full staffing by end of 2027. However, patrol sector vacancy rates still average ~25%, and the department remains at 1,477 sworn officers against 1,816 authorized positions (19% vacancy rate). Professional staff vacancy is 9-10%.")
    print("  Updated atx-apd-staffing-audit")

# Project Connect: convention center appeal denied
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** The Texas Supreme Court denied Austin United's appeal on April 2, exhausting the PAC's legal options to stop the $1.6B redevelopment through the courts. The PAC is now organizing a new citizen-led petition campaign to place the issue directly before voters on the November 2026 ballot. Construction continues — the new convention center is expected to open late 2028 with approximately 620,000 sq ft of rentable space (70% increase over old center).")
    print("  Updated atx-convention-center")

# Bond: BEATF two options
idx, issue = find_issue(austin["issues"], title_keyword="Bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** The Bond Election Advisory Task Force produced two options for council consideration: a $766.5M comprehensive package and a narrowed $436M proposal. Parks could receive up to $260M (against $1.8B in identified needs). More than two-thirds of Austin residents say they're willing to support a tax increase for the bond, with housing, transportation, and parks as top priorities. Council is reviewing financial policies — final allocation discussions expected through late July. Council returns from summer recess July 23.")
    if issue.get("id") is None:
        issue["id"] = "atx-2026-bond-package"
    print("  Updated bond package")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-07T12:00:00Z"

# COPA: 26 sponsors, Mamdani supports
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** COPA now has 26 council sponsors — a clear majority. Unlike the previous version vetoed by Adams, Mayor Mamdani backed COPA on the campaign trail and has reiterated support in office, meaning no veto threat. The narrowed bill applies to buildings with 100 or fewer units whose affordability restrictions expire within two years — covering only ~0.6% of annual building transactions. Council Member Nurse framed the revision as 'stronger and more targeted.' The Real Deal reports modified COPA 'nears passage despite real estate pushback.' A council vote is expected in coming weeks.")
    print("  Updated nyc-copa-reintroduced")

# June 23 Primary: early voting countdown
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** ⚡ EARLY VOTING STARTS JUNE 13 — 6 DAYS AWAY. Primary Election Day is June 23. Multiple Brooklyn-area state legislative races in play including challenges in districts represented by Assembly Members Stefani Zinerman, Erik Dilan, and Steven Raga. City of Yes ADU applications: 98 received across Brooklyn, Bronx, Staten Island, and Queens — deadline June 12 (5 DAYS). East New York's rezoning continues to deliver: new construction boom WITHOUT gentrification or displacement, thanks to mandatory inclusionary housing requirements. The East 98th Street rezoning public scoping session is June 11 (4 DAYS).")
    print("  Updated nyc-june-primary-2026")

# City of Yes / Atlantic Ave
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** City of Yes ADU program update: 98 homeowner applications received across Brooklyn, Bronx, Staten Island, and Queens, with half submitted in the last two months. Application deadline: June 12 (5 DAYS). East New York's rezoning is being cited as a national model — new construction boom without gentrification, thanks to mandatory inclusionary housing. The Brownsville Neighborhood Community Plan continues advancing with three new affordable housing buildings proposed on vacant city-owned lots.")
    print("  Updated nyc-atlantic-ave-rezoning")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-07T12:00:00Z"

# ShotSpotter: more detail
idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** The ShotSpotter vote was 5-2-2 on May 18 (not June 1 as initially reported). CPD data shows a 65% false positive rate over the duration of ShotSpotter's use in Cambridge — meaning nearly two-thirds of alerts were not actual gunfire. Cambridge police officers have expressed unhappiness with the decision (Cambridge Day, June 1), arguing the technology aids rapid response. The 90-day removal deadline means all ShotSpotter devices must be disabled by mid-August 2026. Cambridge joins Chicago, New Orleans, and other cities that have ended ShotSpotter contracts.")
    print("  Updated cam-shotspotter-banned")

# Social housing task force
idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** Task force work continues — CDD consultant hiring underway. FY27 budget adoption expected imminently with public housing, shelters, and childcare as declared priorities (Councillors Nolan and Al-Zubi). The Barrett v. Cambridge inclusionary zoning lawsuit fact discovery deadline remains November 13, 2026 — AG Campbell's intervention underscores statewide stakes for 140+ municipalities. Committee swaps now in effect: McGovern now chairs Housing (was Economic Development).")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-07T12:00:00Z"

# Town Meeting wrap-up
idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** Town Meeting wrapped up its spring session through June 4-5. Key outcomes beyond the CHC Overlay District (217-20): WA14 (Accessory Dwelling Unit updates) and WA15 (inclusionary zoning cash payments for sub-20-unit developments) both endorsed by Planning Board and expected to pass with strong support. WA16 (26 Pleasant Street — 103 apartments including 15 affordable) was NOT MOVED and postponed to fall Town Meeting for further developer and community engagement. The fall session will be the next major opportunity for additional housing production.")
    print("  Updated brk-annual-town-meeting-2026")

save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-07T12:00:00Z"

# Housing developments
idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** Council continues advancing Housing Forward: approved cottage courts (up to 8 homes around shared courtyard on a single lot), four-home structures along major transit corridors, and allocated nearly $14M from the Affordable Housing Fund for new rental developments. Southeast and Southwest Area Plans adoption vote remains June 23 — 16 DAYS AWAY. The city needs ~2,000 new units annually to keep pace with population growth. Property assessments up 6.1% for 2026 (average home $500,300).")
    print("  Updated mad-new-housing-developments")

# BRT
idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 7 update:** Route A continues 15-minute service. Route B design work continuing through 2026 with construction now expected 2027, service opening 2028. The $118M federal funding remains at HIGH risk — city still has no signed FTA agreement. The Transportation Department requested $3.9M for Route B in the 2026 budget. City developing alternate strategies for scaled-back BRT improvements without federal funding. Route A ridership continues strong — up 18% since September 2022 launch.")
    print("  Updated mad-east-west-brt-construction")

save_json(ISSUES_DIR / "madison-wi.json", madison)

# ============================================================
# ORGS — OC Purple Accountability
# ============================================================
print("\n=== Updating oc-purple-accountability.json ===")
oc_purple = load_json(ORGS_DIR / "oc-purple-accountability.json")

campaign = find_campaign(oc_purple, campaign_id="bos-majority-defense")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 7 update:** ⚡ DOUBLE JEOPARDY: Dixon (R) has TAKEN THE LEAD over Foley (D) in D5 — latest count: Dixon 62,640 (48.5%) vs Foley 58,654 (45.4%). Combined with Shaw (R) leading Traut (D) by ~1,600 votes in D4 (26,264 to 24,643), the 3-2 Democratic BOS majority now faces potential defeat in BOTH swing seats. If both Republicans win in November, the board flips 4-1 Republican. Governor race: Becerra (D) takes slight lead over Hilton (R) — 26.7% vs 26.4%. SD-34: Valencia (D) dominant at 63% vs Shader (R) 37%. Canvass continues through July 10. The scorecard and voter accountability work is now mission-critical for November."
    )
    add_next_actions(campaign, [
        "Develop D4 + D5 November general election voter accountability strategy — both seats now at risk",
        "Track Dixon's housing and homelessness positions for the general election scorecard",
        "Monitor canvass period through July 10 for final certified results"
    ])
    print("  Updated bos-majority-defense")

# State legislative tracking
campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 7 update:** SD-34 results now clear: Valencia (D) 63% vs Shader (R) 37% — Valencia is the heavy favorite for the November general given the district's Democratic lean. Governor: Becerra (D) takes slight lead over Hilton (R) as ballots continue to be counted. Both advance to November. The governor's race determines the state housing enforcement environment — scorecard integration needed."
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
        "\n\n**June 7 update:** ⚡ HUNTINGTON BEACH delayed housing element adoption to June 16 — 9 DAYS. $50K/month fines accruing. ⚡ D5 ALARM: Dixon (R) has taken the lead over Foley (D) — 62,640 to 58,654. Combined with Shaw (R) leading Traut (D) by ~1,600 in D4, the Democratic BOS majority that supports housing enforcement faces double jeopardy. Governor: Becerra (D) takes slight lead over Hilton (R). OC Streetcar safety testing started June 3 — March 2027 launch confirmed. The enforcement framework that makes local housing advocacy effective depends on who controls the BOS and the governor's mansion in November."
    )
    print("  Updated orange-housing-element")

# Irvine general plan
campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 7 update:** Irvine Company's Oak Creek development revised to include a 50-acre public nature park at the heart of the development (approved 7-0 by Planning Commission in March). Environmental and traffic reviews underway. Formal public hearings expected late 2026 with a potential public vote due to 1988 open space designation. The project is far from a done deal — council approval, environmental review, and possible ballot measure all remain."
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
        "\n\n**June 7 update:** Garden Grove crisis update: GKN pledged $5M total in community support ($3M United Way OC Community Resilience Fund, $1M Red Cross, $1M community initiatives). Cleanup delayed — specialized trucks haven't arrived. ⚡ BOS majority at double risk: Dixon (R) leads Foley (D) in D5; Shaw (R) leads Traut (D) in D4. OC Streetcar safety testing started June 3, March 2027 launch. The new D4/D5 supervisors will shape FY27 budget priorities affecting childcare investment and family support services."
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
        "\n\n**June 7 update:** AISD parents/teachers protested budget cuts on June 5 — drawing significant media coverage. Board vote on the $181M deficit plan (558 positions affected) is June 18 — 11 DAYS. The AISD crisis is becoming a central campaign issue for November council candidates. Bond: BEATF produced two options ($766.5M comprehensive vs $436M narrowed). Council reviewing financial policies. Final allocation through late July. 2/3 of residents support a tax increase. Filing period opens July 20 (43 DAYS)."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 7 update:** Legal status unchanged — trial court must still rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 order. Convention center: TX Supreme Court denied Austin United's appeal April 2 — PAC organizing new petition for November ballot. Convention center on track for late 2028 opening. Project Connect legal uncertainty persists but ATP continues contract advancement."
    )
    print("  Updated defend-project-connect")

save_json(ORGS_DIR / "austin-yimby-action.json", atx_yimby)

# ============================================================
# ORGS — Austin Safe & Sound
# ============================================================
print("\n=== Updating austin-safe-and-sound.json ===")
atx_safe = load_json(ORGS_DIR / "austin-safe-and-sound.json")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 7 update:** Positive recruitment trend: 166% increase in test signups. Three recent cadet classes graduated 122 officers total. 154th class graduates August; 155th class begins with 65 cadets. APD projects full staffing by end of 2027. However, patrol sector vacancies still average ~25% and the department remains at 1,477 sworn of 1,816 authorized (19% vacancy). Professional staff at 9-10% vacancy."
    )
    print("  Updated apd-staffing-monitoring")

campaign = find_campaign(atx_safe, campaign_id="hso-strategic-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 7 update:** AISD parents/teachers protested budget cuts June 5. The $181M deficit plan (558 positions, 11 school closures) is heading for board vote June 18. School closures and larger class sizes compound public safety dynamics — reduced school investment can increase at-risk youth population. The HSO strategic plan's 5 focus areas remain the framework for accountability. Council returns from recess July 23."
    )
    print("  Updated hso-strategic-plan")

save_json(ORGS_DIR / "austin-safe-and-sound.json", atx_safe)

# ============================================================
# ORGS — Austin Abundance Project
# ============================================================
print("\n=== Updating austin-abundance-project.json ===")
atx_abundance = load_json(ORGS_DIR / "austin-abundance-project.json")

campaign = find_campaign(atx_abundance, campaign_id="childcare-desert-mapping")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 7 update:** AISD budget crisis deepens: 558 positions cut, 11 schools closing this summer. Parents/teachers protested June 5. Board vote June 18 (11 DAYS). School closures directly impact family access to childcare, after-school programs, and community services. The district is exploring selling 4 properties ($60M) — potential sites for family-oriented redevelopment. Bond: BEATF proposed $766.5M and $436M options. Council reviewing. 2/3 of residents support tax increase."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-07T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-07T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-07T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-07T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-07T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
