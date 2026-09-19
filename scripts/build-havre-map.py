"""Historical Le Havre: Notre-Dame, Saint-Francois and the old harbor basins."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1];W,H=64,40;name='LeHavrePast'
old=struct.unpack('<221H',(R/'data/geography/le-havre-v056.bin').read_bytes())
a=[[0x052b]*W for _ in range(H)]
def rect(x,y,w,h,t):
 for yy in range(y,y+h):
  for xx in range(x,x+w):a[yy][xx]=t
# An urban island of quays: Commerce north, Roy between the old quarters,
# Notre-Dame west and Maison de l'Armateur in Saint-Francois to the east.
rect(20,2,42,32,0x3165)
rect(24,5,4,7,0x3010);rect(23,15,4,4,0x3010)
water={(x,y) for x in range(32,59) for y in range(6,11)}
water.update((x,y) for x in range(39,45) for y in range(15,27))
water.update((x,y) for x in range(41,44) for y in range(27,H))
water.update((x,y) for x in range(59,W) for y in range(8,10))
for x,y in water:
 l=(x-1,y) in water;r=(x+1,y) in water;u=(x,y-1) in water;d=(x,y+1) in water
 t=0x12b
 if not u:t=0x123 if l and r else 0x122 if not l else 0x124
 elif not d:t=0x131 if l and r else 0x130 if not l else 0x132
 elif not l:t=0x12a
 elif not r:t=0x12c
 a[y][x]=0x1000|t
# One compressed quay crossing; walk round the south end as an alternate route.
rect(38,18,8,2,0x3165)
rect(40,29,5,2,0x3165)
# Retain the terminal, then widen only the blocked edge behind the worker.
for y in range(13):a[y][:17]=old[y*17:(y+1)*17]
# Pass behind the dockworker without moving this existing quest character.
rect(10,4,2,1,0x3282)
rect(17,3,5,1,0x3165)
blocks=json.loads((R/'data/geography/lehavrepast-landmark-blocks.json').read_text())
for label,x,y in [('church',28,23),('house',51,23)]:
 for dy,row in enumerate(blocks[label]):
  for dx,t in enumerate(row):a[y+dy][x+dx]=0x400|t
signs=[('Church',34,27,['NOTRE-DAME CHURCH','The old church west of BASSIN DU ROY.']),('House',56,28,["MAISON DE L'ARMATEUR",'A tall house in SAINT-FRANCOIS.']),('Commerce',45,12,['BASSIN DU COMMERCE','Walk around the old harbor basin.']),('Roy',46,21,['BASSIN DU ROY','Quays link the two old quarters.'])]
for _,x,y,_ in signs:a[y][x]=0x402
from europe_trees import finish_trees
finish_trees(a)
(R/'data/layouts/EuropeLeHavrePast/map.bin').write_bytes(struct.pack('<%dH'%(W*H),*(v for row in a for v in row)))
p=R/'data/layouts/layouts.json';j=json.loads(p.read_text())
for l in j['layouts']:
 if l.get('id')=='LAYOUT_EUROPE_LE_HAVRE_PAST':l.update(width=W,height=H,secondary_tileset='gTileset_EuropeLeHavrePast')
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeLeHavrePast/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith('EuropeLeHavrePast_Realism')]
for suffix,x,y,lines in signs:j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeLeHavrePast_Realism'+suffix))
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeLeHavrePast/scripts.inc';s=p.read_text().split('\nEuropeLeHavrePast_Realism')[0]
for suffix,x,y,lines in signs:
 label='EuropeLeHavrePast_Realism'+suffix;s+=f'\n{label}::\n\tmsgbox {label}Text, MSGBOX_SIGN\n\tend\n\n{label}Text::\n'
 for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\n')+'"\n'
p.write_text(s)
print('Le Havre 64x40 historic harbor generated; original terminal retained')
