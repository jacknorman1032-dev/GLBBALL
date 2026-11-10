"""Schedule completeness check.

Usage:
  python3 -I audit_schedules.py ../site/index.html [school-id ...] [--season 1975-76] [--out report.md]

Reads the game logs embedded in the built page (DATA.schools[*].games) and flags
seasons that look incomplete or inconsistent. Every flag is a "look at this",
not a verdict: leagues, byes and schedule rules changed over the years.

Game row: [date, season, opponent, site H/R/N, type, result W/L/T/Canceled, us, them, coach, ...]
"""
import json, sys, re, statistics, collections
from datetime import date

REG = {'League', 'Non-League'}
# COVID: the 2020 tournament stopped after districts; 2020-21 was a short season, leagues played each team once
SHORT_SEASONS = {'2020-21'}
HALTED_TOURNEYS = {'2019-20'}

def load(path):
    s = open(path, encoding='utf-8').read()
    i = s.index('const DATA=') + len('const DATA=')
    data, _ = json.JSONDecoder().raw_decode(s[i:])
    return data['schools']

def norm(n):
    n = n.lower().replace('.', '').replace("'", '').strip()
    return re.sub(r'\s+', ' ', n)

def build_names(schools):
    m = {}
    for sc in schools:
        for n in [sc['name'], sc['short']] + sc.get('aliases', []):
            m[norm(n)] = sc['id']
    return m

def d(x):
    try:
        y, mo, dd = map(int, x.split('-'))
        return date(y, mo, dd)
    except Exception:
        return None

def played(g):
    return g[5] != 'Canceled'

def audit_season(sc, season, games, by_season, names, schools_by_id):
    """Return a list of (level, message). level: 'missing' | 'check' | 'data'"""
    out = []
    games = sorted(games, key=lambda g: g[0] or '')
    real = [g for g in games if played(g)]
    reg = [g for g in real if g[4] in REG]
    lg = [g for g in real if g[4] == 'League']
    tour = [g for g in real if g[4] not in REG]

    # 1. regular-season count
    n = len(reg)
    short = season in SHORT_SEASONS
    if n % 2 and not short:
        out.append(('check', f'{n} regular-season games (odd number) - a game may be missing'))
    near = [len([g for g in by_season[s] if played(g) and g[4] in REG])
            for s in by_season if s != season and s not in SHORT_SEASONS and abs(int(s[:4]) - int(season[:4])) <= 3]
    if len(near) >= 2 and not short:
        med = statistics.median(near)
        if n <= med - 2:
            out.append(('missing', f'{n} regular-season games vs. about {med:g} in nearby seasons'))

    # 2. league opponents: usually home and away
    cnt = collections.Counter(g[2] for g in lg)
    for opp, k in sorted(cnt.items()):
        sites = [g[3] for g in lg if g[2] == opp]
        if k == 1 and not short:
            other = 'road' if sites[0] == 'H' else 'home'
            out.append(('missing', f'League opponent {opp} played once ({"home" if sites[0]=="H" else "road" if sites[0]=="R" else "neutral"}) - {other} game missing?'))
        elif k == 2 and sites.count('H') != 1:
            out.append(('check', f'Both league games vs {opp} listed as {"home" if sites[0]=="H" else "road"}'))
        elif k > 2:
            out.append(('check', f'{k} league games vs {opp}'))

    # 3. league opponents in the seasons before and after but not this one
    y = int(season[:4])
    prev = f'{y-1}-{str(y)[2:]}'; nxt = f'{y+1}-{str(y+2)[2:]}'
    if prev in by_season and nxt in by_season:
        lp = {g[2] for g in by_season[prev] if g[4] == 'League'}
        ln = {g[2] for g in by_season[nxt] if g[4] == 'League'}
        here = {g[2] for g in real}
        for opp in sorted((lp & ln) - here):
            out.append(('missing', f'{opp} is a league opponent in {prev} and {nxt} but not on this schedule'))

    # 4. tournament path
    if not tour and season < '2026-27' and real:
        out.append(('check', 'No tournament games listed'))
    lost = None
    for g in tour:
        if lost:
            out.append(('data', f'{g[0]} {g[4]} vs {g[2]} comes after a tournament loss ({lost})'))
        if g[5] == 'L':
            lost = f'{lost or ""}{g[4]} vs {g[2]}'
    if tour and tour[-1][5] == 'W' and tour[-1][4] != 'State Final' and season not in HALTED_TOURNEYS:
        out.append(('missing', f'Last tournament game is a win ({tour[-1][4]} vs {tour[-1][2]}) - the game they lost is missing?'))

    # 5. long gaps in the middle of the season
    ds = [d(g[0]) for g in real if g[4] in REG and d(g[0])]
    for a, b in zip(ds, ds[1:]):
        gap = (b - a).days
        holiday = a.month == 12 and a.day >= 15 and (b.month == 1 and b.day <= 10)
        if gap >= (21 if holiday else 15):
            out.append(('check', f'{gap}-day gap between {a} and {b}'))

    # 6. bad rows
    seen = collections.Counter((g[0], g[2]) for g in games)
    for (dt, opp), k in seen.items():
        if k > 1:
            out.append(('data', f'{dt} vs {opp} listed {k} times'))
    for g in real:
        us, th = g[6], g[7]
        if isinstance(us, int) and isinstance(th, int):
            exp = 'W' if us > th else 'L' if us < th else 'T'
            if g[5] in 'WLT' and g[5] != exp and not g[9]:
                out.append(('data', f'{g[0]} vs {g[2]}: result {g[5]} but score {us}-{th}'))
        elif g[5] in ('W', 'L'):
            out.append(('check', f'{g[0]} vs {g[2]}: no score'))
        if g[3] not in ('H', 'R', 'N'):
            out.append(('data', f'{g[0]} vs {g[2]}: site "{g[3]}"'))

    # 7. cross-check against the other schools' logs
    me = sc['id']
    mine = {}
    for g in games:
        o = names.get(norm(g[2]))
        if o:
            mine.setdefault((o, g[0]), g)
    for other in schools_by_id.values():
        if other['id'] == me:
            continue
        for g in other.get('games') or []:
            if g[1] != season or names.get(norm(g[2])) != me:
                continue
            m = mine.get((other['id'], g[0]))
            if not m:
                # allow a 1-day date slip
                dd = d(g[0])
                m = next((x for (oid, dt), x in mine.items() if oid == other['id'] and dd and d(dt)
                          and abs((d(dt) - dd).days) <= 1), None)
                if m:
                    out.append(('data', f'{other["name"]} log has {g[0]} vs us; ours says {m[0]}'))
            if not m:
                if played(g):
                    out.append(('missing', f'{g[0]} vs {other["name"]} ({g[4]}, {g[7]}-{g[6]} from their log) is not on this schedule'))
                continue
            if played(g) and played(m) and (m[6], m[7]) != (g[7], g[6]) and None not in (g[6], g[7], m[6], m[7]):
                out.append(('data', f'{g[0]} vs {other["name"]}: score {m[6]}-{m[7]} here, {g[7]}-{g[6]} in their log'))
            flip = {'H': 'R', 'R': 'H', 'N': 'N'}
            if m[3] != flip.get(g[3]):
                out.append(('data', f'{g[0]} vs {other["name"]}: site {m[3]} here, {g[3]} in their log'))
    return out

def main(argv):
    path = argv[0]
    rest = argv[1:]
    only_season = None; out_path = None; ids = []
    while rest:
        a = rest.pop(0)
        if a == '--season': only_season = rest.pop(0)
        elif a == '--out': out_path = rest.pop(0)
        else: ids.append(a)
    schools = load(path)
    names = build_names(schools)
    byid = {s['id']: s for s in schools}
    lines = ['# Schedule check', '',
             'Legend: **MISSING** = a game probably missing; **CHECK** = worth a look; **DATA** = conflicting or bad entry.', '']
    totals = collections.Counter()
    for sc in schools:
        if ids and sc['id'] not in ids:
            continue
        games = sc.get('games') or []
        if not games:
            continue
        by_season = collections.defaultdict(list)
        for g in games:
            by_season[g[1]].append(g)
        block = []
        for season in sorted(by_season):
            if only_season and season != only_season:
                continue
            flags = audit_season(sc, season, by_season[season], by_season, names, byid)
            if flags:
                block.append(f'**{season}**')
                order = {'missing': 0, 'data': 1, 'check': 2}
                for lvl, msg in sorted(flags, key=lambda f: order[f[0]]):
                    block.append(f'- {lvl.upper()}: {msg}')
                    totals[lvl] += 1
                block.append('')
        if block:
            lines += [f'## {sc["name"]}', ''] + block
    lines.insert(3, f'Totals: {totals["missing"]} missing, {totals["data"]} data, {totals["check"]} check.\n')
    text = '\n'.join(lines)
    if out_path:
        open(out_path, 'w').write(text)
    print(text)

if __name__ == '__main__':
    main(sys.argv[1:])
