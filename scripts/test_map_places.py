"""Places browsing, map/story controls and unchanged saves through real input."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved

def task(e):
 base=e.symbols['gTasks'];fn=e.symbols['Task_EuropeMap']&~1
 return next(base+i*40 for i in range(16) if e.read(base+i*40+4,1) and e.read(base+i*40)&~1==fn)
def page(e):return e.read(task(e)+22,2)
def prefs(e):return tuple(e.var(v) for v in (0x40c3,0x40c4,0x40d2,0x40d3,0x40d4))
for checkpoint,past in [('world-options-custom',False),('london-past-arrival',True)]:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,checkpoint,True);loc=e.location();before=preserved(e);settings=prefs(e);help_r=e.read('gHelpSystemToggleWithRButtonDisabled',1)
  open_key_item(e,361);wait_task(e,'Task_EuropeMap');e.frames(60);assert not page(e)
  assert bool(e.read('sEuropeMapPast',1))==past
  assert e.read('gHelpSystemToggleWithRButtonDisabled',1)==1
  e.press('R',60);assert page(e)==1
  initial=e.read('sEuropeMapSelection',1)
  for i in range(8):
   selection=(initial+i)%8;assert e.read('sEuropeMapSelection',1)==selection and page(e)==1
   if selection in (0,1,2,6):e.screenshot(ROOT/f'test-output/map-places-{checkpoint}-{selection}.png')
   e.press('DOWN',60)
  assert e.read('sEuropeMapSelection',1)==initial
  e.press('LEFT',60);assert e.read('sEuropeMapSelection',1)==(initial+7)%8
  e.press('RIGHT',60);assert e.read('sEuropeMapSelection',1)==initial
  e.press('R',60);assert not page(e)
  e.press('R',60);e.press('B',60);assert not page(e) and e.task_active('Task_EuropeMap')
  e.press('R',60);e.press('START',60);assert not page(e) and e.task_active('Task_EuropeMap')
  e.press('R',60);e.press('A',60);assert not page(e)
  e.press('R',60);e.press('SELECT',60);assert not page(e) and e.read(task(e)+10,2)==1
  e.press('R',60);assert not page(e) and e.read(task(e)+10,2)==1
  e.press('SELECT',60);assert e.read(task(e)+10,2)==0
  e.screenshot(ROOT/f'test-output/map-places-return-{checkpoint}.png')
  e.press('B',180);e.press('B',180);e.press('B',90)
  assert e.location()==loc and preserved(e)==before and prefs(e)==settings and not e.read('sLockFieldControls',1)
  assert e.read('gHelpSystemToggleWithRButtonDisabled',1)==help_r
  print('PASS: '+checkpoint+' Places eight-stop wrap, R/B/START/A/story controls and unchanged party/progress/preferences/location',flush=True)
 finally:e.close()
