"""Add east-side landmark districts, preserving each town's southern route edge."""
from pathlib import Path
import json,struct,sys
R=Path(__file__).resolve().parents[1]
def build(city):
 W,H=(72 if city=='Chantilly' else 64),24
 old=struct.unpack('<768H',(R/f'data/geography/{city.lower()}-v051.bin').read_bytes())
 a=[[0x3010 for x in range(W)] for y in range(H)]
 for y in range(H):a[y][:32]=old[y*32:(y+1)*32]
 def rect(x,y,w,h,t):
  for yy in range(y,y+h):
   for xx in range(x,x+w):a[yy][xx]=t
 def waterbox(x,y,w,h):water.update((xx,yy) for yy in range(y,y+h) for xx in range(x,x+w))
 # Remove the former eastern forest wall so the town joins its new district.
 rect(30,2,2,20,0x3010)
 rect(28,12,W-30,4,0x3165)
 water=set();bridges=[]
 if city=='Oxford':
  # Radcliffe Square north of the High; Magdalen at the eastern river crossing.
  rect(34,4,9,8,0x3165);rect(37,10,3,3,0x3165)
  rect(47,4,8,8,0x3165);rect(52,15,2,6,0x3165)
  rect(43,18,11,2,0x3165);rect(44,16,5,2,0x3004)
  for y in range(2,22):
   left=56 if y<18 else 55
   waterbox(left,y,3,1)
  bridges=[(54,12,8,2),(53,19,8,2)]
  places=[('camera',36,6),('magdalen',50,6)]
  signs=[('Radcliffe',41,10,['RADCLIFFE SQUARE','The domed RADCLIFFE CAMERA library.']),('Magdalen',53,11,['MAGDALEN TOWER / HIGH STREET','MAGDALEN BRIDGE crosses the CHERWELL.']),('Meadow',46,20,['CHERWELL MEADOW PATH','Follow the river back to HIGH STREET.'])]
 elif city=='Chantilly':
  # Chateau island with a moat; the Great Stables lie to the southwest.
  waterbox(47,4,10,9)
  for y in range(5,12):
   for x in range(48,56):water.discard((x,y));a[y][x]=0x3165
  rect(33,15,10,6,0x3165);rect(43,17,24,2,0x3165)
  rect(58,5,2,13,0x3165);rect(67,5,2,13,0x3165)
  rect(59,6,8,2,0x3004);rect(59,10,8,2,0x3004)
  rect(62,5,2,12,0x3165);waterbox(59,3,9,2)
  bridges=[(50,11,2,5)]
  places=[('chateau',49,6),('stables',35,16)]
  signs=[('Chateau',53,14,['CHATEAU DE CHANTILLY','Cross the moat to the chateau court.']),('Stables',41,19,['GRANDES ECURIES','The estate\'s historic Great Stables.']),('Gardens',65,13,['FORMAL GARDENS / GRAND CANAL','Paths follow the garden axes.'])]
 else:
  # Schloss west of the Havel, formal park farther west, public forecourt south.
  rect(43,5,10,10,0x3165);rect(33,3,10,2,0x3165)
  rect(33,9,10,2,0x3165);rect(36,4,2,8,0x3165)
  rect(40,4,2,8,0x3165);rect(33,6,3,2,0x3004)
  rect(38,6,2,2,0x3004);rect(52,3,2,18,0x3165)
  rect(33,19,21,2,0x3165);waterbox(55,2,3,20)
  bridges=[(53,12,9,2),(53,19,9,2)]
  places=[('palace',44,6)]
  signs=[('Palace',49,11,['SCHLOSS ORANIENBURG','The palace faces SCHLOSSPLATZ.']),('Park',39,10,['SCHLOSSPARK','Garden paths west of the palace.']),('Havel',58,16,['HAVEL RIVERSIDE','Cross the bridges to SCHLOSSPLATZ.'])]
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
   for dx,t in enumerate(row):
    courtyard=label=='palace' and dy==3 and 2<=dx<=5
    a[y+dy][x+dx]=(0x3000 if courtyard else 0x400)|t
 for _,x,y,_ in signs:a[y][x]=0x402
 for y in range(H):
  for x in range(32,W):
   if x>=W-2 or y<2 or y>=H-2:a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
 # Re-cap forest along the new street opening, including existing side variants.
 original=[r[:] for r in a];forestids={0xe,0xf,*range(0x14,0x20),*range(0x24,0x28)}
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
  for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\n')+'"\n'
 p.write_text(s)
 print(city,W,H,'east district generated; original south connection retained')
if __name__=='__main__':
 for city in sys.argv[1:] or ['Oxford','Chantilly','Oranienburg']:build(city)

