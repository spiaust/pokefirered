"""Regional journal leads, independent stamps/badges, topics and pending rewards."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_journal import journal_task, snapshot as saved_snapshot
from test_england_story import set_win

CASES = (
    ('start-england', 0), ('start-france', 0), ('start-germany', 0),
    ('tour-partial', 0), ('tour-complete', 0),
    ('story-active', 1), ('story-rival-won', 4), ('story-pending', 4),
    ('story-complete', 5), ('gym-pending-tm', 6), ('gym-pending-key', 6),
    ('gym-complete', 7), ('france-active', 8), ('france-gardens', 9),
    ('france-forest', 10), ('france-both', 11), ('france-report', 12),
    ('france-pending', 12), ('france-complete', 13),
    ('water-gym-pending-tm', 14), ('water-gym-pending-key', 14),
    ('water-gym-complete', 15), ('germany-active', 16),
    ('germany-delivered', 17), ('germany-pending', 17), ('germany-complete', 18),
    ('electric-gym-pending-tm', 19), ('electric-gym-pending-key', 19),
)


def snapshot(emu):
    location, saved, variables = saved_snapshot(emu)
    # The normal Bag compacts gaps in old capacity fixtures on opening.
    # Compare every item's quantity without treating that rearrangement as loss.
    contents = tuple(sorted(pair for pair in saved[3] if pair[0]))
    return location, saved[:3] + (contents,) + saved[4:], variables


def inspect(emu, expected_lead, label=None):
    before = snapshot(emu)
    save = emu.read('gSaveBlock1Ptr')
    # Decode the actual saved checklist independently of the journal task.
    badges = emu.read(save + 0xEE0 + 0x820 // 8, 1) & 7
    expected_mask = sum(bool(emu.var(v)) << i for i, v in enumerate(range(0x40F2, 0x40F6))) | badges << 4
    open_key_item(emu, 361)
    wait_task(emu, 'Task_EuropeMap')
    task = journal_task(emu)
    emu.press('SELECT', 60)
    celebi = emu.read(task + 12, 2), emu.read(task + 14, 2)
    selection = emu.read('sEuropeMapSelection', 1)
    emu.press('DOWN', 60)
    assert (emu.read(task + 10, 2), emu.read(task + 16, 2)) == (1, 1)
    assert emu.read(task + 12, 2) == expected_lead, (label, emu.read(task + 12, 2), expected_lead)
    assert emu.read(task + 14, 2) == expected_mask
    if label:
        emu.screenshot(ROOT / f'test-output/tour-journal-{label}-lead.png')
    emu.press('A', 60)
    assert emu.read(task + 10, 2) == 2
    if label:
        emu.screenshot(ROOT / f'test-output/tour-journal-{label}-records.png')
    emu.press('UP', 60)
    assert emu.read(task + 16, 2) == 0 and emu.read(task + 10, 2) == 2
    assert (emu.read(task + 12, 2), emu.read(task + 14, 2)) == celebi
    emu.press('DOWN', 60)
    emu.press('SELECT', 60)
    assert emu.read(task + 10, 2) == 0 and emu.read('sEuropeMapSelection', 1) == selection
    emu.press('SELECT', 60)
    assert emu.read(task + 16, 2) == 0
    emu.press('UP', 60)
    assert emu.read(task + 16, 2) == 1
    emu.press('START', 180)
    wait_task(emu, 'Task_BagMenu_HandleInput')
    emu.press('B', 180)
    emu.press('B', 90)
    assert not emu.read('sLockFieldControls', 1)
    assert snapshot(emu) == before


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true')
    args = parser.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        for case, lead in CASES:
            load_checkpoint(emu, case, args.legacy)
            if case.endswith('pending-key'):
                # These old full-pocket fixtures contain only Bicycles. Replace
                # one with Town Map, retaining every occupied slot and no TM Case.
                emu.write(emu.read('gSaveBlock1Ptr') + 0x3B8, 361, 2)
            inspect(emu, lead, case)
            if case == 'gym-pending-tm':
                emu.state(ROOT / 'test-output/tour-journal-pending.state')
            print(f'PASS: {case}: regional lead {lead}, saved stamps/badges and read-only topic switching', flush=True)

        load_checkpoint(emu, 'story-active', args.legacy)
        set_win(emu, 743, True)
        inspect(emu, 2, 'alice-fixture')
        set_win(emu, 746, True)
        inspect(emu, 3, 'rival-fixture')
        print('PASS: targeted trainer-win fixtures distinguish Alice and rival prerequisites', flush=True)

        load_checkpoint(emu, 'electric-gym-complete', args.legacy)
        for count in range(5):
            save = emu.read('gSaveBlock1Ptr')
            for i, var in enumerate(range(0x40F2, 0x40F6)):
                emu.write(save + 0x1000 + (var - 0x4000) * 2, int(i < count), 2)
            inspect(emu, 20 + count, 'stamps-' + str(count))
        emu.state(ROOT / 'test-output/tour-journal-complete.state')
        print('PASS: targeted stamp fixtures distinguish each missing stamp, pending reward and completion', flush=True)
    finally:
        emu.close()
