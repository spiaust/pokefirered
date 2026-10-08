"""Exterior Gym guidance changes no progression or indoor statue behavior."""
from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parents[1]
b=json.loads((R/'data/geography/gym-signs-v111.json').read_text())
for path,old in b.items():
 if path=='unchanged':continue
 s=(R/path).read_text()
 if path.endswith('scripts.inc') and 'Gym/' not in path:
  city=path.split('/Europe')[1].split('/')[0]
  label=f'Europe{city}_Text_GymSign::'
  prefix,body=s.split('\n'+label+'\n')
  prefix=prefix.replace(f'msgbox Europe{city}_Text_GymSign, MSGBOX_SIGN',f'msgbox Europe{city}Gym_Text_Statue, MSGBOX_SIGN')
  assert prefix==old,path
  statue=re.search(re.escape(f'Europe{city}Gym_Text_Statue::')+r'\n((?:[ \t]*\.string[^\n]*\n)+)',(R/f'data/maps/Europe{city}Gym/scripts.inc').read_text()).group(1)
  assert body.startswith(statue.replace('$',r'\p'))
  assert all(line.lstrip().startswith('.string') for line in body.splitlines())
 else:assert s==old,path
for path,digest in b['unchanged'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
print('PASS: exterior signs only redirect to added text; old sign text retained; maps, leader gates, rewards, indoor statues and rail exact')
