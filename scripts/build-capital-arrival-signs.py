"""Expand existing capital route signs; preserve their countryside guidance."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
for city,entry in json.loads((R/'data/geography/capital-arrival-signs.json').read_text()).items():
 p=R/f'data/maps/Europe{city}/scripts.inc';lines=p.read_text().splitlines(keepends=True);label=f'Europe{city}_Text_Route::'
 start=next(i for i,line in enumerate(lines) if line.strip()==label)+1;end=start
 while end<len(lines) and lines[end].lstrip().startswith('.string'):end+=1
 body=entry['base'].replace('$',chr(92)+'p')
 for i,line in enumerate(entry['notes']):body+=chr(9)+'.string "'+line+('$' if i==3 else chr(92)+('p' if i%2 else 'n'))+'"'+chr(10)
 p.write_text(''.join(lines[:start])+body+''.join(lines[end:]))
print('Capital arrival signs generated; countryside guidance retained')
