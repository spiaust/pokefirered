"""Native doubles coach and turn-input helpers; no fake battle mode flags."""
from emulator import ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world
from test_shadow_runtime import go
from test_country import wait_menu
from test_eclipse_natural import first_symbol
from test_eclipse_move_evolution import moves
from tm_teaching_test_helpers import field
CHEER=1<<21;FOCUS=1<<20

def setup(e,dragon=False):
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
    go(e,(12,31));e.press('UP');e.press('A',180);e.finish_dialogue();field(e)
    go(e,(13,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A',180)
    for _ in range(100):
        if e.in_battle():break
        e.press('A',60)
    assert e.in_battle();e.frames(420)
    assert e.read('gBattlersCount',1)==4 and e.read('gBattleTypeFlags')&1
    wait_action(e,0)
    b=e.symbols['gBattleMons']
    for battler in range(4):
        q=b+88*battler
        e.write(q+40,1000,2);e.write(q+44,1000,2)
        for slot in range(4):e.write(q+12+2*slot,moves['MOVE_SPLASH'],2);e.write(q+36+slot,40,1)
    e.write(b+12,moves['MOVE_DRAGON_CHEER'],2);e.write(b+36,15,1)
    e.write(b+2*88+33,16 if dragon else 0,1);e.write(b+2*88+34,16 if dragon else 0,1)
    return b

def wait_action(e,battler):
    action=first_symbol('HandleInputChooseAction')
    for _ in range(180):
        if e.read(e.symbols['gBattlerControllerFuncs']+4*battler)&~1==action:return
        e.press('A',30)
    raise AssertionError(('No action menu',battler))

def select(e,battler):
    wait_action(e,battler);e.press('UP',2);e.press('LEFT',2);e.press('A',90)
    e.press('UP',2);e.press('LEFT',2);e.press('A',0)

def turn(e):
    select(e,0);select(e,2)
    # Return to the next lead action menu after both sides finish their moves.
    e.frames(30);wait_action(e,0)

def flags(e,battler):
    return e.read(e.symbols['gStatuses3']+4*battler)&CHEER,e.read(e.symbols['gBattleMons']+88*battler+80)&FOCUS
