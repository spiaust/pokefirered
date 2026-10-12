"""Native Tough Claws contact, drain/recoil and fixed/self-damage guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/tough-claws-battle.state';e.state(base)
    for move,contact in [('MOVE_QUICK_ATTACK',True),('MOVE_BITE',True),('MOVE_FIRE_PUNCH',True),('MOVE_IRON_HEAD',True),('MOVE_DRAIN_PUNCH',True),('MOVE_EARTHQUAKE',False),('MOVE_WATER_GUN',False),('MOVE_SEISMIC_TOSS',False)]:
        results=[]
        for ability in (0,104):
            e.state(base,True);results.append(attack(e,move,attacker_ability=ability,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True))
        normal,claws=results
        assert claws['power']==(normal['power']*13//10 if contact else normal['power']),(move,results)
        assert claws['damage']>normal['damage'] if contact else claws['damage']==normal['damage'],(move,results)
        if move=='MOVE_DRAIN_PUNCH':assert claws['ownhp']==100+max(1,claws['damage']//2),claws
        print('PASS: native contact/non-contact power',move,normal['power'],claws['power'],flush=True)
    for ability in (0,104):
        e.state(base,True);r=attack(e,'MOVE_SUPER_FANG',attacker_ability=ability,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True)
        assert r['damage']==500,r
        print('PASS: fixed half-HP damage unchanged',ability,flush=True)
    for move,divisor in [('MOVE_TAKE_DOWN',4),('MOVE_STRUGGLE',4)]:
        results=[]
        for ability in (0,104):
            e.state(base,True);r=attack(e,move,attacker_ability=ability,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True)
            assert r['ownhp']==100-max(1,r['damage']//divisor),r
            results.append(r)
        assert results[1]['power']==results[0]['power']*13//10 and results[1]['damage']>results[0]['damage']
        print('PASS: contact recoil move damage and native recoil',move,flush=True)
    e.state(base,True);immune=attack(e,'MOVE_QUICK_ATTACK',attacker_ability=104,enemy_type=7,expected_hits=0,attacker_item=0,stop_before_enemy=True)
    assert immune['damage']==0,immune
    results=[]
    for ability in (0,104):
        e.state(base,True);results.append(attack(e,'MOVE_QUICK_ATTACK',attacker_ability=ability,seed=3,confused=True,attacker_item=0,stop_before_enemy=True))
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: Ghost immunity and confusion self-damage unchanged',flush=True)
finally:e.close()
