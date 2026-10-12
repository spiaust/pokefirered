"""Native turn ordering, weather/priority/status guards and speed regressions."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
from test_eclipse_natural import first_symbol
from test_eclipse_move_evolution import moves

e=Emulator(ROOT/'pokefirered.gba')
try:
    b=single(e);base=ROOT/'test-output/slush-rush-battle.state';e.state(base)
    action=first_symbol('HandleInputChooseAction')
    def configure(weather,ownability=91,enemyability=0,ownspeed=60,enemyspeed=100,paralyzed=False,stage=6,priority=False,duration=5):
        e.state(base,True);e.write('gBattleWeather',weather,2);e.write(e.symbols['gWishFutureKnock']+40,duration,1)
        for battler in (0,1):
            q=b+88*battler;e.write(q+32,enemyability if battler else ownability,1)
            e.write(q+6,enemyspeed if battler else ownspeed,2);e.write(q+40,1000,2);e.write(q+44,1000,2)
            e.write(q+46,0,2);e.write(q+76,64 if paralyzed and not battler else 0);e.write(q+80,0)
            e.write(q+33,15,1);e.write(q+34,15,1)
            for stat in range(8):e.write(q+24+stat,6,1)
            for slot in range(4):
                e.write(q+12+2*slot,moves['MOVE_QUICK_ATTACK'] if priority and battler else moves['MOVE_SPLASH'],2);e.write(q+36+slot,40,1)
        e.write(b+27,stage,1)
    def choose():
        e.press('UP',2);e.press('LEFT',2);e.press('A',90);e.press('UP',2);e.press('LEFT',2);e.frames(2,'A')
    def order():
        pp=[sum(e.read(b+88*j+36+s,1) for s in range(4)) for j in (0,1)]
        choose()
        for n in range(9000):
            changed=[j for j in (0,1) if sum(e.read(b+88*j+36+s,1) for s in range(4))<pp[j]]
            if changed:
                assert len(changed)==1,changed
                first=e.read('gBattlerByTurnOrder',1)
                assert first==changed[0],(first,changed)
                return first
            e.frames(1,'A' if n%60==0 else 0)
        raise AssertionError('No native first move')
    for weather,expected in [(128,0),(0,1),(4,1),(16,1),(32,1)]:
        configure(weather);assert order()==expected,weather
        print('PASS: native Slush Rush weather order',weather,expected,flush=True)
    for suppressor in (13,77):
        configure(128,enemyability=suppressor);assert order()==1
        print('PASS: suppressed hail speed',suppressor,flush=True)
    configure(128,ownability=0,enemyability=91,ownspeed=100,enemyspeed=60);assert order()==1
    print('PASS: opposing Slush Rush user receives speed boost',flush=True)
    for kwargs in [dict(paralyzed=True),dict(stage=4),dict(priority=True),dict(enemyspeed=135)]:
        configure(128,**kwargs);assert order()==1,kwargs
        print('PASS: native speed/priority guard',kwargs,flush=True)
    for ability,weather,expected in [(33,4,0),(33,128,1),(34,32,0),(34,128,1)]:
        configure(weather,ownability=ability);assert order()==expected
        print('PASS: original weather speed ability',ability,weather,flush=True)
    configure(128,duration=1);assert order()==0
    for n in range(9000):
        if e.read('gBattlerControllerFuncs')&~1==action:break
        e.frames(1,'A' if n%60==0 else 0)
    else:raise AssertionError('No next turn after hail expiry')
    assert e.read('gBattleWeather',2)==0 and order()==1
    print('PASS: hail expiry removes boost on next turn',flush=True)
    e.state(base,True);e.write('gBattleWeather',128,2);e.write(e.symbols['gWishFutureKnock']+40,5,1)
    r=attack(e,'MOVE_SPLASH',ownhp=500,attacker_ability=91,enemy_type=15,attacker_types=(0,0),expected_hits=None,attacker_item=0)
    assert r['ownhp']==438,r
    print('PASS: Slush Rush grants no hail immunity after a type change',flush=True)
finally:e.close()
