"""Add local walking notices to existing framed station wall furniture."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
for city,notes in json.loads((R/'data/geography/station-boards.json').read_text()).items():
 name=f'Europe{city}Station';label=name+'_LocalBoard';p=R/f'data/maps/{name}/map.json';m=json.loads(p.read_text())
 m['bg_events']=[e for e in m['bg_events'] if e['script']!=label]
 m['bg_events'].append(dict(type='sign',x=9,y=1,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=label));p.write_text(json.dumps(m,indent=2)+chr(10))
 p=R/f'data/maps/{name}/scripts.inc';s=p.read_text().split(chr(10)+label+'::')[0]
 s+=chr(10)+label+'::'+chr(10)+' lockall'+chr(10)+' msgbox '+label+'Text, MSGBOX_DEFAULT'+chr(10)+' releaseall'+chr(10)+' end'+chr(10)+chr(10)+label+'Text::'+chr(10)
 for i,line in enumerate(notes):s+=' .string "'+line+('$' if i==3 else chr(92)+('p' if i%2 else 'n'))+'"'+chr(10)
 p.write_text(s)
print('Station walking notices generated on existing framed wall furniture')
