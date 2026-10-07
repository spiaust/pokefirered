"""Station signs retain all maps, station staff and existing ticket guidance."""
from pathlib import Path
import re,json,hashlib,subprocess,sys
from rail_compatibility import before_clerk_cues
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,digest in json.loads((R/'data/geography/capital-station-v102.json').read_text()).items():
 raw=(R/path).read_bytes()
 if path=='data/scripts/europe_train.inc':raw=before_clerk_cues(raw)
 if 'Station/' in path:
  city=path.split('/Europe')[1].split('Station/')[0];label=f'Europe{city}Station_LocalBoard'
  if path.endswith('map.json'):
   m=json.loads(raw);m['bg_events']=[e for e in m['bg_events'] if e['script']!=label];raw=(json.dumps(m,indent=2)+chr(10)).encode()
   # Original station files used a mix of LF and CRLF.
   if hashlib.sha256(raw).hexdigest()!=digest:raw=raw.replace(bytes([10]),bytes([13,10]))
  elif path.endswith('scripts.inc'):raw=raw.decode().split(chr(10)+label+'::')[0].encode()
 assert hashlib.sha256(raw).hexdigest()==digest,path
config=json.loads((R/'data/geography/capital-station-signs.json').read_text())
for city,entry in config.items():
 s=(R/f'data/maps/Europe{city}/scripts.inc').read_text();label=f'Europe{city}_Text_Station';start=s.index(label+'::')+len(label)+2;body=s[start:].split(chr(10)+chr(10),1)[0].lstrip(chr(10))+chr(10)
 assert body.startswith(entry['base'].replace('$',chr(92)+'p')) and all(line in body for line in entry['notes'])
 m=json.loads((R/f'data/maps/Europe{city}/map.json').read_text());events=[e for e in m['bg_events'] if e['script']==f'Europe{city}_StationSign'];assert len(events)==1 and (events[0]['x'],events[0]['y'])==(22,11)
print('PASS: station guidance retains exact terrain, events, staff, IDs, train scripts and ticket-office text')
paths=[R/f'data/maps/Europe{city}/scripts.inc' for city in config];before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-capital-station-signs.py')],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
print('PASS: all three station signs regenerate identically')
