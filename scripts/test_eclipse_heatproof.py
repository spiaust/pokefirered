"""Native Heatproof attack power, status and residual damage guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/heatproof-battle.state';e.state(base)
    def trial(move,ability,**kwargs):
        e.state(base,True)
        return attack(e,move,ability=ability,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True,**kwargs)
    for move,fire in [('MOVE_EMBER',True),('MOVE_FIRE_PUNCH',True),('MOVE_FLAMETHROWER',True),('MOVE_FIRE_BLAST',True),('MOVE_ICE_PUNCH',False),('MOVE_WATER_GUN',False),('MOVE_QUICK_ATTACK',False),('MOVE_SEISMIC_TOSS',False),('MOVE_STRUGGLE',False)]:
        normal=trial(move,0);heat=trial(move,95)
        assert heat['power']==(max(1,normal['power']//2) if fire else normal['power']),(move,normal,heat)
        assert heat['damage']<normal['damage'] if fire else heat['damage']==normal['damage'],(move,normal,heat)
        print('PASS: native Heatproof Fire/non-Fire attack',move,normal['power'],heat['power'],flush=True)
    for target in ((8,12),(10,10)):
        normal=trial('MOVE_FLAMETHROWER',0,enemy_types=target);heat=trial('MOVE_FLAMETHROWER',95,enemy_types=target)
        assert heat['power']==47 and 0<heat['damage']<normal['damage'],(target,normal,heat)
        print('PASS: combined typing retains Heatproof reduction',target,flush=True)
    for ability in (0,95):
        r=trial('MOVE_WILL_O_WISP',ability,expected_hits=0)
        assert e.read(e.symbols['gBattleMons']+88+76)&16,r
        print('PASS: Heatproof permits native burn status',ability,flush=True)
    for maxhp,hp,control,protected in [(1000,500,375,438),(1000,1000,875,938),(12,5,4,4)]:
        for ability,expected in [(0,control),(95,protected)]:
            e.state(base,True)
            r=attack(e,'MOVE_SPLASH',ownhp=hp,enemyhp=maxhp,maxhp=maxhp,attacker_ability=ability,attacker_status=16,attacker_item=0,expected_hits=0)
            assert r['ownhp']==expected and e.read(e.symbols['gBattleMons']+76)&16,(maxhp,hp,ability,r)
            print('PASS: native burn reduction/minimum',maxhp,hp,ability,expected,flush=True)
    for ability in (0,95):
        e.state(base,True);r=attack(e,'MOVE_SPLASH',ownhp=500,attacker_ability=ability,attacker_status=8,attacker_item=0,expected_hits=0)
        assert r['ownhp']==375,r
        print('PASS: poison residual remains unchanged',ability,flush=True)
    normal=trial('MOVE_QUICK_ATTACK',0,attacker_status=16);heat=trial('MOVE_QUICK_ATTACK',0,attacker_status=16,attacker_ability=95)
    assert heat['damage']==normal['damage'] and heat['power']==normal['power']
    print('PASS: native burn Attack penalty remains intact',flush=True)
finally:e.close()
