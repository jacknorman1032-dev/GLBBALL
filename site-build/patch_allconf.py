import sys, os, json, re
# All-Conference tab (Jack, Nov 2, 2026). Reads all_conference.json (project: honors/all_conference.json; copy it next to
# this script) and writes it into the page as ALLCONF, replacing any earlier copy, so re-running after adding seasons
# updates the page. Adds: an "All-Conference" nav tab and view, an all-conference section on each school's People tab,
# and all-conference chips on player cards; also area stat leaders (D['leaders']) on the tab, school pages and player cards. Run after patch_layout (step 5) and patch_freep (step 11).
HERE = os.path.dirname(os.path.abspath(__file__))
p = sys.argv[1]
data_file = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'all_conference.json')
D = json.load(open(data_file))
D.pop('_note', None)
s = open(p).read()

def rep(a, b):
    global s
    if b in s: return
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b, 1)

# ---- data (replaced every run)
js_data = 'const ALLCONF=' + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + ';'
if 'const ALLCONF=' in s:
    s = re.sub(r'const ALLCONF=.*?;\n', lambda m: js_data + '\n', s, count=1, flags=re.S)
else:
    rep('const SCHOOLS=DATA.schools;\n', 'const SCHOOLS=DATA.schools;\n' + js_data + '\n')

# ---- nav and router
rep('<a href="#honors">Honors</a>\n', '<a href="#honors">Honors</a>\n    <a href="#allconf">All-Conference</a>\n')
if 'allconf:viewAllConf' not in s: rep('honors:viewHonors,', 'honors:viewHonors,allconf:viewAllConf,')
if 'honors:viewHonors2,' not in s and 'honors:viewHonors3,' not in s: rep('honors:viewHonors,allconf:viewAllConf,', 'honors:viewHonors2,allconf:viewAllConf,')

# ---- helpers and view
CODE = r'''
// ---- all-conference (ALLCONF from honors/all_conference.json)
const AC_TEAM={poy:{label:'Player of the Year',short:'POY',rank:0},first:{label:'1st Team',short:'1st Team',rank:1},second:{label:'2nd Team',short:'2nd Team',rank:2},third:{label:'3rd Team',short:'3rd Team',rank:3},hm:{label:'Honorable Mention',short:'Hon. Mention',rank:4},sm:{label:'Special Mention',short:'Special Mention',rank:5},coy:{label:'Coach of the Year',short:'COY',rank:6}};
const AC=ALLCONF.picks;
const AC_PLAYERS=AC.filter(x=>x.team!=='coy');
function acFor(p,s){const k=pkey(p.name),sc=s?[s.id,...(p.also||[]).map(a=>a.school)]:null;return AC_PLAYERS.filter(x=>pkey(x.name)===k&&(!sc||sc.includes(x.school)))}
function acChip(x){return `<span class="chip${x.team==='poy'?' gold':x.team==='first'?' full':''}" title="${esc(x.listed_team||AC_TEAM[x.team].label)}">${esc(x.team==='first'&&x.listed_team&&!/1st|first/i.test(x.listed_team)?x.listed_team:AC_TEAM[x.team].short)}</span>`}
function acChips(p,s){const a=acFor(p,s);if(!a.length)return '';
  const poy=a.filter(x=>x.team==='poy'),top=a.filter(x=>x.team==='first'||x.team==='second'||x.team==='third'),hm=a.filter(x=>x.team==='hm'||x.team==='sm');
  return (poy.length?`<span class="chip gold" title="${esc(poy.map(x=>x.season+' '+x.league).join(', '))}">League POY${poy.length>1?' ×'+poy.length:''}</span>`:'')+
    (top.length?`<span class="chip" title="${esc(top.map(x=>x.season+' '+x.league+' '+(x.listed_team||AC_TEAM[x.team].label)).join(', '))}">All-Conference${top.length>1?' ×'+top.length:''}</span>`:'')+
    (!top.length&&hm.length?`<span class="chip" title="${esc(hm.map(x=>x.season+' '+x.league).join(', '))}">All-Conf. Hon. Mention${hm.length>1?' ×'+hm.length:''}</span>`:'')}
const AC_CAT={scoring:{label:'Scoring',unit:'ppg',fmt:v=>v.toFixed(1)},rebounds:{label:'Rebounds',unit:'rpg',fmt:v=>v.toFixed(1)},assists:{label:'Assists',unit:'apg',fmt:v=>v.toFixed(1)},steals:{label:'Steals',unit:'spg',fmt:v=>v.toFixed(1)},threes:{label:'3-pointers made',unit:'3PM',fmt:v=>String(v)}};
const AC_LEAD=(ALLCONF.leaders||[]).flatMap(L=>L.rows.map(r=>({...r,season:L.season,cat:L.cat,of:L.total||L.rows.length,asof:L.asof||'',src:L.src})));
function leadFor(p,s){const k=pkey(p.name),sc=s?[s.id,...(p.also||[]).map(a=>a.school)]:null;return AC_LEAD.filter(x=>x.school&&pkey(x.name)===k&&(!sc||sc.includes(x.school)))}
function leadChips(p,s){const a=leadFor(p,s);if(!a.length)return '';const by={};a.forEach(x=>(by[x.season]=by[x.season]||[]).push(x));
  return Object.keys(by).sort().map(se=>`<span class="chip" title="${esc('LSJ area statistical leaders, '+se+(by[se][0].asof?' (as of '+by[se][0].asof+')':'')+': '+by[se].map(x=>AC_CAT[x.cat].label+' #'+x.rank).join(', '))}">${se}: ${by[se].map(x=>(x.shown||AC_CAT[x.cat].fmt(x.value))+' '+AC_CAT[x.cat].unit).join(' · ')}</span>`).join('')}
function leadCols(showCat,showSchool){return [
  ...(showCat?[{k:'season',label:'Season'},{k:'cat',label:'Category',sortv:x=>Object.keys(AC_CAT).indexOf(x.cat),fmt:x=>esc(AC_CAT[x.cat].label)}]:[]),
  {k:'rank',label:'Rank',r:1,fmt:x=>x.rank+'<span class="note"> of '+x.of+'</span>'},
  {k:'name',label:'Player',fmt:x=>esc(x.name)+(x.note?` <span class="note" title="${esc(x.note)}">*</span>`:'')},
  ...(showSchool?[{k:'team',label:'School',fmt:x=>x.school&&byId[x.school]?schoolCell(byId[x.school]):esc(x.team)}]:[]),
  {k:'value',label:'Average / total',r:1,fmt:x=>(x.shown||AC_CAT[x.cat].fmt(x.value))+' <span class="note">'+AC_CAT[x.cat].unit+(x.pts?' ('+x.pts+' pts / '+x.gp+' g)':'')+'</span>'}]}
function acCols(showSchool){return [
  {k:'season',label:'Season',sortv:x=>x.season+(9-AC_TEAM[x.team].rank)},
  {k:'name',label:'Name',fmt:x=>esc(x.name)+(x.note?` <span class="note" title="${esc(x.note)}">*</span>`:'')},
  ...(showSchool?[{k:'school',label:'School',sortv:x=>byId[x.school]?.name,fmt:x=>byId[x.school]?schoolCell(byId[x.school]):esc(x.school)}]:[]),
  {k:'league',label:'League'},
  {k:'team',label:'Team',sortv:x=>-AC_TEAM[x.team].rank,fmt:x=>acChip(x)},
  {k:'pos',label:'Pos',fmt:x=>esc(x.pos||'')},
  {k:'grade',label:'Gr',fmt:x=>esc(x.grade||'')}]}
function acStandings(L){return L.standings.map(r=>{const id=areaId(r[0]);const rec=r[1]!=null?`${r[1]}-${r[2]}`:(r[4]!=null?`${r[4]}-${r[5]} overall`:'');return `${id?`<a class="schoollink" href="#school-${id}">${esc(byId[id].short||r[0])}</a>`:esc(r[0])} ${rec}`}).join(', ')+(L.teams_note?`<br>${esc(L.teams_note)}`:'')}
function acGrade(x){return [x.grade?'Gr. '+x.grade:'',x.pos||''].filter(Boolean).join(' · ')}
function acChampLine(se,lg){const L=ALLCONF.leagues.find(L=>L.season===se&&L.league===lg);if(!L)return '';const top=L.standings.filter(r=>r[3]===1);if(!top.length)return '';
  return 'Champion: '+top.map(r=>{const id=areaId(r[0]);return id?`<a class="schoollink" href="#school-${id}">${esc(byId[id].short||r[0])}</a>`:esc(r[0])}).join(' and ')+(top[0][1]!=null?` (${top[0][1]}-${top[0][2]})`:'')}
function acGroups(rows,limit,opt={}){
  const lgOrder=lg=>{const i=ALLCONF.leagues.findIndex(L=>L.league===lg);return i<0?999:i};
  const g={};rows.forEach(x=>{const k=x.season+'|'+x.league;(g[k]=g[k]||[]).push(x)});
  const keys=Object.keys(g).sort((a,b)=>{const[sa,la]=a.split('|'),[sb,lb]=b.split('|');return sb.localeCompare(sa)||lgOrder(la)-lgOrder(lb)||la.localeCompare(lb)});
  let out='',n=0,cut=false;
  for(const k of keys){if(limit&&n>=limit){cut=true;break}
    const [se,lg]=k.split('|'),xs=g[k].sort((a,b)=>AC_TEAM[a.team].rank-AC_TEAM[b.team].rank||(byId[a.school]?.name||'').localeCompare(byId[b.school]?.name||'')||a.name.localeCompare(b.name));
    const tiers=[...new Set(xs.map(x=>x.team))];n+=xs.length;
    out+=`<div class="acg"><div class="acg-h"><h3>${esc(se)} · ${esc(lg)}</h3><span class="note">${acChampLine(se,lg)}</span></div>`+
      tiers.map(t=>{const ts=xs.filter(x=>x.team===t);const lab=ts[0].team==='first'&&ts[0].listed_team&&!/1st|first/i.test(ts[0].listed_team)?ts[0].listed_team:AC_TEAM[t].label;
        return `<div class="acg-t">${esc(lab)} <span class="num">${ts.length}</span></div><ul class="acl">`+ts.map(x=>{const s=byId[x.school];
          return `<li><span class="acn">${esc(x.name)}${x.note?` <span class="note" title="${esc(x.note)}">*</span>`:''}</span>${opt.noSchool?(acGrade(x)?`<span class="acs">${esc(acGrade(x))}</span>`:''):`<span class="acs">${s?`<a class="schoollink" href="#school-${s.id}">${esc(s.short||s.name)}</a>`:esc(x.school)}${acGrade(x)?' · '+esc(acGrade(x)):''}</span>`}</li>`}).join('')+'</ul>'}).join('')+'</div>'}
  return {html:out,cut};
}
function acSchoolDraw(acs,ld){
  const el=$('#sac');if(!el)return;
  const ses=[...new Set(acs.map(x=>x.season))].sort().reverse();let all=ses.length<=5;
  const draw=()=>{const keep=all?acs:acs.filter(x=>ses.slice(0,5).includes(x.season));
    el.innerHTML=acGroups(keep,0,{noSchool:1}).html+(all?'':`<button class="btn ghost" id="sacmore">Show all ${ses.length} seasons</button>`);
    if(!all)$('#sacmore').onclick=()=>{all=true;draw()}};
  draw();
  const sl=$('#sld');if(!sl||!ld.length)return;
  const bySe={};ld.forEach(x=>{((bySe[x.season]=bySe[x.season]||{})[x.name]=bySe[x.season][x.name]||[]).push(x)});
  sl.innerHTML=Object.keys(bySe).sort().reverse().map(se=>`<div class="acg"><div class="acg-h"><h3>${esc(se)}</h3></div><ul class="acl">`+
    Object.keys(bySe[se]).sort().map(n=>{const xs=bySe[se][n].sort((a,b)=>Object.keys(AC_CAT).indexOf(a.cat)-Object.keys(AC_CAT).indexOf(b.cat));
      return `<li><span class="acn">${esc(n)}</span><span class="acs">${xs.map(x=>`${x.shown||AC_CAT[x.cat].fmt(x.value)} ${AC_CAT[x.cat].unit} <span class="note">(#${x.rank} of ${x.of})</span>`).join(' · ')}</span></li>`}).join('')+'</ul></div>').join('');
}
function honSchoolDraw(hon){
  const el=$('#shon');if(!el||!hon.length)return;
  const ses=[...new Set(hon.map(h=>h.season))].sort().reverse();let all=ses.length<=6;
  const draw=()=>{const keep=all?ses:ses.slice(0,6);
    el.innerHTML=keep.map(se=>{const by={};hon.filter(h=>h.season===se).forEach(h=>(by[h.name]=by[h.name]||[]).push(h));
      const names=Object.keys(by).sort((a,b)=>Math.min(...by[a].map(h=>HON_TIER[h.tier].rank))-Math.min(...by[b].map(h=>HON_TIER[h.tier].rank))||a.localeCompare(b));
      return `<div class="acg"><div class="acg-h"><h3>${esc(se)}</h3></div><ul class="acl">`+names.map(n=>{const hs=by[n].sort((a,b)=>HON_TIER[a.tier].rank-HON_TIER[b.tier].rank);
        const yr=hs.map(h=>h.yr).find(y=>y&&y!=='?'),lv=[...new Set(hs.filter(h=>h.tier!=='dream').map(h=>h.level).filter(Boolean))].join(' / ');
        return `<li><span class="acn">${esc(n)}</span><span class="meta">${hs.map(h=>`<span class="chip${h.tier==='first'||h.tier==='dream'?' gold':h.tier==='second'?' full':''}" title="${esc((h.listed_tier||'')+(h.level_note?' · '+h.level_note:''))}">${esc(h.selector+' '+HON_TIER[h.tier].short)}</span>`).join('')}</span>${lv||yr?`<span class="acs">${esc([lv,yr?yr+'.':''].filter(Boolean).join(' · '))}</span>`:''}</li>`}).join('')+'</ul></div>'}).join('')+
      (all?'':`<button class="btn ghost" id="shonmore">Show all ${ses.length} seasons</button>`);
    if(!all)$('#shonmore').onclick=()=>{all=true;draw()}};
  draw();
}
function honChipFull(h){return `<span class="chip${h.tier==='first'||h.tier==='dream'?' gold':h.tier==='second'?' full':''}" title="${esc((h.listed_tier||'')+(h.level_note?' · '+h.level_note:''))}">${esc(h.selector+' '+HON_TIER[h.tier].short)}</span>`}
function honList(rows,limit){
  const g={};rows.forEach(h=>{(g[h.season]=g[h.season]||{});const k=pkey(h.name)+'|'+h.school;(g[h.season][k]=g[h.season][k]||[]).push(h)});
  let out='',n=0,cut=false;
  for(const se of Object.keys(g).sort().reverse()){if(limit&&n>=limit){cut=true;break}
    const ps=Object.values(g[se]).map(a=>a.sort((x,y)=>HON_TIER[x.tier].rank-HON_TIER[y.tier].rank)).sort((a,b)=>HON_TIER[a[0].tier].rank-HON_TIER[b[0].tier].rank||(byId[a[0].school]?.name||'').localeCompare(byId[b[0].school]?.name||'')||a[0].name.localeCompare(b[0].name));
    n+=ps.length;
    out+=`<div class="acg"><div class="acg-h"><h3>${esc(se)}</h3><span class="note">${ps.length} player${ps.length>1?'s':''}</span></div><ul class="acl">`+ps.map(a=>{const h=a[0],s=byId[h.school];
      const yr=a.map(x=>x.yr).find(y=>y&&y!=='?'),lv=[...new Set(a.filter(x=>x.tier!=='dream').map(x=>x.level).filter(Boolean))].join(' / ');
      return `<li><span class="acn">${esc(h.name)}</span><span class="meta">${a.map(honChipFull).join('')}</span><span class="acs">${s?`<a class="schoollink" href="#school-${s.id}">${esc(s.short||s.name)}</a>`:''}${[lv,yr?yr+'.':''].filter(Boolean).map(x=>' · '+esc(x)).join('')}</span></li>`}).join('')+'</ul></div>'}
  return {html:out,cut};
}
let HON_TAB='sel';
function viewHonors2(){
  setTimeout(()=>{
    const tabs=[...document.querySelectorAll('#hontabs button')];
    const show=t=>{HON_TAB=t;tabs.forEach(b=>b.setAttribute('aria-selected',b.dataset.t===t?'true':'false'));document.querySelectorAll('.honpanel').forEach(p=>p.hidden=p.id!=='honp-'+t)};
    tabs.forEach(b=>b.onclick=()=>show(b.dataset.t));show(HON_TAB);
    let lim=300;
    const draw=()=>{
      const sch=$('#hsch').value,t=$('#htier').value,sel=$('#hsel').value,se=$('#hseason').value,lv=$('#hlevel').value,q=$('#hq').value.trim().toLowerCase();
      const rows=HON.filter(h=>(sch==='all'||h.school===sch)&&(t==='all'||h.tier===t||(t==='lower'&&HON_LOWER.includes(h.tier)))&&(sel==='all'||h.selector===sel)&&(se==='all'||h.season===se)&&(lv==='all'||(h.level||'').startsWith(lv))&&(!q||h.name.toLowerCase().includes(q)||(h.listed_as||'').toLowerCase().includes(q)));
      $('#hcount').textContent=rows.length+(rows.length===1?' selection':' selections');
      const r=honList(rows,lim);
      $('#htbl').innerHTML=(r.html||'<p class="empty">No selections match.</p>')+(r.cut?`<button class="btn ghost" id="hmore">Show all ${rows.length}</button>`:'');
      if(r.cut)$('#hmore').onclick=()=>{lim=0;draw()};
    };
    const allSe=()=>{$('#hseason').value='all'};
    $('#hseason').onchange=()=>{lim=300;draw()};['#htier','#hsel','#hlevel'].forEach(x=>$(x).onchange=draw);
    $('#hsch').onchange=()=>{if($('#hsch').value!=='all')allSe();lim=300;draw()};
    $('#hq').oninput=()=>{if($('#hq').value.trim())allSe();draw()};draw();
    const by=SCHOOLS.map(s=>{const x=HON.filter(h=>h.school===s.id);return {s,name:s.name,top:x.filter(h=>h.tier==='first'||h.tier==='dream').length,second:x.filter(h=>h.tier==='second').length,total:x.length,players:new Set(x.map(h=>pkey(h.name))).size}}).filter(r=>r.total);
    sortTable('hschools',[{k:'name',label:'School',fmt:r=>schoolCell(r.s)},{k:'top',label:'1st / Dream',r:1},{k:'second',label:'2nd',r:1},{k:'total',label:'Total',r:1},{k:'players',label:'Players',r:1}],by,{k:'top',dir:-1});
    const cardHome={};SCHOOLS.forEach(sc=>(sc.notable_players||[]).forEach(p=>(p.also||[]).forEach(o=>{cardHome[pkey(p.name)+'|'+o.school]=sc.id;cardHome[pkey(p.name)+'|'+sc.id]=sc.id})));
    const pm=new Map();HON.forEach(h=>{const k0=pkey(h.name)+'|'+h.school,k=pkey(h.name)+'|'+(cardHome[k0]||h.school);if(!pm.has(k))pm.set(k,[]);pm.get(k).push(h)});
    const multi=[...pm.values()].filter(a=>a.length>1).map(a=>({a:a.sort((x,y)=>x.season.localeCompare(y.season)||HON_TIER[x.tier].rank-HON_TIER[y.tier].rank),top:a.filter(h=>h.tier==='first'||h.tier==='dream').length})).sort((x,y)=>y.a.length-x.a.length||y.top-x.top||x.a[0].season.localeCompare(y.a[0].season));
    let mlim=40;const drawM=()=>{const xs=mlim?multi.slice(0,mlim):multi;
      $('#hmulti').innerHTML=`<ul class="acl acl1">`+xs.map(r=>{const h=r.a.at(-1),scs=[...new Set(r.a.map(x=>x.school))];return `<li><span class="acn">${esc(h.name)} <span class="note">${r.a.length} selections</span></span><span class="acs">${scs.map(id=>byId[id]?`<a class="schoollink" href="#school-${id}">${esc(byId[id].short||byId[id].name)}</a>`:'').join(' · ')}</span><span class="meta">${r.a.map(x=>`<span class="hpick"><span class="note">${esc(x.season)}${scs.length>1?' '+esc(byId[x.school]?.short||''):''}</span> ${honChipFull(x)}</span>`).join('')}</span></li>`}).join('')+'</ul>'+(mlim&&multi.length>mlim?`<button class="btn ghost" id="hmmore">Show all ${multi.length}</button>`:'');
      if(mlim&&multi.length>mlim)$('#hmmore').onclick=()=>{mlim=0;drawM()}};drawM();
  });
  const n=t=>HON.filter(h=>h.tier===t).length;
  const seasons=[...HON_SEASONS].reverse();
  return `<section class="view">
    <div class="block"><div class="eyebrow">All-state selections</div><h1>Honors</h1>
      <p class="lede">Greater Lansing players on the BCAM, Associated Press, Detroit Free Press and UPI all-state teams. Each pick shows who chose the team and the class or division it was listed under. League honors are on the <a href="#allconf">All-Conference</a> page.</p></div>
    <div class="board" id="honboard">
      <div><span class="v">${n('dream')}</span><span class="k">Dream Team</span></div>
      <div><span class="v">${n('first')}</span><span class="k">1st Team</span></div>
      <div><span class="v">${n('second')}</span><span class="k">2nd Team</span></div>
      <div><span class="v">${HON.filter(h=>HON_LOWER.includes(h.tier)).length}</span><span class="k">3rd-6th Team</span></div>
      <div><span class="v">${n('hm')}</span><span class="k">Hon. Mention</span></div>
      <div><span class="v">${new Set(HON.map(h=>pkey(h.name)+'|'+h.school)).size}</span><span class="k">Players</span></div>
    </div>
    <div class="stabs" id="hontabs" role="tablist"><button role="tab" data-t="sel">Selections</button><button role="tab" data-t="multi">Repeat picks</button><button role="tab" data-t="schools">By school</button></div>
    <div class="honpanel block" id="honp-sel">
      <div class="controls">
        <label for="hseason">Season</label><select id="hseason"><option value="all">All</option>${seasons.map((x,i)=>`<option${i===0?' selected':''}>${x}</option>`).join('')}</select>
        <label for="hsch">School</label><select id="hsch"><option value="all">All schools</option>${SCHOOLS.filter(s=>HON.some(h=>h.school===s.id)).map(s=>`<option value="${s.id}">${esc(s.name)}</option>`).join('')}</select>
        <label for="htier">Honor</label><select id="htier"><option value="all">All honors</option><option value="dream">Dream Team</option><option value="first">1st Team</option><option value="second">2nd Team</option><option value="lower">3rd-6th Team</option><option value="special">AP Special Honor</option><option value="hm">Hon. Mention</option></select>
        <label for="hsel">Team</label><select id="hsel"><option value="all">All teams</option><option value="BCAM">BCAM</option><option value="AP">AP</option><option value="Free Press">Free Press</option><option value="UPI">UPI</option></select>
        <label for="hlevel">Class</label><select id="hlevel"><option value="all">All classes</option>${[...new Set(HON.map(h=>h.level).filter(Boolean))].sort().map(l=>`<option>${esc(l)}</option>`).join('')}</select>
        <input type="search" id="hq" placeholder="Search player" aria-label="Search player"><span class="eyebrow num" id="hcount"></span>
      </div>
      <div id="htbl"></div>
    </div>
    <div class="honpanel block" id="honp-multi" hidden><p class="note">Players picked all-state more than once, most selections first.</p><div id="hmulti"></div></div>
    <div class="honpanel block" id="honp-schools" hidden><div id="hschools"></div></div>
    <details class="fold"><summary><span class="eyebrow" style="margin-left:0">About these lists</span></summary><p class="note">BCAM named First through Fifth teams in each class through 2006-07; since 2009-10 its "Best of the BEST" is counted as first team and "BCAM's BEST" as second team, and those lists don't print a class, so picks use the school's class that season. The 2007-08 to 2011-12 BCAM lists call honorable mention "Special Mention"; 2007-08 and 2008-09 had no Best of the BEST, so their BCAM's BEST picks count as second team. BCAM seasons on file: ${esc(BCAM_SEASONS[0]||'')} to ${esc(BCAM_SEASONS.at(-1)||'')}. The Free Press picked a Dream Team across all classes plus class teams; 1968 has AP and UPI teams instead (newspaper strike). A few misspelled names have been corrected; the printed spelling is still searchable.</p></details>
  </section>`;
}
let AC_TAB='teams';
function viewAllConf(){
  const seasons=[...new Set(AC_PLAYERS.map(x=>x.season))].sort().reverse();
  const leagues=[...new Set(ALLCONF.leagues.map(L=>L.league).concat(AC_PLAYERS.map(x=>x.league)))].sort();
  setTimeout(()=>{
    const tabs=[...document.querySelectorAll('#actabs button')];
    const show=t=>{AC_TAB=t;tabs.forEach(b=>b.setAttribute('aria-selected',b.dataset.t===t?'true':'false'));document.querySelectorAll('.acpanel').forEach(p=>p.hidden=p.id!=='acp-'+t)};
    tabs.forEach(b=>b.onclick=()=>show(b.dataset.t));show(AC_TAB);
    let lim=400;
    const draw=()=>{
      const sch=$('#acsch').value,lg=$('#aclg').value,se=$('#acse').value,t=$('#acteam').value,q=$('#acq').value.trim().toLowerCase();
      const rows=AC_PLAYERS.filter(x=>(sch==='all'||x.school===sch)&&(lg==='all'||x.league===lg)&&(se==='all'||x.season===se)&&(t==='all'||x.team===t)&&(!q||x.name.toLowerCase().includes(q)||(x.listed_as||'').toLowerCase().includes(q)));
      $('#account').textContent=rows.length+(rows.length===1?' selection':' selections');
      const r=acGroups(rows,lim);
      $('#actbl').innerHTML=(r.html||'<p class="empty">No selections match.</p>')+(r.cut?`<button class="btn ghost" id="acmore">Show all ${rows.length}</button>`:'');
      if(r.cut)$('#acmore').onclick=()=>{lim=0;draw()};
    };
    const allSeasons=()=>{if($('#acse').value!=='all'){$('#acse').value='all'}};
    $('#acse').onchange=()=>{lim=400;draw()};$('#aclg').onchange=draw;$('#acteam').onchange=draw;
    $('#acsch').onchange=()=>{if($('#acsch').value!=='all')allSeasons();lim=400;draw()};
    $('#acq').oninput=()=>{if($('#acq').value.trim())allSeasons();draw()};draw();
    const bySe={};ALLCONF.leagues.forEach(L=>(bySe[L.season]=bySe[L.season]||[]).push(L));
    $('#acchamps').innerHTML=Object.keys(bySe).sort().reverse().map(se=>`<div class="acg"><div class="acg-h"><h3>${esc(se)}</h3></div><ul class="acl acl1">`+
      bySe[se].map(L=>{const c=acChampLine(se,L.league);return `<li><span class="acn">${esc(L.league)}</span><span class="acs">${c||'No champion listed'}</span><details class="acst"><summary class="note">Standings</summary><span class="note">${acStandings(L)}</span></details></li>`}).join('')+'</ul></div>').join('');
    if(AC_LEAD.length){const drawL=()=>{const se=$('#lse').value,c=$('#lcat').value;
      const rows=AC_LEAD.filter(x=>x.season===se&&x.cat===c);
      sortTable('ltbl',leadCols(false,true),rows,{k:'rank',dir:1});
      const L=(ALLCONF.leaders||[]).find(L=>L.season===se&&L.cat===c);$('#lsrc').textContent=L?('Source: '+L.src+(L.asof?'. Numbers as of '+L.asof+'.':'')):''};
      ['#lse','#lcat'].forEach(x=>$(x).onchange=drawL);drawL()}
    const by=SCHOOLS.map(s=>{const x=AC_PLAYERS.filter(a=>a.school===s.id);return {s,name:s.name,top:x.filter(a=>['poy','first','second','third'].includes(a.team)).length,hm:x.filter(a=>a.team==='hm'||a.team==='sm').length,total:x.length,titles:ALLCONF.leagues.filter(L=>L.standings.some(r=>r[3]===1&&areaId(r[0])===s.id)).length}}).filter(r=>r.total||r.titles);
    sortTable('acschools',[{k:'name',label:'School',fmt:r=>schoolCell(r.s)},{k:'titles',label:'Titles',r:1},{k:'top',label:'All-Conf.',r:1},{k:'hm',label:'Hon. Men.',r:1},{k:'total',label:'Total',r:1}],by,{k:'top',dir:-1});
  });
  const srcs=[...new Set(ALLCONF.leagues.map(L=>L.src).concat((ALLCONF.leaders||[]).map(L=>L.src)).filter(Boolean))];
  return `<section class="view">
    <div class="block"><div class="eyebrow">League honors</div><h1>All-Conference</h1>
      <p class="lede">All-conference teams and league champions for Greater Lansing schools, from CAAC archives and Lansing State Journal clippings. League names are kept as they were each season. All-state picks are on the <a href="#honors">Honors</a> page.</p></div>
    <div class="board" id="acboard">
      <div><span class="v">${AC_PLAYERS.filter(x=>['poy','first','second','third'].includes(x.team)).length}</span><span class="k">All-Conference</span></div>
      <div><span class="v">${AC_PLAYERS.filter(x=>x.team==='hm'||x.team==='sm').length}</span><span class="k">Hon. Mention</span></div>
      <div><span class="v">${new Set(AC_PLAYERS.map(x=>pkey(x.name)+'|'+x.school)).size}</span><span class="k">Players</span></div>
      <div><span class="v">${seasons.length}</span><span class="k">Seasons</span></div>
    </div>
    <div class="stabs" id="actabs" role="tablist">
      <button role="tab" data-t="teams">Teams</button><button role="tab" data-t="champs">Champions</button>${AC_LEAD.length?'<button role="tab" data-t="leaders">Stat leaders</button>':''}<button role="tab" data-t="schools">By school</button>
    </div>
    <div class="acpanel block" id="acp-teams">
      <div class="controls">
        <label for="acse">Season</label><select id="acse"><option value="all">All</option>${seasons.map((x,i)=>`<option${i===0?' selected':''}>${esc(x)}</option>`).join('')}</select>
        <label for="aclg">League</label><select id="aclg"><option value="all">All</option>${leagues.map(l=>`<option>${esc(l)}</option>`).join('')}</select>
        <label for="acsch">School</label><select id="acsch"><option value="all">All schools</option>${SCHOOLS.filter(s=>AC_PLAYERS.some(x=>x.school===s.id)).map(s=>`<option value="${s.id}">${esc(s.name)}</option>`).join('')}</select>
        <label for="acteam">Team</label><select id="acteam"><option value="all">All</option>${Object.keys(AC_TEAM).filter(k=>AC_PLAYERS.some(x=>x.team===k)).map(k=>`<option value="${k}">${AC_TEAM[k].label}</option>`).join('')}</select>
        <input type="search" id="acq" placeholder="Search player" aria-label="Search player"><span class="eyebrow num" id="account"></span>
      </div>
      <div id="actbl"></div>
    </div>
    <div class="acpanel block" id="acp-champs" hidden><p class="note">Champions as the league sheets or game logs show them; tap Standings for the full table.</p><div id="acchamps"></div></div>
    ${AC_LEAD.length?`<div class="acpanel block" id="acp-leaders" hidden>
      <p class="note">Season leaders from the Lansing State Journal's area lists, for players from schools on this site (plus a few transfers). Ranks are from the paper's full area list, so a player missing from a list may simply have missed the cut.</p>
      <div class="controls">
        <label for="lse">Season</label><select id="lse">${[...new Set(AC_LEAD.map(x=>x.season))].sort().reverse().map(x=>`<option>${esc(x)}</option>`).join('')}</select>
        <label for="lcat">Category</label><select id="lcat">${Object.keys(AC_CAT).filter(k=>AC_LEAD.some(x=>x.cat===k)).map(k=>`<option value="${k}">${AC_CAT[k].label}</option>`).join('')}</select>
      </div><div id="ltbl"></div><p class="note" id="lsrc"></p></div>`:''}
    <div class="acpanel block" id="acp-schools" hidden><div id="acschools"></div></div>
    <details class="fold"><summary><span class="eyebrow" style="margin-left:0">Sources (${srcs.length})</span></summary><ul class="note acsrc">${srcs.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></details>
  </section>`;
}
'''
i = s.find('// ---- all-conference (ALLCONF')
if i >= 0:
    j = s.index('function viewHonors(){', i)
    s = s[:i] + s[j:]
rep('function viewHonors(){', CODE.lstrip('\n') + 'function viewHonors(){')

# ---- styles for the All-Conference view (mobile layout, Nov 2, 2026)
CSS = '.acg{display:grid;gap:6px;padding:10px 0;border-top:1px solid var(--line)}\n.acg-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px}\n.acg-h h3{font-size:17px}\n.acg-t{font-family:var(--cond);font-weight:600;font-size:13px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin-top:4px}\n.acl{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr));gap:0 18px}\n.acl li{display:grid;gap:1px;padding:6px 0;border-bottom:1px solid var(--line);min-width:0;align-content:start}\n.acl.acl1{grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr))}\n.acn{font-weight:600}\n.acs{font-size:14px;color:var(--muted)}\n.acst summary{cursor:pointer}\n.acsrc{padding-left:18px;display:grid;gap:4px}\n.ccards{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr));gap:12px}.ccard{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:14px;display:grid;gap:4px;align-content:start;min-width:0}.ccard .pn{font-weight:700;font-size:18px;line-height:1.2}.ccard .ps{font-family:var(--cond);font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}.ccard p{margin:4px 0 0;font-size:15px;line-height:1.5}@media (max-width:640px){#coaches .tbl{overflow:visible}#coaches thead{display:none}#coaches table,#coaches tbody{display:block}#coaches tr{display:flex;flex-wrap:wrap;gap:2px 12px;padding:9px 12px;border-bottom:1px solid var(--line)}#coaches tr:last-child{border-bottom:0}#coaches td{display:block;padding:0;border:0;white-space:normal;text-align:left;font-size:14px;color:var(--muted)}#coaches td:first-child{flex-basis:100%;font-weight:600;font-size:15px;color:var(--ink)}#coaches td:nth-child(3){color:var(--ink);font-weight:600}#coaches td:nth-child(5)::before{content:\"District titles+ \"}#coaches td:nth-child(6)::before{content:\"Final Fours \"}#coaches td:nth-child(7)::before{content:\"State titles \"}}\n.actitles{display:grid;gap:6px}\n#honboard{grid-template-columns:repeat(6,1fr)}\n.hpick{white-space:nowrap}\n@media (max-width:640px){#hontabs button{padding:8px 9px;font-size:14px}#honboard{grid-template-columns:repeat(3,1fr)}#honboard div{padding:8px 6px}#honboard .v{font-size:20px}#honboard .k{font-size:10px;letter-spacing:.04em}#honp-sel .controls select{flex:1 1 40%;min-width:0}#honp-sel .controls label{display:none}#hq{flex:1 1 100%}}\n.acl .meta{display:flex;flex-wrap:wrap;align-items:flex-start;gap:4px;margin:3px 0 1px}\n#sac .acg:first-child{border-top:0}\n#acboard{grid-template-columns:repeat(4,1fr)}\n@media (max-width:640px){#actabs button{padding:8px 9px;font-size:14px}#acboard{grid-template-columns:repeat(4,1fr)}#acboard div{padding:8px 6px}#acboard .v{font-size:20px}#acboard .k{font-size:10px;letter-spacing:.04em}#acp-teams .controls select,#acp-leaders .controls select{flex:1 1 40%;min-width:0}#acp-teams .controls label,#acp-leaders .controls label{display:none}#acq{flex:1 1 100%}}\n'
i0 = s.find('.acg{display:grid')
if i0 >= 0:
    s = s[:i0] + s[s.index('</style>', i0):]
if True:
    k = s.find('</style>\n\n<header')
    if k < 0: k = s.find('</style>')
    s = s[:k] + CSS + s[k:]

# ---- school page coaches (Jack, Nov 2, 2026): notable coaches as cards instead of a three-column table; the
# "Every coach's record" table turns into stacked labeled rows on phones (CSS below)
rep('<h3>Notable coaches</h3><div class="tbl"><table><thead><tr><th>Coach</th><th>Years</th><th>Notes</th></tr></thead><tbody>${nc.map(c=>`<tr><td>${esc(c.name)}</td><td class="wrapok">${esc(c.years)}</td><td class="wrapok">${esc(c.notes)}</td></tr>`).join(\'\')}</tbody></table></div>', '<h3>Notable coaches</h3><div class="ccards">${nc.map(c=>`<div class="ccard"><div class="pn">${esc(c.name)}</div><div class="ps">${esc(c.years)}</div><p>${esc(c.notes)}</p></div>`).join(\'\')}</div>')

# ---- player cards: all-conference chips after the all-state chips
if '${acChips(p,s)}' not in s:
    if '${acChips(p)}' in s: s = s.replace('${acChips(p)}', '${acChips(p,s)}', 1)
    else: rep('${honorChips(p)}${p.pro?', '${honorChips(p)}${acChips(p,s)}${p.pro?')
rep('${acChips(p,s)}${p.pro?', '${acChips(p,s)}${leadChips(p,s)}${p.pro?')

# ---- school page, People tab: section after All-state honors
anchor = "setTimeout(()=>sortTable('shon',honorCols(false),hon,{k:'season',dir:-1}))}\n"
add = anchor + """  if(hon.length)setTimeout(()=>honSchoolDraw(hon));
  {const acs=AC_PLAYERS.filter(x=>x.school===s.id),lt=ALLCONF.leagues.filter(L=>L.standings.some(r=>r[3]===1&&areaId(r[0])===s.id)).sort((a,b)=>b.season.localeCompare(a.season)),ld=AC_LEAD.filter(x=>x.school===s.id);
   if(acs.length||lt.length||ld.length){pe+=`<details class="block fold"><summary><h2>All-conference</h2><span class="eyebrow num">${acs.length} selections${lt.length?' · '+lt.length+' league title'+(lt.length>1?'s':''):''}</span></summary><div class="fold-body">${lt.length?`<div class="actitles"><span class="eyebrow">League titles</span><div class="meta">${lt.map(L=>`<span class="chip">${esc(L.season+' '+L.league)}</span>`).join('')}</div></div>`:''}<div id="sac"></div>${ld.length?`<h3>Area stat leaders</h3><div id="sld"></div>`:''}<a class="note" href="#allconf">All schools</a></div></details>`;setTimeout(()=>acSchoolDraw(acs,ld))}}
"""
i = s.find("  if(hon.length)setTimeout(()=>honSchoolDraw(hon));")
if i < 0: i = s.find("  {const acs=AC")
if i >= 0:
    j = s.index("\n", s.index("  {const acs=AC", i)) + 1
    j = s.index("\n", j) + 1
    s = s[:i] + s[j:]
rep(anchor, add)

# ---- name suffixes (formerly patch_suffix.py; folded in because the project is out of room)
# Name suffixes (Jack, Nov 2, 2026): every name ending in Jr., Sr., II, III or IV gets a comma before the suffix
# ("Brandon Johns Jr." -> "Brandon Johns, Jr."; "Derek Thomas II" -> "Derek Thomas, II"). Rewrites every "name" field in
# DATA (honors, notable players and coaches, Mr. Basketball, LSJ Player of the Year) and in ALLCONF (picks and stat
# leaders). listed_as and prose are left as printed. Then drops any honors entry that became an exact duplicate, so
# re-running an earlier patch that still uses the old spelling (patch_confirmed's Brandon Johns Jr.) is harmless.
# Run LAST, after every other patch (step 13). Card matching is unaffected: pkey() already strips these suffixes.
SUF = re.compile(r'^(.*?[^,\s])\s+(Jr\.?|Sr\.?|II|III|IV)$')
def fix(n):
    m = SUF.match(n)
    if not m: return n
    suf = m.group(2).rstrip('.')
    return '%s, %s%s' % (m.group(1), suf, '.' if suf in ('Jr', 'Sr') else '')
changed = []
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'name' and isinstance(v, str):
                f = fix(v)
                if f != v: o[k] = f; changed.append(v)
            else: walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
for var in ('DATA', 'ALLCONF'):
    key = 'const %s=' % var
    i = s.find(key)
    if i < 0: continue
    i += len(key); j = s.index(';\n', i)
    D = json.loads(s[i:j]); walk(D)
    if var == 'DATA':
        # school-specific renames (Jack, Nov 2, 2026) for names that come from the build's honors file
        RENAME = {('sexton', 'Kivon Brown'): 'Kivon Brown, Jr.', ('sexton', 'Willie Brown'): 'Willie Brown, Jr.',
                  # Jack, Nov 3, 2026: Kayden is the correct spelling (BCAM printed Kaden; kept in listed_as)
                  ('portland', 'Kaden Dickerson'): 'Kayden Dickerson',
                  # BCAM 2019-20 printed 'Browson Sysum' (Eaton Rapids); he is Bronson Sysum on the CAAC and LSJ lists
                  ('eaton-rapids', 'Browson Sysum'): 'Bronson Sysum',
                  # Jack, Nov 8, 2026: BCAM 2009-10 'Zachary Wedesky' (Fowlerville) is Zach Wedesky on the CAAC lists
                  ('fowlerville', 'Zachary Wedesky'): 'Zach Wedesky',
                  # Jack, Nov 9, 2026: BCAM's 'Michael Bailey' (Waverly) is Mike Bailey on the CAC and LSJ lists
                  ('waverly', 'Michael Bailey'): 'Mike Bailey'}
        # player-card fixes (Jack, Nov 2, 2026): Paul Stoll was a senior in 2002-03 (LSJ CAC all-league), so Class of 2003
        GRAD = {('east-lansing', 'Paul Stoll'): '2003'}
        for sc in D['schools']:
            for pl in sc.get('notable_players', []):
                g = GRAD.get((sc['id'], pl.get('name')))
                if g and pl.get('grad_year') != g: pl['grad_year'] = g; changed.append(pl['name'] + ' grad ' + g)
        for h in D['honors']:
            nn = RENAME.get((h.get('school'), h.get('name')))
            if nn:
                if not h.get('listed_as'): h['listed_as'] = h['name']
                h['name'] = nn; changed.append(nn)
        seen, out = set(), []
        for h in D['honors']:
            k = json.dumps(h, sort_keys=True)
            if k in seen: continue
            seen.add(k); out.append(h)
        dropped = len(D['honors']) - len(out); D['honors'] = out
    s = s[:i] + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + s[j:]

open(p, 'w').write(s)
print('ok', p, len(D['picks']) if 'picks' in D else '', 'picks; suffix fixes:', len(changed), '; duplicate honors dropped:', dropped)
