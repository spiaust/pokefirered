"""Only readable wall events/text are added to the three branch stations."""
from pathlib import Path
import json,struct,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
old=json.loads((R/'data/geography/branch-station-v109.json').read_text())
assert json.loads((R/'data/maps/map_groups.json').read_text())==old['groups']
grid=(R/'data/layouts/PalletTown_RivalsHouse/map.bin').read_bytes()
assert struct.unpack('<130H',grid)[22]==0x585
paths=[]
for city,entry in old['cities'].items():
    name=f'Europe{city}Station';label=name+'_LocalBoard'
    p=R/f'data/maps/{name}/map.json';m=json.loads(p.read_text())
    assert m['layout']=='LAYOUT_PALLET_TOWN_RIVALS_HOUSE'
    assert m['bg_events']==[dict(type='sign',x=9,y=1,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=label)]
    m['bg_events']=[];assert m==entry['map']
    p2=R/f'data/maps/{name}/scripts.inc';s=p2.read_text()
    assert s.split('\n'+label+'::')[0]==entry['scripts']
    commands=s.split('\n'+label+'::')[1].split(label+'Text::')[0]
    assert [line.strip() for line in commands.strip().splitlines()]==['lockall','msgbox '+label+'Text, MSGBOX_DEFAULT','releaseall','end']
    paths.extend([p,p2])
print('PASS: branch notices reuse existing solid furniture; terrain, staff, services, rail commands, exits and map IDs remain exact')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-station-boards.py')],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==value for p,value in before.items())
print('PASS: branch station notices regenerate identically and only display text')
