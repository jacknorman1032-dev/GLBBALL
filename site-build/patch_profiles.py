import sys, os, json, re
# Player profiles (Jack, Nov 3, 2026). Every player with an all-state (DATA.honors), all-conference (ALLCONF.picks) or
# LSJ Dream Team / all-area (ALLAREA.picks, from patch_allarea.py; optional)
# selection gets a profile page at #player-<school>--<name>: honors season by season, class year (from printed grades,
# or inferred), position, LSJ area stat-leader lines, season stats and bio from players/player_stats.json, and the
# notable-player card's text when there is one. The Players tab gets an "All players" directory (default) next to the
# existing Notable cards, and player names on the Honors / All-Conference tabs, school All-conference and All-state
# sections and notable cards link to the profile.
# Usage: python3 -I patch_profiles.py page.html [player_stats.json]. Run LAST (after patch_allarea.py). Re-runnable: the data and
# the code block are replaced on every run, so add stats to the JSON and re-run.
HERE = os.path.dirname(os.path.abspath(__file__))
p = sys.argv[1]
data_file = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'players', 'player_stats.json')
PS = json.load(open(data_file))
PS = {'players': [x for x in PS.get('players', []) if x.get('name')]}
s = open(p).read()

def rep(a, b, optional=False):
    global s
    if b in s: return
    if optional and a not in s: return
    assert s.count(a) == 1, a[:100]
    s = s.replace(a, b, 1)

CODE = r'''// ---- player profiles (patch_profiles.py)
const PSTATS=__PSTATS__;
const PF_AA=typeof AA_PLAYERS!=='undefined'?AA_PLAYERS:[];
const YR_GR={Fr:9,So:10,Jr:11,Sr:12},GR_YR={9:'Fr',10:'So',11:'Jr',12:'Sr'};
const PF=(()=>{
  const home={};SCHOOLS.forEach(sc=>(sc.notable_players||[]).forEach(c=>(c.also||[]).forEach(o=>{const ys=(String(o.seasons||'').match(/\d{4}-\d{2}/g)||[]).map(x=>+x.slice(0,4));home[pkey(c.name)+'|'+o.school]={id:sc.id,a:ys.length?Math.min(...ys):0,b:ys.length?Math.max(...ys):9999}})));
  const aka={};PSTATS.players.forEach(x=>(x.aka||[]).forEach(a=>aka[pkey(a)+'|'+x.school]=pkey(x.name)));
  const keyOf=(n,sc,se)=>{let k=pkey(n);k=aka[k+'|'+sc]||k;const h=home[k+'|'+sc],y=se?+String(se).slice(0,4):null;return k+'|'+(h&&(y==null||(y>=h.a&&y<=h.b))?h.id:sc)};
  const M=new Map();
  const get=(n,sc,se)=>{const k=keyOf(n,sc,se);if(!M.has(k))M.set(k,{k,school:k.split('|')[1],names:[],hon:[],ac:[],aa:[],lead:[],ex:null});return M.get(k)};
  HON.forEach(h=>{if(!byId[h.school])return;const p=get(h.name,h.school,h.season);p.hon.push(h);p.names.push([h.season,h.name])});
  AC_PLAYERS.forEach(x=>{if(!byId[x.school])return;const p=get(x.name,x.school,x.season);p.ac.push(x);p.names.push([x.season,x.name])});
  PF_AA.forEach(x=>{if(!byId[x.school])return;const p=get(x.name,x.school,x.season);p.aa.push(x);p.names.push([x.season,x.name])});
  PSTATS.players.forEach(x=>{if(!byId[x.school])return;const p=get(x.name,x.school);p.ex=x;p.names.push(['9999',x.name])});
  AC_LEAD.forEach(x=>{if(!x.school)return;const k=keyOf(x.name,x.school,x.season);if(M.has(k))M.get(k).lead.push(x)});
  const list=[...M.values()],seen={};
  list.forEach(p=>{
    p.names.sort((a,b)=>b[0].localeCompare(a[0]));p.name=p.names[0][1];
    const s=byId[p.school],nk=p.k.split('|')[0];
    p.card=(s.notable_players||[]).find(c=>pkey(c.name)===nk)||null;
    p.gr={};p.inf={};
    p.ac.forEach(x=>{if(x.grade)p.gr[x.season]=+x.grade});
    p.aa.forEach(x=>{if(x.grade&&!p.gr[x.season])p.gr[x.season]=+x.grade});
    p.hon.forEach(h=>{if(YR_GR[h.yr]&&!p.gr[h.season])p.gr[h.season]=YR_GR[h.yr]});
    ((p.ex&&p.ex.seasons)||[]).forEach(x=>{if(x.grade)p.gr[x.season]=+x.grade});
    const gy={};Object.entries(p.gr).forEach(([se,g])=>{const y=+se.slice(0,4)+13-g;gy[y]=(gy[y]||0)+1});
    let grad=(p.ex&&p.ex.grad_year)||(p.card&&parseInt(p.card.grad_year)?String(parseInt(p.card.grad_year)):'');
    if(!grad){const ys=Object.keys(gy).sort((a,b)=>gy[b]-gy[a]||b-a);if(ys.length)grad=ys[0]}
    p.grad=grad;p.gradNote=Object.keys(gy).length>1?'Printed grades disagree ('+Object.keys(gy).map(y=>'Class of '+y).join(' vs. ')+')':'';
    p.seasons=[...new Set([...p.hon,...p.ac,...p.aa,...p.lead,...((p.ex&&p.ex.seasons)||[])].map(x=>x.season))].sort();
    if(grad)p.seasons.forEach(se=>{if(!p.gr[se]){const g=+se.slice(0,4)+13-(+grad);if(g>=9&&g<=12){p.gr[se]=g;p.inf[se]=1}}});
    const pos={};p.ac.forEach(x=>{if(x.pos)pos[x.pos]=(pos[x.pos]||0)+1});
    p.pos=(p.ex&&p.ex.pos)||Object.keys(pos).sort((a,b)=>pos[b]-pos[a])[0]||'';
    p.best=p.hon.slice().sort((a,b)=>HON_TIER[a.tier].rank-HON_TIER[b.tier].rank)[0]||null;
    p.top=p.ac.filter(x=>['poy','first','second','third'].includes(x.team)).length;
    p.poy=p.ac.filter(x=>x.team==='poy').length;
    p.aab=p.aa.slice().sort((a,b)=>AA_TEAM[a.team].rank-AA_TEAM[b.team].rank)[0]||null;p.dream=p.aa.filter(x=>x.team==='dream'||x.team==='poy'||x.team==='poyf').length;
    p.mr=mrKind(p.card||{name:p.name},s);
    p.id=p.school+'--'+pkey(p.name).replace(/ /g,'-');
    if(seen[p.id])p.id+='-'+(++seen[p.id]);else seen[p.id]=1;
  });
  return {list,keyOf,by:Object.fromEntries(list.map(p=>[p.k,p])),id:Object.fromEntries(list.map(p=>[p.id,p]))};
})();
const PROF=PF.list;
function profFor(n,sc,se){return sc?PF.by[PF.keyOf(n,sc,se)]||null:null}
function plink(n,sc,se){const p=profFor(n,sc,se);return p?`<a class="plink" href="#player-${p.id}">${esc(n)}</a>`:esc(n)}
function profChips(p){
  const b=p.best;
  return (p.mr?`<span class="chip gold">${p.mr==='retro'?'Retro ':''}Mr. Basketball</span>`:'')+
    (b?`<span class="chip${b.tier==='first'||b.tier==='dream'?' gold':''}" title="${esc(p.hon.map(h=>h.season+' '+h.selector+' '+HON_TIER[h.tier].short).join('\n'))}">${esc(b.selector+' '+HON_TIER[b.tier].short)}${p.hon.length>1?' ×'+p.hon.length:''}</span>`:'')+
    (p.poy?`<span class="chip gold">League POY${p.poy>1?' ×'+p.poy:''}</span>`:'')+
    (p.top?`<span class="chip full">All-Conf.${p.top>1?' ×'+p.top:''}</span>`:p.ac.length?`<span class="chip">All-Conf. HM${p.ac.length>1?' ×'+p.ac.length:''}</span>`:'')+
    (p.aab?aaChip(p.aab).replace(/<\/span>$/,(p.aa.length>1?' ×'+p.aa.length:'')+'</span>'):'')+
    (p.ex&&(p.ex.seasons||[]).length?'<span class="chip">Stats</span>':'');
}
function profScore(p){return (p.mr?100:0)+p.hon.reduce((a,h)=>a+Math.max(1,8-HON_TIER[h.tier].rank),0)+p.poy*6+p.top*3+p.ac.length+p.aa.reduce((a,x)=>a+(x.team==='poy'?6:x.team==='poyf'?5:x.team==='dream'?4:2),0)}
const PF_STATS=[['gp','GP',0],['pts','PTS',0],['ppg','PPG',1],['reb','REB',0],['rpg','RPG',1],['ast','AST',0],['apg','APG',1],['stl','STL',0],['spg','SPG',1],['blk','BLK',0],['bpg','BPG',1],['tpm','3PM',0],['fgm','FGM',0],['fga','FGA',0],['fg_pct','FG%',2],['ft_pct','FT%',2]];
function pfVal(x,k,t){const v=x[k];if(v==null||v==='')return '';if(t===1)return typeof v==='number'?v.toFixed(1):esc(v);if(t===2)return typeof v==='number'?(v<=1?(v*100).toFixed(1):v.toFixed(1))+'%':esc(v);return esc(v)}
function pfLine(x){return PF_STATS.filter(([k])=>x[k]!=null&&x[k]!==''&&!['pts','reb','ast','stl','blk','fgm','fga'].includes(k)).map(([k,l,t])=>pfVal(x,k,t)+' '+l.toLowerCase().replace('3pm','3PM').replace('fg%','FG').replace('ft%','FT')).join(' · ')}
function viewProfile(id){
  const p=PF.id[id];if(!p)return viewPlayers2();
  const s=byId[p.school],st=(p.ex&&p.ex.seasons)||[];
  const others=[...new Set([...p.hon,...p.ac,...p.aa].map(x=>x.school))].filter(x=>x!==p.school&&byId[x]);
  const seOf=o=>{const a=[...new Set([...p.hon,...p.ac].filter(x=>x.school===o).map(x=>x.season))].sort();const c=p.card&&(p.card.also||[]).find(x=>x.school===o);return c&&c.seasons?c.seasons:a.length>1?a[0]+' to '+a.at(-1):a[0]||''};
  const sub=[p.grad?'Class of '+p.grad:'',p.pos,p.ex&&p.ex.height].filter(Boolean).map(esc).join(' · ');
  const head=`<div class="shead${s.logo?' has-logo':''}" style="${colorVars(s)}">${s.logo?`<span class="slogo-box"><img class="slogo" src="${esc(s.logo)}" alt="${esc(s.name)} logo" style="--ls:${s.logo_scale||1}"></span>`:''}<div class="stext"><div class="eyebrow"><a href="#school-${s.id}" style="color:inherit">${esc(s.name)}</a></div>${others.length?`<div class="eyebrow">Also played at ${others.map(o=>`<a href="#school-${o}" style="color:inherit">${esc(byId[o].name)}</a>${seOf(o)?' ('+esc(seOf(o))+')':''}`).join(', ')}</div>`:''}<h1>${esc(p.name)}</h1>${sub?`<div class="eyebrow">${sub}</div>`:''}</div></div>`;
  const champ=x=>{const L=ALLCONF.leagues.find(L=>L.season===x.season&&L.league===x.league);const r=L&&L.standings.find(r=>r[3]===1&&areaId(r[0])===x.school);return r?` <span class="acx-ch">League champs${r[1]!=null?' '+r[1]+'-'+r[2]:''}</span>`:''};
  const rows=p.seasons.map(se=>{
    const g=p.gr[se],hs=p.hon.filter(h=>h.season===se).sort((a,b)=>HON_TIER[a.tier].rank-HON_TIER[b.tier].rank),as=p.ac.filter(x=>x.season===se).sort((a,b)=>AC_TEAM[a.team].rank-AC_TEAM[b.team].rank),ls=p.lead.filter(x=>x.season===se).sort((a,b)=>Object.keys(AC_CAT).indexOf(a.cat)-Object.keys(AC_CAT).indexOf(b.cat)),ss=st.filter(x=>x.season===se),aas=p.aa.filter(x=>x.season===se).sort((a,b)=>AA_TEAM[a.team].rank-AA_TEAM[b.team].rank);
    const lines=[];
    if(hs.length)lines.push(`<div class="pf-line"><span class="pf-k">All-state</span>${hs.map(h=>honChipFull(h)+(h.level?`<span class="note">${esc(h.level)}</span>`:'')).join('')}</div>`);
    if(as.length)lines.push(`<div class="pf-line"><span class="pf-k">All-conference</span>${as.map(x=>`<span class="chip${x.team==='poy'?' gold':['first','second','third'].includes(x.team)?' full':''}" title="${esc(x.listed_team||'')}">${esc(x.league+' · '+(x.team==='first'&&x.listed_team&&!/1st|first/i.test(x.listed_team)?x.listed_team:AC_TEAM[x.team].label))}</span>`).join('')}${champ(as[0])}</div>`);
    if(aas.length)lines.push(`<div class="pf-line"><span class="pf-k">LSJ</span>${aas.map(x=>aaChip(x,true)).join('')}</div>`);
    if(ls.length)lines.push(`<div class="pf-line"><span class="pf-k">Area leaders</span><span>${ls.map(x=>`${x.shown||AC_CAT[x.cat].fmt(x.value)} ${AC_CAT[x.cat].unit} <span class="note">(#${x.rank} of ${x.of})</span>`).join(' · ')}</span></div>`);
    ss.forEach(x=>{const l=pfLine(x);if(l||x.note)lines.push(`<div class="pf-line"><span class="pf-k">Stats</span><span>${l}${x.note?` <span class="note">${esc(x.note)}</span>`:''}</span></div>`)});
    const ws=[...new Set([...hs,...as,...aas].map(x=>x.school))].filter(x=>x!==p.school&&byId[x]);
    return `<div class="pf-row"><div class="pf-se">${esc(se)}${g?`<small>${GR_YR[g]}${p.inf[se]?' <span title="Inferred from class year">(est.)</span>':''}</small>`:''}${ws.map(o=>`<a class="pf-sch" href="#school-${o}" style="${colorVars(byId[o])}">${esc(byId[o].short||byId[o].name)}</a>`).join('')}</div><div class="pf-it">${lines.join('')}</div></div>`}).join('');
  const cols=PF_STATS.filter(([k])=>st.some(x=>x[k]!=null&&x[k]!==''));
  const tbl=cols.length?`<div class="block"><h2>Season stats</h2><div class="tbl"><table><thead><tr><th>Season</th><th>Gr</th>${cols.map(c=>`<th class="r">${c[1]}</th>`).join('')}</tr></thead><tbody>${st.slice().sort((a,b)=>a.season.localeCompare(b.season)).map(x=>`<tr><td>${esc(x.season)}</td><td>${p.gr[x.season]?GR_YR[p.gr[x.season]]:''}</td>${cols.map(([k,l,t])=>`<td class="r num">${pfVal(x,k,t)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></div>`:'';
  const c=p.card,ex=p.ex||{};
  const about=[ex.bio?`<p>${esc(ex.bio)}</p>`:'',c&&c.accolades?`<p>${esc(c.accolades)}</p>`:'',c&&c.college?`<p><b>College:</b> ${esc(c.college)}</p>`:'',c&&c.pro?`<p><b>Pro:</b> ${esc(c.pro)}</p>`:''].join('');
  const srcs=[...new Set([...p.hon.map(h=>h.selector==='BCAM'&&/ballstate\.pdf$/.test(h.src||'')?'BCAM all-state list ('+h.season+')':h.src),...p.ac.map(x=>x.src),...p.aa.map(x=>x.src),...p.lead.map(x=>x.src),...st.map(x=>x.src),...((ex.links||[]).filter(l=>l.url).map(l=>l.label||l.url))].filter(Boolean))];
  const nSe=p.seasons.length;
  return `<section class="view">${head}
    ${(()=>{const cells=[[p.hon.length,'All-state'],[p.top,'All-conf.'],[p.ac.length-p.top,'All-conf. HM'],[p.aa.length,'LSJ all-area']].filter(c=>c[0]>0).concat([[nSe,'Season'+(nSe===1?'':'s')]]);
      return `<div class="board pfboard" style="grid-template-columns:repeat(${cells.length},1fr)">${cells.map(c=>`<div><span class="v">${c[0]}</span><span class="k">${c[1]}</span></div>`).join('')}</div>`})()}
    ${p.mr||p.poy||p.dream?`<div class="meta" style="display:flex;gap:6px;flex-wrap:wrap">${p.aa.filter(AA_TOP).map(x=>aaChip(x,true).replace('</span>',' '+esc(x.season)+'</span>')).join('')}${p.mr?`<span class="chip gold">${p.mr==='retro'?'Retro ':''}Mr. Basketball</span>`:''}${p.poy?`<span class="chip gold">League Player of the Year${p.poy>1?' ×'+p.poy:''}</span>`:''}</div>`:''}
    <div class="block"><h2>Season by season</h2><div class="pf-tl">${rows}</div>${p.gradNote?`<p class="note">${esc(p.gradNote)}; the class year shown uses the most common one.</p>`:''}</div>
    ${tbl||`<p class="note">No season stats on file yet.</p>`}
    ${about?`<div class="block"><h2>About</h2>${about}</div>`:''}
    ${(ex.links||[]).some(l=>l.url)?`<p class="note">${ex.links.filter(l=>l.url).map(l=>`<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label||'Link')}</a>`).join(' · ')}</p>`:''}
    <details class="fold"><summary><span class="eyebrow" style="margin-left:0">Sources (${srcs.length})</span></summary><ul class="note acsrc">${srcs.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></details>
    <p><a href="#players">← All players</a> · <a href="#school-${s.id}">${esc(s.name)}</a></p>
  </section>`;
}
let P_TAB='all';
function viewPlayers2(){
  const base=viewPlayers();
  const i=base.indexOf('<div class="controls">'),j=base.lastIndexOf('</section>');
  const head=base.slice(0,i).replace('<div class="eyebrow">Notable players</div>','<div class="eyebrow">Profiles and notable players</div>').replace(/<p class="lede">[\s\S]*?<\/p>/,`<p class="lede">Every Greater Lansing player picked all-state, all-conference or LSJ all-area has a profile: honors season by season, class year, and stats as they're added. Notable players are the ones with college or pro careers and other honors.</p>`);
  const decs=[...new Set(PROF.map(p=>p.grad?Math.floor((+p.grad-1)/10)*10:null).filter(x=>x!=null))].sort((a,b)=>b-a);
  setTimeout(()=>{
    const tabs=[...document.querySelectorAll('#ptabs button')];
    const show=t=>{P_TAB=t;tabs.forEach(b=>b.setAttribute('aria-selected',b.dataset.t===t?'true':'false'));document.querySelectorAll('.ppanel').forEach(x=>x.hidden=x.id!=='pp-'+t)};
    tabs.forEach(b=>b.onclick=()=>show(b.dataset.t));show(P_TAB);
    let lim=150;
    const draw=()=>{
      const sc=$('#pdsch').value,d=$('#pddec').value,hn=$('#pdhon').value,q=$('#pdq').value.trim().toLowerCase(),so=$('#pdsort').value;
      const rows=PROF.filter(p=>(sc==='all'||p.school===sc||p.hon.concat(p.ac,p.aa).some(x=>x.school===sc))&&(d==='all'||(d==='none'?!p.grad:p.grad&&Math.floor((+p.grad-1)/10)*10===+d))&&
        (hn==='all'||(hn==='state'&&p.hon.length)||(hn==='first'&&p.hon.some(h=>h.tier==='first'||h.tier==='dream'))||(hn==='conf'&&p.top)||(hn==='poy'&&p.poy)||(hn==='lsjdt'&&p.dream)||(hn==='lsj'&&p.aa.length)||(hn==='mr'&&p.mr)||(hn==='stats'&&p.ex&&(p.ex.seasons||[]).length))&&
        (!q||p.names.some(n=>n[1].toLowerCase().includes(q))||p.hon.concat(p.ac,p.aa).some(x=>(x.listed_as||'').toLowerCase().includes(q))));
      if(so==='honors')rows.sort((a,b)=>profScore(b)-profScore(a)||a.name.localeCompare(b.name));
      else if(so==='name')rows.sort((a,b)=>a.name.split(' ').pop().localeCompare(b.name.split(' ').pop())||a.name.localeCompare(b.name));
      else rows.sort((a,b)=>(+b.grad||0)-(+a.grad||0)||profScore(b)-profScore(a)||a.name.localeCompare(b.name));
      $('#pdcount').textContent=rows.length+(rows.length===1?' player':' players');
      const xs=lim?rows.slice(0,lim):rows;
      const card=p=>{const s=byId[p.school];return `<a class="pdc" href="#player-${p.id}" style="${colorVars(s)}"><span class="ps">${esc(s.short||s.name)}${[...new Set([...p.hon,...p.ac].map(x=>x.school))].filter(x=>x!==p.school&&byId[x]).map(o=>' / '+esc(byId[o].short||byId[o].name)).join('')}${p.grad?' · '+p.grad:''}${p.pos?' · '+esc(p.pos):''}</span><span class="pn">${esc(p.name)}</span><span class="meta">${profChips(p)}</span></a>`};
      let html='';
      if(so==='class'){const g=[];xs.forEach(p=>{const k=p.grad?'Class of '+p.grad:'Class year unknown';if(!g.length||g.at(-1)[0]!==k)g.push([k,[]]);g.at(-1)[1].push(p)});
        html=g.map(([k,ps])=>`<h3 class="pd-h">${esc(k)} <span class="note">${ps.length}</span></h3><div class="pdgrid">${ps.map(card).join('')}</div>`).join('')}
      else html=`<div class="pdgrid">${xs.map(card).join('')}</div>`;
      $('#pdlist').innerHTML=(rows.length?html:'<p class="empty">No players match.</p>')+(lim&&rows.length>lim?`<button class="btn ghost" id="pdmore">Show all ${rows.length}</button>`:'');
      if(lim&&rows.length>lim)$('#pdmore').onclick=()=>{lim=0;draw()};
    };
    ['#pdsch','#pddec','#pdhon','#pdsort'].forEach(x=>$(x).onchange=()=>{lim=150;draw()});$('#pdq').oninput=()=>{lim=150;draw()};draw();
  });
  return head+`<div class="stabs" id="ptabs" role="tablist"><button role="tab" data-t="all">All players <span class="num">${PROF.length}</span></button><button role="tab" data-t="notable">Notable</button></div>
    <div class="ppanel block" id="pp-all">
      <div class="controls">
        <label for="pdsch">School</label><select id="pdsch"><option value="all">All schools</option>${SCHOOLS.filter(s=>PROF.some(p=>p.school===s.id)).map(s=>`<option value="${s.id}">${esc(s.name)}</option>`).join('')}</select>
        <label for="pddec">Class</label><select id="pddec"><option value="all">All classes</option>${decs.map(d=>`<option value="${d}">${d+1}-${String(d+10).slice(-2)}</option>`).join('')}<option value="none">Unknown</option></select>
        <label for="pdhon">Honor</label><select id="pdhon"><option value="all">Any honor</option><option value="state">All-state</option><option value="first">All-state 1st team / Free Press Dream Team</option><option value="conf">All-conference (not HM)</option><option value="poy">League Player of the Year</option><option value="lsjdt">LSJ Dream Team / POY</option><option value="lsj">LSJ all-area (any)</option><option value="mr">Mr. Basketball</option><option value="stats">Has season stats</option></select>
        <label for="pdsort">Sort</label><select id="pdsort"><option value="class">Newest class</option><option value="honors">Most decorated</option><option value="name">Last name</option></select>
        <input type="search" id="pdq" placeholder="Search player" aria-label="Search player"><span class="eyebrow num" id="pdcount"></span>
      </div>
      <div id="pdlist"></div>
    </div>
    <div class="ppanel" id="pp-notable" hidden>`+base.slice(i,j)+`</div></section>`;
}
// ---- end player profiles
'''
CODE = CODE.replace('__PSTATS__', json.dumps(PS, separators=(',', ':'), ensure_ascii=False))
i = s.find('// ---- player profiles (patch_profiles.py)')
if i >= 0:
    j = s.index('// ---- end player profiles\n', i) + len('// ---- end player profiles\n')
    s = s[:i] + s[j:]
k = s.index('function route(){')
s = s[:k] + CODE + s[k:]

# ---- router
rep("if(h.startsWith('school-'))html=viewSchool(h.slice(7));\n  else html=",
    "if(h.startsWith('school-'))html=viewSchool(h.slice(7));\n  else if(h.startsWith('player-'))html=viewProfile(h.slice(7));\n  else html=")
rep('players:viewPlayers,', 'players:viewPlayers2,')
rep("if(a.getAttribute('href')==='#'+(h||'home'))", "if(a.getAttribute('href')==='#'+(h.startsWith('player-')?'players':(h||'home')))")

# upgrade links written by the first version of this script (no season argument)
for a, b in [('plink(x.name,x.school)}', 'plink(x.name,x.school,x.season)}'), ('plink(h.name,h.school)}', 'plink(h.name,h.school,h.season)}'),
             ('plink(n,hs[0].school)}', 'plink(n,hs[0].school,hs[0].season)}'), ('plink(p.x.name,p.x.school)}', 'plink(p.x.name,p.x.school,p.x.season)}'),
             ('plink(p.name,sid)}', 'plink(p.name,sid,p.last)}')]:
    s = s.replace(a, b)
# ---- name links into profiles
rep('<li><span class="acn">${esc(x.name)}${x.note?', '<li><span class="acn">${plink(x.name,x.school,x.season)}${x.note?')
rep('<li><span class="acn">${esc(h.name)}</span><span class="meta">${a.map(honChipFull)', '<li><span class="acn">${plink(h.name,h.school,h.season)}</span><span class="meta">${a.map(honChipFull)')
rep('<li><span class="acn">${esc(h.name)} <span class="note">${r.a.length} selections', '<li><span class="acn">${plink(h.name,h.school,h.season)} <span class="note">${r.a.length} selections')
rep('return `<li><span class="acn">${esc(n)}</span><span class="meta">${hs.map(', 'return `<li><span class="acn">${plink(n,hs[0].school,hs[0].season)}</span><span class="meta">${hs.map(')
rep(">${esc(p.x.name)}${p.mvp?'<b>MVP</b>':''}", ">${plink(p.x.name,p.x.school,p.x.season)}${p.mvp?'<b>MVP</b>':''}")
rep('<li><span class="acx-nm">${esc(p.name)}', '<li><span class="acx-nm">${plink(p.name,sid,p.last)}')
rep("${p.source?`<a class=\"note\" href=\"${esc(String(p.source).split(",
    "${profFor(p.name,s.id)?`<a class=\"note\" href=\"#player-${profFor(p.name,s.id).id}\">Full profile →</a> `:''}${p.source?`<a class=\"note\" href=\"${esc(String(p.source).split(")

# ---- styles
CSS = '''.plink{color:inherit;text-decoration:none;border-bottom:1px dotted currentColor}.plink:hover{border-bottom-style:solid}
.pdgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,230px),1fr));gap:10px}
.pdc{display:grid;gap:4px;align-content:start;padding:10px 12px;background:var(--surface);border:1px solid var(--line);border-left:5px solid var(--c1);border-radius:var(--r);color:var(--ink);text-decoration:none;min-width:0}
.pdc:hover{border-color:var(--c1)}
.pdc .pn{font-weight:700;font-size:16px;line-height:1.2}
.pdc .ps{font-family:var(--cond);font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.pdc .meta{display:flex;flex-wrap:wrap;gap:4px}
.pfboard{grid-template-columns:repeat(4,1fr)}
.pd-h{margin:18px 0 8px;font-size:17px}.pd-h:first-child{margin-top:4px}
.pf-row{display:grid;grid-template-columns:92px 1fr;gap:12px;padding:10px 0;border-top:1px solid var(--line)}
.pf-se{font-weight:700;white-space:nowrap}.pf-se small{display:block;font-weight:400;color:var(--muted);font-size:13px}
.pf-it{display:grid;gap:6px;min-width:0}.pf-line{display:flex;flex-wrap:wrap;gap:4px 8px;align-items:center}
.pf-sch{display:table;margin-top:4px;font-family:var(--cond);font-weight:600;font-size:11px;letter-spacing:.05em;text-transform:uppercase;padding:1px 6px;border-radius:3px;background:var(--c1);color:var(--ct);box-shadow:inset -3px 0 0 var(--c2);text-decoration:none;white-space:nowrap}
.pf-k{font-family:var(--cond);font-size:12px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);min-width:100px}
@media (max-width:640px){.pfboard div{padding:8px 6px}.pfboard .v{font-size:20px}.pfboard .k{font-size:10px;letter-spacing:.04em}.pf-row{grid-template-columns:62px 1fr;gap:8px}.pf-k{min-width:0;flex-basis:100%}#pp-all .controls select{flex:1 1 40%;min-width:0}#pp-all .controls label{display:none}#pdq{flex:1 1 100%}}
'''
i0 = s.find('.plink{')
if i0 >= 0:
    s = s[:i0] + s[s.index('</style>', i0):]
k = s.find('</style>\n\n<header')
if k < 0: k = s.find('</style>')
s = s[:k] + CSS + s[k:]

open(p, 'w').write(s)
print('ok', p, 'profile extras:', len(PS['players']))
