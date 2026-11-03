import sys
# School pages: Notable players, All-state honors and Season-by-season records start collapsed (Jack, Oct 30, 2026).
p=sys.argv[1]; s=open(p).read()
CSS_A=".empty{color:var(--muted);font-style:italic}\n"
CSS=CSS_A+"""/* collapsible sections */
details.fold{border-top:1px solid var(--line);padding-top:4px}
details.fold>summary{list-style:none;cursor:pointer;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;padding:6px 0}
details.fold>summary::-webkit-details-marker{display:none}
details.fold>summary::before{content:"\\25B8";color:var(--maple-ink);font-size:18px;transition:transform .15s ease;display:inline-block;width:1em}
details.fold[open]>summary::before{transform:rotate(90deg)}
details.fold>summary .eyebrow{margin-left:auto}
details.fold>.fold-body{display:grid;gap:14px;padding-top:8px}
@media (prefers-reduced-motion:reduce){details.fold>summary::before{transition:none}}
"""
pairs=[
 (CSS_A,CSS),
 ("""html+=`<div class="block"><h2>Notable players</h2><div class="players">${players.map(p=>playerCard(p,s,false)).join('')}${visiting.map(({p,o})=>playerCard(p,o,true)).join('')}</div></div>`;""",
  """html+=`<details class="block fold"><summary><h2>Notable players</h2><span class="eyebrow num">${players.length+visiting.length} players</span></summary><div class="fold-body"><div class="players">${players.map(p=>playerCard(p,s,false)).join('')}${visiting.map(({p,o})=>playerCard(p,o,true)).join('')}</div></div></details>`;"""),
 ("""<div class="block"><div class="head-row"><h2>All-state honors</h2><a href="#honors">All schools</a></div><div id="shon"></div></div>""",
  """<details class="block fold"><summary><h2>All-state honors</h2><span class="eyebrow num">${hon.length} selections</span></summary><div class="fold-body"><div id="shon"></div><a class="note" href="#honors">All schools</a></div></details>"""),
 ("""<div class="block"><div class="head-row"><h2>Season-by-season records</h2><span class="note">Tap a season for its games</span></div><div id="seasons"></div></div>""",
  """<details class="block fold"><summary><h2>Season-by-season records</h2><span class="eyebrow num">${a.seasons.length} seasons</span></summary><div class="fold-body"><span class="note">Tap a season for its games</span><div id="seasons"></div></div></details>"""),
]
for a,b in pairs:
    if b in s: continue
    assert s.count(a)==1,a[:60]
    s=s.replace(a,b)
open(p,'w').write(s); print('ok',p)
