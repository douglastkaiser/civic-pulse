#!/usr/bin/env python3
"""
June 9, 2026 updates for all issue and organization data files.
Key developments since June 8:
  - OC: TODAY is the LAST DAY for mail ballot receipt (postmarked by June 2) — after today, no new ballots
  - OC D4: Shaw (R) continues to lead Traut (D); D5: Dixon (R) continues to lead Foley (D)
  - Governor: Becerra (D) 26.7% has overtaken Hilton (R) 26.4% — Becerra now leads
  - Garden Grove: Council meeting TOMORROW (June 10) — GKN demanded to send representative
  - HB housing vote June 16 (7 DAYS)
  - Austin: Morales appointment June 11 (2 DAYS); AISD board vote June 18 (9 DAYS)
  - Raising Travis County: 1,000 scholarships now funded (up from ~300 reported earlier)
  - NYC: Early voting starts June 13 (4 DAYS); COPA at 26 sponsors (majority)
  - NYC: City of Yes ADU deadline June 12 (3 DAYS); East 98th St scoping June 11 (2 DAYS)
  - Madison: SE/SW Area Plans vote June 23 (14 DAYS)
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
austin["last_scraped"] = "2026-06-09T12:00:00Z"

# AISD: countdown update
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** Board final vote on the $181M deficit budget is June 18 — 9 DAYS AWAY. Budget must be passed by June 30 (takes effect July 1). The proposed plan impacts 558 positions — teachers with certifications are guaranteed alternative placements, but non-certified staff (counselors, librarians, part-time APs) face layoffs. The 'Reclaim AISD' organization continues calling for a delay. Transportation hub model changes and health benefits reductions remain contentious. State funding formula hasn't changed since 2019 — HB 2's increase has not been enough. George Morales formally appointed Pct 4 commissioner June 11 (2 DAYS). Council on summer recess until July 23.")
    print("  Updated atx-aisd-budget-crisis")

# Pct 4: Morales 2 DAYS
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** George Morales will be formally appointed Pct 4 Commissioner on June 11 — 2 DAYS AWAY. Margaret Gómez's 31-year tenure ends this week. Morales immediately begins voting on county business: Raising Travis County childcare contracts ($28M+ awarded, with additional $17M in new contracts before Commissioners Court), infrastructure investments, and FY2027 budget. The Raising Travis County virtual town hall is June 16 at 6 PM (7 DAYS).")
    print("  Updated tc-pct4-runoff")

# Homelessness: evaluation underway
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** AT-Home Initiative ($6.7M, 5-year) and South Austin Housing Navigation Center RFP evaluations continue. Up to three providers will be selected for AT-Home; contracts start September 2026. The Navigation Center — the city's FIRST city-owned facility — on track for late summer/early fall 2026 opening. A 13-member Center Advisory Board is being formed (5 local reps, 3 people with lived experience, 4 housing/service partners, 1 civic rep). AISD board vote June 18 (9 DAYS) — school closures compound homelessness risk. Bond final vote July 23 (44 DAYS) — shelter infrastructure still NOT in ~$390M direction.")
    print("  Updated atx-hso-plan-adopted")

# Bond: countdown
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** Council on summer recess until July 23 — bond conversation resumes then. The ~$390M bond direction (parks $250M, transportation, community facilities) does NOT include housing. Final vote July 23 (44 DAYS). Mid-August council vote to formally call November election. Two-thirds of residents support a tax increase per community survey (53,000+ responses). AISD board vote on $181M deficit budget June 18 (9 DAYS). Morales appointed Pct 4 commissioner June 11 (2 DAYS).")
    print("  Updated atx-2026-bond")

# D1 Election: filing countdown
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** Filing period opens July 20 (41 DAYS). At least 8 candidates declared for D1, with seven having appointed treasurers — the most competitive open-seat race in the city. Council on summer recess until July 23. Key countdown: Morales appointed Pct 4 commissioner June 11 (2 DAYS). AISD board vote June 18 (9 DAYS). Bond final vote July 23 (44 DAYS). The AISD crisis ($181M deficit, 558 positions, 11 school closures), housing-excluded bond, and Project Connect legal limbo remain the defining candidate litmus tests.")
    print("  Updated atx-d1-election")

# Project Connect: status unchanged
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** Legal status unchanged — trial remains halted per TX Supreme Court May 22 procedural ruling. Travis County court must resolve AG Paxton's jurisdictional plea before trial can proceed. ATP continues $230M land acquisition (18 parcels) and contract advancement. Phase 1: 9.8 miles, 15 stops from 38th Street to Oltorf and east from Downtown to East Riverside. Ground-breaking expected early 2027, service 2033. Council on recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# Childcare: MAJOR UPDATE — 1,000 scholarships funded
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** ⚡ MAJOR MILESTONE: Raising Travis County has now funded childcare scholarships for 1,000 children — reaching its October target months ahead of schedule. Over 2,650 students enrolled in out-of-school time programs. $2.6M in gap funding distributed to 150 providers. This is the fastest implementation of any voter-approved children's fund of its kind in the country — and the first in Texas. Virtual town hall June 16 at 6 PM — 7 DAYS AWAY. George Morales appointed Pct 4 commissioner June 11 (2 DAYS) — he immediately begins voting on additional $17M in childcare contracts before Commissioners Court.")
    print("  Updated tc-childcare-funding")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-09T12:00:00Z"

# D4: LAST DAY mail ballot receipt
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** ⚡ TODAY is the LAST DAY for mail ballot receipt (postmarked by June 2). After today, no new ballots will be accepted — remaining counting is from already-received ballots. Shaw (R) continues to lead Traut (D) with a margin of ~1,600+ votes. The OC Registrar posted updated numbers on June 8 with Shaw's lead holding steady. Certification deadline July 10. The November general election — Shaw (R) vs. Traut (D) — is now the critical contest for the 3-2 Democratic BOS majority. Combined with Dixon (R) leading Foley (D) in D5, Democrats face double jeopardy. Huntington Beach housing vote June 16 (7 DAYS).")
    print("  Updated oc-bos-district-4-open-seat")

# D5: LAST DAY mail ballot receipt
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** ⚡ TODAY is the LAST DAY for mail ballot receipt (postmarked by June 2). After today, no new ballots accepted. Dixon (R) leads Foley (D) — approximately 48.5% to 45.4%. Dixon's lead has continued to widen with late-arriving conservative mail ballots. Both advance to November regardless, but Dixon enters the general with strong momentum. Certification deadline July 10. If Dixon wins in November, the board flips to Republican majority — affecting the $10.8B budget, housing enforcement, and homelessness investment.")
    print("  Updated oc-bos-district-5-defense")

# Governor: Becerra overtakes Hilton
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** Becerra (D) has overtaken Hilton (R) in the latest count — 26.7% to 26.4%. Becerra rapidly closed an initial 8,700-vote gap as mail-in ballots from Democratic-leaning counties were counted. AP has projected Becerra advances. Steyer trails at ~20% and has not conceded, but Hilton is favored for the second spot. The November matchup is crystallizing as Becerra (D) vs. Hilton (R). TODAY is the last day for mail ballot receipt. Certification deadline July 3. The governor determines California's housing enforcement posture — RHNA, Builder's Remedy, AG referrals — all central to OC housing advocacy.")
    print("  Updated ca-governor-2026")

# HB: 7 DAYS to vote
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** Huntington Beach housing element vote is June 16 — 7 DAYS AWAY. $50K/month fines continue accruing — the city has been noncompliant for over 4.5 years. The housing plan would zone for ~13,000 new units and allow opportunity for 413+ affordable homes. All legal avenues exhausted (US Supreme Court declined, state court ruled against, AG enforcement active). The June 16 vote is the most consequential remaining moment — if council adopts, HB begins the long road to compliance; if they refuse again, fines continue indefinitely. Certification deadline July 10 for primary results; July 3 for governor.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove: council meeting TOMORROW
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 9 update:** Garden Grove City Council meeting is TOMORROW (June 10) — council formally demanded GKN Aerospace send a representative. Chemical removal STILL delayed — specialized sealed trucks needed to transport MMA continue to be unavailable. No revised start date for chemical pumping operation announced. GKN's total pledged community support: $5M ($3M OC Community Resilience Fund, $1M Red Cross, $1M broader initiatives) — council has criticized this as insufficient. 44+ lawsuits filed in OC Superior Court and US District Court. Cal/OSHA investigation and DA Spitzer's criminal probe continue. Community demanding permanent facility closure.")
    print("  Updated Garden Grove chemical crisis")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-09T12:00:00Z"

# Primary: early voting 4 DAYS
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** ⚡ EARLY VOTING STARTS JUNE 13 — 4 DAYS AWAY. Early voting runs June 13-21. Primary Election Day is June 23 (14 DAYS). City of Yes ADU application deadline is June 12 (3 DAYS). East 98th Street rezoning public scoping session is June 11 (2 DAYS) at 2 PM. Key Brooklyn races: CD-7 (Velázquez seat — Reynoso, Valdez, Won competing), multiple state legislative seats. Register now if you haven't.")
    print("  Updated nyc-june-primary-2026")

# Atlantic Ave / housing: ADU deadline + scoping
idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** City of Yes ADU application deadline is June 12 — 3 DAYS AWAY. 98 homeowner applications received so far across Brooklyn, Bronx, Staten Island, and Queens, with half submitted in the last two months. East 98th Street rezoning public scoping session in East Flatbush (Community District 17) is June 11 (2 DAYS) at 2 PM. The South of Prospect Plan community engagement begins this summer. City of Yes continues delivering: 23% more housing permits in year one, 12,000+ units in pipeline from office conversions including 3,000+ affordable.")
    print("  Updated nyc-atlantic-ave-rezoning")

# COPA: 26 sponsors
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** COPA reached 26 council sponsors within one week of reintroduction on May 14 — a clear majority. The reintroduced version is narrower: applies to buildings with 100 or fewer units whose affordability restrictions expire within two years. Council Member Nurse expects a hearing in fall, with passage by year's end. Mayor Mamdani publicly supports the bill. No veto threat. Early voting for the June 23 primary starts June 13 (4 DAYS) — multiple Brooklyn seats on the ballot will shape the council's housing agenda.")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-09T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** ShotSpotter 90-day removal deadline approaching — all devices must be disabled by mid-August 2026. The 5-2-2 council vote (May 19) directed City Manager Huang to remove all devices. Cambridge joins Chicago, New Orleans, and other cities ending ShotSpotter contracts. CPD data showed 65% false positive rate. The Police Patrol Officers Association remains 'deeply disappointed.' City Manager Huang and CPD leadership had recommended keeping the technology.")
    print("  Updated cam-shotspotter-banned")

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** Social Housing Task Force continues work — CDD consultant hiring underway to support research on financing, governance, and expansion models. FY27 budget adoption expected with public housing, shelters, and childcare as declared priorities (Councillors Nolan and Al-Zubi). McGovern now chairs Housing Committee. Barrett v. Cambridge inclusionary zoning lawsuit fact discovery deadline remains November 13. Citywide free World Cup watch parties planned for June-July 2026.")
    print("  Updated cam-social-housing-task-force")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-09T12:00:00Z"
save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-09T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** Southeast and Southwest Area Plans adoption vote is June 23 — 14 DAYS AWAY. These are the third and fourth area plans under the city's updated framework. The plans shape land use, housing density, and transportation in two of Madison's fastest-growing areas. Residents have raised concerns about speeding, unsafe intersections, sidewalk gaps, and affordable housing. The plans do not automatically approve development but shape what the city supports. Property assessments up 6.1% for 2026 (average home $500,300). BRT Route A continues 15-minute service. Route B federal funding ($118M) remains at HIGH risk — no signed FTA agreement.")
    print("  Updated mad-new-housing-developments")

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 9 update:** Route A continues 15-minute service. Route B design work continuing through 2026 — construction expected 2027, service opening 2028 if federal funding secured. The $118M federal Capital Investment Grant remains at HIGH risk with no signed FTA agreement. City developing alternate strategies for scaled-back BRT improvements without federal funding. SE/SW Area Plans adoption vote June 23 (14 DAYS) — transit-oriented development along BRT corridors is a key component of both plans.")
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
        "\n\n**June 9 update:** ⚡ TODAY is the LAST DAY for mail ballot receipt (postmarked by June 2). After today, no new ballots accepted — remaining count is from already-received ballots. D4: Shaw (R) leads Traut (D) by ~1,600+ votes. D5: Dixon (R) leads Foley (D) ~48.5% to 45.4%. Both seats trending Republican heading into November. Certification deadline July 10. The window for reversing these trends is the November general election campaign — developing strategy for BOTH D4 and D5 is now the urgent priority. Governor: Becerra (D) has overtaken Hilton (R) 26.7% to 26.4%."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 9 update:** Governor: Becerra (D) has overtaken Hilton (R) — 26.7% to 26.4%. Becerra rapidly closed the gap as mail-in ballots from Democratic counties arrived. TODAY is the last day for ballot receipt. Certification deadline July 3. Steyer at ~20%, has not conceded. SD-34: Valencia (D) 63% vs Shader (R) 37% — Valencia heavy favorite for November. The governor's race determines California's housing enforcement framework."
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
        "\n\n**June 9 update:** Huntington Beach housing element vote is June 16 — 7 DAYS. $50K/month fines accruing — over 4.5 years noncompliant. All legal avenues exhausted. TODAY is the last day for mail ballot receipt. Governor: Becerra (D) has overtaken Hilton (R) 26.7% to 26.4% — a Democratic governor protects the RHNA/Builder's Remedy enforcement framework. D4 Shaw (R) leads Traut (D) by ~1,600+; D5 Dixon (R) leads Foley (D). If both Republicans win November, housing enforcement support at the county level is at serious risk."
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
        "\n\n**June 9 update:** Garden Grove City Council meeting is TOMORROW (June 10) — GKN Aerospace representative demanded to attend. Chemical removal STILL delayed with no revised timeline. Community demanding permanent facility closure. The crisis displaced thousands of families with young children. TODAY is the last day for mail ballot receipt — D4 Shaw (R) leads, D5 Dixon (R) leads. The next supervisors will shape FY27 childcare and family services budgets. Huntington Beach housing vote June 16 (7 DAYS)."
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
        "\n\n**June 9 update:** Filing period opens July 20 (41 DAYS). At least 8 candidates with 7 appointed treasurers for D1. George Morales formally appointed Pct 4 commissioner June 11 (2 DAYS). AISD board vote June 18 (9 DAYS) — 558 positions affected, budget must pass by June 30. Bond final vote July 23 (44 DAYS). Council on summer recess until July 23. The AISD crisis, housing-excluded bond, and Project Connect legal limbo define the candidate litmus tests."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 9 update:** Legal status unchanged — trial halted per TX Supreme Court May 22 ruling. AG Paxton's jurisdictional plea must be resolved first. ATP continues $230M land acquisition. Phase 1: 9.8 miles, 15 stops. Ground-breaking expected early 2027, service 2033. Council on recess until July 23."
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
        "\n\n**June 9 update:** AT-Home Initiative ($6.7M, 5-year) and Navigation Center RFP evaluations continue. A 13-member Center Advisory Board is being formed (5 local reps, 3 people with lived experience, 4 housing/service partners, 1 civic rep). Navigation Center on track for late summer/early fall opening — the city's FIRST city-owned facility. AISD board vote June 18 (9 DAYS) — 558 positions, 11 school closures compound homelessness risk. Bond final vote July 23 (44 DAYS) — shelter infrastructure NOT in ~$390M direction."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 9 update:** 157th cadet class on track for September 2026 graduation. APD remains at ~1,477 sworn of 1,816 authorized (19% vacancy). Patrol sector vacancies average ~25%. Chief Davis projects full staffing by end of 2027. Council on recess until July 23. Morales appointed Pct 4 commissioner June 11 (2 DAYS) — his law enforcement background (former constable) may influence county-level public safety coordination."
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
        "\n\n**June 9 update:** ⚡ MAJOR MILESTONE: Raising Travis County has now funded scholarships for 1,000 children — reaching the October target months ahead of schedule. Over 2,650 students in out-of-school time programs. $2.6M in gap funding distributed to 150 providers. This is the fastest implementation of any voter-approved children's fund in the country — and the first in Texas. Virtual town hall June 16 at 6 PM (7 DAYS). George Morales appointed Pct 4 commissioner June 11 (2 DAYS) — immediately begins voting on additional $17M in childcare contracts. AISD board vote June 18 (9 DAYS) — school closures directly impact family childcare and after-school access."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-09T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-09T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-09T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-09T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-09T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
