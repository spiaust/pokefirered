"""A free Oranienburg palace visitor room with native return doors."""
from pathlib import Path
import json,shutil
r=Path(__file__).resolve().parents[1]
def write(p,j):
 data=(json.dumps(j,indent=2)+'\n').encode()
 if p.exists() and json.loads(p.read_text())==j:return
 nl='\r\n' if p.exists() and b'\r\n' in p.read_bytes() else '\n';p.write_bytes((json.dumps(j,indent=2)+'\n').replace('\n',nl).encode())
name='EuropePalaceVisitor';dest=r/'data/maps'/name;dest.mkdir(exist_ok=True)
m=json.loads((r/'data/maps/EuropeEiffelVisitor/map.json').read_text());m['id']='MAP_EUROPE_PALACE_VISITOR';m['name']=name;m['layout']='LAYOUT_EUROPE_PALACE_VISITOR';m['region_map_section']='MAPSEC_EUROPE_ORANIENBURG'
for e in m['object_events']+m['coord_events']:e['script']=e['script'].replace('EuropeEiffelVisitor',name)
write(dest/'map.json',m)
(dest/'scripts.inc').write_text('''EuropePalaceVisitor_MapScripts::
 .byte 0

EuropePalaceVisitor_Enter::
 lockall
 msgbox EuropePalaceVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropePalaceVisitor_End
 closemessage
 warp MAP_EUROPE_PALACE_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropePalaceVisitor_Exit::
 lockall
 warp MAP_EUROPE_ORANIENBURG, 48, 9
 waitstate
 releaseall
 end

EuropePalaceVisitor_End::
 releaseall
 end

EuropePalaceVisitor_EntryText::
 .string "PALACE VISITOR ROOM\\n"
 .string "Step inside and browse the displays?$"

EuropePalaceVisitor_Guide::
 lock
 faceplayer
 msgbox EuropePalaceVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropePalaceVisitor_GuideText::
 .string "Welcome to the PALACE visitor room!\\n"
 .string "Browse the park and HAVEL displays.\\p"
 .string "The park and Havel are outside.\\n"
 .string "Please keep the water and paths clean.\\p"
 .string "Leave through the south doorway.\\n"
 .string "You return to the PALACE court.$"

EuropePalaceVisitor_GardenExhibit::
 lock
 faceplayer
 msgbox EuropePalaceVisitor_GardenExhibitText, MSGBOX_DEFAULT
 release
 end

EuropePalaceVisitor_GardenExhibitText::
 .string "A garden plan shows paths and water.\\n"
 .string "Watch quietly for visiting POKEMON.\\p"
 .string "Keep notes without disturbing nests.\\n"
 .string "Leave flowers for the next visitor.$"

EuropePalaceVisitor_RiverExhibit::
 lock
 faceplayer
 msgbox EuropePalaceVisitor_RiverExhibitText, MSGBOX_DEFAULT
 release
 end

EuropePalaceVisitor_RiverExhibitText::
 .string "A sketch follows the HAVEL river.\\n"
 .string "Town bridges link the river banks.\\p"
 .string "The station is east of the square.\\n"
 .string "The free clinic is on its west side.$"
''')
layoutdir=r/'data/layouts'/name;layoutdir.mkdir(exist_ok=True)
for f in ['map.bin','border.bin']:shutil.copy2(r/'data/layouts/EuropeEiffelVisitor'/f,layoutdir/f)
p=r/'data/layouts/layouts.json';j=json.loads(p.read_text());l=next(v.copy() for v in j['layouts'] if v.get('id')=='LAYOUT_EUROPE_EIFFEL_VISITOR')
l.update(id='LAYOUT_EUROPE_PALACE_VISITOR',name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
if not any(v.get('id')==l['id'] for v in j['layouts']):j['layouts'].append(l)
write(p,j)
p=r/'data/maps/map_groups.json';j=json.loads(p.read_text())
if name not in j['gMapGroup_Europe']:j['gMapGroup_Europe'].append(name)
write(p,j)
p=r/'data/maps/EuropeOranienburg/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if e['script']!='EuropePalaceVisitor_Enter'];i=next((i for i,e in enumerate(j['bg_events']) if e['script'].startswith('EuropeOranienburg_Realism')),len(j['bg_events']))
j['bg_events'].insert(i,dict(type='sign',x=48,y=8,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropePalaceVisitor_Enter'));write(p,j)
p=r/'data/event_scripts.s';s=p.read_bytes();line=b'\t.include "data/maps/EuropePalaceVisitor/scripts.inc"'
if line not in s:p.write_bytes(s+(b'\r\n' if b'\r\n' in s else b'\n')+line+b'\n')

from palace_gallery import build
build()
