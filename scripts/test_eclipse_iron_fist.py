"""Native Iron Fist punching classification, power and Drain Punch mechanics."""
import json,re
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
from test_eclipse_move_evolution import moves,ids
PUNCHES=('COMET_PUNCH','MEGA_PUNCH','FIRE_PUNCH','ICE_PUNCH','THUNDER_PUNCH','DIZZY_PUNCH','MACH_PUNCH','DYNAMIC_PUNCH','FOCUS_PUNCH','METEOR_MASH','SHADOW_PUNCH','SKY_UPPERCUT','DRAIN_PUNCH')
e=Emulator(ROOT/'pokefirered.gba')
try:
    flagged={name for name,value in moves.items() if value<370 and e.read(e.symbols['gBattleMoves']+12*value+8,1)&64}
    assert flagged=={'MOVE_'+name for name in PUNCHES},flagged
    single(e);base=ROOT/'test-output/iron-fist-base.state';e.state(base)
    for move in ('MOVE_MACH_PUNCH','MOVE_FIRE_PUNCH','MOVE_SHADOW_PUNCH','MOVE_METEOR_MASH','MOVE_DRAIN_PUNCH','MOVE_QUICK_ATTACK','MOVE_KARATE_CHOP','MOVE_DRAINING_KISS'):
        results=[]
        for ability in (0,80):
            e.state(base,True);results.append(attack(e,move,attacker_ability=ability,enemy_type=12 if move=='MOVE_SHADOW_PUNCH' else 0))
        normal,iron=results;power=e.read(e.symbols['gBattleMoves']+12*moves[move]+1,1)
        boosted=move[5:] in PUNCHES
        assert normal['power']==power and iron['power']==(power*6//5 if boosted else power),(move,results)
        assert iron['damage']>normal['damage'] if boosted else iron['damage']==normal['damage'],(move,results)
        if move=='MOVE_DRAIN_PUNCH':
            for r in results:assert r['ownhp']==100+max(1,r['damage']//2),r
        print('PASS: native Iron Fist',move,normal,iron,flush=True)
    e.state(base,True)
    immune=attack(e,'MOVE_SHADOW_PUNCH',attacker_ability=80,expected_hits=0)
    assert immune['damage']==0,immune
    print('PASS: Iron Fist does not bypass Normal immunity to Ghost',immune,flush=True)
    for ownhp,enemyhp,defender,factor in [(999,1000,0,1),(100,1,0,1),(100,1000,64,-1)]:
        e.state(base,True)
        r=attack(e,'MOVE_DRAIN_PUNCH',attacker_ability=80,ownhp=ownhp,enemyhp=enemyhp,ability=defender)
        amount=max(1,r['damage']//2)
        expected=min(1000,ownhp+amount) if factor==1 else max(0,ownhp-amount)
        assert r['ownhp']==expected,(r,expected)
        print('PASS: native Drain Punch HP cap/overkill/Liquid Ooze',ownhp,enemyhp,defender,r,flush=True)
    results=[]
    for ability in (0,80):
        e.state(base,True);results.append(attack(e,'MOVE_DRAIN_PUNCH',seed=3,attacker_ability=ability,confused=True))
    assert all(r['damage']==0 and r['power']==40 for r in results) and results[0]['ownhp']==results[1]['ownhp'],results
    print('PASS: Iron Fist does not boost confusion self-damage or spend attack PP',results,flush=True)
finally:e.close()
