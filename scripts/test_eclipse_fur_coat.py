"""Native Fur Coat physical/special, critical, fixed and self-damage guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

def seed_for_roll(roll):
    state=roll<<16
    for _ in range(3):state=(state-0x6073)*pow(0x41c64e6d,-1,1<<32)%(1<<32)
    return state

e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/fur-coat-battle.state';e.state(base)
    def trial(move,ability,**kwargs):
        e.state(base,True)
        return attack(e,move,ability=ability,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True,**kwargs)
    for move,physical in [('MOVE_QUICK_ATTACK',True),('MOVE_EARTHQUAKE',True),('MOVE_ROCK_SLIDE',True),('MOVE_POISON_FANG',True),('MOVE_DRAIN_PUNCH',True),('MOVE_WATER_GUN',False),('MOVE_FIRE_PUNCH',False),('MOVE_BITE',False),('MOVE_SEISMIC_TOSS',False)]:
        normal=trial(move,0);coat=trial(move,98)
        assert normal['power']==coat['power'],(move,normal,coat)
        assert 0<coat['damage']<normal['damage'] if physical else coat['damage']==normal['damage'],(move,normal,coat)
        if move=='MOVE_DRAIN_PUNCH':
            assert coat['ownhp']==100+max(1,coat['damage']//2),coat
        print('PASS: native physical/special defense',move,normal['damage'],coat['damage'],flush=True)
    results=[]
    for stage in (6,12):
        pair=[trial('MOVE_QUICK_ATTACK',a,enemy_defense_stage=stage,crit_seed=seed_for_roll(0)) for a in (0,98)]
        assert all(r['crits']==[2] for r in pair) and pair[1]['damage']<pair[0]['damage'],pair
        results.append([r['damage'] for r in pair])
    assert results[0]==results[1],results
    print('PASS: critical bypasses raised stages but retains Fur Coat',results,flush=True)
    for stage in (0,12):
        normal=trial('MOVE_QUICK_ATTACK',0,enemy_defense_stage=stage,crit_seed=seed_for_roll(1));coat=trial('MOVE_QUICK_ATTACK',98,enemy_defense_stage=stage,crit_seed=seed_for_roll(1))
        assert normal['crits']==coat['crits']==[1] and 0<coat['damage']<normal['damage'],(stage,normal,coat)
        print('PASS: Defense stage still combines with Fur Coat',stage,flush=True)
    for ability in (0,98):
        r=trial('MOVE_SUPER_FANG',ability)
        assert r['damage']==500,r
        print('PASS: fixed half-HP damage unaffected',ability,flush=True)
    normal=trial('MOVE_STRUGGLE',0);coat=trial('MOVE_STRUGGLE',98)
    assert 0<coat['damage']<normal['damage'] and coat['power']==normal['power']==50
    assert coat['ownhp']==100-max(1,coat['damage']//4),coat
    print('PASS: real Struggle physical damage and native recoil',normal,coat,flush=True)
    immune=trial('MOVE_QUICK_ATTACK',98,enemy_type=7,expected_hits=0)
    assert immune['damage']==0,immune
    print('PASS: Ghost immunity preserved',flush=True)
    results=[trial('MOVE_QUICK_ATTACK',0,attacker_ability=a,seed=3,confused=True) for a in (0,98)]
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: confusion self-damage unchanged',flush=True)
finally:e.close()
