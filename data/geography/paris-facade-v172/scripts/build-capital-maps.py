"""Author compressed Paris and Berlin landmark districts, preserving hub IDs."""
from pathlib import Path
import json,struct,sys
R=Path(__file__).resolve().parents[1]
def build(city):
 W,H=(64,46) if city=='Paris' else (64,44)
 old=struct.unpack('<768H',(R/f'data/geography/{city.lower()}-v050.bin').read_bytes())
 a=[[0x3010 for x in range(W)] for y in range(H)]
 for y in range(22):a[y][:32]=old[y*32:(y+1)*32]
 def rect(x,y,w,h,t):
  for yy in range(y,y+h):
   for xx in range(x,x+w):a[yy][xx]=t
 # New streets connect to the original central approach without moving events.
 for y in range(2,15):
  for x in range(2,30):
   if a[y][x]==0x3296:a[y][x]=0x3165 if (14<=x<=17 or 12<=y<=14) else 0x3010
 water=set()
 if city=='Paris':
  rect(14,22,4,6,0x3165);rect(3,26,34,2,0x3165)
  for x in range(2,38):
   top=28 if x<14 else 29 if x<22 else 30
   for y in range(top,top+(3 if x<22 else 8)):water.add((x,y))
  island={(x,y) for x in range(24,32) for y in range(31,37)};water-=island
  for x,y in island:a[y][x]=0x3165
  rect(3,40,34,2,0x3165);rect(34,28,3,12,0x3165)
  rect(5,38,3,2,0x3004);rect(10,38,3,2,0x3004);rect(8,37,2,7,0x3165)
  # Compressed left-bank promenade and garden loops. Water and landmarks
  # are stamped afterwards, retaining the island and existing river edges.
  rect(3,31,19,2,0x3165)
  rect(3,32,2,12,0x3165);rect(13,32,2,12,0x3165)
  rect(3,36,19,1,0x3165);rect(3,42,12,2,0x3165)
  rect(14,38,21,2,0x3165)
  places=[('eiffel',7,31),('notredame',25,31)]
  signs=[('Eiffel',6,37,['EIFFEL TOWER / CHAMP DE MARS','Visitor room: face the south base.','Press A to ask about visiting.','The SEINE lies to the north.']),('NotreDame',24,35,['NOTRE-DAME / ILE DE LA CITE','The cathedral stands on an island.','Undercroft: face the south door.','Press A to ask about visiting.']),('Seine',18,26,['RIVES DE SEINE','Cross the bridges to the LEFT BANK.','Follow the promenade east for','the bridge to NOTRE-DAME.'])]
 else:
  rect(14,22,4,3,0x3165);rect(3,23,34,2,0x3165)
  for x in range(2,38):
   for y in range(25,28):water.add((x,y))
  rect(18,28,18,2,0x3165);rect(24,28,2,10,0x3165)
  rect(3,37,34,3,0x3165);rect(16,30,2,10,0x3165)
  # Tiergarten lawn and formal east/west paths, west of the Gate.
  rect(4,30,9,2,0x3004);rect(4,34,9,2,0x3004);rect(7,28,2,14,0x3165)
  # Cross paths link the Tiergarten beds to the Gate approach.
  rect(4,32,13,1,0x3165);rect(4,36,13,1,0x3165)
  rect(4,30,1,7,0x3165);rect(12,30,1,7,0x3165)
  places=[('reichstag',18,29),('gate',18,34)]
  signs=[('Reichstag',25,31,['REICHSTAG','The SPREE runs north of here.','Visitor archive: face the south door.','Press A to speak to the curator.']),('Gate',25,36,['BRANDENBURG GATE','UNTER DEN LINDEN leads east.','Visitor room: face the west pillar.','Press A from the path to visit.']),('Tiergarten',13,34,['TIERGARTEN','Garden paths west of the GATE.'])]
 for x,y in water:
  l=(x-1,y) in water;r=(x+1,y) in water;u=(x,y-1) in water;d=(x,y+1) in water
  t=0x12b
  if not u:t=0x123 if l and r else 0x122 if not l else 0x124
  elif not d:t=0x131 if l and r else 0x130 if not l else 0x132
  elif not l:t=0x12a
  elif not r:t=0x12c
  a[y][x]=0x1000|t
 if city=='Paris':
  rect(10,27,2,5,0x3165);rect(16,28,2,5,0x3165);rect(26,28,2,3,0x3165);rect(26,36,2,5,0x3165)
 else:
  rect(15,24,3,5,0x3165);rect(30,24,2,5,0x3165)
 blocks=json.loads((R/f'data/geography/{city.lower()}-landmark-blocks.json').read_text())
 for label,x,y in places:
  for dy,row in enumerate(blocks[label]):
   for dx,t in enumerate(row):a[y+dy][x+dx]=(0x3000 if label=='gate' and dx in (2,3) else 0x400)|t
 for _,x,y,_ in signs:a[y][x]=0x402
 for y in range(H):
  for x in range(W):
   if x<2 or x>=W-2 or y>=H-2 or (y<2 and x>=32):a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
 if city=='Berlin':
  # Restore the native northern sign; the three adjacent lane columns stay open.
  a[4][14]=0x402
  # Preserve the old eastern edge, opening only a ground-level street.
  for y in range(H):
   for x in (38,39):a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
  for y in range(25):
   for x in range(40,62):a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
  rect(36,37,26,3,0x3165)
  rect(40,32,22,2,0x3165);rect(47,32,2,9,0x3165);rect(55,32,2,9,0x3165)
  rect(40,40,22,2,0x3165)
  rect(41,34,5,2,0x3004);rect(50,34,4,2,0x3004);rect(58,34,3,2,0x3004)
  # Native residential fronts: fictional supporting buildings, not landmarks.
  pallet=struct.unpack('<480H',(R/'data/layouts/PalletTown/map.bin').read_bytes())
  for bx in (42,50,57):
   for dy in range(5):
    for dx in range(5):a[27+dy][bx+dx]=0x400|(pallet[(3+dy)*24+5+dx]&1023)
  facades=json.loads((R/'data/geography/berlin-facade-blocks.json').read_text())
  for bx,label in [(42,'home'),(50,'library'),(57,'workroom')]:
   for dy,row in enumerate(facades[label]):
    for dx,t in enumerate(row):a[27+dy][bx+dx]=0x400|t
  signs += [('Boulevard',40,36,['UNTER DEN LINDEN APPROACH','West: BRANDENBURG GATE.','East: the residential court.','Use the side lanes to circle it.']),('Court',56,34,['COURTYARD VISITOR ROOMS','West: home. Middle: reading room.','East: the garden workroom.','Face a door and press A to visit.','COURTYARD NOTES','Seed and watering notes: workroom.','Garden log: middle reading room.','Share a memory in the western home.','Return west along the main road.','The GATE visitor room is on the west.'])]
  for _,x,y,_ in signs:a[y][x]=0x402
 if city=='Paris':
  # Retain the former eastern tree boundary, opening a short lane mouth.
  for y in range(H):
   for x in (38,39):a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
  for y in range(32):
   for x in range(40,62):a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
  rect(34,40,28,2,0x3165);rect(40,39,22,2,0x3165)
  for y in (40,41):a[y][37]=0x3010  # Retain the old grass approach.
  rect(49,39,2,5,0x3165);rect(59,39,2,5,0x3165);rect(40,43,22,1,0x3165)
  rect(43,42,5,1,0x3004);rect(54,42,5,1,0x3004)
  pallet=struct.unpack('<480H',(R/'data/layouts/PalletTown/map.bin').read_bytes())
  for bx in (44,54):
   for dy in range(5):
    for dx in range(5):a[34+dy][bx+dx]=0x400|(pallet[(3+dy)*24+5+dx]&1023)
  for y in range(34,37):
   for x in range(54,59):
    t=a[y][x];a[y][x]=(t&0xfc00)|blocks['garden_roof'][str(t&1023)]
  signs += [('Lane',43,41,['PROMENADE SIDE LANE','West: the river and EIFFEL gardens.','The south path circles the flowers.','Both homes welcome visitors.']),('Homes',55,41,['NEIGHBORHOOD HOMES','West: sketches. East: garden room.','Face either door and press A.','Return west for EIFFEL and bridges.'])]
  for _,x,y,_ in signs:a[y][x]=0x402
 original=[r[:] for r in a];forestids={0x14,0x15,0x1c,0x1d}
 def forest(x,y):return x<0 or y<0 or x>=W or y>=H or original[y][x]&1023 in forestids
 for y in range(H):
  for x in range(W):
   t=original[y][x]&1023
   if t not in forestids:continue
   right=t in (0x15,0x1d)
   if t in (0x1c,0x1d) and not forest(x,y-1):t=0xf if right else 0xe
   elif t in (0x14,0x15) and not forest(x,y+1):t=0x25 if right else 0x24
   if t in (0x14,0x1c,0x24) and not forest(x-1,y):t+=2
   if t in (0x15,0x1d,0x25) and not forest(x+1,y):t+=2
   a[y][x]=(original[y][x]&~1023)|t
 from europe_trees import finish_trees
 finish_trees(a)
 (R/f'data/layouts/Europe{city}/map.bin').write_bytes(struct.pack('<%dH'%(W*H),*(v for row in a for v in row)))
 p=R/'data/layouts/layouts.json';j=json.loads(p.read_text())
 for l in j['layouts']:
  if l.get('id')==f'LAYOUT_EUROPE_{city.upper()}':l.update(width=W,height=H,secondary_tileset=f'gTileset_Europe{city}')
 p.write_text(json.dumps(j,indent=2)+'\n')
 p=R/f'data/maps/Europe{city}/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith(f'Europe{city}_Realism')]
 if city=='Berlin':
  j['object_events']=[e for e in j['object_events'] if not e['script'].startswith('EuropeBerlin_Court')]
  for gfx,x,y,label in [('OBJ_EVENT_GFX_WOMAN_1',45,36,'Gardener'),('OBJ_EVENT_GFX_OLD_MAN_1',53,36,'Neighbor'),('OBJ_EVENT_GFX_PIKACHU',54,36,'Pikachu')]:
   j['object_events'].append(dict(type='object',graphics_id=gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script='EuropeBerlin_Court'+label,flag='0'))
 if city=='Paris':
  j['object_events']=[e for e in j['object_events'] if not e['script'].startswith(('EuropeParis_Garden','EuropeParis_Promenade'))]
  for gfx,x,y,label in [('OBJ_EVENT_GFX_WOMAN_2',6,40,'Observer'),('OBJ_EVENT_GFX_PSYDUCK',7,40,'Psyduck')]:
   j['object_events'].append(dict(type='object',graphics_id=gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script='EuropeParis_Garden'+label,flag='0'))
 if city=='Paris':
  j['object_events'].append(dict(type='object',graphics_id='OBJ_EVENT_GFX_GENTLEMAN',x=30,y=42,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script='EuropeParis_PromenadeArtist',flag='0'))
 for suffix,x,y,lines in signs:j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=f'Europe{city}_Realism{suffix}'))
 p.write_text(json.dumps(j,indent=2)+'\n')
 p=R/f'data/maps/Europe{city}/scripts.inc';s=p.read_text();s=s.split(f'\nEurope{city}_Realism')[0]
 for suffix,x,y,lines in signs:
  label=f'Europe{city}_Realism{suffix}';s+=f'\n{label}::\n\tmsgbox {label}Text, MSGBOX_SIGN\n\tend\n\n{label}Text::\n'
  for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\p' if i%2 else '\\n')+'"\n'
 if city=='Berlin':
  for label,lines in [('Gardener',['I tend these flowers with my ODDISH.','Care makes a place feel like home.','The lane south of us loops back','to the BRANDENBURG GATE.']),('Neighbor',['PIKACHU keeps me company here.','All three doors welcome visitors.','West: home. Middle: reading room.','East: the garden workroom.'])]:
   name='EuropeBerlin_Court'+label
   s+=f'\n{name}::\n\tlock\n\tfaceplayer\n\tmsgbox {name}Text, MSGBOX_DEFAULT\n\trelease\n\tend\n\n{name}Text::\n'
   for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\p' if i%2 else '\\n')+'"\n'
 if city=='Berlin':
  s+='\nEuropeBerlin_CourtPikachu::\n\tlock\n\tfaceplayer\n\twaitse\n\tplaymoncry SPECIES_PIKACHU, CRY_MODE_NORMAL\n\tmsgbox EuropeBerlin_CourtPikachuText, MSGBOX_DEFAULT\n\twaitmoncry\n\trelease\n\tend\n\nEuropeBerlin_CourtPikachuText::\n\t.string "PIKACHU: Pika! Pika!$"\n'
 if city=='Paris':
  s+='\nEuropeParis_GardenObserver::\n\tlock\n\tfaceplayer\n\tmsgbox EuropeParis_GardenObserverText, MSGBOX_DEFAULT\n\trelease\n\tend\n\nEuropeParis_GardenObserverText::\n\t.string "PSYDUCK rests beside these flowers.\\n"\n\t.string "I watch quietly and make notes.\\p"\n\t.string "The EIFFEL visitor room has sketches.\\n"\n\t.string "Follow the path north to visit.$"\n'
  s+='\nEuropeParis_GardenPsyduck::\n\tlock\n\tfaceplayer\n\twaitse\n\tplaymoncry SPECIES_PSYDUCK, CRY_MODE_NORMAL\n\tmsgbox EuropeParis_GardenPsyduckText, MSGBOX_DEFAULT\n\twaitmoncry\n\trelease\n\tend\n\nEuropeParis_GardenPsyduckText::\n\t.string "PSYDUCK: Psy? Psyduck!$"\n'
 if city=='Paris':
  s+='\nEuropeParis_PromenadeArtist::\n\tlock\n\tfaceplayer\n\tmsgbox EuropeParis_PromenadeArtistText, MSGBOX_DEFAULT\n\trelease\n\tend\n\nEuropeParis_PromenadeArtistText::\n\t.string "I sketch the river from this bank.\\n"\n\t.string "The light changes as people pass.\\p"\n\t.string "I leave the path clear for walkers.\\n"\n\t.string "A little space lets us all enjoy it.$"\n'
 p.write_text(s)
 print(city,W,H,'landmark district generated')
if __name__=='__main__':
 for city in sys.argv[1:] or ['Paris','Berlin']:build(city)
