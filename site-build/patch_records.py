import sys
# Program records table: Most wins in a season, then top-5 best seasons, top-5 most points, top-5 biggest wins (Jack, Oct 30, 2026).
p=sys.argv[1]; s=open(p).read()
old_best="""    <tr><td>Best season</td><td class="r">${(()=>{const b=[...a.seasons].filter(x=>x.n>=8).sort((x,y)=>y.p-x.p||y.w-x.w)[0];return b?`<b>${recStr(b.w,b.l,b.t)}</b> <span class="note">${esc(b.season)}</span>`:'—'})()}</td></tr>
    <tr><td>Most wins in a season</td><td class="r">${(()=>{const b=[...a.seasons].sort((x,y)=>y.w-x.w)[0];return `<b>${b.w}</b> <span class="note">${esc(b.season)}</span>`})()}</td></tr>"""
new_best="""    <tr><td>Most wins in a season</td><td class="r">${(()=>{const b=[...a.seasons].sort((x,y)=>y.w-x.w)[0];return `<b>${b.w}</b> <span class="note">${esc(b.season)}</span>`})()}</td></tr>
    ${[...a.seasons].filter(x=>x.n>=8).sort((x,y)=>y.p-x.p||y.w-x.w).slice(0,5).map((b,i)=>`<tr><td>${i?'':'Best seasons'}</td><td class="r"><b>${recStr(b.w,b.l,b.t)}</b> <span class="note">${esc(b.season)}</span></td></tr>`).join('')}"""
pairs=[(old_best,new_best),
 ("a.mostPts.slice(0,3).map((g,i)=>`<tr><td>${i?'':'Most points in a game'}","a.mostPts.slice(0,5).map((g,i)=>`<tr><td>${i?'':'Most points in a game'}"),
 ("a.bigWins.slice(0,3).map((g,i)=>`<tr><td>${i?'':'Biggest wins'}","a.bigWins.slice(0,5).map((g,i)=>`<tr><td>${i?'':'Biggest wins'}")]
for a,b in pairs:
    if b in s: continue
    assert s.count(a)==1,a[:50]
    s=s.replace(a,b)
open(p,'w').write(s); print('ok',p)
