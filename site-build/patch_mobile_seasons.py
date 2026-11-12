import sys
# Phone layout for school pages (Jack, Nov 11, 2026).
#   1. Fold-out sections (Season-by-season records, Coaches, ...) no longer stretch to the width of the table
#      inside them. Before, a wide table made the whole page 800-1000px wide on a phone, so the page slid
#      sideways and the header, search box and charts were cut off.
#   2. On phones (<=640px) the season-by-season table becomes one card per season, like the coaches table:
#      season and finish chip on top, coach under it, then record, win %, league, postseason and scoring,
#      each with a label. Tapping a season still opens its games below the card.
#   3. Game cards on phones (every game list): a game with a note kept its desktop 260px minimum width for the
#      note, which pushed the score past the card's right edge. Now the note wraps inside the card.
# Usage: python3 -I patch_mobile_seasons.py page.html. Re-runnable: the CSS block is replaced on every run.
p = sys.argv[1]
s = open(p).read()
START, END = '/* mobile-seasons (patch_mobile_seasons.py) */', '/* end mobile-seasons */'
CSS = START + r'''
details.fold>.fold-body{grid-template-columns:minmax(0,1fr)}
details.fold>.fold-body>*{min-width:0}
details.fold::details-content{min-width:0}
@media (max-width:640px){
.gtbl tbody>tr{grid-template-columns:minmax(0,1fr) auto}
.gtbl tbody .gnotes{min-width:0}
#seasons>.tbl{overflow:visible}
#seasons>.tbl>table>thead{display:none}
#seasons>.tbl>table,#seasons>.tbl>table>tbody{display:block}
#seasons>.tbl>table>tbody>tr.click{display:flex;flex-wrap:wrap;align-items:baseline;gap:3px 14px;padding:11px 12px;border-bottom:1px solid var(--line)}
#seasons>.tbl>table>tbody>tr.click.open{background:var(--sunk)}
#seasons>.tbl>table>tbody>tr.click td{display:block;padding:0;border:0;background:none;white-space:normal;text-align:left;font-size:14px;color:var(--muted)}
#seasons>.tbl>table>tbody>tr.click td:nth-child(1){order:1;font-weight:700;font-size:17px;color:var(--ink)}
#seasons>.tbl>table>tbody>tr.click td:nth-child(1)::after{content:" \25B8";color:var(--maple-ink);font-size:13px}
#seasons>.tbl>table>tbody>tr.click.open td:nth-child(1)::after{content:" \25BE"}
#seasons>.tbl>table>tbody>tr.click td:nth-child(7){order:2;margin-left:auto}
#seasons>.tbl>table>tbody>tr.click td:nth-child(7):empty{display:none}
#seasons>.tbl>table>tbody>tr.click td:nth-child(2){order:3;flex-basis:100%;font-size:15px;color:var(--ink)}
#seasons>.tbl>table>tbody>tr.click td:nth-child(3){order:4;font-weight:700;font-size:16px;color:var(--ink)}
#seasons>.tbl>table>tbody>tr.click td:nth-child(4){order:5}
#seasons>.tbl>table>tbody>tr.click td:nth-child(5){order:6}
#seasons>.tbl>table>tbody>tr.click td:nth-child(6){order:7}
#seasons>.tbl>table>tbody>tr.click td:nth-child(8){order:8}
#seasons>.tbl>table>tbody>tr.click td:nth-child(9){order:9}
#seasons>.tbl>table>tbody>tr.click td:nth-child(10){order:10}
#seasons>.tbl>table>tbody>tr.click td:nth-child(5)::before{content:"League "}
#seasons>.tbl>table>tbody>tr.click td:nth-child(6)::before{content:"Postseason "}
#seasons>.tbl>table>tbody>tr.click td:nth-child(8)::before{content:"PF "}
#seasons>.tbl>table>tbody>tr.click td:nth-child(9)::before{content:"PA "}
#seasons>.tbl>table>tbody>tr.click td:nth-child(10)::before{content:"Margin "}
#seasons>.tbl>table>tbody>tr.detail{display:block;border-bottom:1px solid var(--line)}
#seasons>.tbl>table>tbody>tr.detail>td{display:block;padding:0}
#seasons>.tbl>table>tbody>tr.detail .inner{position:static;width:auto;overflow-x:auto;padding:6px 8px 12px}
}
''' + END
if START in s:
    a = s.index(START); b = s.index(END) + len(END)
    s = s[:a] + CSS + s[b:]
else:
    i = s.index('</style>')
    s = s[:i] + CSS + '\n' + s[i:]
open(p, 'w').write(s)
print('patch_mobile_seasons: ok')
