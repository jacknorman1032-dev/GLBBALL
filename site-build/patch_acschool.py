import json
import sys
# School pages' All-conference section, redesigned (Jack, Nov 3, 2026): "By season" view (one row per season,
# player chips filled for all-conference / outlined for honorable mention, Sr/Jr/So/Fr, a "League champs" badge only
# when this school won, league name only when it changes, seasons before 2010 folded by decade) and a "By player"
# view (one row per player with a chip per season). Replaces acSchoolDraw's all-conference part; the area stat
# leaders part is kept. Also turns the People tab into a stat strip plus a grid of section cards with previews
# (peCards, hooked into viewSchool from patch_layout). patch_allconf.py (step 12) rewrites acSchoolDraw on every run, so run this AFTER step 12.
p = sys.argv[1]
s = open(p).read()
NEW = r'''function acSchoolDraw(acs,ld){
  const el=$('#sac');if(!el)return;
  const sid=acs.length?acs[0].school:null;
  const GR={'9':'Fr','10':'So','11':'Jr','12':'Sr'};
  const top=x=>['poy','first','second','third'].includes(x.team);
  const meta=x=>[GR[x.grade]||'',x.pos||''].filter(Boolean).join(' · ');
  const tip=x=>[x.season,x.league,x.listed_team||AC_TEAM[x.team].label,x.note||''].filter(Boolean).join(' · ');
  const champ=(se,lg)=>{const L=ALLCONF.leagues.find(L=>L.season===se&&L.league===lg);const r=L&&L.standings.find(r=>r[3]===1&&areaId(r[0])===sid);return r?`<span class="acx-ch">League champs${r[1]!=null?' '+r[1]+'-'+r[2]:''}</span>`:''};
  const merge=xs=>{const by={};xs.forEach(x=>{const n=pkey(x.name);(by[n]=by[n]||[]).push(x)});
    return Object.values(by).map(a=>{a.sort((p,q)=>AC_TEAM[p.team].rank-AC_TEAM[q.team].rank);return {x:a.find(x=>x.team!=='poy')||a[0],mvp:a.some(x=>x.team==='poy'),a}})};
  let mode=window.ACX_MODE||'season',pAll=false;
  const seasonView=()=>{
    const g={};acs.forEach(x=>{const k=x.season+'|'+x.league;(g[k]=g[k]||[]).push(x)});
    const keys=Object.keys(g).sort((a,b)=>b.localeCompare(a));
    const decs={};keys.forEach(k=>{const d=Math.floor(parseInt(k)/10)*10;(decs[d]=decs[d]||[]).push(k)});
    const ds=Object.keys(decs).map(Number).sort((a,b)=>b-a);
    return ds.map((d,i)=>{let prev='';
      const rows=decs[d].map(k=>{const [se,lg]=k.split('|'),c=champ(se,lg),show=lg!==prev;prev=lg;
        const ps=merge(g[k]).sort((p,q)=>AC_TEAM[p.x.team].rank-AC_TEAM[q.x.team].rank||p.x.name.localeCompare(q.x.name));
        return `<div class="acx-row"><div class="acx-se">${esc(se)}</div><div>${show||c?`<div class="acx-lg">${show?esc(lg):''}${c}</div>`:''}<div class="acx-ps">${ps.map(p=>`<span class="acx-p${top(p.x)||p.mvp?' f':''}" title="${esc(p.a.map(tip).join('\n'))}">${esc(p.x.name)}${p.mvp?'<b>MVP</b>':''}${meta(p.x)?`<small>${esc(meta(p.x))}</small>`:''}</span>`).join('')}</div></div></div>`}).join('');
      const open=d>=2010||i===0;
      return `<details class="acx-dec"${open?' open':''}><summary>${d}s <span class="num">${decs[d].length} season${decs[d].length>1?'s':''}</span></summary>${rows}</details>`}).join('');
  };
  const playerView=()=>{
    const by={};acs.forEach(x=>{const k=pkey(x.name);(by[k]=by[k]||[]).push(x)});
    const ps=Object.values(by).map(a=>{a.sort((p,q)=>p.season.localeCompare(q.season));const se={};a.forEach(x=>(se[x.season]=se[x.season]||[]).push(x));
      return {name:a[a.length-1].name,se,last:a[a.length-1].season,n:Object.keys(se).length}})
      .sort((p,q)=>q.last.localeCompare(p.last)||q.n-p.n||p.name.localeCompare(q.name));
    const lim=pAll?ps.length:40;
    return '<ul class="acx-pl">'+ps.slice(0,lim).map(p=>`<li><span class="acx-nm">${esc(p.name)}${p.n>1?` <span class="note">${p.n} seasons</span>`:''}</span><span class="acx-yrs">${Object.keys(p.se).sort().map(s=>{const [m]=merge(p.se[s]);
      return `<span class="acx-y${top(m.x)||m.mvp?' f':''}" title="${esc(m.a.map(tip).join('\n'))}">’${s.slice(-2)}${GR[m.x.grade]?' '+GR[m.x.grade]:''}${m.mvp?' <b>MVP</b>':''}</span>`}).join('')}</span></li>`).join('')+'</ul>'+
      (ps.length>lim?`<button class="btn ghost" id="sacmore">Show all ${ps.length} players</button>`:'');
  };
  const draw=()=>{
    el.innerHTML=`<div class="acx-tg" role="tablist"><button role="tab" data-m="season" aria-selected="${mode==='season'}">By season</button><button role="tab" data-m="player" aria-selected="${mode==='player'}">By player</button></div>`+
      (mode==='season'?seasonView():playerView())+'<p class="acx-key"><span class="acx-p f">All-conference</span><span class="acx-p">Honorable mention</span><span class="note">Hover a name for the exact team listed.</span></p>';
    el.querySelectorAll('.acx-tg button').forEach(b=>b.onclick=()=>{window.ACX_MODE=mode=b.dataset.m;draw()});
    const m=$('#sacmore');if(m)m.onclick=()=>{pAll=true;draw()};
  };
  draw();
'''
CSS = ('.acx-tg{display:inline-flex;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;margin:2px 0 6px;justify-self:start}'
 '.acx-tg button{font-family:var(--cond);font-weight:600;font-size:13px;letter-spacing:.06em;text-transform:uppercase;background:none;border:0;color:var(--muted);padding:6px 12px;cursor:pointer}'
 '.acx-tg button[aria-selected="true"]{background:var(--ink);color:var(--surface)}'
 '.acx-dec{border-top:1px solid var(--line)}'
 '.acx-dec>summary{cursor:pointer;list-style:none;padding:8px 0;font-family:var(--cond);font-weight:600;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);display:flex;gap:8px;align-items:baseline}'
 '.acx-dec>summary::-webkit-details-marker{display:none}'
 '.acx-dec>summary::before{content:"\\25B8";color:var(--maple-ink);display:inline-block;transition:transform .15s ease}'
 '.acx-dec[open]>summary::before{transform:rotate(90deg)}'
 '.acx-row{display:grid;grid-template-columns:84px minmax(0,1fr);gap:4px 14px;padding:10px 0;border-top:1px solid var(--line);align-items:baseline}'
 '.acx-se{font-family:var(--cond);font-weight:700;font-size:17px;white-space:nowrap;font-variant-numeric:tabular-nums}'
 '.acx-lg{font-size:13px;color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-bottom:6px}'
 '.acx-ch{font-family:var(--cond);font-weight:600;font-size:12px;letter-spacing:.06em;text-transform:uppercase;padding:1px 7px;border-radius:3px;background:var(--maple);color:#1a1206}'
 '.acx-ps,.acx-yrs{display:flex;flex-wrap:wrap;gap:6px}'
 '.acx-p,.acx-y{display:inline-flex;align-items:baseline;gap:6px;font-size:14px;padding:4px 10px;border-radius:var(--r);border:1px solid var(--line);color:var(--ink);line-height:1.3}'
 '.acx-p.f,.acx-y.f{background:color-mix(in srgb,var(--maple) 16%,var(--surface));border-color:color-mix(in srgb,var(--maple) 55%,var(--line));font-weight:600}'
 '.acx-p small{font-size:12px;color:var(--muted);font-weight:400}'
 '.acx-p b,.acx-y b{font-family:var(--cond);font-size:11px;letter-spacing:.06em;color:var(--maple-ink)}'
 '.acx-pl{list-style:none;margin:0;padding:0}'
 '.acx-pl li{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:6px 12px;padding:9px 0;border-top:1px solid var(--line)}'
 '.acx-nm{font-weight:600}'
 '.acx-y{font-size:13px;padding:2px 8px;font-variant-numeric:tabular-nums}'
 '.acx-key{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0 0}'
 '.acx-key .acx-p{font-size:12px;padding:2px 8px}'
 '.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,360px),1fr));gap:12px;grid-auto-flow:row dense}'
 '.pgrid>details.fold{border:1px solid var(--line);border-radius:var(--r);background:var(--surface);padding:6px 16px 14px;min-width:0}'
 '.pgrid>details.fold[open]{grid-column:1/-1}'
 # card header (Jack, Nov 3, 2026): title on the first row, count under it in the same left edge, preview below,
 # so every card lines up the same way however long its title is
 '.pgrid>details.fold>summary{display:grid;grid-template-columns:1.1em minmax(0,1fr);column-gap:10px;row-gap:4px;align-items:baseline;align-content:start}'
 '.pgrid>details.fold>summary h2{font-size:22px;grid-column:2}'
 '.pgrid>details.fold>summary>.eyebrow{grid-column:2;margin-left:0;justify-self:start}'
 '.pgrid>details.fold>summary>.pv{grid-column:2;padding-left:0;margin-top:6px}'
 '.pgrid>details.fold[open] .pv{display:none}'
 '.pv{flex-basis:100%;display:grid;gap:8px;padding-left:1.6em;font-size:15px;font-family:var(--body)}'
 '.pv-l{list-style:none;margin:0;padding:0;display:grid;gap:4px}'
 '.pv-l span,.pv-k,.pv-t{color:var(--muted)}'
 '.pv-k{font-size:14px}'
 '.pv-c{display:flex;flex-wrap:wrap;gap:6px;align-items:center}'
 '.pv-x{font-family:var(--cond);font-weight:600;font-size:13px;letter-spacing:.05em;text-transform:uppercase;padding:2px 8px;border-radius:3px;border:1px solid var(--line);color:var(--muted)}'
 '.pv-x.f{border-color:var(--maple);color:var(--maple-ink);background:color-mix(in srgb,var(--maple) 12%,var(--surface))}'
 '.pv-t{margin:0}.pv-t b{color:var(--ink)}'
 '.pv-more{font-size:14px;color:var(--maple-ink);font-weight:600}'
 '@media (max-width:640px){.acx-row{grid-template-columns:1fr;gap:2px}.acx-se{font-size:16px}}\n')
PE = r"""// ---- People tab cards (patch_acschool.py)
function peCards(pe,o){
  const {s,players,visiting,hon,a,nc}=o;const cnt=[];
  const short=(t,n=40)=>{t=String(t||'').split(/[;(]/)[0].trim();return t.length>n?t.slice(0,n-1).trim()+'…':t};
  const add=(title,pv)=>{pe=pe.replace(new RegExp('<details class="block fold"><summary><h2>'+title+'</h2>(<span class="eyebrow num">[^<]*</span>)</summary>'),(m,c)=>'<details class="block fold"><summary><h2>'+title+'</h2>'+c+'<div class="pv">'+pv+'</div></summary>')};
  const pl=[...players,...visiting.map(v=>v.p)];
  if(pl.length){add('Notable players','<ul class="pv-l">'+pl.slice(0,3).map(p=>{const d=p.college?short(p.college):p.grad_year?'Class of '+p.grad_year:'';return `<li><b>${esc(p.name)}</b>${d?' <span>· '+esc(d)+'</span>':''}</li>`}).join('')+'</ul>'+(pl.length>3?`<span class="pv-more">See all ${pl.length} players</span>`:''));cnt.push([pl.length,'Notable players'])}
  if(hon.length){const t1=hon.filter(h=>h.tier==='first'||h.tier==='dream').length,t2=hon.filter(h=>h.tier==='second').length,ot=hon.length-t1-t2;
    const ls=[...new Set(hon.map(h=>h.season))].sort().pop(),lh=hon.filter(h=>h.season===ls).sort((x,y)=>HON_TIER[x.tier].rank-HON_TIER[y.tier].rank),nm=[...new Set(lh.map(h=>h.name))];
    add('All-state honors',`<div class="pv-c">${t1?`<span class="pv-x f">${t1} first team</span>`:''}${t2?`<span class="pv-x">${t2} second team</span>`:''}${ot?`<span class="pv-x">${ot} other</span>`:''}</div><p class="pv-t">Latest, ${esc(ls)}: ${nm.slice(0,2).map(n=>{const h=lh.find(h=>h.name===n);return `<b>${esc(n)}</b> (${esc(h.selector+' '+HON_TIER[h.tier].short)})`}).join(', ')}${nm.length>2?` and ${nm.length-2} more`:''}</p><span class="pv-more">See all selections</span>`);cnt.push([hon.length,'All-state picks'])}
  const acs=AC_PLAYERS.filter(x=>x.school===s.id),lt=ALLCONF.leagues.filter(L=>L.standings.some(r=>r[3]===1&&areaId(r[0])===s.id)).sort((x,y)=>y.season.localeCompare(x.season));
  if(acs.length||lt.length){const by={};acs.forEach(x=>{const k=pkey(x.name);(by[k]=by[k]||{n:x.name,se:new Set()}).se.add(x.season)});const best=Object.values(by).sort((p,q)=>q.se.size-p.se.size||p.n.localeCompare(q.n))[0];
    add('All-conference',`${lt.length?`<div class="pv-c"><span class="pv-k">League titles</span>${lt.slice(0,3).map(L=>`<span class="pv-x f">${esc(L.season)}</span>`).join('')}${lt.length>3?`<span class="pv-x">+${lt.length-3} more</span>`:''}</div>`:''}${best&&best.se.size>1?`<p class="pv-t">Most seasons: <b>${esc(best.n)}</b> (${best.se.size})</p>`:''}<span class="pv-more">See all seasons</span>`);
    cnt.push([acs.length,'All-conference']);if(lt.length)cnt.push([lt.length,'League title'+(lt.length>1?'s':'')])}
  if(a&&a.coaches.length){const lastS=a.seasons.length?a.seasons[a.seasons.length-1].season:'',cur=a.coaches.find(c=>c.last===lastS),mw=[...a.coaches].sort((x,y)=>y.w-x.w)[0];
    const li=(k,c)=>`<li><span>${k}</span> <b>${esc(c.name)}</b> <span>· ${recStr(c.w,c.l,c.t)}${c.champ?' · '+c.champ+' state title'+(c.champ>1?'s':''):''}</span></li>`;
    add('Coaches','<ul class="pv-l">'+(cur&&cur===mw?li('Most recent and most wins',cur):(cur?li('Most recent',cur):'')+(mw?li('Most wins',mw):''))+`</ul><span class="pv-more">See every coach</span>`)}
  else if(nc.length)add('Coaches','<ul class="pv-l">'+nc.slice(0,2).map(c=>`<li><b>${esc(c.name)}</b> <span>· ${esc(short(c.years))}</span></li>`).join('')+`</ul><span class="pv-more">See ${nc.length>2?'all '+nc.length+' coaches':'details'}</span>`);
  const board=cnt.length>1?`<div class="board pv-board" style="grid-template-columns:repeat(${Math.min(cnt.length,4)},1fr)">${cnt.slice(0,4).map(c=>`<div><span class="v">${c[0]}</span><span class="k">${esc(c[1])}</span></div>`).join('')}</div>`:'';
  return board+'<div class="pgrid">'+pe+'</div>';
}
"""
i = s.find('// ---- People tab cards (patch_acschool.py)')
if i >= 0:
    s = s[:i] + s[s.index('function acSchoolDraw(acs,ld){', i):]
k = s.index('function acSchoolDraw(acs,ld){')
s = s[:k] + PE + s[k:]
HOOK = "  if(pe)pe=peCards(pe,{s,players,visiting,hon,a,nc});\n"
if HOOK not in s:
    anchor = "  if(!pe)pe=`<p class=\"empty\">No players or coaches on file yet.</p>`;\n"
    assert s.count(anchor) == 1, 'people anchor'
    s = s.replace(anchor, HOOK + anchor, 1)
a = s.index('function acSchoolDraw(acs,ld){')
b = s.index("  const sl=$('#sld');", a)
s = s[:a] + NEW + s[b:]
i = s.find('.acx-tg{')
if i >= 0:
    s = s[:i] + s[s.index('\n', i) + 1:]
k = s.index('.acg{display:grid')
s = s[:k] + CSS + s[k:]
# ---- honors fixes from Jack (Nov 3, 2026) that the build's honors file doesn't have yet
i = s.index('const DATA=') + 11; j = s.index(';\n', i)
D = json.loads(s[i:j]); nfix = 0
for h in D['honors']:
    # BCAM 1998-99 printed "Adam Kulesca" (Lansing Catholic); the correct spelling is Kulesza
    if h.get('name') == 'Adam Kulesca':
        h['name'] = 'Adam Kulesza'; h['listed_as'] = 'Adam Kulesca'; nfix += 1
    # Onome Scott-Emuakpor (East Lansing) was a senior in 1996-97
    if h.get('name') == 'Onome Scott-Emuakpor' and h.get('season') == '1996-97' and h.get('yr') != 'Sr':
        h['yr'] = 'Sr'; nfix += 1
s = s[:i] + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + s[j:]
open(p, 'w').write(s)
print('ok', p, 'honors fixes:', nfix)
