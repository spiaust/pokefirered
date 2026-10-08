"""Append a fictional compact Eiffel visitor room with stable older map IDs."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
name='EuropeEiffelVisitor';lid='LAYOUT_EUROPE_EIFFEL_VISITOR'
p=R/'data/layouts/layouts.json';ls=json.loads(p.read_text())
source=next(l for l in ls['layouts'] if l.get('id')=='LAYOUT_EUROPE_BERLIN_LIBRARY')
l=dict(source,id=lid,name=name+'_Layout',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
d=R/f'data/layouts/{name}';d.mkdir(exist_ok=True)
for key in ('border_filepath','blockdata_filepath'):(R/l[key]).write_bytes((R/source[key]).read_bytes())
i=next((i for i,v in enumerate(ls['layouts']) if v.get('id')==lid),None)
if i is None:ls['layouts'].append(l)
else:ls['layouts'][i]=l
p.write_text(json.dumps(ls,indent=2)+'\n')
p=R/'data/maps/map_groups.json';groups=json.loads(p.read_text())
if name not in groups['gMapGroup_Europe']:groups['gMapGroup_Europe'].append(name)
p.write_text(json.dumps(groups,indent=2)+'\n')
m=json.loads((R/'data/maps/EuropeBerlinLibrary/map.json').read_text())
m.update(id='MAP_EUROPE_EIFFEL_VISITOR',name=name,layout=lid,region_map_section='MAPSEC_EUROPE_PARIS',music='MUS_PEWTER')
labels={'Librarian':'Guide','GardenBook':'GardenExhibit','HistoryBook':'RiverExhibit'}
for o in m['object_events']:
 label=labels[o['script'].split('_')[-1]];o['script']=name+'_'+label
 if label=='Guide':o['graphics_id']='OBJ_EVENT_GFX_WOMAN_2'
for e in m['coord_events']:e['script']=name+'_Exit'
d=R/f'data/maps/{name}';d.mkdir(exist_ok=True);(d/'map.json').write_text(json.dumps(m,indent=2)+'\n')
s=(R/'data/maps/EuropeBerlinLibrary/scripts.inc').read_text().replace('EuropeBerlinLibrary',name).replace('MAP_EUROPE_BERLIN_LIBRARY','MAP_EUROPE_EIFFEL_VISITOR').replace('MAP_EUROPE_BERLIN, 51, 32','MAP_EUROPE_PARIS, 9, 37')
for old,new in labels.items():s=s.replace(name+'_'+old,name+'_'+new)
texts={'Entry':['EIFFEL VISITOR ROOM','Step inside and browse the exhibits?'],'Guide':['Welcome to our visitor room!','The garden and river are nearby.','Our exhibits show how field notes','begin with careful observation.','Leave through the south doorway.','Follow paths north to the square.','Station: east side of the square.','Free clinic: west side of the square.'],'GardenExhibit':['A sketch of the CHAMP DE MARS.','Watch a patch of flowers quietly.','Which POKEMON visit? When do they','rest? Leave their shelter undisturbed.'],'RiverExhibit':['A sketch follows the SEINE east.','Record what you see along the banks.','Cross by the bridges and keep the','water and riverside paths clean.']}
for label,lines in texts.items():
 text=name+'_'+label+'Text';block=text+'::\n'
 for i,line in enumerate(lines):block+=' .string "'+line+('$' if i==len(lines)-1 else '\\p' if i%2 else '\\n')+'"\n'
 s,n=re.subn(re.escape(text)+r'::\n(?:[ \t]*\.string[^\n]*\n)+',lambda _:block,s);assert n==1,text
(d/'scripts.inc').write_text(s)
p=R/'data/maps/EuropeParis/map.json';m=json.loads(p.read_text())
event=dict(type='sign',x=9,y=36,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=name+'_Enter')
i=next((i for i,e in enumerate(m['bg_events']) if e['script']==event['script']),None)
if i is None:m['bg_events'].append(event)
else:m['bg_events'][i]=event
p.write_text(json.dumps(m,indent=2)+'\n')
print('Eiffel visitor room generated; older map IDs retained')
