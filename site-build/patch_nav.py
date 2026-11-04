import sys, re
# Navigation (Jack, Nov 3, 2026). Run LAST, after patch_profiles.py. Adds:
#   1. A search box in the header (players, schools, coaches); on phones it takes the school picker's place.
#   2. A shorter top nav: Home, Programs, Champions, Players, Honors. Rivalries and Add data move to the footer
#      (Rivalries also gets a link on Programs). The old routes (#allconf, #rivalries, #data) keep working.
#   3. One Honors hub: a sub-nav on All-state (#honors), All-conference (#allconf), LSJ All-Area (#lsj) and
#      Mr. Basketball (#mrbasketball, new: winners, finalists and top-10 finishes, BCAM Retro winners and nominees).
#      The LSJ All-Area tab moves out of the All-state page to its own page.
#   4. Tabs in the address: #school-east-lansing/people, #honors/multi, #allconf/leaders, #players/notable, so
#      refresh, Back and shared links land on the same tab. Clicking a tab updates the address without a reload.
# Usage: python3 -I patch_nav.py page.html. Re-runnable: the code block and CSS are replaced on every run.
p = sys.argv[1]
s = open(p).read()

def rep(a, b):
    global s
    if b in s: return
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b, 1)

CODE = r'''// ---- navigation (patch_nav.py)
const STAB_NAME={ov:'overview',hi:'history',pe:'people',re:'records'},STAB_KEY={overview:'ov',history:'hi',people:'pe',records:'re'};
function navBefore(h,sub){
  if(!sub)return;
  if(h.startsWith('school-')&&STAB_KEY[sub]){try{sessionStorage.setItem('stab',STAB_KEY[sub])}catch(e){}}
  else if(h==='honors')HON_TAB=sub;
  else if(h==='allconf')AC_TAB=sub;
  else if(h==='players')P_TAB=sub;
}
const NAV_OF={honors:'honors',allconf:'honors',lsj:'honors',mrbasketball:'honors',rivalries:'programs',data:'home'};
function navAfter(h){
  const cur=h.startsWith('player-')?'players':h.startsWith('school-')?'':(NAV_OF[h]||h||'home');
  document.querySelectorAll('nav.tabs a').forEach(a=>{if(a.getAttribute('href')==='#'+cur)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
  // school pages: put the open tab in the address
  if(h.startsWith('school-')){const b=document.querySelector('.stabs [role=tab][aria-selected="true"]');if(b&&b.id.startsWith('stab-')){const n=STAB_NAME[b.id.slice(5)];if(n&&n!=='overview')history.replaceState(null,'','#'+h+'/'+n)}}
}
// clicking a tab writes it to the address (no reload, so Back still goes to the previous page)
document.addEventListener('click',e=>{
  const b=e.target.closest&&e.target.closest('.stabs [role=tab]');if(!b)return;
  const H=(location.hash||'#home').slice(1).split('/')[0];let sub='';
  if(b.id&&b.id.startsWith('stab-'))sub=STAB_NAME[b.id.slice(5)]||'';
  else if(b.closest('#hontabs,#actabs,#ptabs'))sub=b.dataset.t||'';
  if(!sub)return;
  const first=b.parentElement.querySelector('[role=tab]')===b;
  history.replaceState(null,'','#'+H+(first?'':'/'+sub));
});
// ---- Honors hub
const HUB=[['honors','All-state','All-state'],['allconf','All-conference','All-conf.'],['lsj','LSJ All-Area','LSJ'],['mrbasketball','Mr. Basketball','Mr. Basketball']];
function hubNav(cur){return `<nav class="hubnav" aria-label="Honors">${HUB.map(([k,l,sh])=>`<a href="#${k}"${k===cur?' aria-current="page"':''}><span class="hl">${l}</span><span class="hs" aria-hidden="true">${sh}</span></a>`).join('')}</nav>`}
function withHub(cur,html){return html.replace('<section class="view">','<section class="view">'+hubNav(cur))}
function viewHonorsHub(){if(HON_TAB==='aa')HON_TAB='sel';return withHub('honors',viewHonors2())}
function viewAllConfHub(){return withHub('allconf',viewAllConf())}
function viewLSJ(){
  if(typeof aaPanelHTML!=='function')return withHub('lsj','<section class="view"><p class="empty">No LSJ lists on file.</p></section>');
  setTimeout(aaPanel);
  return withHub('lsj',`<section class="view"><div class="block"><div class="eyebrow">Lansing State Journal</div><h1>LSJ All-Area</h1></div>${aaPanelHTML().replace('<div class="honpanel block" id="honp-aa" hidden>','<div class="block" id="honp-aa">')}</section>`);
}
function mrbProf(name,schoolId,year){const se=(+year-1)+'-'+String(year).slice(-2);return profFor(name,schoolId,se)}
function viewMrb(){
  const W=(DATA.mr_basketball||[]).map(m=>({...m,sid:areaId(m.school)})).filter(m=>m.sid);
  const off=W.filter(m=>!m.retro).sort((a,b)=>b.year.localeCompare(a.year)),retro=W.filter(m=>m.retro).sort((a,b)=>b.year.localeCompare(a.year));
  const fin=(MRV.finalists||[]).filter(f=>byId[f.school]).sort((a,b)=>b.year.localeCompare(a.year)||a.place-b.place);
  const nom=(MRV.retro||[]).filter(f=>!f.winner&&byId[f.school]).sort((a,b)=>b.year.localeCompare(a.year));
  const who=(name,sid,year)=>{const pr=PROF.find(p=>p.school===sid&&(p.mry===year||p.mrf.some(f=>f.year===year)||p.mrn.some(f=>f.year===year)))||mrbProf(name,sid,year);
    return pr?`<a class="plink" href="#player-${pr.id}">${esc(pr.name)}</a>`:esc(name)};
  const sch=sid=>`<a class="schoollink" href="#school-${sid}">${esc(byId[sid].short||byId[sid].name)}</a>`;
  const li=(x,name,sid,meta)=>`<li><span class="acn">${who(name,sid,x.year)}</span><span class="acs">${sch(sid)} · ${esc(meta)}</span></li>`;
  const srcs=[...new Set([...Object.values(MRV.sources||{}),'Wikipedia, Mr. Basketball of Michigan (https://en.wikipedia.org/wiki/Mr._Basketball_of_Michigan)'])];
  return withHub('mrbasketball',`<section class="view">
    <div class="block"><div class="eyebrow">Michigan's top senior</div><h1>Mr. Basketball</h1>
      <p class="lede">Greater Lansing players and the Hal Schram Mr. Basketball award (BCAM and the Detroit Free Press, since 1981): winners, then finalists and top-10 finishes in the voting. BCAM's Retro Mr. Basketball project named winners and nominees for 1920 to 1980.</p></div>
    <div class="board" style="grid-template-columns:repeat(auto-fit,minmax(140px,1fr))"><div><span class="v">${off.length}</span><span class="k">Winners</span></div><div><span class="v">${fin.length}</span><span class="k">Finalists / top 10</span></div><div><span class="v">${retro.length}</span><span class="k">Retro winners</span></div><div><span class="v">${nom.length}</span><span class="k">Retro nominees</span></div></div>
    <div class="block"><h2>Hal Schram Mr. Basketball winners</h2><ul class="acl acl1">${off.map(m=>li(m,m.name,m.sid,m.year+(m.college?' · '+m.college:''))).join('')}</ul></div>
    <div class="block"><h2>Finalists and top-10 finishes</h2><p class="note">Places 1-5 are finalists; 6th and lower are top-10 finishes from years when no short list was named.</p><ul class="acl acl1">${fin.map(f=>li(f,f.name,f.school,f.year+' · '+ORD(f.place)+(f.points?' · '+Number(f.points).toLocaleString('en-US')+' pts':''))).join('')}</ul></div>
    <div class="block"><h2>BCAM Retro Mr. Basketball</h2><h3>Winners</h3><ul class="acl acl1">${retro.map(m=>li(m,m.name,m.sid,m.year)).join('')}</ul><h3>Nominees</h3><ul class="acl acl1">${nom.map(f=>li(f,f.name,f.school,f.year+(f.listed_school&&f.listed_school!==byId[f.school].name?' · '+f.listed_school:''))).join('')}</ul></div>
    <details class="fold"><summary><span class="eyebrow" style="margin-left:0">Sources</span></summary><ul class="note acsrc">${srcs.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></details>
  </section>`);
}
function viewProgramsNav(){const h=viewPrograms();const i=h.indexOf('</p>');return i<0?h:h.slice(0,i+4)+'<p class="note">Head-to-head records between area programs are on the <a href="#rivalries">Rivalries</a> page.</p>'+h.slice(i+4)}
const NAV_VIEWS={honors:viewHonorsHub,allconf:viewAllConfHub,lsj:viewLSJ,mrbasketball:viewMrb,programs:viewProgramsNav};
// ---- search
let GS_IDX=null;
function gsIndex(){
  if(GS_IDX)return GS_IDX;const out=[],norm=t=>String(t).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9 ]/g,' ').replace(/\s+/g,' ').trim();
  SCHOOLS.forEach(s=>out.push({k:norm([s.name,s.short,...(s.aliases||[]),s.nickname||''].join(' ')),label:s.name,sub:[s.nickname,s.city].filter(Boolean).join(' · ')||'School',href:'#school-'+s.id,rank:0}));
  PROF.forEach(p=>{const s=byId[p.school];out.push({k:norm(p.names.map(n=>n[1]).join(' ')+' '+[...p.hon,...p.ac,...p.aa].map(x=>x.listed_as||'').join(' ')),label:p.name,sub:[s.short||s.name,p.grad?'Class of '+p.grad:''].filter(Boolean).join(' · '),href:'#player-'+p.id,rank:1})});
  const seen=new Set();
  SCHOOLS.forEach(s=>{const a=analyze(s);[...(s.notable_coaches||[]).map(c=>({name:c.name,yrs:c.years})),...((a&&a.coaches)||[]).filter(c=>c.name&&c.name!=='Unknown').map(c=>({name:c.name,yrs:c.first===c.last?c.first:c.first+' to '+c.last}))].forEach(c=>{const key=s.id+'|'+norm(c.name);if(seen.has(key))return;seen.add(key);
    out.push({k:norm(c.name),label:c.name,sub:'Coach · '+(s.short||s.name)+(c.yrs?' · '+String(c.yrs).split(' (')[0]:''),href:'#school-'+s.id+'/people',rank:2})})});
  GS_IDX={out,norm};return GS_IDX;
}
function gsFind(q){const {out,norm}=gsIndex();const t=norm(q).split(' ').filter(Boolean);if(!t.length)return [];
  return out.map(x=>{const w=x.k.split(' ');if(!t.every(a=>x.k.includes(a)))return null;const sc=t.reduce((n,a)=>n+(w.some(v=>v.startsWith(a))?0:5),0)+x.rank*2+(w[0].startsWith(t[0])?0:1);return {...x,sc}}).filter(Boolean).sort((a,b)=>a.sc-b.sc||a.label.localeCompare(b.label)).slice(0,8)}
function gsInit(){
  const inp=$('#gsearch'),box=$('#gsres');if(!inp||inp.dataset.ready)return;inp.dataset.ready=1;let sel=0,res=[];
  const close=()=>{box.hidden=true;inp.setAttribute('aria-expanded','false')};
  const go=r=>{if(!r)return;close();inp.value='';inp.blur();location.hash=r.href.slice(1)};
  const draw=()=>{res=gsFind(inp.value);sel=0;if(!inp.value.trim()){close();return}
    box.innerHTML=res.length?res.map((r,i)=>`<a role="option" href="${r.href}" class="gs-r${i===sel?' on':''}" data-i="${i}"><b>${esc(r.label)}</b><span>${esc(r.sub)}</span></a>`).join(''):'<div class="gs-none">No matches</div>';
    box.hidden=false;inp.setAttribute('aria-expanded','true')};
  inp.oninput=draw;inp.onfocus=()=>{if(inp.value.trim())draw()};
  inp.onkeydown=e=>{if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();if(!res.length)return;sel=(sel+(e.key==='ArrowDown'?1:res.length-1))%res.length;box.querySelectorAll('.gs-r').forEach((a,i)=>a.classList.toggle('on',i===sel))}
    else if(e.key==='Enter'){e.preventDefault();go(res[sel])}else if(e.key==='Escape'){close();inp.blur()}};
  box.onmousedown=e=>{const a=e.target.closest('.gs-r');if(a){e.preventDefault();go(res[+a.dataset.i])}};
  inp.onblur=()=>setTimeout(close,120);
}
// Back button (Jack, Nov 3, 2026): top of every page but Home. Steps back through pages visited on the site
// (NAV_STACK; tab clicks rewrite the address and don't count); on a page opened directly, goes to its parent.
const NAV_STACK=[];
function navParent(h){if(h.startsWith('player-'))return '#players';if(h.startsWith('school-'))return '#programs';return {allconf:'#honors',lsj:'#honors',mrbasketball:'#honors',rivalries:'#programs'}[h]||'#home'}
function backBar(h,H0){
  const base=H0.split('/')[0];
  if(NAV_STACK.length>1&&NAV_STACK[NAV_STACK.length-2]===base)NAV_STACK.pop();
  else if(NAV_STACK[NAV_STACK.length-1]!==base)NAV_STACK.push(base);
  if(h==='home'||!h)return;
  const v=$('#app').querySelector('section.view');if(!v)return;
  v.insertAdjacentHTML('afterbegin','<a class="backbtn" href="'+navParent(h)+'" id="backbtn">‹ Back</a>');
  $('#backbtn').onclick=e=>{if(NAV_STACK.length>1){e.preventDefault();history.back()}};
}
// ---- end navigation
'''
i = s.find('// ---- navigation (patch_nav.py)')
if i >= 0:
    j = s.index('// ---- end navigation\n', i) + len('// ---- end navigation\n')
    s = s[:i] + s[j:]
k = s.index('function route(){')
s = s[:k] + CODE + s[k:]

# ---- router: sub-tab in the address, hub views, nav highlight
rep("  const h=(location.hash||'#home').slice(1);\n",
    "  const H0=(location.hash||'#home').slice(1),h=H0.split('/')[0],SUB=decodeURIComponent(H0.split('/')[1]||'');navBefore(h,SUB);\n")
rep("  if(h.startsWith('school-'))html=viewSchool(h.slice(7));",
    "  if(NAV_VIEWS[h])html=NAV_VIEWS[h]();\n  else if(h.startsWith('school-'))html=viewSchool(h.slice(7));")
rep("  $('#schoolpick').value=h.startsWith('school-')?h.slice(7):'';\n",
    "  $('#schoolpick').value=h.startsWith('school-')?h.slice(7):'';\n  navAfter(h);gsInit();\n")
rep("  navAfter(h);gsInit();\n", "  navAfter(h);gsInit();backBar(h,H0);\n")

# ---- top nav: five links (patch_allconf re-adds All-Conference on a re-run; this removes it again)
NAV = '''  <nav class="tabs" aria-label="Sections">
    <a href="#home">Home</a>
    <a href="#programs">Programs</a>
    <a href="#champions">Champions</a>
    <a href="#players">Players</a>
    <a href="#honors">Honors</a>
  </nav>
  <div class="gs" role="search"><input type="search" id="gsearch" placeholder="Search players, schools, coaches" aria-label="Search players, schools and coaches" autocomplete="off" aria-controls="gsres" aria-expanded="false"><div id="gsres" class="gs-res" role="listbox" hidden></div></div>
'''
s, n = re.subn(r'  <nav class="tabs" aria-label="Sections">.*?</nav>\n(  <div class="gs" role="search">.*?</div></div>\n)?', lambda m: NAV, s, count=1, flags=re.S)
assert n == 1, 'nav'

# ---- footer links
FOOT = '  <div class="foot-links"><a href="#rivalries">Rivalries</a> · <a href="#mrbasketball">Mr. Basketball</a> · <a href="#data">Add data</a></div>\n'
if 'class="foot-links"' not in s:
    rep('<div class="wrap foot">\n', '<div class="wrap foot">\n' + FOOT)

# ---- styles
CSS = '''.hubnav{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;border-bottom:1px solid var(--line);margin:-8px 0 0}
.hubnav a{font-family:var(--cond);font-weight:600;font-size:15px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);text-decoration:none;padding:9px 12px;white-space:nowrap;border-radius:var(--r) var(--r) 0 0}
.hubnav a:hover{color:var(--ink);background:var(--sunk)}
.hubnav a[aria-current="page"]{color:var(--ink);box-shadow:inset 0 -3px 0 var(--maple)}
.gs{position:relative;flex:0 1 280px;min-width:0}
.gs input{width:100%;font-size:15px;padding:6px 10px}
.gs-res{position:absolute;top:calc(100% + 4px);left:0;right:0;min-width:260px;z-index:20;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);box-shadow:0 8px 24px rgba(0,0,0,.18);overflow:hidden}
.gs-r{display:grid;gap:1px;padding:8px 12px;color:var(--ink);text-decoration:none;border-top:1px solid var(--line)}
.gs-r:first-child{border-top:0}
.gs-r b{font-weight:600}.gs-r span{font-size:13px;color:var(--muted)}
.gs-r.on,.gs-r:hover{background:var(--sunk)}
.gs-none{padding:10px 12px;color:var(--muted);font-size:14px}
.foot-links a{color:var(--maple-ink)}
.hubnav .hs{display:none}
.backbtn{justify-self:start;font-family:var(--cond);font-weight:600;font-size:15px;letter-spacing:.05em;text-transform:uppercase;color:var(--maple-ink);text-decoration:none;padding:4px 10px 4px 6px;margin:-14px 0 -14px -6px;border-radius:var(--r)}
.backbtn:hover{background:var(--sunk)}
@media (min-width:721px){nav.tabs{flex:0 0 auto}.gs{flex:1 1 200px;max-width:320px;margin-left:auto}}
@media (max-width:720px){.gs{order:2;flex:1 1 0}.schoolpick{display:none}.gs-res{left:auto;right:0;width:min(92vw,360px)}
  nav.tabs{justify-content:space-between;gap:0;margin-inline:-4px}nav.tabs a{font-size:13px;letter-spacing:.01em;padding:6px 4px}
  .hubnav{justify-content:space-between}.hubnav a{font-size:13.5px;letter-spacing:.02em;padding:8px 6px}.hubnav .hl{display:none}.hubnav .hs{display:inline}}
@media (max-width:380px){nav.tabs a{font-size:12px;padding:6px 3px;letter-spacing:0}.hubnav a{font-size:12px;padding:8px 3px;letter-spacing:0}}
'''
i0 = s.find('.hubnav{')
if i0 >= 0:
    s = s[:i0] + s[s.index('</style>', i0):]
k = s.find('</style>\n\n<header')
if k < 0: k = s.find('</style>')
s = s[:k] + CSS + s[k:]

open(p, 'w').write(s)
print('ok', p)
