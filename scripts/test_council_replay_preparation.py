"""Retain Razor Leaf through the native Sweet Scent learning prompt for replay."""
from council_test_helpers import *
from battle_recovery_test_helpers import moves_pp
from test_country import party_species
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'council-england-stage-4',True);assert council(e)==(4,0);h=history(e);candy=item_count(e,68);nurse(e)
 begin(e,(10,4),757);battle(e);assert council(e)==(5,2) and history(e)==h and item_count(e,68)==candy+1
 assert 75 in moves_pp(e)[0] and 230 not in moves_pp(e)[0]
 e=reload(e,'council-england-champion');assert council(e)==(5,2) and 75 in moves_pp(e)[0]
 npc(e,(10,7));answer(e);e.finish_dialogue();assert council(e)==(0,2)
 nurse(e);begin(e,(2,4),753);battle(e);assert council(e)==(1,2) and item_count(e,68)==candy+1
 e=reload(e,'council-england-replay-stage-1');assert council(e)==(1,2)
 print('PASS: native Sweet Scent No/stop-learning Yes keeps Razor Leaf; earned Championship/title/prize and first replay match save normally',flush=True)
finally:e.close()
