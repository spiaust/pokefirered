"""A free Chantilly château visitor room with native return doors."""
from pathlib import Path
import json,shutil
r=Path(__file__).resolve().parents[1]
def write(p,j):
 nl='\r\n' if p.exists() and b'\r\n' in p.read_bytes() else '\n';data=(json.dumps(j,indent=2)+'\n').replace('\n',nl).encode()
 if not p.exists() or p.read_bytes()!=data:p.write_bytes(data)
name='EuropeChateauVisitor';dest=r/'data/maps'/name;dest.mkdir(exist_ok=True)
m=json.loads((r/'data/maps/EuropeEiffelVisitor/map.json').read_text());m['id']='MAP_EUROPE_CHATEAU_VISITOR';m['name']=name;m['layout']='LAYOUT_EUROPE_CHATEAU_VISITOR';m['region_map_section']='MAPSEC_EUROPE_CHANTILLY'
for e in m['object_events']+m['coord_events']:e['script']=e['script'].replace('EuropeEiffelVisitor',name)
archive = dict(m['object_events'][0]);archive.update(graphics_id='OBJ_EVENT_GFX_SCIENTIST', x=6, y=3, script='EuropeArchive_Chantilly');m['object_events'].append(archive)
write(dest/'map.json',m)
(dest/'scripts.inc').write_text('''EuropeChateauVisitor_MapScripts::
 .byte 0

EuropeChateauVisitor_Enter::
 lockall
 msgbox EuropeChateauVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeChateauVisitor_End
 closemessage
 warp MAP_EUROPE_CHATEAU_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropeChateauVisitor_Exit::
 lockall
 warp MAP_EUROPE_CHANTILLY, 51, 11
 waitstate
 releaseall
 end

EuropeChateauVisitor_End::
 releaseall
 end

EuropeChateauVisitor_EntryText::
 .string "CHATEAU VISITOR ROOM\\n"
 .string "Step inside and browse the displays?$"

EuropeChateauVisitor_Guide::
 lock
 faceplayer
 msgbox EuropeChateauVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropeChateauVisitor_GuideText::
 .string "Welcome to the CHATEAU visitor room!\\n"
 .string "Browse the garden and moat displays.\\p"
 .string "The garden paths and moat are outside.\\n"
 .string "Please keep the water and paths clean.\\p"
 .string "Leave through the south doorway.\\n"
 .string "You return to the CHATEAU court.$"

EuropeChateauVisitor_GardenExhibit::
 lock
 faceplayer
 msgbox EuropeChateauVisitor_GardenExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeChateauVisitor_GardenExhibitText::
 .string "A garden plan shows paths and water.\\n"
 .string "Watch quietly for visiting POKEMON.\\p"
 .string "Keep notes without disturbing nests.\\n"
 .string "Leave flowers for the next visitor.$"

EuropeChateauVisitor_RiverExhibit::
 lock
 faceplayer
 msgbox EuropeChateauVisitor_RiverExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeChateauVisitor_RiverExhibitText::
 .string "A sketch follows the CHATEAU moat.\\n"
 .string "Bridges lead back to the town paths.\\p"
 .string "The station is east of the square.\\n"
 .string "The free clinic is on its west side.$"
''')
layoutdir=r/'data/layouts'/name;layoutdir.mkdir(exist_ok=True)
for f in ['map.bin','border.bin']:shutil.copy2(r/'data/layouts/EuropeEiffelVisitor'/f,layoutdir/f)
p=r/'data/layouts/layouts.json';j=json.loads(p.read_text());l=next(v.copy() for v in j['layouts'] if v.get('id')=='LAYOUT_EUROPE_EIFFEL_VISITOR')
l.update(id='LAYOUT_EUROPE_CHATEAU_VISITOR',name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
if not any(v.get('id')==l['id'] for v in j['layouts']):j['layouts'].append(l)
write(p,j)
p=r/'data/maps/map_groups.json';j=json.loads(p.read_text())
if name not in j['gMapGroup_Europe']:j['gMapGroup_Europe'].append(name)
write(p,j)
p=r/'data/maps/EuropeChantilly/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if e['script']!='EuropeChateauVisitor_Enter'];i=next((i for i,e in enumerate(j['bg_events']) if e['script'].startswith('EuropeChantilly_Realism')),len(j['bg_events']))
j['bg_events'].insert(i,dict(type='sign',x=51,y=10,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeChateauVisitor_Enter'));write(p,j)
p=r/'data/event_scripts.s';s=p.read_bytes();line=b'\t.include "data/maps/EuropeChateauVisitor/scripts.inc"'
if line not in s:p.write_bytes(s+(b'\r\n' if b'\r\n' in s else b'\n')+line+b'\n')

from chateau_gallery import build as build_gallery
build_gallery()
