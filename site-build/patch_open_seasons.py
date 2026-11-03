import sys
# School pages: Season-by-season records open by default (Jack, Oct 31, 2026). Run after patch_layout.py.
p=sys.argv[1]; s=open(p).read()
old='<details class="block fold"><summary><h2>Season-by-season records</h2>'
new='<details class="block fold" open><summary><h2>Season-by-season records</h2>'
if new not in s:
    assert s.count(old)==1,'season-by-season anchor missing'
    s=s.replace(old,new)
open(p,'w').write(s); print('ok',p)
