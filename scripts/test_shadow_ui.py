"""Open the real journal and capture a visible Pokemon with normal Poke Balls."""
from emulator import Emulator,ROOT
from test_shadow_runtime import talk,go,ensure_visible
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_country import wait_menu
import json
e=Emulator(ROOT/'pokefirered.gba')
try:
    e.state(ROOT/'test-output/start-england.state',True);talk(e,(10,16))
    open_key_item(e,361);wait_task(e,'Task_EuropeMap');e.press('SELECT',90)
    fn=e.symbols['Task_EuropeMap']&~1;t=e.symbols['gTasks'];idx=next(i for i in range(16) if e.read(t+40*i)&~1==fn and e.read(t+40*i+4,1));a=t+40*idx+8
    assert e.read(a+4,2)==25 and e.read(a+8,2)==1
    e.screenshot(ROOT/'test-output/eclipse-journal.png');e.press('A',90);e.screenshot(ROOT/'test-output/eclipse-records.png')
    for _ in range(3):e.press('B',180)
    print('PASS: native Town Map shows campaign chapter and records',flush=True)
    talk(e,(10,7));ensure_visible(e)
    # Select a common Pidgey through native map visits, avoiding a rare-partner
    # catch/grind test with the starter alone. No encounter/catch values are edited.
    for _ in range(20):
        if e.var(0x40A0)==16:break
        talk(e,(15,20));talk(e,(10,7));ensure_visible(e)
    assert e.var(0x40A0)==16
    go(e,(17,15));e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A',180)
    for _ in range(40):
        if e.in_battle():break
        e.press('A',60)
    assert e.in_battle();e.frames(420)
    action=next(int(line.split()[0],16)&~1 for line in (ROOT/'pokefirered.sym').read_text().splitlines() if line.split()[-1:]==['HandleInputChooseAction'])
    for attempt in range(20):
        for _ in range(150):
            if e.read('gBattlerControllerFuncs')&~1==action:break
            e.press('A',30)
        e.press('UP',2);e.press('LEFT',2);e.press('RIGHT',2);e.press('A',180)
        e.screenshot(ROOT/'test-output/eclipse-capture-menu-debug.png')
        wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
        for _ in range(5):
            if e.read(bag+6,2)==2:break
            e.press('RIGHT',60)
        assert e.read(bag+6,2)==2
        e.press('A',90);e.press('A',400)
        for _ in range(120):
            if e.read('gPlayerPartyCount',1)==2:break
            if e.read('gBattlerControllerFuncs')&~1==action:break
            e.press('A',30)
        if e.read('gPlayerPartyCount',1)==2:break
    assert e.read('gPlayerPartyCount',1)==2
    for _ in range(40):
        if e.task_active('Task_YesNoMenu_HandleInput'):e.press('B',180)
        else:e.press('A',90)
        if not e.in_battle() and not e.read('sLockFieldControls',1):break
    e.frames(240);assert not e.in_battle() and e.location()[:2]==(44,1)
    e.screenshot(ROOT/'test-output/eclipse-captured.png')
    print('PASS: visible overworld Pokemon triggers a real wild battle, is caught with ordinary balls, and returns to the route',flush=True)
finally:e.close()
