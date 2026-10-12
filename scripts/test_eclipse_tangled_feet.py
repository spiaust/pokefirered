"""Exact native accuracy rolls, confusion gates and always-hit guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

def seed_for_roll(roll):
    state=roll<<16
    for _ in range(3):state=(state-0x6073)*pow(0x41c64e6d,-1,1<<32)%(1<<32)
    return state

e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/tangled-feet-battle.state';e.state(base)
    def trial(move,roll,ability=94,confusion=True,**kwargs):
        e.state(base,True)
        return attack(e,move,ability=ability,enemy_confused=confusion,stop_before_enemy=True,accuracy_seed=seed_for_roll(roll),expected_hits=None,attacker_item=0,**kwargs)
    for move in ('MOVE_QUICK_ATTACK','MOVE_WATER_GUN'):
        for roll,expected in [(0,1),(49,1),(50,0),(99,0)]:
            r=trial(move,roll)
            assert r['accuracy_rolls']==[roll] and r['hits']==expected,(move,roll,r)
            assert e.read(e.symbols['gBattleMons']+88+80)&7==3
            print('PASS: exact confused accuracy boundary',move,roll,expected,flush=True)
    for ability,confusion in [(0,True),(94,False),(51,True)]:
        r=trial('MOVE_QUICK_ATTACK',99,ability,confusion)
        assert r['accuracy_rolls']==[99] and r['hits']==1,(ability,confusion,r)
        print('PASS: ability/confusion activation gate',ability,confusion,flush=True)
    for roll,expected in [(36,1),(37,0)]:
        r=trial('MOVE_QUICK_ATTACK',roll,enemy_evasion=7)
        assert r['accuracy_rolls']==[roll] and r['hits']==expected,r
        print('PASS: native evasion stage stacks with Tangled Feet',roll,expected,flush=True)
    for roll,expected in [(64,1),(65,0)]:
        r=trial('MOVE_QUICK_ATTACK',roll,attacker_ability=14)
        assert r['accuracy_rolls']==[roll] and r['hits']==expected,r
        print('PASS: Compound Eyes accuracy stacks correctly',roll,expected,flush=True)
    for move in ('MOVE_SWIFT','MOVE_AERIAL_ACE'):
        r=trial(move,99)
        assert r['hits']==1,r
        print('PASS: always-hit move bypasses Tangled Feet',move,flush=True)
    print('PASS: no target confusion self-hit contaminates first-action damage checks',flush=True)
finally:e.close()
