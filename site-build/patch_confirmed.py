import sys, json
# Facts Jack confirmed that aren't in the honors file or overrides yet; applied to the built page.
HONORS=[
 {"season":"2016-17","name":"Brandon Johns Jr.","listed_as":"","school":"east-lansing","listed_school":"East Lansing","yr":"Jr","tier":"first","level":"Class A","selector":"AP","src":"Confirmed by Jack Norman, Oct 30, 2026","listed_tier":"First Team All-State"},
 {"season":"2012-13","name":"Trevor Manuel","listed_as":"","school":"sexton","listed_school":"Lansing Sexton","yr":"So","tier":"hm","level":"Class B","selector":"AP","src":"Confirmed by Jack Norman, Oct 30, 2026","listed_tier":"Honorable Mention"},
]
CARD_ALSO={"Trevor Manuel":[{"school":"sexton","seasons":"2011-12 to 2012-13"}]}

# East Lansing notable coaches: years and records from the ELHS game log (Jack, Oct 30, 2026)
COACH_FIELDS={
 "Gus Ganakas":{"years":"1952-53 to 1963-64 (12 seasons)",
  "notes":"176-54 (.765), 109-35 in league games (the Hall of Fame lists 176-53). Coached the 1958 Class B state champions (24-0), part of a 38-game winning streak from December 1957 to February 1959, and the 1958 team won his seventh straight conference title. Unbeaten regular seasons in 1961-62 and 1962-63; also reached regional finals in 1956 and 1959 and the state quarterfinals in 1961. At Michigan State: assistant coach 1966-69, head coach 1969-76 (89-84), assistant athletic director 1976-97, special assistant to Tom Izzo 1997-2000, and longtime Spartan radio analyst. Greater Lansing Area Sports Hall of Fame, 2003. Died Jan. 11, 2019.",
  "add_source":"https://lansingsportshalloffame.org/people/gus-ganakas/"},
 "Steve Finamore":{"years":"2010-11 to 2017-18 (8 seasons)",
  "notes":"128-44 (.744), 79-30 in league games. Two straight CAAC Blue titles; coached Brandon Johns Jr. (23-1 in 2015-16 and 24-1 in 2016-17, both ending in the regional final). Resigned in February 2018 with the team 15-2; under interim coach Kevin Mayes it went on to win the regional and reach the state quarterfinals. Also coached at Okemos and, in 2018-19, Lansing Sexton. Died Nov. 14, 2024, at 60.",
  "add_source":"https://www.vickersfuneralhomes.com/obituaries/Steven-Richard-Finamore?obId=33951678"},
 "Ray Mitchell":{"years":"2018-19 to present (8 seasons)",
  "notes":"154-35 (.815), 74-17 in league games. East Lansing graduate: a 1992 Lansing State Journal Dream Team pick who averaged 20.4 points and played college basketball at Eastern Michigan. Assistant to Carlton Valentine at Lansing Sexton on the back-to-back Class B state champions in 2011 and 2012. Coached the 2025 Division 1 state champions (28-1) and the 2026 Division 1 runners-up (27-2); state quarterfinals in 2021, 2023 and 2024.",
  "add_source":"https://www.lansingstatejournal.com/story/sports/high-school/2018/06/23/east-lansing-boys-basketball-coach-ray-mitchell/726373002/"},
 # Everett's Johnny Jones: from Graham Couch's LSJ column, May 1, 2025 (pasted by Jack, Oct 30, 2026)
 "Johnny Jones":{"years":"32 years at Everett, coaching girls and boys; coached both teams through 2007-08, the first season girls basketball was played in the winter",
  "notes":"Won the 2004 boys Class A title. His girls teams reached three straight Class A finals, starting in the fall of 1999: runners-up in 1999, then champions in 2000 and 2001. Had 334 boys wins after 2003-04. As a player at Battle Creek Central he was a standout in basketball and a running back on the 1966 football state champions (a title decided by poll at the time), then played football at Central Michigan. Died April 2025 at age 75.",
  "add_source":"https://www.lansingstatejournal.com/story/sports/columnists/graham-couch/2025/05/01/johnny-jones-won-big-with-everett-basketball-his-legacy-runs-deeper/83354652007/"},
 # Sexton's Carlton Valentine: seasons and record from the Sexton game log; honors from his Hall of Fame page (Jack, Oct 30, 2026)
 "Carlton Valentine":{"years":"2005-06, 2007-08 to 2012-13, and 2014-15 to 2015-16 (9 seasons)",
  "notes":"152-62 (.710), 81-37 in league games (the Hall of Fame lists 152-61). Won Class B state titles in 2011 (26-2) and 2012 (27-1) and was runner-up in 2010; six CAAC titles. Coach of the Year in 2012 from the Detroit News, the Detroit Free Press, BCAM (overall) and the Michigan High School Coaches Association; Lansing State Journal Coach of the Year in 2011 and 2012; BCAM Class B Coach of the Year in 2011. At Michigan State he lettered from 1984 to 1988 and was the 1987-88 captain, leading scorer, leading rebounder and team MVP. Father of Denzel and Drew Valentine. Greater Lansing Area Sports Hall of Fame, 2025.",
  "add_source":"https://lansingsportshalloffame.org/people/carlton-valentine/"},
 # Sexton's Clayton Kowalk: details from his Hall of Fame page (Jack, Oct 30, 2026)
 "Clayton Kowalk":{"years":"1950s-60s",
  "notes":"Won back-to-back Class A titles in 1959 (80-79 in overtime over Hamtramck) and 1960 (22-1). Michigan Coaches Association Basketball Coach of the Year in 1954. Ken Eckman was his assistant in 1959. Later athletic director for the Lansing School District. Co-founder of the Greater Lansing Area Sports Hall of Fame, which inducted him in 1978; also in the Michigan High School Coaches Hall of Fame.",
  "add_source":"https://lansingsportshalloffame.org/people/clayton-kowalk-2/"},
 # Waverly's Phil Odlum: details from his Hall of Fame page (Jack, Oct 30, 2026)
 "Phil Odlum":{"years":"",
  "notes":"More than 400 career wins. Coached Waverly's 2000 Class A state champions (25-2), led by Marcus Taylor, who credited him at his 2017 Hall of Fame induction. Eight league titles, seven district titles and one regional title. Also coached John Smoltz, Muhsin Muhammad and Danton Cole. State Class A & B Coach of the Year in 2000; Lansing State Journal Coach of the Year four times in Class A & B, plus once overall; BCAM Hall of Fame (2001) and Michigan High School Coaches Hall of Fame (2007). Went to high school at Lexington and played basketball at Central Michigan. Greater Lansing Area Sports Hall of Fame.",
  "add_source":"https://lansingsportshalloffame.org/phillip-odlum/"},
 # Eastern's Paul Cook: details from his Hall of Fame page (Jack, Oct 30, 2026)
 "Paul Cook":{"years":"Coached boys from 1949 to 1991 at several schools, including Lansing Eastern",
  "notes":"Career boys record of 639-245 across Jackson St. Johns, Lansing Resurrection, Gabriels, Lansing Catholic and Eastern, with 17 conference, 13 district and 6 regional titles. Won the 1980 Class A title with Eastern (26-1). 1978-79 AP Class A Coach of the Year and Lansing YMCA Outstanding Achievement Award; 1985 Region Four National Coach of the Year. Later coached the Lansing Catholic girls from 1993 to 2002 (189-46), winning the 1995 Class C title. A Resurrection High School graduate. Inducted into the Michigan HS Coaches HOF (1978), the BCAM HOF (1986) and the Greater Lansing Area Sports HOF (1990).",
  "add_source":"https://lansingsportshalloffame.org/people/paul-cook/"},
 # Eastern's Walter Graff: Hall of Fame page plus Jack's text (Oct 31, 2026)
 "Walter Graff":{"years":"1928 to 1941",
  "notes":"Coached basketball, baseball and football at Eastern from its first years of competition. His 1934 basketball team won the Class A state title, and his football teams won 26 straight games from 1932 to 1934. Lettered in basketball and baseball at Western Michigan. Greater Lansing Area Sports Hall of Fame, 1980.",
  "add_source":"https://lansingsportshalloffame.org/people/walter-graff/"},
 # Holt's Bruce Larner: "The Larner legacy" box, Lansing State Journal, April 11, 2006, p. 15 (clipped by Jack, Oct 31, 2026)
 "Bruce Larner":{"years":"1985-86 to 2005-06 (21 seasons)",
  "notes":"222-242 career record and two conference titles. Won three district titles, all in his last three seasons; the first came in 2003-04 after he lost his first five district finals. Won the 2005 Class A state title (26-2), getting his 200th win in the semifinal. 2005 AP Class A Coach of the Year and State Journal Dream Team Coach of the Year.",
  "add_source":"https://www.newspapers.com/image/210463990/"},
 # Holt's Matt Essell: Jack's pasted LSJ text plus WKAR, May 7, 2017 (Oct 31, 2026). Jack confirmed he directly followed Bruce Larner.
 "Matt Essell":{"years":"2006-07 to 2016-17 (11 seasons)",
  "notes":"165-88 (.652), with six district titles and three CAAC Blue titles. Reached the regional final in his first season, losing to Ann Arbor Pioneer, and three more times after that, but never got past the regional final. His last team won a district title in 2017 and reached the regional semifinal. Coached Jaron Faulds. Spent more than two decades in the Holt program, including as JV boys and girls coach, and stepped down in May 2017 to spend more time with his family.",
  "add_source":"https://www.wkar.org/current-sports-on-am870/2017-05-07/longtime-holt-basketball-coach-essell-puts-family-first-retires-from-coaching ; https://www.lansingstatejournal.com/story/sports/high-school/2017/03/10/size-shooting-lead-holt-boys-past-mason-district-title/98999836/"},
 # DeWitt's Jim Lutzke: DeWitt Athletic Hall of Fame, Class of 2008 (Jack, Oct 31, 2026)
 "Jim Lutzke":{"years":"1990s at DeWitt (coached the 1994-95 and 1995-96 teams), after coaching Williamston",
  "notes":"214-77 (.735) career record. Won five straight district titles at Williamston and then district titles in each of his first five seasons at DeWitt, ten in a row. Coached the 1994-95 team (26-1, first regional title, first undefeated regular season) and the 1995-96 team; both reached the Class B Final Four, going 51-3 combined, and are in the DeWitt Athletic Hall of Fame. BCAM Class B Coach of the Year in 1995. Also DeWitt's athletic director and human resources director. Died of pancreatic cancer in 1999. DeWitt Athletic Hall of Fame, 2008.",
  "add_source":"https://sites.google.com/a/gapps.dewittschools.net/dhs-athletic-hall-of-fame/class-of-2008/jim-lutzke"},
 # Lansing Catholic's Darren Zwick: record and titles from Jack (Oct 31, 2026); 2014-15 was his 16th and last season
 "Darren Zwick":{"years":"1999-2000 to 2014-15 (16 seasons)",
  "notes":"200-94 (.680), including three 20-win seasons. Eight league titles, four district titles and one regional title, and coached the 2008 Class B state champions (23-4).",
  "add_source":""},
 # Lansing St. Mary's Ray Lehman: details from his Hall of Fame page (Jack, Oct 31, 2026)
 "Ray Lehman":{"years":"1928 to 1937 (Lansing St. Mary)",
  "notes":"173-43 (.801). Won back-to-back Class C titles in 1936 and 1937, plus five regional and eight district titles. A St. Mary's graduate who played basketball there. Killed in action in World War II. Greater Lansing Area Sports Hall of Fame, 1981.",
  "add_source":"https://lansingsportshalloffame.org/people/ray-lehman/"},
 # Lansing St. Mary's Len Lapka: details from his Hall of Fame page (Jack, Oct 31, 2026)
 "Len Lapka":{"years":"Coached the 1953-54 team (Lansing St. Mary); still coaching in Lansing in the 1970s",
  "notes":"Coached the 1954 Class C state champions. City of Lansing Basketball Coach of the Year in 1970 and Baseball Coach of the Year in 1975, with Diamond Classic titles in 1975 and 1976. Michigan Baseball Coaches Hall of Fame, 1995. On Michigan State's 1946 varsity football team. Greater Lansing Area Sports Hall of Fame, 2003.",
  "add_source":"https://lansingsportshalloffame.org/people/len-lapka/"},
 # Everett's George Fox: details from his Hall of Fame page (Jack, Oct 31, 2026)
 "George Fox":{"years":"Coached through at least 1975-77 (full span not found)",
  "notes":"Career record of 305-125 per the Hall of Fame (WFMK gives 350-125 at Everett). Won the 1977 Class A title (27-1) and was named UPI and AP Coach of the Year that season. The first Michigander to win a state title as both a player and a coach: he captained Fowler's 1952 Class D champions. At Alma College he was team MVP in 1953 and 1954 and All-MIAA in 1954. Greater Lansing Area Sports Hall of Fame, 1990. Died in April 2023 at age 88.",
  "add_source":"https://lansingsportshalloffame.org/people/george-fox/"},
 # Everett: 65-52 is Jack's placeholder until the Sexton game-log import gives a computed record (Oct 30, 2026)
 "Desmond Ferguson":{"years":"2012-13 to 2016-17 (5 seasons)",
  "notes":"65-52 (.556). Everett alumnus and former NBA player. Took over a program that went 5-16 in 2011-12, when he was an assistant, and led Everett to back-to-back Class A semifinals in 2015 (24-3) and 2016 (16-11). Stepped down in May 2017 to focus on his business interests. Greater Lansing Area Sports Hall of Fame (2023).",
  "add_source":"https://lansingsportshalloffame.org/desmond-ferguson-3/ ; https://www.lansingstatejournal.com/story/sports/high-school/2017/05/30/desmond-ferguson-steps-down-everett/356719001/ ; https://www.wkar.org/sports/2015-02-16/fergusons-plan-turning-everett-hoops-around-current-sports-wkar"},
}

# Notable coaches listed at more than one school: (school id, name) -> fields; found in that school's block (Jack, Oct 30, 2026)
SCHOOL_COACH_FIELDS={
 ("okemos","Dan Stolz"):{"years":"1994-95 to 2011-12",
  "notes":"Son of Stan. 338-78 at Okemos (428-99 counting Williamston), with 16 league titles, 12 district titles and 2 regional titles. Coached the 2006 Class A runners-up (25-3), who lost the first double-overtime final in Class A history. Class A Coach of the Year in 2006 and Regional Coach of the Year four times. Moved Okemos into the CAAC's top division. Also coached state champions in girls tennis (1993) and Class A softball (1999), plus CAAC Blue titles in boys and girls golf. As an Okemos player he was All-State in 1974 and 1975; at Alma College he was All-MIAA three times and the 1978 MIAA MVP (Alma Hall of Fame, 1996). Greater Lansing Area Sports Hall of Fame, 2017.",
  "add_source":"https://lansingsportshalloffame.org/people/dan-stolz/"},
 ("williamston","Dan Stolz"):{"years":"",
  "notes":"90-21 at Williamston with three league titles; Class C Coach of the Year in 1983. Went on to coach Okemos from 1994-95 to 2011-12 (338-78), for 428-99 combined. Greater Lansing Area Sports Hall of Fame, 2017.",
  "add_source":"https://lansingsportshalloffame.org/people/dan-stolz/"},
}

# Extra East Lansing notable coaches, inserted before the named coach (Jack, Oct 30, 2026)
ADD_COACHES=[("east-lansing","Steve Finamore",{"name":"Chris Ferguson","years":"1989-90 to 2000-01 (12 seasons)",
 "notes":"132-126 (.512), 76-92 in league games. Took over a program that had gone 38-68 in the five seasons before him, including 2-19 in 1988-89, and posted seven winning seasons, among them the 1991-92 team (16-5) led by future East Lansing coach Ray Mitchell and the 1996-97 regional champions (21-4) that reached the state quarterfinals. As a player he was captain and MVP of Lansing Sexton's 1959 Class A state champions and played at Michigan State in 1961 and 1962. Greater Lansing Area Sports Hall of Fame, 2010.",
 "source":"https://lansingsportshalloffame.org/people/chris-ferguson/"}),
 # Sexton's Mike Major: seasons and record from the Sexton game log; Sexton Athletic HOF per WILX (Jack, Oct 31, 2026)
 ("sexton","Carlton Valentine",{"name":"Mike Major","years":"January 1990 to 2004-05 (16 seasons; took over from Al Darden midway through 1989-90)",
 "notes":"228-127 (.642), 141-80 in league games, in the Sexton game log (his 17 games of 1989-90 went 13-4). Five district titles (1992, 1993, 1994, 2001 and 2003). His 2000-01 team won the regional, beating Garden City and Ypsilanti, and reached the state quarterfinals, losing to Kalamazoo Central 83-72. Also coached Sexton's girls. Lansing Sexton Athletic Hall of Fame, Class of 2025.",
 "source":"https://www.wilx.com/2025/08/02/mike-major-saddi-washington-headline-lansing-sextons-athletic-hof-class-2025/"}),
 # Sexton's Doug Herner: Hall of Fame page plus his Michigan State staff bio (Jack, Nov 1, 2026). Must come after Mike Major above.
 # Update the game-log sentence as more of his seasons are entered.
 ("sexton","Mike Major",{"name":"Doug Herner","years":"1964 to 1984 (Al Darden took over in 1984-85)",
 "notes":"248-147 (.628) per the Hall of Fame; Sexton's game log has only his last season so far, 1983-84 (23-1, 14-0 in the league), which won the district before losing to Jackson 72-68 in the regional semifinal. Michigan High School All-Class Coach of the Year in 1984. As a Sexton player he was All-City in 1959 and 1960 and All-State in 1960, playing on the 1959 and 1960 Class A state champions, and was student council president. Played at Michigan from 1961 to 1964, lettering three times, and was on the 1964 Big Ten champions and the 1964 Academic All-Big Ten team. Taught for 34 years; later directed Michigan State's basketball camps for seven seasons and is in his 18th season as an assistant video coordinator for the Spartans. Michigan State's bio says he coached 22 years at Sexton; the Hall of Fame gives 1964 to 1984. Greater Lansing Area Sports Hall of Fame, 1988.",
 "source":"https://lansingsportshalloffame.org/people/doug-herner/ ; https://msuspartans.com/sports/mens-basketball/roster/coaches/doug-herner/1303"})]
p=sys.argv[1]; s=open(p).read()
for h in HONORS:
    j=json.dumps(h,separators=(',',':'),ensure_ascii=False)
    if j in s: continue
    assert s.count('"honors":[')==1
    s=s.replace('"honors":[','"honors":['+j+',',1)
for name,also in CARD_ALSO.items():
    key='{"name":"%s",'%name
    i=s.find(key); assert i>=0,name
    end=s.find('}',s.find('"source":',i))
    if '"also"' in s[i:end]: continue
    s=s[:end]+',"also":'+json.dumps(also,separators=(',',':'))+s[end:]
for name,fields in COACH_FIELDS.items():
    key='{"name":"%s","years":'%name
    i=s.find(key); assert i>=0,name
    end=s.find('"source":',i)
    obj=s[i:end]
    new='{"name":"%s","years":%s,"notes":%s,'%(name,json.dumps(fields["years"]),json.dumps(fields["notes"]))
    s=s[:i]+new+s[end:]
    if fields.get("add_source"):
        j=s.find('"source":"',i)+len('"source":"'); k=s.find('"',j)
        if fields["add_source"] not in s[j:k]:
            s=s[:j]+fields["add_source"]+' ; '+s[j:]
for (sid,name),fields in SCHOOL_COACH_FIELDS.items():
    key='{"name":"%s","years":'%name
    sch=s.find('"id":"%s"'%sid); assert sch>=0,sid
    i=s.rfind(key,0,sch); assert i>=0,(sid,name)
    assert s.rfind('"id":"',i,sch)<0,(sid,name)  # entry must sit in this school's block
    end=s.find('"source":',i)
    new='{"name":"%s","years":%s,"notes":%s,'%(name,json.dumps(fields["years"]),json.dumps(fields["notes"]))
    s=s[:i]+new+s[end:]
    if fields.get("add_source"):
        j=s.find('"source":"',i)+len('"source":"'); k=s.find('"',j)
        if fields["add_source"] not in s[j:k]:
            s=s[:j]+fields["add_source"]+' ; '+s[j:]
for sid,before,c in ADD_COACHES:
    if '{"name":"%s","years":'%c["name"] in s: continue
    key='{"name":"%s","years":'%before
    i=s.find(key); assert i>=0,before
    s=s[:i]+json.dumps(c,separators=(',',':'),ensure_ascii=False)+','+s[i:]
open(p,'w').write(s); print('ok',p)
