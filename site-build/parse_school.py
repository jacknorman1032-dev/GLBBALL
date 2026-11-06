"""Parse a school's season text list (Jack's format) into the site's game tuples.
Handles forfeits (FFW/FFL), canceled games ("(Canceled <reason>)"), tournament rounds written out ("* District Semifinal at Fowlerville") or as codes (*DQ, *DS ...),
4-digit or 2-digit years, and tournament notes on the same line or the next line.
League games = regular-season games vs the opponents passed with --league.

Usage: python3 -I parse_school.py <input.txt> <out.json> --school "Williamston" --league "Haslett,Fowlerville,..."
"""
import re, sys, json, argparse

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--school', required=True, help="the school the list is for (used to drop 'at <school>' venues)")
ap.add_argument('--league', default='', help='comma-separated league opponents for this season')
a = ap.parse_args()
LEAGUE = {x.strip() for x in a.league.split(',') if x.strip()}
SELF = {a.school, a.school.replace('Lansing ', '')}

ROUNDS = ['District Quarterfinal', 'District Semifinal', 'District Final', 'Regional Quarterfinal', 'Regional Semifinal',
          'Regional Final', 'State Quarterfinal', 'State Semifinal', 'State Final']
CODES = {'DQ': 'District Quarterfinal', 'DS': 'District Semifinal', 'DF': 'District Final', 'RS': 'Regional Semifinal',
         'RF': 'Regional Final', 'SQ': 'State Quarterfinal', 'SS': 'State Semifinal', 'SF': 'State Final'}
VENUES = {'Breslin Center': 'the Breslin Center', 'Eastern': 'Lansing Eastern', 'Waverly': 'Lansing Waverly',
          'KC': 'Kalamazoo Central', 'Lakewood': 'Lake Odessa Lakewood', 'EL': 'East Lansing', 'GL': 'Grand Ledge',
          'Smithville (OH)': 'Smithville, Ohio', 'St Johns': 'St. Johns'}
NAMES = {'Ottawa Hills': 'Grand Rapids Ottawa Hills'}

SEASON = re.compile(r'^(\d{4})/(\d{2,4})\s*\|\s*(\d+)-(\d+)(?:\s*\((\d+)-(\d+)\))?')
COACH = re.compile(r'^Head Coach:\s*(.*)$')
GAME = re.compile(r'^\((\d{1,2})/(\d{1,2})/(\d{2,4})\)\s*(vs|at|\(n\))\s+(.+?)\s*\((FFW|FFL|W|L|T)\s+(\d+)-(\d+)\)(.*)$')

CANCEL = re.compile(r'^\((\d{1,2})/(\d{1,2})/(\d{2,4})\)\s*(vs|at|\(n\))\s+(.+?)\s*\(Cancell?ed\s*(.*?)\)\s*$', re.I)

season = coach = None; header = None; games = []
for raw in open(a.src, encoding='utf-8').read().splitlines():
    line = raw.strip()
    if not line: continue
    m = SEASON.match(line)
    if m:
        y = int(m.group(1)); season = f'{y}-{str(y + 1)[2:]}'
        header = tuple(int(x) if x else None for x in m.groups()[2:]); continue
    m = COACH.match(line)
    if m: coach = re.sub(r'\s*\(.*?\)', '', m.group(1)).strip(); continue
    m = CANCEL.match(line)
    if m:  # e.g. "(01/22/19) vs Williamston (Canceled Inclement Weather)"; stored like Sexton's canceled games
        mo, dy, yr, where, opp, why = m.groups()
        y0 = int(season[:4]); year = y0 if int(mo) >= 7 else y0 + 1
        assert int(yr[-2:]) == year % 100, ('date year does not fit the season', line)
        opp = NAMES.get(opp.strip(), opp.strip())
        note = 'Canceled' + (f' because of {why.strip().lower()}' if why.strip() else '') + '.'
        games.append(dict(row=[f'{year}-{int(mo):02}-{int(dy):02}', season, opp, {'vs': 'H', 'at': 'R', '(n)': 'N'}[where],
                               'Non-League', 'Canceled', None, None, coach, 0, '', 0, '', '', ''], note=note))
        continue
    m = GAME.match(line)
    if not m:
        # tournament note on its own line, for the previous game
        note = line.strip('* ').strip()
        if games and note and not games[-1]['note']:
            games[-1]['note'] = 'Played in the ' + re.sub(r'^the\s+', '', note, flags=re.I) + '.'
        continue
    mo, dy, yr, where, opp, res, us, them, tail = m.groups()
    y0 = int(season[:4]); year = y0 if int(mo) >= 7 else y0 + 1
    assert int(yr[-2:]) == year % 100, ('date year does not fit the season', line)
    tail = tail.replace('*', ' ').strip()
    rnd = next((r for r in ROUNDS if r.lower() in tail.lower()), None)
    cm = re.search(r'\b(DQ|DS|DF|RS|RF|SQ|SS|SF)\b', tail)
    if not rnd and cm: rnd = CODES[cm.group(1)]
    note = ''
    if rnd:
        vm = re.search(r'\bat\s+(.+)$', tail)
        v = vm.group(1).strip() if vm else ''
        v = VENUES.get(v, v)
        if v and v not in SELF and v != NAMES.get(opp, opp):
            note = f'Played at {v}.'
    elif re.match(r'at\s', tail):  # a venue with no event name, e.g. "* at Smithville (OH)"
        v = tail[3:].strip(); note = f'Played at {VENUES.get(v, v)}.'
    elif tail:
        note = 'Played in the ' + re.sub(r'^the\s+', '', tail, flags=re.I).rstrip('.') + '.'
    opp = NAMES.get(opp.strip(), opp.strip())
    site = {'vs': 'H', 'at': 'R', '(n)': 'N'}[where]
    typ = rnd or ('League' if opp in LEAGUE and not note else 'Non-League')
    ff = int(res.startswith('FF'))  # forfeit, stored like EL's log: result W/L, flag 1, note 'Forfeit win/loss'
    if ff:
        res = res[2:]; note = ('Forfeit win' if res == 'W' else 'Forfeit loss') + (' ' + note if note else '')
    games.append(dict(row=[f'{year}-{int(mo):02}-{int(dy):02}', season, opp, site, typ, res, int(us), int(them), coach, ff, '', 0, '', '', ''], note=note))

out = []
for g in games:
    g['row'][10] = g['note']; out.append(g['row'])
json.dump(out, open(a.out, 'w'), separators=(',', ':'))
w = sum(r[5] == 'W' for r in out); l = sum(r[5] == 'L' for r in out)
lw = sum(r[5] == 'W' for r in out if r[4] == 'League'); ll = sum(r[5] == 'L' for r in out if r[4] == 'League')
ok = all(h is None or h == v for h, v in zip(header, (w, l, lw, ll)))
print(len(out), 'games;', season, 'parsed', (w, l, lw, ll), 'header', header, '' if ok else '<-- differs from header')
