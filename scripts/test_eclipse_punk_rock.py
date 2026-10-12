"""Native sound boost/resistance, status moves and Soundproof guards."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);base=ROOT/'test-output/punk-rock-battle.state';e.state(base)
    def trial(move,own=0,target=0,**kwargs):
        e.state(base,True)
        if move=='MOVE_SNORE':kwargs.setdefault('attacker_status',2)
        return attack(e,move,attacker_ability=own,ability=target,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True,**kwargs)
    for move in ('MOVE_HYPER_VOICE','MOVE_UPROAR','MOVE_SNORE'):
        normal=trial(move);boost=trial(move,100);resist=trial(move,0,100);both=trial(move,100,100)
        assert boost['power']==both['power']==normal['power']*13//10 and resist['power']==normal['power'],(move,normal,boost,resist,both)
        assert boost['damage']>normal['damage']>resist['damage']>0
        assert abs(2*resist['damage']-normal['damage'])<=4 and abs(2*both['damage']-boost['damage'])<=4
        print('PASS: native sound boost/resistance and combined abilities',move,normal['damage'],boost['damage'],resist['damage'],both['damage'],flush=True)
        blocked=trial(move,100,43,expected_hits=0)
        assert blocked['damage']==0,blocked
        print('PASS: Soundproof blocks boosted sound',move,flush=True)
    for move in ('MOVE_QUICK_ATTACK','MOVE_WATER_GUN','MOVE_SEISMIC_TOSS','MOVE_SONIC_BOOM','MOVE_STRUGGLE'):
        normal=trial(move);punk=trial(move,100,100)
        assert normal['power']==punk['power'] and normal['damage']==punk['damage'],(move,normal,punk)
        print('PASS: non-sound/fixed/native Struggle unchanged',move,flush=True)
    for move,stat,expected in [('MOVE_GROWL',25,5),('MOVE_SCREECH',26,4)]:
        normal=trial(move,0,100,expected_hits=0);value=e.read(e.symbols['gBattleMons']+88+stat,1)
        boosted=trial(move,100,100,expected_hits=0)
        assert value==e.read(e.symbols['gBattleMons']+88+stat,1)==expected
        assert normal['damage']==boosted['damage']==0
        trial(move,100,43,expected_hits=0)
        assert e.read(e.symbols['gBattleMons']+88+stat,1)==6
        print('PASS: status sound effect unchanged; Soundproof still blocks',move,flush=True)
    results=[trial('MOVE_HYPER_VOICE',a,seed=3,confused=True) for a in (0,100)]
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: confusion self-damage receives no sound bonus/resistance',flush=True)
finally:e.close()
