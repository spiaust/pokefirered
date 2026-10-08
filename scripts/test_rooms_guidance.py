"""New Rooms guidance on a genuine v1.15 completed save."""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved
from test_landmark_cases import save


def page(e):
    base = e.symbols['gTasks']
    fn = e.symbols['Task_EuropeMap'] & ~1
    task = next(base+i*40 for i in range(16)
                if e.read(base+i*40+4,1) and e.read(base+i*40) & ~1 == fn)
    return e.read(task+22,2)


def rooms(e):
    return e.read('sEuropePlacesRooms',1)

e = Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e, 'walkthrough-interiors-complete', True)
    location = e.location()
    before = preserved(e)
    history = tuple(e.var(v) for v in range(0x40C0,0x4100))
    for city, selection in [('London',0),('Paris',1),('Berlin',2)]:
        open_key_item(e,361)
        wait_task(e,'Task_EuropeMap')
        e.frames(60)
        for _ in range(8):
            if e.read('sEuropeMapSelection',1)==selection: break
            e.press('DOWN',60)
        assert e.read('sEuropeMapSelection',1)==selection
        e.press('R',60); e.press('L',60)
        assert page(e) and rooms(e)
        e.screenshot(ROOT/f'test-output/rooms-guidance-{city}.png')
        e.press('L',60); assert page(e) and not rooms(e)
        e.press('L',60); assert rooms(e)
        e.press('B',60); e.press('B',180); e.press('B',180); e.press('B',90)
        assert e.location()==location and preserved(e)==before
        assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
        assert not e.read('sLockFieldControls',1)
        print('PASS: '+city+' updated Rooms page renders, L/B controls work and v1.15 completed save remains exact',flush=True)
    save(e,'rooms-guidance-v116')
    saved = preserved(e)
    e.close()
    e = Emulator(ROOT/'pokefirered.gba')
    load_checkpoint(e,'rooms-guidance-v116',True)
    assert e.location()==location and preserved(e)==saved
    assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
    e.press('DOWN'); e.press('A',900)
    e.screenshot(ROOT/'test-output/rooms-guidance-ada.png')
    e.finish_dialogue()
    assert preserved(e)==saved and not e.read('sLockFieldControls',1)
    print('PASS: new v1.16 save cold Continues with exact completed state and repeatable Ada conclusion',flush=True)
finally:
    e.close()
