#!/usr/bin/env python3
"""
June 3, 2026 updates for all 6 organization data files.
Reads each JSON, appends targeted updates to campaign summaries and next_actions, writes back.
"""

import json
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'data', 'orgs')


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def find_campaign(data, campaign_id=None, keywords=None):
    """Find a campaign by id or by keyword matching in title/summary."""
    for campaign in data.get('active_campaigns', []):
        if campaign_id and campaign.get('id') == campaign_id:
            return campaign
    if keywords:
        for campaign in data.get('active_campaigns', []):
            title = campaign.get('title', '').lower()
            summary = campaign.get('summary', '').lower()
            text = title + ' ' + summary
            if all(kw.lower() in text for kw in keywords):
                return campaign
    return None


def append_to_summary(campaign, text):
    """Append text to a campaign's summary field."""
    campaign['summary'] = campaign['summary'] + text


def add_next_actions(campaign, new_actions):
    """Add new items to a campaign's next_actions array (only if not already present)."""
    existing = set(campaign.get('next_actions', []))
    for action in new_actions:
        if action not in existing:
            campaign['next_actions'].append(action)


def update_austin_yimby_action():
    filename = 'austin-yimby-action.json'
    data = load_json(filename)
    updates = []

    # 1. defend-project-connect
    campaign = find_campaign(data, campaign_id='defend-project-connect')
    if campaign:
        append_to_summary(campaign,
            "\n\n**June 3 update:** Legal status unchanged — Travis County trial halted per TX Supreme Court’s May 22 order requiring resolution of AG Paxton’s jurisdictional plea first. Either path (plea denied → interlocutory appeal; plea granted → suit dismissed) means months of delay. ATP continues advancing: $230M land acquisition for 18 parcels, $60M design-build contract, $25M maintenance facility. The transit-oriented development trifecta (HOME + Light Rail Overlay + DBC) is fully operational. Council in summer recess until July 23. Statewide: James Talarico holds early Senate polling lead over AG Paxton — political dynamics could influence litigation posture. CA primary June 2: Hilton (R) 27% / Becerra (D) 26% — governor’s race determines federal-state alignment on transit funding."
        )
        add_next_actions(campaign, [
            "Track Travis County court proceedings on AG Paxton’s jurisdictional plea — next major deadline TBD"
        ])
        updates.append('defend-project-connect: summary + next_actions updated')
    else:
        updates.append('defend-project-connect: NOT FOUND')

    # 2. council-elections-2026
    campaign = find_campaign(data, campaign_id='council-elections-2026')
    if campaign:
        append_to_summary(campaign,
            "\n\n**June 3 update:** Council in summer recess until July 23. Filing period opens July 20 (47 DAYS). Twenty candidates across five open seats (D1, D3, D5, D8, D9). The defining litmus tests are set: DBC density bonus (approved May 22), bond direction ($390M parks/transportation, housing excluded, final vote July 23), gas peaker plant oversight, and AISD fiscal crisis ($181M deficit, 215 educator cuts, board vote June 18). The gap between now and filing is the critical evaluation window. Pew Research credited Austin’s housing construction surge with driving down rents — this is the narrative pro-housing candidates should lead with."
        )
        updates.append('council-elections-2026: summary updated')
    else:
        updates.append('council-elections-2026: NOT FOUND')

    # 3. Bond/BEATF campaign (ongoing-housing-advocacy)
    campaign = find_campaign(data, campaign_id='ongoing-housing-advocacy')
    if campaign:
        append_to_summary(campaign,
            "\n\n**June 3 update:** Council voted 6-2-1 on May 29 to proceed with ~$390M bond — parks ($250M), transportation, and community facilities. Housing ($200M) NOT included. Mayor Watson opposed. Final vote July 23. Council in summer recess. The bond conversation resumes at the July 23 meeting."
        )
        updates.append('ongoing-housing-advocacy (bond/BEATF): summary updated')
    else:
        updates.append('ongoing-housing-advocacy: NOT FOUND')

    save_json(filename, data)
    return filename, updates


def update_austin_abundance_project():
    filename = 'austin-abundance-project.json'
    data = load_json(filename)
    updates = []

    # The most relevant campaign for infrastructure/development is childcare-desert-mapping
    # (it tracks all development reforms, DBC, bond, AISD, etc.)
    campaign = find_campaign(data, campaign_id='childcare-desert-mapping')
    if campaign:
        append_to_summary(campaign,
            "\n\n**June 3 update:** Council approved sweeping development reforms in late May: DBC density bonus (May 22), Dog’s Head 2,600-acre annexation (May 22), minimum lot size reduction from 5,750 to 1,800 sq ft (May 26), and new missing middle/mixed-use zoning districts. The ~$390M bond (parks/transportation, final vote July 23) and $156.3M Certificates of Obligation (fire stations, public safety) advance infrastructure investment. Council in summer recess until July 23. AISD FY27 budget ($181M deficit) creates both fiscal headwinds and housing production incentives."
        )
        updates.append('childcare-desert-mapping: summary updated')
    else:
        updates.append('childcare-desert-mapping: NOT FOUND')

    save_json(filename, data)
    return filename, updates


def update_austin_safe_and_sound():
    filename = 'austin-safe-and-sound.json'
    data = load_json(filename)
    updates = []

    # Most relevant campaign for public safety is hso-strategic-plan
    campaign = find_campaign(data, campaign_id='hso-strategic-plan')
    if campaign:
        append_to_summary(campaign,
            "\n\n**June 3 update:** George Morales won Pct 4 commissioner runoff ~55% (May 26) — first new commissioner in 30+ years, brings law enforcement background (former constable) and infrastructure focus. Council approved $156.3M Certificates of Obligation for fire/EMS stations, family violence shelter, and public safety facilities (May 28). Gas peaker plant oversight guidelines approved (May 29). AISD budget crisis ($181M deficit, 215 educator cuts) intersects with public safety through school resource officers and community investment. Council in summer recess until July 23."
        )
        updates.append('hso-strategic-plan: summary updated')
    else:
        updates.append('hso-strategic-plan: NOT FOUND')

    save_json(filename, data)
    return filename, updates


def update_oc_housing_now():
    filename = 'oc-housing-now.json'
    data = load_json(filename)
    updates = []

    # orange-housing-element
    campaign = find_campaign(data, campaign_id='orange-housing-element')
    if campaign:
        append_to_summary(campaign,
            "\n\n**June 3 update:** ⚡ JUNE 2 PRIMARY RESULTS: Tim Shaw (R, 17,895) and Connor Traut (D, 17,827) advance to November in an ultra-tight D4 race — just 68 votes separating them. Fred Jung and Rose Espinoza eliminated. The NAR’s $125K investment in Shaw proved decisive. The November Shaw vs. Traut contest determines whether D4 maintains the Democratic lean that supports housing enforcement. In D5, incumbent Katrina Foley (D, 47,953) leads Diane Dixon (R, 45,368) — if Foley holds, the 3-2 Democratic BOS majority survives.\n\n⚡ GOVERNOR: Hilton (R) 27%, Becerra (D) 26% with ~50% counted — both likely advance. A Hilton governorship could weaken RHNA enforcement, Builder’s Remedy implementation, and AG referrals that are the backbone of every OC housing fight. Becerra as AG was instrumental in the HB enforcement.\n\n⚡ HUNTINGTON BEACH COMPLIANCE CONFIRMED: HCD approved HB’s housing plan, ending 4.5+ years of noncompliance under sustained state pressure ($160K in fines, $50K/month escalation). The plan zones for 413+ affordable homes. This is a major enforcement success proving the state pressure model works.\n\n21.7% turnout countywide, 414,303 ballots counted. Canvass period through July 3."
        )
        add_next_actions(campaign, [
            "Prepare for Shaw vs. Traut D4 general election — evaluate housing positions for November",
            "Monitor Huntington Beach Housing Element implementation — compliance is only step one",
            "Track CA governor race count (canvass through July 3) — enforcement depends on who wins"
        ])
        updates.append('orange-housing-element: summary + next_actions updated')
    else:
        updates.append('orange-housing-element: NOT FOUND')

    save_json(filename, data)
    return filename, updates


def update_oc_purple_accountability():
    filename = 'oc-purple-accountability.json'
    data = load_json(filename)
    updates = []

    # Most relevant campaign is bos-majority-defense
    campaign = find_campaign(data, campaign_id='bos-majority-defense')
    if campaign:
        append_to_summary(campaign,
            "\n\n**June 3 update:** ⚡ JUNE 2 PRIMARY RESULTS — KEY OUTCOMES: D4: Shaw (R, 17,895) vs. Traut (D, 17,827) advance — 68-vote margin, ultra-tight. D5: Foley (D) leads Dixon (R). Governor: Hilton (R) 27% / Becerra (D) 26% — both likely advance. 21.7% turnout countywide. The D4 result sets up a direct partisan contest for November — if Shaw wins, the 3-2 Democratic BOS majority flips to Republican, affecting the $10.5B budget, housing enforcement, and the Garden Grove crisis response. The Andrew Do corruption scandal backdrop (former D1 supervisor) emphasizes accountability for all candidates. DA Spitzer’s criminal investigation into GKN Aerospace expanding."
        )
        updates.append('bos-majority-defense: summary updated')
    else:
        updates.append('bos-majority-defense: NOT FOUND')

    save_json(filename, data)
    return filename, updates


def update_oc_abundance_project():
    filename = 'oc-abundance-project.json'
    data = load_json(filename)
    updates = []

    # Most relevant campaign is oc-childcare-desert-mapping
    campaign = find_campaign(data, campaign_id='oc-childcare-desert-mapping')
    if campaign:
        append_to_summary(campaign,
            "\n\n**June 3 update:** ⚡ PRIMARY RESULTS (June 2): D4 — Shaw (R) vs. Traut (D) advance to November (68-vote margin). D5 — Foley (D) leads Dixon (R). Governor — Hilton (R) 27% / Becerra (D) 26%. The FY2026-27 Recommended Budget ($10.5B) is under BOS review. Garden Grove chemical crisis cleanup continues under CUPA. OC Streetcar (92-95% complete) on track for August 2026 launch. Homelessness PIT count down 13.7% to 6,321 (first time more sheltered than unsheltered). The new D4 supervisor will inherit budget pressures from Airport Fire payouts, sexual harassment settlements, federal funding cuts, and Garden Grove crisis response costs."
        )
        updates.append('oc-childcare-desert-mapping: summary updated')
    else:
        updates.append('oc-childcare-desert-mapping: NOT FOUND')

    save_json(filename, data)
    return filename, updates


def main():
    print("=" * 60)
    print("June 3, 2026 Organization Data Updates")
    print("=" * 60)

    all_results = []
    update_functions = [
        update_austin_yimby_action,
        update_austin_abundance_project,
        update_austin_safe_and_sound,
        update_oc_housing_now,
        update_oc_purple_accountability,
        update_oc_abundance_project,
    ]

    for func in update_functions:
        try:
            filename, updates = func()
            all_results.append((filename, updates))
            print(f"\n[OK] {filename}")
            for u in updates:
                print(f"     - {u}")
        except Exception as e:
            all_results.append((func.__name__, [f"ERROR: {e}"]))
            print(f"\n[ERROR] {func.__name__}: {e}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_updates = sum(len(u) for _, u in all_results)
    errors = sum(1 for _, u in all_results if any("ERROR" in x or "NOT FOUND" in x for x in u))
    print(f"Files processed: {len(all_results)}")
    print(f"Updates applied: {total_updates}")
    if errors:
        print(f"Errors/warnings: {errors}")
    else:
        print("All updates applied successfully.")


if __name__ == '__main__':
    main()
