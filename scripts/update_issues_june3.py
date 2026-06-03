"""Update all issue data files with June 3, 2026 news."""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "public" / "data" / "issues"

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

def append_to_field(issue, field, text):
    if field in issue:
        issue[field] += text
    else:
        issue[field] = text

# ============================================================
# AUSTIN
# ============================================================
print("=== Updating austin-78702.json ===")
austin = load_json(DATA_DIR / "austin-78702.json")
austin["last_scraped"] = "2026-06-03T12:00:00Z"

# D1 Election update
idx, issue = find_issue(austin["issues"], "atx-d1-election")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** Council is now in summer recess — no meetings until July 23. The AISD FY27 budget proposal ($181M deficit) was published June 4 with the Board of Trustees final vote on June 18. 215 educator positions cut. Superintendent Segura is trying to close a ~$50M gap beyond the $130M already identified. Property sales could generate $45M. AISD teachers rallied at the Capitol on June 2 asking legislators to increase school funding — the state funding formula hasn't changed since 2019. The bond final vote is July 23 (50 DAYS). Filing period for council races opens July 20 (47 DAYS). Twenty candidates total across five open seats (D1, D3, D5, D8, D9). The DBC density bonus (approved May 22), bond direction ($390M, housing excluded), gas peaker plant oversight, and AISD fiscal crisis are the defining litmus tests.")
    append_to_field(issue, "why_it_matters_to_you",
        " ⚡ Council is in summer recess until July 23 — the gap between now and the filing period (July 20) is the critical window to evaluate candidates. The AISD budget crisis ($181M deficit, 215 educator cuts, board vote June 18) will be a central campaign issue. Watch for candidates' positions on school funding alongside housing, transit, and the bond.")
    print("  Updated atx-d1-election")

# Golf course rezone update
idx, issue = find_issue(austin["issues"], "atx-golf-course-rezone")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** Council in summer recess until July 23. The density bonus program (DBC) approved May 22 and the Dog's Head annexation (2,600 acres) approved the same day show strong council pro-development trajectory. Council also approved new development rules on May 26: minimum lot size reduced from 5,750 to 1,800 sq ft citywide — the most significant lot size change in 80 years. Missing middle zoning districts and new mixed-use zoning districts also created. These reforms complement the golf course rezoning opportunity.")
    print("  Updated atx-golf-course-rezone")

# Pct 4 runoff update (completed)
idx, issue = find_issue(austin["issues"], "tc-pct4-runoff")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** Morales transition underway. Raising Travis County childcare program scaling rapidly: nearly 300 kids have received scholarships, target 1,000 by October. $28M+ awarded including $17.34M to Workforce Solutions Capital Area for scholarships and $4.16M for quality improvements at 150 providers. Virtual town hall about the program June 16 at 6 PM. Additional $17M in childcare contracts coming before Commissioners Court. Morales's infrastructure-focused priorities (roads, CapMetro/Central Health coordination) align with county-level transit and housing investment.")
    issue["quadrant"] = "background"
    print("  Updated tc-pct4-runoff")

# Add new issue: AISD budget crisis
austin["issues"].append({
    "id": "atx-aisd-budget-crisis",
    "title": "AISD FY27 Budget Crisis — $181M Deficit, 215 Educator Cuts, Board Vote June 18",
    "governing_body": "Austin ISD Board of Trustees",
    "governing_body_type": "school_board",
    "meeting_date": "2026-06-18",
    "summary": "NEW (June 3, 2026): Austin ISD faces a $181 million deficit for FY2026-27, the district's worst fiscal crisis in decades. Superintendent Matias Segura has identified $130M in cuts but is still trying to close a ~$50M gap. 215 full-time educator positions are being cut (85 elementary, 51 middle, 79 high school), though some may be filled through attrition of open vacancies. The budget proposal was published June 4 with the Board of Trustees final vote scheduled for June 18.\n\nKey drivers: declining enrollment (district lost ~8,000 students since 2019), stagnant state funding formula (unchanged since 2019), and missed property sales. The district is exploring selling surplus properties which could generate ~$45M. Class sizes will increase for grades 2-5 and planning time will be cut for secondary teachers.\n\nAISD teachers rallied at the Texas Capitol on June 2, asking legislators to increase school funding. The state funding formula — the Basic Allotment — has not been adjusted since 2019, meaning districts absorb inflation without additional state support. This is a statewide structural problem, not just an AISD management issue.",
    "policy_domains": ["Public Education", "Taxation & Public Finance"],
    "decision_type": "vote",
    "geographic_scope": "district",
    "public_comment": {
        "available": True,
        "deadline": "2026-06-18",
        "instructions": "AISD Board of Trustees public hearing on the FY27 budget. Check austinisd.org/budget for hearing schedule and how to submit written testimony."
    },
    "estimated_contestedness": "high",
    "importance_score": 75,
    "impact_score": 55,
    "quadrant": "watch",
    "why_it_matters_to_you": "The AISD budget crisis is the backdrop for every November council race conversation. 215 educator cuts and larger class sizes will galvanize parents — a constituency that overlaps with both pro-housing and anti-development camps. The structural problem (state funding formula frozen since 2019) requires state-level advocacy, but the local symptom (budget cuts, school quality) becomes a campaign issue. Support increased housing production as a structural budget solution (more property tax revenue) while advocating for state funding reform. Board vote June 18."
})
print("  Added atx-aisd-budget-crisis")

# Add new issue: Development rules overhaul
austin["issues"].append({
    "id": "atx-development-rules-overhaul",
    "title": "Austin Approves Sweeping Development Rule Changes — Lot Size, Missing Middle, Mixed-Use",
    "governing_body": "Austin City Council",
    "governing_body_type": "city_council",
    "meeting_date": "2026-05-26",
    "summary": "NEW (June 3, 2026): In a landmark week for Austin housing policy, the City Council approved multiple development rule changes in late May:\n\n• Minimum Lot Size (May 26): Reduced from 5,750 sq ft to 1,800 sq ft citywide — the first change in over 80 years. Allows smaller, cheaper homes and enables more homes per block.\n\n• Density Bonus Program (May 22): Developers can build 15-60 feet taller in exchange for affordable housing units or community benefits (wider sidewalks, green space). Only CM Duchen voted against. Replaces the controversial DB90 program.\n\n• Missing Middle Zoning (May 2026): New zoning districts created for smaller housing types — townhomes, cottage courts, small multiplexes.\n\n• Mixed-Use Zoning (May 2026): New districts allowing commercial and residential development in tandem.\n\n• Dog's Head Annexation (May 22): 2,600-acre annexation approved with a 45-year development agreement. 20% of housing must be affordable.\n\nCombined with the HOME Initiative and Light Rail Transit Overlay (adopted May 16), Austin now has the most comprehensive pro-housing zoning framework of any major Texas city. Pew Research (March 2026) credited Austin's housing construction surge with driving down rents.",
    "policy_domains": ["Housing & Land Use", "Economic Development"],
    "decision_type": "vote",
    "geographic_scope": "citywide",
    "public_comment": {
        "available": False,
        "instructions": "Reforms adopted. Monitor implementation through permitting data. The DBC uptake rate will be the key indicator of whether zoning reform produces actual housing."
    },
    "estimated_contestedness": "medium",
    "importance_score": 92,
    "impact_score": 70,
    "quadrant": "act_now",
    "why_it_matters_to_you": "This is the YIMBY policy trifecta Austin has been building toward: HOME Initiative (housing by right) + Density Bonus (height for affordability) + Light Rail Overlay (transit-oriented density) + lot size reduction (enabling smaller homes). Pew Research credited Austin's construction surge with driving down rents. These reforms lock in the pro-building trajectory for years. The key now is implementation — monitor DBC uptake, track permitting timelines, and support the reforms against any rollback attempts from the next council."
})
print("  Added atx-development-rules-overhaul")

save_json(DATA_DIR / "austin-78702.json", austin)

# ============================================================
# MADISON
# ============================================================
print("\n=== Updating madison-wi.json ===")
madison = load_json(DATA_DIR / "madison-wi.json")
madison["last_scraped"] = "2026-06-03T12:00:00Z"

idx, issue = find_issue(madison["issues"], "mad-east-west-brt-construction")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** Route A continues 15-minute service. Legistar data shows CDD authorized to accept up to $50,000 in additional federal/state grants for community development (Resolution 92931, June 3). Federal funding for North-South Route B ($118M) remains at HIGH risk — no signed FTA agreement yet. City developing alternate strategies for scaled-back BRT improvements. BRT ridership up 18% since September 2022 launch. New council leadership — President Sabrina Madison (D17) and VP Carmella Glenn (D18) — in place.")
    print("  Updated mad-east-west-brt-construction")

idx, issue = find_issue(madison["issues"], "mad-new-housing-developments")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** Southwest and Southeast Area Plans heading toward June 23 Council adoption vote — 20 DAYS AWAY. Madison's Housing Forward Initiative continues — the mayor's zoning changes approved by the Common Council include: allowing duplexes/two-flats on most residentially zoned lots, 17-3 vote for more density near public transit, and unanimous approval for cottage courts. The Council voted to raise height limits near residential zones and reduce minimum lot areas. Polling shows 74%+ voter support for all zoning changes. The city needs ~2,000 new units annually to keep pace with population growth. New alders Ellen Zhang (D8) and Noah Lieberman (D14) now seated.")
    print("  Updated mad-new-housing-developments")

# Add police oversight debate
madison["issues"].append({
    "id": "mad-police-oversight-debate",
    "title": "Police Oversight Restrictions Debated — Independent Monitor Opposes Amendments",
    "governing_body": "Madison Common Council",
    "governing_body_type": "city_council",
    "meeting_date": None,
    "summary": "NEW (June 3, 2026): The Common Council considered amendments to the Office of the Independent Monitor that would require quarterly public reports and restrict when the office can use its own legal counsel. Interim Independent Police Monitor Aeiramique Glass fiercely opposed the restrictions, arguing they would undermine the office's independence. The debate reflects ongoing tension between police accountability advocates and some council members who want more oversight of the oversight body. New council leadership — President Sabrina Madison (D17) and VP Carmella Glenn (D18) — will shape how this debate unfolds.",
    "policy_domains": ["Public Safety", "Government Transparency", "Civil Rights & Social Equity"],
    "decision_type": "discussion",
    "geographic_scope": "citywide",
    "public_comment": {
        "available": True,
        "deadline": None,
        "instructions": "Monitor Common Council agenda at madison.legistar.com for hearing dates."
    },
    "estimated_contestedness": "high",
    "importance_score": 65,
    "impact_score": 40,
    "quadrant": "watch",
    "why_it_matters_to_you": "Police oversight is a defining issue for Madison's progressive identity. The tension between independent oversight and council control reflects broader questions about institutional design and accountability."
})
print("  Added mad-police-oversight-debate")

save_json(DATA_DIR / "madison-wi.json", madison)

# ============================================================
# BROOKLYN
# ============================================================
print("\n=== Updating brooklyn-ny.json ===")
brooklyn = load_json(DATA_DIR / "brooklyn-ny.json")
brooklyn["last_scraped"] = "2026-06-03T12:00:00Z"

idx, issue = find_issue(brooklyn["issues"], "nyc-atlantic-ave-rezoning")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** The South of Prospect Plan community engagement begins this summer — Mayor Mamdani's first major rezoning targeting McDonald Avenue and Coney Island Avenue corridors south of Prospect Park. City of Yes implementation showing results: 23% more housing permits in year one. Governor Hochul announced RFP for 300 new housing units on underutilized MTA land in Crown Heights — made possible by the AAMUP rezoning. An application for East 98th Street rezoning in East Flatbush (Community District 17) has a public scoping session scheduled for June 11 at 2:00 PM. The NYC June 23 primary election approaches — multiple Brooklyn council and state legislative seats on the ballot.")
    print("  Updated nyc-atlantic-ave-rezoning")

idx, issue = find_issue(brooklyn["issues"], "nyc-speaker-menin-priorities")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** The Council Advisory Group on Housing Affordability has been formed — co-chaired by Gary LaBarbera (Building Trades Council president), Barika Williams (ANHD executive director), and James Simmons III (Asland Capital Partners CEO). The advisory group will refine proposals to boost and preserve housing. The small lots reform targets 2,850 identified lots that could unlock up to 35,000 new homes including thousands of affordable units — all without costly rezonings. The Council hasn't set a legislative timeline and says it's in early talks with the Mamdani administration. Combined with the Block by Block housing plan ($22B capital) and SPEED reforms, the policy infrastructure for delivering at scale is being built.")
    print("  Updated nyc-speaker-menin-priorities")

# Add NYC June primary
brooklyn["issues"].append({
    "id": "nyc-june-primary-2026",
    "title": "NYC June 23 Primary Election — Brooklyn Council and State Races",
    "governing_body": "New York City Council / New York State Legislature",
    "governing_body_type": "city_council",
    "meeting_date": "2026-06-23",
    "summary": "NEW (June 3, 2026): The June 23 primary election includes multiple Brooklyn-area races. Key context: NYC's pro-housing policy trajectory — City of Yes, Atlantic Avenue rezoning (4,600 units), Block by Block ($22B housing plan), South of Prospect rezoning — depends on maintaining a pro-building council majority. Evaluate candidates on their positions regarding the small lots reform (35,000 potential units), NYCHA investment ($5.6B committed), and Construction Justice Act. The East 98th Street rezoning in East Flatbush and the Brownsville Neighborhood Community Plan are advancing, creating development-specific issues for Brooklyn district candidates to address.",
    "policy_domains": ["Housing & Land Use", "Government Transparency"],
    "decision_type": "election",
    "geographic_scope": "district",
    "public_comment": {
        "available": False,
        "instructions": "Check nycvotes.org/whats-on-the-ballot for your specific races. Primary is June 23."
    },
    "estimated_contestedness": "medium",
    "importance_score": 78,
    "impact_score": 65,
    "quadrant": "act_now",
    "why_it_matters_to_you": "The June 23 primary determines which candidates advance for Brooklyn council seats. With the City of Yes framework in place and Speaker Menin's small lots reform in development, the next council's composition will determine whether NYC's historic housing momentum continues or stalls."
})
print("  Added nyc-june-primary-2026")

save_json(DATA_DIR / "brooklyn-ny.json", brooklyn)

# ============================================================
# CAMBRIDGE
# ============================================================
print("\n=== Updating cambridge-ma.json ===")
cambridge = load_json(DATA_DIR / "cambridge-ma.json")
cambridge["last_scraped"] = "2026-06-03T12:00:00Z"

idx, issue = find_issue(cambridge["issues"], "cam-social-housing-task-force")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** The June 1 Council meeting produced several notable outcomes: (1) Council APPROVED the Surveillance Technology Impact Report for Open Architects student data platform. (2) Council DISAPPROVED further use of SoundThinking's Acoustic Gunshot Detection Technology (ShotSpotter) — a significant civil liberties decision under the Surveillance Technology Ordinance. (3) Councillors Nolan and Al-Zubi declared budget priorities: public housing, shelters, and childcare. (4) Committee swaps: Simmons moves from Housing to Economic Development; McGovern moves from Economic Development to Housing. The FY27 budget adoption is imminent. The social housing task force continues with CDD hiring a consultant. Cambridge is also planning citywide free World Cup watch parties in June-July 2026.")
    print("  Updated cam-social-housing-task-force")

idx, issue = find_issue(cambridge["issues"], "cam-zoning-reform-implementation")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** One year post-reform: 4,880+ new units expected, 1,195 projected by 2030 including 220 affordable. The Barrett v. Cambridge inclusionary zoning lawsuit continues — fact discovery deadline November 13, 2026. AG Campbell's intervention underscores statewide stakes for 140+ municipalities. The FY27 budget process advancing with housing, shelters, and childcare declared as priorities by Councillors Nolan and Al-Zubi.")
    print("  Updated cam-zoning-reform-implementation")

# Add ShotSpotter ban
cambridge["issues"].append({
    "id": "cam-shotspotter-banned",
    "title": "Cambridge Bans ShotSpotter — Surveillance Technology Ordinance Applied",
    "governing_body": "Cambridge City Council",
    "governing_body_type": "city_council",
    "meeting_date": "2026-06-01",
    "summary": "NEW (June 3, 2026): At the June 1 meeting, the Cambridge City Council disapproved further use of SoundThinking's Acoustic Gunshot Detection Technology (ShotSpotter) pursuant to the city's Surveillance Technology Ordinance. This follows the May 20 hearing where the impact report was reviewed. ShotSpotter has been controversial nationally — studies show high false positive rates and potential for over-policing in communities of color. Cambridge joins Chicago, New Orleans, and other cities that have ended their ShotSpotter contracts. Separately, the Council approved the Surveillance Technology Impact Report for Open Architects student data platform — showing the ordinance's framework is being applied case-by-case.",
    "policy_domains": ["Public Safety", "Technology & Innovation", "Civil Rights & Social Equity"],
    "decision_type": "vote",
    "geographic_scope": "citywide",
    "public_comment": {
        "available": False,
        "instructions": "Decision made. Monitor implementation of the Surveillance Technology Ordinance for future technology reviews."
    },
    "estimated_contestedness": "medium",
    "importance_score": 70,
    "impact_score": 45,
    "quadrant": "know",
    "why_it_matters_to_you": "Cambridge's Surveillance Technology Ordinance is a model for evidence-based technology governance — evaluating each tool on its merits rather than blanket adoption or rejection. The ShotSpotter disapproval is significant: the council weighed public safety benefits against civil liberties concerns."
})
print("  Added cam-shotspotter-banned")

save_json(DATA_DIR / "cambridge-ma.json", cambridge)

# ============================================================
# BROOKLINE
# ============================================================
print("\n=== Updating brookline-ma.json ===")
brookline = load_json(DATA_DIR / "brookline-ma.json")
brookline["last_scraped"] = "2026-06-03T12:00:00Z"

idx, issue = find_issue(brookline["issues"], "brk-annual-town-meeting-2026")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** ⚡ MASSIVE VICTORY: Town Meeting voted 217-20 on May 29 to approve the CHC Overlay District rezoning — far exceeding the required two-thirds supermajority. City Realty's proposal for 1280-1330 Boylston Street (three buildings of 14, 12, and 7 stories containing a 200-room hotel, 266 apartments/condos, medical office space, and ground-floor retail) can now proceed. City Realty CDO Clifford Kensington said he was 'excited to continue moving forward' and didn't expect the margin to be that large. Fiscal impact: $4.2-6.3M/year in net new tax revenue. This is Brookline's biggest redevelopment approval in decades and a watershed moment for MBTA Communities Act compliance. Town Meeting continues through June 4 for remaining warrant articles including ADU updates (WA14) and zoning bylaw amendments (WA15), both with strong support.")
    append_to_field(issue, "why_it_matters_to_you",
        " ⚡ THE VOTE PASSED 217-20 — a landslide. The feared opposition bloc of 42 South Brookline members was overwhelmed. This is Brookline's biggest pro-housing vote in a generation and proves that even in historically NIMBY communities, organized pro-housing advocacy can win decisively. The 266 units plus hotel represent meaningful housing production and $4.2-6.3M/year in tax revenue. Now monitor implementation — permitting timelines, construction start, and whether opponents attempt legal challenges.")
    issue["quadrant"] = "know"
    print("  Updated brk-annual-town-meeting-2026")

idx, issue = find_issue(brookline["issues"], "brk-override-vote")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** ⚡ OVERRIDE PASSED OVERWHELMINGLY on May 5: $23.25M over three years, approved 8,675 to 5,732 with the highest-ever local turnout (34%+). The override funds schools ($17.94M) and town departments ($5.31M), avoiding hundreds of teacher layoffs and Fire Department cuts. Property taxes will increase approximately 18% over 3 years. The decisive margin (60% to 40%) shows strong community support for maintaining service levels.")
    issue["quadrant"] = "background"
    print("  Updated brk-override-vote")

idx, issue = find_issue(brookline["issues"], "brk-mbta-communities-compliance")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** ⚡ CHC OVERLAY DISTRICT APPROVED 217-20 on May 29. This is a direct victory for MBTA Communities compliance — 266 new housing units in a transit-adjacent corridor on Route 9. The overwhelming margin (far exceeding the two-thirds threshold) signals that Brookline's political center has shifted decisively toward compliance. ADU updates (WA14) and additional zoning amendments (WA15) also expected to pass with strong support. Brookline is now advancing from grudging compliance to proactive development.")
    issue["quadrant"] = "know"
    print("  Updated brk-mbta-communities-compliance")

save_json(DATA_DIR / "brookline-ma.json", brookline)

# ============================================================
# ORANGE COUNTY
# ============================================================
print("\n=== Updating orange-92868.json ===")
oc = load_json(DATA_DIR / "orange-92868.json")
oc["last_scraped"] = "2026-06-03T12:00:00Z"

# Garden Grove (first issue, no id — find by title)
idx, issue = find_issue(oc["issues"], title_keyword="Garden Grove")
if issue:
    # This issue uses "analysis" field instead of "summary"
    field = "analysis" if "analysis" in issue else "summary"
    append_to_field(issue, field,
        "\n\n**June 3 update:** Cleanup operations continue under the OC Health Care Agency (CUPA), working with GKN Aerospace. 20+ real-time air monitoring instruments running around-the-clock with no exceedances detected. Responders constructed channels to prevent liquid MMA from reaching storm drains. DA Spitzer's criminal investigation expanding — now includes potential price gouging and predatory attorney practices. Investigators using drones and anonymous whistleblower tip line. The crisis will define the D4 general election: Shaw (R) vs. Traut (D) must both articulate industrial safety and emergency management positions through November.")
    print("  Updated Garden Grove chemical crisis")

# D4 race
idx, issue = find_issue(oc["issues"], "oc-bos-district-4-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** ⚡ PRIMARY RESULTS (June 2): In an extremely tight race, Tim Shaw (R) edged Connor Traut (D) for the top two spots advancing to November: Shaw 17,895 votes vs. Traut 17,827 — a margin of just 68 votes. Fred Jung and Rose Espinoza eliminated. 21.7% turnout with 414,303 ballots counted countywide. The $125K National Association of Realtors investment in Shaw paid off — despite modest personal fundraising, the institutional backing propelled him past Jung ($347K war chest) and Espinoza (self-funded $150K). Traut's broad institutional support (OC Dem Party $76K, OCEA, Chaffee endorsement) was barely enough. The November general election is now Shaw (R) vs. Traut (D) — a direct partisan contest for the seat that determines whether the 3-2 Democratic BOS majority holds.")
    append_to_field(issue, "why_it_matters_to_you",
        " ⚡ RESULTS ARE IN: Shaw (R) vs. Traut (D) advance to November by just 68 votes. This is now a direct partisan contest — if Shaw wins, the 3-2 Democratic BOS majority flips. The board controls the $10.5B budget, housing enforcement posture, Garden Grove crisis response, and homelessness investment. Traut has the broadest institutional support (OCEA, Dem Party, Chaffee) but Shaw has NAR backing. The November general is a must-win for maintaining the pro-housing BOS majority.")
    issue["importance_score"] = 92
    print("  Updated oc-bos-district-4-open-seat")

# SD-34
idx, issue = find_issue(oc["issues"], "oc-state-senate-sd34-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** ⚡ PRIMARY RESULTS: As expected, Valencia (D) and Shader (R) both advanced to the November general. Valencia is the heavy favorite given the district's Democratic lean.")
    print("  Updated oc-state-senate-sd34-open-seat")

# AD-68
idx, issue = find_issue(oc["issues"], "oc-ad68-open-seat")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** ⚡ PRIMARY RESULTS: Top two from the four-candidate field advance to November. Heavy outside spending defined the race — Peñaloza $407K (Dem Party/tech/law enforcement) vs. Lopez $224K (labor/environmental/progressive). Results to be certified during canvass period (deadline July 3).")
    print("  Updated oc-ad68-open-seat")

# D5 race if it exists
idx, issue = find_issue(oc["issues"], "oc-bos-district-5")
if issue:
    append_to_field(issue, "summary",
        "\n\n**June 3 update:** ⚡ PRIMARY RESULTS (June 2): Incumbent Katrina Foley (D) leads with 47,953 votes over Diane Dixon (R) with 45,368 votes. Lucy Vellema (educator) was eliminated. Foley and Dixon advance to November. If Foley holds, the 3-2 Democratic BOS majority survives on her end — but D4 (Shaw vs. Traut) is the swing seat.")
    print("  Updated oc-bos-district-5")

# Add new: Governor race
oc["issues"].append({
    "id": "oc-ca-governor-race",
    "title": "CA Governor Primary — Hilton (R) 27% and Becerra (D) 26% Lead, Race Too Close to Call",
    "governing_body": "State of California",
    "governing_body_type": "state_legislature",
    "meeting_date": "2026-11-03",
    "summary": "NEW (June 3, 2026): The June 2 California primary produced a tight three-way race for governor with about half of votes counted: Steve Hilton (R) 27%, Xavier Becerra (D) 26%, Tom Steyer (D) 20%. Hilton and Becerra are the likely top-two advancing to November, though Steyer has not conceded. A Hilton-Becerra November matchup would present a stark choice for housing enforcement. Becerra as AG was instrumental in the Huntington Beach compliance fight ($160K fines, $50K/month escalation). A Republican governor could dramatically weaken enforcement of state housing mandates — RHNA, Builder's Remedy, AG referrals. YIMBY Action endorsed Steyer. Ballots continue to be counted through canvass period (July 3). This is the most consequential race for California housing policy.",
    "policy_domains": ["Housing & Land Use", "Government Transparency"],
    "decision_type": "election",
    "geographic_scope": "statewide",
    "public_comment": {
        "available": False,
        "instructions": "Results continue to be updated through canvass period (July 3). Monitor California Secretary of State results page."
    },
    "estimated_contestedness": "high",
    "importance_score": 88,
    "impact_score": 75,
    "quadrant": "act_now",
    "why_it_matters_to_you": "The governor's race is upstream of every OC housing fight. The Huntington Beach enforcement success was only possible because of coordinated state pressure. A Republican governor could weaken RHNA enforcement, soften Builder's Remedy, and reduce AG referrals — undoing the framework that makes local housing advocacy effective."
})
print("  Added oc-ca-governor-race")

# Add new: FY2027 budget
oc["issues"].append({
    "id": "oc-fy2027-budget",
    "title": "OC FY2026-27 Recommended Budget — $10.5B, Released for Review",
    "governing_body": "Orange County Board of Supervisors",
    "governing_body_type": "county_commission",
    "meeting_date": None,
    "summary": "NEW (June 3, 2026): The FY2026-27 Recommended Budget totaling $10.5 billion was released on May 20 for Board of Supervisors and public review. Key context: the county faces fiscal pressures from Airport Fire payouts, sexual harassment settlement costs, and federal funding uncertainty. The Garden Grove chemical crisis response adds additional unbudgeted costs. The homelessness PIT count shows progress (down 13.7% to 6,321, first time more sheltered than unsheltered) but sustained funding is needed. The new D4 supervisor (Shaw or Traut after November) will cast deciding votes on budget priorities.",
    "policy_domains": ["Taxation & Public Finance", "Housing & Land Use"],
    "decision_type": "vote",
    "geographic_scope": "countywide",
    "public_comment": {
        "available": True,
        "deadline": None,
        "instructions": "Budget available for public review on ocgov.com. Public hearings before final adoption."
    },
    "estimated_contestedness": "medium",
    "importance_score": 60,
    "impact_score": 40,
    "quadrant": "watch",
    "why_it_matters_to_you": "The $10.5B budget determines county investment in housing, homelessness services, emergency preparedness, and infrastructure. With the Garden Grove crisis adding unbudgeted costs and federal funding uncertainty, the budget priorities set by the current board will constrain or enable the next supervisor's options."
})
print("  Added oc-fy2027-budget")

save_json(DATA_DIR / "orange-92868.json", oc)

print("\n=== ALL ISSUE FILES UPDATED ===")
