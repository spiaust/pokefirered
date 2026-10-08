"""Read new travel-board help in all six towns and follow its shortcut steps."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_navigation import wait_task
from test_time import preserved
from test_tour import travel
from key_item_test_helpers import registered,toggle_registration,reload
from collections import Counter

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'map-select-complete',True)
    assert registered(e)==0
    before=preserved(e);history=tuple(e.var(v) for v in range(0x40C0,0x4100))
    assert not any(item==363 for item,quantity in before[3])
    go(e,(19,12))
    e.press('UP')
    e.press('A',900)
    for _ in range(12):
        if e.task_active('Task_EuropeMap'):break
        e.press('A',900)
    wait_task(e,'Task_EuropeMap');e.press('B',180);e.press('B',90)
    after=preserved(e)
    assert after[1:3]==before[1:3] and after[4]==before[4]
    assert Counter(i for i in after[3] if i[0])==Counter(i for i in before[3] if i[0])+Counter([(363,1)])
    assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history and registered(e)==0
    original=preserved(e)[1:]
    print('PASS: missing World Options item is granted normally exactly once; map, party, money and completed quests remain intact',flush=True)
    for index,city in enumerate(['London','Paris','Berlin','Oxford','Chantilly','Oranienburg']):
        go(e,(16,14))
        if e.location()[1]!=index*4:travel(e,index)
        go(e,(19,12));e.press('UP');before=preserved(e);registration=registered(e)
        e.press('A',900)
        for page in range(3):
            assert e.read('sLockFieldControls',1)
            e.press('A',900)
            if page>=1:e.screenshot(ROOT/f'test-output/travel-board-shortcut-{city}-{page}.png')
        e.press('A',900);wait_task(e,'Task_EuropeMap');e.frames(60)
        assert e.read('sEuropeMapCurrent',1)==index
        e.press('SELECT',60);e.press('SELECT',60);e.press('B',180);e.press('B',180);e.press('B',90)
        assert e.location()==(43,index*4,19,12) and preserved(e)==before and registered(e)==registration
        assert not e.read('sLockFieldControls',1)
        assert preserved(e)[1:]==original and tuple(e.var(v) for v in range(0x40C0,0x4100))==history
        print('PASS: '+city+' travel board shows both new shortcut pages and correct map; field return retains exact state and existing registration',flush=True)
        if index==0:
            toggle_registration(e,361);assert registered(e)==361
            e.press('SELECT',180);wait_task(e,'Task_EuropeMap')
            assert e.read('sEuropeMapCurrent',1)==0
            e.press('SELECT',60);e.press('SELECT',60);e.press('B',180);e.press('B',90)
            assert not e.read('sLockFieldControls',1) and preserved(e)[1:]==original
            print('PASS: normal REGISTER and field SELECT follow the new board instructions; in-map SELECT and field callback work',flush=True)
    e=reload(e,'travel-board-shortcut-v121');assert registered(e)==361
    e.press('SELECT',180);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapCurrent',1)==5
    e.press('B',180);e.press('B',90)
    assert preserved(e)[1:]==original and tuple(e.var(v) for v in range(0x40C0,0x4100))==history
    print('PASS: new v1.21 cold Continue retains exact state and registered Town Map SELECT at the final town',flush=True)
finally:e.close()
