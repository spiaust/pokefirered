"""Native Technician power/damage boundaries, dynamic power and multi-hit QA."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
from test_eclipse_move_evolution import ids
cases=[('MOVE_QUICK_ATTACK',40,60,1,None,False),('MOVE_AERIAL_ACE',60,90,1,None,False),
 ('MOVE_DARK_PULSE',80,80,1,None,False),('MOVE_DRAINING_KISS',50,75,1,None,False),
 ('MOVE_DOUBLE_HIT',35,52,2,None,False),('MOVE_LOW_KICK',20,30,1,ids['SPECIES_PIKACHU'],False),
 ('MOVE_LOW_KICK',120,120,1,ids['SPECIES_SNORLAX'],False),
 ('MOVE_THUNDER_SHOCK',20,30,1,None,True),('MOVE_THUNDERBOLT',47,47,1,None,True)]
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);e.state(ROOT/'test-output/technician-battle-base.state')
    for move,ordinary,boosted,hits,species,sport in cases:
        results=[]
        for ability in (0,78):
            e.state(ROOT/'test-output/technician-battle-base.state',True)
            if sport:e.write('gStatuses3',1<<16)
            results.append(attack(e,move,attacker_ability=ability,expected_hits=hits,enemy_species=species))
        normal,tech=results
        assert normal['power']==ordinary and tech['power']==boosted,(move,results)
        assert tech['damage']>normal['damage'] if boosted>ordinary else tech['damage']==normal['damage'],(move,results)
        if move=='MOVE_DRAINING_KISS':assert tech['ownhp']==100+max(1,tech['damage']*3//4)
        print('PASS: Technician',move,'normal',normal,'boosted',tech,'Mud Sport',sport,flush=True)
finally:e.close()
