"""A free Oxford radcliffe visitor room with native return doors."""
from pathlib import Path
import json,shutil
r=Path(__file__).resolve().parents[1]
def write(p,j):
 nl='\r\n' if p.exists() and b'\r\n' in p.read_bytes() else '\n';data=(json.dumps(j,indent=2)+'\n').replace('\n',nl).encode()
 if not p.exists() or p.read_bytes()!=data:p.write_bytes(data)
name='EuropeRadcliffeVisitor';dest=r/'data/maps'/name;dest.mkdir(exist_ok=True)
m=json.loads((r/'data/maps/EuropeEiffelVisitor/map.json').read_text());m['id']='MAP_EUROPE_RADCLIFFE_VISITOR';m['name']=name;m['layout']='LAYOUT_EUROPE_RADCLIFFE_VISITOR';m['region_map_section']='MAPSEC_EUROPE_OXFORD'
for e in m['object_events']+m['coord_events']:e['script']=e['script'].replace('EuropeEiffelVisitor',name).replace('GardenExhibit','ReadingExhibit').replace('RiverExhibit','ObservationExhibit')
archive = dict(m['object_events'][0]);archive.update(graphics_id='OBJ_EVENT_GFX_SCIENTIST', x=6, y=3, script='EuropeArchive_Oxford');m['object_events'].append(archive)
write(dest/'map.json',m)
(dest/'scripts.inc').write_text('''EuropeRadcliffeVisitor_MapScripts::
 .byte 0

EuropeRadcliffeVisitor_Enter::
 lockall
 msgbox EuropeRadcliffeVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeRadcliffeVisitor_End
 closemessage
 warp MAP_EUROPE_RADCLIFFE_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropeRadcliffeVisitor_Exit::
 lockall
 warp MAP_EUROPE_OXFORD, 38, 10
 waitstate
 releaseall
 end

EuropeRadcliffeVisitor_End::
 releaseall
 end

EuropeRadcliffeVisitor_EntryText::
 .string "RADCLIFFE VISITOR ROOM\\n"
 .string "Step inside and browse the displays?$"

EuropeRadcliffeVisitor_Guide::
 lock
 faceplayer
 msgbox EuropeRadcliffeVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropeRadcliffeVisitor_GuideText::
 .string "Welcome to the RADCLIFFE room!\\n"
 .string "Browse the notes beside the shelves.\\p"
 .string "This is a quiet room for reading.\\n"
 .string "Share the tables with other visitors.\\p"
 .string "Leave through the south doorway.\\n"
 .string "You return to RADCLIFFE SQUARE.$"

EuropeRadcliffeVisitor_ReadingExhibit::
 lock
 faceplayer
 msgbox EuropeRadcliffeVisitor_ReadingExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeRadcliffeVisitor_ReadingExhibitText::
 .string "A notebook records careful sightings.\\n"
 .string "Write where and when you saw POKEMON.\\p"
 .string "Compare notes before drawing a map.\\n"
 .string "Leave the books for the next reader.$"

EuropeRadcliffeVisitor_ObservationExhibit::
 lock
 faceplayer
 msgbox EuropeRadcliffeVisitor_ObservationExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeRadcliffeVisitor_ObservationExhibitText::
 .string "A sketch shows the CHERWELL bridges.\\n"
 .string "MAGDALEN lies east of the square.\\p"
 .string "The station is east of the square.\\n"
 .string "The free clinic is on its west side.$"
''')
layoutdir=r/'data/layouts'/name;layoutdir.mkdir(exist_ok=True)
for f in ['map.bin','border.bin']:shutil.copy2(r/'data/layouts/EuropeEiffelVisitor'/f,layoutdir/f)
p=r/'data/layouts/layouts.json';j=json.loads(p.read_text());l=next(v.copy() for v in j['layouts'] if v.get('id')=='LAYOUT_EUROPE_EIFFEL_VISITOR')
l.update(id='LAYOUT_EUROPE_RADCLIFFE_VISITOR',name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
if not any(v.get('id')==l['id'] for v in j['layouts']):j['layouts'].append(l)
write(p,j)
p=r/'data/maps/map_groups.json';j=json.loads(p.read_text())
if name not in j['gMapGroup_Europe']:j['gMapGroup_Europe'].append(name)
write(p,j)
p=r/'data/maps/EuropeOxford/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if e['script']!='EuropeRadcliffeVisitor_Enter'];i=next((i for i,e in enumerate(j['bg_events']) if e['script'].startswith('EuropeOxford_Realism')),len(j['bg_events']))
j['bg_events'].insert(i,dict(type='sign',x=38,y=9,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeRadcliffeVisitor_Enter'));write(p,j)
p=r/'data/event_scripts.s';s=p.read_bytes();line=b'\t.include "data/maps/EuropeRadcliffeVisitor/scripts.inc"'
if line not in s:p.write_bytes(s+(b'\r\n' if b'\r\n' in s else b'\n')+line+b'\n')

from radcliffe_reading_room import build as build_reading_room
build_reading_room()
