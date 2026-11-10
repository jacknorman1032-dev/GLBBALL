"""Add one season (Jack's text list, already saved in game-logs/) to a school's game log and the live page.

Usage (from the repo root):
  python3 -I site-build/add_season.py <school-id> <log.json> <source.txt> --school "Okemos" --league "A,B,..." [--coach "Name"]
Parses with parse_school.py, replaces that season in game-logs/<log.json>, writes the school's games into
site/index.html's DATA, and prints cross-checks against every other loaded log (same date, opponent = this school).
"""
import json, subprocess, sys, argparse, os, re
ap = argparse.ArgumentParser()
ap.add_argument('sid'); ap.add_argument('log'); ap.add_argument('src')
ap.add_argument('--school', required=True); ap.add_argument('--league', default=''); ap.add_argument('--coach', default='')
a = ap.parse_args()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tmp = os.path.join(ROOT, '.season_tmp.json')
out = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'site-build/parse_school.py'), a.src, tmp,
                      '--school', a.school, '--league', a.league], capture_output=True, text=True)
print(out.stdout.strip(), out.stderr.strip())
if out.returncode: sys.exit(1)
new = json.load(open(tmp)); os.remove(tmp)
for r in new:
    if not r[8]: r[8] = a.coach
season = new[0][1]
lp = os.path.join(ROOT, 'game-logs', a.log)
g = json.load(open(lp)) if os.path.exists(lp) else []
g = sorted([r for r in g if r[1] != season] + new, key=lambda r: r[0])
json.dump(g, open(lp, 'w'), separators=(',', ':'))
hp = os.path.join(ROOT, 'site/index.html'); h = open(hp).read()
i = h.index('const DATA=') + len('const DATA='); d, end = json.JSONDecoder().raw_decode(h, i)
sch = {s['id']: s for s in d['schools']}
# replace only this season on the page: other seasons there carry corrections.json fixes the log files don't
sch[a.sid]['games'] = sorted([r for r in sch[a.sid].get('games', []) if r[1] != season] + new, key=lambda r: r[0])
open(hp, 'w').write(h[:i] + json.dumps(d, separators=(',', ':'), ensure_ascii=False) + h[end:])
print(a.sid, 'log now', len(g), 'rows; seasons', sorted({r[1] for r in g})[0], 'to', sorted({r[1] for r in g})[-1])
# cross-check with other schools' logs
names = {a.school, a.school.replace('Lansing ', '')}
for oid, s in sch.items():
    if oid == a.sid or not any(r[1] == season for r in s.get('games', [])): continue
    theirs = {r[0]: r for r in s['games'] if r[2] in names and r[1] == season}
    mine = {r[0]: r for r in new if r[2] in (s['name'], s.get('short'), *s.get('aliases', []))}
    for dt in sorted(set(theirs) | set(mine)):
        m, t = mine.get(dt), theirs.get(dt)
        if m and t:
            ok = (m[6], m[7]) == (t[7], t[6]) and {('H','R'),('R','H'),('N','N')} >= {(m[3], t[3])}
            print(f"  {'ok ' if ok else 'DIFF'} {dt} vs {s['name']}: us {m[6]}-{m[7]} {m[3]} {m[4]} | their log {t[6]}-{t[7]} {t[3]} {t[4]}")
        else:
            r = m or t
            print(f"  ONLY IN {'ours' if m else s['name']+' log'} {dt}: {r[2] if m else s['name']} {r[6]}-{r[7]}")
