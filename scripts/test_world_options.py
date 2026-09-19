"""Geographic map and World Options through real board, Bag and save input."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item,start_action
from test_navigation import wait_task
from test_time import preserved

def prefs(e):return tuple(e.var(v) for v in (0x40D2,0x40D3,0x40D4))
def identity(e):
    p=e.read('gSaveBlock2Ptr');return bytes(e.read(p+i,1) for i in range(14))
def close(e):
    e.press('B',180);e.press('B',180);e.press('B',90)
    assert not e.read('sLockFieldControls',1)
def options(e):
    open_key_item(e,363);wait_task(e,'Task_EuropeMap');e.frames(60)
    assert e.read('sWorldOptions',1)

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'start-england',True)
    e.walk('RIGHT',4);e.walk('UP',2);assert e.location()==(43,0,19,12)
    for _ in range(2):
        e.press('UP');e.press('A',180)
        for n in range(40):
            if e.task_active('Task_EuropeMap'):break
            e.press('A',90)
        wait_task(e,'Task_EuropeMap');e.frames(60)
        e.screenshot(ROOT/'test-output/geographic-map-simple.png')
        e.press('B',180);e.finish_dialogue()
    p=e.read('gSaveBlock1Ptr')+0x3B8
    assert sum(e.read(p+i*4,2)==363 for i in range(30))==1
    before=preserved(e);who=identity(e);loc=e.location()
    options(e);e.press('RIGHT',60);assert e.var(0x40D4)==1
    e.press('DOWN',60);e.press('RIGHT',60);e.press('RIGHT',60);assert e.var(0x40D3)==2
    e.press('DOWN',60);e.press('RIGHT',60);assert e.var(0x40D2)==1
    e.screenshot(ROOT/'test-output/world-options.png');close(e)
    assert e.read(e.symbols['gPlayerAvatar']+7,1)==1
    assert preserved(e)==before and identity(e)==who and e.location()==loc
    e.screenshot(ROOT/'test-output/world-options-leaf.png')
    open_key_item(e,361);wait_task(e,'Task_EuropeMap');e.frames(60)
    for i in range(8):
        assert e.read('sEuropeMapSelection',1)==i
        e.press('RIGHT',60)
    e.screenshot(ROOT/'test-output/geographic-map-shaded.png');close(e)
    assert prefs(e)==(1,2,1)
    start_action(e,4)
    for _ in range(5):e.press('A',150)
    e.battery(ROOT/'test-output/world-options-custom.sav')
    print('PASS: map-board grant, no duplicate key item, geography selection, preferences and cosmetic avatar',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'world-options-custom',True)
    assert prefs(e)==(1,2,1) and identity(e)==who and e.location()==loc
    assert e.read(e.symbols['gPlayerAvatar']+7,1)==1
    options(e);e.press('DOWN',60);e.press('RIGHT',60);assert e.var(0x40D3)==0
    close(e);assert identity(e)==who
    assert e.read(e.symbols['gPlayerAvatar']+7,1)==e.read(e.read('gSaveBlock2Ptr')+8,1)
    e.walk('LEFT',1);e.walk('RIGHT',1);assert e.location()==loc
    print('PASS: normal Save/cold Continue retains settings; original avatar restores without changing trainer identity',flush=True)
finally:e.close()
