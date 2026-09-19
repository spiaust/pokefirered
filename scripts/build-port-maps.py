"""Extend the existing ferry terminals into compressed coastal districts."""
from pathlib import Path
import json,struct,sys
R=Path(__file__).resolve().parents[1]
def build(city):
 name=city+'Port';W,H=56,40
 original=(R/'data/layouts/Island_Harbor/map.bin').read_bytes()
 old=struct.unpack('<221H',original)
 a=[[0x052b]*W for _ in range(H)]
 def rect(x,y,w,h,t):
  for yy in range(y,y+h):
   for xx in range(x,x+w):a[yy][xx]=t
 if city=='Dover':
  rect(17,2,37,22,0x3010)
  rect(18,3,3,21,0x3165);rect(20,18,34,3,0x3165)
  rect(24,21,30,3,0x3165);rect(24,24,3,10,0x3165)
  rect(27,31,12,3,0x3165) # western harbor arm, open to the southeast
  rect(36,4,12,10,0x3165);rect(39,13,3,8,0x3165)
  rect(43,11,11,3,0x3165);rect(52,11,2,10,0x3165)
  rect(44,17,8,7,0x052b) # chalk face meets the sea below the cliff path
  places=[('castle',38,6),('cliffs',44,14)]
  signs=[('Castle',44,12,['DOVER CASTLE','The Great Tower above the harbor.']),('Cliffs',53,18,['WHITE CLIFFS OF DOVER','Chalk cliffs above the CHANNEL.']),('Harbor',29,22,['DOVER SEAFRONT','Follow the quay to the ferry.'])]
 else:
  rect(20,9,34,29,0x3010)
  rect(20,9,34,3,0x3165);rect(22,3,2,34,0x3165)
  rect(24,16,28,3,0x3165);rect(35,18,3,18,0x3165)
  rect(30,23,15,12,0x3165);rect(40,11,10,6,0x3165)
  rect(25,28,4,5,0x3004);rect(46,28,5,5,0x3004)
  # A northern beach promenade, lighthouse in the maritime quarter, hall south.
  rect(24,8,17,1,0x3165);rect(50,5,3,12,0x3165)
  places=[('hall',34,25),('lighthouse',44,11)]
  signs=[('Hall',40,30,['CALAIS TOWN HALL / BELFRY','The red-brick civic landmark.']),('Lighthouse',47,16,['CALAIS LIGHTHOUSE','Above the COURGAIN MARITIME.']),('Seafront',30,11,['CALAIS SEAFRONT','The CHANNEL lies to the north.'])]
 # Original terminal and every old save coordinate remain byte-identical.
 for y in range(13):a[y][:17]=old[y*17:(y+1)*17]
 rect(17,3,7,1,0x3165)
 blocks=json.loads((R/f'data/geography/{name.lower()}-landmark-blocks.json').read_text())
 for label,x,y in places:
  for dy,row in enumerate(blocks[label]):
   for dx,t in enumerate(row):a[y+dy][x+dx]=0x400|t
 for _,x,y,_ in signs:a[y][x]=0x402
 dest=R/f'data/layouts/Europe{name}';dest.mkdir(exist_ok=True)
 from europe_trees import finish_trees
 finish_trees(a)
 (dest/'map.bin').write_bytes(struct.pack('<%dH'%(W*H),*(v for row in a for v in row)))
 (dest/'border.bin').write_bytes(struct.pack('<4H',*[0x052b]*4))
 p=R/'data/layouts/layouts.json';j=json.loads(p.read_text());id=f'LAYOUT_EUROPE_{city.upper()}_PORT'
 l=dict(id=id,name=f'Europe{name}_Layout',width=W,height=H,border_width=2,border_height=2,primary_tileset='gTileset_General',secondary_tileset=f'gTileset_Europe{name}',border_filepath=f'data/layouts/Europe{name}/border.bin',blockdata_filepath=f'data/layouts/Europe{name}/map.bin')
 found=next((i for i,v in enumerate(j['layouts']) if v.get('id')==id),None)
 if found is None:j['layouts'].append(l)
 else:j['layouts'][found]=l
 p.write_text(json.dumps(j,indent=2)+'\n')
 p=R/f'data/maps/Europe{name}/map.json';j=json.loads(p.read_text());j['layout']=id
 j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith(f'Europe{name}_Realism')]
 for suffix,x,y,lines in signs:j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=f'Europe{name}_Realism{suffix}'))
 p.write_text(json.dumps(j,indent=2)+'\n')
 p=R/f'data/maps/Europe{name}/scripts.inc';s=p.read_text().split(f'\nEurope{name}_Realism')[0]
 for suffix,x,y,lines in signs:
  label=f'Europe{name}_Realism{suffix}';s+=f'\n{label}::\n\tmsgbox {label}Text, MSGBOX_SIGN\n\tend\n\n{label}Text::\n'
  for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\n')+'"\n'
 p.write_text(s);print(city,W,H,'coast generated; original terminal retained')
if __name__=='__main__':
 for city in sys.argv[1:] or ['Dover','Calais']:build(city)
