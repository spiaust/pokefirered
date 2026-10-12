"""Controlled native end-turn semi-invulnerable weather healing guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);p=ROOT/'test-output/ice-body-submerged.state';e.state(p)
    for ability,weather,flag,expected in [(90,128,1<<7,500),(90,128,1<<18,500),(44,4,1<<7,562),(44,4,1<<18,562)]:
        e.state(p,True);e.write('gBattleWeather',weather,2);e.write(e.symbols['gWishFutureKnock']+40,5,1);e.write('gStatuses3',flag)
        r=attack(e,'MOVE_SPLASH',ownhp=500,attacker_ability=ability,attacker_types=(15,15),enemy_type=15,expected_hits=None,attacker_item=0)
        assert e.read('gStatuses3')&flag and r['ownhp']==expected,(ability,flag,r,e.read('gStatuses3'))
        print('PASS: semi-invulnerable heal guard',ability,flag,expected,flush=True)
finally:e.close()
