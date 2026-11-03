import sys, json
# Lansing Hill (Panthers): a closed Lansing city school, in the league with Sexton, Everett, Eastern, Waverly and
# East Lansing from about 1971-72 to 1980-81. Added Nov 1, 2026 at Jack's request. Only district results are known
# so far (michigan-football.com). Full name Harry Hill; orange and black per Jack (Harry Hill Alums group merch, Nov 1, 2026). No logo, coaches or season records were found. Skips if already present.
HILL={"nickname":"Panthers","colors":{"primary":"#F26B1D","secondary":"#111111","names":"Orange and Black"},"city":"Lansing","status":"Closed school (about 1971-72 to 1980-81)",
 "state_titles":[],"state_runner_ups":[],"final_fours":[],"notable_players":[],"notable_coaches":[],
 "tournament_summary":{"through_season":"1980-81","record":"1-10","district_titles":[],"regional_titles":[],
  "best_finish":{"season":"1972-73","round":"District","opponent":"Lansing Eastern","score":"61-67","season_tournament_record":"1-1"},
  "regional_exits":[],"source":"https://michigan-football.com/bb/lhhill.htm"},
 "sources":["https://michigan-football.com/bb/lhhill.htm","https://michmemories.org/exhibits/topics/catalog/7ab5cc4026eb3d5a5281347860f2f44c"],
 "id":"hill","name":"Lansing Hill","short":"Hill","aliases":["Hill","Harry Hill","Lansing Harry Hill"]}
p=sys.argv[1]; s=open(p).read()
if '"id":"hill","name":"Lansing Hill"' not in s:
    key='{"schools":['; assert s.count('const DATA='+key)==1
    s=s.replace('const DATA='+key,'const DATA='+key+json.dumps(HILL,separators=(',',':'),ensure_ascii=False)+',',1)
# pages built before Nov 1 colors: add colors and aliases in place
old='{"nickname":"Panthers","city":"Lansing","status":"Closed school'
if old in s:
    s=s.replace(old,'{"nickname":"Panthers","colors":{"primary":"#F26B1D","secondary":"#111111","names":"Orange and Black"},"city":"Lansing","status":"Closed school',1)
    s=s.replace('"id":"hill","name":"Lansing Hill","short":"Hill","aliases":["Hill"]}','"id":"hill","name":"Lansing Hill","short":"Hill","aliases":["Hill","Harry Hill","Lansing Harry Hill"]}',1)
open(p,'w').write(s); print('ok',p)
