#!/usr/bin/env python3
"""
July 8, 2026 updates for all organization data files.
Key developments since July 7:
  - Austin: Dog's Head TIRZ county vote July 14 (6 DAYS); Environmental Commission delay recommendation
  - Austin: CDBG hearing July 14 (6 DAYS); public comments through July 20
  - Austin: City Manager budget July 16 (8 DAYS)
  - Austin: D1 filing opens July 20 (12 DAYS); 7+ candidates including Goodwin (assistant DA)
  - Austin: Project Connect legal limbo continues — Judge Shepperd ruling still pending
  - Austin: APD staffing: KXAN reports ~1,484 sworn of 1,812 authorized (~330 vacancies)
  - Austin: DBC still zero applications after 7+ weeks
  - Austin: SAHNC operator vote July 23 (15 DAYS); opening delayed to June 2027
  - OC: NEW — San Diego court dismissed HB's latest lawsuit (June 30 ruling, reported July 7)
  - OC: Anti-SLAPP granted; penalties at $50K/month, AG seeking $100K/month from July 1
  - OC: HB adopted housing element June 16; HCD review pending; hearing July 17 (9 DAYS)
  - OC: State primary certification July 10 (2 DAYS); D5 razor-thin 0.17-point margin
  - OC: OCEA fourth bargaining session July 1 — union calls it "borderline bad faith"
  - OC: Voice of OC July 7: cascading municipal budget deficits across OC
  - OC: GKN Phase 1 cleanup commenced June 30; FBI investigation underway
  - OC: Oak Creek revised to include 50+ acre nature park, under 3,000 units
  - OC: Court of Appeal ruled zoning overlays insufficient for RHNA — expands builder's remedy exposure
"""
import json
from pathlib import Path

ORGS_DIR = Path(__file__).resolve().parent.parent / "public" / "data" / "orgs"
META_DIR = Path(__file__).resolve().parent.parent / "public" / "data" / "meta"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Saved {path.name}")


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


def append_to_summary(campaign, text):
    campaign["summary"] = campaign["summary"] + text


# ============================================================
# AUSTIN YIMBY ACTION
# ============================================================
print("\n=== Austin YIMBY Action ===")
yimby = load_json(ORGS_DIR / "austin-yimby-action.json")

c = find_campaign(yimby, campaign_id="defend-project-connect")
if c:
    append_to_summary(c, "\n\n**July 8 update:** Legal status unchanged — Judge Shepperd still has not ruled on AG Paxton's jurisdictional plea. TX Supreme Court's May 22 procedural ruling sent the case back, requiring the lower court to resolve the plea before any trial. Either path (plea denied → interlocutory appeal; plea granted → suit dismissed) means months of delay. Federal funding uncertain — Trump admin has not agreed to any new transit projects; Sen. Cornyn publicly opposes. ATP continues design, property acquisition ($230M for 18 parcels), and contract advancement. Three major contracts expected in 2026: full 9.8-mile buildout, O&M facility, train cars. Ground-breaking expected early 2027, service 2033. Convention center: D-wall complete, structural steel in progress — June 18 bond ruling precedent holds. City Manager budget July 16 (8 DAYS). Council returns July 23 (15 DAYS).")
    print("  Updated: defend-project-connect")

c = find_campaign(yimby, campaign_id="council-elections-2026")
if c:
    append_to_summary(c, "\n\n**July 8 update:** D1 filing opens July 20 (12 DAYS); deadline August 17. At least 7 candidates with appointed treasurers — most competitive open-seat race since 2014. Key candidates: Amber Goodwin (assistant DA, gun violence prevention advocate), Misael Ramos (2022 runner-up, 25.3%/6,065 votes), Steven Brown (Save Austin Now co-chair), Alexandria Anderson (MLK Neighborhood Assoc). Semi-annual campaign finance filings due mid-July will reveal fundraising trajectories. ⚡ Dog's Head TIRZ: Environmental Commission unanimously recommended delay to Jan 2027 — county vote July 14 (6 DAYS). Candidates' positions on the TIRZ are a key litmus test. City Manager budget July 16 (8 DAYS). Bond final vote July 23 (15 DAYS). Election Day November 3.")
    print("  Updated: council-elections-2026")

c = find_campaign(yimby, campaign_id="golf-course-rezone")
if c:
    append_to_summary(c, "\n\n**July 8 update:** Rezoning continues for 445-acre Jimmy Clay/Roy Kizer site (5,000-15,000 unit potential). ⚡ Dog's Head TIRZ: Environmental Commission unanimously recommended delay to Jan 2027 — wants full environmental assessment, 400-ft river setback, affordable housing requirements (30-80% MFI). Travis County TIRZ vote July 14 (6 DAYS); council vote July 23 (15 DAYS) if not delayed. Commissioner Howard called process 'rushed'; Commissioner Shea skeptical of developer Endeavor's 'Project Toaster' promises. Bond: housing ($200M) excluded from ~$390M direction; final vote July 23 (15 DAYS). Council returns July 23.")
    print("  Updated: golf-course-rezone")

c = find_campaign(yimby, campaign_id="ongoing-housing-advocacy")
if c:
    append_to_summary(c, "\n\n**July 8 update:** DBC still zero applications after 7+ weeks — Austin Planning confirmed no submissions. SB 840 by-right multifamily in commercial zones may be reducing developer incentive for DBC participation. Downtown DDB400/DDB850 also seeing no activity. ⚡ Dog's Head TIRZ: Environmental Commission unanimously recommended delay to Jan 2027 — county vote July 14 (6 DAYS). Bond: housing ($200M) excluded from ~$390M direction; final vote July 23 (15 DAYS). City Manager budget July 16 (8 DAYS). Council returns July 23 (15 DAYS).")
    print("  Updated: ongoing-housing-advocacy")

save_json(ORGS_DIR / "austin-yimby-action.json", yimby)


# ============================================================
# AUSTIN ABUNDANCE PROJECT
# ============================================================
print("\n=== Austin Abundance Project ===")
abundance = load_json(ORGS_DIR / "austin-abundance-project.json")

c = find_campaign(abundance, campaign_id="childcare-desert-mapping")
if c:
    append_to_summary(c, "\n\n**July 8 update:** Raising Travis County continues record-pace implementation — over $28M awarded total. $17.34M to Workforce Solutions for 1,000 annual scholarships (children up to 3); $4.16M for quality improvements at 150 providers. 13 community partners serving 5,200+ children. Children 3 and under no longer waiting for scholarships by end of summer. Families pay no more than 7% of income. ⚡ CDBG public hearing July 14 at 9 AM (6 DAYS) — comment period through July 20. AISD boundary realignment Phase 1 draft August 7 (30 DAYS); Phase 2 postponed to 2028-29. City Manager budget July 16 (8 DAYS). Council returns July 23 (15 DAYS) — bond final vote ($390M, housing excluded).")
    print("  Updated: childcare-desert-mapping")

c = find_campaign(abundance, campaign_id="employer-index")
if c:
    append_to_summary(c, "\n\n**July 8 update:** Campaign in planning phase. City Manager budget July 16 (8 DAYS) — FY2027 budget provides context for public employer benefit policies. D1 filing opens July 20 (12 DAYS). Council returns July 23 (15 DAYS).")
    print("  Updated: employer-index")

c = find_campaign(abundance, campaign_id="family-housing-campaign")
if c:
    append_to_summary(c, "\n\n**July 8 update:** DBC still zero applications after 7+ weeks — developer uptake remains the key indicator of whether the framework produces family-sized housing. Dog's Head TIRZ: Environmental Commission unanimously recommended delay to Jan 2027 — county vote July 14 (6 DAYS). AISD boundary realignment Phase 1 draft August 7 (30 DAYS). Bond: housing ($200M) excluded from ~$390M direction; final vote July 23 (15 DAYS). Council returns July 23.")
    print("  Updated: family-housing-campaign")

c = find_campaign(abundance, campaign_id="parental-leave-city-hall")
if c:
    append_to_summary(c, "\n\n**July 8 update:** City Manager budget July 16 (8 DAYS) — FY2027 budget context for workforce benefit advocacy. Proposed FY2027 APD budget $544M ($26M increase); city-wide $6.3B with $33M deficit. D1 filing opens July 20 (12 DAYS). Council returns July 23 (15 DAYS).")
    print("  Updated: parental-leave-city-hall")

save_json(ORGS_DIR / "austin-abundance-project.json", abundance)


# ============================================================
# AUSTIN SAFE & SOUND
# ============================================================
print("\n=== Austin Safe & Sound ===")
safe = load_json(ORGS_DIR / "austin-safe-and-sound.json")

c = find_campaign(safe, campaign_id="hso-strategic-plan")
if c:
    append_to_summary(c, "\n\n**July 8 update:** Sunrise selected as tentative SAHNC operator — council approval vote July 23 (15 DAYS). SAHNC at 2401 S. I-35 — construction continues, opening June 2027. 13-member Advisory Board formed from 69 applicants. AT-Home Initiative ($6.7M, 5-year) contract awards expected September — 98% retention rate in permanent supportive housing. CDBG public hearing July 14 at 9 AM (6 DAYS). City Manager budget July 16 (8 DAYS) — FY2027 budget at $6.3B with $33M deficit. Triple-digit heat driving cooling center demand for unhoused residents. Council returns July 23 (15 DAYS).")
    print("  Updated: hso-strategic-plan")

c = find_campaign(safe, campaign_id="shelter-capacity-outcomes")
if c:
    append_to_summary(c, "\n\n**July 7 update:** SAHNC vote July 23 (16 DAYS) — Sunrise named tentative operator. AT-Home Initiative ($6.7M, 5-year) contract awards expected September. Endeavors emergency shelter contract through September; competitive solicitation October 1. HSO expanding to 6 HEM teams (42 staff). City Manager budget July 16 (9 DAYS). Council returns July 23 (16 DAYS).\n\n**July 8 update:** SAHNC operator vote (Sunrise) July 23 (15 DAYS). SAHNC opening delayed to June 2027 — construction at 2401 S. I-35 through spring 2027. AT-Home Initiative ($6.7M, 5-year) contract awards expected September. Endeavors emergency shelter contract through September; competitive solicitation October 1. Marshalling Yard exit rate still 30%. City Manager budget July 16 (8 DAYS). Council returns July 23 (15 DAYS).")
    print("  Updated: shelter-capacity-outcomes")

c = find_campaign(safe, campaign_id="apd-staffing-response")
if c:
    append_to_summary(c, "\n\n**July 8 update:** ⚡ STAFFING CLARIFICATION: KXAN (June 3) reports APD has ~1,484 sworn officers out of 1,812 authorized — approximately 330 open positions (18% vacancy rate). APA President Bullock's '700 short' figure accounts for population growth beyond current authorized levels. Net +3 officers last year — first positive year in recent memory. 157th cadet class (65 cadets, started January 26) on track for September 18 graduation. $3.7M recruitment budget (highest in 5 years); applications up 166%. Chief Davis: full staffing by end of 2027. City auditor: APD has no formal long-term recruitment plan. Proposed FY2027 APD budget: $544M ($26M increase). City Manager budget July 16 (8 DAYS). Council returns July 23 (15 DAYS).")
    print("  Updated: apd-staffing-response")

c = find_campaign(safe, campaign_id="heal-initiative-transparency")
if c:
    append_to_summary(c, "\n\n**July 7 update:** HEAL teams continue 5 days/week operations with 42 staff across 6 HEM teams. AT-Home Initiative ($6.7M, 5-year) contracts expected September — designed to address shelter-to-housing pipeline. SAHNC vote July 23 (16 DAYS). CDBG hearing July 14 (7 DAYS). City Manager budget July 16 (9 DAYS). Council returns July 23 (16 DAYS).\n\n**July 8 update:** HEAL teams continue 5 days/week operations with 42 staff across 6 HEM teams. AT-Home Initiative ($6.7M, 5-year) contracts expected September — designed to address the shelter-to-permanent-housing pipeline. SAHNC operator vote (Sunrise) July 23 (15 DAYS). CDBG hearing July 14 (6 DAYS). City Manager budget July 16 (8 DAYS). Council returns July 23 (15 DAYS).")
    print("  Updated: heal-initiative-transparency")

save_json(ORGS_DIR / "austin-safe-and-sound.json", safe)


# ============================================================
# OC HOUSING NOW
# ============================================================
print("\n=== OC Housing Now ===")
oc_housing = load_json(ORGS_DIR / "oc-housing-now.json")

c = find_campaign(oc_housing, campaign_id="orange-housing-element")
if c:
    append_to_summary(c, "\n\n**July 8 update:** ⚡ NEW COURT RULING: San Diego County Superior Court dismissed Huntington Beach's latest lawsuit against the state on June 30 (reported July 7 by HeySoCal). Judge Katherine Bacal granted AG Bonta's anti-SLAPP motion, rejecting HB's argument that state Housing Element Law and CEQA are incompatible. Governor Newsom: 'In ruling after ruling, the City of Huntington Beach has lost.' ⚡ PENALTY ESCALATION: Fines now $50,000/month since June 2026 (up from $10K/month Jan-May). AG seeking $100,000/month from July 1. After 3 months of continued non-compliance, fines can triple; further non-compliance triggers 6x multiplier and potential court-appointed receiver. ⚡ HB adopted a housing element update June 16 — HCD review pending; 120 days to complete required zoning changes. Hearing July 17 (9 DAYS). State primary certification July 10 (2 DAYS). ⚡ OC BUDGET CRISIS: Voice of OC (July 7) reports cascading municipal deficits — City of Orange faces $20M deficit and has placed a 1% sales tax increase on the November ballot ($37M/year over 13 years). Voters rejected a 0.5% increase in 2024. City of Orange housing element remains in compliance with HCD (certified January 2024).")
    print("  Updated: orange-housing-element")

c = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if c:
    append_to_summary(c, "\n\n**July 8 update:** Irvine 2045 General Plan adopted August 2024 — ongoing zoning amendments to implement. ⚡ Oak Creek: Irvine Company revised plan to include 50+ acre public nature park, reducing units to under 3,000 (from 3,100). Planning Commission voted 7-0 (March 19) to recommend; Council approved zoning amendment April 14 for the nature park option. Full Council vote on the development has not occurred — Council could approve or place on November 2026 ballot. The 1988 voter-approved open space designation remains the central legal debate. ⚡ Irvine faces $6M current deficit, projected $47M by 2030 (Voice of OC, July 7). State primary certification July 10 (2 DAYS).")
    print("  Updated: irvine-general-plan")

c = find_campaign(oc_housing, campaign_id="rhna-compliance-tracking")
if c:
    append_to_summary(c, "\n\n**July 8 update:** ⚡ SIGNIFICANT LEGAL DEVELOPMENT: Court of Appeal ruled that zoning overlays alone do not satisfy RHNA obligations — cities must actually rezone, not just create overlay zones. This could reopen builder's remedy exposure for cities statewide that relied on overlays for compliance. 7th cycle timeline: HCD must provide regional housing need determination to SCAG by October 2026, with draft methodology through early 2028. OC now qualifies as 'urban transit county' under SB 79, triggering new transit-oriented development requirements. State primary certification July 10 (2 DAYS).")
    print("  Updated: rhna-compliance-tracking")

c = find_campaign(oc_housing, campaign_id="builders-remedy-awareness")
if c:
    append_to_summary(c, "\n\n**July 8 update:** ⚡ LANDMARK RULING: Cedar Street won the first successful builder's remedy case in California Superior Court (La Canada Flintridge, 80-unit project at 600 Foothill Blvd). AG Bonta attached this decision to a legal alert sent to all 539 jurisdictions statewide. AB 1893 (effective Jan 1, 2025) formalized builder's remedy as an entitlement pathway under the Housing Accountability Act. ⚡ OC activity: La Habra accepted a Lennar builder's remedy application for 530 homes on the Westridge golf course, requiring environmental review. Newport Beach residents debating whether to reduce housing element unit count (8,000+ units by 2030), which could re-expose the city. ⚡ The Court of Appeal overlay ruling significantly expands builder's remedy exposure for cities relying on that compliance strategy. State primary certification July 10 (2 DAYS).")
    print("  Updated: builders-remedy-awareness")

save_json(ORGS_DIR / "oc-housing-now.json", oc_housing)


# ============================================================
# OC PURPLE ACCOUNTABILITY
# ============================================================
print("\n=== OC Purple Accountability ===")
oc_purple = load_json(ORGS_DIR / "oc-purple-accountability.json")

c = find_campaign(oc_purple, campaign_id="bos-majority-defense")
if c:
    append_to_summary(c, "\n\n**July 8 update:** ⚡ State primary certification deadline July 10 (2 DAYS) — Secretary of State must certify final tallies. D5: Katrina Foley (D) 46.98% vs Diane Dixon (R) 46.81% — razor-thin 0.17-point margin; November runoff all but guaranteed. D4: Connor Traut (D) 33%+ vs Tim Shaw (R) 31%+ — both advance to November. Key endorsements: Traut has OC Democratic Party, Supervisors Chaffee/Foley/Sarmiento, Buena Park Police Association. Shaw has Rep. Young Kim, OC Republican Party, National Association of Realtors ($125K+ in independent expenditures). D2: Supervisor Sarmiento (D) appears positioned for reelection with 60%+ support. ⚡ OCEA labor negotiations: fourth bargaining session July 1 — union's chief spokesperson called it 'borderline bad faith bargaining.' County's initial proposal (June 17) called 'insulting' and 'tone deaf.' OCEA argues county has funds — General Fund reserves $204M above target. No strike vote or impasse declaration yet. ⚡ OC budget crisis: Voice of OC (July 7) reports county $75M structural deficit, $400M+ Airport Fire liability ($9.5M settled, CalFire $32M lawsuit), only $35M insurance coverage. Multiple city deficits: Anaheim $60M+, Santa Ana $13M, Orange $20M, HB $15.6M, Fullerton $14M, Irvine $6M/$47M projected.")
    print("  Updated: bos-majority-defense")

c = find_campaign(oc_purple, campaign_id="orange-council-scorecard")
if c:
    append_to_summary(c, "\n\n**July 8 update:** ⚡ City of Orange faces $20M budget deficit — placed 1% sales tax increase on November ballot (expected to generate $37M/year over 13 years). Voters rejected a 0.5% increase in 2024. State primary certification July 10 (2 DAYS). Council fiscal management is a key scorecard metric as the city weighs tax increases against service cuts.")
    print("  Updated: orange-council-scorecard")

c = find_campaign(oc_purple, campaign_id="irvine-council-scorecard")
if c:
    append_to_summary(c, "\n\n**July 8 update:** Irvine faces $6M current deficit, projected $47M by 2030 (Voice of OC, July 7). Oak Creek development revised: 50+ acre nature park, under 3,000 units (down from 3,100). Full Council vote pending — could approve or place on November 2026 ballot. State primary certification July 10 (2 DAYS).")
    print("  Updated: irvine-council-scorecard")

c = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if c:
    append_to_summary(c, "\n\n**July 8 update:** ⚡ HB court loss #9: San Diego court dismissed HB's latest lawsuit June 30 — anti-SLAPP granted. AG Bonta's penalty escalation continues: $50K/month since June, seeking $100K/month from July 1. HB adopted housing element June 16 — HCD review pending. ⚡ Court of Appeal ruled zoning overlays insufficient for RHNA compliance — expands builder's remedy statewide. Cedar Street won first successful builder's remedy case (La Canada Flintridge). AB 1893 formalized builder's remedy pathway. Governor Newsom issued final warning to 15 jurisdictions in March 2026. State primary certification July 10 (2 DAYS).")
    print("  Updated: state-legislative-tracking")

save_json(ORGS_DIR / "oc-purple-accountability.json", oc_purple)


# ============================================================
# OC ABUNDANCE PROJECT
# ============================================================
print("\n=== OC Abundance Project ===")
oc_abundance = load_json(ORGS_DIR / "oc-abundance-project.json")

c = find_campaign(oc_abundance, campaign_id="oc-childcare-desert-mapping")
if c:
    append_to_summary(c, "\n\n**July 8 update:** ⚡ OC budget crisis compounds childcare challenges — county faces $75M structural deficit, $400M+ Airport Fire liability (Voice of OC, July 7). Multiple OC cities face budget deficits that could impact local childcare programs: Anaheim $60M+, Santa Ana $13M, Orange $20M, Fullerton $14M. ⚡ GKN Aerospace cleanup: Phase 1 began June 30 in Garden Grove — 50,000 residents were evacuated from 6 cities in May. FBI investigation underway (evidence seized June 10). Regulatory gaps exposed. Cleanup impacts childcare access in affected neighborhoods. State primary certification July 10 (2 DAYS).")
    print("  Updated: oc-childcare-desert-mapping")

c = find_campaign(oc_abundance, campaign_id="oc-employer-index")
if c:
    append_to_summary(c, "\n\n**July 8 update:** Campaign in planning phase. ⚡ OCEA labor negotiations ongoing — fourth bargaining session July 1 described as 'borderline bad faith.' County's initial proposal called 'insulting.' OCEA argues county has $204M in reserves above target. Public sector employer landscape under pressure from OC-wide budget deficits. State primary certification July 10 (2 DAYS).")
    print("  Updated: oc-employer-index")

c = find_campaign(oc_abundance, campaign_id="oc-family-housing")
if c:
    append_to_summary(c, "\n\n**July 8 update:** ⚡ Oak Creek (Irvine): revised to include 50+ acre public nature park, reducing units to under 3,000. Planning Commission voted 7-0 (March 19); Council approved zoning amendment April 14. Full Council vote pending — could approve or place on November 2026 ballot. ⚡ OC housing costs remain among nation's highest ($1.2M-$1.6M median). Court of Appeal ruled zoning overlays insufficient for RHNA — could increase housing production pressure on OC cities. State primary certification July 10 (2 DAYS).")
    print("  Updated: oc-family-housing")

save_json(ORGS_DIR / "oc-abundance-project.json", oc_abundance)


# ============================================================
# UPDATE FRESHNESS METADATA
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-07-08T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_key in ["austin-78702", "orange-92868"]:
    if loc_key in freshness.get("locations", {}):
        freshness["locations"][loc_key]["issues_scraped"] = "2026-07-08T12:00:00Z"
        freshness["locations"][loc_key]["issues_scored"] = "2026-07-08T12:00:00Z"

for profile_key in freshness.get("profiles", {}):
    freshness["profiles"][profile_key]["issues_scraped"] = "2026-07-08T12:00:00Z"
    freshness["profiles"][profile_key]["issues_scored"] = "2026-07-08T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\nAll July 8 updates complete.")
