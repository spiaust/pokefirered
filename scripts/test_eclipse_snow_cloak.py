"""Native hail evasion, weather suppression and residual protection QA."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/snow-cloak-battle.state';e.state(base)
    def trial(weather,ability,seed=1,ownability=0,move='MOVE_TACKLE',ownice=True):
        e.state(base,True);e.write('gBattleWeather',weather,2);e.write(e.symbols['gWishFutureKnock']+40,5,1)
        return attack(e,move,seed=seed,ownhp=500,ability=ability,attacker_ability=ownability,enemy_type=15,attacker_types=(15,15) if ownice else (0,0),expected_hits=None,attacker_item=0)
    dodge=None
    for seed in range(1,65):
        control=trial(128,0,seed);cloak=trial(128,89,seed)
        assert control['hits']==1,(seed,control)
        if cloak['hits']==0:dodge=seed;break
    assert dodge is not None
    print('PASS: hail Snow Cloak causes native accuracy miss',dodge,flush=True)
    for weather in (0,4,16,32):
        control=trial(weather,0,dodge);cloak=trial(weather,89,dodge)
        assert control['hits']==cloak['hits'] and control['hits']>=1 and control['damage']==cloak['damage'],(weather,control,cloak)
        print('PASS: no Snow Cloak evasion outside hail',weather,flush=True)
    for suppressor in (13,77):
        control=trial(128,0,dodge,suppressor);cloak=trial(128,89,dodge,suppressor)
        assert control['hits']==cloak['hits']==1 and control['damage']==cloak['damage']
        print('PASS: weather suppressor cancels hail evasion',suppressor,flush=True)
    for weather in (128,16):
        control=trial(weather,0,move='MOVE_SPLASH',ownice=False)
        cloak=trial(weather,0,ownability=89,move='MOVE_SPLASH',ownice=False)
        assert control['ownhp']==438,control
        assert cloak['ownhp']==(500 if weather==128 else 438),cloak
        print('PASS: non-Ice Snow Cloak protects hail only',weather,flush=True)
    ice=trial(128,0,move='MOVE_SPLASH')
    suppressed=trial(128,0,ownability=13,move='MOVE_SPLASH',ownice=False)
    assert ice['ownhp']==suppressed['ownhp']==500
    print('PASS: native Ice immunity and suppressed hail remain intact',flush=True)
finally:e.close()
