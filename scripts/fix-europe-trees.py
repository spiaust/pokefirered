"""Repair native tree silhouettes on every existing European outdoor layout."""
from pathlib import Path
import json,struct
from europe_trees import finish_trees
R=Path(__file__).resolve().parents[1]
for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']:
 if not l.get('name','').startswith('Europe') or l['primary_tileset']!='gTileset_General':continue
 p=R/l['blockdata_filepath'];w,h=l['width'],l['height'];raw=p.read_bytes();old=struct.unpack('<%dH'%(w*h),raw);a=[list(old[y*w:(y+1)*w]) for y in range(h)];finish_trees(a);new=[v for row in a for v in row]
 assert all((b&~1023)==(n&~1023) for b,n in zip(old,new))
 data=struct.pack('<%dH'%len(new),*new)
 if raw!=data:p.write_bytes(data);print(l['name'])
