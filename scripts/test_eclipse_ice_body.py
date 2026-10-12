"""Native Ice Body healing, weather guards and Rain Dish regressions."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/ice-body-battle.state';e.state(base)
    def trial(weather,ability,hp=500,maxhp=1000,suppressor=0,ice=True):
        e.state(base,True);e.write('gBattleWeather',weather,2);e.write(e.symbols['gWishFutureKnock']+40,5,1)
        return attack(e,'MOVE_SPLASH',ownhp=hp,enemyhp=maxhp,maxhp=maxhp,attacker_ability=ability,ability=suppressor,attacker_types=(15,15) if ice else (0,0),enemy_type=15,expected_hits=None,attacker_item=0)
    for hp,maxhp,expected in [(500,1000,562),(999,1000,1000),(1000,1000,1000),(5,12,6)]:
        r=trial(128,90,hp,maxhp)
        assert r['ownhp']==expected,(hp,maxhp,r)
        print('PASS: hail healing and HP limits',hp,maxhp,expected,flush=True)
    for weather in (0,4,16,32):
        r=trial(weather,90)
        assert r['ownhp']==(438 if weather==16 else 500),(weather,r)
        print('PASS: no Ice Body healing outside hail',weather,flush=True)
    for suppressor in (13,77):
        r=trial(128,90,suppressor=suppressor)
        assert r['ownhp']==500,r
        print('PASS: weather suppression disables Ice Body healing',suppressor,flush=True)
    for ability,expected in [(0,438),(89,500),(90,562)]:
        r=trial(128,ability,ice=False)
        assert r['ownhp']==expected,(ability,r)
        print('PASS: type-independent hail guard',ability,expected,flush=True)
    for weather,suppressor,expected in [(4,0,562),(128,0,500),(4,13,500),(4,77,500)]:
        r=trial(weather,44,suppressor=suppressor)
        assert r['ownhp']==expected,(weather,suppressor,r)
        print('PASS: original Rain Dish behavior',weather,suppressor,flush=True)
finally:e.close()
