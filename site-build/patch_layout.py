import sys
# School pages reorganized into tabs: Overview, History, People, Records (Jack, Oct 30, 2026).
# Replaces the whole viewSchool function, so run it AFTER add_uniforms.py, patch_players.py,
# patch_board.py and patch_fold.py (it relies on UNIFORMS, byGrad and the fold CSS they add).
p=sys.argv[1]; s=open(p).read()
NEW_FN=r'''function viewSchool(id){
  const s=byId[id];if(!s)return viewHome();
  const a=analyze(s),h=honors(s),R=championTeams();
  const p=programRow(s);
  const ffOnly=h.ff.filter(x=>!h.champ.some(c=>c.season===x)&&!h.ru.some(c=>c.season===x));
  const banners=[...h.champ.map(c=>bannerHTML(s,c.season,'champ',c.class)),...h.ru.map(c=>bannerHTML(s,c.season,'ru',c.class)),...ffOnly.map(x=>bannerHTML(s,x,'ff',ffClass(s,x)))].join('');
  const status=[s.nickname,s.city,s.status,s.class_current,s.conference_current].filter(Boolean).map(esc).join(' · ');
  const players=[...(s.notable_players||[])].sort(byGrad);
  const visiting=[];SCHOOLS.forEach(o=>{if(o.id!==id)(o.notable_players||[]).forEach(p=>{if((p.also||[]).some(a=>a.school===id))visiting.push({p,o})})});
  const hon=HON.filter(h=>h.school===id);
  const regN=new Set([...(a?a.seasons.filter(x=>['champ','ru','ff','reg'].includes(x.finish)).map(x=>x.season):[]),...(s.tournament_summary?.regional_titles||[]),...h.ff]).size;
  // ---- header (always shown)
  let head=`<div class="shead${s.logo?' has-logo':''}" style="${colorVars(s)}">${s.logo?`<span class="slogo-box"><img class="slogo" src="${esc(s.logo)}" alt="${esc(s.name)} logo" style="--ls:${s.logo_scale||1}"></span>`:''}<div class="stext"><div class="eyebrow">${status}</div><h1>${esc(s.name)}</h1>${s.colors?.names?`<div class="eyebrow">${esc(s.colors.names)}</div>`:''}</div></div>`;
  // ---- Overview: stats, banners, uniforms
  let ov=`<div class="board">
      ${a?`<div><span class="v">${recStr(a.total.w,a.total.l,a.total.t)}</span><span class="k">Record ${esc(a.seasons[0].season)} to ${esc(a.seasons.at(-1).season)}</span></div><div><span class="v">${fmtPct(a.total.p)}</span><span class="k">Win %</span></div><div><span class="v">${a.seasons.length}</span><span class="k">Seasons on file</span></div>`:''}
      <div><span class="v">${h.champ.length}</span><span class="k">State titles</span></div>
      <div><span class="v">${h.ru.length}</span><span class="k">Runner-up</span></div>
      <div><span class="v">${h.ff.length}</span><span class="k">Final Fours</span></div>
      ${(a||s.tournament_summary?.regional_titles)?`<div><span class="v">${regN}</span><span class="k">Regional titles</span></div>`:''}
      ${a?`<div><span class="v">${a.seasons.filter(x=>x.finish&&x.finish!=='out').length}</span><span class="k">District titles+</span></div>`:''}
      <div><span class="v">${p.points}</span><span class="k">Program points</span></div>
    </div>${a?`<p class="note">District titles+ counts every season a team won its district or played on past the district round. That includes early years when the tournament started at the regional level and years a team advanced after losing its district final, so it can run a little higher than a count of district final wins alone. Regional titles counts seasons a team won a regional or went further.</p>`:''}`;
  if(banners)ov+=`<div class="block"><h2>Banners</h2><div class="rafters">${banners}</div></div>`;
  if(s.lineage){const lff=(s.lineage.final_fours||[]).filter(x=>!s.lineage.state_titles.some(c=>c.season===x)&&!s.lineage.state_runner_ups.some(c=>c.season===x));
    ov+=`<div class="block"><h2>${esc(s.lineage.name)} banners</h2><p class="note">${esc(s.lineage.note||'')}</p><div class="rafters">${[...s.lineage.state_titles.map(c=>bannerHTML(s,c.season,'champ',c.class,s.lineage.name)),...s.lineage.state_runner_ups.map(c=>bannerHTML(s,c.season,'ru',c.class,s.lineage.name)),...lff.map(x=>bannerHTML(s,x,'ff','',s.lineage.name))].join('')}</div></div>`;}
  const unis=(typeof UNIFORMS!=='undefined'&&UNIFORMS[id])||null;
  if(unis)ov+=`<div class="block"><h2>Uniforms</h2><div class="unis">${unis.map(u=>`<figure><img src="${esc(u.src)}" alt="${esc(s.name)} ${esc(u.label.toLowerCase())} uniform"><figcaption>${esc(u.label)}</figcaption></figure>`).join('')}</div></div>`;
  // ---- History: best teams, tournament history, decade chart, seasons
  let hi='';
  const champs=R.rows.filter(r=>r.school.id===id&&['champ','ru','ff'].includes(r.finish)).sort((x,y)=>(y.score??-1)-(x.score??-1));
  if(champs.length)hi+=`<div class="block"><h2>Best teams</h2><div class="tbl"><table><thead><tr><th>Season</th><th>Finish</th><th>Record</th><th>Rating</th><th>Coach</th></tr></thead><tbody>${champs.map(r=>`<tr><td class="num">${esc(r.season)}</td><td><span class="chip ${r.finish==='champ'?'gold':''}">${LV[r.finish].label}</span></td><td class="num">${r.w!=null?recStr(r.w,r.l,r.t):'—'}</td><td>${rateBar(r)}</td><td>${esc(r.coach)}</td></tr>`).join('')}</tbody></table></div></div>`;
  const ts=s.tournament_summary;
  if(ts){const bf=ts.best_finish;
    hi+=`<div class="block"><h2>Tournament history</h2><div class="tbl"><table><tbody>
      <tr><td>District titles</td><td class="wrapok num">${ts.district_titles?.length?`<b>${ts.district_titles.length}</b> · ${ts.district_titles.map(esc).join(', ')}`:'None found'}</td></tr>
      <tr><td>Regional titles</td><td class="wrapok num">${ts.regional_titles?.length?`<b>${ts.regional_titles.length}</b> · ${ts.regional_titles.map(esc).join(', ')}`:'None found'}</td></tr>
      ${bf?`<tr><td>Deepest run</td><td class="wrapok">${esc(bf.season)} ${esc(bf.round)}, lost to ${esc(bf.opponent)} ${esc(bf.score)}</td></tr>`:''}
      ${ts.record?`<tr><td>Tournament record</td><td class="num">${esc(ts.record)}${ts.through_season?` through ${esc(ts.through_season)}`:''}</td></tr>`:''}
    </tbody></table></div><p class="note">${ts.note?esc(ts.note)+' ':''}${ts.source?`<a href="${esc(ts.source)}" target="_blank" rel="noopener">Source</a>`:''}</p></div>`;}
  if(a)hi+=`<div class="block"><h2>Win % by decade</h2><div class="tbl" style="padding:12px" id="dec"></div></div>
    <details class="block fold"><summary><h2>Season-by-season records</h2><span class="eyebrow num">${a.seasons.length} seasons</span></summary><div class="fold-body"><span class="note">Tap a season for its games</span><div id="seasons"></div></div></details>`;
  else hi+=`<div class="callout"><h3>Season-by-season results coming</h3><p>This program's history comes from MHSAA records and news coverage. Once its spreadsheet is added, this page gets the full treatment: every season and game, coaching records, win % by decade, rivalry records and team ratings built from actual margins.</p><p><a href="#data">See the spreadsheet format</a></p></div>`;
  // ---- People: players, all-state, coaches (one block)
  let pe='';
  if(players.length||visiting.length)pe+=`<details class="block fold"><summary><h2>Notable players</h2><span class="eyebrow num">${players.length+visiting.length} players</span></summary><div class="fold-body"><div class="players">${players.map(p=>playerCard(p,s,false)).join('')}${visiting.map(({p,o})=>playerCard(p,o,true)).join('')}</div></div></details>`;
  if(hon.length){pe+=`<details class="block fold"><summary><h2>All-state honors</h2><span class="eyebrow num">${hon.length} selections</span></summary><div class="fold-body"><div id="shon"></div><a class="note" href="#honors">All schools</a></div></details>`;setTimeout(()=>sortTable('shon',honorCols(false),hon,{k:'season',dir:-1}))}
  const nc=s.notable_coaches||[];
  if(a||nc.length){
    pe+=`<details class="block fold"><summary><h2>Coaches</h2><span class="eyebrow num">${a?a.coaches.length+' on file':nc.length+' notable'}</span></summary><div class="fold-body">`;
    if(nc.length)pe+=`<h3>Notable coaches</h3><div class="tbl"><table><thead><tr><th>Coach</th><th>Years</th><th>Notes</th></tr></thead><tbody>${nc.map(c=>`<tr><td>${esc(c.name)}</td><td class="wrapok">${esc(c.years)}</td><td class="wrapok">${esc(c.notes)}</td></tr>`).join('')}</tbody></table></div>`;
    if(a)pe+=`<h3>Every coach's record</h3><div id="coaches"></div>`;
    pe+=`</div></details>`;
  }
  if(!pe)pe=`<p class="empty">No players or coaches on file yet.</p>`;
  // ---- Records: program records, opponents
  let re='';
  if(a)re=`<div class="two"><div class="block"><h2>Program records</h2><div id="records"></div></div><div class="block"><h2>Most-played opponents</h2><div id="opps"></div></div></div>`;
  const tabs=[['ov','Overview',ov],['hi','History',hi],['pe','People',pe],['re','Records',re]].filter(t=>t[2]);
  let saved='ov';try{saved=sessionStorage.getItem('stab')||'ov'}catch(e){}
  if(!tabs.some(t=>t[0]===saved))saved='ov';
  let html=`<section class="view">${head}
    <div class="stabs" role="tablist" aria-label="${esc(s.name)} sections">${tabs.map(t=>`<button type="button" role="tab" id="stab-${t[0]}" aria-controls="spanel-${t[0]}" aria-selected="${t[0]===saved}">${t[1]}</button>`).join('')}</div>
    ${tabs.map(t=>`<div class="spanel" role="tabpanel" id="spanel-${t[0]}" aria-labelledby="stab-${t[0]}"${t[0]===saved?'':' hidden'}>${t[2]}</div>`).join('')}`;
  const srcs=[...new Set([...(s.state_titles||[]),...(s.state_runner_ups||[]),...(s.notable_coaches||[])].map(x=>x.source).filter(Boolean).flatMap(x=>String(x).split(/\s*;\s*/)).concat(s.sources||[]))];
  if(srcs.length)html+=`<details class="block fold"><summary><h3>Sources</h3><span class="eyebrow num">${srcs.length}</span></summary><div class="fold-body"><ul class="note">${srcs.map(u=>`<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(u.replace(/^https?:\/\/(www\.)?/,'').slice(0,80))}</a></li>`).join('')}</ul></div></details>`;
  html+='</section>';
  setTimeout(()=>{
    document.querySelectorAll('.stabs [role=tab]').forEach(b=>b.onclick=()=>{const k=b.id.slice(5);
      document.querySelectorAll('.stabs [role=tab]').forEach(x=>x.setAttribute('aria-selected',x===b));
      document.querySelectorAll('.spanel').forEach(x=>x.hidden=x.id!=='spanel-'+k);
      try{sessionStorage.setItem('stab',k)}catch(e){}});
    if(a)schoolDetail(s,a);
  });
  return html;
}
'''
CSS_A=".empty{color:var(--muted);font-style:italic}\n"
CSS=CSS_A+"""/* school page tabs */
.stabs{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;border-bottom:1px solid var(--line);margin-top:-6px}
.stabs button{font-family:var(--cond);font-weight:600;font-size:16px;letter-spacing:.05em;text-transform:uppercase;background:none;border:0;color:var(--muted);padding:10px 14px;cursor:pointer;white-space:nowrap;border-radius:var(--r) var(--r) 0 0}
.stabs button:hover{color:var(--ink);background:var(--sunk)}
.stabs button[aria-selected="true"]{color:var(--ink);box-shadow:inset 0 -3px 0 var(--maple)}
.stabs button:focus-visible{outline:2px solid var(--maple);outline-offset:-2px}
.spanel{display:grid;gap:28px;min-width:0}
.spanel>*{min-width:0}
.fold-body h3{margin-top:6px}
"""
i=s.index('function viewSchool(id){'); j=s.index('function schoolDetail(s,a){')
s=s[:i]+NEW_FN+s[j:]
if '/* school page tabs */' not in s:
    assert s.count(CSS_A)==1; s=s.replace(CSS_A,CSS)
open(p,'w').write(s); print('ok',p)
