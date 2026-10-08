"""Append a fictional London sitting room without changing existing map IDs."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
name='EuropeLondonHome';lid='LAYOUT_EUROPE_LONDON_HOME'
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
 return dict(type='object',graphics_id=gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script='EuropeLondonHome_'+label,flag='0')
m=dict(id='MAP_EUROPE_LONDON_HOME',name=name,layout=lid,music='MUS_PALLET',region_map_section='MAPSEC_EUROPE_LONDON',requires_flash=False,weather='WEATHER_NONE',map_type='MAP_TYPE_INDOOR',allow_cycling=False,allow_escaping=False,allow_running=False,show_map_name=False,floor_number=0,battle_scene='MAP_BATTLE_SCENE_INDOOR_1',connections=None,object_events=[obj('OBJ_EVENT_GFX_WOMAN_2',8,4,'Host'),obj('OBJ_EVENT_GFX_POKEDEX',3,3,'Notebook'),obj('OBJ_EVENT_GFX_POKEDEX',6,4,'Album')],warp_events=[],coord_events=[dict(type='trigger',x=x,y=8,elevation=3,var='VAR_TEMP_0',var_value='0',script='EuropeLondonHome_Exit') for x in (4,5)],bg_events=[dict(type='sign',x=6,y=4,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeLondonHome_Album')])
d=R/f'data/maps/{name}';d.mkdir(exist_ok=True);(d/'map.json').write_text(json.dumps(m,indent=2)+'\n')
(d/'scripts.inc').write_text('''EuropeLondonHome_MapScripts::
 .byte 0

EuropeLondonHome_Enter::
 lockall
 msgbox EuropeLondonHome_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeLondonHome_End
 closemessage
 warp MAP_EUROPE_LONDON_HOME, 5, 7
 waitstate
 releaseall
 end

EuropeLondonHome_Exit::
 lockall
 warp MAP_EUROPE_LONDON, 45, 33
 waitstate
 releaseall
 end

EuropeLondonHome_Host::
 lock
 faceplayer
 msgbox EuropeLondonHome_HostText, MSGBOX_DEFAULT
 release
 end

EuropeLondonHome_Notebook::
 lock
 msgbox EuropeLondonHome_NotebookText, MSGBOX_DEFAULT
 release
 end

EuropeLondonHome_Album::
 lock
 msgbox EuropeLondonHome_AlbumText, MSGBOX_DEFAULT
 release
 end

EuropeLondonHome_AlbumText::
 .string "An album of neighborhood photos.\\n"
 .string "The first shows a bare garden bed.\\p"
 .string "Later photos show spring flowers\\n"
 .string "and neighbors watering together.\\p"
 .string "A note: Every season, a little care\\n"
 .string "makes this lane feel like home.$"

EuropeLondonHome_End::
 releaseall
 end

EuropeLondonHome_EntryText::
 .string "A neighbor has opened their home.\\n"
 .string "Visit the sitting room?$"

EuropeLondonHome_HostText::
 .string "Welcome! Rest your feet a moment.\\n"
 .string "Our photo album is on the table.\\p"
 .string "We take turns looking after the beds.\\n"
 .string "Small acts of care add up.\\p"
 .string "The blue-roofed home to the east\\n"
 .string "has a reading room. Visitors welcome!$"

EuropeLondonHome_NotebookText::
 .string "A notebook of garden observations.\\n"
 .string "JIGGLYPUFF rests near the EYE.\\p"
 .string "Keep the public paths clear,\\n"
 .string "so visitors can circle the gardens.$"
''')
p=R/'data/maps/EuropeLondon/map.json';m=json.loads(p.read_text())
event=dict(type='sign',x=45,y=32,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeLondonHome_Enter')
i=next((i for i,e in enumerate(m['bg_events']) if e['script']==event['script']),None)
if i is None:m['bg_events'].append(event)
else:m['bg_events'][i]=event
p.write_text(json.dumps(m,indent=2)+'\n')
print('London sitting room generated; existing map IDs retained')
