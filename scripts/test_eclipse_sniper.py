"""Native Sniper critical damage, probability, stat-stage and defensive guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

def seed_for_roll(roll):
    state=roll<<16
    for _ in range(3):state=(state-0x6073)*pow(0x41c64e6d,-1,1<<32)%(1<<32)
    return state
CASES=[('MOVE_QUICK_ATTACK',0,0,True),('MOVE_WATER_GUN',10,0,True),
 ('MOVE_DRAIN_PUNCH',0,0,True),('MOVE_QUICK_ATTACK',0,1,False),
 ('MOVE_QUICK_ATTACK',0,8,False),('MOVE_SEISMIC_TOSS',0,0,False)]
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/sniper-base.state';e.state(base)
    for move,target,roll,boost in CASES:
        results=[]
        for ability in (0,87):
            e.state(base,True)
            results.append(attack(e,move,attacker_ability=ability,enemy_type=target,attacker_item=0,crit_seed=seed_for_roll(roll)))
        normal,sniper=results
        assert normal['crits']==sniper['crits'] and normal['power']==sniper['power'],(move,results)
        if boost:assert sniper['crits']==[2] and sniper['damage']>normal['damage'] and abs(sniper['damage']*2-normal['damage']*3)<=6,(move,results)
        else:assert sniper['damage']==normal['damage'],(move,results)
        if move=='MOVE_DRAIN_PUNCH':
            for r in results:assert r['ownhp']==100+max(1,r['damage']//2),r
        print('PASS: native Sniper',move,target,roll,results,flush=True)
    for defender in (4,75):
        results=[]
        for ability in (0,87):
            e.state(base,True);results.append(attack(e,'MOVE_QUICK_ATTACK',attacker_ability=ability,ability=defender,attacker_item=0,crit_seed=seed_for_roll(0)))
        assert all(r['crits']==[1] for r in results) and results[0]['damage']==results[1]['damage'],results
        print('PASS: critical armor disables Sniper bonus',defender,results,flush=True)
    results=[]
    for stage,defense in ((6,6),(0,12)):
        e.state(base,True)
        results.append(attack(e,'MOVE_QUICK_ATTACK',attacker_ability=87,attacker_item=0,crit_seed=seed_for_roll(0),attacker_attack_stage=stage,enemy_defense_stage=defense))
    assert results[0]['damage']==results[1]['damage'] and all(r['crits']==[2] for r in results),results
    print('PASS: Sniper preserves native critical stat-stage bypass',results,flush=True)
    for defender in (85,86):
        results=[]
        for ability in (0,87):
            e.state(base,True);results.append(attack(e,'MOVE_WATER_GUN',attacker_ability=ability,ability=defender,enemy_type=10,attacker_item=0,crit_seed=seed_for_roll(0)))
        assert results[1]['damage']>results[0]['damage'] and abs(results[1]['damage']*2-results[0]['damage']*3)<=6,results
        print('PASS: Sniper combines with defensive weakness reduction',defender,results,flush=True)
    results=[]
    for ability in (0,87):
        e.state(base,True);results.append(attack(e,'MOVE_QUICK_ATTACK',seed=3,attacker_ability=ability,confused=True))
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: Sniper excludes confusion self-damage',results,flush=True)
finally:e.close()
