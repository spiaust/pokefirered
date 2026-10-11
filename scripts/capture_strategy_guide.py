"""Capture guide illustrations from earned battery saves on the released v3.3 ROM."""
import json,hashlib
from pathlib import Path
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
out=ROOT/'strategy-guide/dist/images';out.mkdir(parents=True,exist_ok=True)
cases={'england':'release-england-badge-one','france':'release-england-badge-two','germany':'release-england-badge-three','celebi':'celebi-forest','refuge':'celebi-refuge-arrived','post':'celebi-refuge-departure','beauvais':'beauvais-directions-checked-in','garden':'beauvaisgarden-realism-save','amiens':'amiens-arrival','rouen':'rouen-arrival','le-havre':'le-havre-arrival','southampton':'southampton-arrival','london-1940':'release-england-london-ending','ending':'release-england-all-accounts','stamps':'current-stamps-complete','gastly':'notredame-gastly-caught','lapras':'expansion-integration-water','archive':'archive-4-5-oxford','chateau':'archive-4-5-town-4','palace':'archive-4-5-town-5','council':'council-england-stage-1'}
records=[]
for label,name in cases.items():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,name,True);e.frames(60);e.screenshot(out/(label+'.png'))
  records.append({'image':label+'.png','source_battery':name+'.sav','location':e.location(),'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest()})
  print('CAPTURE:',label,e.location(),flush=True)
 finally:e.close()
(out/'provenance.json').write_text(json.dumps(records,indent=2)+'\n')
