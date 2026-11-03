"""Parse Jack's Lansing Sexton text results (1989-90 on) into the site's game tuples.
Usage: python3 -I parse_sexton.py <input.txt> <out.json>"""
import re, sys, json, collections

SRC, OUT = sys.argv[1], sys.argv[2]
lines = open(SRC, encoding='utf-8').read().splitlines()

NAMES = {
    'Ottawa Hills': 'Grand Rapids Ottawa Hills',
    'Carman-Ainsworth': 'Flint Ainsworth',
    'Toledo Roy Start': 'Toledo Start',
    'Gary Lew Wallace': 'Gary (Ind.) Lew Wallace',
    'Reeths-Puffer': 'Muskegon Reeths-Puffer',
    'Lansing Catholic': 'Lansing Catholic',
}
ROUNDS = {'DQ': 'District Quarterfinal', 'DS': 'District Semifinal', 'DF': 'District Final',
          'RS': 'Regional Semifinal', 'RF': 'Regional Final',
          'SQ': 'State Quarterfinal', 'SS': 'State Semifinal', 'SF': 'State Final'}
VENUES = {'SJ': 'St. Johns', 'EV': 'Lansing Everett', 'Eastern': 'Lansing Eastern', 'GRCC': 'Grand Rapids Community College',
          'LCC': 'Lansing Catholic', 'KC': 'Kalamazoo Central', 'Lumen Christi': 'Jackson Lumen Christi',
          'Lakewood': 'Lake Odessa Lakewood', 'Waverly': 'Lansing Waverly'}

GAME = re.compile(r'\((\d{1,2})/(\d{1,2})/(\d{2,4})\)?\s*(vs|at|\(n\))\s+(.+?)\s*\((W|L|T)\s+(\d+)-(\d+)\)|\((\d{1,2})/(\d{1,2})/(\d{2})\)\s*(vs|at|\(n\))\s+(.+?)\s*\((Canceled)\)')
SEASON = re.compile(r'^(\d{4})/(\d{2,4})\s*\|\s*(\d+)-(\d+)(?:\s*\((\d+)-(\d+)\))?')  # league record optional
COACH = re.compile(r'^Head Coach:\s*(.*)$')

season = None; coach = 'Mike Major'; games = []; headers = {}; fixes = []; pending_note = None
for i, raw in enumerate(lines):
    line = raw.strip()
    if not line:
        continue
    m = SEASON.match(line)
    if m:
        y = int(m.group(1)); season = f'{y}-{str(y + 1)[2:]}'
        headers[season] = tuple(int(m.group(k)) if m.group(k) else None for k in range(3, 7)); continue
    m = COACH.match(line)
    if m:
        name = re.sub(r'\s*\(.*?\)', '', m.group(1)).strip()
        if '/' in name:
            name = name.split('/')[0].strip()
        if name:
            coach = name
        else:
            fixes.append(f'{season}: coach line is blank; kept {coach}')
        continue
    if 'Resigns' in line:
        m2 = re.search(r';\s*(.+?)\s+interim', line, re.I)
        if m2: coach = m2.group(1).strip()
        continue
    if line.startswith('*') and line.endswith('*') and not GAME.search(line):
        note = line.strip('*').strip()
        for g in reversed(games):
            if g['note_slot']:
                note = re.sub(r'^the\s+', '', note, flags=re.I)  # avoid "Played in the The D-Zone ..."
                g['notes'].append(f'Played in the {note}.' if not note.lower().startswith('played') else note); g['note_slot'] = False
                break
        continue
    found = list(GAME.finditer(line))
    if not found:
        if season and not line.startswith('Lansing Sexton') and 'suspended' not in line.lower():
            if games and games[-1]['season'] == season:
                games[-1]['notes'].append(f'Played in the {line.strip("*").strip()}.')
        elif 'suspended' in line.lower():
            headers.setdefault('_notes', []).append((season, line.strip('*')))
        continue
    for j, m in enumerate(found):
        if m.group(14):
            mo, dy, where, opp = int(m.group(9)), int(m.group(10)), m.group(12), m.group(13); res = 'Canceled'; us = them = None
        else:
            mo, dy, where, opp = int(m.group(1)), int(m.group(2)), m.group(4), m.group(5); res = m.group(6); us, them = int(m.group(7)), int(m.group(8))
        y0 = int(season[:4]); year = y0 if mo >= 7 else y0 + 1
        written = m.group(3) if not m.group(14) else m.group(11)
        if written and int(written[-2:]) != year % 100:
            fixes.append(f'{season}: date {mo:02}/{dy:02}/{written} read as {year}')
        tail = line[m.end(): found[j + 1].start() if j + 1 < len(found) else len(line)]
        code = re.search(r'\b(DQ|DS|DF|RS|RF|SQ|SS|SF)\b', tail)
        star = '*' in tail
        venue = None
        vm = re.search(r'\bat\s+(.+?)\s*\*?\s*$', re.sub(r'\b(DQ|DS|DF|RS|RF|SQ|SS|SF)\b', '', tail).replace('*', ' ').strip())
        if vm: venue = vm.group(1).strip()
        inline_note = None
        if star and not code and venue is None:
            t2 = tail.replace('*', '').strip()
            if t2: inline_note = t2
        opp = opp.strip()
        opp = NAMES.get(opp, opp)
        site = {'vs': 'H', 'at': 'R', '(n)': 'N'}[where]
        g = dict(date=f'{year}-{mo:02}-{dy:02}', season=season, opp=opp, site=site, res=res, us=us, them=them,
                 coach=coach, code=code.group(1) if code else None, star=star, notes=[], note_slot=star and not code)
        if venue in ('Sexton', 'Lansing Sexton'):
            venue = None  # 'at Sexton' on a home tournament game
        if venue and NAMES.get(VENUES.get(venue, venue), VENUES.get(venue, venue)) == NAMES.get(opp.strip(), opp.strip()):
            venue = None
        if venue:
            v = VENUES.get(venue, venue)
            g['notes'].append(f'Played at {v}.')
        if inline_note:
            parts = re.split(r'\s+at\s+', inline_note, maxsplit=1)
            g['notes'].append(f'Played in the {parts[0]}' + (f' at {parts[1]}.' if len(parts) > 1 else '.'))
            g['note_slot'] = False
        games.append(g)

by = collections.defaultdict(list)
for g in games: by[g['season']].append(g)
order = ['DQ', 'DS', 'DF', 'RS', 'RF', 'SQ', 'SS', 'SF']
assumed = []
for s, gs in by.items():
    gs.sort(key=lambda g: g['date'])
    post = False
    for g in gs:
        mo = int(g['date'][5:7])
        if g['code'] or (mo == 3 and (g['star'] or g['site'] == 'N')):
            post = True
        g['post'] = post and g['res'] != 'Canceled'
    seq = [g for g in gs if g['post']]
    if seq and not any(g['code'] for g in seq):
        for k, g in enumerate(seq): g['code'] = order[k]
        assumed.append(s)
    elif seq:
        first = next(k for k, g in enumerate(seq) if g['code'])
        base = order.index(seq[first]['code'])
        for k in range(first): seq[k]['code'] = order[max(0, base - (first - k))]
        for k in range(first + 1, len(seq)):
            if not seq[k]['code']: seq[k]['code'] = order[min(7, order.index(seq[k - 1]['code']) + 1)]

CAAC_A = {'Lansing Everett', 'Lansing Eastern', 'Lansing Waverly', 'East Lansing', 'Holt', 'Grand Ledge', 'Jackson'}
GOLD = {'St Johns', 'Mason', 'Lansing Waverly', 'Jackson Northwest', 'Jackson Lumen Christi', 'Owosso'}
BLUE = {'Lansing Everett', 'Lansing Eastern', 'East Lansing', 'Holt', 'Grand Ledge', 'Jackson', 'Okemos'}
# 2018-19 on: Sexton in the CAAC White with Charlotte, Eaton Rapids, Ionia, Lansing Catholic, Portland (matches the 1-9 header)
WHITE = {'Charlotte', 'Eaton Rapids', 'Ionia', 'Lansing Catholic', 'Portland'}
report = []
for s, gs in by.items():
    reg = [g for g in gs if not g['post'] and g['res'] != 'Canceled']
    y = int(s[:4])
    if 2007 <= y <= 2010:
        lg = GOLD
    else:
        cnt = collections.Counter(g['opp'] for g in reg if not g['star'])
        # 2023-24: Olivet and Lake Odessa Lakewood join the White (14-game league schedule)
        pool = (WHITE | ({'Olivet', 'Lake Odessa Lakewood'} if y >= 2023 else set())) if y >= 2018 else CAAC_A | BLUE | {'St Johns', 'Mason'}
        # White years: every regular-season game vs a White school is league (2020-21 COVID season met Portland once)
        lg = {o for o, n in cnt.items() if o in pool and (n >= 2 or y >= 2018)}
        if s == '1998-99': lg.add('Lansing Waverly')
    for g in gs:
        g['type'] = ROUNDS[g['code']] if g['post'] else ('League' if g['opp'] in lg and not g['star'] else 'Non-League')
    played = [g for g in gs if g['res'] in 'WLT' and g['res'] != 'Canceled']
    w = sum(g['res'] == 'W' for g in played); l = sum(g['res'] == 'L' for g in played)
    lw = sum(g['res'] == 'W' for g in played if g['type'] == 'League'); ll = sum(g['res'] == 'L' for g in played if g['type'] == 'League')
    report.append((s, (w, l, lw, ll), headers.get(s), sorted(lg)))

out = []
for g in games:
    note = ' '.join(g['notes'])
    if g['res'] == 'Canceled': g['type'] = 'Non-League'
    out.append([g['date'], g['season'], g['opp'], g['site'], g['type'], g['res'], g['us'], g['them'], g['coach'], 0, note, 0, '', '', ''])
json.dump(out, open(OUT, 'w'), separators=(',', ':'))
print(len(out), 'games')
for r in report:
    hdr = r[2]
    ok = hdr and all(h is None or h == v for h, v in zip(hdr, r[1]))
    flag = ('' if ok else '  <-- differs from header') + ('  (no league record in header)' if hdr and hdr[2] is None else '')
    print(r[0], 'parsed', r[1], 'header', r[2], flag)
print('assumed round order:', assumed)
print('fixes:'); [print('  ', f) for f in fixes]
print('notes:', headers.get('_notes'))
