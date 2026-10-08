"""Only the inactive contact dialogue changes; all quest commands stay exact."""
from pathlib import Path
import re,json
R=Path(__file__).resolve().parents[1]
labels={'europe_story.inc':'EuropeStory_Text_NotStarted','europe_france_story.inc':'EuropeFrance_Text_NotStarted','europe_germany_story.inc':'EuropeGermany_Text_NotStarted'}
for path,old in json.loads((R/'data/geography/quest-contact-v113.json').read_text()).items():
 label=labels[Path(path).name]
 pattern=re.escape(label)+r'::\n(?:[ \t]*\.string[^\n]*\n)+'
 new=(R/path).read_text()
 assert re.sub(pattern,'CONTACT_TEXT\n',old)==re.sub(pattern,'CONTACT_TEXT\n',new),path
 body=re.search(pattern,new).group()
 assert 'west of the' in body
 if 'france' in path:assert 'OXFORD GYM badge' in body
 if 'germany' in path:assert 'OXFORD and' in body and 'CHANTILLY GYM badges' in body
print('PASS: only three inactive contact text blocks change; quest gates, acceptance, battles, rewards and progress commands exact')
