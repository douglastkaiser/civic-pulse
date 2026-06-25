#!/usr/bin/env python3
"""
June 25, 2026 updates for all issue and organization data files.
Key developments since June 24:
  - Austin: Bond battle erupts — council majority directs staff to build ~$400M package
    (parks $250-260M, active transport $75-80M, facilities $50-60M); Mayor Watson & Duchen oppose;
    staff recommends delaying to 2028. Staff presents July 23; council decides by August.
  - Austin: D1 filing period opens July 19 (24 DAYS); council recess until July 23 (28 DAYS)
  - Austin: AISD boundary comment card open through July 31; revised draft map to trustees August
  - Austin: Raising Travis County at $51.7M+; CDBG comment through July 20; hearing July 14 (19 DAYS)
  - OC: No new ballot count today — next count June 26 (TOMORROW); D5 razor-thin:
    Foley (D) ~47.0% vs Dixon (R) ~46.8%; ~10,000 ballots remaining countywide
  - OC: GKN extraction STILL delayed — sealed trucks haven't arrived (35+ days post-incident);
    GKN employees conducting safety checks for partial production restart in unaffected sections
  - OC: Grand Jury homelessness response deadline June 30 (5 DAYS)
  - OC: HB housing element adopted June 16 — 120-day zoning deadline ~Oct 14;
    AG seeking additional $100K/month penalties starting July 1
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
austin["last_scraped"] = "2026-06-25T12:00:00Z"

# AISD: boundary comment card still open
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** AISD boundary realignment comment card remains open through July 31 — revised draft map to trustees in August; board vote expected September; implementation August 2027. 10 campuses closing this summer. ⚡ Bond battle: council majority voted to direct staff to build ~$400M bond package (parks $250-260M, active transport $75-80M, facilities $50-60M) — Mayor Watson and CM Duchen oppose; staff recommends delaying to 2028. Staff presents when council returns July 23 (28 DAYS). CDBG public comment through July 20; hearing July 14 (19 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Filing period opens July 19 (24 DAYS). First day to file in person July 20. Filing deadline August 17. At least 8 candidates declared — most competitive open D1 race since geographic representation began in 2014. Semi-annual campaign finance filings due July will reveal fundraising trajectories. ⚡ Bond debate intensifies: council majority directs staff to build ~$400M package; Mayor Watson opposes — bond decision shapes D1 race dynamics. Council on recess until July 23 (28 DAYS). Election Day November 3.")
    print("  Updated atx-d1-election")

# Bond: council divided
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** ⚡ Council DIVIDED on bond — majority (Alter, Ellis, Siegel, Vela, Qadri, Velásquez) voted to direct staff to create ~$400M bond package: parks ($250-260M), active transportation ($75-80M), community facilities/cultural arts ($50-60M). Mayor Watson and CM Duchen oppose, citing Prop Q defeat last fall. Staff recommends delaying to 2028 but will present potential package when council returns July 23 (28 DAYS). Council must decide by August whether to place on November ballot. Housing ($200M) remains excluded. Community input survey closed — 53,000+ responses compiled.")
    print("  Updated atx-2026-bond")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 order. No new court filings. Phase 1: 9.8-mile surface line, 15 stations, all-electric trains every 5 minutes. Full price tag estimated at $8B+ including interest. ATP continues design, property acquisition ($230M for 18 parcels), contract advancement. Target completion 2033. Council on recess until July 23 (28 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# HSO
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Sunrise Navigation Center tentative operator selection for South Austin Housing Navigation Center at 2401 S. I-35 — council approval vote July 23 (28 DAYS). AT-Home Initiative ($6.7M, 5-year) proposals under review — contract awards September 2026. Bond battle: shelter infrastructure NOT in ~$400M bond direction; housing ($200M) also excluded. CDBG public comment through July 20; hearing July 14 (19 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** 157th cadet class mid-training — graduation September 18. APD remains 300+ officers short of authorized strength (~1,819 of ~2,120 authorized). 156th class graduated May 1. Austin's 30th homicide of 2026 recorded June 24 on South Lamar. Council on recess until July 23 (28 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Raising Travis County at $51.7M+ distributed — 25 contracts serving 9,402 children/youth. Nearly 300 scholarships issued, target 1,000 by October. Families pay ≤7% of income; eligible up to 85% SMI (~$92K for family of four). Infant/toddler care and nontraditional-hours coverage remain key gaps. CDBG public comment through July 20; hearing July 14 at 9 AM (19 DAYS). Bond debate: housing ($200M) excluded from ~$400M direction.")
    print("  Updated tc-childcare-funding")

# Pct 4
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Morales serving as Pct 4 Commissioner. $51.7M+ distributed through Raising Travis County — 9,402 children/youth served. CDBG public comment through July 20; hearing July 14 at 9 AM (19 DAYS). Council on recess until July 23 (28 DAYS).")
    print("  Updated tc-pct4-runoff")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Excavation in full force — continuing through August 2026; 293,000+ cubic yards of dirt removed. D-wall construction progressing between 2nd & 3rd Streets. Judge Thomas's June 18 ruling affirmed the $1.35B bond funding plan. On track for spring 2029 reopening as world's first Net Zero Carbon Certified Convention Center — nearly doubling rentable space to ~620,000 sq ft. Austin United PAC organizing new petition for November 2026 ballot. Council on recess until July 23 (28 DAYS).")
    print("  Updated atx-convention-center")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Rezoning process continues for 445-acre Jimmy Clay/Roy Kizer site (5,000-15,000 unit potential). Council resolution sponsored by Fuentes, Alter, Ellis, and Laine. Bond battle may affect broader housing/infrastructure landscape. Council on recess until July 23 (28 DAYS). Filing period for D1 opens July 19 (24 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Citywide DBC in effect since May 22 — five tiers adding 0-60 feet of extra height. Rental projects reserve units at ≤50% MFI; homeownership at ≤80% MFI. Monitoring DBC uptake as key indicator of whether framework produces actual housing. SB 840 allows multifamily by-right in commercial zones — Austin code still updating. Council on recess until July 23 (28 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Development rules implementation continuing. SB 840 compliance: multifamily by-right in CS, GR, LO, GO districts at 36 units/acre and 45 ft. Missing middle housing draft ordinances due March 2027. Council on recess until July 23 (28 DAYS).")
    print("  Updated atx-development-rules-overhaul")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-25T12:00:00Z"

# D5: no new count today, next count TOMORROW
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** No new ballot count today — next OC Registrar count TOMORROW (June 26). D5 remains razor-thin: Foley (D) ~47.0% vs Dixon (R) ~46.8% with ~10,000 ballots remaining countywide. Lead has changed hands multiple times during canvass. Both advance to November regardless. Final certification July 10 (15 DAYS). Grand Jury homelessness response deadline June 30 (5 DAYS). If Dixon wins November, the board flips to Republican majority — affecting $10.8B budget, housing enforcement, and homelessness investment.")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Traut (D) leads with ~33% vs Shaw (R) ~31% — both advancing to November general. Next OC Registrar count TOMORROW (June 26). Final certification July 10 (15 DAYS). GKN chemical extraction STILL delayed — sealed trucks haven't arrived 35+ days post-incident; GKN employees conducting safety checks for partial production restart in unaffected sections while under three criminal investigations (FBI/EPA, DA Spitzer, Cal/OSHA). Grand Jury response deadline June 30 (5 DAYS).")
    print("  Updated oc-bos-district-4-open-seat")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** General election confirmed: Becerra (D) vs Hilton (R). Primary results nearly final — Becerra 28%, Hilton 25% with 88% counted. County certification deadline July 3 for governor, July 10 for local races. Next OC Registrar count TOMORROW — D5 remains razor-thin. Grand Jury response deadline June 30 (5 DAYS).")
    print("  Updated ca-governor-2026")

# HB: fines accruing, AG seeking additional penalties
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** HB housing element adopted June 16 (6-1) — HCD review and certification still pending. Court-ordered $50,000/month fines accruing since June 2026; total owed now ~$400K+. ⚡ AG seeking additional $100,000/month penalties starting July 1 — could reach $150K/month. After 3 months, court may triple fines; after that, multiply by six and appoint receiver. 120-day zoning deadline from June 16 adoption = ~October 14. Only 1,187 of 5,845 required very-low/low-income units permitted so far.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Garden Grove: extraction STILL delayed
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 25 update:** GKN chemical extraction STILL delayed — specialized sealed trucks have NOT arrived, 35+ days post-incident. No revised start date announced. GKN employees conducted safety checks during third week of June for partial production restart in unaffected facility sections — while under three parallel criminal investigations (FBI/EPA federal search warrant served June 10, OC DA Spitzer state, Cal/OSHA workplace safety). 44+ lawsuits filed. Company pledged $5M total ($3M OC Community Resilience Fund + $1M Red Cross + $1M county). OC Registrar next count TOMORROW — D5 race directly affects county industrial safety oversight. Grand Jury response deadline June 30 (5 DAYS).")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Construction at ~92%. Street testing underway since February 20 on Santa Ana Boulevard. Revenue service target pushed to March 2027. Track complete along entire route. Fleet: eight Siemens S700 vehicles manufactured in Sacramento. Expected 5,000 passengers/day across 10 stops. $2 one-way/$5 day pass. 6 AM-11 PM daily.")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury: 5 DAYS
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 25 update:** Grand Jury response deadline June 30 — 5 DAYS remaining. County must earmark sufficient discretionary funds toward homelessness prevention by deadline. Grand Jury report emphasized shift from reactive (shelters, encampment clearances) to preventative approaches (rental assistance, early intervention). OC completed 1,544 permanent supportive housing units with 1,811 more planned. PIT Count: 6,321 (down 13.7%). Next OC Registrar count TOMORROW — D5 race affects homelessness policy direction.")
    print("  Updated OC Homelessness")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** Grand Jury homelessness response deadline June 30 — 5 DAYS. $20.9M Supportive Housing NOFA + $35.1M HHAP continue. PIT Count: 6,321 (down 13.7%). Next Registrar count TOMORROW — D5 outcome determines board majority and enforcement vs. services balance.")
    print("  Updated oc-homelessness-enforcement")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** $20.9M Supportive Housing NOFA application period continues. Combined with $35.1M HHAP = $56M+ in housing funding. Grand Jury response deadline June 30 (5 DAYS). OC completed 1,544 units with 1,811 more planned. Next Registrar count TOMORROW — supervisor race affects housing funding priorities.")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 25 update:** General election confirmed: Valencia (D) vs Shader (R). Valencia dominated primary at 63%. County certification deadline July 10 (15 DAYS). Next OC Registrar count TOMORROW.")
    print("  Updated oc-state-senate-sd34")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ORGS — OC Purple Accountability
# ============================================================
print("\n=== Updating oc-purple-accountability.json ===")
oc_purple = load_json(ORGS_DIR / "oc-purple-accountability.json")

campaign = find_campaign(oc_purple, campaign_id="bos-majority-defense")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 25 update:** No new ballot count today — next OC Registrar count TOMORROW (June 26). D5 razor-thin: Foley (D) ~47.0% vs Dixon (R) ~46.8%; ~10,000 ballots remaining. D4: Traut (D) leads Shaw (R) ~33% to ~31%. Grand Jury response deadline June 30 (5 DAYS). GKN extraction STILL delayed — 35+ days; sealed trucks haven't arrived. HB 120-day zoning deadline ~Oct 14; AG seeking $100K/month additional penalties starting July 1. Final certification July 10 (15 DAYS)."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 25 update:** Becerra (D) vs Hilton (R) for governor — primary results nearly final (Becerra 28%, Hilton 25%). Valencia (D) vs Shader (R) for SD-34. County certification July 3 (governor), July 10 (local). Next OC Registrar count TOMORROW — D5 razor-thin."
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
        "\n\n**June 25 update:** HB housing element adopted June 16 (6-1) — HCD certification pending. Court-ordered $50K/month fines accruing; total owed ~$400K+. ⚡ AG seeking additional $100K/month penalties starting July 1 — could escalate to receivership. 120-day zoning deadline from June 16 = ~October 14. Only 1,187 of 5,845 required units permitted. Four Builder's Remedy applications (696 units) remain in pipeline. Next OC Registrar count TOMORROW — D5 razor-thin; board majority affects housing enforcement posture. Grand Jury deadline June 30 (5 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 25 update:** Oak Creek Golf Course conversion: environmental and traffic reviews underway; public hearings expected late 2026. Irvine Company revised plan: 50-acre nature park + ~3,000 housing units. November council elections (3 seats + mayor) critical. Next OC Registrar count TOMORROW — D5 razor-thin; countywide housing coordination affected by supervisor race."
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
        "\n\n**June 25 update:** GKN extraction STILL delayed — sealed trucks haven't arrived, 35+ days post-incident. GKN employees conducted safety checks for partial production restart in unaffected sections while under three criminal investigations. 44+ lawsuits filed. Company pledged $5M total. Next OC Registrar count TOMORROW — D5 razor-thin; supervisor race controls county budget and childcare/family services investment. Grand Jury response deadline June 30 (5 DAYS)."
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
        "\n\n**June 25 update:** Filing period opens July 19 (24 DAYS). At least 8 candidates declared for D1. ⚡ Bond battle shapes race dynamics — council majority directs staff to build ~$400M package (parks $250-260M, active transport $75-80M, facilities $50-60M); Mayor Watson opposes. Staff presents July 23. Semi-annual campaign finance filings due July. Council on recess until July 23 (28 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 25 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. Phase 1: 9.8-mile surface line, 15 stations, trains every 5 min. Full cost $8B+ including interest. ATP continues design, property acquisition ($230M for 18 parcels). Convention center excavation through August — 293,000+ cubic yards removed; June 18 bond ruling provides precedent. Council on recess until July 23 (28 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 25 update:** Rezoning continues for 445-acre site. Bond battle may reshape broader housing/infrastructure landscape. Council on recess until July 23 (28 DAYS)."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 25 update:** DBC in effect since May 22 — monitoring uptake. SB 840 multifamily by-right in commercial zones — Austin code still updating. Missing middle draft ordinances due March 2027. ⚡ Bond battle: council majority directs staff to build ~$400M package but housing ($200M) excluded — parks, active transport, and facilities prioritized over housing. Staff recommends delaying to 2028. Council on recess until July 23 (28 DAYS)."
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
        "\n\n**June 25 update:** Sunrise Navigation Center tentative operator selection — council vote July 23 (28 DAYS). AT-Home Initiative ($6.7M, 5-year) proposals under review — awards September 2026. Bond battle: shelter infrastructure NOT in ~$400M bond direction; housing ($200M) also excluded. CDBG public comment through July 20; hearing July 14 (19 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 25 update:** 157th cadet class mid-training — graduation September 18. APD remains 300+ officers short (~1,819 of ~2,120 authorized). Austin's 30th homicide of 2026 recorded June 24 on South Lamar. Council on recess until July 23 (28 DAYS)."
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
        "\n\n**June 25 update:** Raising Travis County at $51.7M+ distributed — 25 contracts serving 9,402 children/youth. Nearly 300 scholarships issued, target 1,000 by October. Families pay ≤7% of income. Infant/toddler care and nontraditional-hours coverage remain key gaps. CDBG public comment through July 20; hearing July 14 at 9 AM (19 DAYS). Bond debate: housing ($200M) excluded from ~$400M direction."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 25 update:** Raising Travis County at $51.7M+ distributed. Bond battle: council majority directs staff to build ~$400M package; staff recommends delaying to 2028. Council on recess until July 23 (28 DAYS). Filing period for council races opens July 19 (24 DAYS)."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-25T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-25T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-25T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-25T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-25T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
