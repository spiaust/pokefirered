"""Append the Council Hall without renumbering existing maps or layouts."""
from pathlib import Path
import json,struct
r=Path(__file__).resolve().parents[1]
def write(p,j):
 nl='\r\n' if p.exists() and b'\r\n' in p.read_bytes() else '\n';b=(json.dumps(j,indent=2)+'\n').replace('\n',nl).encode()
 if not p.exists() or p.read_bytes()!=b:p.write_bytes(b)
def binary(p,b):
 if not p.exists() or p.read_bytes()!=b:p.write_bytes(b)
name='EuropeCouncilHall';d=r/'data/maps'/name;d.mkdir(exist_ok=True)
m=json.loads((r/'data/maps/EuropeLondonReadingRoom/map.json').read_text());m.update(id='MAP_EUROPE_COUNCIL_HALL',name=name,layout='LAYOUT_EUROPE_COUNCIL_HALL',music='MUS_GYM',battle_scene='MAP_BATTLE_SCENE_GYM')
template=m['object_events'][0];m['object_events']=[]
for label,gfx,x,y in [('Alfred','GENTLEMAN',2,3),('Solene','WOMAN_1',4,3),('Otmar','SCIENTIST',6,3),('Elara','WOMAN_2',8,3),('Rowan','COOLTRAINER_M',10,3),('Nurse','NURSE',2,6),('Steward','GYM_GUY',10,6),('Coach','COOLTRAINER_M',6,6),('Shop','MAN',4,6)]:
 o=dict(template);o.update(graphics_id='OBJ_EVENT_GFX_'+gfx,x=x,y=y,script='EuropeCouncil_'+label);m['object_events'].append(o)
m['coord_events']=[dict(type='trigger',x=x,y=8,elevation=3,var='VAR_TEMP_0',var_value='0',script='EuropeCouncil_Exit') for x in (4,5)];m['bg_events']=[];m['warp_events']=[];write(d/'map.json',m)
p=r/'data/layouts/layouts.json';j=json.loads(p.read_text());l=next(dict(x) for x in j['layouts'] if x.get('id')=='LAYOUT_EUROPE_LONDON_READING_ROOM');l.update(id='LAYOUT_EUROPE_COUNCIL_HALL',name=name+'_Layout',border_filepath='data/layouts/'+name+'/border.bin',blockdata_filepath='data/layouts/'+name+'/map.bin')
d=r/'data/layouts'/name;d.mkdir(exist_ok=True);a=list(struct.unpack('<130H',(r/'data/layouts/EuropeLondonReadingRoom/map.bin').read_bytes()))
for y in range(2,8):
 for x in range(1,12):a[y*13+x]=0x3001
# Walls and south doorway remain native; the battle floor is unobstructed.
binary(d/'map.bin',struct.pack('<130H',*a));binary(d/'border.bin',(r/'data/layouts/EuropeLondonReadingRoom/border.bin').read_bytes())
if not any(x.get('id')==l['id'] for x in j['layouts']):j['layouts'].append(l)
write(p,j);p=r/'data/maps/map_groups.json';j=json.loads(p.read_text())
if name not in j['gMapGroup_Europe']:j['gMapGroup_Europe'].append(name)
write(p,j)
