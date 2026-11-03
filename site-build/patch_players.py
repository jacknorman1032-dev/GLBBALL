import sys
# Notable players: newest graduating class first, players with no grad year last.
p=sys.argv[1]; s=open(p).read()
pairs=[
 ("list.sort((a,b)=>String(a.p.grad_year||'9999').localeCompare(String(b.p.grad_year||'9999')));",
  "list.sort((a,b)=>byGrad(a.p,b.p));"),
 ("const players=(s.notable_players||[]);",
  "const players=[...(s.notable_players||[])].sort(byGrad);"),
 ("function playerCard(p,s,showSchool){",
  "function byGrad(a,b){const y=p=>parseInt(p.grad_year)||0;return y(b)-y(a)}\nfunction playerCard(p,s,showSchool){"),
]
for a,b in pairs:
    if b in s: continue
    assert s.count(a)==1,a
    s=s.replace(a,b)
open(p,'w').write(s); print('ok',p)
