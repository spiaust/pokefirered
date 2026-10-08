"""Normal Bicycle use and cold Continue on the completed walkthrough save."""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go, save
from test_gym_ui import open_key_item
from test_time import preserved
from test_ride import steps


def history(e):
    return tuple(e.var(v) for v in range(0x40C0, 0x4100))


e = Emulator(ROOT / 'pokefirered.gba')
try:
    load_checkpoint(e, 'walkthrough-gastly-complete', True)
    original = preserved(e)[1:], history(e)
    go(e, (16, 14))
    before = preserved(e)
    open_key_item(e, 360)
    e.frames(120)
    assert e.read('gPlayerAvatar', 1) & 2
    assert preserved(e) == before
    steps(e, 'LEFT', 2)
    assert e.location() == (43, 12, 14, 14)
    e.screenshot(ROOT / 'test-output/walkthrough-bicycle-riding.png')
    print('PASS: normal Key Items Bicycle use mounts and moves on completed Oxford save with all rewards/progress retained', flush=True)
    save(e, 'walkthrough-bicycle-riding')
    saved = preserved(e), history(e)
    e.close()
    e = Emulator(ROOT / 'pokefirered.gba')
    load_checkpoint(e, 'walkthrough-bicycle-riding', True)
    assert (preserved(e), history(e)) == saved
    assert e.location() == (43, 12, 14, 14) and e.read('gPlayerAvatar', 1) & 2
    steps(e, 'RIGHT', 2)
    assert e.location() == (43, 12, 16, 14)
    print('PASS: cold Continue retains Bicycle riding and exact saved party/inventory/progress; movement remains controllable', flush=True)
    before = preserved(e)
    open_key_item(e, 360)
    e.frames(120)
    assert not e.read('gPlayerAvatar', 1) & 2 and preserved(e) == before
    go(e, (18, 14))
    save(e, 'walkthrough-bicycle-complete')
    saved = preserved(e), history(e)
    e.close()
    e = Emulator(ROOT / 'pokefirered.gba')
    load_checkpoint(e, 'walkthrough-bicycle-complete', True)
    assert (preserved(e), history(e)) == saved
    assert not e.read('gPlayerAvatar', 1) & 2
    before = preserved(e)
    e.press('DOWN')
    e.press('A', 900)
    e.screenshot(ROOT / 'test-output/walkthrough-bicycle-ada.png')
    e.finish_dialogue()
    assert preserved(e) == before
    assert (preserved(e)[1:], history(e)) == original
    print('PASS: using Bicycle again dismounts; walking Continue and Ada conclusion retain all completed activities and captured party', flush=True)
finally:
    e.close()
