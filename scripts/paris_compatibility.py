"""Retain the original Paris district outside the residential lane mouth."""
import struct
def assert_old_paris(raw,old_raw,width=64):
 old=struct.unpack('<1840H',old_raw);new=struct.unpack('<%dH'%(len(raw)//2),raw)
 for i,a in enumerate(old):
  x,y=i%40,i//40;b=new[y*width+x]
  if x in (38,39) and y in (40,41):assert b==0x3165;continue
  assert a&0xfc00==b&0xfc00,(x,y,'collision/elevation')
  if not a&0xc00:assert a==b,(x,y,'old walkable terrain')

def assert_paris_facade(raw,old_raw):
 import json
 from pathlib import Path
 r=Path(__file__).resolve().parents[1]
 mapping=json.loads((r/'data/geography/paris-landmark-blocks.json').read_text())['garden_roof']
 walls=json.loads((r/'data/geography/paris-landmark-blocks.json').read_text()).get('western_wall',{})
 old=struct.unpack('<2944H',old_raw);new=struct.unpack('<2944H',raw)
 for i,(a,b) in enumerate(zip(old,new)):
  x,y=i%64,i//64
  expected=(a&0xfc00)|mapping[str(a&1023)] if 54<=x<59 and 34<=y<37 else a
  if 44<=x<49 and 37<=y<39 and str(a&1023) in walls:expected=(a&0xfc00)|walls[str(a&1023)]
  assert b==expected,(x,y,hex(a),hex(b))
