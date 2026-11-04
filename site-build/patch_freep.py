import sys, json
# Detroit Free Press all-state teams, 1930s to 2020s, Greater Lansing schools only (Jack, Nov 2, 2026).
# Source: detroitpslbasketball.com's Free Press 1990s page (1993's team was the joint Detroit News team; not included).
# The Free Press picked a Dream Team across all classes, then Class A/B/C/D teams 1-6 plus honorable mention.
# Adds a 'dream' tier and the 'Free Press' selector to the honors code. Skips anything already there.
SRC = "Detroit Free Press all-state, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/freep-all-state-1990s/)"
def h(season, name, school, listed_school, tier, level, listed_tier, note="", listed_as=""):
    d = {"season": season, "name": name, "listed_as": listed_as, "school": school, "listed_school": listed_school, "yr": "",
         "tier": tier, "level": level, "selector": "Free Press", "src": SRC, "listed_tier": listed_tier}
    if note: d["level_note"] = note
    return d
DT = "Dream Team (all classes)"
SRC10 = "Detroit Free Press all-state, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/detroit-free-press-all-state-2010s/)"
HONORS = [
 h("1998-99", "Marcus Taylor", "waverly", "Lansing Waverly", "dream", DT, "Dream Team"),
 h("1998-99", "Kevin Lee", "everett", "Lansing Everett", "fifth", "Class A", "Fifth Team"),
 h("1998-99", "Cortney Scott", "waverly", "Lansing Waverly", "sixth", "Class A", "Sixth Team", listed_as="Courtney Scott"),
 h("1997-98", "Marcus Taylor", "waverly", "Lansing Waverly", "dream", DT, "Dream Team"),
 h("1997-98", "Thomas Jackson", "east-lansing", "East Lansing", "first", "Class A", "First Team"),
 h("1997-98", "Mark Kissling", "okemos", "Okemos", "second", "Class A", "Second Team"),
 h("1996-97", "Marcus Taylor", "waverly", "Lansing Waverly", "second", "Class A", "Second Team"),
 h("1996-97", "Thomas Jackson", "east-lansing", "East Lansing", "third", "Class A", "Third Team"),
 h("1995-96", "Ron Banks", "sexton", "Lansing Sexton", "first", "Class A", "First Team"),
 h("1995-96", "Jason Price", "okemos", "Okemos", "second", "Class A", "Second Team",
   "The 1996 AP list has a John Price of Okemos (honorable mention); probably the same player, not confirmed."),
 h("1994-95", "Ron Banks", "sexton", "Lansing Sexton", "first", "Class A", "First Team"),
 h("1994-95", "Desmond Ferguson", "everett", "East Lansing", "sixth", "Class A", "Sixth Team",
   "The Free Press lists him at East Lansing; he played for Lansing Everett (Jack, Nov 2, 2026)."),
 h("1993-94", "Antwann Jones", "sexton", "Lansing Sexton", "first", "Class A", "First Team (captain)"),
 h("1993-94", "Ron Banks", "sexton", "Lansing Sexton", "third", "Class A", "Third Team"),
 h("1991-92", "Eric Menk", "charlotte", "Charlotte", "fourth", "Class A", "Fourth Team"),
 h("1991-92", "Jason Black", "holt", "Holt", "sixth", "Class A", "Sixth Team"),
 h("1989-90", "Jason Bossard", "charlotte", "Charlotte", "second", "Class A", "Second Team"),
 h("1989-90", "Kareem Washington", "sexton", "Lansing Sexton", "second", "Class A", "Second Team"),
 h("1989-90", "Jeff Wendt", "okemos", "Okemos", "fifth", "Class A", "Fifth Team"),
 h("1989-90", "Corey Henderson", "eastern", "Lansing Eastern", "sixth", "Class A", "Sixth Team"),
]
# 2010s (Jack, Nov 2, 2026). Class levels as the Free Press listed them (2018-19 used divisions). Yr comes from the
# source for 2010 and 2011; for other years it is copied from the same player's BCAM entry that season, when there is one.
def h10(season, name, school, listed_school, tier, level, listed_tier, yr="", note=""):
    d = h(season, name, school, listed_school, tier, level, listed_tier, note); d["src"] = SRC10; d["yr"] = yr; return d
HONORS += [
 h10("2018-19", "Evan Thomas", "okemos", "Okemos", "third", "Division 1", "Third Team", "Sr"),
 h10("2017-18", "Brandon Johns, Jr.", "east-lansing", "East Lansing", "dream", DT, "Dream Team", "Sr"),
 h10("2017-18", "Jordan Henry", "okemos", "Okemos", "hm", "Class A", "Honorable Mention", "Sr"),
 h10("2017-18", "Troy Jordan", "holt", "Holt", "hm", "Class A", "Honorable Mention", "Sr"),
 h10("2017-18", "Luke Hyde", "dewitt", "DeWitt", "hm", "Class A", "Honorable Mention", "Sr"),
 h10("2016-17", "Jaron Faulds", "holt", "Holt", "first", "Class A", "First Team", "Sr"),
 h10("2016-17", "Brandon Johns, Jr.", "east-lansing", "East Lansing", "first", "Class A", "First Team", "Jr"),
 h10("2015-16", "Brandon Allen", "haslett", "Haslett", "first", "Class A", "First Team", "Sr"),
 h10("2015-16", "Brandon Johns, Jr.", "east-lansing", "East Lansing", "first", "Class A", "First Team", "So"),
 h10("2015-16", "Jamyrin Jackson", "everett", "Lansing Everett", "third", "Class A", "Third Team"),
 h10("2015-16", "Jaron Faulds", "holt", "Holt", "fifth", "Class A", "Fifth Team", "Jr"),
 h10("2015-16", "Malek Adams", "grand-ledge", "Grand Ledge", "sixth", "Class A", "Sixth Team", "Sr"),
 h10("2015-16", "Tony Poljan", "lansing-catholic", "Lansing Catholic", "first", "Class B", "First Team", "Sr"),
 h10("2015-16", "Riley Lewis", "williamston", "Williamston", "first", "Class B", "First Team", "Sr"),
 h10("2014-15", "Trevor Manuel", "everett", "Lansing Everett", "dream", DT, "Dream Team", "Sr"),
 h10("2014-15", "Conner George", "okemos", "Okemos", "third", "Class A", "Third Team", "Sr"),
 h10("2014-15", "Brandon Johns, Jr.", "east-lansing", "East Lansing", "hm", "Class A", "Honorable Mention"),
 h10("2011-12", "Denzel Valentine", "sexton", "Lansing Sexton", "dream", DT, "Dream Team", "Sr"),
 h10("2011-12", "Fredrick Edmond", "eastern", "Lansing Sexton", "first", "Class A", "First Team", "Sr",
     "The Free Press lists him at Lansing Sexton; BCAM's 2012 list has him at Lansing Eastern (Class A), and Sexton was Class B."),
 h10("2011-12", "Chris Harrison-Docks", "okemos", "Okemos", "first", "Class A", "First Team", "Sr"),
 h10("2011-12", "Bryn Forbes", "sexton", "Lansing Sexton", "first", "Class B", "First Team", "Sr"),
 h10("2010-11", "LaDontae Henton", "eastern", "Lansing Eastern", "dream", DT, "Dream Team", "Sr"),
 h10("2010-11", "Denzel Valentine", "sexton", "Lansing Sexton", "first", "Class B", "First Team", "Jr"),
 h10("2009-10", "Cole Darling", "holt", "Holt", "first", "Class A", "First Team", "Sr"),
 h10("2009-10", "LaDontae Henton", "eastern", "Lansing Eastern", "first", "Class A", "First Team", "Jr"),
 h10("2009-10", "Jon Horford", "grand-ledge", "Grand Ledge", "first", "Class A", "First Team", "Sr"),
 h10("2009-10", "Alex Gauna", "eaton-rapids", "Eaton Rapids", "first", "Class B", "First Team", "Sr"),
]
# 2000s and 2020s (Jack, Nov 2, 2026). The source is missing 2003 and 2005, and its 2020s lists skip most non-Detroit
# honorable mentions and several division teams. Names follow the site's BCAM spelling; the Free Press spelling is kept
# in listed_as when it differs. Yr is copied from the same player's BCAM entry that season when there is one.
SRC00 = "Detroit Free Press all-state, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/freepall-state2000s/)"
SRC20 = "Detroit Free Press all-state, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/detroit-free-press-all-state-2020s/)"
def hx(src, season, name, school, listed_school, tier, level, listed_tier, yr="", listed_as="", note=""):
    d = h(season, name, school, listed_school, tier, level, listed_tier, note, listed_as); d["src"] = src; d["yr"] = yr; return d
HONORS += [
 hx(SRC00, "2008-09", "Cole Darling", "holt", "Holt", "first", "Class A", "First Team"),
 hx(SRC00, "2008-09", "LaDontae Henton", "eastern", "Lansing Eastern", "fourth", "Class A", "Fourth Team"),
 hx(SRC00, "2008-09", "Travis Bader", "okemos", "Okemos", "sixth", "Class A", "Sixth Team"),
 hx(SRC00, "2007-08", "Charlie Woods", "east-lansing", "East Lansing", "first", "Class A", "First Team"),
 hx(SRC00, "2007-08", "JaVaughn Acree-Manuel", "sexton", "Lansing Sexton", "third", "Class A", "Third Team"),
 hx(SRC00, "2007-08", "LaDontae Henton", "eastern", "Lansing Eastern", "fourth", "Class A", "Fourth Team", listed_as="LaDonte Heaton",
    note="Listed as LaDonte Heaton, Lansing Eastern; taken to be LaDontae Henton (Class of 2011), then a sophomore."),
 hx(SRC00, "2007-08", "Drew Valentine", "sexton", "Lansing Sexton", "sixth", "Class A", "Sixth Team"),
 hx(SRC00, "2006-07", "Paul Crosby", "holt", "Holt", "first", "Class A", "First Team (captain)"),
 hx(SRC00, "2006-07", "Anthony Ianni", "okemos", "Okemos", "fifth", "Class A", "Fifth Team"),
 hx(SRC00, "2006-07", "Jason Hill", "mason", "Mason", "sixth", "Class A", "Sixth Team"),
 hx(SRC00, "2006-07", "Willie Brown", "eastern", "Lansing Eastern", "sixth", "Class A", "Sixth Team"),
 hx(SRC00, "2005-06", "Johnathon Jones", "okemos", "Okemos", "first", "Class A", "First Team"),
 hx(SRC00, "2005-06", "Paul Crosby", "holt", "Holt", "second", "Class A", "Second Team"),
 hx(SRC00, "2005-06", "John Lierman", "holt", "Holt", "fifth", "Class A", "Fifth Team"),
 hx(SRC00, "2005-06", "Lendyn Davis", "sexton", "Lansing Sexton", "fifth", "Class A", "Fifth Team"),
 hx(SRC00, "2005-06", "Gerald Busby", "east-lansing", "East Lansing", "sixth", "Class A", "Sixth Team"),
 hx(SRC00, "2003-04", "Al Horford", "grand-ledge", "Grand Ledge", "dream", DT, "Dream Team"),
 hx(SRC00, "2003-04", "Derick Nelson", "everett", "Lansing Everett", "first", "Class A", "First Team", listed_as="Derrick Nelson"),
 hx(SRC00, "2003-04", "Goran Suton", "everett", "Lansing Everett", "fourth", "Class A", "Fourth Team", listed_as="Goran Sutton"),
 hx(SRC00, "2003-04", "Johnathon Jones", "okemos", "Okemos", "fifth", "Class A", "Fifth Team"),
 hx(SRC00, "2003-04", "Clyde McKinney, Jr.", "everett", "Lansing Everett", "sixth", "Class A", "Sixth Team", listed_as="Clyde McKinney"),
 hx(SRC00, "2001-02", "Alonzo Mans", "everett", "Lansing Everett", "third", "Class A", "Third Team"),
 hx(SRC00, "2001-02", "Al Horford", "grand-ledge", "Grand Ledge", "hm", "Class A", "Honorable Mention"),
 hx(SRC00, "2000-01", "Anton Currie", "okemos", "Okemos", "sixth", "Class A", "Sixth Team"),
 hx(SRC00, "1999-00", "Marcus Taylor", "waverly", "Lansing Waverly", "dream", DT, "Dream Team"),
 hx(SRC00, "1999-00", "Cortney Scott", "waverly", "Lansing Waverly", "fourth", "Class A", "Fourth Team"),
 hx(SRC00, "1999-00", "Doug Lepisto", "okemos", "Okemos", "fifth", "Class A", "Fifth Team"),
 hx(SRC20, "2025-26", "Kelvin (KJ) Torbert, Jr.", "east-lansing", "East Lansing", "dream", DT, "Dream Team (captain)", "Sr", listed_as="K.J. Torbert"),
 hx(SRC20, "2025-26", "Kingston Thomas", "east-lansing", "East Lansing", "third", "Division 1", "Third Team", "Jr"),
 hx(SRC20, "2024-25", "Cameron Hutson", "east-lansing", "East Lansing", "dream", DT, "Dream Team", "Sr", listed_as="Cam Hutson"),
 hx(SRC20, "2023-24", "Cameron Hutson", "east-lansing", "East Lansing", "first", "Division 1", "First Team", "Jr", listed_as="Cam Hutson"),
 hx(SRC20, "2023-24", "Kelvin (KJ) Torbert, Jr.", "east-lansing", "East Lansing", "third", "Division 1", "Third Team", "So", listed_as="KJ Torbert"),
 hx(SRC20, "2022-23", "Bryce Kurncz", "dewitt", "DeWitt", "second", "Division 1", "Second Team", "Sr"),
 hx(SRC20, "2022-23", "Teddy Williams", "grand-ledge", "Grand Ledge", "third", "Division 1", "Third Team", "Sr"),
 hx(SRC20, "2021-22", "Mason Docks", "williamston", "Williamston", "dream", DT, "Dream Team", "Sr"),
 hx(SRC20, "2021-22", "Max Burton", "williamston", "Williamston", "first", "Division 2", "First Team (captain)", "Sr"),
 hx(SRC20, "2019-20", "Andrel Anthony, Jr.", "east-lansing", "East Lansing", "hm", "Division 1", "Honorable Mention", listed_as="Andrel Anthony"),
 hx(SRC20, "2019-20", "Mason Docks", "williamston", "Williamston", "second", "Division 2", "Second Team", "So"),
]
# 1980s (Jack, Nov 2, 2026). Season is the Free Press year minus one (1989 -> 1988-89). No area Coach of the Year.
SRC80 = "Detroit Free Press all-state, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/freep-all-state1980s/)"
AC = "All classes"
HONORS += [
 hx(SRC80, "1988-89", "Kareem Washington", "sexton", "Lansing Sexton", "third", "Class A", "Third Team"),
 hx(SRC80, "1988-89", "Randy Grundstrom", "charlotte", "Charlotte", "fifth", "Class A", "Fifth Team"),
 hx(SRC80, "1987-88", "Charles Pasley", "eastern", "Lansing Eastern", "sixth", "Class A", "Sixth Team"),
 hx(SRC80, "1986-87", "Jim Paul", "east-lansing", "East Lansing", "third", "Class A", "Third Team"),
 hx(SRC80, "1986-87", "Tom Lick", "eastern", "Lansing Eastern", "fourth", "Class A", "Fourth Team"),
 hx(SRC80, "1986-87", "Carl Thomas", "everett", "Lansing Eastern", "fifth", "Class A", "Fifth Team",
    note="The Free Press lists him at Lansing Eastern; Wikipedia and this site have him at Lansing Everett (Class of 1987). Not confirmed."),
 hx(SRC80, "1985-86", "Herb Schoepke", "everett", "Lansing Everett", "third", "Class A", "Third Team"),
 hx(SRC80, "1985-86", "Bill Gibbs", "eastern", "Lansing Eastern", "fifth", "Class A", "Fifth Team"),
 hx(SRC80, "1984-85", "Dennell Dismuke", "eastern", "Lansing Eastern", "second", "Class A", "Second Team"),
 hx(SRC80, "1984-85", "Vernon Norris", "eastern", "Lansing Eastern", "fourth", "Class A", "Fourth Team"),
 hx(SRC80, "1984-85", "Scooter Tropf", "holt", "Holt", "fifth", "Class A", "Fifth Team"),
 hx(SRC80, "1984-85", "John Smoltz", "waverly", "Lansing Waverly", "hm", AC, "Honorable Mention (all classes)"),
 hx(SRC80, "1983-84", "Jeff King", "sexton", "Lansing Sexton", "third", "Class A", "Third Team"),
 hx(SRC80, "1983-84", "James Simmons", "sexton", "Lansing Sexton", "fourth", "Class A", "Fourth Team"),
 hx(SRC80, "1983-84", "Steve Haney", "everett", "Lansing Everett", "fifth", "Class A", "Fifth Team"),
 hx(SRC80, "1982-83", "Kevin Smith", "everett", "Lansing Everett", "second", "Class A", "Second Team"),
 hx(SRC80, "1981-82", "Robert Henderson", "eastern", "Lansing Eastern", "first", "Class A", "First Team"),
 hx(SRC80, "1980-81", "Sam Vincent", "eastern", "Lansing Eastern", "first", "Class A", "First Team"),
 hx(SRC80, "1980-81", "Robert Henderson", "eastern", "Lansing Eastern", "fourth", "Class A", "Fourth Team"),
 hx(SRC80, "1980-81", "Bruce Fields", "everett", "Lansing Everett", "fourth", "Class A", "Fourth Team"),
 hx(SRC80, "1979-80", "Sam Vincent", "eastern", "Lansing Eastern", "first", "Class A", "First Team"),
]

# 1970s (Jack, Nov 2, 2026). Lower teams often give surnames only; those entries keep the surname and say so.
SRC70 = "Detroit Free Press all-state, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/free-press-all-state-1970s/)"
SN = "The Free Press list gives only the surname."
MJ = 'Earvin (Magic) Johnson'
HONORS += [
 hx(SRC70, "1978-79", "Travis Stanley", "eastern", "Lansing Eastern", "second", "Class A", "Second Team"),
 hx(SRC70, "1978-79", "Todd Shumway", "grand-ledge", "Grand Ledge", "sixth", "Class A", "Sixth Team", listed_as="Shumway",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC70, "1977-78", "Tony Daniels", "everett", "Lansing Everett", "third", "Class A", "Third Team"),
 hx(SRC70, "1976-77", MJ, "everett", "Lansing Everett", "first", "Class A", "First Team"),
 hx(SRC70, "1976-77", "Jay Vincent", "eastern", "Lansing Eastern", "first", "Class A", "First Team"),
 hx(SRC70, "1975-76", MJ, "everett", "Lansing Everett", "first", "Class A", "First Team"),
 hx(SRC70, "1975-76", "Jay Vincent", "eastern", "Lansing Eastern", "second", "Class A", "Second Team"),
 hx(SRC70, "1974-75", "Greg Lloyd", "eastern", "Lansing Eastern", "first", "Class A", "First Team"),
 hx(SRC70, "1974-75", MJ, "everett", "Lansing Everett", "second", "Class A", "Second Team"),
 hx(SRC70, "1974-75", "Gary Fox", "waverly", "Lansing Waverly", "sixth", "Class A", "Sixth Team", listed_as="Fox",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC70, "1974-75", "Jay Vincent", "eastern", "Lansing Eastern", "hm", AC, "Honorable Mention (all classes)"),
 hx(SRC70, "1973-74", "Greg Lloyd", "eastern", "Lansing Eastern", "third", "Class A", "Third Team"),
 hx(SRC70, "1972-73", "Ben Poquette", "east-lansing", "East Lansing", "second", "Class A", "Second Team"),
 hx(SRC70, "1972-73", "Kevin Humphrey", "sexton", "Lansing Sexton", "fourth", "Class A", "Fourth Team", listed_as="Humphrey",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC70, "1971-72", "Ed Allen", "sexton", "Lansing Sexton", "third", "Class A", "Third Team"),
 hx(SRC70, "1970-71", "Rodney Benson", "sexton", "Lansing Sexton", "first", "Class A", "First Team"),
 hx(SRC70, "1970-71", "Tim May", "eastern", "Lansing Eastern", "second", "Class A", "Second Team"),
 hx(SRC70, "1970-71", "Dean Eisler", "st-johns", "St. Johns", "fifth", "Class A", "Fifth Team", listed_as="Eisler",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC70, "1969-70", "Julian Hood", "sexton", "Lansing Sexton", "fifth", "Class A", "Fifth Team", listed_as="Hood",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
]

# 1960s (Jack, Nov 2, 2026). "Eastern" on these lists without "Lansing" is Detroit Eastern and is left out.
# 1968 had no Detroit paper teams (newspaper strike); that year's AP and UPI Class A teams come from the Battle Creek
# Enquirer (March 28-29, 1968), as given on the same page, and are filed under those selectors.
SRC60 = "Detroit Free Press all-state, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/freep-all-state-1960s/)"
SRC68 = "Battle Creek Enquirer, March 28-29, 1968, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/freep-all-state-1960s/)"
def h68(sel, *a, **k):
    d = hx(SRC68, *a, **k); d["selector"] = sel; return d
HONORS += [
 hx(SRC60, "1968-69", "Brian Breslin", "east-lansing", "East Lansing", "first", "Class A", "First Team"),
 hx(SRC60, "1968-69", "Blake Ashdown", "east-lansing", "East Lansing", "third", "Class A", "Third Team"),
 hx(SRC60, "1968-69", "T.C. Blair", "east-lansing", "East Lansing", "fifth", "Class A", "Fifth Team", listed_as="Blair",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 h68("UPI", "1967-68", "T.C. Blair", "east-lansing", "East Lansing", "first", "Class A", "First Team"),
 h68("UPI", "1967-68", "Blake Ashdown", "east-lansing", "East Lansing", "third", "Class A", "Third Team"),
 h68("UPI", "1967-68", "Bernard Moore", "sexton", "Lansing Sexton", "hm", "Class A", "Honorable Mention"),
 h68("AP", "1967-68", "T.C. Blair", "east-lansing", "East Lansing", "hm", "Class A", "Honorable Mention"),
 hx(SRC60, "1966-67", "Tom Curtis", "everett", "Lansing Everett", "sixth", "Class A", "Sixth Team", listed_as="Curtis",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC60, "1965-66", "Chris Janson", "east-lansing", "East Lansing", "fourth", "Class A", "Fourth Team", listed_as="Jansen",
    note="The Free Press list gives only the surname, spelled Jansen; name and spelling from Jack (Nov 2, 2026)."),
 hx(SRC60, "1964-65", "John Holms", "sexton", "Lansing Sexton", "third", "Class A", "Third Team"),
 hx(SRC60, "1963-64", "Cliff Foster", "sexton", "Lansing Sexton", "second", "Class A", "Second Team"),
 hx(SRC60, "1963-64", "John Holms", "sexton", "Lansing Sexton", "third", "Class A", "Third Team"),
 hx(SRC60, "1963-64", "Jim Harris", "east-lansing", "East Lansing", "sixth", "Class A", "Sixth Team", listed_as="Harris",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC60, "1962-63", "Jim Hornberger", "east-lansing", "East Lansing", "second", "Class A", "Second Team"),
 hx(SRC60, "1962-63", "Homer Scarborough", "sexton", "Lansing Sexton", "third", "Class A", "Third Team"),
 hx(SRC60, "1961-62", "John Truitt", "east-lansing", "East Lansing", "first", "Class A", "First Team"),
 hx(SRC60, "1961-62", "Jim Hornberger", "east-lansing", "East Lansing", "fourth", "Class A", "Fourth Team", listed_as="Hornberger"),
 hx(SRC60, "1960-61", "Brian Ferguson", "sexton", "Lansing Sexton", "second", "Class A", "Second Team"),
 hx(SRC60, "1960-61", "Bob Davis", "sexton", "Lansing Sexton", "fourth", "Class A", "Fourth Team", listed_as="Davis",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC60, "1960-61", "Sandy Johnson", "everett", "Lansing Everett", "fifth", "Class A", "Fifth Team", listed_as="Johnson",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC60, "1960-61", "Mike Henderson", "east-lansing", "East Lansing", "sixth", "Class A", "Sixth Team", listed_as="Henderson",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC60, "1959-60", "Doug Herner", "sexton", "Lansing Sexton", "first", "Class A", "First Team"),
 hx(SRC60, "1959-60", "Doug Miller", "east-lansing", "East Lansing", "first", "Class A", "First Team"),
 hx(SRC60, "1959-60", "Brian Ferguson", "sexton", "Lansing Sexton", "fifth", "Class A", "Fifth Team", listed_as="Ferguson",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
]

# 1950s (Jack, Nov 2, 2026). Plain "Eastern" on these lists is Detroit Eastern and is left out; Lansing Eastern is named in full.
SRC50 = "Detroit Free Press all-state, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/freep-all-state-1950s/)"
HONORS += [
 hx(SRC50, "1958-59", "Ron Robbe", "eastern", "Lansing Eastern", "third", "Class A", "Third Team"),
 hx(SRC50, "1957-58", "Denny Groat", "sexton", "Lansing Sexton", "third", "Class A", "Third Team"),
 hx(SRC50, "1956-57", "Mike Penner", "eastern", "Lansing Eastern", "fourth", "Class A", "Fourth Team", listed_as="Penner",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC50, "1956-57", "Roy Ferguson", "sexton", "Lansing Sexton", "fifth", "Class A", "Fifth Team", listed_as="Ferguson",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC50, "1955-56", "Dick Ramont", "sexton", "Lansing Sexton", "second", "Class A", "Second Team"),
 hx(SRC50, "1955-56", "Pat Wightman", "eastern", "Lansing Eastern", "sixth", "Class A", "Sixth Team", listed_as="Wightman",
    note="The Free Press list gives only the surname; first name from Jack (Nov 2, 2026)."),
 hx(SRC50, "1954-55", "Art Gowens", "sexton", "Lansing Sexton", "first", "Class A", "First Team"),
 hx(SRC50, "1953-54", "Art Gowens", "sexton", "Lansing Sexton", "first", "Class A", "First Team"),
 hx(SRC50, "1952-53", "Tom Klewicki", "sexton", "Lansing Sexton", "first", "Class A", "First Team"),
 hx(SRC50, "1952-53", "Don Ellis", "sexton", "Lansing Sexton", "second", "Class A", "Second Team"),
 hx(SRC50, "1950-51", "Jim Raymond", "sexton", "Lansing Sexton", "first", "Class A", "First Team"),
]

# 1940s (Jack, Nov 2, 2026). The source is missing 1943 and 1944 and lists only one Class A team in 1940 and 1941; the
# 1942-49 teams give no class, so level is left blank. Plain "Eastern" is Detroit Eastern. Lansing Central (closed 1943)
# is filed under Sexton and Lansing St. Mary under Lansing Catholic, as the predecessor schools, with a note.
SRC40 = "Detroit Free Press all-state, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/freep-all-state-1940s/)"
HONORS += [
 hx(SRC40, "1946-47", "Bob Nagel", "eastern", "Lansing Eastern", "first", "", "First Team"),
 hx(SRC40, "1945-46", "Bob Grant", "sexton", "Lansing Sexton", "first", "", "First Team"),
 hx(SRC40, "1944-45", "Bob Swanson", "sexton", "Lansing Sexton", "first", "", "First Team", listed_as="Robert Swanson"),
 hx(SRC40, "1944-45", "Tom Petroff", "eastern", "Lansing Eastern", "second", "", "Second Team"),
 hx(SRC40, "1941-42", "Bob Carpenter", "sexton", "Lansing Central", "second", "", "Second Team",
    note="Listed at Lansing Central, which Sexton replaced in 1943; filed under Sexton as its predecessor."),
 hx(SRC40, "1941-42", "Tom King", "east-lansing", "East Lansing", "third", "", "Third Team", listed_as="Tommy King"),
 hx(SRC40, "1941-42", "Charles Marks", "eastern", "Lansing Eastern", "third", "", "Third Team"),
 hx(SRC40, "1940-41", "Tom King", "east-lansing", "East Lansing", "third", "Class A", "Third Team"),
 hx(SRC40, "1940-41", "Ray Crissey", "lansing-catholic", "Lansing St. Mary", "third", "Class A", "Third Team (captain)",
    note="Listed at Lansing St. Mary, a predecessor of Lansing Catholic; filed under Lansing Catholic."),
]

# 1930s (Jack, Nov 2, 2026; text pasted from detroitpslbasketball.com). Lansing Central and Lansing St. Mary filed under
# their successor schools (Sexton, Lansing Catholic) with a note, as in the 1940s. Only 1939 names a class.
SRC30 = "Detroit Free Press all-state, via detroitpslbasketball.com (https://www.detroitpslbasketball.com/all-time-psl-all-state-selections/freepall-state/freep-all-state-1930s/)"
LC = "Listed at Lansing Central, which Sexton replaced in 1943; filed under Sexton as its predecessor."
SM = "Listed at Lansing St. Mary, a predecessor of Lansing Catholic; filed under Lansing Catholic."
HONORS += [
 hx(SRC30, "1938-39", "Russ Collins", "sexton", "Lansing Central", "second", "Class A", "Second Team", note=LC),
 hx(SRC30, "1936-37", "Eugene Brogan", "lansing-catholic", "Lansing St. Mary", "first", "", "First Team", note=SM),
 hx(SRC30, "1935-36", "Herbert Brogan", "lansing-catholic", "Lansing St. Mary", "second", "", "Second Team", note=SM),
 hx(SRC30, "1935-36", "Robert Sherman", "eastern", "Lansing Eastern", "third", "", "Third Team"),
 hx(SRC30, "1934-35", "Bill Carpenter", "sexton", "Lansing Central", "first", "", "First Team (captain)",
    note="Captain of Lansing Central's 1935 Class A state champions. " + LC),
 hx(SRC30, "1934-35", "Edwin Abraham", "sexton", "Lansing Central", "second", "", "Second Team",
    note="Lansing Central won the 1935 Class A title. " + LC),
]

# Notable player cards added with these honors (Jack, Nov 2, 2026). Inserted at the start of the school's list;
# the page sorts players by class. Grad year inferred from his all-state seasons and his 1942-43 start at MSU.
ADD_PLAYERS = [("east-lansing", {"name": "Tom King", "grad_year": "1942",
  "accolades": "Free Press third-team all-state in 1941 (Class A) and 1942. Played basketball and baseball at Michigan State (1942-43) and Michigan (1943-44), and served in the Marine Corps in World War II and the Korean War. A guard for the Detroit Falcons in the BAA's first season, 1946-47 (5.1 points a game in 58 games), he also negotiated jobs as the team's publicity director, business manager and traveling secretary, which made his $16,500 salary the league's highest. Later a Chicago businessman with Wirtz Enterprises and the Merchandise Mart, and a jazz drummer. Married Olympic figure skating champion Barbara Ann Scott. Died Nov. 12, 2015, at 91.",
  "college": "Michigan State (1942-43); Michigan (1943-44)",
  "pro": "Detroit Falcons (BAA, 1946-47)",
  "source": "https://en.wikipedia.org/wiki/Tom_King_(basketball) ; https://peachbasketsociety.blogspot.com/2016/10/tom-king.html ; " + SRC40.split("(")[1].rstrip(")"),
  "approx": True})]

# Free Press Coach of the Year (Jack, Nov 2, 2026): sentence added to each coach's notes plus the source page.
# Runs after patch_confirmed (step 8), which rewrites some of these notes.
COY = [
 ("waverly", "Phil Odlum", "State Class A & B Coach of the Year in 2000;",
  "State Class A & B Coach of the Year and Detroit Free Press Coach of the Year in 2000;", SRC00.split("(")[1].rstrip(")")),
 ("everett", "Johnny Jones", "Won the 2004 boys Class A title.",
  "Won the 2004 boys Class A title and was the Detroit Free Press Coach of the Year that season.", SRC00.split("(")[1].rstrip(")")),
 ("east-lansing", "Ray Mitchell", "state quarterfinals in 2021, 2023 and 2024.",
  "state quarterfinals in 2021, 2023 and 2024. Detroit Free Press Coach of the Year in 2025.", SRC20.split("(")[1].rstrip(")")),
 ("sexton", "Clayton Kowalk", "Michigan Coaches Association Basketball Coach of the Year in 1954.",
  "Michigan Coaches Association Basketball Coach of the Year in 1954 and Detroit Free Press Coach of the Year in 1964.", SRC60.split("(")[1].rstrip(")")),
 ("sexton", "Doug Herner", "All-State in 1960,", "Detroit Free Press first-team All-State in 1960,", SRC60.split("(")[1].rstrip(")")),
 ("williamston", "Tom Lewis", "Led the unbeaten 2022 Division 2 champions in his sixth season.",
  "Led the unbeaten 2022 Division 2 champions in his sixth season. Detroit Free Press Coach of the Year in 2022.", SRC20.split("(")[1].rstrip(")")),
]
p = sys.argv[1]; s = open(p).read()
def rep(a, b):
    global s
    if b in s: return
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b, 1)
# code: Dream Team tier ranked above first team; Free Press in the player chips and the Team filter
rep("HON_TIER={first:{", "HON_TIER={dream:{label:'Free Press Dream Team',short:'Dream Team',rank:-1},first:{")
if "return ['BCAM','AP','Free Press','UPI'].flatMap(sel=>" not in s:
    rep("return ['BCAM','AP'].flatMap(sel=>", "return ['BCAM','AP','Free Press'].flatMap(sel=>")
    rep("return ['BCAM','AP','Free Press'].flatMap(sel=>", "return ['BCAM','AP','Free Press','UPI'].flatMap(sel=>")
rep("${HON_TIER[t].short}${x.length>1?' ×'+x.length:''}</span>`})).join('')}".replace("${HON_TIER","${HON_TIER"),
    "${HON_TIER[t].short}${x.length>1?' ×'+x.length:''}</span>`})).join('')}")  # no-op anchor check
if '<option value="UPI">UPI</option>' not in s:
    rep('<option value="BCAM">BCAM</option><option value="AP">AP</option></select>', '<option value="BCAM">BCAM</option><option value="AP">AP</option><option value="Free Press">Free Press</option></select>')
    rep('<option value="Free Press">Free Press</option></select>', '<option value="Free Press">Free Press</option><option value="UPI">UPI</option></select>')
rep("<span class=\"chip${t==='first'?' gold':''}\" title=\"${esc(sel)} ${esc(HON_TIER[t].short)}",
    "<span class=\"chip${t==='first'||t==='dream'?' gold':''}\" title=\"${esc(sel)} ${esc(HON_TIER[t].short)}")
rep("function honorChip(h){return `<span class=\"chip${h.tier==='first'?' gold'", "function honorChip(h){return `<span class=\"chip${h.tier==='first'||h.tier==='dream'?' gold'")
rep('<select id="htier"><option value="all">All</option><option value="first">1st Team</option>',
    '<select id="htier"><option value="all">All</option><option value="dream">Dream Team</option><option value="first">1st Team</option>')
rep('<option value="lower">3rd-5th Team</option>', '<option value="lower">3rd-6th Team</option>')
# name fixes (Jack, Nov 2, 2026): correct spelling in every honors entry; the old spelling stays searchable in listed_as
s = s.replace('"name":"Atwon Currie","listed_as":""', '"name":"Anton Currie","listed_as":"Atwon Currie"')
s = s.replace('"name":"Antwon Currie","listed_as":"Atwon Currie"', '"name":"Anton Currie","listed_as":"Atwon Currie"')
s = s.replace(json.dumps(hx(SRC00, "2000-01", "Antwon Currie", "okemos", "Okemos", "sixth", "Class A", "Sixth Team", listed_as="Anton Currie"), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace('"name":"Andre Taylor Jr.","listed_as":"Andre Taylor Jr"', '"name":"Andre (AJ) Taylor, Jr.","listed_as":"Andre Taylor Jr."')
s = s.replace('"name":"Andrel Anthony","listed_as":""', '"name":"Andrel Anthony, Jr.","listed_as":"Andrel Anthony"')
s = s.replace('"name":"Derrick Nelson","listed_as":""', '"name":"Derick Nelson","listed_as":"Derrick Nelson"')
old_shum = json.dumps(hx(SRC70, "1978-79", "Shumway", "grand-ledge", "Grand Ledge", "sixth", "Class A", "Sixth Team", note=SN), separators=(',', ':'), ensure_ascii=False)
s = s.replace(old_shum + ',', '')
old_fox = json.dumps(hx(SRC70, "1974-75", "Fox", "waverly", "Lansing Waverly", "sixth", "Class A", "Sixth Team", note=SN), separators=(',', ':'), ensure_ascii=False)
s = s.replace(old_fox + ',', '')
old_hum = json.dumps(hx(SRC70, "1972-73", "Humphrey", "sexton", "Lansing Sexton", "fourth", "Class A", "Fourth Team", note=SN), separators=(',', ':'), ensure_ascii=False)
s = s.replace(old_hum + ',', '')
s = s.replace(json.dumps(hx(SRC70, "1970-71", "Eisler", "st-johns", "St. Johns", "fifth", "Class A", "Fifth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC70, "1969-70", "Hood", "sexton", "Lansing Sexton", "fifth", "Class A", "Fifth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC60, "1968-69", "Blair", "east-lansing", "East Lansing", "fifth", "Class A", "Fifth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC60, "1963-64", "Harris", "east-lansing", "East Lansing", "sixth", "Class A", "Sixth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC60, "1966-67", "Curtis", "everett", "Lansing Everett", "sixth", "Class A", "Sixth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC60, "1965-66", "Jansen", "east-lansing", "East Lansing", "fourth", "Class A", "Fourth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC60, "1960-61", "Davis", "sexton", "Lansing Sexton", "fourth", "Class A", "Fourth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC60, "1960-61", "Johnson", "everett", "Lansing Everett", "fifth", "Class A", "Fifth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC60, "1960-61", "Henderson", "east-lansing", "East Lansing", "sixth", "Class A", "Sixth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC60, "1959-60", "Ferguson", "sexton", "Lansing Sexton", "fifth", "Class A", "Fifth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC50, "1956-57", "Penner", "eastern", "Lansing Eastern", "fourth", "Class A", "Fourth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC50, "1956-57", "Ferguson", "sexton", "Lansing Sexton", "fifth", "Class A", "Fifth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
s = s.replace(json.dumps(hx(SRC50, "1955-56", "Wightman", "eastern", "Lansing Eastern", "sixth", "Class A", "Sixth Team", note=SN), separators=(',', ':'), ensure_ascii=False) + ',', '')
old_currie = json.dumps(hx(SRC00, "2000-01", "Atwon Currie", "okemos", "Okemos", "sixth", "Class A", "Sixth Team", listed_as="Anton Currie"), separators=(',', ':'), ensure_ascii=False)
s = s.replace(old_currie + ',', '')
# data
old_scott = json.dumps(h("1998-99", "Courtney Scott", "waverly", "Lansing Waverly", "sixth", "Class A", "Sixth Team"), separators=(',', ':'), ensure_ascii=False)
s = s.replace(old_scott + ',', '')
old_ferg = json.dumps(h("1994-95", "Desmond Ferguson", "east-lansing", "East Lansing", "sixth", "Class A", "Sixth Team"), separators=(',', ':'), ensure_ascii=False)
s = s.replace(old_ferg + ',', '')
added = 0
for x in HONORS:
    j = json.dumps(x, separators=(',', ':'), ensure_ascii=False)
    if j in s: continue
    assert s.count('"honors":[') == 1
    s = s.replace('"honors":[', '"honors":[' + j + ',', 1); added += 1
for sid, coach, old, new, url in COY:
    key = '{"name":"%s","years":' % coach
    sch = s.find('"id":"%s"' % sid); assert sch >= 0, sid
    i = s.rfind(key, 0, sch); assert i >= 0 and s.rfind('"id":"', i, sch) < 0, (sid, coach)
    end = s.find('}', s.find('"source":"', i))
    obj = s[i:end]
    if new not in obj:
        assert obj.count(old) == 1, (coach, old)
        obj = obj.replace(old, new)
    j = obj.find('"source":"') + len('"source":"')
    if url not in obj:
        obj = obj[:j] + url + (' ; ' if obj[j] != '"' else '') + obj[j:]
    s = s[:i] + obj + s[end:]
for sid, pl in ADD_PLAYERS:
    if '{"name":"%s","grad_year":' % pl["name"] in s: continue
    sch = s.find('"id":"%s"' % sid); assert sch >= 0, sid
    key = '"notable_players":['
    i = s.rfind(key, 0, sch); assert i >= 0 and s.rfind('"id":"', i, sch) < 0, sid
    j = i + len(key)
    s = s[:j] + json.dumps(pl, separators=(',', ':'), ensure_ascii=False) + (',' if s[j] != ']' else '') + s[j:]
open(p, 'w').write(s); print('ok', p, 'added', added)
