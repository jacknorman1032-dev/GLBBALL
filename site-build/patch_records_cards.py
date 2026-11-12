import sys
# Program records as cards (Jack, Nov 11, 2026). Replaces the two-column Program records table on school pages
# (Records tab), whose right column was cut off on phones, with one card per record type: a heading, then each
# entry on its own line with the number in bold, the season or opponent (linked when it's a covered school) and,
# under it, the date written out (Jan 4, 2011) plus the result. Same records and counts as patch_records.py.
# On phones the Most-played opponents table gets tighter padding so its Win % column fits.
# On desktop the two columns (records cards, opponents table) no longer stretch, which pushed the opponents table down.
# Run after patch_records.py. Usage: python3 -I patch_records_cards.py page.html. Re-runnable.
p = sys.argv[1]
s = open(p).read()
OLD_START = "$('#records').innerHTML=`<div class=\"tbl\"><table><tbody>"
OLD_END = "</tbody></table></div>${a.perf.length?'<p class=\"note\">Individual leaders exist only for games where box scores were found.</p>':''}`;"
NEW = r"""{// program records cards (patch_records_cards.py)
  const lk=n=>areaId(n)?`<a class="schoollink" href="#school-${areaId(n)}">${esc(n)}</a>`:esc(n);
  const grp=(t,items)=>items.length?`<div class="prec"><h3>${t}</h3><ol>${items.join('')}</ol></div>`:'';
  const li=(v,main,sub)=>`<li><b>${v}</b><span class="pm">${main}</span>${sub?`<span class="note">${sub}</span>`:''}</li>`;
  const coach=b=>b.coaches&&b.coaches.length?' · '+esc(b.coaches.join(' / ')):'';
  const mw=[...a.seasons].sort((x,y)=>y.w-x.w)[0];
  const best=[...a.seasons].filter(x=>x.n>=8).sort((x,y)=>y.p-x.p||y.w-x.w).slice(0,5);
  $('#records').innerHTML=`<div class="precs">${
    grp('Longest win streak',[li(st.len,'straight wins',st.start?`${fmtDate(st.start[0])} to ${fmtDate(st.end[0])}`:'')])+
    grp('Most wins in a season',[li(mw.w,esc(mw.season),recStr(mw.w,mw.l,mw.t)+coach(mw))])+
    grp('Best seasons',best.map(b=>li(recStr(b.w,b.l,b.t),esc(b.season),fmtPct(b.p)+coach(b))))+
    grp('Most points in a game',a.mostPts.slice(0,5).map(g=>li(g[6],'vs '+lk(g[2]),`${fmtDate(g[0])} · ${g[5]} ${g[6]}-${g[7]}`)))+
    grp('Biggest wins',a.bigWins.slice(0,5).map(g=>li(`${g[6]}-${g[7]}`,'vs '+lk(g[2]),`${fmtDate(g[0])} · by ${g[6]-g[7]}`)))+
    grp('Top individual games found',a.perf.slice(0,5).map(q=>li(q.pts,`${esc(q.name)} vs ${lk(q.g[2])}`,fmtDate(q.g[0]))))
  }</div>${a.perf.length?'<p class="note">Individual leaders exist only for games where box scores were found.</p>':''}`;}"""
CSS = """/* program records cards (patch_records_cards.py) */
.precs{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,280px),1fr));gap:12px}
.prec{border:1px solid var(--line);border-radius:var(--r);background:var(--surface);padding:12px 14px;min-width:0}
.prec h3{font-size:14px;color:var(--muted);margin:0 0 4px}
.prec ol{list-style:none;margin:0;padding:0}
.prec li{display:grid;grid-template-columns:4.2em minmax(0,1fr);column-gap:12px;align-items:center;padding:8px 0;border-top:1px solid var(--line)}
.prec li:first-child{border-top:0}
.prec li b{grid-row:1/3;align-self:center;justify-self:center;text-align:center;font-size:19px;font-variant-numeric:tabular-nums;white-space:nowrap}
.prec .pm{grid-column:2;font-size:15px}
.prec li .note{grid-column:2;font-size:13px}
.two>.block:has(#records),.two>.block:has(#opps){align-content:start}
@media (max-width:640px){#opps th,#opps td{padding-left:7px;padding-right:7px}#opps th:first-child,#opps td:first-child{padding-left:12px;white-space:normal}#opps th:last-child,#opps td:last-child{padding-right:12px}}
/* end program records cards */"""
if 'program records cards (patch_records_cards.py)' not in s:
    a = s.index(OLD_START); b = s.index(OLD_END, a) + len(OLD_END)
    assert s.count(OLD_START) == 1
    s = s[:a] + NEW + s[b:]
cs = '/* program records cards (patch_records_cards.py) */'
if cs in s:
    a = s.index(cs); b = s.index('/* end program records cards */') + len('/* end program records cards */')
    s = s[:a] + CSS + s[b:]
else:
    i = s.index('</style>'); s = s[:i] + CSS + '\n' + s[i:]
open(p, 'w').write(s)
print('patch_records_cards: ok')
