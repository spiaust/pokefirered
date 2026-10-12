"""Native single-target effects, spread targeting and drain mechanics."""
from emulator import Emulator,ROOT
from modern_moves_test_helpers import single,attack
from dragon_cheer_test_helpers import setup,turn
from test_eclipse_move_evolution import moves

e=Emulator(ROOT/'pokefirered.gba')
try:
    single(e);e.state(ROOT/'test-output/modern-moves-battle.state')
    for move,factor,ability,ownhp,enemyhp in [('MOVE_DRAINING_KISS',75,0,100,1000),('MOVE_GIGA_DRAIN',50,0,100,1000),('MOVE_DRAINING_KISS',-75,64,100,1000),('MOVE_DRAINING_KISS',75,0,999,1000),('MOVE_DRAINING_KISS',75,0,100,1)]:
        e.state(ROOT/'test-output/modern-moves-battle.state',True)
        result=attack(e,move,ownhp=ownhp,enemyhp=enemyhp,ability=ability)
        amount=max(1,result['damage']*abs(factor)//100)
        expected=min(1000,ownhp+amount) if factor>0 else max(0,ownhp-amount)
        assert result['ownhp']==expected,(move,result,expected)
        print('PASS: native drain',move,result,'factor',factor,flush=True)
    for move,field,ability in [('MOVE_ENERGY_BALL','spdef',29),('MOVE_DARK_PULSE','flinched',39)]:
        for seed in range(1,65):
            e.state(ROOT/'test-output/modern-moves-battle.state',True)
            result=attack(e,move,seed=seed)
            if result[field] if field=='flinched' else result[field]==5:break
        else:raise AssertionError(('No secondary effect in deterministic seed sweep',move))
        print('PASS: native secondary effect',move,'seed',seed,result,flush=True)
        e.state(ROOT/'test-output/modern-moves-battle.state',True)
        guarded=attack(e,move,seed=seed,ability=ability)
        assert not guarded['flinched'] if field=='flinched' else guarded['spdef']==6
        print('PASS: native ability blocks secondary effect',move,ability,guarded,flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    b=setup(e)
    for battler in range(4):
        q=b+88*battler;e.write(q+32,0,1);e.write(q+33,0,1);e.write(q+34,0,1)
        e.write(q+8,100,2);e.write(q+10,100,2)
    e.write(b+12,moves['MOVE_DAZZLING_GLEAM'],2);e.write(b+36,10,1)
    turn(e)
    hp=[e.read(b+88*i+40,2) for i in range(4)]
    assert hp[0]==1000 and hp[2]==1000 and hp[1]<1000 and hp[3]<1000,hp
    assert e.read(b+36,1)==9
    print('PASS: native Dazzling Gleam damages both foes, spares ally and spends one PP',hp,flush=True)
finally:e.close()
