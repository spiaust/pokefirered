"""Compatibility assertions for the London eastern residential extension."""
import struct
def assert_old_london(raw,old_raw,width):
 old=struct.unpack('<1760H',old_raw);new=struct.unpack('<%dH'%(len(raw)//2),raw)
 for i,a in enumerate(old):
  x,y=i%40,i//40;b=new[y*width+x]
  if x in (38,39) and y in (36,37):assert b==0x3165;continue
  assert a&0xfc00==b&0xfc00,(x,y,'collision/elevation')
  if not a&0xc00:
   assert a==b or (x in (36,37) and y in (36,37) and b==0x3165),(x,y,'old walkable terrain')

def assert_london_facade(raw,old_raw):
 """Only the eastern roof may use alternate art; all tile attributes stay."""
 import json
 from pathlib import Path
 r=Path(__file__).resolve().parents[1]
 mapping=json.loads((r/'data/geography/london-landmark-blocks.json').read_text())['reading_roof']
 old=struct.unpack('<2816H',old_raw);new=struct.unpack('<2816H',raw)
 for i,(a,b) in enumerate(zip(old,new)):
  x,y=i%64,i//64
  expected=(a&0xfc00)|mapping[str(a&1023)] if 54<=x<59 and 28<=y<31 else a
  assert b==expected,(x,y,hex(a),hex(b))
