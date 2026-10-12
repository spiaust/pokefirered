"""Native flinch loss, Speed caps, repeated triggers and prevention QA."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/steadfast-battle.state';e.state(base)
    for ability,stage,expected,flinch,pp in [(0,6,6,True,160),(96,6,7,True,160),(96,11,12,True,160),(96,12,12,True,160),(39,6,6,False,159)]:
        e.state(base,True);r=attack(e,'MOVE_FAKE_OUT',ability=ability,enemy_speed_stage=stage,attacker_item=0)
        assert r['speed']==expected and r['flinched']==flinch and r['enemy_pp']==pp,(ability,stage,r)
        print('PASS: native Fake Out flinch/cap/prevention',ability,stage,expected,pp,flush=True)
    e.state(base,True);first=attack(e,'MOVE_FAKE_OUT',ability=96,attacker_item=0)
    assert first['speed']==7 and first['enemy_pp']==160
    follow=ROOT/'test-output/steadfast-next-turn.state';e.state(follow)
    found=False
    for seed in range(1,65):
        e.state(follow,True);r=attack(e,'MOVE_ROCK_SLIDE',ability=96,enemy_speed_stage=7,seed=seed,attacker_accuracy=12,attacker_item=0)
        if r['flinched']:
            assert r['speed']==8 and r['enemy_pp']==160,r
            found=True;break
    assert found
    print('PASS: later-turn secondary flinch raises Speed once more',seed,flush=True)
    r=attack(e,'MOVE_QUICK_ATTACK',ability=96,enemy_speed_stage=8,attacker_item=0)
    assert r['speed']==8 and not r['flinched'] and r['enemy_pp']==159,r
    print('PASS: no flinch grants no extra stage and next action remains available',flush=True)
    e.state(follow,True);r=attack(e,'MOVE_FAKE_OUT',ability=96,enemy_speed_stage=7,expected_hits=0,attacker_item=0)
    assert r['speed']==7 and not r['flinched'] and r['enemy_pp']==159,r
    print('PASS: failed later-turn Fake Out does not activate Steadfast',flush=True)
finally:e.close()
