import re, glob, os, json, sys
SRC = sys.argv[1]  # dir with .cols files
SEASON = {'08BoysAllStateTeams':'2007-08','0809BoysBCAMsBEST':'2008-09','09-10boysbcamsbest':'2009-10','10-11boysbcamsbest':'2010-11','11-12boysbcamsbest':'2011-12',
 '13-14BoysBCAMsBEST':'2013-14','14-15BoysBCAMsBEST_1':'2014-15','15-16BoysBest_1':'2015-16','17BoysBestWeb-Sheet1':'2016-17',
 '18BoysBestWeb-Sheet1_0_1':'2017-18','19BoysBestWeb-Sheet1':'2018-19','20BoysBEST3':'2019-20','21BoyssBEST_1':'2020-21','22BoysBESTWeeb_1':'2021-22',
 '23BoysBESTYIR_1':'2022-23','24BestBoys_1':'2023-24','25BoysBest_1':'2024-25','26BoysBEST_1':'2025-26'}
YR = {'frosh':'Fr','false':'?','fr':'Fr','fresh':'Fr','freshman':'Fr','so':'So','soph':'So','sophomore':'So','jr':'Jr','junior':'Jr','sr':'Sr','senior':'Sr','8th':'8th'}
YRX = r'(?:Fr|So|Jr|Sr|Fresh|Soph|Junior|Senior|Freshman|Sophomore)\.?'
def hdr(line):
    l = line.strip().replace('’',"'").replace('“','"').replace('”','"')
    if re.search(r'Best of the\s*"?BEST', l, re.I): return ('BotB', None)
    m = re.search(r'(Class|CLASS|Division|DIVISION)\s+([ABCD1-4])\s+(?:Honorable|Special) Mention', l)
    if m: return ('HM', m.group(2))
    m = re.search(r"BCAM's BEST\s*-\s*Division\s+([1-4])", l, re.I) or re.search(r"^(?:Class|CLASS|Division)\s+([ABCD1-4])(?:\s+BCAM's BEST)?\s*$", l)
    if m: return ('BEST', m.group(1))
    if re.match(r'Honorable Mention:', l): return ('HM', '__keep__')
    return None
WORDY = r'(?:Senior|Junior|Sophomore|Freshman|Soph\.?|Fresh\.?|Frosh|FALSE)'
def parse_entry(s):
    s = s.strip().rstrip('.;').strip()
    s = s.replace('–','-')
    m = re.match(rf"^(.+?)\s+({WORDY})\s+(.+)$", s, re.I)
    if not m:
        m = re.match(rf"^(.+?),\s*({YRX})\s*[-,]?\s*(.+)$", s)
    if not m:
        m = re.match(rf"^(.+?)\s+({YRX})\s+(.+)$", s)
    if not m:
        m2 = re.match(r"^(.+?)\s+-\s+(.+)$", s)  # 2007-08 and 2008-09 lists give no class year
        if m2 and len(m2.group(1).split()) <= 5: return m2.group(1).strip(), '', m2.group(2).strip(' -,')
        return None
    name, yr, school = m.group(1).strip(), m.group(2), m.group(3).strip(' -,')
    return name, YR.get(yr.lower().rstrip('.'), yr), school
rows = []; unparsed = []
for f in sorted(glob.glob(os.path.join(SRC, '*.cols'))):
    key = os.path.basename(f)[:-5]; season = SEASON.get(key)
    if not season: continue
    text = open(f).read()
    cols = re.split(r'^##### (page\d+ [LR])\n', text, flags=re.M)[1:]
    state = {'L': ('BotB', None), 'R': ('BotB', None)}
    for tag, body in zip(cols[::2], cols[1::2]):
        side = tag[-1]
        sec, grp = state[side]
        hm_buf = []
        def flush_hm():
            if not hm_buf: return
            para = ' '.join(hm_buf)
            para = re.sub(r'^Honorable Mention:\s*', '', para)
            pos = 0
            for m in re.finditer(rf"([^;,]+?),\s*({YRX}|Frosh),\s*([^;,]+)", para):
                gap = para[pos:m.start()].strip(' ;,.')
                if gap: unparsed.append((season, 'HM-gap', gap))
                pos = m.end()
                rows.append(dict(season=season, tier='HM', group=grp, name=m.group(1).strip(), yr=YR.get(m.group(2).lower().rstrip('.'), m.group(2)), school=m.group(3).strip(' .'), file=key, raw=m.group(0).strip()))
            if para[pos:].strip(' ;,.'): unparsed.append((season, 'HM-gap', para[pos:].strip()))
            hm_buf.clear()
        lines = body.split('\n')
        for line in lines:
            h = hdr(line)
            if h:
                flush_hm()
                if h[1] == '__keep__':
                    sec = 'HMP'; rest = re.sub(r'^\s*Honorable Mention:\s*', '', line.strip())
                    if rest: hm_buf.append(rest)
                else:
                    sec, grp = h
                    # header may share a line with an entry (centered BotB title)
                continue
            if sec == 'HMP':
                if line.strip(): hm_buf.append(line.strip())
                continue
            e = parse_entry(line)
            if e:
                rows.append(dict(season=season, tier=sec, group=grp, name=e[0], yr=e[1], school=e[2], file=key, raw=line.strip()))
            elif line.strip():
                unparsed.append((season, sec, line.strip()))
        flush_hm()
        if sec == 'HMP': sec = 'HM'
        state[side] = (sec, grp)
json.dump(rows, open(os.path.join(SRC, 'all_rows.json'), 'w'), indent=0)
json.dump(unparsed, open(os.path.join(SRC, 'unparsed.json'), 'w'), indent=0)
from collections import Counter
print(len(rows), 'rows;', len(unparsed), 'unparsed')
print(Counter((r['season'], r['tier'], r['group']) for r in rows))
