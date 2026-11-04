import sys, os, json, re
# LSJ Dream Team and all-area (Jack, Nov 3, 2026). Reads honors/lsj_all_area.json and writes it into the page as
# ALLAREA, replacing any earlier copy, so re-running after adding seasons updates the page. Adds:
#   - an "LSJ All-Area" tab on the Honors page (router points honors to viewHonors3, which wraps viewHonors2),
#   - an "LSJ Dream Team / All-Area" section on each school's People tab (after All-conference),
#   - AA_PLAYERS / aaChip helpers that patch_profiles.py uses for profile chips, the season timeline and the
#     directory's honor filter.
# Teams: poy, poyf (Player of the Year finalist, 2021-22), dream, first, second, area, hm, coy.
# Usage: python3 -I patch_allarea.py page.html [lsj_all_area.json]. Run after step 13 and before patch_profiles.py.
HERE = os.path.dirname(os.path.abspath(__file__))
p = sys.argv[1]
data_file = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'honors', 'lsj_all_area.json')
D = json.load(open(data_file))
D.pop('_note', None)
s = open(p).read()

def rep(a, b):
    global s
    if b in s: return
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b, 1)

# ---- data (replaced every run)
js_data = 'const ALLAREA=' + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + ';'
if 'const ALLAREA=' in s:
    s = re.sub(r'const ALLAREA=.*?;\n', lambda m: js_data + '\n', s, count=1, flags=re.S)
else:
    m = re.search(r'const ALLCONF=.*?;\n', s, flags=re.S)
    assert m, 'ALLCONF missing: run patch_allconf.py first'
    s = s[:m.end()] + js_data + '\n' + s[m.end():]

CODE = r'''// ---- LSJ all-area (patch_allarea.py)
const AA_TEAM={poy:{label:'LSJ Player of the Year',short:'LSJ POY',rank:0},poyf:{label:'Player of the Year Finalist',short:'LSJ POY Finalist',rank:0.5},dream:{label:'Dream Team',short:'LSJ Dream Team',rank:1},first:{label:'All-Area 1st Team',short:'All-Area 1st',rank:2},second:{label:'All-Area 2nd Team',short:'All-Area 2nd',rank:3},area:{label:'All-Area',short:'All-Area',rank:4},hm:{label:'All-Area Hon. Mention',short:'All-Area HM',rank:5},coy:{label:'Coach of the Year',short:'COY',rank:6}};
const AA=(typeof ALLAREA!=='undefined'?ALLAREA.picks:[]).filter(x=>byId[x.school]);
const AA_PLAYERS=AA.filter(x=>x.team!=='coy');
const AA_TOP=x=>x.team==='poy'||x.team==='poyf'||x.team==='dream';
function aaLabel(x){return x.team==='coy'?(x.division?x.division+' Coach of the Year':'Coach of the Year'):x.team==='area'&&x.division?'All-Area · '+x.division:AA_TEAM[x.team].label}
function aaChip(x,long){const t=AA_TEAM[x.team];return `<span class="chip${AA_TOP(x)?' gold':x.team==='first'?' full':''}" title="${esc(['LSJ',x.season,aaLabel(x),x.listed_as?'listed as '+x.listed_as:'',x.note||''].filter(Boolean).join(' · '))}">${esc(long?(x.team==='poy'?'LSJ Player of the Year':x.team==='poyf'?'LSJ POY Finalist':x.team==='dream'?'LSJ Dream Team':'LSJ '+aaLabel(x)):t.short)}</span>`}
function aaName(x){return typeof plink==='function'&&x.team!=='coy'?plink(x.name,x.school,x.season):esc(x.name)}
const aaLast=n=>n.replace(/,? (Jr\.|Sr\.|II|III|IV)$/,'').split(' ').pop();
const AA_GR={'9':'Fr.','10':'So.','11':'Jr.','12':'Sr.'};
function aaGroups(rows,opt={}){
  const g={};rows.forEach(x=>(g[x.season]=g[x.season]||[]).push(x));
  return Object.keys(g).sort().reverse().map(se=>{
    const xs=g[se],info=(ALLAREA.seasons||[]).find(S=>S.season===se)||{};
    const grp=[];const key=x=>x.team==='coy'?'coy':x.team+'|'+(AA_TOP(x)?'':x.division||'');
    xs.slice().sort((a,b)=>(a.team==='coy')-(b.team==='coy')||AA_TEAM[a.team].rank-AA_TEAM[b.team].rank||(a.division||'').localeCompare(b.division||'')||aaLast(a.name).localeCompare(aaLast(b.name))).forEach(x=>{const k=key(x);if(!grp.length||grp.at(-1)[0]!==k)grp.push([k,[]]);grp.at(-1)[1].push(x)});
    const nPl=xs.filter(x=>x.team!=='coy').length;
    return `<div class="acg"><div class="acg-h"><h3>${esc(se)}</h3><span class="note">${opt.school?'':nPl+' Greater Lansing pick'+(nPl===1?'':'s')+(info.full_counts?' of '+Object.entries(info.full_counts).filter(([k])=>k!=='coy').reduce((a,[,v])=>a+v,0)+' on the full list':'')}</span></div>`+
      grp.map(([k,ys])=>{const x0=ys[0],lab=k==='coy'?'Coaches of the Year':x0.team==='area'?'All-Area'+(x0.division?' · '+x0.division:''):AA_TEAM[x0.team].label+(x0.division?' · '+x0.division:'');
        return `<div class="acg-t">${esc(lab)} <span class="num">${ys.length}</span></div><ul class="acl">`+ys.map(x=>{const sc=byId[x.school];
          const meta=[AA_GR[x.grade]||'',k==='coy'&&x.division?x.division:''].filter(Boolean).join(' · ');
          return `<li><span class="acn">${aaName(x)}${x.note?` <span class="note" title="${esc(x.note)}">*</span>`:''}</span>${opt.school?(meta?`<span class="acs">${esc(meta)}</span>`:''):`<span class="acs"><a class="schoollink" href="#school-${sc.id}">${esc(sc.short||sc.name)}</a>${meta?' · '+esc(meta):''}</span>`}</li>`}).join('')+'</ul>'}).join('')+
      (!opt.school&&(info.teams_note||info.left_out)?`<p class="note">${esc([info.teams_note,info.left_out?'Not shown: '+info.left_out:''].filter(Boolean).join(' '))}</p>`:'')+'</div>'}).join('');
}
function aaPanel(){
  const el=$('#haa');if(!el)return;
  const draw=()=>{const sc=$('#aasch').value,t=$('#aatier').value,q=$('#aaq').value.trim().toLowerCase();
    const rows=AA.filter(x=>(sc==='all'||x.school===sc)&&(t==='all'||(t==='top'?AA_TOP(x):t==='coy'?x.team==='coy':x.team!=='coy'&&!AA_TOP(x)))&&(!q||x.name.toLowerCase().includes(q)||(x.listed_as||'').toLowerCase().includes(q)));
    $('#aacount').textContent=rows.length+(rows.length===1?' pick':' picks');
    $('#aalist').innerHTML=rows.length?aaGroups(rows):'<p class="empty">No picks match.</p>'};
  ['#aasch','#aatier'].forEach(x=>$(x).onchange=draw);$('#aaq').oninput=draw;draw();
}
function aaPanelHTML(){
  const n=t=>AA.filter(x=>x.team===t).length,se=[...new Set(AA.map(x=>x.season))].sort();
  return `<div class="honpanel block" id="honp-aa" hidden>
    <p class="note">The Lansing State Journal's own honors, picked across every area school and separate from all-state and all-conference: Player of the Year (in 2021-22, three finalists instead), the Dream Team (the area's top players regardless of class or division), then all-area teams${se.length?'. Seasons on file: '+esc(se.length>1?se[0]+' to '+se.at(-1):se[0]):''}. Only schools on this site are listed.</p>
    <div class="board" style="grid-template-columns:repeat(auto-fit,minmax(140px,1fr))"><div><span class="v">${n('poy')}</span><span class="k">Player of the Year</span></div>${n('poyf')?`<div><span class="v">${n('poyf')}</span><span class="k">POY finalists</span></div>`:''}<div><span class="v">${n('dream')}</span><span class="k">Dream Team</span></div><div><span class="v">${AA_PLAYERS.length-n('poy')-n('poyf')-n('dream')}</span><span class="k">All-Area</span></div><div><span class="v">${n('coy')}</span><span class="k">Coach of the Year</span></div></div>
    <div class="controls" id="haa">
      <label for="aasch">School</label><select id="aasch"><option value="all">All schools</option>${SCHOOLS.filter(s=>AA.some(x=>x.school===s.id)).map(s=>`<option value="${s.id}">${esc(s.name)}</option>`).join('')}</select>
      <label for="aatier">Honor</label><select id="aatier"><option value="all">All honors</option><option value="top">Player of the Year / Dream Team</option><option value="area">All-Area</option><option value="coy">Coach of the Year</option></select>
      <input type="search" id="aaq" placeholder="Search player" aria-label="Search player"><span class="eyebrow num" id="aacount"></span>
    </div>
    <div id="aalist"></div>
    <details class="fold"><summary><span class="eyebrow" style="margin-left:0">Sources</span></summary><ul class="note acsrc">${[...new Set((ALLAREA.seasons||[]).map(S=>S.src))].map(x=>`<li>${esc(x)}</li>`).join('')}</ul></details>
  </div>`;
}
function viewHonors3(){
  let h=viewHonors2();
  if(!AA.length)return h;
  h=h.replace('<button role="tab" data-t="schools">By school</button>','<button role="tab" data-t="schools">By school</button><button role="tab" data-t="aa">LSJ All-Area</button>');
  h=h.replace('<div class="honpanel block" id="honp-schools" hidden>',aaPanelHTML()+'<div class="honpanel block" id="honp-schools" hidden>');
  h=h.replace('League honors are on the <a href="#allconf">All-Conference</a> page.','League honors are on the <a href="#allconf">All-Conference</a> page; the LSJ Dream Team and all-area teams are under the LSJ All-Area tab.');
  setTimeout(aaPanel);
  return h;
}
function aaSchoolSec(s){
  const xs=AA.filter(x=>x.school===s.id);if(!xs.length)return '';
  const top=xs.filter(AA_TOP),pl=xs.filter(x=>x.team!=='coy'),ls=[...new Set(xs.map(x=>x.season))].sort().pop(),lt=pl.filter(x=>x.season===ls).sort((a,b)=>AA_TEAM[a.team].rank-AA_TEAM[b.team].rank);
  const pv=`<div class="pv">${top.length?`<div class="pv-c"><span class="pv-x f">${top.length} Dream Team${top.some(x=>x.team==='poy'||x.team==='poyf')?' / POY':''}</span></div>`:''}${lt.length?`<p class="pv-t">Latest, ${esc(ls)}: ${lt.slice(0,2).map(x=>`<b>${esc(x.name)}</b> (${esc(AA_TEAM[x.team].short)})`).join(', ')}${lt.length>2?` and ${lt.length-2} more`:''}</p>`:''}<span class="pv-more">See all picks</span></div>`;
  return `<details class="block fold"><summary><h2>LSJ Dream Team / All-Area</h2><span class="eyebrow num">${pl.length} pick${pl.length===1?'':'s'}</span>${pv}</summary><div class="fold-body">${aaGroups(xs,{school:true})}<a class="note" href="#lsj">All schools</a></div></details>`;
}
// ---- end LSJ all-area
'''
i = s.find('// ---- LSJ all-area (patch_allarea.py)')
if i >= 0:
    j = s.index('// ---- end LSJ all-area\n', i) + len('// ---- end LSJ all-area\n')
    s = s[:i] + s[j:]
# insert ahead of the profiles block (its startup code reads AA_PLAYERS), else ahead of route()
k = s.find('// ---- player profiles (patch_profiles.py)')
if k < 0: k = s.index('function route(){')
s = s[:k] + CODE + s[k:]

# ---- router and school People tab
if 'honors:viewHonors3,' not in s:
    rep('honors:viewHonors2,', 'honors:viewHonors3,')
rep('  const nc=s.notable_coaches||[];\n  if(a||nc.length){',
    '  pe+=aaSchoolSec(s);\n  const nc=s.notable_coaches||[];\n  if(a||nc.length){')

open(p, 'w').write(s)
print('ok', p, 'all-area picks:', len(D['picks']))
