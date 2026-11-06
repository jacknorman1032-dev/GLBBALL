"""Turn an MHSAA printable-schedule PDF (pdftotext -layout output) into Jack's text-list format.
Usage: python3 -I mhsaa_pdf.py <sched.txt>  -> prints '<season header>' and one line per game, no times.
Host H/A becomes vs/at; anything else is left for hand edits (neutral sites, rounds, notes)."""
import re, sys
t = open(sys.argv[1]).read()
# drop page footers/headers so a game split across pages reads as one block
t = re.sub(r'\n\s*https://www\.mhsaa\.com/printable-schedule\S*.*?\n\s*Page \d+ of \d+\s*\n:?', '\n', t)
season = re.search(r'(\d{4})-(\d{4}) .*?Varsity', t)
rec = re.search(r'Record:\s*\((\d+)-(\d+)\)', t)
games = []
for b in re.split(r'(?=Date/Time:)', t)[1:]:  # one block per game, so a missing field can't borrow the next game's
    f = lambda k: (re.search(k + r':[ \t]*(.*)', b) or [None, ''])[1].strip()
    mo, dy, yr = re.match(r'Date/Time:\s*(\d+)/(\d+)(?:/(\d{4}))?', b).groups()
    # MHSAA drops the year on dates in the printing year; infer it from the season (July onward = first year)
    d = (mo, dy, yr or (season.group(1) if int(mo) >= 7 else season.group(2)))
    sc = re.match(r'[\d-]*', f('Score')).group(0)
    wl = f('W/L'); wl = {'WF': 'FFW', 'LF': 'FFL'}.get(wl, wl)  # MHSAA marks forfeits WF / LF
    games.append((*d, f('Host'), f('Opponent'), wl, sc, ''))
print(f'{season.group(1)}/{season.group(2)} | {rec.group(1)}-{rec.group(2)}')
for mo, dy, yr, host, opp, wl, sc, ot in games:
    print(f"({int(mo):02}/{int(dy):02}/{yr[2:]}) {'vs' if host == 'H' else 'at' if host == 'A' else '(n)'} {opp.strip()} ({wl} {sc})")
