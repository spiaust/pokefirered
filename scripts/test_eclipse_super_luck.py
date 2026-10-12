"""Native Super Luck critical-stage boundaries, combinations and armor guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

def seed_for_roll(roll):
    # Two native VBlank RNG advances precede the critical command's own roll.
    state=roll<<16
    for _ in range(3):state=(state-0x6073)*pow(0x41c64e6d,-1,1<<32)%(1<<32)
    return state
# ability, held item, Focus Energy, move, requested RNG roll, critical multiplier
CASES=[(0,0,False,'MOVE_QUICK_ATTACK',8,1),(83,0,False,'MOVE_QUICK_ATTACK',8,2),
 (0,198,False,'MOVE_QUICK_ATTACK',4,1),(83,198,False,'MOVE_QUICK_ATTACK',4,2),
 (0,0,True,'MOVE_QUICK_ATTACK',3,1),(83,0,True,'MOVE_QUICK_ATTACK',3,2),
 (0,198,True,'MOVE_QUICK_ATTACK',2,1),(83,198,True,'MOVE_QUICK_ATTACK',2,2),
 (83,198,True,'MOVE_SLASH',1,1),(83,198,True,'MOVE_SLASH',2,2)]
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--cheer-only',action='store_true');args=parser.parse_args()
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/super-luck-base.state';e.state(base)
    for ability,item,focus,move,roll,expected in (() if args.cheer_only else CASES):
        e.state(base,True)
        r=attack(e,move,attacker_ability=ability,attacker_item=item,focus_energy=focus,crit_seed=seed_for_roll(roll))
        assert r['crit_rolls']==[roll] and r['crits']==[expected],(ability,item,focus,move,roll,r)
        print('PASS: native critical stage',ability,item,focus,move,roll,r,flush=True)
    for ability,expected in ((0,1),(83,2)):
        e.state(base,True);e.write('gStatuses3',1<<21)
        r=attack(e,'MOVE_QUICK_ATTACK',attacker_ability=ability,attacker_item=0,crit_seed=seed_for_roll(4))
        assert r['crit_rolls']==[4] and r['crits']==[expected],r
        print('PASS: Super Luck combines with Dragon Cheer',ability,r,flush=True)
    if args.cheer_only:raise SystemExit(0)
    for armor in (4,75):
        e.state(base,True)
        r=attack(e,'MOVE_QUICK_ATTACK',attacker_ability=83,attacker_item=198,focus_energy=True,ability=armor,crit_seed=seed_for_roll(0))
        assert r['crits']==[1],(armor,r)
        print('PASS: critical armor blocks Super Luck',armor,r,flush=True)
    e.state(base,True);e.write('gStatuses3',1<<15)
    r=attack(e,'MOVE_QUICK_ATTACK',attacker_ability=83,attacker_item=198,focus_energy=True,crit_seed=seed_for_roll(0))
    assert r['crits']==[1],r
    print('PASS: cannot-score-critical flag blocks Super Luck',r,flush=True)
finally:e.close()
