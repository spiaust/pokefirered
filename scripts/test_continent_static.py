"""Check continental content, native capacities, reachability, and saved-state allocations."""
from pathlib import Path
from collections import deque
import json,re,struct
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'data/continent-campaign.json').read_text())['countries'];G=json.loads((R/'data/maps/map_groups.json').read_text());L={x.get('id'):x for x in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
assert len(D)==39 and len(G['gMapGroup_Continent'])==78
assert len(json.loads((R/'src/data/region_map/region_map_sections.json').read_text())['map_sections'])<253
assert not any(d['country']=='USA' for d in D)
assert {'Poland','Russia','Ukraine','Belarus','Norway','Denmark','Finland','Hungary','Romania','Bulgaria','Slovakia','Serbia','Croatia','Slovenia','Bosnia','Albania','Montenegro','N Macedonia','Estonia','Latvia','Lithuania','Malta'} <= {d['country'] for d in D}
hashes=set()
for n in G['gMapGroup_Continent']:
 m=json.loads((R/f'data/maps/{n}/map.json').read_text());l=L[m['layout']];w,h=l['width'],l['height'];blob=(R/l['blockdata_filepath']).read_bytes();a=struct.unpack('<%dH'%(w*h),blob)
 if not n.endswith('Past'):hashes.add(blob)
 assert len(m['object_events'])<=16
 assert sum(o['script']=='Shadow_Storage' for o in m['object_events'])==1,(n,'storage attendant missing')
 blocked={(o['x'],o['y']) for o in m['object_events']};start=(15,30);q=deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  for z in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   xx,yy=z
   if 0<=xx<w and 0<=yy<h and z not in blocked and z not in seen and not a[yy*w+xx]&0xc00 and a[yy*w+xx]&1023!=0x12b:seen.add(z);q.append(z)
 for o in m['object_events']:
  x,y=o['x'],o['y'];assert (x,y+1) in seen,(n,o['script'],'south approach blocked')
 for o in m['bg_events']:assert (o['x'],o['y']+1) in seen,(n,'landmark inaccessible')
assert len(hashes)==39,'countries must have independent geography'
s=(R/'src/data/trainers.h').read_text(encoding='utf8');ids=[int(x) for x in re.findall(r'^\s*\[(\d+)\]',s,re.M)];assert len(ids)==len(set(ids));assert set(range(100,376))<=set(ids)
s=(R/'data/scripts/shadow_campaign.inc').read_text();labels=re.findall(r'^(\w+)::',s,re.M);assert len(labels)==len(set(labels)),'duplicate scripts'
for n in G['gMapGroup_Continent']:
 for o in json.loads((R/f'data/maps/{n}/map.json').read_text())['object_events']:assert o['script'] in labels
font=(R/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(encoding='utf8'),re.M)};chars["'"]=0xb4
for t in re.findall(r'\.string "([^"\n]+)"',s):
 t=re.sub(r'\{(?:RIVAL|PLAYER)\}','WWWWWWW',t);t=t.replace('{STR_VAR_1}','39')
 for line in re.split(r'\\[npl]|\$',t):
  width=sum(widths[chars[c]] for c in line);assert width<=216,(width,line)
print('PASS: 39 independent city layouts, 78 era maps, 276 unique trainers, all event approaches reachable, and native text fits.')

# Every weighted visible species has a native sprite mapping; none are silently dropped.
wild=json.loads((R/'src/data/wild_encounters.json').read_text())
entries=[x for x in wild['wild_encounter_groups'][0]['encounters'] if x['map'].startswith(('MAP_SHADOW_','MAP_CONTINENT_'))]
encounter_species={m['species'] for x in entries for m in x.get('land_mons',{}).get('mons',[])}
field=(R/'src/wild_encounter.c').read_text()
for species in encounter_species:assert re.search(r'case '+species+r': return OBJ_EVENT_GFX_',field),species
assert len(entries)==99
print('PASS: all 99 new encounter tables retain weighted species with native sprite coverage.')
