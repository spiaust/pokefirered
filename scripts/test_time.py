"""First historical visit: two-way travel, independent quest, UI and rail detour."""
import argparse
import os
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, visit_forest, forest, STORY
from test_country import wait_menu
from test_ride import party
from test_trainers import money
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_tour import travel
from rail_test_helpers import BOOKING, choose_destination, board, finish_saved_journey

PAST = 0x40ED
ARRIVAL = (43, 29, 5, 10)
PRESENT = (43, 17, 15, 24)


def preserved(emu):
    save = emu.read('gSaveBlock1Ptr')
    key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
    return (party(emu), money(emu),
            tuple(emu.var(v) for v in (STORY, 0x40EF, 0x40F0, *range(0x40F2, 0x4100))),
            tuple((emu.read(save + i, 2), emu.read(save + i + 2, 2) ^ key)
                  for i in range(0x310, 0x5F8, 4)),
            bytes(emu.read(save + 0xEE0 + i, 1) for i in range(0x820 // 8, 0x828 // 8)))


def portal_prompt(emu):
    assert emu.location() in (PRESENT, ARRIVAL, (43, 30, 5, 10), (43, 31, 4, 7), (43, 32, 10, 16), (43, 33, 10, 16), (43, 34, 10, 16), (43, 35, 8, 5), (43, 36, 8, 5), (43, 37, 10, 16)), emu.location()
    emu.press('LEFT')
    emu.press('A', 180)
    wait_menu(emu, 'Task_YesNoMenu_HandleInput')
    emu.frames(60)


def cross(emu):
    destination = ARRIVAL if emu.location() == PRESENT else PRESENT
    before = preserved(emu)
    portal_prompt(emu)
    emu.press('A', 180)
    if destination == ARRIVAL and emu.var(0x40D9) == 1:
        wait_menu(emu, 'Task_MultichoiceMenu_HandleInput'); emu.frames(60)
        emu.press('A', 180)
    emu.finish_dialogue()
    emu.frames(90)
    assert emu.location() == destination, emu.location()
    assert preserved(emu) == before
    assert not emu.read('sLockFieldControls', 1)


def cancel_checks(emu):
    origin = emu.location()
    before = preserved(emu), emu.var(PAST)
    portal_prompt(emu)
    prompt = ROOT / f'test-output/time-prompt-{os.getpid()}.state'
    emu.state(prompt)
    for choice in ('B', 'NO'):
        emu.state(prompt, True)
        if choice == 'NO':
            emu.press('DOWN')
            emu.press('A', 180)
        else:
            emu.press('B', 180)
        emu.finish_dialogue()
        assert emu.location() == origin
        assert (preserved(emu), emu.var(PAST)) == before
        assert not emu.read('sLockFieldControls', 1)
    prompt.unlink()


def child(emu):
    assert emu.location() == ARRIVAL
    emu.walk('RIGHT', 3)
    emu.walk('UP', 3)
    assert emu.location()[2:] == (8, 7)
    emu.press('UP')
    emu.press('A', 180)
    emu.finish_dialogue()
    emu.walk('DOWN', 3)
    emu.walk('LEFT', 3)
    assert emu.location() == ARRIVAL


def keeper(emu):
    assert emu.location() == ARRIVAL
    emu.walk('UP', 3)
    assert emu.location()[2:] == (5, 7)
    emu.press('UP')
    emu.press('A', 180)
    emu.finish_dialogue()
    emu.walk('DOWN', 3)
    assert emu.location() == ARRIVAL


def finish_visit(emu):
    if emu.var(PAST) < 2:
        child(emu)
    if emu.var(PAST) < 3:
        keeper(emu)
    child(emu)
    assert emu.var(PAST) == 4
    cross(emu)


def resume_booking(emu):
    assert emu.location() == PRESENT
    emu.walk('DOWN', 16)
    emu.walk('DOWN', 24)
    emu.walk('DOWN', 14)
    emu.walk('RIGHT', 8)
    emu.walk('UP', 5)
    emu.frames(180)
    emu.walk('UP', 1)
    assert emu.location() == (43, 6, 4, 7), emu.location()
    finish_saved_journey(emu)
    assert emu.location() == (43, 14, 4, 7) and emu.var(BOOKING) == 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true')
    args = parser.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'celebi-report', args.legacy)
        visit_forest(emu)
        forest(emu)
        emu.finish_dialogue()
        assert emu.location() == PRESENT and emu.var(PAST) == 0
        assert not emu.task_active('Task_YesNoMenu_HandleInput')
        print('PASS: sighting alone cannot unlock time travel before Ada reviews the report', flush=True)

        load_checkpoint(emu, 'celebi-complete', args.legacy)
        assert emu.var(PAST) == 0 and emu.var(STORY) == 3
        visit_forest(emu)
        before = preserved(emu)
        emu.state(ROOT / 'test-output/time-ready.state')
        cancel_checks(emu)
        cross(emu)
        assert emu.var(PAST) == 1
        emu.state(ROOT / 'test-output/time-arrival.state')
        emu.screenshot(ROOT / 'test-output/time-refuge.png')
        cancel_checks(emu)
        cross(emu)
        cross(emu)
        assert emu.var(PAST) == 1
        keeper(emu)
        assert emu.var(PAST) == 1
        emu.walk('RIGHT', 6)
        emu.walk('UP', 5)
        emu.press('UP')
        emu.press('A', 180)
        emu.finish_dialogue()
        emu.walk('DOWN', 5)
        emu.walk('LEFT', 6)
        assert emu.location() == ARRIVAL
        print('PASS: No/B in both eras, immediate return/reentry, refuge sign and quest ordering', flush=True)

        child(emu)
        assert emu.var(PAST) == 2
        emu.state(ROOT / 'test-output/time-child.state')
        child(emu)
        assert emu.var(PAST) == 2
        keeper(emu)
        assert emu.var(PAST) == 3
        emu.state(ROOT / 'test-output/time-blanket.state')
        keeper(emu)
        cross(emu)
        emu.state(ROOT / 'test-output/time-returned.state')
        cross(emu)
        assert emu.var(PAST) == 3
        child(emu)
        keeper(emu)
        child(emu)
        assert emu.var(PAST) == 4 and preserved(emu) == before
        emu.state(ROOT / 'test-output/time-complete.state')
        print('PASS: blanket handoff and repeat talks; unfinished visit resumes without inventory or present-quest changes', flush=True)

        open_key_item(emu, 361)
        wait_task(emu, 'Task_EuropeMap')
        assert emu.read('sEuropeMapCurrent', 1) == 4
        assert emu.read('sEuropeMapPast', 1) == 1
        emu.screenshot(ROOT / 'test-output/time-map.png')
        emu.press('A', 90)
        emu.press('RIGHT', 60)
        emu.press('B', 180)
        emu.press('B', 180)
        emu.press('B', 90)
        assert emu.location() == ARRIVAL
        cross(emu)
        open_key_item(emu, 361)
        wait_task(emu, 'Task_EuropeMap')
        assert emu.read('sEuropeMapPast', 1) == 0
        emu.press('B', 180)
        emu.press('B', 180)
        emu.press('B', 90)
        open_key_item(emu, 360)
        emu.frames(120)
        assert emu.read('gPlayerAvatar', 1) & 2
        cross(emu)
        assert not emu.read('gPlayerAvatar', 1) & 2
        cross(emu)
        print('PASS: map labels the historical era and return anchor; cycling arrival becomes walking', flush=True)

        # A real Chantilly -> Oxford booking stops first in Paris. Walk to the
        # forest and detour through time without booking another train.
        load_checkpoint(emu, 'celebi-complete', args.legacy)
        emu.walk('LEFT', 2)
        travel(emu, 4)
        emu.walk('RIGHT', 7)
        emu.walk('UP', 5)
        emu.frames(180)
        emu.walk('UP', 1)
        emu.walk('RIGHT', 3)
        emu.press('UP')
        emu.press('A', 180)
        choose_destination(emu, 3)
        board(emu, 1, 3)
        emu.walk('DOWN', 2)
        emu.frames(180)
        emu.walk('DOWN', 4)
        emu.walk('LEFT', 8)
        emu.walk('UP', 15)
        emu.walk('UP', 24)
        emu.walk('UP', 15)
        assert emu.location() == PRESENT and emu.var(BOOKING) == 4
        cross(emu)
        emu.state(ROOT / 'test-output/time-booking.state')
        cross(emu)
        resume_booking(emu)
        print('PASS: actual booked Oxford journey survives time travel and completes through the Paris clerk', flush=True)
    finally:
        emu.close()
