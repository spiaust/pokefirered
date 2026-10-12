"""Native double coach decline, two-fit requirement, victory and repeatability."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world
from test_shadow_runtime import go
from test_country import wait_menu
from dragon_cheer_test_helpers import setup,turn,wait_action
from test_eclipse_move_evolution import moves
from tm_teaching_test_helpers import field
from test_trainers import money

def offer(e):
    go(e,(13,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput')
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
    before=money(e);offer(e);e.press('B',180);field(e)
    assert not e.in_battle() and money(e)==before
    for slot in range(1,6):e.write(e.symbols['gPlayerParty']+100*slot+0x56,0,2)
    offer(e);e.press('A',180)
    for _ in range(25):e.press('A',60)
    field(e);assert not e.in_battle() and money(e)==before
    print('PASS: coach decline and insufficient fit partners do not start a battle or charge money',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    b=setup(e)
    for battler in (1,3):e.write(b+88*battler+40,1,2)
    e.write(b+12,moves['MOVE_SWIFT'],2);e.write(b+36,20,1)
    from dragon_cheer_test_helpers import select
    select(e,0);select(e,2)
    for _ in range(100):
        if not e.in_battle():break
        e.press('A',60)
    assert not e.in_battle();e.finish_dialogue();field(e)
    offer(e);e.press('A',180)
    for _ in range(100):
        if e.in_battle():break
        e.press('A',60)
    assert e.in_battle() and e.read('gBattlersCount',1)==4
    print('PASS: fixture-assisted native doubles victory returns to London and the same coach starts a repeat match',flush=True)
finally:e.close()
