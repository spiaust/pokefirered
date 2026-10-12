"""Native normal-switch clearing and Baton Pass preservation of a Cheer boost."""
from emulator import Emulator,ROOT
from dragon_cheer_test_helpers import setup,turn,flags,CHEER,select,wait_action
from test_eclipse_move_evolution import moves
from natural_preparation_test_helpers import choose
from test_navigation import wait_task
for baton in (False,True):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        b=setup(e);turn(e);assert flags(e,2)==(CHEER,0)
        e.write(b+12,moves['MOVE_SPLASH'],2);e.write(b+36,40,1)
        select(e,0)
        if baton:
            e.write(b+176+12,moves['MOVE_BATON_PASS'],2);e.write(b+176+36,40,1);select(e,2)
            for _ in range(120):
                if e.task_active('Task_HandleChooseMonInput'):break
                e.press('A',30)
            wait_task(e,'Task_HandleChooseMonInput');choose(e,2);e.press('A',180)
        else:
            wait_action(e,2);e.press('LEFT',2);e.press('DOWN',2);e.press('A',180)
            wait_task(e,'Task_HandleChooseMonInput');choose(e,2);e.press('A',180);e.press('A',180)
        for _ in range(120):
            if e.read(e.symbols['gBattlerPartyIndexes']+4,2)==2:break
            e.press('A',30)
        assert e.read(e.symbols['gBattlerPartyIndexes']+4,2)==2
        e.frames(120);wait_action(e,0)
        assert flags(e,2)==((CHEER,0) if baton else (0,0)),(baton,flags(e,2))
        print('PASS:', 'Baton Pass preserves' if baton else 'normal switch clears', 'the ally one-stage Cheer boost',flush=True)
    finally:e.close()
