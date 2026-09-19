"""Compressed Amiens and Rouen districts east of their original quest areas."""
from pathlib import Path
import json,struct
import sys
city=sys.argv[1] if len(sys.argv)>1 else 'Amiens'
assert city in ('Amiens','Rouen')
R=Path(__file__).resolve().parents[1];W,H=(64 if city=='Amiens' else 80),36;ow=24 if city=='Amiens' else 36
old=struct.unpack('<%dH'%(ow*20),(R/f'data/geography/{city.lower()}-v055.bin').read_bytes())
a=[[0x3010]*W for _ in range(H)]
def rect(x,y,w,h,t):
 for yy in range(y,y+h):
  for xx in range(x,x+w):a[yy][xx]=t
for y in range(20):a[y][:ow]=old[y*ow:(y+1)*ow]
rect(ow-2,16,W-ow,4,0x3165)
if city=='Amiens':
 rect(25,8,36,2,0x3165);rect(25,13,36,2,0x3165)
 rect(26,13,3,18,0x3165);rect(52,8,3,23,0x3165)
 rect(25,28,34,3,0x3165);rect(42,15,12,10,0x3165)
 rect(27,3,11,6,0x3165);rect(42,3,13,6,0x3165)
 water={(x,y) for x in range(24,62) for y in range(10,13)}
 water.update((x,y) for x in range(39,42) for y in range(3,10))
 bridges=[(30,9,3,6),(53,9,3,6),(38,6,5,2)]
 places=[('cathedral',43,17),('houses',29,5)]
 signs=[('Cathedral',50,23,["NOTRE-DAME D'AMIENS",'The cathedral above SAINT-LEU.']),('SaintLeu',35,8,['SAINT-LEU','Canals and houses north of the church.']),('Somme',45,13,['SOMME RIVERSIDE','Bridges connect the canal banks.'])]
else:
 rect(39,22,38,2,0x3165);rect(39,30,38,3,0x3165)
 rect(43,20,3,12,0x3165);rect(71,20,3,12,0x3165)
 rect(45,7,12,10,0x3165);rect(60,5,14,14,0x3165)
 rect(52,13,12,3,0x3165)
 water={(x,y) for x in range(36,78) for y in range(25,28)}
 bridges=[(43,24,3,6),(71,24,3,6)]
 places=[('cathedral',64,7),('clock',48,8)]
 signs=[('Cathedral',70,14,['NOTRE-DAME DE ROUEN','The cathedral north of the SEINE.']),('Clock',53,13,['GROS-HORLOGE','The clock west of the cathedral.']),('Seine',60,23,['SEINE QUAYS','Follow the paths along both banks.'])]
for x,y in water:
 l=(x-1,y) in water;r=(x+1,y) in water;u=(x,y-1) in water;d=(x,y+1) in water
 t=0x12b
 if not u:t=0x123 if l and r else 0x122 if not l else 0x124
 elif not d:t=0x131 if l and r else 0x130 if not l else 0x132
 elif not l:t=0x12a
 elif not r:t=0x12c
 a[y][x]=0x1000|t
for x,y,w,h in bridges:rect(x,y,w,h,0x3165)
blocks=json.loads((R/f'data/geography/{city.lower()}-landmark-blocks.json').read_text())
for label,x,y in places:
 for dy,row in enumerate(blocks[label]):
  for dx,t in enumerate(row):a[y+dy][x+dx]=0x400|t
for _,x,y,_ in signs:a[y][x]=0x402
# Complete tree crowns at every exposed forest edge, including the old opening.
for y in range(H):
 for x in range(W):
  if (x>=ow or y>=20) and (x<2 or x>=W-2 or y<2 or y>=H-2):a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
original=[row[:] for row in a];forestids={0xe,0xf,*range(0x14,0x20),*range(0x24,0x28)}
def forest(x,y):return x<0 or y<0 or x>=W or y>=H or original[y][x]&1023 in forestids
for y in range(H):
 for x in range(W):
  if original[y][x]&1023 not in forestids:continue
  right=bool(x%2);t=(0x14 if y%2 else 0x1c)+right
  if not forest(x,y-1):t=0xf if right else 0xe
  elif not forest(x,y+1):t=0x25 if right else 0x24
  if not right and not forest(x-1,y) and t in (0x14,0x1c,0x24):t+=2
  if right and not forest(x+1,y) and t in (0x15,0x1d,0x25):t+=2
  a[y][x]=(original[y][x]&~1023)|t
from europe_trees import finish_trees
finish_trees(a)
(R/f'data/layouts/Europe{city}Past/map.bin').write_bytes(struct.pack('<%dH'%(W*H),*(v for row in a for v in row)))
p=R/'data/layouts/layouts.json';j=json.loads(p.read_text())
for l in j['layouts']:
 if l.get('id')==f'LAYOUT_EUROPE_{city.upper()}_PAST':l.update(width=W,height=H,secondary_tileset=f'gTileset_Europe{city}')
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/f'data/maps/Europe{city}Past/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith(f'Europe{city}Past_Realism')]
for suffix,x,y,lines in signs:j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=f'Europe{city}Past_Realism'+suffix))
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/f'data/maps/Europe{city}Past/scripts.inc';s=p.read_text().split(f'\nEurope{city}Past_Realism')[0]
for suffix,x,y,lines in signs:
 label=f'Europe{city}Past_Realism'+suffix;s+=f'\n{label}::\n\tmsgbox {label}Text, MSGBOX_SIGN\n\tend\n\n{label}Text::\n'
 for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\n')+'"\n'
p.write_text(s)
print(city,'historical district generated; original quest hub retained')
