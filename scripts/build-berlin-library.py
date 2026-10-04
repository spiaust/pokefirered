"""Add a fictional neighborhood reading room, retaining earlier map IDs."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
name='EuropeBerlinLibrary';lid='LAYOUT_EUROPE_BERLIN_LIBRARY'
p=R/'data/layouts/layouts.json';ls=json.loads(p.read_text())
source=next(l for l in ls['layouts'] if l.get('id')=='LAYOUT_EUROPE_BERLIN_HOME')
l=dict(source,id=lid,name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
d=R/f'data/layouts/{name}';d.mkdir(exist_ok=True)
a=list(struct.unpack('<130H',(R/source['blockdata_filepath']).read_bytes()))
# A compact reading table replaces the sitting-room rug and chairs.
for y in range(3,7):
 for x in range(4,10):a[y*13+x]=0x3001
for y,row in enumerate([(0x44c,0x44d),(0x454,0x455)]):
 for x,t in enumerate(row):a[(4+y)*13+6+x]=t
(d/'map.bin').write_bytes(struct.pack('<130H',*a))
(d/'border.bin').write_bytes((R/source['border_filepath']).read_bytes())
i=next((i for i,v in enumerate(ls['layouts']) if v.get('id')==lid),None)
if i is None:ls['layouts'].append(l)
else:ls['layouts'][i]=l
p.write_text(json.dumps(ls,indent=2)+'\n')
p=R/'data/maps/map_groups.json';groups=json.loads(p.read_text())
if name not in groups['gMapGroup_Europe']:groups['gMapGroup_Europe'].append(name)
p.write_text(json.dumps(groups,indent=2)+'\n')
def obj(gfx,x,y,label):
 return dict(type='object',graphics_id=gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script=name+'_'+label,flag='0')
m=json.loads((R/'data/maps/EuropeBerlinHome/map.json').read_text())
m.update(id='MAP_EUROPE_BERLIN_LIBRARY',name=name,layout=lid,object_events=[obj('OBJ_EVENT_GFX_GENTLEMAN',8,3,'Librarian'),obj('OBJ_EVENT_GFX_POKEDEX',3,3,'GardenBook'),obj('OBJ_EVENT_GFX_POKEDEX',11,3,'HistoryBook')])
for event in m['coord_events']:event['script']=name+'_Exit'
d=R/f'data/maps/{name}';d.mkdir(exist_ok=True);(d/'map.json').write_text(json.dumps(m,indent=2)+'\n')
s='''EuropeBerlinLibrary_MapScripts::
 .byte 0

EuropeBerlinLibrary_Enter::
 lockall
 msgbox EuropeBerlinLibrary_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeBerlinLibrary_End
 closemessage
 warp MAP_EUROPE_BERLIN_LIBRARY, 5, 7
 waitstate
 releaseall
 end

EuropeBerlinLibrary_Exit::
 lockall
 warp MAP_EUROPE_BERLIN, 51, 32
 waitstate
 releaseall
 end

EuropeBerlinLibrary_End::
 releaseall
 end

EuropeBerlinLibrary_EntryText::
 .string "NEIGHBORHOOD READING ROOM\\n"
 .string "Come in and browse the records?$"
'''
for label,lines in [('Librarian',['Welcome! These are local records.','People write down what they notice.','A garden, a journey, a helping hand:','small stories deserve a place too.']),('GardenBook',['A shared garden log.','ODDISH rests in the shaded beds.','Each neighbor tends a small patch.','Together, they keep the court green.']),('HistoryBook',['A notebook of neighborhood memories.','Visitors once brought field notes','from journeys across EUROPE.','Care connected one place to another.'])]:
 s+=f'\n{name}_{label}::\n lock\n faceplayer\n msgbox {name}_{label}Text, MSGBOX_DEFAULT\n release\n end\n\n{name}_{label}Text::\n'
 for i,line in enumerate(lines):s+=' .string "'+line+('$' if i==len(lines)-1 else '\\p' if i%2 else '\\n')+'"\n'
(d/'scripts.inc').write_text(s)
p=R/'data/maps/EuropeBerlin/map.json';m=json.loads(p.read_text())
event=dict(type='sign',x=51,y=31,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=name+'_Enter')
i=next((i for i,e in enumerate(m['bg_events']) if e['script']==event['script']),None)
if i is None:m['bg_events'].append(event)
else:m['bg_events'][i]=event
p.write_text(json.dumps(m,indent=2)+'\n')
print('Berlin reading room generated; earlier map IDs retained')
