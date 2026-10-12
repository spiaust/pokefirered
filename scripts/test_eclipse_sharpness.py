"""Native slicing classification, dynamic power, STAB and non-slicing guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
SLICES=('MOVE_CUT','MOVE_RAZOR_LEAF','MOVE_SLASH','MOVE_FURY_CUTTER','MOVE_AIR_CUTTER','MOVE_AERIAL_ACE','MOVE_LEAF_BLADE')
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/sharpness-battle.state';e.state(base)
    for move in SLICES+('MOVE_FALSE_SWIPE','MOVE_IRON_HEAD','MOVE_BITE','MOVE_DRAIN_PUNCH','MOVE_SEISMIC_TOSS','MOVE_STRUGGLE'):
        results=[]
        for ability in (0,103):
            e.state(base,True);results.append(attack(e,move,attacker_ability=ability,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True))
        normal,sharp=results;boost=move in SLICES
        assert sharp['power']==(normal['power']*3//2 if boost else normal['power']),(move,results)
        assert sharp['damage']>normal['damage'] if boost else sharp['damage']==normal['damage'],(move,results)
        print('PASS: native slicing/non-slicing move',move,normal['power'],sharp['power'],flush=True)
    for ability,factor in [(0,1),(103,1.5)]:
        e.state(base,True);powers=[]
        for power in (10,20,40,80,160):
            r=attack(e,'MOVE_FURY_CUTTER',attacker_ability=ability,attacker_accuracy=12,attacker_item=0)
            assert r['power']==int(power*factor),(ability,power,r)
            powers.append(r['power'])
        print('PASS: native consecutive Fury Cutter power',ability,powers,flush=True)
    results=[]
    for ability in (0,103):
        e.state(base,True);results.append(attack(e,'MOVE_LEAF_BLADE',attacker_ability=ability,attacker_types=(12,12),attacker_accuracy=12,attacker_item=0,stop_before_enemy=True))
    assert results[1]['damage']>results[0]['damage']
    print('PASS: Sharpness combines with actual Grass STAB',flush=True)
    e.state(base,True);r=attack(e,'MOVE_SLASH',attacker_ability=103,enemy_type=7,attacker_item=0,expected_hits=0)
    assert r['damage']==0,r
    print('PASS: Normal/Ghost immunity remains intact',flush=True)
    results=[]
    for ability in (0,103):
        e.state(base,True);results.append(attack(e,'MOVE_SLASH',attacker_ability=ability,seed=3,confused=True,attacker_item=0,stop_before_enemy=True))
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: confusion self-damage unchanged',flush=True)
finally:e.close()
