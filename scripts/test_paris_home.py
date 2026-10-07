"""Button-input home visits, cancellation, conversations and cold saves."""
import json,struct
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved
from test_gym_ui import open_key_item
from test_navigation import wait_task
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
inside=groups['gMapGroup_Europe'].index('EuropeParisHome')
def read(e,point,label,facing='UP'):
 go(e,point);e.press(facing);e.press('A',180)
 assert e.read('sLockFieldControls',1),label
 e.screenshot(ROOT/f'test-output/paris-home-{label}.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1)
def checkmap(e):
 raw=struct.unpack('<130H',(ROOT/'data/layouts/EuropeParisHome/map.bin').read_bytes())
 w=e.read('VMap');base=e.read(e.symbols['VMap']+8)
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(10) for x in range(13))==raw

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'paris-home-v093',True)
 assert e.location()==(43,inside,9,7);checkmap(e);before=preserved(e)
 read(e,(9,2),'display-old-save');assert preserved(e)==before
 go(e,(4,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,4,45,39)
 print('PASS: v0.93 indoor battery refreshes the display artwork, reads it and exits with progress retained',flush=True)
finally:e.close()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'paris-realism-save',True);before=preserved(e)[1:]
 for choice in ['NO','B']:
  talk(e,(45,39),choice=choice);assert e.location()==(43,4,45,39)
 talk(e,(45,39),choice='YES');assert e.location()==(43,inside,5,7)
 e.screenshot(ROOT/'test-output/paris-home-interior.png')
 read(e,(9,2),'display');read(e,(8,5),'host');read(e,(3,4),'notebook')
 assert not e.read('sLockFieldControls',1) and preserved(e)[1:]==before
 go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,4,45,39)
 talk(e,(45,39),choice='YES');go(e,(9,7));save(e,'paris-home-save');saved=preserved(e)
 print('PASS: home No/B, entry, host, notebook, exit and re-entry preserve progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'paris-home-save',True)
 assert e.location()==(43,inside,9,7) and preserved(e)==saved;checkmap(e)
 open_key_item(e,361);wait_task(e,'Task_EuropeMap');e.frames(60);assert e.read('sEuropeMapCurrent',1)==1
 e.screenshot(ROOT/'test-output/paris-home-map.png')
 e.press('B',180);e.press('B',180);e.press('B',90);assert preserved(e)==saved
 read(e,(3,4),'notebook-reloaded');go(e,(4,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,4,45,39)
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180)
 assert e.location()[:2]==(43,5)
 print('PASS: sketch-room Save/cold Continue, second exit tile and return to countryside',flush=True)
finally:e.close()
