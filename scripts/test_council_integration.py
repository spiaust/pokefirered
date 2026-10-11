"""Saved championship survives World Options reset, Lapras and Ada rereading."""
from council_test_helpers import *
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_ride import ride,dismount,SURF
from test_celebi import researcher
PREFS=(0x40d4,0x40d3,0x40d2,0x40c3,0x40c4,0x40c5,0x40c6,0x40c7)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'council-england-champion',True);assert council(e)==(5,2);h=history(e)
 exit_hall(e);go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 go(e,(19,12));e.press('UP');e.press('A',900)
 for _ in range(12):
  if e.task_active('Task_EuropeMap'):break
  e.press('A',900)
 wait_task(e,'Task_EuropeMap');e.press('B',180);e.press('B',90);e.finish_dialogue()
 open_key_item(e,363);wait_task(e,'Task_EuropeMap')
 for _ in range(6):e.press('DOWN',60)
 e.press('LEFT',60)
 for _ in range(4):e.press('B',180)
 assert e.var(0x40c6)==4 and council(e)==(5,2)
 go(e,(26,16));ride(e);assert e.read('gPlayerAvatar',1)&SURF and council(e)==(5,2)
 e=reload(e,'council-champion-water');assert council(e)==(5,2) and e.read('gPlayerAvatar',1)&SURF
 dismount(e);open_key_item(e,363);wait_task(e,'Task_EuropeMap');e.press('UP',60)
 e.press('A',60);e.press('B',60);assert e.var(0x40c6)==4 and council(e)==(5,2)
 e.press('A',60);e.press('A',60)
 for _ in range(4):e.press('B',180)
 assert all(e.var(v)==0 for v in PREFS) and council(e)==(5,2)
 e=reload(e,'council-champion-defaults');assert council(e)==(5,2) and history(e)==h
 go(e,(16,14));travel(e,3);go(e,(18,14));before=preserved(e);researcher(e);e.finish_dialogue()
 assert preserved(e)==before and council(e)==(5,2) and history(e)==h
 print('PASS: saved Champion title/stage survives skin changes, water Save/Continue, dismount, reset cancel/confirm and Ada ending replay',flush=True)
finally:e.close()
