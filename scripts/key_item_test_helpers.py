"""Normal Bicycle registration and SELECT use across saves and indoor visits."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_gym_ui import start_action
from test_navigation import wait_task
from test_time import preserved


def registered(e):
    return e.read(e.read('gSaveBlock1Ptr')+0x296,2)


def toggle_registration(e,item=360):
    start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput')
    bag=e.symbols['gBagMenuState']
    for _ in range(5):
        if e.read(bag+6,2)==1:break
        e.press('RIGHT',90)
    assert e.read(bag+6,2)==1
    base=e.read('gSaveBlock1Ptr')+0x3B8
    target=next(i for i in range(30) if e.read(base+4*i,2)==item)
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
    after=preserved(e),e.location(),registered(e)
    assert after==state,{'party_byte_differences':[(i,a,b) for i,(a,b) in enumerate(zip(state[0][0][1],after[0][0][1])) if a!=b],'other_changes':state[0][1:]!=after[0][1:],'locations':(state[1],after[1]),'registered':(state[2],after[2])}
    return e


