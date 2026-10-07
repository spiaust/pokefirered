"""Rooms pages in retained capital saves and existing map/story controls."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved

def task(e):
 base=e.symbols['gTasks'];fn=e.symbols['Task_EuropeMap']&~1
 return next(base+i*40 for i in range(16) if e.read(base+i*40+4,1) and e.read(base+i*40)&~1==fn)
def page(e):return e.read(task(e)+22,2)
def rooms(e):return e.read('sEuropePlacesRooms',1)
def prefs(e):return tuple(e.var(v) for v in (0x40c3,0x40c4,0x40d2,0x40d3,0x40d4))

for city,selection,checkpoint in [('london',0,'london-home-v087'),('paris',1,'paris-home-v093'),('berlin',2,'berlin-court-v098')]:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,checkpoint,True);loc=e.location();before=preserved(e);settings=prefs(e);help_r=e.read('gHelpSystemToggleWithRButtonDisabled',1);help_enabled=e.read('gHelpSystemEnabled',1)
  open_key_item(e,361);wait_task(e,'Task_EuropeMap');e.frames(60);assert not page(e) and not rooms(e) and not e.read('gHelpSystemEnabled',1)
  while e.read('sEuropeMapSelection',1)!=selection:e.press('DOWN',60)
  e.press('L',60);assert not page(e) and not rooms(e)
  e.press('R',60);e.press('L',60);assert page(e) and rooms(e)
  e.screenshot(ROOT/f'test-output/map-rooms-{city}.png')
  e.press('L',60);assert page(e) and not rooms(e)
  e.press('L',60);assert rooms(e)
  e.press('DOWN',60);assert page(e) and not rooms(e)
  e.press('UP',60);e.press('L',60);assert rooms(e)
  e.press('B',60);assert not page(e) and not rooms(e) and e.task_active('Task_EuropeMap')
  for key in ['R','START','A','SELECT']:
   e.press('R',60);e.press('L',60);assert rooms(e)
   e.press(key,60);assert not page(e) and not rooms(e)
   if key=='SELECT':e.press('SELECT',60)
  while e.read('sEuropeMapSelection',1)!=3:e.press('DOWN',60)
  e.press('R',60);e.press('L',60);assert page(e) and not rooms(e)
  e.screenshot(ROOT/f'test-output/map-rooms-noncapital-{city}.png')
  e.press('B',60);e.press('B',180);e.press('B',180);e.press('B',90)
  assert e.location()==loc and preserved(e)==before and prefs(e)==settings and not e.read('sLockFieldControls',1)
  assert e.read('gHelpSystemToggleWithRButtonDisabled',1)==help_r and e.read('gHelpSystemEnabled',1)==help_enabled
  print('PASS: '+city+' retained save Rooms L toggle, stop reset, noncapital fallback, R/B/START/A/story controls and unchanged save state',flush=True)
 finally:e.close()
