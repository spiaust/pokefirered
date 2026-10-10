"""A free Oxford magdalen visitor room with native return doors."""
from pathlib import Path
import json,shutil
r=Path(__file__).resolve().parents[1]
def write(p,j):
 nl='\r\n' if p.exists() and b'\r\n' in p.read_bytes() else '\n';data=(json.dumps(j,indent=2)+'\n').replace('\n',nl).encode()
 if not p.exists() or p.read_bytes()!=data:p.write_bytes(data)
name='EuropeMagdalenVisitor';dest=r/'data/maps'/name;dest.mkdir(exist_ok=True)
m=json.loads((r/'data/maps/EuropeEiffelVisitor/map.json').read_text());m['id']='MAP_EUROPE_MAGDALEN_VISITOR';m['name']=name;m['layout']='LAYOUT_EUROPE_MAGDALEN_VISITOR';m['region_map_section']='MAPSEC_EUROPE_OXFORD'
for e in m['object_events']+m['coord_events']:e['script']=e['script'].replace('EuropeEiffelVisitor',name)
m['object_events'][0]['graphics_id']='OBJ_EVENT_GFX_MAN'
write(dest/'map.json',m)
(dest/'scripts.inc').write_text('''EuropeMagdalenVisitor_MapScripts::
 .byte 0

EuropeMagdalenVisitor_Enter::
 lockall
 msgbox EuropeMagdalenVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeMagdalenVisitor_End
 closemessage
 warp MAP_EUROPE_MAGDALEN_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropeMagdalenVisitor_Exit::
 lockall
 warp MAP_EUROPE_OXFORD, 51, 11
 waitstate
 releaseall
 end

EuropeMagdalenVisitor_End::
 releaseall
 end

EuropeMagdalenVisitor_EntryText::
 .string "MAGDALEN VISITOR ROOM\\n"
 .string "Step inside and browse the displays?$"

EuropeMagdalenVisitor_Guide::
 lock
 faceplayer
 msgbox EuropeMagdalenVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropeMagdalenVisitor_GuideText::
 .string "Welcome to the MAGDALEN visitor room!\\n"
 .string "Browse the tower and river displays.\\p"
 .string "The CHERWELL paths are outside.\\n"
 .string "Pause quietly to watch river POKEMON.\\p"
 .string "Leave through the south doorway.\\n"
 .string "You return to the MAGDALEN approach.$"

EuropeMagdalenVisitor_GardenExhibit::
 lock
 faceplayer
 msgbox EuropeMagdalenVisitor_GardenExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeMagdalenVisitor_GardenExhibitText::
 .string "A drawing shows the tower silhouette.\\n"
 .string "Compare its outline from the street.\\p"
 .string "The display is for quiet visitors.\\n"
 .string "Leave the tower drawing on the desk.$"

EuropeMagdalenVisitor_RiverExhibit::
 lock
 faceplayer
 msgbox EuropeMagdalenVisitor_RiverExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeMagdalenVisitor_RiverExhibitText::
 .string "A path plan follows the CHERWELL.\\n"
 .string "The meadow paths lie to the south.\\p"
 .string "The station is east of the square.\\n"
 .string "The free clinic is on its west side.$"
''')
layoutdir=r/'data/layouts'/name;layoutdir.mkdir(exist_ok=True)
for f in ['map.bin','border.bin']:shutil.copy2(r/'data/layouts/EuropeEiffelVisitor'/f,layoutdir/f)
p=r/'data/layouts/layouts.json';j=json.loads(p.read_text());l=next(v.copy() for v in j['layouts'] if v.get('id')=='LAYOUT_EUROPE_EIFFEL_VISITOR')
l.update(id='LAYOUT_EUROPE_MAGDALEN_VISITOR',name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
if not any(v.get('id')==l['id'] for v in j['layouts']):j['layouts'].append(l)
write(p,j)
p=r/'data/maps/map_groups.json';j=json.loads(p.read_text())
if name not in j['gMapGroup_Europe']:j['gMapGroup_Europe'].append(name)
write(p,j)
p=r/'data/maps/EuropeOxford/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if e['script']!='EuropeMagdalenVisitor_Enter'];i=next((i for i,e in enumerate(j['bg_events']) if e['script'].startswith('EuropeOxford_Realism')),len(j['bg_events']))
j['bg_events'].insert(i,dict(type='sign',x=51,y=10,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeMagdalenVisitor_Enter'));write(p,j)
p=r/'data/event_scripts.s';s=p.read_bytes();line=b'\t.include "data/maps/EuropeMagdalenVisitor/scripts.inc"'
if line not in s:p.write_bytes(s+(b'\r\n' if b'\r\n' in s else b'\n')+line+b'\n')

from magdalen_study_room import build as build_study_room
build_study_room()
