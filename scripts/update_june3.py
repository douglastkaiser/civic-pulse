#!/usr/bin/env python3
"""
June 3, 2026 update script for civic-pulse dashboard issue data files.
Reads each JSON file, makes targeted updates, and writes back.
"""

import json
import os
import sys
from datetime import datetime

DATA_DIR = "/home/user/civic-pulse/public/data/issues"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def find_issue_by_id(issues, issue_id):
    for i, issue in enumerate(issues):
        if issue.get("id") == issue_id:
            return i, issue
    return None, None

def find_issue_by_title_substring(issues, title_substring):
    for i, issue in enumerate(issues):
        if title_substring.lower() in issue.get("title", "").lower():
            return i, issue
    return None, None

def append_to_field(issue, field, text):
    if field in issue:
        issue[field] += text
    else:
        issue[field] = text

changes_log = []

def log_change(file, description):
    changes_log.append(f"  [{file}] {description}")


# ============================================================
# AUSTIN (austin-78702.json)
# ============================================================
def update_austin():
    filepath = os.path.join(DATA_DIR, "austin-78702.json")
    data = load_json(filepath)
    fname = "austin-78702.json"

    # Update last_scraped
    data["last_scraped"] = "2026-06-03T12:00:00Z"
    log_change(fname, "Updated last_scraped to 2026-06-03T12:00:00Z")

    issues = data["issues"]

    # 1. atx-d1-election - append to summary and why_it_matters_to_you
    idx, issue = find_issue_by_id(issues, "atx-d1-election")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** Council is now in summer recess — no meetings until July 23. The AISD FY27 budget proposal ($181M deficit) was published June 4 with the Board of Trustees final vote on June 18. 215 educator positions cut. Superintendent Segura is trying to close a ~$50M gap beyond the $130M already identified. Property sales could generate $45M. AISD teachers rallied at the Capitol on June 2 asking legislators to increase school funding — the state funding formula hasn't changed since 2019. The bond final vote is July 23 (50 DAYS). Filing period for council races opens July 20 (47 DAYS). Twenty candidates total across five open seats (D1, D3, D5, D8, D9). The DBC density bonus (approved May 22), bond direction ($390M, housing excluded), gas peaker plant oversight, and AISD fiscal crisis are the defining litmus tests.")
        append_to_field(issue, "why_it_matters_to_you",
            " ⚡ Council is in summer recess until July 23 — the gap between now and the filing period (July 20) is the critical window to evaluate candidates. The AISD budget crisis ($181M deficit, 215 educator cuts, board vote June 18) will be a central campaign issue. Watch for candidates' positions on school funding alongside housing, transit, and the bond.")
        log_change(fname, "Updated atx-d1-election: appended to summary and why_it_matters_to_you")
    else:
        log_change(fname, "WARNING: atx-d1-election not found")

    # 2. atx-golf-course-rezone - append to summary
    idx, issue = find_issue_by_id(issues, "atx-golf-course-rezone")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** Council in summer recess until July 23. The density bonus program (DBC) approved May 22 and the Dog's Head annexation (2,600 acres) approved the same day show strong council pro-development trajectory. Council also approved new development rules on May 26: minimum lot size reduced from 5,750 to 1,800 sq ft citywide — the most significant lot size change in 80 years. Missing middle zoning districts and new mixed-use zoning districts also created. These reforms complement the golf course rezoning opportunity.")
        log_change(fname, "Updated atx-golf-course-rezone: appended to summary")
    else:
        log_change(fname, "WARNING: atx-golf-course-rezone not found")

    # 3. Check for defend-project-connect in issues (skip if not found)
    idx, issue = find_issue_by_id(issues, "defend-project-connect")
    if issue:
        log_change(fname, "Found defend-project-connect in issues (unexpected) - skipping per instructions")
    else:
        log_change(fname, "defend-project-connect not in issues file (expected) - skipped")

    # 5. Add NEW issue: atx-aisd-budget-crisis
    # Check if it already exists
    idx, existing = find_issue_by_id(issues, "atx-aisd-budget-crisis")
    if existing:
        # The issue already exists - update its title, summary and other fields
        # to reflect the June 3 update content rather than adding a duplicate
        log_change(fname, "atx-aisd-budget-crisis already exists (updating existing issue with June 3 content)")
        append_to_field(existing, "summary",
            "\n\n**June 3 update:** AISD FY27 budget proposal ($181M deficit) was published June 4 with the Board of Trustees final vote scheduled for June 18. 215 full-time educator positions are being cut (85 elementary, 51 middle, 79 high school), though some may be filled through attrition of open vacancies. Superintendent Segura has identified $130M in cuts but is still trying to close a ~$50M gap. The district is exploring selling surplus properties which could generate ~$45M. Class sizes will increase for grades 2-5 and planning time will be cut for secondary teachers. AISD teachers rallied at the Texas Capitol on June 2, asking legislators to increase school funding. The state funding formula — the Basic Allotment — has not been adjusted since 2019, meaning districts absorb inflation without additional state support. This is a statewide structural problem, not just an AISD management issue. The fiscal crisis creates both headwinds and tailwinds for housing policy: budget pressure incentivizes the city to approve new development (property tax revenue), but school quality concerns can fuel NIMBY arguments against density. Council candidates must articulate a position on school funding alongside housing and transit.")
        append_to_field(existing, "why_it_matters_to_you",
            " The AISD budget crisis is the backdrop for every November council race conversation. 215 educator cuts and larger class sizes will galvanize parents — a constituency that overlaps with both pro-housing and anti-development camps. The structural problem (state funding formula frozen since 2019) requires state-level advocacy, but the local symptom (budget cuts, school quality) becomes a campaign issue. Support increased housing production as a structural budget solution (more property tax revenue) while advocating for state funding reform. Board vote June 18.")
        existing["importance_score"] = 75
        existing["impact_score"] = 60  # keep existing or use new
    else:
        new_issue = {
            "id": "atx-aisd-budget-crisis",
            "title": "AISD FY27 Budget Crisis — $181M Deficit, 215 Educator Cuts, Board Vote June 18",
            "governing_body": "Austin ISD Board of Trustees",
            "governing_body_type": "school_board",
            "meeting_date": "2026-06-18",
            "summary": "NEW (June 3, 2026): Austin ISD faces a $181 million deficit for FY2026-27, the district's worst fiscal crisis in decades. Superintendent Matias Segura has identified $130M in cuts but is still trying to close a ~$50M gap. 215 full-time educator positions are being cut (85 elementary, 51 middle, 79 high school), though some may be filled through attrition of open vacancies. The budget proposal was published June 4 with the Board of Trustees final vote scheduled for June 18.\n\nKey drivers: declining enrollment (district lost ~8,000 students since 2019), stagnant state funding formula (unchanged since 2019), and missed property sales. The district is exploring selling surplus properties which could generate ~$45M. Class sizes will increase for grades 2-5 and planning time will be cut for secondary teachers.\n\nAISD teachers rallied at the Texas Capitol on June 2, asking legislators to increase school funding. The state funding formula — the Basic Allotment — has not been adjusted since 2019, meaning districts absorb inflation without additional state support. This is a statewide structural problem, not just an AISD management issue.\n\nThe fiscal crisis creates both headwinds and tailwinds for housing policy: budget pressure incentivizes the city to approve new development (property tax revenue), but school quality concerns can fuel NIMBY arguments against density. Council candidates must articulate a position on school funding alongside housing and transit.",
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
        }
        issues.append(new_issue)
        log_change(fname, "Added NEW issue: atx-aisd-budget-crisis")

    # 6. Add NEW issue: atx-development-rules-overhaul
    idx, existing = find_issue_by_id(issues, "atx-development-rules-overhaul")
    if existing:
        log_change(fname, "atx-development-rules-overhaul already exists - skipping")
    else:
        new_issue = {
            "id": "atx-development-rules-overhaul",
            "title": "Austin Approves Sweeping Development Rule Changes — Lot Size, Missing Middle, Mixed-Use",
            "governing_body": "Austin City Council",
            "governing_body_type": "city_council",
            "meeting_date": "2026-05-26",
            "summary": "NEW (June 3, 2026): In a landmark week for Austin housing policy, the City Council approved multiple development rule changes in late May:\n\n• **Minimum Lot Size** (May 26): Reduced from 5,750 sq ft to 1,800 sq ft citywide — the first change in over 80 years. Allows smaller, cheaper homes and enables more homes per block.\n\n• **Density Bonus Program** (May 22): Developers can build 15-60 feet taller in exchange for affordable housing units or community benefits (wider sidewalks, green space). Only CM Duchen voted against. Replaces the controversial DB90 program.\n\n• **Missing Middle Zoning** (May 2026): New zoning districts created for smaller housing types — townhomes, cottage courts, small multiplexes — that fill the gap between single-family homes and large apartment buildings.\n\n• **Mixed-Use Zoning** (May 2026): New districts allowing commercial and residential development in tandem, enabling walkable neighborhood commercial corridors.\n\n• **Dog's Head Annexation** (May 22): 2,600-acre annexation approved with a 45-year development agreement. 20% of housing must be affordable. Projected $3.5B in property tax revenue over the agreement term.\n\nCombined with the HOME Initiative and Light Rail Transit Overlay (adopted May 16), Austin now has the most comprehensive pro-housing zoning framework of any major Texas city. Pew Research (March 2026) credited Austin's housing construction surge with driving down rents — these reforms extend that trajectory.\n\nThe Real Deal asked (May 29): 'Austin's builders can now build taller. Will they?' The answer depends on market conditions, interest rates, and developer uptake of the new DBC framework.",
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
            "why_it_matters_to_you": "This is the YIMBY policy trifecta Austin has been building toward: HOME Initiative (housing by right) + Density Bonus (height for affordability) + Light Rail Overlay (transit-oriented density) + lot size reduction (enabling smaller homes). Pew Research credited Austin's construction surge with driving down rents. These reforms lock in the pro-building trajectory for years. The key now is implementation — monitor DBC uptake, track permitting timelines, and support the reforms against any rollback attempts from the next council. The November council elections will determine whether this trajectory continues."
        }
        issues.append(new_issue)
        log_change(fname, "Added NEW issue: atx-development-rules-overhaul")

    save_json(filepath, data)
    log_change(fname, "File saved successfully")


# ============================================================
# MADISON (madison-wi.json)
# ============================================================
def update_madison():
    filepath = os.path.join(DATA_DIR, "madison-wi.json")
    data = load_json(filepath)
    fname = "madison-wi.json"

    # Update last_scraped
    data["last_scraped"] = "2026-06-03T12:00:00Z"
    log_change(fname, "Updated last_scraped to 2026-06-03T12:00:00Z")

    issues = data["issues"]

    # 2. mad-east-west-brt-construction - append to summary
    idx, issue = find_issue_by_id(issues, "mad-east-west-brt-construction")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** Route A continues 15-minute service. Legistar data shows CDD authorized to accept up to $50,000 in additional federal/state grants for community development (Resolution 92931, June 3). Federal funding for North-South Route B ($118M) remains at HIGH risk — no signed FTA agreement yet. City developing alternate strategies for scaled-back BRT improvements. BRT ridership up 18% since September 2022 launch. New council leadership — President Sabrina Madison (D17) and VP Carmella Glenn (D18) — in place.")
        log_change(fname, "Updated mad-east-west-brt-construction: appended to summary")
    else:
        log_change(fname, "WARNING: mad-east-west-brt-construction not found")

    # 3. mad-new-housing-developments - append to summary
    idx, issue = find_issue_by_id(issues, "mad-new-housing-developments")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** Southwest and Southeast Area Plans heading toward June 23 Council adoption vote — 20 DAYS AWAY. Madison's Housing Forward Initiative continues — the mayor's zoning changes approved by the Common Council include: allowing duplexes/two-flats on most residentially zoned lots, 17-3 vote for more density near public transit, and unanimous approval for cottage courts. The Council voted to raise height limits near residential zones and reduce minimum lot areas. Polling shows 74%+ voter support for all zoning changes. The city needs ~2,000 new units annually to keep pace with population growth. New alders Ellen Zhang (D8) and Noah Lieberman (D14) now seated.")
        log_change(fname, "Updated mad-new-housing-developments: appended to summary")
    else:
        log_change(fname, "WARNING: mad-new-housing-developments not found")

    # 4. Add NEW issue: mad-police-oversight-debate
    idx, existing = find_issue_by_id(issues, "mad-police-oversight-debate")
    if existing:
        log_change(fname, "mad-police-oversight-debate already exists - skipping")
    else:
        new_issue = {
            "id": "mad-police-oversight-debate",
            "title": "Police Oversight Restrictions Debated — Independent Monitor Opposes Amendments",
            "governing_body": "Madison Common Council",
            "governing_body_type": "city_council",
            "meeting_date": None,
            "summary": "NEW (June 3, 2026): The Common Council considered amendments to the Office of the Independent Monitor that would require quarterly public reports and restrict when the office can use its own legal counsel. Interim Independent Police Monitor Aeiramique Glass fiercely opposed the restrictions, arguing they would undermine the office's independence. The debate reflects ongoing tension between police accountability advocates (who want a strong, independent monitor) and some council members (who want more oversight of the oversight body). The new council leadership — President Sabrina Madison (D17) and VP Carmella Glenn (D18) — will shape how this debate unfolds.",
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
            "why_it_matters_to_you": "Police oversight is a defining issue for Madison's progressive identity. The tension between independent oversight and council control reflects broader questions about institutional design and accountability. Watch how the new council leadership handles this — it signals their approach to governance and civil liberties."
        }
        issues.append(new_issue)
        log_change(fname, "Added NEW issue: mad-police-oversight-debate")

    save_json(filepath, data)
    log_change(fname, "File saved successfully")


# ============================================================
# BROOKLYN (brooklyn-ny.json)
# ============================================================
def update_brooklyn():
    filepath = os.path.join(DATA_DIR, "brooklyn-ny.json")
    data = load_json(filepath)
    fname = "brooklyn-ny.json"

    # Update last_scraped
    data["last_scraped"] = "2026-06-03T12:00:00Z"
    log_change(fname, "Updated last_scraped to 2026-06-03T12:00:00Z")

    issues = data["issues"]

    # 2. nyc-atlantic-ave-rezoning - append to summary
    idx, issue = find_issue_by_id(issues, "nyc-atlantic-ave-rezoning")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** The South of Prospect Plan community engagement begins this summer — Mayor Mamdani's first major rezoning targeting McDonald Avenue and Coney Island Avenue corridors south of Prospect Park. City of Yes implementation showing results: 23% more housing permits in year one. Governor Hochul announced RFP for 300 new housing units on underutilized MTA land in Crown Heights — made possible by the AAMUP rezoning. An application for East 98th Street rezoning in East Flatbush (Community District 17) has a public scoping session scheduled for June 11 at 2:00 PM. The NYC June 23 primary election approaches — multiple Brooklyn council and state legislative seats on the ballot.")
        log_change(fname, "Updated nyc-atlantic-ave-rezoning: appended to summary")
    else:
        log_change(fname, "WARNING: nyc-atlantic-ave-rezoning not found")

    # 3. nyc-speaker-menin-priorities - append to summary
    idx, issue = find_issue_by_id(issues, "nyc-speaker-menin-priorities")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** The Council Advisory Group on Housing Affordability has been formed — co-chaired by Gary LaBarbera (Building Trades Council president), Barika Williams (ANHD executive director), and James Simmons III (Asland Capital Partners CEO). The advisory group will refine proposals to boost and preserve housing. The small lots reform targets 2,850 identified lots that could unlock up to 35,000 new homes including thousands of affordable units — all without costly rezonings. The Council hasn't set a legislative timeline and says it's in early talks with the Mamdani administration. Combined with the Block by Block housing plan ($22B capital) and SPEED reforms, the policy infrastructure for delivering at scale is being built.")
        log_change(fname, "Updated nyc-speaker-menin-priorities: appended to summary")
    else:
        log_change(fname, "WARNING: nyc-speaker-menin-priorities not found")

    # 4. Add NEW issue: nyc-june-primary-2026
    idx, existing = find_issue_by_id(issues, "nyc-june-primary-2026")
    if existing:
        log_change(fname, "nyc-june-primary-2026 already exists - skipping")
    else:
        new_issue = {
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
            "why_it_matters_to_you": "The June 23 primary determines which candidates advance for Brooklyn council seats. With the City of Yes framework in place and Speaker Menin's small lots reform in development, the next council's composition will determine whether NYC's historic housing momentum continues or stalls. Evaluate every candidate on their housing record and reform positions."
        }
        issues.append(new_issue)
        log_change(fname, "Added NEW issue: nyc-june-primary-2026")

    save_json(filepath, data)
    log_change(fname, "File saved successfully")


# ============================================================
# CAMBRIDGE (cambridge-ma.json)
# ============================================================
def update_cambridge():
    filepath = os.path.join(DATA_DIR, "cambridge-ma.json")
    data = load_json(filepath)
    fname = "cambridge-ma.json"

    # Update last_scraped
    data["last_scraped"] = "2026-06-03T12:00:00Z"
    log_change(fname, "Updated last_scraped to 2026-06-03T12:00:00Z")

    issues = data["issues"]

    # 2. cam-social-housing-task-force - append to summary
    idx, issue = find_issue_by_id(issues, "cam-social-housing-task-force")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** The June 1 Council meeting produced several notable outcomes: (1) Council APPROVED the Surveillance Technology Impact Report for Open Architects student data platform. (2) Council DISAPPROVED further use of SoundThinking's Acoustic Gunshot Detection Technology (ShotSpotter) — a significant civil liberties decision under the Surveillance Technology Ordinance. (3) Councillors Nolan and Al-Zubi declared budget priorities: public housing, shelters, and childcare. (4) Committee swaps: Simmons moves from Housing to Economic Development; McGovern moves from Economic Development to Housing. The FY27 budget adoption is imminent — anticipated date was June 1. The social housing task force continues with CDD hiring a consultant. Cambridge is also planning citywide free World Cup watch parties in June-July 2026.")
        log_change(fname, "Updated cam-social-housing-task-force: appended to summary")
    else:
        log_change(fname, "WARNING: cam-social-housing-task-force not found")

    # 3. cam-zoning-reform-implementation - append to summary
    idx, issue = find_issue_by_id(issues, "cam-zoning-reform-implementation")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** One year post-reform: 4,880+ new units expected, 1,195 projected by 2030 including 220 affordable. The Barrett v. Cambridge inclusionary zoning lawsuit continues — fact discovery deadline November 13, 2026. AG Campbell's intervention underscores statewide stakes for 140+ municipalities. The FY27 budget process advancing with housing, shelters, and childcare declared as priorities by Councillors Nolan and Al-Zubi.")
        log_change(fname, "Updated cam-zoning-reform-implementation: appended to summary")
    else:
        log_change(fname, "WARNING: cam-zoning-reform-implementation not found")

    # 4. Add NEW issue: cam-shotspotter-banned
    idx, existing = find_issue_by_id(issues, "cam-shotspotter-banned")
    if existing:
        log_change(fname, "cam-shotspotter-banned already exists - skipping")
    else:
        new_issue = {
            "id": "cam-shotspotter-banned",
            "title": "Cambridge Bans ShotSpotter — Surveillance Technology Ordinance Applied",
            "governing_body": "Cambridge City Council",
            "governing_body_type": "city_council",
            "meeting_date": "2026-06-01",
            "summary": "NEW (June 3, 2026): At the June 1 meeting, the Cambridge City Council disapproved further use of SoundThinking's Acoustic Gunshot Detection Technology (ShotSpotter) pursuant to the city's Surveillance Technology Ordinance. This follows the May 20 hearing where the impact report was reviewed. ShotSpotter has been controversial nationally — studies show high false positive rates and potential for over-policing in communities of color, while proponents argue it accelerates police response to shootings. Cambridge joins Chicago, New Orleans, and other cities that have ended their ShotSpotter contracts.\n\nSeparately, the Council approved the Surveillance Technology Impact Report for Open Architects student data platform — showing the ordinance's framework is being applied case-by-case, not as a blanket ban on technology.",
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
            "why_it_matters_to_you": "Cambridge's Surveillance Technology Ordinance is a model for evidence-based technology governance — evaluating each tool on its merits rather than blanket adoption or rejection. The ShotSpotter disapproval is significant: the council weighed public safety benefits against civil liberties concerns and privacy impacts. This is the kind of deliberative tech policy that produces better outcomes than either 'ban everything' or 'deploy everything' approaches."
        }
        issues.append(new_issue)
        log_change(fname, "Added NEW issue: cam-shotspotter-banned")

    save_json(filepath, data)
    log_change(fname, "File saved successfully")


# ============================================================
# BROOKLINE (brookline-ma.json)
# ============================================================
def update_brookline():
    filepath = os.path.join(DATA_DIR, "brookline-ma.json")
    data = load_json(filepath)
    fname = "brookline-ma.json"

    # Update last_scraped
    data["last_scraped"] = "2026-06-03T12:00:00Z"
    log_change(fname, "Updated last_scraped to 2026-06-03T12:00:00Z")

    issues = data["issues"]

    # 2. brk-annual-town-meeting-2026 - append to summary, update quadrant, append to why_it_matters_to_you
    idx, issue = find_issue_by_id(issues, "brk-annual-town-meeting-2026")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** ⚡ MASSIVE VICTORY: Town Meeting voted 217-20 on May 29 to approve the CHC Overlay District rezoning — far exceeding the required two-thirds supermajority. City Realty's proposal for 1280-1330 Boylston Street (three buildings of 14, 12, and 7 stories containing a 200-room hotel, 266 apartments/condos, medical office space, and ground-floor retail) can now proceed. City Realty CDO Clifford Kensington said he was 'excited to continue moving forward' and didn't expect the margin to be that large. Fiscal impact: $4.2-6.3M/year in net new tax revenue. This is Brookline's biggest redevelopment approval in decades and a watershed moment for MBTA Communities Act compliance. Town Meeting continues through June 4 for remaining warrant articles including ADU updates (WA14) and zoning bylaw amendments (WA15), both with strong support.")
        issue["quadrant"] = "know"
        append_to_field(issue, "why_it_matters_to_you",
            " ⚡ THE VOTE PASSED 217-20 — a landslide. The feared opposition bloc of 42 South Brookline members was overwhelmed. This is Brookline's biggest pro-housing vote in a generation and proves that even in historically NIMBY communities, organized pro-housing advocacy can win decisively. The 266 units plus hotel represent meaningful housing production and $4.2-6.3M/year in tax revenue. Now monitor implementation — permitting timelines, construction start, and whether opponents attempt legal challenges.")
        log_change(fname, "Updated brk-annual-town-meeting-2026: appended to summary, changed quadrant to 'know', appended to why_it_matters_to_you")
    else:
        log_change(fname, "WARNING: brk-annual-town-meeting-2026 not found")

    # 3. brk-override-vote - append to summary
    idx, issue = find_issue_by_id(issues, "brk-override-vote")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** ⚡ OVERRIDE PASSED OVERWHELMINGLY on May 5: $23.25M over three years, approved 8,675 to 5,732 with the highest-ever local turnout (34%+). The override funds schools ($17.94M) and town departments ($5.31M), avoiding hundreds of teacher layoffs and Fire Department cuts. Property taxes will increase approximately 18% over 3 years. The decisive margin (60% to 40%) shows strong community support for maintaining service levels.")
        log_change(fname, "Updated brk-override-vote: appended to summary")
    else:
        log_change(fname, "WARNING: brk-override-vote not found")

    # 4. brk-mbta-communities-compliance - append to summary
    idx, issue = find_issue_by_id(issues, "brk-mbta-communities-compliance")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** ⚡ CHC OVERLAY DISTRICT APPROVED 217-20 on May 29. This is a direct victory for MBTA Communities compliance — 266 new housing units in a transit-adjacent corridor on Route 9. The overwhelming margin (far exceeding the two-thirds threshold) signals that Brookline's political center has shifted decisively toward compliance. ADU updates (WA14) and additional zoning amendments (WA15) also expected to pass with strong support. Brookline is now advancing from grudging compliance to proactive development.")
        log_change(fname, "Updated brk-mbta-communities-compliance: appended to summary")
    else:
        log_change(fname, "WARNING: brk-mbta-communities-compliance not found")

    save_json(filepath, data)
    log_change(fname, "File saved successfully")


# ============================================================
# ORANGE COUNTY (orange-92868.json)
# ============================================================
def update_orange():
    filepath = os.path.join(DATA_DIR, "orange-92868.json")
    data = load_json(filepath)
    fname = "orange-92868.json"

    # Update last_scraped
    data["last_scraped"] = "2026-06-03T12:00:00Z"
    log_change(fname, "Updated last_scraped to 2026-06-03T12:00:00Z")

    issues = data["issues"]

    # 2. oc-bos-district-4-open-seat - append to summary, update quadrant, update importance_score
    idx, issue = find_issue_by_id(issues, "oc-bos-district-4-open-seat")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** ⚡ PRIMARY RESULTS (June 2): In an extremely tight race, Tim Shaw (R) edged Connor Traut (D) for the top two spots advancing to November: Shaw 17,895 votes vs. Traut 17,827 — a margin of just 68 votes. Fred Jung and Rose Espinoza were eliminated. 21.7% turnout with 414,303 ballots counted countywide. The $125K National Association of Realtors investment in Shaw paid off — despite modest personal fundraising, the institutional backing propelled him past Jung ($347K war chest) and Espinoza (self-funded $150K). Traut's broad institutional support (OC Dem Party $76K, OCEA, Chaffee endorsement) was barely enough. The November general election is now Shaw (R) vs. Traut (D) — a direct partisan contest for the seat that determines whether the 3-2 Democratic BOS majority holds.")
        issue["quadrant"] = "act_now"
        issue["importance_score"] = 90
        log_change(fname, "Updated oc-bos-district-4-open-seat: appended to summary, quadrant=act_now, importance_score=90")
    else:
        log_change(fname, "WARNING: oc-bos-district-4-open-seat not found")

    # 3. Garden Grove Chemical Crisis - find by title substring, append to analysis field
    idx, issue = find_issue_by_title_substring(issues, "Garden Grove Chemical Crisis")
    if issue:
        # This issue uses "analysis" field name - check what field it uses
        # From the file, it has an "analysis" field
        if "analysis" in issue:
            append_to_field(issue, "analysis",
                "\n\n**June 3 update:** Cleanup operations continue under the OC Health Care Agency (CUPA), working with GKN Aerospace. 20+ real-time air monitoring instruments running around-the-clock with no exceedances detected. Responders constructed channels to prevent liquid MMA from reaching storm drains. DA Spitzer's criminal investigation expanding — now includes potential price gouging and predatory attorney practices. Investigators using drones and anonymous whistleblower tip line. Wikipedia article now published on the incident. The crisis will define the D4 general election: Shaw (R) vs. Traut (D) must both articulate industrial safety and emergency management positions through November.")
            log_change(fname, "Updated Garden Grove Chemical Crisis: appended to analysis field")
        else:
            # Maybe it uses "summary" field instead
            # The first issue in the file doesn't have an "id" field and has no "summary" - it uses "analysis"
            # Let me check - actually from the read, the first issue doesn't have "summary", it has "analysis"
            # Let me just try the summary field as well
            log_change(fname, "WARNING: Garden Grove Chemical Crisis found but no 'analysis' field")
    else:
        log_change(fname, "WARNING: Garden Grove Chemical Crisis not found by title")

    # 4. oc-state-senate-sd34-open-seat - append to summary
    idx, issue = find_issue_by_id(issues, "oc-state-senate-sd34-open-seat")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** ⚡ PRIMARY RESULTS: As expected, Valencia (D) and Shader (R) both advanced to the November general. Valencia is the heavy favorite given the district's Democratic lean. His Assembly record on housing and governance remains the key evaluation.")
        log_change(fname, "Updated oc-state-senate-sd34-open-seat: appended to summary")
    else:
        log_change(fname, "WARNING: oc-state-senate-sd34-open-seat not found")

    # 5. oc-ad68-open-seat - append to summary
    idx, issue = find_issue_by_id(issues, "oc-ad68-open-seat")
    if issue:
        append_to_field(issue, "summary",
            "\n\n**June 3 update:** ⚡ PRIMARY RESULTS: Top two from the four-candidate field advance to November. Updated fundraising showed heavy outside spending — Peñaloza $407K with Dem Party/tech/law enforcement support vs. Lopez $224K with labor/environmental/progressive backing. Results to be certified during canvass period (deadline July 3).")
        log_change(fname, "Updated oc-ad68-open-seat: appended to summary")
    else:
        log_change(fname, "WARNING: oc-ad68-open-seat not found")

    # 6. Add NEW issue: oc-ca-governor-race
    idx, existing = find_issue_by_id(issues, "oc-ca-governor-race")
    if existing:
        log_change(fname, "oc-ca-governor-race already exists - skipping")
    else:
        new_issue = {
            "id": "oc-ca-governor-race",
            "title": "CA Governor Primary — Hilton (R) and Becerra (D) Lead, Race Too Close to Call",
            "governing_body": "State of California",
            "governing_body_type": "state_legislature",
            "meeting_date": "2026-11-03",
            "summary": "NEW (June 3, 2026): The June 2 California primary produced a tight three-way race for governor with about half of votes counted: Steve Hilton (R) 27%, Xavier Becerra (D) 26%, Tom Steyer (D) 20%. Hilton and Becerra are the likely top-two advancing to November, though Steyer has not conceded.\n\nThis is the most consequential race for OC housing policy. The next governor controls RHNA enforcement, Builder's Remedy implementation, AG referrals for noncompliant cities, and the state housing mandate framework that is the backbone of every OC housing fight. Hilton — a former Fox News host and British political adviser — has promised to 'reset' California after years of one-party rule. Becerra — former state AG and U.S. Health Secretary — positions himself as a steady governance hand. Steyer — billionaire climate activist — ran as the progressive option.\n\nA Hilton-Becerra November matchup would present a stark choice for housing enforcement. Becerra as AG was instrumental in the Huntington Beach compliance fight ($160K fines, $50K/month escalation). A Republican governor could dramatically weaken enforcement of state housing mandates. YIMBY Action endorsed Steyer. Ballots continue to be counted during the canvass period through July 3.",
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
            "why_it_matters_to_you": "The governor's race is upstream of every OC housing fight. The Huntington Beach enforcement success ($160K fines, compliance achieved after 4.5+ years of resistance) was only possible because of the state AG and governor's coordinated pressure. A Republican governor could weaken RHNA enforcement, soften Builder's Remedy implementation, and reduce AG referrals for noncompliant cities — undoing the legal framework that makes local housing advocacy effective. The November general is the most important race for California housing policy."
        }
        issues.append(new_issue)
        log_change(fname, "Added NEW issue: oc-ca-governor-race")

    # 7. Add NEW issue: oc-fy2027-budget
    idx, existing = find_issue_by_id(issues, "oc-fy2027-budget")
    if existing:
        log_change(fname, "oc-fy2027-budget already exists - skipping")
    else:
        new_issue = {
            "id": "oc-fy2027-budget",
            "title": "OC FY2026-27 Recommended Budget — $10.5B, Released for Review",
            "governing_body": "Orange County Board of Supervisors",
            "governing_body_type": "county_commission",
            "meeting_date": None,
            "summary": "NEW (June 3, 2026): The FY2026-27 Recommended Budget totaling $10.5 billion was released on May 20 for Board of Supervisors and public review. Key context: the county faces fiscal pressures from Airport Fire payouts, sexual harassment settlement costs, and federal funding uncertainty. The Garden Grove chemical crisis response adds additional unbudgeted costs. The homelessness PIT count shows progress (down 13.7% to 6,321, first time more sheltered than unsheltered) but sustained funding is needed to maintain these gains. The new D4 supervisor (Shaw or Traut after November) will cast deciding votes on budget priorities including housing investment, emergency management capacity, and social services.",
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
        }
        issues.append(new_issue)
        log_change(fname, "Added NEW issue: oc-fy2027-budget")

    save_json(filepath, data)
    log_change(fname, "File saved successfully")


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("CIVIC PULSE — June 3, 2026 Update Script")
    print("=" * 60)
    print()

    files_to_update = [
        ("austin-78702.json", update_austin),
        ("madison-wi.json", update_madison),
        ("brooklyn-ny.json", update_brooklyn),
        ("cambridge-ma.json", update_cambridge),
        ("brookline-ma.json", update_brookline),
        ("orange-92868.json", update_orange),
    ]

    for fname, update_func in files_to_update:
        filepath = os.path.join(DATA_DIR, fname)
        if not os.path.exists(filepath):
            print(f"ERROR: {filepath} not found — skipping")
            continue
        print(f"Processing {fname}...")
        try:
            update_func()
            print(f"  ✓ {fname} updated successfully")
        except Exception as e:
            print(f"  ✗ ERROR processing {fname}: {e}")
            import traceback
            traceback.print_exc()
        print()

    print("=" * 60)
    print("CHANGE LOG")
    print("=" * 60)
    for entry in changes_log:
        print(entry)

    print()
    print(f"Total changes logged: {len(changes_log)}")
    print("Done.")


if __name__ == "__main__":
    main()
