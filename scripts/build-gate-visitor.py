"""Append a fictional Gate visitor room without changing the outdoor terrain."""
from pathlib import Path
import json,struct,re
R=Path(__file__).resolve().parents[1]
name='EuropeGateVisitor';lid='LAYOUT_EUROPE_GATE_VISITOR'
p=R/'data/layouts/layouts.json';ls=json.loads(p.read_text())
source=next(l for l in ls['layouts'] if l.get('id')=='LAYOUT_EUROPE_BERLIN_LIBRARY')
l=dict(source,id=lid,name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
d=R/f'data/layouts/{name}';d.mkdir(exist_ok=True)
a=list(struct.unpack('<130H',(R/source['blockdata_filepath']).read_bytes()))
for y in (4,5):
 for x in (6,7):a[y*13+x]=0x3001
# Two side workbenches leave the central passage and front exit clear.
for bx in (2,10):
 for y,row in enumerate([(0x44c,0x44d),(0x454,0x455)]):
  for x,t in enumerate(row):a[(5+y)*13+bx+x]=t
for x in (2,9):
 a[x:x+2]=[0x421,0x422];a[13+x:15+x]=[0x429,0x42a]
(d/'map.bin').write_bytes(struct.pack('<130H',*a))
(d/'border.bin').write_bytes((R/source['border_filepath']).read_bytes())
i=next((i for i,v in enumerate(ls['layouts']) if v.get('id')==lid),None)
if i is None:ls['layouts'].append(l)
else:ls['layouts'][i]=l
p.write_text(json.dumps(ls,indent=2)+'\n')
p=R/'data/maps/map_groups.json';groups=json.loads(p.read_text())
if name not in groups['gMapGroup_Europe']:groups['gMapGroup_Europe'].append(name)
p.write_text(json.dumps(groups,indent=2)+'\n')
m=json.loads((R/'data/maps/EuropeBerlinLibrary/map.json').read_text())
m.update(id='MAP_EUROPE_GATE_VISITOR',name=name,layout=lid,bg_events=[])
labels={'Librarian':'Guide','GardenBook':'GardenPanel','HistoryBook':'CourtPanel'}
for o in m['object_events']:
 label=labels[o['script'].split('_')[-1]];o['script']=name+'_'+label
 if label=='Guide':o['graphics_id']='OBJ_EVENT_GFX_MAN'
for e in m['coord_events']:e['script']=name+'_Exit'
d=R/f'data/maps/{name}';d.mkdir(exist_ok=True);(d/'map.json').write_text(json.dumps(m,indent=2)+'\n')
s=(R/'data/maps/EuropeBerlinLibrary/scripts.inc').read_text().replace('EuropeBerlinLibrary',name).replace('MAP_EUROPE_BERLIN_LIBRARY','MAP_EUROPE_GATE_VISITOR').replace('51, 32','19, 37')
for old,new in labels.items():s=s.replace(name+'_'+old,name+'_'+new)
texts={'Entry':['GATE VISITOR ROOM','Come inside and browse the displays?'],'Guide':['Welcome to our GATE visitor room!','Our walks connect places and people.','The garden lies west of the GATE.','The courtyard rooms lie east.'],'GardenPanel':['A sketch links the garden paths.','Pause beside the flower beds.','Watch which POKEMON visit them,','then leave their shelter undisturbed.'],'CourtPanel':['A map follows the boulevard east.','The courtyard shares books and tools.','Walk the lanes and visit the rooms.','Small acts of care connect neighbors.']}
for label,lines in texts.items():
 text=name+'_'+label+'Text';block=text+'::\n'
 for i,line in enumerate(lines):block+=' .string "'+line+('$' if i==len(lines)-1 else '\\p' if i%2 else '\\n')+'"\n'
 pattern=re.escape(text)+r'::\n(?:[ \t]*\.string[^\n]*\n)+'
 s,n=re.subn(pattern,lambda _:block,s);assert n==1,text
s=s.split(name+'_Catalog::')[0]
(d/'scripts.inc').write_text(s)
p=R/'data/maps/EuropeBerlin/map.json';m=json.loads(p.read_text())
event=dict(type='sign',x=19,y=36,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=name+'_Enter')
i=next((i for i,e in enumerate(m['bg_events']) if e['script']==event['script']),None)
if i is None:m['bg_events'].append(event)
else:m['bg_events'][i]=event
p.write_text(json.dumps(m,indent=2)+'\n')
print('Gate visitor room generated; earlier map IDs retained')
