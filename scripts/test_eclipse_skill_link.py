"""Native Skill Link hit counts, fixed-hit guards and compiled regular slots."""
import json
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
from test_eclipse_move_evolution import ids

e=Emulator(ROOT/'pokefirered.gba')
try:
    for name in ('SHELLDER','CLOYSTER','PIKIPEK','TRUMBEAK','TOUCANNON'):
        assert e.read(e.symbols['gSpeciesInfo']+28*ids['SPECIES_'+name]+23,1)==79,name
    meta=json.loads((ROOT/'data/eclipse-roster.json').read_text())
    assert [r['token'] for r in meta['species'] if 'ABILITY_SKILL_LINK' in r['abilities']]==['SPECIES_PIKIPEK','SPECIES_TRUMBEAK','SPECIES_TOUCANNON']
    single(e);base=ROOT/'test-output/skill-link-base.state';e.state(base)
    ordinary=[]
    for move in ('MOVE_BULLET_SEED','MOVE_ICICLE_SPEAR','MOVE_FURY_SWIPES'):
        for seed in (1,2,3,4):
            e.state(base,True)
            result=attack(e,move,seed=seed,attacker_ability=79,expected_hits=None if move=='MOVE_FURY_SWIPES' else 5)
            assert result['hits'] in (0,5) if move=='MOVE_FURY_SWIPES' else result['hits']==5,result
            print('PASS: Skill Link',move,seed,result,flush=True)
        e.state(base,True)
        result=attack(e,move,expected_hits=None)
        assert 2<=result['hits']<=5 or (move=='MOVE_FURY_SWIPES' and result['hits']==0),result
        ordinary.append(result['hits'])
    for move,hits in (('MOVE_DOUBLE_HIT',2),('MOVE_TWIN_BEAM',2),('MOVE_TRIPLE_KICK',3),('MOVE_QUICK_ATTACK',1)):
        e.state(base,True)
        result=attack(e,move,attacker_ability=79,expected_hits=hits)
        print('PASS: fixed hit count',move,result,flush=True)
    assert any(n<5 for n in ordinary),ordinary
    e.state(base,True)
    result=attack(e,'MOVE_BULLET_SEED',attacker_ability=79,enemyhp=1,expected_hits=1)
    assert result['damage']==1,result
    print('PASS: target fainting stops Skill Link; regular species slots compiled',flush=True)
finally:e.close()
