"""Author compressed Paris and Berlin landmark districts, preserving hub IDs."""
from pathlib import Path
import json,struct,sys
R=Path(__file__).resolve().parents[1]
def build(city):
 W,H=40,46 if city=='Paris' else 44
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
  signs=[('Eiffel',6,37,['EIFFEL TOWER / CHAMP DE MARS','The SEINE lies to the north.','Garden paths circle the flower beds.','The riverside walk continues east.']),('NotreDame',24,35,['NOTRE-DAME / ILE DE LA CITE','The cathedral stands on an island.','Undercroft: face the south door.','Press A to ask about visiting.']),('Seine',18,26,['RIVES DE SEINE','Cross the bridges to the LEFT BANK.','Follow the promenade east for','the bridge to NOTRE-DAME.'])]
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
  signs=[('Reichstag',25,31,['REICHSTAG','The SPREE runs north of here.','Visitor archive: face the south door.','Press A to speak to the curator.']),('Gate',25,36,['BRANDENBURG GATE','UNTER DEN LINDEN leads east.']),('Tiergarten',13,34,['TIERGARTEN','Garden paths west of the GATE.'])]
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
 for suffix,x,y,lines in signs:j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=f'Europe{city}_Realism{suffix}'))
 p.write_text(json.dumps(j,indent=2)+'\n')
 p=R/f'data/maps/Europe{city}/scripts.inc';s=p.read_text();s=s.split(f'\nEurope{city}_Realism')[0]
 for suffix,x,y,lines in signs:
  label=f'Europe{city}_Realism{suffix}';s+=f'\n{label}::\n\tmsgbox {label}Text, MSGBOX_SIGN\n\tend\n\n{label}Text::\n'
  for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\p' if i%2 else '\\n')+'"\n'
 p.write_text(s)
 print(city,W,H,'landmark district generated')
if __name__=='__main__':
 for city in sys.argv[1:] or ['Paris','Berlin']:build(city)
