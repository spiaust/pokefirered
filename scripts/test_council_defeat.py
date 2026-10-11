"""Genuine blackout/retry preserves the first recorded Council victory."""
from council_test_helpers import *
from test_trainers import money
name='council-england-stage-1'
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,name,True);assert council(e)==(1,0);h=history(e);nurse(e);beforemoney=money(e)
 begin(e,(4,4),754);battle(e,lose=True)
 assert e.location()[:2]==(43,3),(e.location(),council(e));assert council(e)==(1,0) and history(e)==h
 assert money(e)<beforemoney
 e.screenshot(ROOT/'test-output/council-defeat-clinic.png');e=reload(e,'council-defeat-clinic');assert council(e)==(1,0)
 go(e,(7,7));e.walk('DOWN',2);e.frames(180);assert e.location()[:2]==(43,0)
 enter(e);nurse(e);begin(e,(4,4),754);battle(e);assert council(e)==(2,0) and history(e)==h
 e=reload(e,'council-defeat-recovered');assert council(e)==(2,0)
 print('PASS: actual opposing attacks cause blackout and normal money loss; cleared stage survives clinic Save/Continue and a native retry wins',flush=True)
finally:e.close()
