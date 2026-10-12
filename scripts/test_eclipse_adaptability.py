"""Native Adaptability matching types, fixed damage, Struggle and immunity QA."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
CASES=[('MOVE_QUICK_ATTACK',(0,0),0,True,1),('MOVE_QUICK_ATTACK',(0,12),0,True,1),('MOVE_QUICK_ATTACK',(12,0),0,True,1),
 ('MOVE_WATER_GUN',(11,11),0,True,1),('MOVE_THUNDER_SHOCK',(11,13),0,True,1),
 ('MOVE_FIRE_PUNCH',(11,11),0,False,1),('MOVE_DRAIN_PUNCH',(1,1),0,True,1),
 ('MOVE_SEISMIC_TOSS',(1,1),0,False,1),('MOVE_STRUGGLE',(0,0),0,False,1),
 ('MOVE_SHADOW_PUNCH',(7,7),0,False,0)]
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--quick-types-only',action='store_true');args=parser.parse_args()
if args.quick_types_only:CASES=CASES[:3]
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/adaptability-base.state';e.state(base)
    matching=[]
    for move,types,enemy,boost,hits in CASES:
        results=[]
        for ability in (0,81):
            e.state(base,True);results.append(attack(e,move,attacker_ability=ability,attacker_types=types,enemy_type=enemy,expected_hits=hits))
        normal,adapt=results
        assert adapt['power']==normal['power'],(move,results)
        assert adapt['damage']>normal['damage'] if boost else adapt['damage']==normal['damage'],(move,results)
        if boost:assert abs(adapt['damage']*3-normal['damage']*4)<=6,(move,results)
        if move=='MOVE_DRAIN_PUNCH':
            for r in results:assert r['ownhp']==100+max(1,r['damage']//2),r
        if move=='MOVE_QUICK_ATTACK':matching.append((normal['damage'],adapt['damage']))
        print('PASS: native Adaptability',move,'types',types,normal,adapt,flush=True)
    assert len(set(matching))==1,matching
    if args.quick_types_only:raise SystemExit(0)
    results=[]
    for ability in (0,81):
        e.state(base,True);results.append(attack(e,'MOVE_QUICK_ATTACK',seed=3,attacker_ability=ability,confused=True))
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: Adaptability does not boost confusion self-damage',results,flush=True)
finally:e.close()
