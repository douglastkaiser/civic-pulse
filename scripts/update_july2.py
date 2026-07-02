#!/usr/bin/env python3
"""
July 2, 2026 updates for all issue and organization data files.
Key developments since July 1:
  - Austin: Environmental Commission completed Dog's Head review July 1 — Commissioner Shea raised "trust me" concerns about Project Toaster
  - Austin: Austin Energy signed 40MW residential battery storage deal with Base Power
  - Austin: 109-degree day caused substation trip, 15K customers lost power; ERCOT warns 12% rolling blackout chance in August
  - Austin: 208 affordable units broke ground (Bailey at Berkman + Bailey at Stassney)
  - Austin: Council recess continues (returns July 23, 21 DAYS); City Manager budget July 16 (14 DAYS)
  - OC: GKN Phase 1 cleanup FINAL DAY today (July 2) — removal of neutralized MMA completing
  - OC: Governor county certification deadline TOMORROW (July 3); state certification July 10 (8 DAYS)
  - OC: AG HB penalties Day 2 at escalated rate ($150K/month)
  - Brooklyn: CORRECTION — NYC FY2027 budget is $125.8B (not $115.9B FY2026); $300M housing vouchers, Fair Fares expansion
  - Brooklyn: Monitor Point must return to CPC for scope approval before full Council vote
  - Brooklyn: South of Prospect Plan community walkshop held in June; zoning concept map expected later 2026
  - Madison: Extreme Heat Warning EXTENDED through July 2 10PM; heat dome affecting 250M+ Americans
  - Madison: UW-Madison correction — 34 buildings affected (23 fully closed, 11 partially); ~30 temporary chillers being installed
  - Madison: Board of Regents had approved $6M for chilled water repairs on June 4 — 26 days before failure
  - Cambridge: AHO — developers warn CDD changes could reduce housing production ~50% on some lots
  - Cambridge: Doug Brown petition could temporarily become de facto law under MA law until Council votes
  - Brookline: Heat emergency continues through July 4; temps forecast ~100°F, heat index 100-110°F
  - Brookline: Chestnut Hill — Town Meeting approved overlay 217-20 May 28; 783 units + 200-room hotel; groundbreaking spring 2028
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
austin["last_scraped"] = "2026-07-02T12:00:00Z"

# Dog's Head
idx, issue = find_issue(austin["issues"], "atx-dogs-head-annexation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Environmental Commission completed Dog's Head review July 1 — heard nearly 4 hours of public comment opposing the project on ecological grounds. Commissioner Brigid Shea publicly skeptical, citing 'a whole lot of trust me' from Endeavor Real Estate and insufficient detail about the mysterious 300-acre 'Project Toaster' tenant (undisclosed Fortune 100 company). Key concerns: Colorado River discharge impacts, environmental degradation, Tesla's past tax incentive noncompliance as cautionary precedent. Draft TIRZ plan expected after July 4 weekend. Travis County TIRZ vote July 14 (12 DAYS). City Council adoption vote July 23 (21 DAYS). 2,600 acres; 12,000+ homes; projected $3.5B property tax revenue over 30 years.")
    print("  Updated atx-dogs-head-annexation")

# Golf course (also references Environmental Commission)
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Environmental Commission completed Dog's Head review July 1 with significant skepticism. Travis County TIRZ vote July 14 (12 DAYS). Council vote July 23 (21 DAYS). Council on recess until July 23 (21 DAYS).")
    print("  Updated atx-golf-course-rezone")

# Gas peaker plant + energy
idx, issue = find_issue(austin["issues"], "atx-gas-peaker-plant")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** ⚡ Austin Energy signed deal with Base Power for 40 MW of residential battery storage — dispatchable peak demand resources plus homeowner backup power. Contrasts with the $1B gas peaker approach. Austin Energy now over 70% carbon-free (vs 46% statewide, 42% nationally). Recent 109°F day caused substation equipment trip, knocking out power to ~15,000 customers (local equipment issue, not ERCOT grid). ERCOT warns 12% chance of rolling blackouts in August. New Kramer Substation energized in North Austin to add capacity. Council on recess until July 23 (21 DAYS).")
    print("  Updated atx-gas-peaker-plant")

# HSO / homelessness
idx, issue = find_issue(austin["issues"], "atx-hso-plan-adopted")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** ⚡ City broke ground on 208 affordable housing units — Bailey at Berkman (104 units, D3) and Bailey at Stassney (104 units, D4), including dedicated permanent supportive housing and veterans' units. SAHNC opening June 2027; Sunrise operator vote July 23 (21 DAYS). City Manager budget July 16 (14 DAYS). Council on recess until July 23 (21 DAYS).")
    print("  Updated atx-hso-plan-adopted")

# AISD
idx, issue = find_issue(austin["issues"], "atx-aisd-budget-crisis")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** AISD Police Chief Wayne Sneed released from hospital after ~4 weeks following motorcycle crash. Bus service changes announced for 2026-27 school year. District lost 3,000+ students last year; deficit estimated at $95M-$181M. Superintendent Segura says rubric for potential additional closures will be shared this fall. Phase 1 boundary draft changes expected August 7 (36 DAYS); board vote September. Phase 2 pushed to 2028-29. City Manager budget July 16 (14 DAYS).")
    print("  Updated atx-aisd-budget-crisis")

# D1 Election
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Additional candidate detail: Kyra Lorena Rogers (small business owner, Sweepz Cleaning Service) and Misael Daguan Ramos (ran in 2022, placed 2nd with 25.3%) also declared. Across all 5 open seats (D1, D3, D5, D7, D9), 20 people have appointed treasurers. Filing opens July 20 (18 DAYS); deadline August 17. Election Day November 3. Council on recess until July 23 (21 DAYS).")
    print("  Updated atx-d1-election")

# Bond
idx, issue = find_issue(austin["issues"], "atx-2026-bond")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Bond breakdown clarification: ~$250M for parks and trails (largest share), remainder for transportation and community facilities. Austin Parks Foundation notes 'summer standstill' as bond awaits formal council action. Staff Alternative Scenario is roughly half the original task force recommendation of $750M. Final vote to place on November ballot: July 23 (21 DAYS). City Manager budget July 16 (14 DAYS).")
    print("  Updated atx-2026-bond")

# Density bonus
idx, issue = find_issue(austin["issues"], "atx-density-bonus-approved")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** DBC detail: 5 combining districts with height tiers from no additional height to up to 60 ft additional. For-sale projects: 10% affordable at 80% MFI; rental: 10% at 50% MFI, no fee-in-lieu. No new DB90 or VMU rezoning applications being accepted. DBC still zero applications. ⚡ 208 affordable units broke ground (Bailey at Berkman + Bailey at Stassney). Council on recess until July 23 (21 DAYS).")
    print("  Updated atx-density-bonus-approved")

# Project Connect
idx, issue = find_issue(austin["issues"], "atx-project-connect-legal-update")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Federal funding uncertainty: Trump administration has not agreed to fund any new transit projects. Sen. Cornyn publicly opposes federal funding for Austin rail. ATP expects some construction activities to begin 2027; major solicitations for final design and construction teams underway 2026. Legal threat heading to Texas Supreme Court — challenge to whether city's property tax hike to fund transit is legal. AG jurisdictional plea ruling still pending from Judge Shepperd. Council on recess until July 23 (21 DAYS).")
    print("  Updated atx-project-connect-legal-update")

# APD
idx, issue = find_issue(austin["issues"], "atx-apd-staffing-audit")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** City auditor report found APD 'does not have an effective strategy' to recruit and fully staff the department. No formal recruitment plan established despite Chief Davis calling it a 'big priority.' Violent crime rate ~370 per 100,000 (slightly above national average of 359). City Manager budget July 16 (14 DAYS). Council on recess until July 23 (21 DAYS).")
    print("  Updated atx-apd-staffing-audit")

# Convention center
idx, issue = find_issue(austin["issues"], "atx-convention-center")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Total project cost: $1.6B (up from previously stated $1.35B in bonds). Expansion will produce over 1 million total sq ft. SXSW and other events using alternative venues through 2028. Planned as world's first zero-carbon certified convention center, running on 100% renewable energy. Excavation continues through 2026; completion target spring 2029. Council on recess until July 23 (21 DAYS).")
    print("  Updated atx-convention-center")

# Childcare
idx, issue = find_issue(austin["issues"], "tc-childcare-funding")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Travis County Commissioners Court approved $17.65M in contracts to expand child care and after-school programs. Described as fastest implementation of any initiative of its kind in the country and first of its kind in Texas. Cleared families waitlisted since 2023; expanded after-school/summer services to 3,000 children. 150 childcare centers funded so far. City Manager budget July 16 (14 DAYS).")
    print("  Updated tc-childcare-funding")

# Development rules
idx, issue = find_issue(austin["issues"], "atx-development-rules-overhaul")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** DBC: 5 combining districts, zero applications in first month. 208 affordable units broke ground. Austin Energy signed 40MW residential battery storage deal. Council on recess until July 23 (21 DAYS).")
    print("  Updated atx-development-rules-overhaul")

save_json(ISSUES_DIR / "austin-78702.json", austin)

# ============================================================
# ISSUES — ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(ISSUES_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-07-02T12:00:00Z"

# Garden Grove / GKN
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**July 2 update:** ⚡ GKN Phase 1 cleanup FINAL DAY — removal of neutralized MMA from tanks #2 and #4 completing today. Original crisis began May 21 — 42 days ago. Crews confirmed MMA concentrations 'well below levels associated with health concerns.' Air quality monitoring available online through OC Health Care Agency. 44+ lawsuits filed. Three criminal investigations ongoing (FBI/EPA federal probe, OC DA Spitzer, Cal/OSHA). Phase 2 details not yet released. Governor county certification TOMORROW (July 3). State certification July 10 (8 DAYS).")
    print("  Updated Garden Grove chemical crisis")

# D5
idx, issue = find_issue(oc["issues"], "oc-bos-district-5-defense")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Foley backed by county employee unions (OC Professional Firefighters Local 3631, OCEA, AOCDS) which collectively spent $565K+ advertising her candidacy. Dixon endorsed by OC Republican Party; Lincoln Club spent $38K+ supporting Dixon and $163K+ opposing Foley. Considered one of OC's most competitive races — Foley is the only Democrat on the Board. Governor county certification TOMORROW (July 3). State certification July 10 (8 DAYS). AG HB penalties Day 2 at $150K/month. BOS cancelled through August.")
    print("  Updated oc-bos-district-5-defense")

# D4
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Shaw endorsed by Rep. Young Kim, OC Republican Party, State Sens. Choi and Strickland. Traut endorsed by Supervisors Chaffee, Foley, and Sarmiento, OC Democratic Party, Buena Park Police Association. District encompasses Fullerton, Buena Park, La Habra, Brea, Placentia, Stanton, and portions of Anaheim. GKN Phase 1 cleanup completing today. Governor certification TOMORROW (July 3). BOS cancelled through August.")
    print("  Updated oc-bos-district-4-open-seat")

# HB housing element
idx, issue = find_issue(oc["issues"], "oc-newsom-housing-warning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** AG penalties Day 2 at escalated rate ($150K/month). HB projects hotel conversions, ADUs, and site rezoning could yield 5,497 of 5,845 required units by cycle's end — but only 1,187 permitted so far. Council unanimously postponed voting on updated general plan changes at June 2 meeting, citing insufficient review time for 1,000+ page document. Governor county certification TOMORROW (July 3). State certification July 10 (8 DAYS). 120-day zoning deadline ~October 14.")
    print("  Updated oc-newsom-housing-warning (HB)")

# Governor
idx, issue = find_issue(oc["issues"], "ca-governor-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Becerra ~28%, Hilton ~25% with 88% of expected votes tallied one week post-election. Hilton enters November as significant underdog — registered Democrats outnumber Republicans nearly 2-to-1 in CA; state hasn't elected Republican governor in 20 years. Governor county certification TOMORROW (July 3). State certification July 10 (8 DAYS).")
    print("  Updated ca-governor-2026")

# OC FY2027 Budget
idx, issue = find_issue(oc["issues"], "oc-fy2027-budget")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** County faces $75M structural deficit; tapping reserves for 4th consecutive year. Context on supervisor raises: Chaffee and Sarmiento donated their 25% raises to charity after backlash; Wagner, Nguyen, and Foley retained theirs. Teamsters Local 952 contract expired June 25. County also faces estimated $400M liability from Airport Fire. Interim CEO Roestenberg in role ($430K, indefinite term). BOS cancelled through August. AG HB penalties Day 2 at $150K/month.")
    print("  Updated oc-fy2027-budget")

# OC Streetcar
idx, issue = find_issue(oc["issues"], "oc-streetcar-launch")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Project 95% complete per OCTA CEO Darrell Johnson. Current testing phase covers platform operations, control systems, and street signal interface. Six of eight Siemens S700 vehicles will be in operation at any time. Revenue service March 2027. 4.15-mile, 10-stop route. Governor county certification TOMORROW (July 3).")
    print("  Updated oc-streetcar-launch")

# Homelessness Grand Jury
idx, issue = find_issue(oc["issues"], "oc-homelessness-grand-jury")
if issue:
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**July 2 update:** Grand Jury report found despite spending a billion dollars, the county is 'in largely the same position.' Response deadline passed June 30 — still no public reporting on county or city responses. Supervisor Chaffee highlighted pilot prevention programs; supervisors debated that lack of affordable housing creates 'homeless deadlock.' BOS cancelled through August — governance gap continues. GKN Phase 1 completing today.")
    print("  Updated OC Homelessness Grand Jury")

# Supportive Housing NOFA
idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa-2026")
if not issue:
    idx, issue = find_issue(oc["issues"], "oc-supportive-housing-nofa")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** NOFA includes HOME, HOME-ARP, MHSA/BHSA, 15G Reserves, and Housing Successor Agency federal funds. Small-scale housing eligible per Commission to End Homelessness report (received by Board January 28, 2025). NOFA open until closed, replaced, or all funds committed. Governor certification TOMORROW (July 3). State certification July 10 (8 DAYS).")
    print("  Updated oc-supportive-housing-nofa")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** District covers most of Santa Ana, Anaheim, Placentia, Fullerton, Buena Park, La Habra, west Orange, and South Whittier (LA County). Seat vacated by termed-out State Sen. Tom Umberg (D-Santa Ana). Governor county certification TOMORROW (July 3). State certification July 10 (8 DAYS).")
    print("  Updated oc-state-senate-sd34")

# Homelessness Enforcement
idx, issue = find_issue(oc["issues"], "oc-homelessness-enforcement-post-grants-pass")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Grand Jury report: county spent a billion dollars but 'in largely the same position.' Supervisors debated 'homeless deadlock' from lack of affordable housing. GKN Phase 1 completing today. Governor certification TOMORROW (July 3). BOS cancelled through August.")
    print("  Updated oc-homelessness-enforcement")

save_json(ISSUES_DIR / "orange-92868.json", oc)

# ============================================================
# ISSUES — BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(ISSUES_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-07-02T12:00:00Z"

idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** ⚡ CORRECTION: NYC adopted $125.8B FY2027 budget on June 30 (not $115.9B FY2026 as previously noted) — largest in Council history, passed 45-6. Key provisions: $300M housing vouchers across FY27-FY28 reaching ~30,000 additional New Yorkers facing eviction/homelessness; Fair Fares expansion to 200% federal poverty level (up from 150%), adding 340,000 eligible New Yorkers for half-price transit; $350M additional reserves. Monitor Point must return to City Planning Commission for scope approval before full Council vote — specific vote date not yet confirmed. South of Prospect Plan: community engagement 'walkshop' held in June; zoning concept map expected later 2026. First neighborhood plan to account for planned IBX light rail.")
    print("  Updated nyc-atlantic-ave-rezoning")

# City of Yes
idx, issue = find_issue(brooklyn["issues"], "nyc-city-of-yes-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** ⚡ CORRECTION: NYC FY2027 budget is $125.8B (adopted June 30, 2026), not $115.9B FY2026. Includes $300M for housing vouchers, Fair Fares expansion to 200% FPL. Monitor Point must return to CPC for scope approval before full Council vote. Council-modified City of Yes expected to produce ~25% fewer units than original proposal due to carve-outs for single-family areas and parking. ADUs now legal across all five boroughs. IBX Draft EIS expected fall 2026; MTA completed 6 public meetings through May 2026. South of Prospect: first neighborhood plan accounting for IBX; zoning concept map expected later 2026.")
    print("  Updated nyc-city-of-yes-implementation")

save_json(ISSUES_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# ISSUES — MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(ISSUES_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-07-02T12:00:00Z"

idx, issue = find_issue(madison["issues"], "budget-rules-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** ⚡ Extreme Heat Warning EXTENDED through July 2 10PM (originally through July 1 7PM). Heat dome affecting 250M+ Americans heading into July 4 weekend. ⚡ UW-Madison CORRECTION: 34 buildings affected total (23 fully closed including Bascom Hall, Science Hall, Grainger Hall; 11 partially open) — not 23 as previously reported. Chilled water line from Charter Street Heating Plant broke June 17, releasing ~40,000 gallons of lake water. ~30 temporary chillers being installed across campus. ⚡ Board of Regents had approved nearly $6M for chilled water infrastructure repairs on June 4 — just 26 days before the AC failure. Repairs still expected to take at least one month. Christine Knapp confirmed as new Madison Water Utility General Manager (appointed June 25; starts August 31 pending Council approval). Budget shortfall projection growing: expenditures expected to exceed state ERIP limit by $7.2M; structural deficit expected to grow $6-7M annually. Next council meetings: July 7, July 21.")
    print("  Updated budget-rules-2026")

save_json(ISSUES_DIR / "madison-wi.json", madison)

# ============================================================
# ISSUES — CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(ISSUES_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-07-02T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-zoning-reform-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** ⚡ AHO impact warning: developers warn CDD's recommended changes could reduce housing production by ~50% on some lots. Councilors Zusy and Flaherty proposed separate amendments revisiting open space, setback, and parking requirements. ⚡ Doug Brown citizen petition (filed June 3, 13 signatures): under MA state law, the petition temporarily becomes de facto municipal law until Council votes on it — creating potential roadblocks for affordable projects in the interim. Petition would cut max heights from 9 to 6 stories and block inclusionary projects from building to 6 stories unless adjacent properties are 3+ stories. Council cannot vote until August 3. Harvard Crimson editorial: 'Stop Backtracking on Housing.' Cambridge Schools adopted $290M FY27 budget (~5% increase). Cambridge Police FY27 budget: $57M (~$1.5M increase).")
    print("  Updated cam-zoning-reform-implementation")

save_json(ISSUES_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# ISSUES — BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(ISSUES_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-07-02T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** Heat emergency continues through July 4 — temps forecast ~100°F, heat index 100-110°F. Cooling centers open; Eversource discounts available for qualifying customers. Override context: without it, ~240 FTE positions would have been eliminated. Tax override turnout was 34% — record for a local election. FY2027 budget mostly maintains existing services though some smaller cuts remain.")
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**July 2 update:** ⚡ Chestnut Hill overlay detail: Town Meeting approved 217-20 on May 28 (well above two-thirds threshold). Developer City Realty (acquired site for $41M in May 2024). Three buildings: 14, 12, and 7 stories. 783 multifamily units (25% affordable under Chapter 40B), 200-room hotel, medical offices, ground-floor retail. Over 50% commercial use. Projected $4-6M annual net revenue for Brookline. Groundbreaking spring 2028 at earliest. MBTA compliance: rezoning plan along Harvard Street approved 207-33. Must designate 41+ acres allowing multifamily by right with theoretical capacity of 6,990 units. Heat emergency continues through July 4.")
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
        "\n\n**July 2 update:** D5 spending: Foley backed by county employee unions ($565K+ in ads); Lincoln Club spent $38K+ for Dixon, $163K+ opposing Foley. D4 endorsements: Shaw has Rep. Young Kim, OC GOP; Traut has Supervisors Chaffee/Foley/Sarmiento, OC Dems. County faces $75M structural deficit + $400M Airport Fire liability. GKN Phase 1 completing today. Governor certification TOMORROW (July 3). AG HB penalties Day 2 at $150K/month. BOS cancelled through August."
    )
    print("  Updated bos-majority-defense")

campaign = find_campaign(oc_purple, campaign_id="state-legislative-tracking")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 2 update:** Becerra ~28%, Hilton ~25% (88% counted); Hilton significant underdog — CA hasn't elected Republican governor in 20 years. SD-34 district covers Santa Ana, Anaheim, Placentia, Fullerton, Buena Park, La Habra, west Orange, South Whittier. Governor county certification TOMORROW (July 3). State certification July 10 (8 DAYS)."
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
        "\n\n**July 2 update:** AG penalties Day 2 at escalated rate ($150K/month). HB projects hotel conversions, ADUs, and rezoning could yield 5,497 of 5,845 required units by cycle's end — but only 1,187 permitted so far. Council postponed voting on updated general plan changes citing insufficient review time for 1,000+ page document. Governor certification TOMORROW (July 3). State certification July 10 (8 DAYS). 120-day zoning deadline ~October 14."
    )
    print("  Updated orange-housing-element")

campaign = find_campaign(oc_housing, campaign_id="irvine-general-plan")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 2 update:** GKN Phase 1 cleanup completing today (final day). FBI/EPA federal investigation ongoing. Phase 2 details not yet released. County faces $75M structural deficit + $400M Airport Fire liability. Governor certification TOMORROW (July 3). BOS cancelled through August."
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
        "\n\n**July 2 update:** GKN Phase 1 completing today. County faces $75M structural deficit + $400M Airport Fire liability — impacts family services funding. Teamsters Local 952 contract expired June 25; negotiations ongoing. Grand Jury: county spent $1B on homelessness but 'in largely the same position.' Governor certification TOMORROW (July 3). BOS cancelled through August."
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
        "\n\n**July 2 update:** Additional D1 candidates: Kyra Lorena Rogers (small business owner) and Misael Daguan Ramos (ran 2022, placed 2nd at 25.3%). Across all 5 open seats (D1, D3, D5, D7, D9), 20 people have appointed treasurers. Filing opens July 20 (18 DAYS); deadline August 17. Bond final vote July 23 (21 DAYS). City Manager budget July 16 (14 DAYS). Election Day November 3."
    )
    print("  Updated council-elections-2026")

campaign = find_campaign(atx_yimby, campaign_id="defend-project-connect")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 2 update:** ⚡ Federal funding uncertainty: Trump administration has not agreed to fund any new transit projects. Sen. Cornyn publicly opposes federal funding for Austin rail. ATP expects construction activities to begin 2027. Legal challenge heading to Texas Supreme Court. ⚡ Austin Energy signed 40MW residential battery storage deal with Base Power. 109°F day caused substation trip (local issue, not ERCOT). ERCOT warns 12% rolling blackout chance in August. Council on recess until July 23 (21 DAYS)."
    )
    print("  Updated defend-project-connect")

campaign = find_campaign(atx_yimby, campaign_id="golf-course-rezone")
if not campaign:
    campaign = find_campaign(atx_yimby, keywords=["golf", "rezoning"])
if campaign:
    append_to_summary(campaign,
        "\n\n**July 2 update:** Environmental Commission completed review July 1 — Commissioner Shea skeptical of 'Project Toaster' and Endeavor's promises, citing Tesla tax incentive noncompliance as precedent. Nearly 4 hours of public comment opposing on ecological grounds. Draft TIRZ plan expected after July 4 weekend. Travis County TIRZ vote July 14 (12 DAYS); council vote July 23 (21 DAYS)."
    )
    print("  Updated golf-course-rezoning campaign")

campaign = find_campaign(atx_yimby, campaign_id="ongoing-housing-advocacy")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 2 update:** ⚡ 208 affordable units broke ground (Bailey at Berkman + Bailey at Stassney) — permanent supportive housing and veterans' units included. DBC detail: 5 combining districts, rental requires 10% at 50% MFI, no fee-in-lieu. Still zero DBC applications. Council on recess until July 23 (21 DAYS)."
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
        "\n\n**July 2 update:** ⚡ 208 affordable units broke ground (Bailey at Berkman + Bailey at Stassney) — includes dedicated permanent supportive housing and veterans' units. City expanded encampment cleanup strategy with new dedicated response teams (April 2026). SAHNC operator vote July 23 (21 DAYS). City Manager budget July 16 (14 DAYS)."
    )
    print("  Updated hso-strategic-plan")

campaign = find_campaign(atx_safe, campaign_id="apd-staffing-response")
if campaign:
    append_to_summary(campaign,
        "\n\n**July 2 update:** City auditor: APD 'does not have an effective strategy' to recruit — no formal recruitment plan established. Violent crime rate ~370 per 100,000 (slightly above national avg 359). ⚡ 109°F day caused substation trip, 15K customers lost power (local equipment issue). ERCOT warns 12% rolling blackout chance in August. City Manager budget July 16 (14 DAYS). Council on recess until July 23 (21 DAYS)."
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
        "\n\n**July 2 update:** Travis County Commissioners Court approved $17.65M in contracts to expand child care and after-school programs. Described as fastest implementation of its kind in the country, first in Texas. Cleared families waitlisted since 2023; expanded after-school/summer to 3,000 children; 150 childcare centers funded. City Manager budget July 16 (14 DAYS). Council on recess until July 23 (21 DAYS)."
    )
    print("  Updated childcare-desert-mapping")

campaign = find_campaign(atx_abundance, campaign_id="parental-leave-city-hall")
if not campaign:
    campaign = find_campaign(atx_abundance, keywords=["parental", "leave"])
if campaign:
    append_to_summary(campaign,
        "\n\n**July 2 update:** City Manager budget July 16 (14 DAYS). D1 filing opens July 20 (18 DAYS). Council on recess until July 23 (21 DAYS)."
    )
    print("  Updated parental-leave campaign")

save_json(ORGS_DIR / "austin-abundance-project.json", atx_abundance)

# ============================================================
# META — Freshness
# ============================================================
print("\n=== Updating freshness.json ===")
freshness = load_json(META_DIR / "freshness.json")
freshness["last_full_run"] = "2026-07-02T12:00:00Z"
freshness["last_run_status"] = "success"
freshness["last_run_errors"] = []

for loc_id in ["austin-78702", "orange-92868", "brooklyn-ny", "madison-wi", "cambridge-ma", "brookline-ma"]:
    if loc_id in freshness.get("locations", {}):
        freshness["locations"][loc_id]["issues_scraped"] = "2026-07-02T12:00:00Z"
        freshness["locations"][loc_id]["issues_scored"] = "2026-07-02T12:00:00Z"

for profile_id in freshness.get("profiles", {}):
    freshness["profiles"][profile_id]["issues_scraped"] = "2026-07-02T12:00:00Z"
    freshness["profiles"][profile_id]["issues_scored"] = "2026-07-02T12:00:00Z"

save_json(META_DIR / "freshness.json", freshness)

print("\n=== ALL FILES UPDATED ===")
