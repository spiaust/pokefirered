from pathlib import Path
import json,subprocess,sys
r=Path(__file__).resolve().parents[1];b=r/'.local-tools/palace-before-v216';j=lambda p:json.loads(p.read_text())
a=j(b/'data/maps/map_groups.json');z=j(r/'data/maps/map_groups.json');assert z['gMapGroup_Europe']==a['gMapGroup_Europe']+['EuropePalaceVisitor']
a=j(b/'data/layouts/layouts.json')['layouts'];z=j(r/'data/layouts/layouts.json')['layouts'];assert z[:-1]==a
assert (r/'data/layouts/EuropeOranienburg/map.bin').read_bytes()==(b/'data/layouts/EuropeOranienburg/map.bin').read_bytes()
a=j(b/'data/maps/EuropeOranienburg/map.json');z=j(r/'data/maps/EuropeOranienburg/map.json');z['bg_events']=[e for e in z['bg_events'] if e['script']!='EuropePalaceVisitor_Enter'];assert a==z
s=(r/'data/maps/EuropePalaceVisitor/scripts.inc').read_text();assert 'setvar' not in s and 'giveitem' not in s and '48, 9' in s
print('PASS: append-only room IDs, unchanged palace collision/art/existing events and reward-free scripts')
files=['data/maps/map_groups.json','data/layouts/layouts.json','data/event_scripts.s','data/maps/EuropeOranienburg/map.json','data/maps/EuropePalaceVisitor/map.json','data/maps/EuropePalaceVisitor/scripts.inc','data/layouts/EuropePalaceVisitor/map.bin','data/layouts/EuropePalaceVisitor/border.bin'];before={n:(r/n).read_bytes() for n in files}
subprocess.run([sys.executable,str(r/'scripts/build-palace-visitor.py')],check=True);assert all((r/n).read_bytes()==v for n,v in before.items())
m=j(r/'data/maps/EuropePalaceVisitor/map.json');assert sorted((e['x'],e['y']) for e in m['coord_events'])==[(4,8),(5,8)]
print('PASS: deterministic visitor-room generation and both native south exits')
