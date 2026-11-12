import sys
# Program records as cards (Jack, Nov 11, 2026). Replaces the two-column Program records table on school pages
# (Records tab), whose right column was cut off on phones, with one card per record type: a heading, then each
# entry on its own line with the number in bold, the season or opponent (linked when it's a covered school) and,
# under it, the date written out (Jan 4, 2011) plus the result. Same records and counts as patch_records.py.
# On phones the Most-played opponents table gets tighter padding so its Win % column fits.
# On desktop the two columns (records cards, opponents table) no longer stretch, which pushed the opponents table down.
# Longest win streaks shows the top five runs (season span, then dates) (Jack, Nov 12, 2026).
# Worst losses (Jack, Nov 12, 2026) sits next to Biggest wins: five widest losing margins, forfeits left out.
# Biggest wins skips the games in BW_SKIP (EL's 61-4 over Grand Ledge in 1931, Jack, Nov 11, 2026).
# Run after patch_records.py. Usage: python3 -I patch_records_cards.py page.html. Re-runnable.
p = sys.argv[1]
s = open(p).read()
OLD_START = "$('#records').innerHTML=`<div class=\"tbl\"><table><tbody>"
OLD_END = "</tbody></table></div>${a.perf.length?'<p class=\"note\">Individual leaders exist only for games where box scores were found.</p>':''}`;"
NEW = r"""{// program records cards (patch_records_cards.py)
  // games left out of Biggest wins (still in the logs and records): EL's 61-4 over Grand Ledge, 1/22/1931 (Jack, Nov 11, 2026)
  const BW_SKIP=['east-lansing|1931-01-22|Grand Ledge'];
  const lk=n=>areaId(n)?`<a class="schoollink" href="#school-${areaId(n)}">${esc(n)}</a>`:esc(n);
  const grp=(t,items)=>items.length?`<div class="prec"><h3>${t}</h3><ol>${items.join('')}</ol></div>`:'';
  const li=(v,main,sub)=>`<li><b>${v}</b><span class="pm">${main}</span>${sub?`<span class="note">${sub}</span>`:''}</li>`;
  const coach=b=>b.coaches&&b.coaches.length?' · '+esc(b.coaches.join(' / ')):'';
  // top 5 win streaks across all games in date order (Jack, Nov 12, 2026); same rule as a.streak: any non-win ends a run
  const runs=(()=>{const gs=a.seasons.flatMap(x=>x.games).slice().sort((x,y)=>(x[0]||x[1]).localeCompare(y[0]||y[1]));const out=[];let c=null;
    gs.forEach(g=>{if(g[5]==='W'){if(!c)c={len:0,s0:g[1],d0:g[0]};c.len++;c.s1=g[1];c.d1=g[0]}else{if(c)out.push(c);c=null}});if(c)out.push(c);
    return out.filter(r=>r.len>=2).sort((x,y)=>y.len-x.len||(x.d0||'').localeCompare(y.d0||'')).slice(0,5)})();
  const mw=[...a.seasons].sort((x,y)=>y.w-x.w)[0];
  const best=[...a.seasons].filter(x=>x.n>=8).sort((x,y)=>y.p-x.p||y.w-x.w).slice(0,5);
  $('#records').innerHTML=`<div class="precs">${
    grp('Longest win streaks',runs.map(r=>li(r.len,r.s0===r.s1?esc(r.s0):`${esc(r.s0)} to ${esc(r.s1)}`,`${fmtDate(r.d0)} to ${fmtDate(r.d1)}`)))+
    grp('Most wins in a season',[li(mw.w,esc(mw.season),recStr(mw.w,mw.l,mw.t)+coach(mw))])+
    grp('Best seasons',best.map(b=>li(recStr(b.w,b.l,b.t),esc(b.season),fmtPct(b.p)+coach(b))))+
    grp('Most points in a game',a.mostPts.slice(0,5).map(g=>li(g[6],'vs '+lk(g[2]),`${fmtDate(g[0])} · ${g[5]} ${g[6]}-${g[7]}`)))+
    grp('Biggest wins',a.bigWins.filter(g=>!BW_SKIP.includes(s.id+'|'+g[0]+'|'+g[2])).slice(0,5).map(g=>li(`${g[6]}-${g[7]}`,'vs '+lk(g[2]),`${fmtDate(g[0])} · by ${g[6]-g[7]}`)))+
    grp('Worst losses',scored(a.seasons.flatMap(x=>x.games)).filter(g=>g[6]<g[7]).sort((x,y)=>(y[7]-y[6])-(x[7]-x[6])||(x[0]||'').localeCompare(y[0]||'')).slice(0,5).map(g=>li(`${g[6]}-${g[7]}`,'vs '+lk(g[2]),`${fmtDate(g[0])} · by ${g[7]-g[6]}`)))+
    grp('Top individual games found',a.perf.slice(0,5).map(q=>li(q.pts,`${esc(q.name)} vs ${lk(q.g[2])}`,fmtDate(q.g[0]))))
  }</div>${a.perf.length?'<p class="note">Individual leaders exist only for games where box scores were found.</p>':''}`;}"""
CSS = """/* program records cards (patch_records_cards.py) */
.precs{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,280px),1fr));gap:12px}
.prec{border:1px solid var(--line);border-radius:var(--r);background:var(--surface);padding:12px 14px;min-width:0}
.prec h3{font-size:14px;color:var(--muted);margin:0 0 4px}
.prec ol{list-style:none;margin:0;padding:0}
.prec li{display:grid;grid-template-columns:4.8em minmax(0,1fr);column-gap:12px;align-items:center;padding:8px 0;border-top:1px solid var(--line)}
.prec li:first-child{border-top:0}
.prec li b{grid-row:1/3;align-self:center;justify-self:center;text-align:center;font-size:19px;font-variant-numeric:tabular-nums;white-space:nowrap}
.prec .pm{grid-column:2;font-size:15px}
.prec li .note{grid-column:2;font-size:13px}
.two>.block:has(#records),.two>.block:has(#opps){align-content:start}
@media (max-width:640px){#opps th,#opps td{padding-left:7px;padding-right:7px}#opps th:first-child,#opps td:first-child{padding-left:12px;white-space:normal}#opps th:last-child,#opps td:last-child{padding-right:12px}}
/* end program records cards */"""
MARK = '{// program records cards (patch_records_cards.py)'
if MARK in s:
    a = s.index(MARK); b = s.index("found.</p>':''}`;}", a) + len("found.</p>':''}`;}")
    s = s[:a] + NEW + s[b:]
else:
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
