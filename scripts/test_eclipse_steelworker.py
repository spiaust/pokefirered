"""Native Steelworker type power/STAB and Iron Head flinch guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
from test_eclipse_move_evolution import moves

e=Emulator(ROOT/'pokefirered.gba')
try:
    p=e.symbols['gBattleMoves']+12*moves['MOVE_IRON_HEAD']
    assert [e.read(p+j,1) for j in (1,2,3,4,5,6,7)]==[80,8,100,15,30,0,0]
    assert e.read(p+8,1)&1 and not e.read(p+8,1)&192
    single(e);base=ROOT/'test-output/steelworker-battle.state';e.state(base)
    def trial(move,ability,**kwargs):
        e.state(base,True)
        return attack(e,move,attacker_ability=ability,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True,**kwargs)
    for move,steel in [('MOVE_IRON_HEAD',True),('MOVE_METAL_CLAW',True),('MOVE_IRON_TAIL',True),('MOVE_METEOR_MASH',True),('MOVE_STEEL_WING',True),('MOVE_QUICK_ATTACK',False),('MOVE_WATER_GUN',False),('MOVE_SEISMIC_TOSS',False),('MOVE_STRUGGLE',False)]:
        normal=trial(move,0);worker=trial(move,102)
        assert worker['power']==(normal['power']*3//2 if steel else normal['power']),(move,normal,worker)
        assert worker['damage']>normal['damage'] if steel else worker['damage']==normal['damage'],(move,normal,worker)
        print('PASS: native Steelworker type power',move,normal['power'],worker['power'],flush=True)
    ordinary=trial('MOVE_IRON_HEAD',0,attacker_types=(8,8));worker=trial('MOVE_IRON_HEAD',102,attacker_types=(8,8));plain=trial('MOVE_IRON_HEAD',102)
    assert worker['damage']>ordinary['damage'] and worker['damage']>plain['damage']
    print('PASS: Steelworker stacks with actual Steel STAB',flush=True)
    found=False
    for seed in range(1,65):
        e.state(base,True);r=attack(e,'MOVE_IRON_HEAD',seed=seed,attacker_item=0)
        if r['flinched']:
            assert r['enemy_pp']==160,r
            for guard in (19,39):
                e.state(base,True);safe=attack(e,'MOVE_IRON_HEAD',seed=seed,ability=guard,attacker_item=0)
                assert not safe['flinched'] and safe['enemy_pp']==159 and safe['damage']==r['damage'],(guard,r,safe)
            e.state(base,True);steady=attack(e,'MOVE_IRON_HEAD',seed=seed,ability=96,attacker_item=0)
            assert steady['flinched'] and steady['speed']==7 and steady['enemy_pp']==160,steady
            found=True;break
    assert found
    print('PASS: native Iron Head flinch, Shield Dust/Inner Focus and Steadfast',seed,flush=True)
    results=[trial('MOVE_IRON_HEAD',a,seed=3,confused=True) for a in (0,102)]
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: confusion self-damage unchanged',flush=True)
finally:e.close()
