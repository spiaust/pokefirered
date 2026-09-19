"""Separate the station post from the refuge while retaining v0.54 save positions."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1];W,H=56,32
old=struct.unpack('<1792H',(R/'data/geography/chantilly-post-v054.bin').read_bytes());a=[list(old[y*W:(y+1)*W]) for y in range(H)]
former=json.loads((R/'data/geography/chantilly-landmark-blocks.json').read_text());removed={t for v in former.values() for row in v for t in row}
# Estate buildings and inaccessible moat become an open station forecourt.
for y in range(H):
 for x in range(W):
  if a[y][x]&1023 in removed or (x>=16 and a[y][x]>>12==1):a[y][x]=0x3165
blocks=json.loads((R/'data/geography/chantillypost-landmark-blocks.json').read_text())
for dy,row in enumerate(blocks['station']):
 for dx,t in enumerate(row):a[6+dy][33+dx]=0x400|t
# Walkable level crossings preserve old on-foot coordinates. Trains use the notice.
for y in range(3,5):
 for x in range(18,54):a[y][x]=0x3000|blocks['track'][(y-3)%2][(x-18)%2]
signs=[('Station',37,10,['CHANTILLY STATION - 1940','The notice handles onward travel.']),('Platform',25,19,['STATION FORECOURT','The dispatcher waits to the west.']),('Return',34,26,['STATION APPROACH','Return west for the refuge guide.'])]
a[14][37]=0x3165
for _,x,y,_ in signs:a[y][x]=0x402
dest=R/'data/layouts/EuropeChantillyPastPost';dest.mkdir(exist_ok=True)
from europe_trees import finish_trees
finish_trees(a)
(dest/'map.bin').write_bytes(struct.pack('<1792H',*(v for row in a for v in row)))
(dest/'border.bin').write_bytes((R/'data/layouts/EuropeChantillyPast/border.bin').read_bytes())
p=R/'data/layouts/layouts.json';j=json.loads(p.read_text());id='LAYOUT_EUROPE_CHANTILLY_PAST_POST'
l=dict(id=id,name='EuropeChantillyPastPost_Layout',width=W,height=H,border_width=2,border_height=2,primary_tileset='gTileset_General',secondary_tileset='gTileset_EuropeChantillyPost',border_filepath='data/layouts/EuropeChantillyPastPost/border.bin',blockdata_filepath='data/layouts/EuropeChantillyPastPost/map.bin')
i=next((i for i,v in enumerate(j['layouts']) if v.get('id')==id),None)
if i is None:j['layouts'].append(l)
else:j['layouts'][i]=l
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeChantillyPastPost/map.json';j=json.loads(p.read_text());j['layout']=id;j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith('EuropeChantillyPastPost_Realism')]
for suffix,x,y,lines in signs:j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeChantillyPastPost_Realism'+suffix))
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeChantillyPastPost/scripts.inc';s=p.read_text().split('\nEuropeChantillyPastPost_Realism')[0]
for suffix,x,y,lines in signs:
 label='EuropeChantillyPastPost_Realism'+suffix;s+=f'\n{label}::\n\tmsgbox {label}Text, MSGBOX_SIGN\n\tend\n\n{label}Text::\n'
 for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\n')+'"\n'
p.write_text(s);print('Independent historical station layout generated')
