import sys
# School page stat board: add a Regional titles count (Jack, Oct 30, 2026).
# With a game log: seasons that won a regional or went further (finish champ/ru/ff/reg).
# Plus the tournament_summary list, and every Final Four season (reaching it meant winning a regional).
# Schools with neither a game log nor a tournament summary don't show the stat.
p=sys.argv[1]; s=open(p).read()
old="""${a?`<div><span class="v">${a.seasons.filter(x=>x.finish&&x.finish!=='out').length}</span><span class="k">District titles+</span></div>`:''}"""
new=old+"""
      ${(a||s.tournament_summary?.regional_titles)?`<div><span class="v">${new Set([...(a?a.seasons.filter(x=>['champ','ru','ff','reg'].includes(x.finish)).map(x=>x.season):[]),...(s.tournament_summary?.regional_titles||[]),...h.ff]).size}</span><span class="k">Regional titles</span></div>`:''}"""
if new not in s:
    assert s.count(old)==1
    s=s.replace(old,new)

# Note under the stat board explaining the two tournament counts (Jack, Oct 30, 2026)
old2="""<span class="k">Program points</span></div>
    </div>`;
  // 2. banners"""
new2="""<span class="k">Program points</span></div>
    </div>${a?`<p class="note">District titles+ counts every season a team won its district or played on past the district round. That includes early years when the tournament started at the regional level and years a team advanced after losing its district final, so it can run a little higher than a count of district final wins alone. Regional titles counts seasons a team won a regional or went further.</p>`:''}`;
  // 2. banners"""
if new2 not in s:
    assert s.count(old2)==1
    s=s.replace(old2,new2)
open(p,'w').write(s); print('ok',p)
