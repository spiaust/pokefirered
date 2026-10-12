"""Regression for original stat protection abilities sharing Big Pecks commands."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);p=ROOT/'test-output/stat-guards.state';e.state(p)
    for ability,move,stat,expected in [(52,'MOVE_GROWL',1,6),(52,'MOVE_TAIL_WHIP',2,5),(51,'MOVE_SAND_ATTACK',6,6),(51,'MOVE_TAIL_WHIP',2,5),(29,'MOVE_TAIL_WHIP',2,6),(73,'MOVE_TAIL_WHIP',2,6)]:
        e.state(p,True);attack(e,move,ability=ability,expected_hits=0,attacker_accuracy=12)
        assert e.read(e.symbols['gBattleMons']+88+24+stat,1)==expected,(ability,move)
        print('PASS: original stat protection',ability,move,flush=True)
finally:e.close()
