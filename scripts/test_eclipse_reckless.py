"""Native Reckless recoil/crash power, damage, guards and Head Charge QA."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
CASES=[('MOVE_TAKE_DOWN',90,4),('MOVE_DOUBLE_EDGE',120,3),('MOVE_SUBMISSION',80,4),('MOVE_HEAD_CHARGE',120,4),('MOVE_JUMP_KICK',70,0),('MOVE_HI_JUMP_KICK',85,0)]
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/reckless-base.state';e.state(base)
    for move,power,recoil in CASES:
        results=[]
        for ability in (0,82):
            e.state(base,True);results.append(attack(e,move,attacker_ability=ability,ownhp=500,attacker_accuracy=12))
        normal,reckless=results
        assert normal['power']==power and reckless['power']==power*6//5,(move,results)
        assert reckless['damage']>normal['damage'],(move,results)
        for r in results:assert r['ownhp']==500-max(1,r['damage']//recoil) if recoil else r['ownhp']==500,(move,r)
        print('PASS: native Reckless',move,normal,reckless,'recoil divisor',recoil,flush=True)
    for move in ('MOVE_MEGA_KICK','MOVE_DRAIN_PUNCH','MOVE_STRUGGLE'):
        results=[]
        for ability in (0,82):
            e.state(base,True);results.append(attack(e,move,attacker_ability=ability,ownhp=500,attacker_accuracy=12))
        assert results[0]==results[1],(move,results)
        print('PASS: Reckless excludes',move,results,flush=True)
    for ability in (0,82):
        e.state(base,True)
        r=attack(e,'MOVE_HI_JUMP_KICK',seed=2,attacker_ability=ability,ownhp=500,attacker_accuracy=0,enemy_evasion=12,expected_hits=0)
        assert r['damage']==0 and r['ownhp']<500 and r['power']==(85 if ability==0 else 102),r
        print('PASS: native missed kick crash retained',ability,r,flush=True)
    e.state(base,True)
    r=attack(e,'MOVE_HEAD_CHARGE',attacker_ability=82,ownhp=500,enemyhp=1)
    assert r['damage']==1 and r['ownhp']==499,r
    print('PASS: overkill uses actual damage and minimum one recoil',r,flush=True)
    e.state(base,True)
    r=attack(e,'MOVE_HEAD_CHARGE',attacker_ability=69,ownhp=500)
    assert r['power']==120 and r['ownhp']==500,r
    print('PASS: native Rock Head still prevents regular recoil',r,flush=True)
    results=[]
    for ability in (0,82):
        e.state(base,True);results.append(attack(e,'MOVE_HEAD_CHARGE',seed=3,attacker_ability=ability,confused=True))
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: Reckless excludes confusion self-damage and preserves PP',results,flush=True)
finally:e.close()
