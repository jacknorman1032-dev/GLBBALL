import json, glob, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
# Set True to count Lansing St. Mary's titles as Lansing Catholic's own
CREDIT_PREDECESSORS = False
# Folder holding the research/*.json files (download them from the project's research/ folder)
RESEARCH = os.path.join(HERE, 'research')

BASE = [
    ('east-lansing', 'East Lansing', 'East Lansing', []),
    ('everett', 'Lansing Everett', 'Everett', ['Everett']),
    ('sexton', 'Lansing Sexton', 'Sexton', ['Sexton']),
    ('eastern', 'Lansing Eastern', 'Eastern', ['Eastern']),
    ('okemos', 'Okemos', 'Okemos', []),
    ('holt', 'Holt', 'Holt', []),
    ('grand-ledge', 'Grand Ledge', 'Grand Ledge', []),
    ('waverly', 'Lansing Waverly', 'Waverly', ['Waverly']),
    ('dewitt', 'DeWitt', 'DeWitt', []),
    ('haslett', 'Haslett', 'Haslett', []),
    ('mason', 'Mason', 'Mason', []),
    ('st-johns', 'St. Johns', 'St. Johns', ['St Johns', 'Saint Johns']),
    ('lansing-catholic', 'Lansing Catholic', 'Lansing Catholic', ['Lansing Catholic Central', 'Lansing Catholic Central (LCC)']),
    ('williamston', 'Williamston', 'Williamston', []),
    ('portland', 'Portland', 'Portland', []),
    ('eaton-rapids', 'Eaton Rapids', 'Eaton Rapids', []),
    ('charlotte', 'Charlotte', 'Charlotte', []),
    ('fowlerville', 'Fowlerville', 'Fowlerville', []),
]

# Game notes on the site: keep only sentences about forfeits, cancellations, showcases/tournaments and locations
# (Jack, Oct 28, 2026). The raw logs keep every note.
SPLIT = re.compile(r'(?<!\bSt\.)(?<!\bMt\.)(?<!\bFt\.)(?<!\bJr\.)(?<!\bSr\.)(?<!\bDr\.)(?<!\bvs\.)(?<!\b[A-Z]\.)(?<=[.!?;])\s+(?=[A-Z("])')
KEEP = re.compile(r'forfeit|cancel|postpon|suspend|rescheduled|'
                  r'\bplayed (in|at)\b|^(district|regional|state)\b.*\bat\b|'
                  r'classic|invitational|tournament|tourney|showcase|showdown|shootout|tip.?off|holiday|jamboree|'
                  r'score shown|on-court|quarter scores are from|overtime game played|neutral', re.I)
def split(note): return [x.strip() for x in SPLIT.split(note.strip()) if x.strip()]
def clean_note(note):
    """Keep only sentences about forfeits, cancellations, showcases/tournaments and locations."""
    if not note: return note
    return ' '.join(x for x in split(note) if KEEP.search(x))

def norm(n):
    return re.sub(r'[^a-z]', '', n.lower().replace('saint', 'st'))

research = {}
extra = {'mr_basketball': [], 'lsj_player_of_year': []}
for f in sorted(glob.glob(os.path.join(RESEARCH, '*.json'))):
    try:
        d = json.load(open(f))
    except Exception as e:
        print('skip', f, e); continue
    for s in d.get('schools', []):
        research[norm(s.get('name', ''))] = s
    for k in extra:
        extra[k] += d.get(k, []) or []
    for m in d.get('mr_basketball_retro', []) or []:
        extra['mr_basketball'].append({**m, 'retro': True, 'name': m['name'].replace("Earvin 'Magic' Johnson", 'Earvin "Magic" Johnson'),
                                       'college': '' if m.get('college') == 'none listed' else m.get('college', '')})

OVERRIDES_FILE = os.path.join(HERE, 'overrides.json')
overrides = json.load(open(OVERRIDES_FILE)) if os.path.exists(OVERRIDES_FILE) else {}
CORRECTIONS = json.load(open(os.path.join(HERE, 'corrections.json'))) if os.path.exists(os.path.join(HERE, 'corrections.json')) else {}
# Player facts Jack confirmed (grad years etc.), applied on top of research + overrides so a rebuild keeps them
PLAYER_UPDATES_FILE = os.path.join(HERE, 'player_updates.json')
PLAYER_UPDATES = json.load(open(PLAYER_UPDATES_FILE)) if os.path.exists(PLAYER_UPDATES_FILE) else {}
PLAYER_UPDATES.pop('_note', None)
# All-state honors (honors/bcam_allstate.json in the project); shown on the Honors tab, school pages and player cards
HONORS_FILE = os.path.join(HERE, 'honors_bcam.json')
honors = json.load(open(HONORS_FILE)) if os.path.exists(HONORS_FILE) else []

schools = []
for sid, name, short, aliases in BASE:
    r = research.get(norm(name)) or research.get(norm(short)) or {}
    s = {k: r.get(k) for k in ['nickname', 'colors', 'city', 'status', 'class_current', 'conference_current',
                               'state_titles', 'state_runner_ups', 'final_fours', 'notable_players', 'notable_coaches', 'sources', 'tournament_summary']}
    s = {k: v for k, v in s.items() if v}
    s.update(id=sid, name=name, short=short, aliases=aliases)
    # final fours: normalize to season strings
    s['final_fours'] = sorted({(f['season'] if isinstance(f, dict) else f) for f in s.get('final_fours', [])})
    # players: drop grouped roster entries, clean grad years
    players = []
    for p in s.get('notable_players', []):
        if ',' in p['name'].replace(', Jr.', '') or 'roster' in p['name'].lower():
            continue
        gy = str(p.get('grad_year') or '')
        m = re.search(r'(19|20)\d\d', gy)
        p['grad_year'] = m.group(0) if m else ''
        p['approx'] = bool(m and re.search(r'infer|~|c\.|probabl|not explicit', gy, re.I))
        players.append(p)
    s['notable_players'] = players
    # predecessor lineage (Lansing St. Mary -> Lansing Catholic): kept separate from the school's own totals
    if CREDIT_PREDECESSORS is False and sid == 'lansing-catholic':
        pre = lambda t: 'as lansing st. mary' in (str(t.get('notes', '')) + str(t.get('result', ''))).lower()
        lin = {'name': 'Lansing St. Mary', 'state_titles': [], 'state_runner_ups': [], 'final_fours': []}
        for k in ['state_titles', 'state_runner_ups']:
            keep = []
            for t in s.get(k, []):
                (lin[k] if pre(t) else keep).append(t)
            s[k] = keep
        if lin['state_titles'] or lin['state_runner_ups']:
            pre_seasons = {t['season'] for t in lin['state_titles'] + lin['state_runner_ups']} | {'1934-35'}
            lin['final_fours'] = sorted(x for x in s['final_fours'] if x in pre_seasons)
            s['final_fours'] = [x for x in s['final_fours'] if x not in pre_seasons]
            lin['note'] = ("Lansing St. Mary closed in 1963. Its students went to the Catholic high schools that merged in 1970 "
                           "to form today's Lansing Catholic. MHSAA lists these results under Lansing St. Mary, so they're shown "
                           "as predecessor history and not counted in Lansing Catholic's totals.")
            s['lineage'] = lin
    # Lansing Central (city's first high school, 1875-1943) -> Lansing Sexton, which replaced it in 1943 (Jack, Oct 28, 2026).
    # MHSAA lists these under Lansing Central; shown as predecessor history, not in Sexton's totals.
    if sid == 'sexton':
        mh = 'https://www.mhsaa.com/sports/boys-basketball/past-champions'
        s['lineage'] = {
            'name': 'Lansing Central',
            'note': ("Lansing Central was the city's first high school (built 1875, rebuilt 1910) and closed in 1943, "
                     "when Sexton replaced it. MHSAA lists these results under Lansing Central, so they're shown as "
                     "predecessor history and not counted in Sexton's totals. The 1935 champions are a Greater Lansing "
                     "Area Sports Hall of Fame team."),
            'state_titles': [{'season': '1934-35', 'class': 'Class A', 'coach': 'John Middlesworth', 'final_opponent': 'Flint Northern',
                              'final_score': '25-24', 'source': mh + ' ; https://lansingsportshalloffame.org/team-inductees-by-name/'}],
            'state_runner_ups': [{'season': '1930-31', 'class': 'Class A', 'final_opponent': 'Grand Haven', 'final_score': '15-31', 'source': mh},
                                 {'season': '1931-32', 'class': 'Class A', 'final_opponent': 'Kalamazoo Central', 'final_score': '24-26', 'source': mh}],
            'final_fours': ['1930-31', '1931-32', '1934-35'],
            'source': mh + ' ; https://en.wikipedia.org/wiki/Lansing_School_District',
        }
    for p in s['notable_players']:
        if '(Lansing St. Mary)' in p['name'] and 'lineage' in s:
            p['name'] = p['name'].replace(' (Lansing St. Mary)', '')
            p['predecessor'] = 'Lansing St. Mary'
    for k in ['state_titles', 'state_runner_ups']:
        for t in s.get(k, []):
            m = re.search(r'(Class|Division)\s*\w+', t.get('class') or ''); t['class'] = m.group(0) if m else ''
    # tidy display strings
    s.pop('status', None)
    if s.get('class_current'):
        m = re.search(r'(Division|Class)\s*\w+', s['class_current']); s['class_current'] = m.group(0) if m else ''
    if s.get('conference_current'):
        m = re.search(r'(Blue|White|Red|Gold)', s['conference_current'])
        s['conference_current'] = 'CAAC ' + m.group(1) if 'CAAC' in s['conference_current'] or 'Capital Area' in s['conference_current'] else s['conference_current']
    if s.get('city'):
        s['city'] = re.sub(r',\s*(MI|Michigan)$', '', s['city'])
    if s.get('nickname'):
        s['nickname'] = re.sub(r'\s*\(.*$', '', s['nickname'])
    if s.get('colors', {}).get('names'):
        s['colors']['names'] = re.sub(r'\s*[\(;].*$', '', s['colors']['names'])
    s.update({k: v for k, v in overrides.get(sid, {}).items() if k != 'add_players'})
    s['notable_players'] = s.get('notable_players', []) + overrides.get(sid, {}).get('add_players', [])
    # confirmed player facts (player_updates.json); a name that no longer matches stops the build
    for pname, upd in PLAYER_UPDATES.get(sid, {}).items():
        hit = [p for p in s['notable_players'] if p['name'] == pname]
        assert len(hit) == 1, ('player update did not match exactly one player', sid, pname)
        for k, v in upd.items():
            if not k.startswith('_'): hit[0][k] = v
        if 'grad_year' in upd: hit[0]['approx'] = False
    for k in ['state_titles', 'state_runner_ups']:
        for t in s.get(k, []):
            if t.get('coach'): t['coach'] = re.sub(r'\s*\(.*?\)', '', t['coach']).strip()
    # records the parser would misread (regular-season-only or pre-final records in the source)
    fix = {('sexton', '1958-59'): '15-7', ('okemos', '2005-06'): '25-3', ('everett', '2003-04'): '26-2', ('eastern', '1979-80'): '26-1', ('okemos', '1980-81'): '26-1', ('lansing-catholic', '2007-08'): '23-4'}  # Everett 2003-04, Eastern 1979-80, Okemos 1980-81 and Lansing Catholic 2007-08 records from Jack, Oct 30, 2026
    for k in ['state_titles', 'state_runner_ups']:
        for t in s.get(k, []):
            if (sid, t.get('season')) in fix:
                t['record'] = fix[(sid, t['season'])]
    if sid == 'east-lansing' and not any(x['season'] == '1931-32' for x in s.get('state_runner_ups', [])):
        s.setdefault('state_runner_ups', []).append({'season': '1931-32', 'class': 'Class C', 'final_opponent': 'Kalamazoo St. Augustine', 'final_score': '5-10', 'source': 'https://www.mhsaa.com/sports/boys-basketball/past-champions'})
    GAME_FILES = {'east-lansing': 'el_games.json', 'sexton': 'sexton_games.json', 'williamston': 'williamston_games.json'}
    if sid in GAME_FILES and os.path.exists(os.path.join(HERE, GAME_FILES[sid])):
        s['games'] = json.load(open(os.path.join(HERE, GAME_FILES[sid])))
        # single-game fixes, matched by date + opponent as the log has it. Optional fields:
        # us/them (score; result recomputed), new_opp (opponent was wrong), site (H/R/N).
        for c in CORRECTIONS.get('fix', []):
            if c['school'] != sid: continue
            hit = [g for g in s['games'] if g[0] == c['date'] and g[2] == c['opp']]
            assert len(hit) == 1, ('correction did not match', c)
            g = hit[0]
            if 'us' in c:
                g[6], g[7] = c['us'], c['them']; g[5] = 'W' if g[6] > g[7] else 'L' if g[6] < g[7] else 'T'
            if 'new_opp' in c: g[2] = c['new_opp']
            if 'site' in c: g[3] = c['site']
        # opponent renames (e.g. EL's pre-1943 "Lansing Sexton" games were really Lansing Central); count is checked
        for c in CORRECTIONS.get('rename', []):
            if c['school'] != sid: continue
            hit = [g for g in s['games'] if g[2] == c['opp'] and g[1] < c['before_season']]
            assert len(hit) == c['expect'], ('rename matched', len(hit), 'games, expected', c['expect'], c)
            for g in hit: g[2] = c['new_opp']
        for c in CORRECTIONS.get('add', []):
            if c['school'] == sid and not any(g[0] == c['game'][0] and g[2] == c['game'][2] for g in s['games']):
                s['games'].append(c['game'])
        s['games'].sort(key=lambda g: (g[0] or g[1]))
        for g in s['games']: g[10] = clean_note(g[10] or '')  # site shows only forfeit/cancellation/showcase/location notes
    schools.append(s)

data = {'schools': schools, **extra, 'honors': honors}
js = 'const DATA=' + json.dumps(data, separators=(',', ':'), ensure_ascii=False) + ';'
tpl = open(os.path.join(HERE, 'template.html')).read()
open(os.path.join(HERE, 'greater-lansing-hoops.html'), 'w').write(tpl.replace('/*__DATA__*/', js))
open(os.path.join(HERE, 'data_check.js'), 'w').write(js)
print('schools with research:', [s['name'] for s in schools if s.get('state_titles') or s.get('notable_players')])
print('honors:', len(honors))
print('player updates applied:', sum(len(v) for v in PLAYER_UPDATES.values()))
