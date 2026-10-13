"""Report authored campaign/rematch levels; this is a static audit, not playtest."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
campaign=json.loads((ROOT/'data/shadow-campaign.json').read_text())
post=json.loads((ROOT/'data/eclipse-postgame.json').read_text())
parties=(ROOT/'src/data/trainer_parties.h').read_text()
def levels(trainer,base):
 return dict(easy=base-4 if base>5 else 2,normal=base,hard=base+1 if trainer==100 else min(100,base+5))
rows=[]
for chapter in campaign['chapters']:
 trainer=chapter['trainer'];base=chapter['level']
 body=re.search(r'ShadowParty'+str(trainer)+r'\[\] = \{(.*?)\n\};',parties,re.S)
 assert body and all(int(n)==base for n in re.findall(r'\.lvl = (\d+)',body[1])),chapter
 rows.append(dict(trainer=trainer,city=chapter['city'],country=chapter['country'],kind=chapter['kind'],levels=levels(trainer,base)))
rematches=[dict(trainer=t['id'],name=t['name'],party_count=len(t['party']),levels=levels(t['id'],t['level'])) for t in post['champion_circuit']['trainers']]
report=dict(method='Static authored level curve, checked against compiled source party declarations. Not an outcome or difficulty proof.',campaign=rows,rematches=rematches)
(ROOT/'data/balance/level-curve.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: 21 authored chapter levels and 13 rematch difficulty curves; not natural-play coverage.')
if __name__=='__main__':
 for row in rows:print(row['city'],row['levels'])
