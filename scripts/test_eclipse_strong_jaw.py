"""Native biting flags, physical/special power and fixed/self-damage guards."""
import re
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
from test_eclipse_move_evolution import moves
BITES={'MOVE_BITE','MOVE_CRUNCH','MOVE_HYPER_FANG','MOVE_POISON_FANG'}
e=Emulator(ROOT/'pokefirered.gba')
try:
    count=int(re.search(r'#define MOVES_COUNT (\d+)',(ROOT/'include/constants/moves.h').read_text())[1])
    flagged={name for name,value in moves.items() if value<count and e.read(e.symbols['gBattleMoves']+12*value+8,1)&128}
    assert flagged==BITES,flagged
    assert all(e.read(e.symbols['gBattleMoves']+12*moves[m]+8,1)&1 for m in BITES)
    assert all(not e.read(e.symbols['gBattleMoves']+12*moves[m]+8,1)&64 for m in BITES)
    print('PASS: four native biting flags preserve contact and exclude punching',flush=True)
    single(e);base=ROOT/'test-output/strong-jaw-battle.state';e.state(base)
    for move in ('MOVE_BITE','MOVE_CRUNCH','MOVE_HYPER_FANG','MOVE_POISON_FANG','MOVE_QUICK_ATTACK','MOVE_MACH_PUNCH','MOVE_WATER_GUN','MOVE_SEISMIC_TOSS','MOVE_STRUGGLE'):
        results=[]
        for ability in (0,97):
            e.state(base,True);results.append(attack(e,move,attacker_ability=ability,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True))
        normal,jaw=results;boosted=move in BITES
        assert jaw['power']==(normal['power']*3//2 if boosted else normal['power']),(move,results)
        assert jaw['damage']>normal['damage'] if boosted else jaw['damage']==normal['damage'],(move,results)
        print('PASS: native Strong Jaw power/damage',move,normal['power'],jaw['power'],flush=True)
    for ability in (0,97):
        e.state(base,True);r=attack(e,'MOVE_SUPER_FANG',attacker_ability=ability,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True)
        assert r['damage']==500,r
        print('PASS: Super Fang fixed half-HP damage is not boosted',ability,flush=True)
    e.state(base,True);r=attack(e,'MOVE_HYPER_FANG',attacker_ability=97,enemy_type=7,attacker_accuracy=12,attacker_item=0,stop_before_enemy=True,expected_hits=0)
    assert r['damage']==0,r
    print('PASS: Normal/Ghost immunity remains intact',flush=True)
    results=[]
    for ability in (0,97):
        e.state(base,True);results.append(attack(e,'MOVE_BITE',attacker_ability=ability,seed=3,confused=True,attacker_item=0,stop_before_enemy=True))
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: no confusion self-damage boost or move PP consumption',flush=True)
finally:e.close()
