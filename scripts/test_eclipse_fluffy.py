"""Native contact/Fire modifiers, healing/recoil and fixed/self-damage guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

def seed_for_roll(roll):
    state=roll<<16
    for _ in range(3):state=(state-0x6073)*pow(0x41c64e6d,-1,1<<32)%(1<<32)
    return state

e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/fluffy-battle.state';e.state(base)
    def trial(move,ability,**kwargs):
        e.state(base,True)
        return attack(e,move,ability=ability,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True,**kwargs)
    for move,factor in [('MOVE_QUICK_ATTACK',0.5),('MOVE_BITE',0.5),('MOVE_DRAIN_PUNCH',0.5),('MOVE_POISON_FANG',0.5),('MOVE_EARTHQUAKE',1),('MOVE_ROCK_SLIDE',1),('MOVE_WATER_GUN',1),('MOVE_EMBER',2),('MOVE_FLAMETHROWER',2),('MOVE_FIRE_PUNCH',1),('MOVE_BLAZE_KICK',1),('MOVE_FLAME_WHEEL',1),('MOVE_SEISMIC_TOSS',1)]:
        normal=trial(move,0);fluffy=trial(move,99)
        assert normal['power']==fluffy['power'],(move,normal,fluffy)
        if factor==0.5:assert 0<fluffy['damage']<normal['damage'] and abs(2*fluffy['damage']-normal['damage'])<=4,(move,normal,fluffy)
        elif factor==2:assert fluffy['damage']>normal['damage'] and abs(fluffy['damage']-2*normal['damage'])<=4,(move,normal,fluffy)
        else:assert normal['damage']==fluffy['damage'],(move,normal,fluffy)
        if move=='MOVE_DRAIN_PUNCH':assert fluffy['ownhp']==100+max(1,fluffy['damage']//2),fluffy
        print('PASS: native contact/Fire damage',move,factor,normal['damage'],fluffy['damage'],flush=True)
    normal=trial('MOVE_QUICK_ATTACK',0,crit_seed=seed_for_roll(0));fluffy=trial('MOVE_QUICK_ATTACK',99,crit_seed=seed_for_roll(0))
    assert normal['crits']==fluffy['crits']==[2] and fluffy['damage']<normal['damage']
    print('PASS: critical retains Fluffy reduction',flush=True)
    for ability in (0,99):
        r=trial('MOVE_SUPER_FANG',ability);assert r['damage']==500,r
        print('PASS: fixed half-HP damage unaffected',ability,flush=True)
    normal=trial('MOVE_STRUGGLE',0);fluffy=trial('MOVE_STRUGGLE',99)
    assert normal['power']==fluffy['power']==50 and 0<fluffy['damage']<normal['damage']
    assert fluffy['ownhp']==100-max(1,fluffy['damage']//4),fluffy
    print('PASS: real Struggle contact reduction and native recoil',flush=True)
    immune=trial('MOVE_QUICK_ATTACK',99,enemy_type=7,expected_hits=0);assert immune['damage']==0,immune
    print('PASS: Ghost immunity remains intact',flush=True)
    results=[trial('MOVE_QUICK_ATTACK',0,attacker_ability=a,seed=3,confused=True) for a in (0,99)]
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: confusion self-damage unchanged',flush=True)
finally:e.close()
