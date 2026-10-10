"""A free Chantilly stables visitor room with native return doors."""
from pathlib import Path
import json,shutil
r=Path(__file__).resolve().parents[1]
def write(p,j):
 nl='\r\n' if p.exists() and b'\r\n' in p.read_bytes() else '\n';data=(json.dumps(j,indent=2)+'\n').replace('\n',nl).encode()
 if not p.exists() or p.read_bytes()!=data:p.write_bytes(data)
name='EuropeStablesVisitor';dest=r/'data/maps'/name;dest.mkdir(exist_ok=True)
m=json.loads((r/'data/maps/EuropeEiffelVisitor/map.json').read_text());m['id']='MAP_EUROPE_STABLES_VISITOR';m['name']=name;m['layout']='LAYOUT_EUROPE_STABLES_VISITOR';m['region_map_section']='MAPSEC_EUROPE_CHANTILLY'
for e in m['object_events']+m['coord_events']:e['script']=e['script'].replace('EuropeEiffelVisitor',name)
m['object_events'][0]['graphics_id']='OBJ_EVENT_GFX_MAN'
write(dest/'map.json',m)
(dest/'scripts.inc').write_text('''EuropeStablesVisitor_MapScripts::
 .byte 0

EuropeStablesVisitor_Enter::
 lockall
 msgbox EuropeStablesVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeStablesVisitor_End
 closemessage
 warp MAP_EUROPE_STABLES_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropeStablesVisitor_Exit::
 lockall
 warp MAP_EUROPE_CHANTILLY, 38, 19
 waitstate
 releaseall
 end

EuropeStablesVisitor_End::
 releaseall
 end

EuropeStablesVisitor_EntryText::
 .string "STABLES VISITOR ROOM\\n"
 .string "Step inside and browse the displays?$"

EuropeStablesVisitor_Guide::
 lock
 faceplayer
 msgbox EuropeStablesVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropeStablesVisitor_GuideText::
 .string "Welcome to the STABLES visitor room!\\n"
 .string "Browse care notes beside the benches.\\p"
 .string "The estate paths are outside.\\n"
 .string "Give resting POKEMON plenty of space.\\p"
 .string "Leave through the south doorway.\\n"
 .string "You return to the STABLES path.$"

EuropeStablesVisitor_GardenExhibit::
 lock
 faceplayer
 msgbox EuropeStablesVisitor_GardenExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeStablesVisitor_GardenExhibitText::
 .string "A care board lists water and rest.\\n"
 .string "Travelling POKEMON need breaks too.\\p"
 .string "Ask before approaching an animal.\\n"
 .string "Keep paths clear for the caretakers.$"

EuropeStablesVisitor_RiverExhibit::
 lock
 faceplayer
 msgbox EuropeStablesVisitor_RiverExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeStablesVisitor_RiverExhibitText::
 .string "An estate plan marks the moat bridge.\\n"
 .string "The CHATEAU lies north of here.\\p"
 .string "The station is east of the square.\\n"
 .string "The free clinic is on its west side.$"
''')
layoutdir=r/'data/layouts'/name;layoutdir.mkdir(exist_ok=True)
for f in ['map.bin','border.bin']:shutil.copy2(r/'data/layouts/EuropeEiffelVisitor'/f,layoutdir/f)
p=r/'data/layouts/layouts.json';j=json.loads(p.read_text());l=next(v.copy() for v in j['layouts'] if v.get('id')=='LAYOUT_EUROPE_EIFFEL_VISITOR')
l.update(id='LAYOUT_EUROPE_STABLES_VISITOR',name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
if not any(v.get('id')==l['id'] for v in j['layouts']):j['layouts'].append(l)
write(p,j)
p=r/'data/maps/map_groups.json';j=json.loads(p.read_text())
if name not in j['gMapGroup_Europe']:j['gMapGroup_Europe'].append(name)
write(p,j)
p=r/'data/maps/EuropeChantilly/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if e['script']!='EuropeStablesVisitor_Enter'];i=next((i for i,e in enumerate(j['bg_events']) if e['script'].startswith('EuropeChantilly_Realism')),len(j['bg_events']))
j['bg_events'].insert(i,dict(type='sign',x=38,y=18,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeStablesVisitor_Enter'));write(p,j)
p=r/'data/event_scripts.s';s=p.read_bytes();line=b'\t.include "data/maps/EuropeStablesVisitor/scripts.inc"'
if line not in s:p.write_bytes(s+(b'\r\n' if b'\r\n' in s else b'\n')+line+b'\n')

from stables_care_room import build as build_care_room
build_care_room()
