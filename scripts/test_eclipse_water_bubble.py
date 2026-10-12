"""Native Water Bubble power, Fire reduction and burn immunity/cure QA."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/water-bubble-battle.state';e.state(base)
    def trial(move,own=0,target=0,**kwargs):
        e.state(base,True)
        return attack(e,move,attacker_ability=own,ability=target,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True,**kwargs)
    for move,water in [('MOVE_WATER_GUN',True),('MOVE_BUBBLE_BEAM',True),('MOVE_SURF',True),('MOVE_WATERFALL',True),('MOVE_QUICK_ATTACK',False),('MOVE_FIRE_PUNCH',False),('MOVE_SEISMIC_TOSS',False),('MOVE_STRUGGLE',False)]:
        normal=trial(move);bubble=trial(move,101)
        assert bubble['power']==(normal['power']*2 if water else normal['power']),(move,normal,bubble)
        assert bubble['damage']>normal['damage'] if water else bubble['damage']==normal['damage'],(move,normal,bubble)
        print('PASS: Water-only power boost',move,normal['power'],bubble['power'],flush=True)
    for move,fire in [('MOVE_EMBER',True),('MOVE_FIRE_PUNCH',True),('MOVE_FLAMETHROWER',True),('MOVE_ICE_PUNCH',False),('MOVE_WATER_GUN',False),('MOVE_QUICK_ATTACK',False),('MOVE_SEISMIC_TOSS',False)]:
        normal=trial(move);bubble=trial(move,0,101)
        assert bubble['power']==(max(1,normal['power']//2) if fire else normal['power']),(move,normal,bubble)
        assert bubble['damage']<normal['damage'] if fire else bubble['damage']==normal['damage'],(move,normal,bubble)
        print('PASS: Fire-only incoming reduction',move,flush=True)
    for ability,expected in [(0,16),(41,0),(101,0)]:
        trial('MOVE_WILL_O_WISP',0,ability,expected_hits=0)
        assert e.read(e.symbols['gBattleMons']+88+76)&16==expected
        print('PASS: native primary burn prevention',ability,expected,flush=True)
    found=False
    for seed in range(1,65):
        trial('MOVE_EMBER',seed=seed)
        if e.read(e.symbols['gBattleMons']+88+76)&16:
            for ability in (41,101):
                trial('MOVE_EMBER',0,ability,seed=seed)
                assert not e.read(e.symbols['gBattleMons']+88+76)&16
            found=True;break
    assert found
    print('PASS: secondary burn blocked for Water Veil and Water Bubble',seed,flush=True)
    for ability,expected_hp,expected_status in [(0,375,16),(41,500,0),(101,500,0)]:
        e.state(base,True);r=attack(e,'MOVE_SPLASH',ownhp=500,attacker_ability=ability,attacker_status=16,attacker_item=0,expected_hits=0)
        assert r['ownhp']==expected_hp and e.read(e.symbols['gBattleMons']+76)==expected_status,(ability,r,e.read(e.symbols['gBattleMons']+76))
        print('PASS: native existing-burn cure',ability,expected_hp,expected_status,flush=True)
    trial('MOVE_TOXIC',0,101,expected_hits=0)
    assert e.read(e.symbols['gBattleMons']+88+76)&128
    print('PASS: Water Bubble does not block poison',flush=True)
    immune=trial('MOVE_WATER_GUN',101,11,expected_hits=0)
    assert immune['damage']==0,immune
    print('PASS: Water Absorb blocks boosted Water',flush=True)
    results=[trial('MOVE_WATER_GUN',a,seed=3,confused=True) for a in (0,101)]
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: confusion self-damage unchanged',flush=True)
finally:e.close()
