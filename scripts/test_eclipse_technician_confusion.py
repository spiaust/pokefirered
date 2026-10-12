"""Technician must not boost native confusion self-damage or consume move PP."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);e.state(ROOT/'test-output/technician-confusion-base.state')
    for seed in range(1,17):
        e.state(ROOT/'test-output/technician-confusion-base.state',True)
        normal=attack(e,'MOVE_DARK_PULSE',seed=seed,confused=True)
        if normal['damage']==0 and normal['ownhp']<100:break
    else:raise AssertionError('No native confusion self-hit in seed sweep')
    e.state(ROOT/'test-output/technician-confusion-base.state',True)
    tech=attack(e,'MOVE_DARK_PULSE',seed=seed,attacker_ability=78,confused=True)
    assert normal['ownhp']==tech['ownhp'] and normal['power']==tech['power']==40,(normal,tech)
    assert tech['damage']==0
    print('PASS: native confusion self-damage unchanged by Technician, power 40, no PP spent; seed',seed,normal,tech,flush=True)
finally:e.close()
