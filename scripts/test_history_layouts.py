"""Historical map save-position and GBA buffer checks."""
from pathlib import Path
import json,struct,sys
R=Path(__file__).resolve().parents[1]
layouts={v.get('id'):v for v in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
maps=[json.loads(p.read_text()) for p in (R/'data/maps').glob('Europe*/map.json')]
for id in ['LAYOUT_EUROPE_CHANTILLY_PAST','LAYOUT_EUROPE_CHANTILLY_PAST_POST','LAYOUT_EUROPE_BEAUVAIS_GARDEN']:
 assert sum(m['layout']==id for m in maps)==1,('historical scenery must not leak through shared layouts',id)
for city in sys.argv[1:] or ['ChantillyPost','Beauvais']:
 id,source,ow,oh,oldset,newset=(('LAYOUT_EUROPE_CHANTILLY_PAST_POST','chantilly-post-v054.bin',56,32,'europe_chantilly','europe_chantillypost') if city=='ChantillyPost' else ('LAYOUT_EUROPE_BEAUVAIS_GARDEN','beauvais-garden-v054.bin',24,20,'pallet_town','europe_beauvais'))
 l=layouts[id];w,h=l['width'],l['height'];old=struct.unpack('<%dH'%(ow*oh),(R/'data/geography'/source).read_bytes());new=struct.unpack('<%dH'%(w*h),(R/l['blockdata_filepath']).read_bytes())
 primary=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()
 attrs=primary+(R/f'data/tilesets/secondary/{newset}/metatile_attributes.bin').read_bytes()
 prior=primary+(R/f'data/tilesets/secondary/{oldset}/metatile_attributes.bin').read_bytes()
 for i,b in enumerate(old):
  if b&0xc00 or b>>12==1:continue # no riding/surfing is allowed on these maps
  n=new[(i//ow)*w+i%ow]
  assert not n&0xc00 and n>>12==b>>12,(city,i,b,n)
  assert struct.unpack_from('<I',prior,(b&1023)*4)[0]&511==struct.unpack_from('<I',attrs,(n&1023)*4)[0]&511,(city,i,'behavior')
 assert (w+15)*(h+14)<=0x2800 and max(b&1023 for b in new)<len(attrs)//4
 print(f'PASS: {city} all prior on-foot save coordinates retain elevation/behavior and map fits hardware')
