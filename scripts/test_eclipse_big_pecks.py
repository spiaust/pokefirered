"""Native Big Pecks stat protection with controlled battle fixtures."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack

e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);checkpoint=ROOT/'test-output/big-pecks-battle.state';e.state(checkpoint)
    for move,stat,drop in [('MOVE_TAIL_WHIP',2,1),('MOVE_LEER',2,1),('MOVE_SCREECH',2,2),('MOVE_GROWL',1,1),('MOVE_SAND_ATTACK',6,1)]:
        for ability in (0,88):
            e.state(checkpoint,load=True);attack(e,move,ability=ability,expected_hits=0,attacker_accuracy=12)
            expected=6 if ability==88 and stat==2 else 6-drop
            assert e.read(e.symbols['gBattleMons']+88+24+stat,1)==expected,(move,ability)
        print('PASS: stat move protection',move,flush=True)
    for move in ('MOVE_ROCK_SMASH','MOVE_IRON_TAIL','MOVE_CRUSH_CLAW'):
        found=False
        for seed in range(1,65):
            e.state(checkpoint,load=True);control=attack(e,move,seed=seed,attacker_accuracy=12)
            if e.read(e.symbols['gBattleMons']+88+26,1)==5:
                e.state(checkpoint,load=True);guard=attack(e,move,seed=seed,ability=88,attacker_accuracy=12)
                assert e.read(e.symbols['gBattleMons']+88+26,1)==6 and guard['damage']==control['damage'],(move,seed)
                found=True;break
        assert found,move
        print('PASS: damaging secondary blocked with damage preserved',move,seed,flush=True)
    found=False
    for seed in range(1,65):
        e.state(checkpoint,load=True);attack(e,'MOVE_CRUNCH',seed=seed,ability=88)
        if e.read(e.symbols['gBattleMons']+88+29,1)==5:found=True;break
    assert found
    print('PASS: native Crunch Special Defense drop remains allowed',flush=True)
    e.state(checkpoint,load=True);attack(e,'MOVE_SUPERPOWER',attacker_ability=88)
    assert e.read(e.symbols['gBattleMons']+25,1)==5 and e.read(e.symbols['gBattleMons']+26,1)==5
    print('PASS: Superpower retains self-inflicted Attack and Defense costs',flush=True)
finally:e.close()
