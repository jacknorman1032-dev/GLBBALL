import sys
p=sys.argv[1]; s=open(p).read()
css_anchor=".empty{color:var(--muted);font-style:italic}\n"
css=css_anchor+"""/* uniforms */
.unis{display:flex;justify-content:space-around;flex-wrap:wrap;gap:20px;background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:22px 16px}
.unis figure{margin:0;display:grid;justify-items:center;gap:8px}
.unis img{width:120px;height:auto}
.unis figcaption{font-weight:700;font-size:20px;color:#121a23}
"""
js_anchor="const SCHOOLS=DATA.schools;\n"
js=js_anchor+"""// uniform drawings, published as files next to the page
const UNIFORMS={'east-lansing':[{label:'Home',src:'uniforms/east-lansing-home.svg'},{label:'Away',src:'uniforms/east-lansing-away.svg'}],'waverly':[{label:'Home',src:'uniforms/waverly-home.svg'},{label:'Away',src:'uniforms/waverly-away.svg'}],'sexton':[{label:'Home',src:'uniforms/sexton-home.svg'},{label:'Away',src:'uniforms/sexton-road.svg'},{label:'Alternate',src:'uniforms/sexton-away.svg'}],'dewitt':[{label:'Home',src:'uniforms/dewitt-home.svg'},{label:'Away',src:'uniforms/dewitt-road.svg'}],'holt':[{label:'Home',src:'uniforms/holt-home.svg'},{label:'Away',src:'uniforms/holt-road.svg'}],'grand-ledge':[{label:'Home',src:'uniforms/grand-ledge-home.svg'},{label:'Away',src:'uniforms/grand-ledge-away.svg'},{label:'Alternate',src:'uniforms/grand-ledge-alt.svg'}],'okemos':[{label:'Home',src:'uniforms/okemos-home.svg'},{label:'Away',src:'uniforms/okemos-away.svg'}],'mason':[{label:'Home',src:'uniforms/mason-home.svg'},{label:'Away',src:'uniforms/mason-away.svg'}],'everett':[{label:'Home',src:'uniforms/everett-home.svg'},{label:'Away',src:'uniforms/everett-road.svg'}],'eastern':[{label:'Home',src:'uniforms/eastern-home.svg'},{label:'Away',src:'uniforms/eastern-road.svg'}],'williamston':[{label:'Home',src:'uniforms/williamston-home.svg'}]};
"""
view_anchor="  // 3. best teams\n"
view="""  const unis=UNIFORMS[id];
  if(unis)html+=`<div class="block"><h2>Uniforms</h2><div class="unis">${unis.map(u=>`<figure><img src="${esc(u.src)}" alt="${esc(s.name)} ${esc(u.label.toLowerCase())} uniform"><figcaption>${esc(u.label)}</figcaption></figure>`).join('')}</div></div>`;
"""+view_anchor
for a,b in [(css_anchor,css),(js_anchor,js),(view_anchor,view)]:
    assert s.count(a)==1,a
    s=s.replace(a,b)
open(p,'w').write(s); print('ok',p)
