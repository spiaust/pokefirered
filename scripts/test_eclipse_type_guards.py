"""Native Solid Rock/Filter weakness reduction, typing and damage exceptions."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

def seed_for_roll(roll):
    state=roll<<16
    for _ in range(3):state=(state-0x6073)*pow(0x41c64e6d,-1,1<<32)%(1<<32)
    return state
CASES=[('MOVE_WATER_GUN',(10,10),True,1),('MOVE_WATER_GUN',(10,4),True,1),
 ('MOVE_BRICK_BREAK',(5,17),True,1),('MOVE_DRAIN_PUNCH',(0,0),True,1),
 ('MOVE_WATER_GUN',(0,0),False,1),('MOVE_WATER_GUN',(11,11),False,1),
 ('MOVE_WATER_GUN',(10,11),False,1),('MOVE_WATER_GUN',(11,10),False,1),
 ('MOVE_QUICK_ATTACK',(7,7),False,0),('MOVE_SEISMIC_TOSS',(0,0),False,1),
 ('MOVE_STRUGGLE',(5,5),False,1)]
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/type-guards-base.state';e.state(base)
    for move,types,reduced,hits in CASES:
        results=[]
        for ability in (0,85,86):
            e.state(base,True)
            results.append(attack(e,move,ability=ability,enemy_types=types,expected_hits=hits,attacker_item=0,crit_seed=seed_for_roll(1)))
        normal,rock,filtered=results
        assert rock==filtered,(move,types,results)
        for r in (rock,filtered):
            assert r['power']==normal['power'],(move,results)
            if reduced:assert r['damage']<normal['damage'] and abs(r['damage']*4-normal['damage']*3)<=6,(move,types,results)
            else:assert r['damage']==normal['damage'],(move,types,results)
        if move=='MOVE_DRAIN_PUNCH':
            for r in results:assert r['ownhp']==100+max(1,r['damage']//2),r
        print('PASS: native type guards',move,types,results,flush=True)
    results=[]
    for ability in (0,85,86):
        e.state(base,True)
        results.append(attack(e,'MOVE_WATER_GUN',ability=ability,enemy_type=10,attacker_item=0,crit_seed=seed_for_roll(0)))
    assert all(r['crits']==[2] for r in results) and results[1]['damage']==results[2]['damage']<results[0]['damage'],results
    print('PASS: type guards also reduce critical weakness damage',results,flush=True)
    results=[]
    for ability in (0,85,86):
        e.state(base,True)
        results.append(attack(e,'MOVE_QUICK_ATTACK',ability=ability,enemy_type=8,attacker_ability=84,attacker_item=0,crit_seed=seed_for_roll(1)))
    assert results[0]==results[1]==results[2],results
    print('PASS: type guards do not alter Tinted Lens resisted damage',results,flush=True)
finally:e.close()
