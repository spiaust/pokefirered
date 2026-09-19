"""Three small fictional visitor areas with independent saved landmark cases."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
DATA=[('NotreDame','PARIS','Paris',28,34,'MUS_POKE_TOWER'),('Westminster','LONDON','London',14,34,'MUS_PEWTER'),('Reichstag','BERLIN','Berlin',21,32,'MUS_PEWTER')]
def obj(gfx,x,y,script):return dict(type='object',graphics_id=gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script=script,flag='0')
p=R/'data/maps/map_groups.json';groups=json.loads(p.read_text())
p=R/'data/layouts/layouts.json';layouts=json.loads(p.read_text())
for tag,region,city,dx,dy,music in DATA:
 name='Europe'+tag;mid='MAP_EUROPE_'+tag.upper();lid='LAYOUT_EUROPE_'+tag.upper();w,h=20,18
 a=[[0x681]*w for _ in range(h)]
 for y in range(1,17):
  for x in range(2,18):a[y][x]=(0x698 if tag=='NotreDame' else 0x401) if y==1 else (0x6a0 if tag=='NotreDame' else 0x403) if y==2 else (0x3282 if tag=='NotreDame' else 0x3000)
 for x in (5,14):
  for y in (5,9,13):
   a[y][x]=0x691 if tag=='NotreDame' else 0x401
   a[y+1][x]=0x3282 if tag=='NotreDame' else 0x403
 # Side aisles, central passage and an exit marker remain walkable.
 a[16][10]=0x3286
 dest=R/f'data/layouts/{name}';dest.mkdir(exist_ok=True)
 (dest/'map.bin').write_bytes(struct.pack('<%dH'%(w*h),*(t for row in a for t in row)))
 (dest/'border.bin').write_bytes(struct.pack('<4H',*[0x681]*4))
 l=dict(id=lid,name=name+'_Layout',width=w,height=h,border_width=2,border_height=2,primary_tileset='gTileset_Building',secondary_tileset='gTileset_PokemonTower',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
 found=next((i for i,v in enumerate(layouts['layouts']) if v.get('id')==lid),None)
 if found is None:layouts['layouts'].append(l)
 else:layouts['layouts'][found]=l
 m=dict(id=mid,name=name,layout=lid,music=music,region_map_section='MAPSEC_EUROPE_'+region,requires_flash=False,weather='WEATHER_NONE',map_type='MAP_TYPE_INDOOR',allow_cycling=False,allow_escaping=False,allow_running=False,show_map_name=False,floor_number=0,battle_scene='MAP_BATTLE_SCENE_INDOOR_1',connections=None,object_events=[obj('OBJ_EVENT_GFX_GENTLEMAN',8,14,'EuropeCase_'+tag+'_Curator'),obj('OBJ_EVENT_GFX_POKEDEX',4,5,'EuropeCase_'+tag+'_ClueA'),obj('OBJ_EVENT_GFX_POKEDEX',15,7,'EuropeCase_'+tag+'_ClueB'),obj('OBJ_EVENT_GFX_OLD_MAN_1' if tag=='NotreDame' else 'OBJ_EVENT_GFX_WORKER_M',10,4,'EuropeCase_'+tag+'_Resolve'),obj('OBJ_EVENT_GFX_SIGN',12,15,'EuropeCase_Ledger')],warp_events=[],coord_events=[dict(type='trigger',x=10,y=16,elevation=3,var='VAR_TEMP_0',var_value='0',script='EuropeCase_'+tag+'_Exit')],bg_events=[dict(type='sign',x=10,y=16,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeCase_'+tag+'_Exit')])
 dest=R/f'data/maps/{name}';dest.mkdir(exist_ok=True);(dest/'map.json').write_text(json.dumps(m,indent=2)+'\n');(dest/'scripts.inc').write_text(name+'_MapScripts::\n\t.byte 0\n')
 if name not in groups['gMapGroup_Europe']:groups['gMapGroup_Europe'].append(name)
 p=R/f'data/maps/Europe{city}/map.json';m=json.loads(p.read_text());m['bg_events']=[v for v in m['bg_events'] if v['script']!='EuropeCase_'+tag+'_Enter'];m['bg_events'].append(dict(type='sign',x=dx,y=dy,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeCase_'+tag+'_Enter'));p.write_text(json.dumps(m,indent=2)+'\n')
(R/'data/maps/map_groups.json').write_text(json.dumps(groups,indent=2)+'\n');(R/'data/layouts/layouts.json').write_text(json.dumps(layouts,indent=2)+'\n')
