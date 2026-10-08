"""A fictional London Eye visitor gallery with native windows and exhibits."""
from pathlib import Path
import struct,json,re
R=Path(__file__).resolve().parents[1]
name='EuropeLondonEyeGallery';lid='LAYOUT_EUROPE_LONDON_EYE_GALLERY'
p=R/'data/layouts/layouts.json';ls=json.loads(p.read_text())
source=next(l for l in ls['layouts'] if l.get('id')=='LAYOUT_EUROPE_EIFFEL_VISITOR')
l=dict(source,id=lid,name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
d=R/f'data/layouts/{name}';d.mkdir(exist_ok=True)
a=[[0x408]*13 for _ in range(10)]
for y in range(2,9):
 for x in range(1,12):a[y][x]=0x3001
for x in range(1,12):a[0][x]=0x420;a[1][x]=0x428
for x in (2,6,10):
 a[0][x:x+2]=[0x421,0x422];a[1][x:x+2]=[0x429,0x42a]
a[8][3:6]=[0x3012,0x3013,0x3014];a[9][3:6]=[0x41a,0x41b,0x41c]
(d/'map.bin').write_bytes(struct.pack('<130H',*(v for row in a for v in row)))
(d/'border.bin').write_bytes((R/source['border_filepath']).read_bytes())
i=next((i for i,v in enumerate(ls['layouts']) if v.get('id')==lid),None)
if i is None:ls['layouts'].append(l)
else:ls['layouts'][i]=l
p.write_text(json.dumps(ls,indent=2)+'\n')
p=R/'data/maps/map_groups.json';groups=json.loads(p.read_text())
if name not in groups['gMapGroup_Europe']:groups['gMapGroup_Europe'].append(name)
p.write_text(json.dumps(groups,indent=2)+'\n')
m=json.loads((R/'data/maps/EuropeEiffelVisitor/map.json').read_text())
m.update(id='MAP_EUROPE_LONDON_EYE_GALLERY',name=name,layout=lid,region_map_section='MAPSEC_EUROPE_LONDON')
labels={'Guide':'Attendant','GardenExhibit':'GardenPanel','RiverExhibit':'BridgePanel'}
for o,point in zip(m['object_events'],[(6,3),(2,3),(10,3)]):
 label=labels[o['script'].split('_')[-1]];o.update(script=name+'_'+label,x=point[0],y=point[1])
for e in m['coord_events']:e['script']=name+'_Exit'
d=R/f'data/maps/{name}';d.mkdir(exist_ok=True);(d/'map.json').write_text(json.dumps(m,indent=2)+'\n')
s=(R/'data/maps/EuropeEiffelVisitor/scripts.inc').read_text().replace('EuropeEiffelVisitor',name).replace('MAP_EUROPE_EIFFEL_VISITOR','MAP_EUROPE_LONDON_EYE_GALLERY').replace('MAP_EUROPE_PARIS, 9, 37','MAP_EUROPE_LONDON, 29, 29')
for old,new in labels.items():s=s.replace(name+'_'+old,name+'_'+new)
texts={'Entry':['LONDON EYE VISITOR GALLERY','Come inside and browse the displays?'],'Attendant':['Welcome to our riverside gallery!','The SOUTH BANK paths link gardens','and bridges. Look at the displays,','then explore the walks outside.','Leave through the south doorway.','Follow paths north to the square.','Station: east side of the square.','Free clinic: west side of the square.'],'GardenPanel':['A sketch of the SOUTH BANK gardens.','Quiet paths circle the flower beds.','Watch the POKEMON without disturbing','their resting places or the plants.'],'BridgePanel':['A map marks the two river crossings.','Green rails: WESTMINSTER BRIDGE.','Red rails: the southern crossing.','Both connect the riverside walks.']}
for label,lines in texts.items():
 text=name+'_'+label+'Text';block=text+'::\n'
 for i,line in enumerate(lines):block+=' .string "'+line+('$' if i==len(lines)-1 else '\\p' if i%2 else '\\n')+'"\n'
 s,n=re.subn(re.escape(text)+r'::\n(?:[ \t]*\.string[^\n]*\n)+',lambda _:block,s);assert n==1,text
(d/'scripts.inc').write_text(s)
p=R/'data/maps/EuropeLondon/map.json';m=json.loads(p.read_text())
event=dict(type='sign',x=29,y=28,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=name+'_Enter')
i=next((i for i,e in enumerate(m['bg_events']) if e['script']==event['script']),None)
if i is None:m['bg_events'].append(event)
else:m['bg_events'][i]=event
p.write_text(json.dumps(m,indent=2)+'\n')
print('London Eye gallery generated; earlier maps retained')
