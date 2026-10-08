"""Append a fictional Paris garden workroom without changing existing map IDs."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
name='EuropeParisGardenRoom';lid='LAYOUT_EUROPE_PARIS_GARDEN_ROOM'
p=R/'data/layouts/layouts.json';ls=json.loads(p.read_text())
source=next(l for l in ls['layouts'] if l.get('id')=='LAYOUT_PALLET_TOWN_PLAYERS_HOUSE_1F')
l=dict(source,id=lid,name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
d=R/f'data/layouts/{name}';d.mkdir(exist_ok=True)
a=list(struct.unpack('<130H',(R/source['blockdata_filepath']).read_bytes()))
# Replace the full stair artwork and landing with matching wall/floor tiles.
for y,tile in [(1,0x428),(2,0x3009),(3,0x3001)]:
 for x in (10,11,12):a[y*13+x]=tile
# Side workbenches leave a broad central passage to both front exits.
for y in range(3,7):
 for x in range(4,10):a[y*13+x]=0x3001
for bx in (2,10):
 for y,row in enumerate([(0x44c,0x44d),(0x454,0x455)]):
  for x,t in enumerate(row):a[(5+y)*13+bx+x]=t
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
 return dict(type='object',graphics_id=gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script='EuropeParisGardenRoom_'+label,flag='0')
m=dict(id='MAP_EUROPE_PARIS_GARDEN_ROOM',name=name,layout=lid,music='MUS_PALLET',region_map_section='MAPSEC_EUROPE_PARIS',requires_flash=False,weather='WEATHER_NONE',map_type='MAP_TYPE_INDOOR',allow_cycling=False,allow_escaping=False,allow_running=False,show_map_name=False,floor_number=0,battle_scene='MAP_BATTLE_SCENE_INDOOR_1',connections=None,object_events=[obj('OBJ_EVENT_GFX_WOMAN_1',8,4,'Host'),obj('OBJ_EVENT_GFX_POKEDEX',3,3,'Notebook')],warp_events=[],coord_events=[dict(type='trigger',x=x,y=8,elevation=3,var='VAR_TEMP_0',var_value='0',script='EuropeParisGardenRoom_Exit') for x in (4,5)],bg_events=[dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeParisGardenRoom_'+label) for bx,label in [(2,'Plan'),(10,'Rota')] for x in (bx,bx+1) for y in (5,6)])
d=R/f'data/maps/{name}';d.mkdir(exist_ok=True);(d/'map.json').write_text(json.dumps(m,indent=2)+'\n')
(d/'scripts.inc').write_text('''EuropeParisGardenRoom_MapScripts::
 .byte 0

EuropeParisGardenRoom_Enter::
 lockall
 msgbox EuropeParisGardenRoom_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeParisGardenRoom_End
 closemessage
 warp MAP_EUROPE_PARIS_GARDEN_ROOM, 5, 7
 waitstate
 releaseall
 end

EuropeParisGardenRoom_Exit::
 lockall
 warp MAP_EUROPE_PARIS, 55, 39
 waitstate
 releaseall
 end

EuropeParisGardenRoom_Host::
 lock
 faceplayer
 msgbox EuropeParisGardenRoom_HostText, MSGBOX_DEFAULT
 release
 end

EuropeParisGardenRoom_Notebook::
 lock
 msgbox EuropeParisGardenRoom_NotebookText, MSGBOX_DEFAULT
 release
 end

EuropeParisGardenRoom_Plan::
 lockall
 msgbox EuropeParisGardenRoom_PlanText, MSGBOX_DEFAULT
 releaseall
 end

EuropeParisGardenRoom_PlanText::
 .string "A plan for the neighborhood beds.\\n"
 .string "Low flowers beside the public paths.\\p"
 .string "Leave a quiet patch for POKEMON.\\n"
 .string "Keep the walking loop open.$"

EuropeParisGardenRoom_Rota::
 lockall
 msgbox EuropeParisGardenRoom_RotaText, MSGBOX_DEFAULT
 releaseall
 end

EuropeParisGardenRoom_RotaText::
 .string "A rota of small garden tasks.\\n"
 .string "One neighbor waters the flower beds.\\p"
 .string "Another clears leaves from the path.\\n"
 .string "The work is shared, a little daily.$"

EuropeParisGardenRoom_End::
 releaseall
 end

EuropeParisGardenRoom_EntryText::
 .string "A neighbor welcomes visitors.\\n"
 .string "Visit the garden workroom?$"

EuropeParisGardenRoom_HostText::
 .string "Welcome to our garden workroom.\\n"
 .string "We plan the flower beds together.\\p"
 .string "Both benches hold our garden plans.\\n"
 .string "Take a look; everyone can help.\\p"
 .string "Leave south; follow the lane west.\\n"
 .string "The promenade leads to the EIFFEL.$"

EuropeParisGardenRoom_NotebookText::
 .string "A notebook of shared garden plans.\\n"
 .string "Give resting POKEMON a quiet space.\\p"
 .string "Keep the promenade clear for walkers.\\n"
 .string "Share the work and enjoy the flowers.$"
''')
p=R/'data/maps/EuropeParis/map.json';m=json.loads(p.read_text())
event=dict(type='sign',x=55,y=38,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeParisGardenRoom_Enter')
i=next((i for i,e in enumerate(m['bg_events']) if e['script']==event['script']),None)
if i is None:m['bg_events'].append(event)
else:m['bg_events'][i]=event
p.write_text(json.dumps(m,indent=2)+'\n')
print('Paris garden workroom generated; existing map IDs retained')
