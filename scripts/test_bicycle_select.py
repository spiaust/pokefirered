"""Normal Bicycle registration and SELECT use across saves and indoor visits."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_gym_ui import start_action
from test_navigation import wait_task
from test_time import preserved


def registered(e):
    return e.read(e.read('gSaveBlock1Ptr')+0x296,2)


def toggle_registration(e):
    start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput')
    bag=e.symbols['gBagMenuState']
    for _ in range(5):
        if e.read(bag+6,2)==1:break
        e.press('RIGHT',90)
    assert e.read(bag+6,2)==1
    base=e.read('gSaveBlock1Ptr')+0x3B8
    target=next(i for i in range(30) if e.read(base+4*i,2)==360)
    for _ in range(35):
        current=e.read(bag+10,2)+e.read(bag+16,2)
        if current==target:break
        e.press('DOWN' if current<target else 'UP')
    assert current==target
    e.press('A',90);e.press('DOWN');e.press('A',180)
    e.press('B',180);e.press('B',180);e.press('B',90)
    assert not e.read('sLockFieldControls',1)


def reload(e,name):
    save(e,name);state=preserved(e),e.location(),registered(e)
    e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,name,True)
    assert (preserved(e),e.location(),registered(e))==state
    return e


e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'case-bike-complete',True)
    original=preserved(e)[1:];history=tuple(e.var(v) for v in range(0x40C0,0x4100))
    assert not e.read('gPlayerAvatar',1)&2
    if registered(e)==360:toggle_registration(e)
    before=preserved(e);toggle_registration(e)
    assert registered(e)==360 and preserved(e)==before
    print('PASS: normal Bag REGISTER assigns Bicycle to SELECT without changing party/items/quests',flush=True)
    e.press('SELECT',180);assert e.read('gPlayerAvatar',1)&2
    e.press('SELECT',180);assert not e.read('gPlayerAvatar',1)&2
    assert preserved(e)==before
    print('PASS: field SELECT mounts and dismounts registered Bicycle with exact state retained',flush=True)
    e.press('SELECT',180);e=reload(e,'bicycle-select-riding')
    assert e.read('gPlayerAvatar',1)&2 and registered(e)==360
    e.screenshot(ROOT/'test-output/bicycle-select-riding.png')
    e.press('SELECT',180);assert not e.read('gPlayerAvatar',1)&2
    print('PASS: riding cold Continue retains Bicycle registration and working SELECT dismount',flush=True)
    go(e,(16,14))
    from test_tour import travel
    travel(e,0);talk(e,(45,33),choice='YES')
    before=preserved(e);e.press('SELECT',180);e.finish_dialogue()
    assert not e.read('gPlayerAvatar',1)&2 and registered(e)==360 and preserved(e)==before
    e=reload(e,'bicycle-select-inside')
    assert registered(e)==360 and not e.read('gPlayerAvatar',1)&2
    print('PASS: indoor SELECT cannot mount; interior cold Continue retains registration and exact party/progress',flush=True)
    go(e,(5,7));e.walk('DOWN',1);e.frames(180)
    e.press('SELECT',180);assert e.read('gPlayerAvatar',1)&2
    e.press('SELECT',180);assert not e.read('gPlayerAvatar',1)&2
    go(e,(16,14));travel(e,3);go(e,(18,14))
    before=preserved(e);e.press('DOWN');e.press('A',900);e.finish_dialogue();assert preserved(e)==before
    assert preserved(e)[1:]==original and tuple(e.var(v) for v in range(0x40C0,0x4100))==history
    print('PASS: outdoor SELECT works after indoor exit; normal return retains Ada conclusion and all completed activities',flush=True)
    before=preserved(e);toggle_registration(e);assert registered(e)==0 and preserved(e)==before
    e=reload(e,'bicycle-select-complete');assert registered(e)==0
    print('PASS: normal Bag DESELECT removes shortcut; cold Continue retains exact deregistered state',flush=True)
finally:e.close()
