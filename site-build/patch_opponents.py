import sys
# Opponents section on school pages, Records tab (Jack, Nov 11, 2026). Replaces "Most-played opponents" (top 25).
#   - Every opponent on file, not just the top 25, sortable by name, games, record, win % and last meeting.
#   - Filters: a name search; All opponents / Area schools on this site / League opponents / Postseason
#     opponents / Played once; and a years filter by decade (records recount for those years only).
#   - Tap an opponent for the head-to-head: home / road / neutral and postseason splits, average score,
#     first and last meeting, current streak, then every game against them, newest first.
#   - Program records now run full width above it (its cards sit two or three across on desktop).
# Run after patch_records_cards.py. Usage: python3 -I patch_opponents.py page.html. Re-runnable.
p = sys.argv[1]
s = open(p).read()

def rep(a, b):
    global s
    if b in s: return
    assert s.count(a) == 1, a[:100]
    s = s.replace(a, b, 1)

rep('''<div class="two"><div class="block"><h2>Program records</h2><div id="records"></div></div><div class="block"><h2>Most-played opponents</h2><div id="opps"></div></div></div>''',
    '''<div class="block"><h2>Program records</h2><div id="records"></div></div><div class="block"><div class="head-row"><h2>Opponents</h2><span class="eyebrow num">${a.opponents.length} on file</span></div><div id="oppsbox"></div></div>''')
rep("""sortTable('opps',[{k:'name',label:'Opponent',fmt:r=>r.area?`<a class="schoollink" href="#school-${r.area}">${esc(r.name)}</a>`:esc(r.name)},{k:'n',label:'G',r:1},{k:'w',label:'Record',r:1,fmt:r=>recStr(r.w,r.l,r.t)},{k:'p',label:'Win %',r:1,fmt:r=>fmtPct(r.p)}],a.opponents.slice(0,25),{k:'n',dir:-1});""",
    "oppsDraw(s,a);")

FN = r'''// ---- opponents section (patch_opponents.py)
function oppsDraw(s,a){
  const box=document.getElementById('oppsbox');if(!box)return;
  const dec=g=>Math.floor(+String(g[1]).slice(0,4)/10)*10;
  const decs=[...new Set(a.opponents.flatMap(o=>o.games.map(dec)))].filter(d=>!isNaN(d)).sort((x,y)=>y-x);
  box.innerHTML=`<div class="ofilt">
    <input type="search" id="oq" placeholder="Find an opponent" aria-label="Find an opponent" autocomplete="off">
    <select id="ofl" aria-label="Which opponents"><option value="all">All opponents</option><option value="area">Area schools on this site</option><option value="league">League opponents</option><option value="post">Postseason opponents</option><option value="once">Played once</option></select>
    ${decs.length>1?`<select id="odec" aria-label="Years"><option value="">All years</option>${decs.map(d=>`<option value="${d}">${d}s</option>`).join('')}</select>`:''}
  </div><p class="note" id="osum"></p><div id="opps"></div>`;
  const draw=()=>{
    const q=($('#oq').value||'').trim().toLowerCase(),fl=$('#ofl').value,dv=$('#odec')?$('#odec').value:'';
    let rows=a.opponents.map(o=>{const gs=dv?o.games.filter(g=>dec(g)==dv):o.games;if(!gs.length)return null;
      return {name:o.name,area:o.area,games:gs,...tally(gs),last:gs[gs.length-1]}}).filter(Boolean);
    if(q)rows=rows.filter(r=>r.name.toLowerCase().includes(q));
    if(fl==='area')rows=rows.filter(r=>r.area&&r.area!==s.id);
    else if(fl==='league')rows=rows.filter(r=>r.games.some(g=>g[4]==='League'));
    else if(fl==='post')rows=rows.filter(r=>r.games.some(isPost));
    else if(fl==='once')rows=rows.filter(r=>r.n===1);
    const t=tally(rows.flatMap(r=>r.games));
    $('#osum').textContent=rows.length?`${rows.length} opponent${rows.length>1?'s':''} · ${t.n} games · ${recStr(t.w,t.l,t.t)} (${fmtPct(t.p)}) · tap one for every game`:'No opponents match.';
    sortTable('opps',[
      {k:'name',label:'Opponent',fmt:r=>r.area?`<a class="schoollink" href="#school-${r.area}">${esc(r.name)}</a>`:esc(r.name)},
      {k:'n',label:'G',r:1},
      {k:'w',label:'Record',r:1,fmt:r=>recStr(r.w,r.l,r.t)},
      {k:'p',label:'Win %',r:1,fmt:r=>fmtPct(r.p)},
      {k:'lastm',label:'Last met',r:1,sortv:r=>r.last[0]||r.last[1],fmt:r=>esc(r.last[1])}
    ],rows,{k:'n',dir:-1,rowAttr:(r,i)=>`class="click" data-i="${i}" tabindex="0" aria-expanded="false"`,after:(el,rs)=>oppExpand(el,rs)});
  };
  $('#oq').oninput=draw;$('#ofl').onchange=draw;if($('#odec'))$('#odec').onchange=draw;
  draw();
}
function oppExpand(el,rs){
  el.querySelectorAll('tr.click').forEach(tr=>{const go=e=>{if(e&&e.target.closest&&e.target.closest('a'))return;
    const open=tr.classList.toggle('open');tr.setAttribute('aria-expanded',open);const nx=tr.nextElementSibling;if(nx&&nx.classList.contains('detail')){nx.remove();return}
    const r=rs[+tr.dataset.i],gs=r.games;
    const sp=(lab,f)=>{const x=tally(gs.filter(f));return x.n?`<span><b>${lab}</b> ${recStr(x.w,x.l,x.t)}</span>`:''};
    const av=avgs(gs);let k=0;const lastRes=gs[gs.length-1][5];for(let i=gs.length-1;i>=0&&gs[i][5]===lastRes;i--)k++;
    const first=gs[0],last=gs[gs.length-1];
    const summ=`<div class="osplit">${sp('Home',g=>g[3]==='H')}${sp('Road',g=>g[3]==='R')}${sp('Neutral',g=>g[3]==='N')}${sp('League',g=>g[4]==='League')}${sp('Postseason',isPost)}${av.pf!=null?`<span><b>Avg score</b> ${fmt1(av.pf)}-${fmt1(av.pa)}</span>`:''}<span><b>Streak</b> ${lastRes}${k}</span><span><b>First met</b> ${first[0]?fmtDate(first[0]):esc(first[1])}</span>${gs.length>1?`<span><b>Last met</b> ${last[0]?fmtDate(last[0]):esc(last[1])}</span>`:''}</div>`;
    const d=document.createElement('tr');d.className='detail';d.innerHTML=`<td colspan="5"><div class="inner">${summ}${gameTable([...gs].reverse())}</div></td>`;tr.after(d)};
    tr.onclick=go;tr.onkeydown=e=>{if(e.key==='Enter'){e.preventDefault();go()}}});
}
// ---- end opponents section
'''
if '// ---- opponents section (patch_opponents.py)' in s:
    a = s.index('// ---- opponents section (patch_opponents.py)'); b = s.index('// ---- end opponents section\n') + len('// ---- end opponents section\n')
    s = s[:a] + FN + s[b:]
else:
    rep('function expandRows(el,rs,cols){', FN + 'function expandRows(el,rs,cols){')

CSS = '''/* opponents section (patch_opponents.py) */
.ofilt{display:flex;flex-wrap:wrap;gap:8px}
.ofilt input,.ofilt select{font:inherit;font-size:15px;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:8px 10px;min-width:0}
.ofilt input{flex:2 1 220px}
.ofilt select{flex:1 1 160px}
#opps tr.open td{background:var(--sunk)}
.osplit{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:14px;color:var(--muted);padding:2px 4px 10px}
.osplit b{font-weight:600;color:var(--ink)}
#opps .detail .inner{position:static;width:auto;padding:10px 10px 14px}
@media (max-width:640px){#opps th:nth-child(5),#opps td:nth-child(5){display:none}#opps th:nth-child(4),#opps td:nth-child(4){padding-right:12px}#opps .detail .inner{padding:8px 6px 12px}.ofilt select{flex:1 1 40%}}
/* end opponents section */'''
cs = '/* opponents section (patch_opponents.py) */'
if cs in s:
    a = s.index(cs); b = s.index('/* end opponents section */') + len('/* end opponents section */')
    s = s[:a] + CSS + s[b:]
else:
    i = s.index('</style>'); s = s[:i] + CSS + '\n' + s[i:]
open(p, 'w').write(s)
print('patch_opponents: ok')
