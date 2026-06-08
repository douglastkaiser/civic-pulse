#!/usr/bin/env python3
"""
June 8, 2026 updates for all issue and organization data files.
Key developments since June 7:
  - AISD: Public comment hearing June 5 drew significant turnout; "Reclaim AISD" org calls for delay
  - AISD board vote June 18 (10 DAYS); new transportation hub model proposed
  - George Morales formally appointed Pct 4 commissioner June 11 (3 DAYS)
  - Raising Travis County virtual town hall June 16 at 6 PM (8 DAYS)
  - OC canvass: June 8 scheduled vote count update (D4: Shaw leads; D5: Dixon leads)
  - Huntington Beach housing element vote June 16 (8 DAYS)
  - South Austin Navigation Center + AT-Home Initiative proposals closed June 2; evaluation underway
  - Garden Grove: City council formally demanded GKN send representative to next meeting
  - CA Governor: Becerra 26.7%, Hilton 26.4% — Katie Porter conceded
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
# ISSUES — AUSTIN
# ============================================================
print("=== Updating austin-78702.json ===")
austin = load_json(ISSUES_DIR / "austin-78702.json")
austin["last_scraped"] = "2026-06-08T12:00:00Z"

# AISD: Public comment hearing + countdown
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** Public comment hearing on June 5 drew significant turnout — teachers, staff, and parents urged the board to reconsider cuts. Key concerns: special programs (band, orchestra), new transportation hub model (students picked up at closest elementary school instead of designated stops), and health benefits changes. A new organization, 'Reclaim AISD,' has called for delaying the budget proposal to next year. Board final vote: June 18 — 10 DAYS AWAY. Budget takes effect July 1. The $181M deficit leaves few alternatives without state funding reform — HB 2's funding increase has not been enough to save districts from cutting positions, per a recent Texas House Public Education Committee hearing.")
    print("  Updated atx-aisd-budget-crisis")

# Pct 4: Morales appointment countdown
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** George Morales will be formally appointed Pct 4 Commissioner on June 11 — 3 DAYS AWAY. Margaret Gómez's formal retirement marks the end of 31 years in office. Morales will immediately begin voting on county business including the Raising Travis County childcare program ($28M+ awarded), infrastructure contracts, and the FY2027 county budget. Virtual town hall about the Raising Travis County initiative is June 16 at 6 PM (8 DAYS).")
    print("  Updated tc-pct4-runoff")

# Homelessness: Navigation Center + AT-Home proposals closed
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** South Austin Housing Navigation Center RFP and AT-Home Initiative proposals both closed June 2 — evaluation underway. Up to three providers will be selected for the AT-Home Initiative ($6.7M, 5-year contracts starting September 2026). The Navigation Center — the city's FIRST city-owned facility — is expected to open late summer/early fall 2026. AISD board vote June 18 (10 DAYS) — school closures compound homelessness risk for vulnerable families. Bond final vote July 23 — shelter infrastructure still NOT in ~$390M direction. Council on summer recess until July 23.")
    print("  Updated atx-hso-plan-adopted")

# Bond: countdown update
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** Summer standstill continues — council on recess until July 23. The ~$390M bond direction (parks $250M, transportation, community facilities) does NOT include housing. Final vote July 23 (45 DAYS). Mid-August deadline to call November election. Two-thirds of residents support a tax increase per community survey (53,000+ responses). Housing advocates have a 45-day window to lobby for inclusion before the final vote. AISD board vote on $181M deficit budget is June 18 (10 DAYS) — the simultaneous fiscal pressure strengthens the case for a comprehensive bond that addresses infrastructure holistically.")
    print("  Updated atx-2026-bond")

# D1 Election: filing countdown
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** Filing period opens July 20 (42 DAYS). Council on summer recess until July 23. AISD public comment hearing June 5 drew significant turnout — the budget crisis ($181M deficit, 558 positions, 11 school closures) is cementing itself as a central November campaign issue alongside housing, transit, and the bond. George Morales formally appointed Pct 4 commissioner June 11 (3 DAYS). Board final vote on AISD budget June 18 (10 DAYS). Bond final vote July 23 (45 DAYS). The gap between now and the filing period is the critical window to evaluate candidates' positions on all these issues.")
    print("  Updated atx-d1-election")

# Project Connect: status unchanged
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** Legal status unchanged — trial remains halted per TX Supreme Court May 22 procedural ruling. Travis County court must resolve AG Paxton's jurisdictional plea before trial can proceed. ATP continues $230M land acquisition (18 parcels) and contract advancement. Ground-breaking expected early 2027, lines open 2033. Council on summer recess until July 23.")
    print("  Updated atx-project-connect-legal-update")

# Childcare: town hall countdown
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** Raising Travis County virtual town hall scheduled June 16 at 6 PM — 8 DAYS AWAY. Nearly 300 kids have received childcare scholarships, 1,000 expected by October. Wait times have dropped from 2 years to months. Children 3 and under will no longer wait for scholarships by end of summer. George Morales formally appointed Pct 4 commissioner June 11 (3 DAYS) — he will immediately begin voting on childcare contracts and county budget priorities.")
    print("  Updated tc-childcare-funding")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-08T12:00:00Z"

# D4: Shaw lead — canvass update day
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** June 8 is a scheduled vote count update from the OC Registrar — new numbers expected today. As of June 5: Shaw (R) 26,264 (33.27%) vs Traut (D) 24,643 (31.22%). Shaw's lead widened from a 68-vote election-night margin to ~1,621 votes. Mail-in ballots postmarked by June 2 accepted through June 9 (TOMORROW is the last day for mail ballot receipt). Certification deadline July 10. Combined with Dixon (R) leading Foley (D) in D5, the 3-2 Democratic BOS majority faces double jeopardy in November.")
    print("  Updated oc-bos-district-4-open-seat")

# D5: Dixon lead — canvass update day
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** June 8 is a scheduled vote count update from the OC Registrar — new numbers expected today. As of June 7: Dixon (R) 62,640 (48.5%) vs Foley (D) 58,654 (45.4%). Dixon's lead has continued to widen as late-arriving conservative mail ballots are counted. Mail-in ballots postmarked by June 2 accepted through June 9 (TOMORROW is the last day for mail ballot receipt). Both advance to November regardless, but Dixon's growing lead establishes strong momentum for the general election. If Dixon wins in November, the board flips to Republican majority. Certification deadline July 10.")
    print("  Updated oc-bos-district-5-defense")

# Governor: Katie Porter conceded
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** Katie Porter has conceded — she will not advance. Becerra (D) 26.7% vs Hilton (R) 26.4% with counting continuing. Tom Steyer trails at ~21%. AP projected Becerra advances; the race for second between Hilton and Steyer remains too close to call but Hilton is favored. The November general election matchup is crystallizing as Becerra (D) vs Hilton (R) — though Steyer has not conceded. Certification deadline July 3. The governor's race determines California's housing enforcement posture — RHNA, Builder's Remedy, AG referrals.")
    print("  Updated ca-governor-2026")

# HB: countdown to June 16
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** Huntington Beach housing element vote is June 16 — 8 DAYS AWAY. The council voted 6-0 (Van Der Mark absent) to postpone to June 16. $50K/month fines are accruing — each day of delay costs taxpayers ~$1,667. The city has been noncompliant for over 4.5 years. The housing plan would zone for ~13,000 new units (but not require they be built) and allow opportunity for 413+ affordable homes. All legal avenues exhausted (US Supreme Court, state court, AG enforcement). The June 16 vote is the most consequential remaining moment in the HB compliance saga.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove: city council demands GKN presence
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 8 update:** Garden Grove City Council sent a formal letter to GKN Aerospace on June 4, criticizing the $3M donation as insufficient and demanding a company representative attend the next council meeting. Chemical removal STILL delayed — specialized sealed trucks needed to transport MMA have not arrived. OC Health Care Agency warns residents that odors may occur as cleanup continues. 44+ lawsuits filed. Cal/OSHA investigation and DA Spitzer's criminal probe continue in parallel. The community is demanding permanent facility closure.")
    print("  Updated Garden Grove chemical crisis")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-08T12:00:00Z"

# June 23 Primary: early voting countdown tightening
idx, issue = find_issue(brooklyn["issues"], "nyc-june-primary-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** ⚡ EARLY VOTING STARTS JUNE 13 — 5 DAYS AWAY. Primary Election Day is June 23 (15 DAYS). City of Yes ADU application deadline is June 12 (4 DAYS). East 98th Street rezoning public scoping session was June 11 (3 DAYS). Multiple Brooklyn-area state legislative races in play. Register to vote NOW if you haven't already.")
    print("  Updated nyc-june-primary-2026")

# COPA
idx, issue = find_issue(brooklyn["issues"], "nyc-copa-reintroduced")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** COPA has 26 council sponsors — a clear majority. No veto threat from Mayor Mamdani. Council vote expected in coming weeks. The narrowed bill applies to buildings with 100 or fewer units whose affordability restrictions expire within two years. Early voting for the June 23 primary starts June 13 (5 DAYS).")
    print("  Updated nyc-copa-reintroduced")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-08T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-shotspotter-banned")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** ShotSpotter 90-day removal deadline approaches — all devices must be disabled by mid-August 2026. Cambridge joins Chicago, New Orleans, and other cities ending ShotSpotter contracts. CPD data showed 65% false positive rate. Police officers remain unhappy with the decision (Cambridge Day, June 1).")
    print("  Updated cam-shotspotter-banned")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-08T12:00:00Z"
save_json(ISSUES_DIR / "brookline-ma.json", brookline)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-08T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 8 update:** Southeast and Southwest Area Plans adoption vote remains June 23 — 15 DAYS AWAY. The city needs ~2,000 new units annually to keep pace with population growth. Property assessments up 6.1% for 2026 (average home $500,300). Housing Forward reforms (cottage courts, four-home transit corridor structures) continue through implementation.")
    print("  Updated mad-new-housing-developments")

save_json(ISSUES_DIR / "madison-wi.json", madison)

# ============================================================
# ORGS — OC Purple Accountability
# ============================================================
print("\n=== Updating oc-purple-accountability.json ===")
oc_purple = load_json(ORGS_DIR / "oc-purple-accountability.json")

campaign = find_campaign(oc_purple, campaign_id="bos-majority-defense")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 8 update:** June 8 is a scheduled canvass vote count update day. As of latest counts: D4 — Shaw (R) 26,264 vs Traut (D) 24,643 (~1,621-vote gap). D5 — Dixon (R) 62,640 vs Foley (D) 58,654 (~4,000-vote gap). TOMORROW (June 9) is the last day for mail ballot receipt (postmarked by June 2). Certification deadline July 10. Both seats trending Republican heading into November. Governor: Becerra (D) 26.7% vs Hilton (R) 26.4% — Katie Porter conceded. Developing the November general election strategy for BOTH D4 and D5 is now the top priority."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 8 update:** Governor race update: Katie Porter conceded. AP projected Becerra advances. Hilton vs Steyer race for second remains close but Hilton favored — Becerra 26.7%, Hilton 26.4%, Steyer ~21%. Certification deadline July 3. SD-34: Valencia (D) 63% vs Shader (R) 37% — Valencia is the heavy favorite for November."
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
        "\n\n**June 8 update:** Huntington Beach housing element vote is June 16 — 8 DAYS. Council voted 6-0 to postpone (Van Der Mark absent). $50K/month fines accruing. The housing plan zones for ~13,000 new units and allows 413+ affordable homes. BOS canvass update expected today — D4 Shaw (R) leads Traut (D) by ~1,621; D5 Dixon (R) leads Foley (D) by ~4,000. TOMORROW (June 9) is the last day for mail ballot receipt. If both Republicans win November, the enforcement framework that supports local housing advocacy is at serious risk."
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
        "\n\n**June 8 update:** Garden Grove City Council formally demanded GKN send a representative to next meeting — $3M donation criticized as insufficient. Chemical removal STILL delayed. OC Health warns of odors during cleanup. The crisis displaced thousands of families with young children and exposed childcare infrastructure fragility. June 8 canvass update expected — BOS double jeopardy continues: Shaw (R) leads in D4, Dixon (R) leads in D5. The new supervisors will shape FY27 childcare and family services budget priorities. Huntington Beach housing element vote June 16 (8 DAYS)."
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
        "\n\n**June 8 update:** AISD public comment hearing June 5 drew significant turnout — teachers, parents, and staff testified against the $181M deficit cuts. A new organization 'Reclaim AISD' is calling for delaying the budget. Board final vote June 18 (10 DAYS). Filing period opens July 20 (42 DAYS). Bond final vote July 23 (45 DAYS). George Morales formally appointed Pct 4 commissioner June 11 (3 DAYS). Council on summer recess until July 23. The AISD crisis, bond direction, and Project Connect legal limbo are the defining issues candidates must address."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 8 update:** Legal status unchanged — trial halted per TX Supreme Court May 22 procedural ruling. ATP continues $230M land acquisition and contract advancement. Ground-breaking expected early 2027, lines open 2033. Council on summer recess until July 23."
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
        "\n\n**June 8 update:** South Austin Housing Navigation Center RFP and AT-Home Initiative ($6.7M, 5-year) proposals both closed June 2 — evaluation underway. Up to three providers will be selected; contracts start September 2026. Navigation Center — the city's FIRST city-owned facility — expected to open late summer/early fall 2026. AISD board vote June 18 (10 DAYS) — 558 positions affected, 11 schools closing. New transportation hub model proposed. School closures compound homelessness risk. Bond final vote July 23 — shelter infrastructure NOT in ~$390M direction."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-monitoring")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 8 update:** 157th cadet class (began January 2026) on track for September 2026 graduation. APD remains at ~1,477 sworn of 1,816 authorized (19% vacancy). Patrol sector vacancies still average ~25%. Chief Davis projects full staffing by end of 2027. Council on summer recess until July 23."
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
        "\n\n**June 8 update:** Raising Travis County virtual town hall June 16 at 6 PM — 8 DAYS AWAY. Nearly 300 kids have received scholarships, 1,000 expected by October. Wait times dropped from 2 years to months (KUT). Children 3 and under will no longer wait for scholarships by end of summer. George Morales formally appointed Pct 4 commissioner June 11 (3 DAYS) — he will immediately begin voting on childcare contracts. AISD board vote June 18 (10 DAYS) — new transportation hub model proposed alongside 558 position cuts and 11 school closures. School closures directly impact family childcare and after-school program access."
    )
    print("  Updated childcare-desert-mapping")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-08T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-08T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-08T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-08T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-08T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
