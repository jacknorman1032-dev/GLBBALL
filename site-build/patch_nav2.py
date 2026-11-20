import sys
# Navigation, part 2 (Jack, Nov 20, 2026). Run after patch_nav.py (CSS lands in the page's own stylesheet, so the
# phone-layout patches that follow patch_nav.py don't care about order). Adds:
#   1. Scroll memory: browser Back (or the page's "‹ Back" link) returns to where you were on the previous page,
#      not the top. Positions are kept per page for the visit (in memory; a reload starts fresh). New pages
#      still open at the top.
#   2. School pages: the Overview / History / People / Records tabs stay pinned under the header while you
#      scroll; each tab with two or more sections gets a row of "jump to" links at its top; switching tabs while
#      scrolled down brings you to the top of the new tab.
#   3. A "back to top" button on every page once you're about two screens down.
#   4. Page titles: the browser tab, history and bookmarks read "East Lansing · History — Greater Lansing Hoops",
#      "Mr. Basketball — Greater Lansing Hoops", a player's name, etc. Home keeps the site's own title.
# Usage: python3 -I patch_nav2.py page.html. Re-runnable: the code and CSS blocks are replaced on every run.
p = sys.argv[1]
s = open(p).read()

def rep(a, b):
    global s
    if b in s: return
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b, 1)

def block(start, end, body, anchor_fn):
    global s
    if start in s:
        a = s.index(start); b = s.index(end, a) + len(end)
        s = s[:a] + body + s[b:]
    else:
        i = anchor_fn()
        s = s[:i] + body + '\n' + s[i:]

CS, CE = '// ---- navigation 2 (patch_nav2.py)', '// ---- end navigation 2'
CODE = CS + r'''
const NAV2_TITLE=document.title,NAV2_SCROLL={};let NAV2_BASE=null;
try{history.scrollRestoration='manual'}catch(e){}
function nav2Save(){if(NAV2_BASE!==null)NAV2_SCROLL[NAV2_BASE]=window.scrollY}
window.addEventListener('scroll',()=>{if(NAV2_BASE!==null&&NAV2_BASE===(location.hash||'#home').slice(1).split('/')[0])NAV2_SCROLL[NAV2_BASE]=window.scrollY;nav2Top()},{passive:true});
const NAV2_HUB={honors:'All-state honors',allconf:'All-conference',lsj:'LSJ All-Area',mrbasketball:'Mr. Basketball',rivalries:'Rivalries',data:'Add data'};
function nav2Title(h){
  if(!h||h==='home'){document.title=NAV2_TITLE;return}
  const h1=document.querySelector('#app section.view h1');
  let t=NAV2_HUB[h]||(h1?h1.textContent.trim():'');
  if(h.startsWith('school-')){const b=document.querySelector('.stabs [role=tab][aria-selected="true"]');if(b&&b.id!=='stab-ov')t+=' · '+b.textContent.trim()}
  document.title=t?t+' — Greater Lansing Hoops':NAV2_TITLE;
}
function nav2Hdr(){const hd=document.querySelector('header.top');if(hd)document.documentElement.style.setProperty('--hdr',hd.offsetHeight+'px')}
window.addEventListener('resize',nav2Hdr);
// jump-to links for each school tab with 2+ sections
function nav2Jumps(){
  document.querySelectorAll('[role=tabpanel][id^="spanel-"]').forEach(panel=>{
    if(panel.querySelector(':scope>.jumps'))return;
    const T=[...panel.querySelectorAll(':scope>.block,:scope>.pgrid>*')].map(el=>{
      const hd=el.querySelector('h2');return hd?[el,hd.textContent.trim()]:null}).filter(Boolean);
    if(T.length<2)return;
    T.forEach(([el],i)=>{if(!el.id)el.id=panel.id+'-j'+i});
    panel.insertAdjacentHTML('afterbegin',`<nav class="jumps" aria-label="Jump to section"><span class="jl">Jump to</span>${T.map(([el,t])=>`<a href="#" data-j="${el.id}">${esc(t)}</a>`).join('')}</nav>`);
  });
}
document.addEventListener('click',e=>{
  const j=e.target.closest&&e.target.closest('.jumps a[data-j]');
  if(j){e.preventDefault();const el=document.getElementById(j.dataset.j);if(el){el.scrollIntoView({behavior:'smooth',block:'start'});const f=el.querySelector('summary,h2');if(f){f.setAttribute('tabindex','-1');f.focus({preventScroll:true})}}return}
  const b=e.target.closest&&e.target.closest('.stabs [role=tab]');
  if(b)setTimeout(()=>{
    nav2Jumps();nav2Title((location.hash||'#home').slice(1).split('/')[0]);
    // the tab row is pinned, so measure from what sits above it: the top of the tab row's natural spot
    const tabs=b.closest('.stabs'),prev=tabs.previousElementSibling,hdr=parseFloat(getComputedStyle(tabs).top)||0;
    const y=Math.max(0,(prev?prev.getBoundingClientRect().bottom:tabs.getBoundingClientRect().top)+window.scrollY-hdr);
    if(window.scrollY>y+1)window.scrollTo(0,y);
  });
});
// back-to-top button
function nav2Top(){const t=document.getElementById('totop');if(t)t.classList.toggle('on',window.scrollY>window.innerHeight*2)}
function nav2After(h,H0,wentBack){
  NAV2_BASE=h||'home';
  nav2Hdr();nav2Jumps();nav2Title(h);
  if(!document.getElementById('totop')){
    document.body.insertAdjacentHTML('beforeend','<button type="button" id="totop" aria-label="Back to top">↑<span> Top</span></button>');
    document.getElementById('totop').onclick=()=>{window.scrollTo({top:0,behavior:'smooth'});const a=document.querySelector('#app h1');if(a){a.setAttribute('tabindex','-1');a.focus({preventScroll:true})}};
  }
  const y=wentBack?NAV2_SCROLL[NAV2_BASE]||0:0;
  window.scrollTo(0,y);
  if(y){let n=0;const again=()=>{if(window.scrollY<y-2&&n++<6){window.scrollTo(0,y);setTimeout(again,80)}};setTimeout(again,60)}
  nav2Top();
}
''' + CE

CSS_S, CSS_E = '/* navigation 2 (patch_nav2.py) */', '/* end navigation 2 */'
CSS = CSS_S + r'''
.stabs{position:sticky;top:var(--hdr,57px);z-index:5;background:var(--bg)}
[role=tabpanel][id^="spanel-"]>.block,[role=tabpanel][id^="spanel-"]>.pgrid>*{scroll-margin-top:calc(var(--hdr,57px) + 64px)}
.jumps{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;margin:4px 0 18px}
.jumps .jl{font-family:var(--cond);font-weight:600;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-right:2px}
.jumps a{font-size:14px;color:var(--ink);text-decoration:none;background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:4px 11px;white-space:nowrap}
.jumps a:hover{background:var(--sunk)}
.jumps a:focus-visible{outline:2px solid var(--maple);outline-offset:1px}
#totop{position:fixed;right:18px;bottom:18px;z-index:20;font-family:var(--cond);font-weight:600;font-size:15px;letter-spacing:.05em;text-transform:uppercase;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:9px 15px;box-shadow:0 2px 10px rgba(0,0,0,.18);cursor:pointer;opacity:0;pointer-events:none;transform:translateY(8px);transition:opacity .2s,transform .2s}
#totop.on{opacity:1;pointer-events:auto;transform:none}
#totop:hover{background:var(--sunk)}
#totop:focus-visible{outline:2px solid var(--maple);outline-offset:2px}
@media (max-width:640px){.jumps{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;margin-right:-16px;padding-right:16px}.jumps::-webkit-scrollbar{display:none}#totop{right:12px;bottom:12px;padding:10px 13px}#totop span{display:none}}
@media (prefers-reduced-motion:reduce){#totop{transition:none}}
''' + CSS_E

block(CS, CE, CODE, lambda: s.index('// ---- end navigation\n'))
block(CSS_S, CSS_E, CSS, lambda: s.index('</style>', s.index('/* Layout: a gym')))

# route(): save the old page's scroll before rendering; restore it (or go to the top) after
rep("const H0=(location.hash||'#home').slice(1),h=H0.split('/')[0],SUB=",
    "nav2Save();const NAV2_N=NAV_STACK.length;\n  const H0=(location.hash||'#home').slice(1),h=H0.split('/')[0],SUB=")
rep("backBar(h,H0);\n  window.scrollTo(0,0);", "backBar(h,H0);\n  nav2After(h,H0,NAV_STACK.length<NAV2_N);")

open(p, 'w').write(s)
print('patch_nav2: ok')
