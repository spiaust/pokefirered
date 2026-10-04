"""New Berlin street blocks preserve the previous district and regenerate safely."""
from pathlib import Path
import json,struct,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
p=R/'data/layouts/EuropeBerlin/map.bin';old=struct.unpack('<1760H',(R/'data/geography/berlin-v062.bin').read_bytes());new=struct.unpack('<2816H',p.read_bytes())
for i,a in enumerate(old):
 x,y=i%40,i//40;b=new[y*64+x]
 if x in (38,39) and y in (37,38,39):assert not b&0xc00;continue
 assert a&0xfc00==b&0xfc00,(x,y,'collision/elevation')
 if not a&0xc00:assert a==b or (x==37 and y in (37,38,39) and b==0x3165),(x,y,'old walkable terrain changed')
assert (64+15)*(44+14)<=0x2800
events=json.loads((R/'data/maps/EuropeBerlin/map.json').read_text())
residents=[o for o in events['object_events'] if o['script'].startswith('EuropeBerlin_Court')]
assert len(residents)==2
assert {(o['x'],o['y']) for o in residents}=={(45,36),(53,36)}
script=(R/'data/maps/EuropeBerlin/scripts.inc').read_text()
for o in residents:
 assert not new[o['y']*64+o['x']]&0xc00
 assert script.count(o['script']+'::')==1
 assert '\tlock\n\tfaceplayer\n\tmsgbox '+o['script']+'Text, MSGBOX_DEFAULT\n\trelease\n\tend' in script
for bx in (42,50,57):
 for y in range(27,32):
  for x in range(bx,bx+5):assert new[y*64+x]&0xc00
print('PASS: old Berlin positions retained; boundary opens with a paved approach; new buildings are solid')
paths=[p,R/'data/maps/EuropeBerlin/map.json',R/'data/maps/EuropeBerlin/scripts.inc',R/'data/layouts/layouts.json',R/'data/layouts/EuropeParis/map.bin']
paths += [R/'data/maps/map_groups.json']+list((R/'data/maps/EuropeBerlinHome').glob('*'))+list((R/'data/layouts/EuropeBerlinHome').glob('*'))
paths += list((R/'data/maps/EuropeBerlinLibrary').glob('*'))+list((R/'data/layouts/EuropeBerlinLibrary').glob('*'))
paths += list((R/'data/maps/EuropeBerlinGardenRoom').glob('*'))+list((R/'data/layouts/EuropeBerlinGardenRoom').glob('*'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-berlin-home.py')],check=True,stdout=subprocess.DEVNULL)
subprocess.run([sys.executable,str(R/'scripts/build-berlin-library.py')],check=True,stdout=subprocess.DEVNULL)
subprocess.run([sys.executable,str(R/'scripts/build-berlin-garden-room.py')],check=True,stdout=subprocess.DEVNULL)
subprocess.run([sys.executable,str(R/'scripts/build-capital-maps.py'),'Berlin'],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==h for p,h in before.items())
assert any(e['script']=='EuropeCase_Reichstag_Enter' for e in json.loads((R/'data/maps/EuropeBerlin/map.json').read_text())['bg_events'])
print('PASS: neighborhood generation is stable, preserves Reichstag entrance and leaves Paris unchanged')
