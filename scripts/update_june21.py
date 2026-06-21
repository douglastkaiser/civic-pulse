#!/usr/bin/env python3
"""
June 21, 2026 updates for all issue and organization data files.
Key developments since June 20:
  - Austin: ⚡ Judge Thomas ruled June 18 that convention center $1.35B bond
    funding plan is lawful — major legal victory for the project
  - Austin: AISD boundary workshops TOMORROW June 22 (10-11:30 AM) and June 23
    (6-7:30 PM) — Oak and Elm map scenarios; comment card open through July 31
  - Austin: Bond survey closes June 23 (2 DAYS); Council recess until July 23 (32 DAYS)
  - Austin: D1 filing period opens July 19 (28 DAYS)
  - Austin: Raising Travis County — $51.7M distributed so far
  - OC: ⚡ D5 FLIPPED — Foley (D) now leads Dixon (R) ~47.0% to ~46.8% in latest count;
    ~10,000 ballots remaining countywide; next count June 24
  - OC: ⚡ FBI executed search warrant at GKN Aerospace June 10 — federal criminal
    probe for hazardous substance law violations; seized training logs, safety complaints
  - OC: 6,000+ United Way OC assistance applications from Garden Grove incident
  - OC: HB fines now $50K/month since June; judge ruling next month on $150K/month increase
  - OC: Grand Jury homelessness response deadline June 30 (9 DAYS)
  - OC: Garden Grove council meeting June 23 (2 DAYS)
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
austin["last_scraped"] = "2026-06-21T12:00:00Z"

# AISD: Boundary workshops TOMORROW
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** AISD boundary realignment virtual workshops begin TOMORROW — June 22 (10-11:30 AM) and June 23 (6-7:30 PM). Two draft scenarios presented: 'Oak' and 'Elm' maps showing different configurations for attendance zones after 10 school closures. Nothing is final — online comment card open through July 31. Board update expected August; vote anticipated September; implementation August 2027. Bond survey closes June 23 (2 DAYS). Council on recess until July 23 (32 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Filing period opens July 19 (28 DAYS). First day to file in person July 20. Filing deadline August 17. At least 8 candidates declared — most competitive open D1 race since geographic representation began in 2014. AISD boundary workshops TOMORROW: June 22 (10-11:30 AM) and June 23 (6-7:30 PM). Bond survey closes June 23 (2 DAYS). Council on recess until July 23 (32 DAYS). Election Day November 3.")
    print("  Updated atx-d1-election")

# Bond: survey 2 DAYS
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Bond community input survey closes June 23 — 2 DAYS remaining. 53,000+ individual responses; top priorities: transportation (19.8%), housing & homelessness (18.5%), parks (16.3%); ~70% support a property tax increase. The ~$390M bond direction (parks, transportation, community facilities) does NOT include housing. Council on recess until July 23 — final bond vote that day (32 DAYS). City Manager Broadnax to present bond proposal at July 23 meeting.")
    print("  Updated atx-2026-bond")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea per TX Supreme Court May 22 order. No new court filings. Phase 1 scope: 9.8-mile surface line (reduced from original 20.2-mile network with downtown subway). ATP continues design work, property acquisition ($230M for 18 parcels), and contract advancement under federal Record of Decision. Target completion 2033. Council on recess until July 23 (32 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# HSO
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Sunrise Homeless Navigation Center tentative selection for South Austin Housing Navigation Center at 2401 S. I-35 — council approval vote July 23 (32 DAYS). Sunrise is the largest homelessness services provider in central Texas: 800+ people rehoused in 2026, 1,880 connected to housing in 2025, 28,801 served across all programs. 13-member Advisory Board formed. AT-Home Initiative ($6.7M, 5-year) proposals under review. AISD boundary workshops TOMORROW — school closures compound homelessness risk. Bond survey closes June 23 (2 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** 157th cadet class mid-training — graduation September 18. APD remains 300+ officers short of authorized strength (~1,819 of ~2,120 authorized). 156th cadet class graduated May 1. AISD campus police cuts from $205M budget could increase demand on APD patrol resources. Council on recess until July 23 (32 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** ⚡ $51.7M already distributed through Raising Travis County initiative — nearly 300 scholarships issued, target 1,000 by October. Families pay no more than 7% of annual income on childcare; eligible up to 85% of State Median Income (~$92K for family of four). AISD boundary workshops TOMORROW: June 22 and 23 — school closures directly impact childcare access patterns. CDBG public comment continues through July 20; public hearing July 14 at 9 AM.")
    print("  Updated tc-childcare-funding")

# Pct 4
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Morales serving as Pct 4 Commissioner. $51.7M already distributed through Raising Travis County initiative. CDBG public comment continues through July 20; public hearing July 14 at 9 AM. Bond survey closes June 23 (2 DAYS). AISD boundary workshops TOMORROW: June 22 and 23.")
    print("  Updated tc-pct4-runoff")

# ⚡ Convention center: MAJOR UPDATE — Judge ruled funding lawful June 18
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** ⚡ MAJOR LEGAL VICTORY: Travis County District Court Judge Sherine Thomas ruled June 18 that Austin's $1.35B bond funding plan for the convention center expansion is lawful. The city can use hotel occupancy tax funds to pay down debt on up to $1.35B in bonds approved by Council last month. Construction continues on the $1.6B project — excavation in full force, reaching depths of 50+ feet for underground exhibit halls and loading docks; 293,000 cubic yards of dirt removed. Reopening target: spring 2029, nearly doubling rentable space to ~620,000 sq ft. Austin United PAC's TX Supreme Court appeal denied April 2 — PAC now organizing NEW petition for November 2026 ballot. Council on recess until July 23 (32 DAYS).")
    print("  Updated atx-convention-center")

# Golf course
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Rezoning process continues for 445-acre Jimmy Clay/Roy Kizer site (5,000-15,000 unit potential). Council resolution sponsored by Fuentes, Alter, Ellis, and Laine. AISD boundary workshops TOMORROW: June 22 and 23 — south Austin school consolidation could reshape housing demand for this site. Bond survey closes June 23 (2 DAYS). Council on recess until July 23 (32 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Citywide DBC in effect since May 22 — five tiers adding 0-60 feet of extra height. Rental projects must reserve units at ≤50% MFI; homeownership at ≤80% MFI. Previous DB90 program produced dozens of rezonings with ~20,000 homes planned; DBC expected to replace DB90 going forward. SB 840 (effective Sept 2025) allows multifamily by-right in commercial zones at 36 units/acre and 45 ft — Austin code still being updated for full compliance. Council on recess until July 23 (32 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Development rules overhaul implementation continuing. SB 840 compliance: multifamily now allowed by-right in CS, GR, LO, GO and similar districts at 36 units/acre minimum and 45 ft height — no rezoning, variance, or CUP required. Missing middle housing resolution approved; draft ordinances due by March 2027. Council on recess until July 23 (32 DAYS).")
    print("  Updated atx-development-rules-overhaul")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-21T12:00:00Z"

# ⚡ D5: Foley now leads
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** ⚡ RACE FLIPPED: Foley (D) now leads Dixon (R) ~47.0% to ~46.8% in latest count — a dramatic reversal from earlier counts. Only ~10,000 ballots remaining countywide. No candidate above 50%, so BOTH advance to November general election. Next registrar count June 24 (3 DAYS). Final certification July 10. Becerra (D) +21 over Hilton (R) in first general governor poll may boost Democratic turnout in November. If Dixon wins November, the board flips to Republican majority — affecting $10.8B budget, housing enforcement, and homelessness investment. Grand Jury response deadline June 30 (9 DAYS).")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Shaw (R) and Traut (D) both advancing to November general. Next registrar count June 24 (3 DAYS). Final certification July 10. ⚡ D5 has flipped — Foley (D) now leads Dixon (R) ~47.0% to ~46.8%. Garden Grove council meeting June 23 (2 DAYS) — GKN accountability hearings continue. ⚡ FBI executed search warrant at GKN June 10; federal criminal probe ongoing. SBA Business Recovery Center open.")
    print("  Updated oc-bos-district-4-open-seat")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** General election confirmed: Becerra (D) vs Hilton (R). Primary results with 88% counted: Becerra 28%, Hilton 25%. Becerra +21 points in first general poll among likely voters. Democrats outnumber Republicans nearly 2-to-1 statewide. Hilton has vowed to cut income taxes, slash environmental regulations, boost oil drilling — a Hilton win could weaken state housing enforcement (RHNA, Builder's Remedy, AG referrals). County certification deadline July 3 for governor, July 10 for local races. ⚡ D5 has flipped — Foley (D) now leads Dixon (R).")
    print("  Updated ca-governor-2026")

# HB: HCD review pending; fines escalating
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** HB housing element adopted June 16 (6-1) — HCD review and certification still pending. ⚡ Fines escalated to $50,000/month starting June 2026 (up from $10K/month since Jan 2025). Judge ruling NEXT MONTH on further increase to $150,000/month — could reach $900K/month and receivership if still noncompliant. HB has lost EVERY legal challenge including US Supreme Court (denied Feb 2026). HB was the ONLY noncompliant city in all of Orange County. Becerra (D) win would maintain aggressive state enforcement.")
    print("  Updated oc-newsom-housing-warning (HB)")

# ⚡ Garden Grove: FBI search warrant
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 21 update:** ⚡ FBI executed search warrant at GKN Aerospace June 10 — U.S. Magistrate Judge Christensen signed warrant June 4. Federal criminal probe targets violations of laws requiring companies to prevent accidental release of extremely hazardous substances. Authorized seizure: chemical samples, employee training logs, internal safety complaints, company communications, storage tank and cooling equipment documents. Three parallel investigations: FBI/EPA (federal criminal), OC DA Spitzer (state criminal), Cal/OSHA (workplace safety). 6,000+ assistance applications to United Way OC. Chemical extraction still delayed — sealed trucks not arrived; no revised start date. 44+ lawsuits filed. Garden Grove council meeting June 23 (2 DAYS) — continued GKN accountability hearings. SBA Business Recovery Center open Mon-Fri 8 AM-7 PM. Grand Jury response deadline June 30 (9 DAYS).")
    print("  Updated Garden Grove chemical crisis")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Construction at 95%. Safety testing underway since June 3 — verifying train operations, control systems, and street signal interface. Revenue service pushed to March 2027. Fleet: eight Siemens S700 vehicles delivered, six planned for daily service. Expected 5,000 passengers/day across 10 stops. $2 one-way/$5 day pass. 6 AM-11 PM daily.")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury: 9 DAYS
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 21 update:** Grand Jury response deadline June 30 — 9 DAYS remaining. Grand Jury recommended county earmark sufficient discretionary funds toward homelessness prevention by June 30. OC completed 1,544 permanent supportive housing units with 1,811 more planned. PIT Count: 6,321 (down 13.7%), more sheltered than unsheltered for first time. ⚡ D5 flipped — Foley (D) now leads Dixon (R); supervisor race outcome directly affects homelessness policy.")
    print("  Updated OC Homelessness")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** Grand Jury homelessness response deadline June 30 — 9 DAYS. $20.9M Supportive Housing NOFA + $35.1M HHAP funding continue flowing. PIT Count: 6,321 (down 13.7%). ⚡ D5 flipped — Foley (D) now leads Dixon (R); November outcome determines board majority and enforcement vs. services balance.")
    print("  Updated oc-homelessness-enforcement")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** $20.9M Supportive Housing NOFA application period continues. Combined with $35.1M HHAP = $56M+ in housing funding. ⚡ D5 flipped — Foley (D) leads Dixon (R); supervisor race affects housing funding priorities. Grand Jury response deadline June 30 (9 DAYS). OC completed 1,544 permanent supportive housing units with 1,811 more planned.")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 21 update:** General election confirmed: Valencia (D) vs Shader (R). Valencia dominated primary at 63%. County certification deadline July 10. ⚡ D5 race has flipped — Foley (D) now leads Dixon (R), reshaping downstream ticket dynamics.")
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
        "\n\n**June 21 update:** ⚡ D5 FLIPPED: Foley (D) now leads Dixon (R) ~47.0% to ~46.8% in latest count — dramatic reversal. ~10,000 ballots remaining. Both advance to November (no candidate above 50%). Next count June 24 (3 DAYS). Certification July 10. Grand Jury homelessness response deadline June 30 (9 DAYS). Becerra (D) +21 over Hilton (R) in first general governor poll — strong Democratic headwinds for November."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 21 update:** Becerra (D) vs Hilton (R) confirmed for governor; Valencia (D) vs Shader (R) for SD-34. ⚡ D5 flipped — Foley (D) now leads Dixon (R). HB housing element adopted June 16 — fines at $50K/month, could increase to $150K/month next month. HB lost every legal challenge including US Supreme Court. Certification July 10."
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
        "\n\n**June 21 update:** HB housing element adopted June 16 (6-1) — HCD certification pending. ⚡ Fines escalated to $50K/month since June; judge ruling NEXT MONTH on $150K/month increase; could reach $900K/month and receivership. HB lost every legal challenge including US Supreme Court (denied Feb 2026). Becerra (D) +21 over Hilton (R) — Becerra win maintains aggressive state housing enforcement. ⚡ D5 flipped — Foley (D) leads Dixon (R). Grand Jury deadline June 30 (9 DAYS)."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 21 update:** Oak Creek Golf Course conversion: environmental and traffic reviews underway; public hearings expected late 2026. Irvine Company revised plan: 50-acre nature park + ~3,000 housing units. Former mayors gathering signatures for citizen's initiative challenging 1988 open space designation. November council elections (3 seats + mayor) critical. ⚡ D5 flipped — Foley (D) leads Dixon (R); countywide housing coordination affected by supervisor race."
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
        "\n\n**June 21 update:** ⚡ FBI executed search warrant at GKN Aerospace June 10 — federal criminal probe ongoing. 6,000+ assistance applications to United Way OC. Chemical extraction still delayed; sealed trucks not arrived. Garden Grove council meeting June 23 (2 DAYS) — continued GKN accountability. SBA Business Recovery Center open. Grand Jury response deadline June 30 (9 DAYS). ⚡ D5 flipped — Foley (D) leads Dixon (R); supervisor race controls county budget and childcare/family services investment."
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
        "\n\n**June 21 update:** Filing period opens July 19 (28 DAYS). At least 8 candidates declared for D1. AISD boundary workshops TOMORROW: June 22 (10-11:30 AM) and June 23 (6-7:30 PM) — Oak and Elm map scenarios. Bond survey closes June 23 (2 DAYS). Council on recess until July 23 (32 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 21 update:** Legal status unchanged — Judge Shepperd must rule on AG Paxton's jurisdictional plea. Phase 1: 9.8-mile surface line (reduced from 20.2-mile network). ATP continues design, property acquisition ($230M for 18 parcels), contract advancement. Target completion 2033. ⚡ Convention center: Judge Thomas ruled June 18 that $1.35B bond funding plan is lawful — positive precedent for public project financing. Council on recess until July 23 (32 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 21 update:** Rezoning continues for 445-acre site (resolution by Fuentes, Alter, Ellis, Laine). AISD boundary workshops TOMORROW — south Austin school consolidation reshapes housing demand. Bond survey closes June 23 (2 DAYS). Council on recess until July 23 (32 DAYS)."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 21 update:** DBC in effect since May 22 — five tiers (0-60 ft extra height). DB90 produced ~20,000 homes planned; DBC expected to replace DB90. SB 840 allows multifamily by-right in commercial zones — Austin code still updating for full compliance. Missing middle draft ordinances due March 2027. ⚡ Convention center: Judge Thomas ruled June 18 that $1.35B bond plan is lawful. Bond survey closes June 23 (2 DAYS). Council on recess until July 23 (32 DAYS)."
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
        "\n\n**June 21 update:** Sunrise tentative selection for South Austin Navigation Center — council vote July 23 (32 DAYS). Sunrise stats: 800+ rehoused in 2026, 1,880 connected to housing in 2025, 28,801 served total. AT-Home Initiative ($6.7M, 5-year) proposals under review. AISD boundary workshops TOMORROW — school closures compound homelessness risk. Bond survey closes June 23 (2 DAYS) — shelter infrastructure NOT in ~$390M bond direction."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**June 21 update:** 157th cadet class mid-training — graduation September 18. 156th class graduated May 1. APD remains 300+ officers short (~1,819 of ~2,120 authorized). AISD campus police cuts from $205M budget increase demand on APD. Council on recess until July 23 (32 DAYS)."
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
        "\n\n**June 21 update:** ⚡ $51.7M already distributed through Raising Travis County initiative. Nearly 300 scholarships issued, target 1,000 by October. Families pay ≤7% of income; eligible up to 85% SMI (~$92K for family of four). AISD boundary workshops TOMORROW: June 22 and 23 — school closures impact childcare access. CDBG public comment through July 20; hearing July 14 at 9 AM."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**June 21 update:** AISD budget at $205M — 558 positions eliminated; impacts AISD employees as public employer. $51.7M distributed through Raising Travis County initiative. Council on recess until July 23 (32 DAYS)."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-06-21T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-06-21T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-06-21T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-06-21T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-06-21T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
