"""Rental steering, water Continue and shore return on the completed save."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_ride import attendant,ride,steps,dismount,SURF
from test_ferry import sail
from test_country import wait_menu
from test_time import preserved
from test_gym_ui import open_key_item

def decline(e):
 for choice in ['B','NO']:
  before=preserved(e);location=e.location();attendant(e)
  wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();assert preserved(e)==before and e.location()==location and not e.read('gPlayerAvatar',1)&SURF
def reload(e,name,location):
 save(e,name);saved=preserved(e);e.close();e=Emulator(ROOT/'pokefirered.gba')
 load_checkpoint(e,name,True);assert preserved(e)==saved and e.location()==location
 return e

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'walkthrough-riverboat-complete',True);original=preserved(e)[1:]
 cases=tuple(e.var(v) for v in range(0x40C0,0x40C3))
 for city,index in [('Oxford',12),('London',0)]:
  if e.location()[1]!=index:go(e,(24,16));sail(e,index)
  go(e,(26,16));decline(e);before=preserved(e);ride(e)
  assert preserved(e)==before
  e.screenshot(ROOT/f'test-output/walkthrough-lapras-{city}-water.png')
  print('PASS: '+city+' rental No/B declines and free boarding preserve exact party/inventory/progress without adding a Pokemon',flush=True)
  e=reload(e,'walkthrough-lapras-'+city+'-water',(43,index,26,19))
  assert e.read('gPlayerAvatar',1)&SURF
  steps(e,'LEFT',2);assert e.location()==(43,index,24,19)
  steps(e,'RIGHT',2);assert e.location()==(43,index,26,19) and e.read('gPlayerAvatar',1)&SURF
  assert preserved(e)[1:]==original
  print('PASS: '+city+' water save cold Continues with exact state and retained surfing; free steering works',flush=True)
  dismount(e);e.screenshot(ROOT/f'test-output/walkthrough-lapras-{city}-shore.png')
  e.walk('UP',1);e.walk('RIGHT',1);before=preserved(e);ride(e);assert preserved(e)==before
  dismount(e);assert e.location()==(43,index,25,17) and preserved(e)[1:]==original
  print('PASS: '+city+' clear-bank dismount restores walking and repeated rental retains all rewards/progress',flush=True)
 go(e,(24,16));sail(e,12);go(e,(26,16));open_key_item(e,360);e.frames(120)
 assert e.read('gPlayerAvatar',1)&2
 before=preserved(e);ride(e);assert preserved(e)==before and not e.read('gPlayerAvatar',1)&2
 dismount(e);assert not e.read('gPlayerAvatar',1)&(SURF|2)
 print('PASS: Bicycle rider boards rental with exact party and returns to walking on shore',flush=True)
 go(e,(18,14));e=reload(e,'walkthrough-lapras-complete',(43,12,18,14))
 assert not e.read('gPlayerAvatar',1)&SURF
 before=preserved(e);e.press('DOWN');e.press('A',900)
 e.screenshot(ROOT/'test-output/walkthrough-lapras-ada.png')
 for _ in range(160):
  if not e.read('sLockFieldControls',1):break
  e.press('A',90)
 assert preserved(e)==before and preserved(e)[1:]==original and not e.read('sLockFieldControls',1)
 assert tuple(e.var(v) for v in range(0x40C0,0x40C3))==cases
 print('PASS: final shore cold Continue retains walking, all completed activities and repeatable Ada ending',flush=True)
finally:e.close()
