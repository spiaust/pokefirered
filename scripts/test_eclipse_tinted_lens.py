"""Native Tinted Lens resistance, mixed typing, immunity and fixed-damage QA."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

def seed_for_roll(roll):
    state=roll<<16
    for _ in range(3):state=(state-0x6073)*pow(0x41c64e6d,-1,1<<32)%(1<<32)
    return state
CASES=[('MOVE_QUICK_ATTACK',(8,8),True,0,1),('MOVE_QUICK_ATTACK',(5,8),True,0,1),
 ('MOVE_FIRE_PUNCH',(11,11),True,41,1),('MOVE_QUICK_ATTACK',(0,0),False,0,1),
 ('MOVE_FIRE_PUNCH',(12,12),False,41,1),('MOVE_FIRE_PUNCH',(10,12),False,41,1),
 ('MOVE_FIRE_PUNCH',(12,10),False,41,1),('MOVE_QUICK_ATTACK',(7,7),False,0,0),
 ('MOVE_MUD_SLAP',(2,2),False,0,0),('MOVE_MUD_SLAP',(12,12),False,26,0),
 ('MOVE_WATER_GUN',(12,12),False,11,0),('MOVE_QUICK_ATTACK',(8,8),False,25,0),
 ('MOVE_SEISMIC_TOSS',(6,2),False,0,1),('MOVE_STRUGGLE',(8,8),False,0,1)]
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/tinted-lens-base.state';e.state(base)
    for move,types,boost,defender,hits in CASES:
        results=[]
        for ability in (0,84):
            e.state(base,True)
            results.append(attack(e,move,attacker_ability=ability,enemy_types=types,ability=defender,expected_hits=hits,attacker_item=0,crit_seed=seed_for_roll(1)))
        normal,lens=results
        assert normal['power']==lens['power'],(move,types,results)
        if boost:assert lens['damage']>normal['damage'] and abs(lens['damage']-2*normal['damage'])<=2,(move,types,results)
        else:assert lens['damage']==normal['damage'],(move,types,results)
        print('PASS: native Tinted Lens',move,types,'defender',defender,normal,lens,flush=True)
    results=[]
    for ability in (0,84):
        e.state(base,True);results.append(attack(e,'MOVE_QUICK_ATTACK',seed=3,attacker_ability=ability,confused=True))
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: Tinted Lens excludes confusion self-damage and preserves PP',results,flush=True)
finally:e.close()
