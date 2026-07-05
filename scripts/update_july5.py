#!/usr/bin/env python3
"""
July 5, 2026 updates for all issue and organization data files.
Key developments since July 4:
  - Post-holiday Saturday — most offices remain closed for extended weekend
  - Austin: Council recess continues (returns July 23 = 18 DAYS)
  - Austin: Environmental Commission unanimously recommends delaying Dog's Head TIRZ vote to Jan 2027
  - Austin: City Manager FY2027 budget due July 16 (11 DAYS)
  - Austin: ERCOT forecasts possible record peak demand >92 GW this summer; grid emergency chance <1%
  - Austin: AISD Teacher Career Fair July 16 (11 DAYS); boundary Phase 1 draft August 7
  - Austin: DBC still zero applications after nearly 7 weeks since approval
  - OC: State certification July 10 (5 DAYS); AG HB penalties Day 5 at escalated rate
  - OC: OCEA July 1 session described as "borderline bad faith bargaining" — county has $204M above reserve target
  - OC: GKN Phase 1 complete; Phase 2 timeline still pending; Wikipedia article created
  - OC: HB cross-complaint struck July 2 via anti-SLAPP; AG fees recovery hearing July 17
  - OC: Streetcar launch pushed to March 2027 (was spring 2026)
  - Brooklyn: NYC offices reopening Monday; $125.8B FY2027 budget in effect
  - Madison: Council meeting July 7 (2 DAYS); city faces $11M shortfall for 2027
  - Cambridge: Doug Brown petition remains de facto law; AHO concerns continue
  - Brookline: Extended holiday weekend; Chestnut Hill overlay application expected this summer
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
austin["last_scraped"] = "2026-07-05T12:00:00Z"

# Dog's Head
idx, issue = find_issue(austin["issues"], "atx-dogs-head-annexation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — offices closed. Environmental Commission voted unanimously to recommend delaying Council's July 23 TIRZ vote until January 2027 or later, citing need for full environmental assessment, 400-ft Colorado River setback, and affordable housing (30-80% MFI). Council members Siegel, Watson, Vela, and Velásquez proposed stronger river protections and dedicating TIRZ revenues to affordable housing. Travis County TIRZ vote July 14 (9 DAYS). TIRZ modeling projects land value reaching $26B by 2061.")
    print("  Updated atx-dogs-head-annexation")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — offices closed. Travis County TIRZ vote July 14 (9 DAYS). Council vote July 23 (18 DAYS). D1 filing opens July 20 (15 DAYS). Environmental Commission's TIRZ delay recommendation could affect broader development timeline if Council defers.")
    print("  Updated atx-golf-course-rezone")

# Gas peaker plant
idx, issue = find_issue(austin["issues"], "atx-gas-peaker-plant")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. ERCOT forecasts possible record peak demand >92 GW this summer (vs 85.5 GW record in August 2023), driven by population growth and data center surge. Grid emergency chance remains <1% for June-July per ERCOT. Peak demand shifted to ~9 PM as solar fades while cooling and data centers stay high. Austin Energy over 70% carbon-free. City Manager budget July 16 (11 DAYS). Council returns July 23 (18 DAYS).")
    print("  Updated atx-gas-peaker-plant")

# HSO / homelessness
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. Sunrise Homeless Navigation Center confirmed as tentative SAHNC operator — has already rehoused 800 people in 2026. Council vote on operator July 23 (18 DAYS). SAHNC at 2401 S. I-35 — construction continues, opening June 2027. City Manager budget July 16 (11 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# AISD
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — AISD offices closed. $181M deficit: 558 positions affected, 215 educator salary cuts for 2026-27. Teacher Career Fair July 16 at Toney Burger Center (11 DAYS). Boundary changes: Phase 1 draft August 7 (33 DAYS) covers schools receiving students from 10 closed campuses + over-enrolled schools + Marshall Middle School attendance area. Phase 2 pushed to 2028-29. Board vote September.")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — campaign activity quiet. Harper-Madison term-limited; seat open for first time in 8 years. Filing opens July 20 (15 DAYS); deadline August 17. Semi-annual campaign finance filings due mid-July — will reveal fundraising trajectories. At least 7 candidates have appointed treasurers. City Manager budget July 16 (11 DAYS). Election Day November 3. Council returns July 23 (18 DAYS).")
    print("  Updated atx-d1-election")

# Bond
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. Bond discussion resumes at July 23 meeting; final vote to place on ballot not until mid-August. Staff Alternative Scenario: $390M baseline — ~$250M parks/trails (largest share), $92M transit including $52M sidewalks/trails/bike paths. Housing ($200M) excluded. Mayor Watson opposed but lost 6-2-1. Austin Parks Foundation actively advocating for parks investment. City Manager budget July 16 (11 DAYS).")
    print("  Updated atx-2026-bond")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. DBC approaching 7 weeks since approval with still zero applications. Program offers 15-60 ft extra height across 5 tiers in multifamily/commercial zones. Replaced controversial DB90 program. Council returns July 23 (18 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — courts closed. TX Supreme Court ruled May 22 that trial court deliberately erred by advancing case without addressing Paxton's jurisdictional plea. Case remanded: lower court must rule on AG's plea before proceeding. Chief Justice Blacklock wrote lower court's approach 'was a deliberate effort to frustrate the State's appellate rights.' Bond validation process paused pending jurisdictional ruling. Federal funding still uncertain — Trump admin has not agreed to any new transit projects. Council returns July 23 (18 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — APD normal operations. Department still ~700 officers short but reporting 166% increase in test sign-ups; on pace for full staffing by end of 2027. $3.7M budgeted for recruitment (highest in 5 years). City auditor found no formal long-term recruitment plan. City Manager budget July 16 (11 DAYS). Council returns July 23 (18 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — construction paused. $1.6B 'Unconventional ATX' project: 293,000 cubic yards of dirt removed; demolition complete; excavation continues through 2026. Citizen petition to halt project overruled by judge June 18. Targeting world's first zero-carbon convention center — mass timber roof, low-carbon concrete/steel, salvaged materials. LEED Gold. Spring 2029 reopening. Council returns July 23 (18 DAYS).")
    print("  Updated atx-convention-center")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. Raising Travis County: $75M voter-approved initiative (Nov 2024, 59% yes) — fastest implementation of its kind nationally, first in Texas. $17.65M in contracts with ~180 providers; eligibility up to 85% SMI ($92K for family of 4). Wait times dropped from 2 years to months. 5,200 families to be served. City Manager budget July 16 (11 DAYS).")
    print("  Updated tc-childcare-funding")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. DBC: zero applications in nearly 7 weeks. Minimum lot size 1,800 sq ft citywide — implementation ongoing. Council returns July 23 (18 DAYS).")
    print("  Updated atx-development-rules-overhaul")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-07-05T12:00:00Z"

# Garden Grove / GKN
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**July 5 update:** Extended holiday weekend — offices closed. Phase 1 complete (June 29-July 2): neutralized MMA removed from tanks #2 and #4. No evacuations needed during removal; fruity odor detected but concentrations well below health concern levels. Phase 2 timeline still pending — includes remaining tank and facility remediation. Wikipedia article now exists documenting incident. Air monitoring continues with no exceedances. 44+ lawsuits filed. Three criminal investigations ongoing (FBI/EPA, OC DA Spitzer, Cal/OSHA). State certification July 10 (5 DAYS). Crisis Day 45.")
    print("  Updated Garden Grove chemical crisis")

# D5
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — offices closed. Primary results: Foley (D) 48.4% vs Dixon (R) 45.8% vs Vellema 5.7% — November runoff confirmed. 3-2 Democratic BOS majority hinges on this race. AG HB penalties Day 5 at escalated rate. OCEA July 1 session: union called it 'borderline bad faith bargaining' — county has $204M above reserve target per OCEA forensic audit while proposing zero wage increases. State certification July 10 (5 DAYS). BOS cancelled through August.")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — offices closed. Shaw (R) vs Traut (D) confirmed for November. GKN Phase 1 complete; Phase 2 pending. OCEA forensic audit: county has $204M above reserve target, $252M reserve increase since 2019 — disputes county's deficit narrative. State certification July 10 (5 DAYS). BOS cancelled through August.")
    print("  Updated oc-bos-district-4-open-seat")

# HB housing element
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — courts closed. July 2 ruling: court struck HB's cross-complaint via anti-SLAPP motion — found city's lawsuit arose from State's protected activity of enforcing CA law. State entitled to recover attorney's fees. Hearing July 17 for additional penalties. AG HB penalties Day 5 at escalated rate ($150K/month combined). State certification July 10 (5 DAYS). 120-day zoning deadline ~October 14.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. Final primary count: Hilton (R) ~28%, Becerra (D) ~26% with all precincts partially reporting. County certifications completed July 3. Secretary of State certification July 10 (5 DAYS). State hasn't elected Republican governor in 20 years. General election November 3.")
    print("  Updated ca-governor-2026")

# OC FY2027 Budget
idx, issue = find_issue(oc["issues"], "oc-fy2027-budget")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. OCEA July 1 negotiations (4th session): OCEA's forensic auditor found county has $204M above reserve target; reserves increased $252M since 2019. OCEA chief spokesperson called session 'borderline bad faith bargaining.' County took 25% supervisor pay raises + $715K executive comp while proposing hiring freezes and zero wage increases for workers. Teamsters Local 952 contract expired June 25. AG HB penalties Day 5. State certification July 10 (5 DAYS). BOS cancelled through August.")
    print("  Updated oc-fy2027-budget")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — testing paused. Launch date pushed from spring 2026 to March 2027 per OCTA May 2026 announcement, citing 'challenges related to construction.' Street testing began Feb 20 on Santa Ana Blvd. 4.15-mile, 10-stop all-electric route between Santa Ana and Garden Grove. State certification July 10 (5 DAYS).")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**July 5 update:** Extended holiday weekend. Grand Jury response deadline passed June 30 — still no public reporting on county or city responses. OCEA forensic audit reveals county has $204M above reserve target despite deficit claims. BOS cancelled through August. State certification July 10 (5 DAYS).")
    print("  Updated OC Homelessness Grand Jury")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. NOFA remains open until closed, replaced, or all funds committed. State certification July 10 (5 DAYS). BOS cancelled through August.")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. Valencia (D) dominated primary at 63% — heavy favorite for November given district's Democratic lean. State certification July 10 (5 DAYS).")
    print("  Updated oc-state-senate-sd34")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. Grand Jury response deadline passed — no public reporting. Common Good workforce reentry campus groundbreaking June 24 — first publicly owned facility of its kind in SoCal. State certification July 10 (5 DAYS). BOS cancelled through August.")
    print("  Updated oc-homelessness-enforcement")

# Orange Housing Element
idx, issue = find_issue(oc["issues"], "oc-orange-housing-element")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. HB cross-complaint struck July 2 — court found city can't sue state for enforcing housing law. Strengthens precedent for all noncompliant cities including Orange. AG HB penalties Day 5 at escalated rate. State certification July 10 (5 DAYS).")
    print("  Updated oc-orange-housing-element")

# AD-68
idx, issue = find_issue(oc["issues"], "oc-ad68-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. State certification July 10 (5 DAYS). Valencia's move to SD-34 leaves seat open.")
    print("  Updated oc-ad68-open-seat")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-07-05T12:00:00Z"

idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — city offices closed. NYC $125.8B FY2027 budget now in effect (adopted June 30). Offices reopen Monday July 7. Monitor Point must return to CPC for scope approval before full Council vote — no date confirmed. South of Prospect Plan: first neighborhood plan accounting for IBZ; zoning concept map expected later 2026.")
    print("  Updated nyc-atlantic-ave-rezoning")

idx, issue = find_issue(brooklyn["issues"], "nyc-city-of-yes-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — city offices closed. ADU progress: 3,100+ homeowner applications received; legal across all five boroughs (restrictions in R1-R3, historic districts, and flood zones). Q1 2026 housing permits nearly doubled: 28,773 units filed vs 14,338/quarter average in 2025. RPA notes persistent challenges around ADU financing and contractor availability. Offices reopen Monday July 7.")
    print("  Updated nyc-city-of-yes-implementation")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-07-05T12:00:00Z"

idx, issue = find_issue(madison["issues"], "budget-rules-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend — offices closed. Next council meeting July 7 (2 DAYS). City faces $11M shortfall for 2027; agencies preparing 2% budget reductions. FY2026 operating budget: $452.5M (4.6% increase). Christine Knapp starts as Madison Water Utility GM August 31. Heat wave continues across Midwest. Next meeting after July 7: July 21.")
    print("  Updated budget-rules-2026")

save_json(ISSUES_DIR / "madison-wi.json", madison)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-07-05T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-zoning-reform-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. Doug Brown citizen petition (signed by 13 residents) remains de facto law until Council votes (earliest August 3). Would impose additional setback requirements, height restrictions, and parking requirements — effectively freeze several development projects per Vice Mayor Azeem. Flaherty-Zusy amendments also pending. Residents sharply divided. Council summer recess continues.")
    print("  Updated cam-zoning-reform-implementation")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-07-05T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. Heat emergency continues across the Northeast. Cooling centers remain open. FY2027 budget maintaining existing services after override passed. Town offices reopen Monday.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 5 update:** Extended holiday weekend. Chestnut Hill overlay approved 217-20 on May 28. City Realty formal redevelopment application expected this summer; special permit review 9-12 months. 783 multifamily units + 200-room hotel. Groundbreaking spring 2028 at earliest. Heat emergency continues through the weekend.")
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
        "\n\n**July 5 update:** Extended holiday weekend. D5: Foley 48.4% vs Dixon 45.8% — November runoff confirmed. OCEA July 1: forensic audit shows county $204M above reserve target; union called session 'borderline bad faith bargaining.' HB cross-complaint struck July 2 via anti-SLAPP. GKN Phase 1 complete. State certification July 10 (5 DAYS). BOS cancelled through August."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 5 update:** Extended holiday weekend. Governor: final county certifications complete — Becerra (D) vs Hilton (R) confirmed. State certification July 10 (5 DAYS). SD-34: Valencia (D) dominated at 63%. AD-68: open seat, certification pending."
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
        "\n\n**July 5 update:** Extended holiday weekend. HB cross-complaint struck July 2 via anti-SLAPP — court ruled city can't sue state for enforcing housing law; AG entitled to fee recovery. Hearing July 17 for additional penalties. AG HB penalties Day 5 at escalated rate ($150K/month). Strengthens precedent for all noncompliant cities. State certification July 10 (5 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 5 update:** Extended holiday weekend. GKN Phase 1 complete. OCEA forensic audit: county has $204M above reserve target despite deficit narrative. State certification July 10 (5 DAYS). BOS cancelled through August."
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
        "\n\n**July 5 update:** Extended holiday weekend. OCEA forensic audit reveals county has $204M above reserve target — disputes deficit narrative threatening family services. County took 25% supervisor raises while proposing zero for workers. Teamsters contract expired June 25. State certification July 10 (5 DAYS). BOS cancelled through August."
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
        "\n\n**July 5 update:** Extended holiday weekend — campaign quiet. Harper-Madison term-limited; D1 open for first time in 8 years. Filing opens July 20 (15 DAYS); deadline August 17. Semi-annual finance filings due mid-July. At least 7 candidates with treasurers. Bond discussion resumes July 23. City Manager budget July 16 (11 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 5 update:** Extended holiday weekend — courts closed. TX Supreme Court May 22 ruling remanded case: trial court must rule on Paxton's jurisdictional plea first. Chief Justice Blacklock called lower court's approach 'a deliberate effort to frustrate the State's appellate rights.' Bond validation paused. Federal funding still uncertain. Council returns July 23 (18 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 5 update:** Extended holiday weekend. Environmental Commission unanimously recommended delaying TIRZ vote to Jan 2027 — wants full environmental assessment, 400-ft river setback, affordable housing requirements. Travis County TIRZ vote July 14 (9 DAYS); council vote July 23 (18 DAYS) if not delayed."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 5 update:** Extended holiday weekend. DBC approaching 7 weeks with zero applications. 5 tiers offering 15-60 ft extra height in multifamily/commercial zones. Council returns July 23 (18 DAYS)."
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
        "\n\n**July 5 update:** Extended holiday weekend. Sunrise confirmed as tentative SAHNC operator — largest homelessness services provider in central TX, already rehoused 800 people in 2026. Council operator vote July 23 (18 DAYS). SAHNC opening June 2027. City Manager budget July 16 (11 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 5 update:** Extended holiday weekend — APD normal operations. Still ~700 officers short but 166% increase in test sign-ups; on pace for full staffing by end of 2027. $3.7M recruitment budget (highest in 5 years). Auditor: no formal long-term recruitment plan. ERCOT forecasts possible record peak >92 GW. City Manager budget July 16 (11 DAYS). Council returns July 23 (18 DAYS)."
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
        "\n\n**July 5 update:** Extended holiday weekend. Raising Travis County: $75M voter-approved initiative (Nov 2024, 59%) — fastest implementation nationally, first in Texas. $17.65M contracted with ~180 providers; eligibility up to 85% SMI ($92K/family of 4). Wait times dropped from 2 years to months. 5,200 families to be served. City Manager budget July 16 (11 DAYS)."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**July 5 update:** Extended holiday weekend. City Manager budget July 16 (11 DAYS). D1 filing opens July 20 (15 DAYS). Council returns July 23 (18 DAYS)."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-07-05T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-07-05T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-07-05T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-07-05T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-07-05T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
