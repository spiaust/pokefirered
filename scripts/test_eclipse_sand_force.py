"""Native Sand Force type, weather, damage and residual guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/sand-force-battle.state';e.state(base)
    def trial(move,weather,attacker_ability,**kwargs):
        e.state(base,True);e.write('gBattleWeather',weather,2);e.write(e.symbols['gWishFutureKnock']+40,5,1)
        # Rock/Ice isolates move damage from both sandstorm and hail residuals.
        kwargs.setdefault('enemy_types',(5,15))
        return attack(e,move,attacker_ability=attacker_ability,enemy_type=5,attacker_types=(5,5),attacker_accuracy=12,attacker_item=0,**kwargs)
    for move,boost in [('MOVE_EARTHQUAKE',True),('MOVE_ROCK_SLIDE',True),('MOVE_METAL_CLAW',True),('MOVE_MAGNITUDE',True),('MOVE_QUICK_ATTACK',False),('MOVE_WATER_GUN',False),('MOVE_SEISMIC_TOSS',False),('MOVE_STRUGGLE',False)]:
        normal=trial(move,8,0);force=trial(move,8,93)
        assert force['power']==(normal['power']*13//10 if boost else normal['power']),(move,normal,force)
        assert force['damage']>normal['damage'] if boost else force['damage']==normal['damage'],(move,normal,force)
        print('PASS: sand move power/damage',move,normal['power'],force['power'],flush=True)
    for weather in (16,0,4,32,128):
        normal=trial('MOVE_EARTHQUAKE',weather,0);force=trial('MOVE_EARTHQUAKE',weather,93)
        assert force['power']==(130 if weather==16 else 100)
        assert force['damage']>normal['damage'] if weather==16 else force['damage']==normal['damage'],(weather,normal,force)
        print('PASS: permanent sand/other weather guard',weather,flush=True)
    for suppressor in (13,77):
        normal=trial('MOVE_EARTHQUAKE',8,0,ability=suppressor);force=trial('MOVE_EARTHQUAKE',8,93,ability=suppressor)
        assert normal['power']==force['power']==100 and force['damage']==normal['damage']
        print('PASS: suppressed Sand Force',suppressor,flush=True)
    immune=trial('MOVE_EARTHQUAKE',8,93,enemy_types=(2,8),expected_hits=0)
    assert immune['damage']==0,immune
    print('PASS: Ground immunity preserved',flush=True)
    results=[trial('MOVE_EARTHQUAKE',8,a,seed=3,confused=True) for a in (0,93)]
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: confusion self-damage receives no ability bonus',flush=True)
    for weather,ability,expected in [(8,0,438),(8,93,500),(128,93,438)]:
        e.state(base,True);e.write('gBattleWeather',weather,2);e.write(e.symbols['gWishFutureKnock']+40,5,1)
        r=attack(e,'MOVE_SPLASH',ownhp=500,attacker_ability=ability,enemy_type=5,attacker_types=(0,0),expected_hits=None,attacker_item=0)
        assert r['ownhp']==expected,(weather,ability,r)
        print('PASS: Sand Force weather immunity',weather,ability,expected,flush=True)
finally:e.close()
