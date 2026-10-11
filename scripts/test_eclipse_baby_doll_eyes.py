"""Native priority and Attack-down battle check with explicit combat fixtures."""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world, var, battle_start
from test_eclipse_natural import first_symbol
from test_eclipse_move_evolution import moves

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-league-20-complete',True)
    world(e,0);var(e,0x40a0,753);battle_start(e,(40,25))
    b=e.symbols['gBattleMons'];action=first_symbol('HandleInputChooseAction')
    for _ in range(100):
        if e.read('gBattlerControllerFuncs')&~1==action:break
        e.press('A',30)
    assert e.read('gBattlerControllerFuncs')&~1==action
    # Player is slower. Both sides use a harmless status move; no damage fixtures.
    e.write(b+6,1,2);e.write(b+88+6,999,2)
    e.write(b+12,moves['MOVE_BABY_DOLL_EYES'],2);e.write(b+36,30,1)
    for slot in range(4):
        e.write(b+88+12+slot*2,moves['MOVE_SPLASH'],2);e.write(b+88+36+slot,40,1)
    hp=e.read(b+88+40,2);before=e.read(b+88+25,1)
    e.press('UP',2);e.press('LEFT',2);e.press('A',90)
    e.press('UP',2);e.press('LEFT',2);e.press('A',90)
    saw_order=False
    for _ in range(240):
        if e.read(b+36,1)==29:
            assert e.read('gBattlerByTurnOrder',1)==0
            saw_order=True
        if e.read('gBattlerControllerFuncs')&~1==action:break
        e.press('A',10)
    assert saw_order, 'Move did not execute'
    assert e.read(b+88+25,1)==before-1,(before,e.read(b+88+25,1))
    assert e.read(b+88+40,2)==hp
    e.screenshot(ROOT/'test-output/baby-doll-eyes-battle.png')
    print('PASS: Baby-Doll Eyes acts before a faster opponent, lowers Attack one stage, uses one PP and deals no damage')
finally:e.close()
