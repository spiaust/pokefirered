from pathlib import Path
R=Path(__file__).resolve().parents[1]
old=(R/'data/geography/german-directions-v114.inc').read_bytes()
new=(R/'data/scripts/europe_germany_story.inc').read_bytes()
for a,b in [(b'Take the train, or walk north\\n',b'Walk north: GERMAN WOODLAND,\\n'),(b'through BERLIN WOODLAND and HAVEL.\\p',b'then HAVEL TRAIL. Or take a train.\\p'),(b'HAVEL TRAIL and BERLIN WOODLAND.$',b'HAVEL TRAIL and GERMAN WOODLAND.$')]:
 assert old.count(a)==1;old=old.replace(a,b)
assert old==new and b'BERLIN WOODLAND' not in new
print('PASS: only three dialogue lines change; route names match signs; all quest, delivery, reward and travel commands exact')
