"""Read-only story journal, real saved milestones, map controls and both callers."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved

CASES = (
    ('start-england', 0, 0), ('electric-gym-complete', 1, 0),
    ('celebi-active', 2, 0), ('celebi-sighting', 3, 0),
    ('celebi-pending', 3, 0), ('celebi-complete', 4, 1),
    ('time-arrival', 5, 1), ('time-child', 6, 1), ('time-blanket', 7, 1),
    ('time-complete', 8, 3), ('departure-active', 9, 3),
    ('departure-notice', 10, 3), ('departure-confirmed', 11, 3),
    ('departure-delivered', 12, 7), ('evac-arrival', 13, 7),
    ('evac-complete', 14, 15), ('message-active', 15, 15),
    ('message-delivered', 16, 15), ('message-acknowledged', 17, 15),
    ('message-pending', 17, 15), ('message-complete', 18, 31),
    ('relief-active', 19, 31), ('relief-parcel', 20, 31),
    ('relief-complete', 21, 63), ('garden-active', 22, 63),
    ('garden-found', 23, 63), ('garden-complete', 24, 127),
)


def snapshot(emu):
    return emu.location(), preserved(emu), tuple(emu.var(v) for v in range(0x40D5, 0x4100))


def journal_task(emu):
    expected = emu.symbols['Task_EuropeMap'] & ~1
    for i in range(16):
        task = emu.symbols['gTasks'] + i * 40
        if emu.read(task + 4, 1) and emu.read(task) & ~1 == expected:
            return task
    raise AssertionError('Map task absent')


def milestone_mask(emu, task):
    return emu.read(task + 14, 2) | (emu.read(task + 20, 2) << 16)


def inspect(emu, lead, milestones, label=None):
    before = snapshot(emu)
    open_key_item(emu, 361)
    wait_task(emu, 'Task_EuropeMap')
    task = journal_task(emu)
    assert emu.read(task + 10, 2) == 0
    initial = emu.read('sEuropeMapSelection', 1)
    emu.press('RIGHT', 60)
    selection = (initial + 1) % 8
    assert emu.read('sEuropeMapSelection', 1) == selection
    emu.press('A', 60)  # Existing travel help still works.
    emu.press('SELECT', 60)
    assert (emu.read(task + 10, 2), emu.read(task + 12, 2), milestone_mask(emu, task)) == (1, lead, milestones)
    if label:
        emu.screenshot(ROOT / f'test-output/journal-{label}-lead.png')
    for key in ('LEFT', 'RIGHT', 'UP', 'DOWN'):
        emu.press(key, 30)
    assert emu.read('sEuropeMapSelection', 1) == selection
    emu.press('A', 60)
    assert emu.read(task + 10, 2) == 2
    if label:
        emu.screenshot(ROOT / f'test-output/journal-{label}-milestones.png')
    emu.press('A', 60)
    assert emu.read(task + 10, 2) == 1
    emu.press('SELECT', 60)
    assert emu.read(task + 10, 2) == 0 and emu.read('sEuropeMapSelection', 1) == selection
    emu.press('SELECT', 60)
    emu.press('B', 180)
    wait_task(emu, 'Task_BagMenu_HandleInput')
    emu.press('B', 180)
    emu.press('B', 90)
    assert not emu.read('sLockFieldControls', 1)
    assert snapshot(emu) == before


def registered(emu):
    before = snapshot(emu)
    open_key_item(emu, 361)
    wait_task(emu, 'Task_EuropeMap')
    emu.press('B', 180)
    wait_task(emu, 'Task_BagMenu_HandleInput')
    emu.press('A', 90)
    emu.press('DOWN')
    emu.press('A', 90)
    assert emu.read(emu.read('gSaveBlock1Ptr') + 0x296, 2) == 361
    emu.press('B', 180)
    emu.press('B', 90)
    for key in ('B', 'START'):
        emu.press('SELECT', 180)
        wait_task(emu, 'Task_EuropeMap')
        task = journal_task(emu)
        assert emu.read(task + 10, 2) == 0
        emu.press('SELECT', 60)
        emu.press('A', 60)
        assert emu.read(task + 10, 2) == 2
        emu.press(key, 180)
        assert not emu.task_active('Task_EuropeMap')
        assert not emu.read('sLockFieldControls', 1)
        assert snapshot(emu) == before


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true', help='Cold-load existing battery saves.')
    args = parser.parse_args()
    for case, lead, milestones in CASES:
        emu = Emulator(ROOT / 'pokefirered.gba')
        try:
            load_checkpoint(emu, case, args.legacy)
            inspect(emu, lead, milestones, case)
            if case == 'message-pending':
                emu.state(ROOT / 'test-output/journal-pending.state')
            if case == 'garden-complete':
                registered(emu)
                emu.state(ROOT / 'test-output/journal-complete.state')
                emu.walk('RIGHT', 1)
                assert emu.location() == (43, 32, 11, 16)
            print(f'PASS: {case}: correct lead {lead}, milestones {milestones:02x}, read-only journal and map controls', flush=True)
        finally:
            emu.close()
    print('PASS: registered Town Map journal exits with B/START, reopens on map and restores field movement', flush=True)
