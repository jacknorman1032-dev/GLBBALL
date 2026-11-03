import sys
# School pages: show 25 most-played opponents instead of 15 (Jack, Oct 30, 2026).
p=sys.argv[1]; s=open(p).read()
a="a.opponents.slice(0,15),{k:'n',dir:-1});"; b="a.opponents.slice(0,25),{k:'n',dir:-1});"
if b not in s:
    assert s.count(a)==1; s=s.replace(a,b)
open(p,'w').write(s); print('ok',p)
