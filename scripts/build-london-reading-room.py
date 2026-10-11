"""Append a fictional London reading room without changing existing map IDs."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
name='EuropeLondonReadingRoom';lid='LAYOUT_EUROPE_LONDON_READING_ROOM'
p=R/'data/layouts/layouts.json';ls=json.loads(p.read_text())
source=next(l for l in ls['layouts'] if l.get('id')=='LAYOUT_PALLET_TOWN_PLAYERS_HOUSE_1F')
l=dict(source,id=lid,name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
d=R/f'data/layouts/{name}';d.mkdir(exist_ok=True)
a=list(struct.unpack('<130H',(R/source['blockdata_filepath']).read_bytes()))
# Replace the full stair artwork and landing with matching wall/floor tiles.
for y,tile in [(1,0x428),(2,0x3009),(3,0x3001)]:
 for x in (10,11,12):a[y*13+x]=tile
# Open reading area; the compact table occupies its existing footprint.
for y in range(3,7):
 for x in range(4,10):a[y*13+x]=0x3001
for y,row in enumerate([(0x44c,0x44d),(0x454,0x455)]):
 for x,t in enumerate(row):a[(4+y)*13+6+x]=t
# Cabinet artwork stays within the existing solid back wall.
a[9:11]=[0x421,0x422];a[22:24]=[0x429,0x42a]
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
 return dict(type='object',graphics_id=gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script='EuropeLondonReadingRoom_'+label,flag='0')
m=dict(id='MAP_EUROPE_LONDON_READING_ROOM',name=name,layout=lid,music='MUS_PALLET',region_map_section='MAPSEC_EUROPE_LONDON',requires_flash=False,weather='WEATHER_NONE',map_type='MAP_TYPE_INDOOR',allow_cycling=False,allow_escaping=False,allow_running=False,show_map_name=False,floor_number=0,battle_scene='MAP_BATTLE_SCENE_INDOOR_1',connections=None,object_events=[obj('OBJ_EVENT_GFX_MAN',8,4,'Host'),obj('OBJ_EVENT_GFX_POKEDEX',3,3,'Notebook')],warp_events=[],coord_events=[dict(type='trigger',x=x,y=8,elevation=3,var='VAR_TEMP_0',var_value='0',script='EuropeLondonReadingRoom_Exit') for x in (4,5)],bg_events=[dict(type='sign',x=9,y=1,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeLondonReadingRoom_Books')])
reception=obj('OBJ_EVENT_GFX_GYM_GUY',5,3,'CouncilReception');reception['script']='EuropeCouncil_Reception';m['object_events'].append(reception)
d=R/f'data/maps/{name}';d.mkdir(exist_ok=True);(d/'map.json').write_text(json.dumps(m,indent=2)+'\n')
(d/'scripts.inc').write_text('''EuropeLondonReadingRoom_MapScripts::
 .byte 0

EuropeLondonReadingRoom_Enter::
 lockall
 msgbox EuropeLondonReadingRoom_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeLondonReadingRoom_End
 closemessage
 warp MAP_EUROPE_LONDON_READING_ROOM, 5, 7
 waitstate
 releaseall
 end

EuropeLondonReadingRoom_Exit::
 lockall
 warp MAP_EUROPE_LONDON, 55, 33
 waitstate
 releaseall
 end

EuropeLondonReadingRoom_Host::
 lock
 faceplayer
 msgbox EuropeLondonReadingRoom_HostText, MSGBOX_DEFAULT
 release
 end

EuropeLondonReadingRoom_Notebook::
 lock
 msgbox EuropeLondonReadingRoom_NotebookText, MSGBOX_DEFAULT
 release
 end

EuropeLondonReadingRoom_Books::
 lockall
 msgbox EuropeLondonReadingRoom_BooksText, MSGBOX_DEFAULT
 releaseall
 end

EuropeLondonReadingRoom_BooksText::
 .string "A cabinet of well-read books.\\n"
 .string "Neighbors leave notes in the margins.\\p"
 .string "A label says: Share a favorite walk,\\n"
 .string "and help the next visitor explore.$"

EuropeLondonReadingRoom_End::
 releaseall
 end

EuropeLondonReadingRoom_EntryText::
 .string "READING ROOM / COUNCIL RECEPTION\\n"
 .string "Visit the reading room?$"

EuropeLondonReadingRoom_HostText::
 .string "Welcome to our reading room.\\n"
 .string "I collect notes about local walks.\\p"
 .string "The bridges link both riverbanks.\\n"
 .string "Take your time and enjoy the view.\\p"
 .string "Leave south, then follow the lane\\n"
 .string "west to the EYE and its gallery.$"

EuropeLondonReadingRoom_NotebookText::
 .string "A notebook of riverside walks.\\n"
 .string "West: the EYE and its gallery.\\p"
 .string "Cross the bridges for WESTMINSTER.\\n"
 .string "The garden loop leads back here.$"
''')
p=R/'data/maps/EuropeLondon/map.json';m=json.loads(p.read_text())
event=dict(type='sign',x=55,y=32,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeLondonReadingRoom_Enter')
i=next((i for i,e in enumerate(m['bg_events']) if e['script']==event['script']),None)
if i is None:m['bg_events'].append(event)
else:m['bg_events'][i]=event
p.write_text(json.dumps(m,indent=2)+'\n')
print('London reading room generated; existing map IDs retained')
