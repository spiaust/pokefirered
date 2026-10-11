"""Capture guide illustrations from earned battery saves on the released v3.3 ROM."""
import json,hashlib
from pathlib import Path
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
out=ROOT/'strategy-guide/dist/images';out.mkdir(parents=True,exist_ok=True)
cases={'bicycle':'current-bicycle-riding','riverboat':'current-riverboat-0','dover':'current-coast-27-ferry','calais':'current-coast-28-ferry','notredame':'current-landmarks-notredame-active','westminster':'current-landmarks-westminster-active','reichstag':'current-landmarks-reichstag-active','home':'current-rooms-London','reading':'current-interiors-London-reading','amiens-bridge':'amiens-bridge-west','rouen-bridge':'rouen-arrival','london-bridge':'london-past-bridge-westminster','southampton-quay':'southampton-quay-tip'}
records=json.loads((out/'provenance.json').read_text())
for label,name in cases.items():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,name,True);e.frames(60);e.screenshot(out/(label+'.png'))
  records.append({'image':label+'.png','source_battery':name+'.sav','location':e.location(),'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest()})
  print('CAPTURE:',label,e.location(),flush=True)
 finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 from test_country import start_new_game
 start_new_game(e);e.screenshot(out/'country-menu.png')
 records.append({'image':'country-menu.png','source':'native NEW GAME country menu','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest()})
finally:e.close()
(out/'provenance.json').write_text(json.dumps(records,indent=2)+'\n')
