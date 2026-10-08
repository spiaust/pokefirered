"""Both present-day coach/ferry routes after story, cases and stamps."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_coast import coach,prompt,accept,leave_port
from test_tour import travel
from test_time import preserved
from test_gym_ui import open_key_item
from test_navigation import wait_task

def town(e,dest):
 go(e,(16,14))
 if e.location()[1]!=dest*4:travel(e,dest)
def decline(e,port=False):
 for choice in ['B','NO']:
  before=preserved(e);location=e.location();prompt(e,port)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();assert preserved(e)==before and e.location()==location
def reload(e,name,location):
 save(e,name);saved=preserved(e);e.close();e=Emulator(ROOT/'pokefirered.gba')
 load_checkpoint(e,name,True);assert preserved(e)==saved and e.location()==location
 return e
def check_map(e,port):
 before=preserved(e);open_key_item(e,361);wait_task(e,'Task_EuropeMap')
 assert e.read('sEuropeMapCurrent',1)==port-21 and e.read('sEuropeMapSelection',1)==port-21
 assert not e.read('sEuropeMapPast',1)
 e.screenshot(ROOT/f'test-output/walkthrough-coast-{port}-map.png')
 e.press('B',180);e.press('B',180);e.press('B',90);assert preserved(e)==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'walkthrough-stamps-complete',True);original=preserved(e)[1:]
 cases=tuple(e.var(v) for v in range(0x40C0,0x40C3));assert cases==(6,6,6)
 for origin,first,second,destination in [(0,27,28,4),(1,28,27,0)]:
  town(e,origin);coach(e);decline(e);prompt(e);accept(e,first)
  assert preserved(e)[1:]==original
  e.screenshot(ROOT/f'test-output/walkthrough-coast-{first}-arrival.png')
  print('PASS: '+str(first)+' coach No/B declines and free trip retain inventory, badges, stamps and completed story',flush=True)
  e=reload(e,'walkthrough-coast-'+str(first)+'-coach',(43,first,8,5));check_map(e,first)
  print('PASS: '+str(first)+' coach arrival cold Continues with exact state and correct present-day port map',flush=True)
  decline(e,True);prompt(e,True);accept(e,second)
  assert preserved(e)[1:]==original and tuple(e.var(v) for v in range(0x40C0,0x40C3))==cases
  e.screenshot(ROOT/f'test-output/walkthrough-coast-{first}-to-{second}.png')
  print('PASS: '+str(first)+' to '+str(second)+' ferry No/B declines and free crossing preserve progress and case rewards',flush=True)
  e=reload(e,'walkthrough-coast-'+str(second)+'-ferry',(43,second,8,5));check_map(e,second)
  leave_port(e);assert e.location()==(43,destination,23,10) and preserved(e)[1:]==original
  print('PASS: '+str(second)+' ferry arrival cold Continues and north return exit reaches the correct capital',flush=True)
 town(e,3);go(e,(18,14));e=reload(e,'walkthrough-coast-complete',(43,12,18,14))
 before=preserved(e);e.press('DOWN');e.press('A',900)
 e.screenshot(ROOT/'test-output/walkthrough-coast-ada.png')
 for _ in range(160):
  if not e.read('sLockFieldControls',1):break
  e.press('A',90)
 assert preserved(e)==before and preserved(e)[1:]==original and not e.read('sLockFieldControls',1)
 assert tuple(e.var(v) for v in range(0x40C0,0x40C3))==cases
 print('PASS: final cold Continue retains both coast trips, all rewards/cases and repeatable Ada ending',flush=True)
finally:e.close()
