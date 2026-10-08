"""Append a fictional courtyard sitting room without changing existing map IDs."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
name='EuropeBerlinHome';lid='LAYOUT_EUROPE_BERLIN_HOME'
p=R/'data/layouts/layouts.json';ls=json.loads(p.read_text())
source=next(l for l in ls['layouts'] if l.get('id')=='LAYOUT_PALLET_TOWN_PLAYERS_HOUSE_1F')
l=dict(source,id=lid,name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
d=R/f'data/layouts/{name}';d.mkdir(exist_ok=True)
a=list(struct.unpack('<130H',(R/source['blockdata_filepath']).read_bytes()))
# Replace the full stair artwork and landing with matching wall/floor tiles.
for y,tile in [(1,0x428),(2,0x3009),(3,0x3001)]:
 for x in (10,11,12):a[y*13+x]=tile
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
 return dict(type='object',graphics_id=gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script='EuropeBerlinHome_'+label,flag='0')
m=dict(id='MAP_EUROPE_BERLIN_HOME',name=name,layout=lid,music='MUS_PALLET',region_map_section='MAPSEC_EUROPE_BERLIN',requires_flash=False,weather='WEATHER_NONE',map_type='MAP_TYPE_INDOOR',allow_cycling=False,allow_escaping=False,allow_running=False,show_map_name=False,floor_number=0,battle_scene='MAP_BATTLE_SCENE_INDOOR_1',connections=None,object_events=[obj('OBJ_EVENT_GFX_WOMAN_2',8,4,'Host'),obj('OBJ_EVENT_GFX_POKEDEX',3,3,'Notebook')],warp_events=[],coord_events=[dict(type='trigger',x=x,y=8,elevation=3,var='VAR_TEMP_0',var_value='0',script='EuropeBerlinHome_Exit') for x in (4,5)],bg_events=[dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeBerlinHome_Guestbook') for x in (6,7) for y in (4,5)])
d=R/f'data/maps/{name}';d.mkdir(exist_ok=True);(d/'map.json').write_text(json.dumps(m,indent=2)+'\n')
(d/'scripts.inc').write_text('''EuropeBerlinHome_MapScripts::
 .byte 0

EuropeBerlinHome_Enter::
 lockall
 msgbox EuropeBerlinHome_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeBerlinHome_End
 closemessage
 warp MAP_EUROPE_BERLIN_HOME, 5, 7
 waitstate
 releaseall
 end

EuropeBerlinHome_Exit::
 lockall
 warp MAP_EUROPE_BERLIN, 43, 32
 waitstate
 releaseall
 end

EuropeBerlinHome_Host::
 lock
 faceplayer
 msgbox EuropeBerlinHome_HostText, MSGBOX_DEFAULT
 release
 end

EuropeBerlinHome_Notebook::
 lock
 msgbox EuropeBerlinHome_NotebookText, MSGBOX_DEFAULT
 release
 end

EuropeBerlinHome_Guestbook::
 lockall
 msgbox EuropeBerlinHome_GuestbookText, MSGBOX_DEFAULT
 releaseall
 end

EuropeBerlinHome_GuestbookText::
 .string "A guestbook of courtyard memories.\\n"
 .string "Visitors sketch the flowers and trees.\\p"
 .string "One recalls a quiet walk by the GATE.\\n"
 .string "Another thanks the garden neighbors.$"

EuropeBerlinHome_End::
 releaseall
 end

EuropeBerlinHome_EntryText::
 .string "A neighbor has opened their home.\\n"
 .string "Visit the sitting room?$"

EuropeBerlinHome_HostText::
 .string "Welcome! Rest your feet a moment.\\n"
 .string "Our garden is a shared little joy.\\p"
 .string "Neighbors take turns tending it.\\n"
 .string "The guestbook is on the table.\\p"
 .string "Walk east along the courtyard.\\n"
 .string "The middle door is the reading room.$"

EuropeBerlinHome_NotebookText::
 .string "A notebook of garden observations.\\n"
 .string "ODDISH prefers the shaded beds.\\p"
 .string "Leave the southern lane clear,\\n"
 .string "so everyone can reach the flowers.$"
''')
p=R/'data/maps/EuropeBerlin/map.json';m=json.loads(p.read_text())
event=dict(type='sign',x=43,y=31,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeBerlinHome_Enter')
i=next((i for i,e in enumerate(m['bg_events']) if e['script']==event['script']),None)
if i is None:m['bg_events'].append(event)
else:m['bg_events'][i]=event
p.write_text(json.dumps(m,indent=2)+'\n')
print('Berlin sitting room generated; existing map IDs retained')
