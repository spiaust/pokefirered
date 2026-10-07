"""Wall notices preserve room grids, staff, services, exits and map IDs."""
from pathlib import Path
import json,hashlib,struct,subprocess,sys
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();old=json.loads((R/'data/geography/station-boards-v103.json').read_text())
assert sha(R/'data/layouts/PalletTown_RivalsHouse/map.bin')==old['layout_sha']
assert struct.unpack('<130H',(R/'data/layouts/PalletTown_RivalsHouse/map.bin').read_bytes())[1*13+9]==0x585
assert json.loads((R/'data/maps/map_groups.json').read_text())==old['groups']
paths=[]
for city,entry in old['cities'].items():
 name=f'Europe{city}Station';label=name+'_LocalBoard';p=R/f'data/maps/{name}/map.json';m=json.loads(p.read_text());events=m['bg_events'];assert len(events)==1 and events[0]==dict(type='sign',x=9,y=1,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=label)
 m['bg_events']=[];assert m==entry['map']
 q=R/f'data/maps/{name}/scripts.inc';s=q.read_text();assert s.split(chr(10)+label+'::')[0]==entry['scripts']
 block=s.split(label+'::')[1];assert all(cmd not in block for cmd in ['setflag','setvar','giveitem','additem'])
 paths.extend([p,q])
print('PASS: all wall notices use existing solid furniture; exact room terrain, staff, services, exits and map IDs retained')
before={p:sha(p) for p in paths};subprocess.run([sys.executable,str(R/'scripts/build-station-boards.py')],check=True,stdout=subprocess.DEVNULL);assert all(sha(p)==v for p,v in before.items())
print('PASS: station notices regenerate identically and reading grants no items or progression')
