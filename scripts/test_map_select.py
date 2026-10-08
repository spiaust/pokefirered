"""Normal Town Map registration, SELECT callbacks and Bicycle replacement."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved
from key_item_test_helpers import registered,toggle_registration,reload
from test_tour import travel


def map_select(e,label):
    before=preserved(e);location=e.location();avatar=e.read('gPlayerAvatar',1)
    e.press('SELECT',180);wait_task(e,'Task_EuropeMap');e.frames(60)
    assert e.read('sEuropeMapCurrent',1)==(0 if location[1] not in (12,) else 3)
    for _ in range(8):
        if e.read('sEuropeMapSelection',1)==0:break
        e.press('DOWN',60)
    assert e.read('sEuropeMapSelection',1)==0
    e.press('R',60);e.press('L',60);assert e.read('sEuropePlacesRooms',1)
    e.screenshot(ROOT/f'test-output/map-select-{label}.png')
    e.press('SELECT',60);e.press('SELECT',60)
    e.press('B',180);e.press('B',180);e.press('B',90)
    assert e.location()==location and preserved(e)==before
    assert e.read('gPlayerAvatar',1)==avatar and registered(e)==361
    assert not e.read('sLockFieldControls',1) and not e.task_active('Task_BagMenu_HandleInput')


e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'bicycle-select-complete',True)
    original=preserved(e)[1:];history=tuple(e.var(v) for v in range(0x40C0,0x4100))
    assert registered(e)==0
    before=preserved(e);toggle_registration(e,361)
    assert registered(e)==361 and preserved(e)==before
    map_select(e,'walking')
    print('PASS: normal Town Map REGISTER and field SELECT open European Rooms/story controls and return directly to field with exact state',flush=True)
    open_key_item(e,360);e.frames(120);assert e.read('gPlayerAvatar',1)&2
    map_select(e,'riding')
    print('PASS: registered Town Map SELECT preserves mounted Bicycle and field control after map exit',flush=True)
    e=reload(e,'map-select-riding');assert registered(e)==361 and e.read('gPlayerAvatar',1)&2
    map_select(e,'riding-continued');open_key_item(e,360);e.frames(120)
    print('PASS: riding cold Continue retains Town Map registration and functional SELECT map callback',flush=True)
    go(e,(16,14));travel(e,0);talk(e,(45,33),choice='YES')
    map_select(e,'inside');e=reload(e,'map-select-inside');map_select(e,'inside-continued')
    print('PASS: interior Town Map SELECT shows correct capital and exact indoor Continue retains shortcut and map controls',flush=True)
    toggle_registration(e,360);assert registered(e)==360
    e.press('SELECT',180);e.finish_dialogue();assert not e.read('gPlayerAvatar',1)&2
    go(e,(5,7));e.walk('DOWN',1);e.frames(180)
    e.press('SELECT',180);assert e.read('gPlayerAvatar',1)&2
    e.press('SELECT',180);assert not e.read('gPlayerAvatar',1)&2
    e=reload(e,'map-select-replaced');assert registered(e)==360
    print('PASS: registering Bicycle replaces Town Map; indoor restriction and outdoor SELECT use remain correct after Continue',flush=True)
    toggle_registration(e,361);assert registered(e)==361
    toggle_registration(e,361);assert registered(e)==0
    e=reload(e,'map-select-complete');assert registered(e)==0
    assert preserved(e)[1:]==original and tuple(e.var(v) for v in range(0x40C0,0x4100))==history
    print('PASS: map can replace Bicycle then be DESELECTed; cold Continue retains no shortcut and all completed activities',flush=True)
finally:e.close()
