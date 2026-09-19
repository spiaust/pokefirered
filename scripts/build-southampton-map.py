"""Historical Southampton: Bargate, Tudor House, western walls and Town Quay."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1];W,H=64,40;name='SouthamptonPast'
old=struct.unpack('<221H',(R/'data/geography/southampton-v057.bin').read_bytes())
a=[[0x052b]*W for _ in range(H)]
def rect(x,y,w,h,t):
 for yy in range(y,y+h):
  for xx in range(x,x+w):a[yy][xx]=t
# Bargate north, High Street south to Town Quay, wall walk to the west.
rect(22,2,40,33,0x3010)
rect(22,3,40,2,0x3165)
rect(40,4,12,7,0x3165)
rect(44,9,3,26,0x3165)
rect(23,6,3,27,0x3165)
rect(28,10,3,23,0x3165)
rect(25,20,23,2,0x3165) # compressed Blue Anchor Lane
rect(29,22,9,6,0x3165)
rect(22,32,40,3,0x3165) # Town Quay and southern waterfront
rect(48,35,3,4,0x3165)
rect(31,16,5,4,0x3004)
rect(47,14,12,2,0x3165);rect(56,14,3,20,0x3165)
# Retain the terminal, then widen only the blocked edge behind the worker.
for y in range(13):a[y][:17]=old[y*17:(y+1)*17]
# Bypass the luggage worker and London clerk without moving either.
rect(10,5,2,1,0x3282)
rect(11,4,1,1,0x3282)
rect(17,3,6,1,0x3165)
blocks=json.loads((R/'data/geography/southamptonpast-landmark-blocks.json').read_text())
for label,x,y in [('bargate',42,5),('tudor',31,23),('wall',26,10),('wall',26,16),('wall',26,24)]:
 for dy,row in enumerate(blocks[label]):
  for dx,t in enumerate(row):a[y+dy][x+dx]=0x400|t
signs=[('Bargate',49,9,['BARGATE','The northern gate of the old town.']),('Tudor',37,27,['TUDOR HOUSE','Timber framing beside the old lanes.']),('Walls',28,15,['WESTERN TOWN WALLS','Follow the lane towards TOWN QUAY.']),('Quay',51,33,['TOWN QUAY','The waterfront south of HIGH STREET.'])]
for _,x,y,_ in signs:a[y][x]=0x402
from europe_trees import finish_trees
finish_trees(a)
(R/'data/layouts/EuropeSouthamptonPast/map.bin').write_bytes(struct.pack('<%dH'%(W*H),*(v for row in a for v in row)))
p=R/'data/layouts/layouts.json';j=json.loads(p.read_text())
for l in j['layouts']:
 if l.get('id')=='LAYOUT_EUROPE_SOUTHAMPTON_PAST':l.update(width=W,height=H,secondary_tileset='gTileset_EuropeSouthamptonPast')
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeSouthamptonPast/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith('EuropeSouthamptonPast_Realism')]
for suffix,x,y,lines in signs:j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeSouthamptonPast_Realism'+suffix))
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeSouthamptonPast/scripts.inc';s=p.read_text().split('\nEuropeSouthamptonPast_Realism')[0]
for suffix,x,y,lines in signs:
 label='EuropeSouthamptonPast_Realism'+suffix;s+=f'\n{label}::\n\tmsgbox {label}Text, MSGBOX_SIGN\n\tend\n\n{label}Text::\n'
 for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\n')+'"\n'
p.write_text(s)
print('Southampton 64x40 old town generated; original terminal retained')
