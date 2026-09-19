"""Onward Amiens journey, meeting instructions, return paths and journal."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_garden import GARDEN, leave as leave_garden, choose
from test_evac import RECEPTION, return_service, board_train
from test_departure import POST, dispatcher, visit_post
from test_time import ARRIVAL, PRESENT, cross, preserved, resume_booking
from test_journal import inspect
from test_gym_ui import open_key_item
from test_navigation import wait_task

STORY = 0x40E1
AMIENS = (43, 33, 10, 16)


def board(emu, choice='YES'):
    assert emu.location() == POST
    emu.walk('RIGHT', 3)
    emu.walk('UP', 3)
    before = preserved(emu)
    emu.press('UP')
    emu.press('A', 180)
    choose(emu, choice)
    assert preserved(emu) == before
    if choice != 'YES':
        emu.walk('DOWN', 3)
        emu.walk('LEFT', 3)
    assert emu.location() == (AMIENS if choice == 'YES' else POST), emu.location()


def leave(emu, choice='YES'):
    assert emu.location() == AMIENS
    emu.walk('UP', 1)
    before = preserved(emu)
    emu.press('UP')
    emu.press('A', 180)
    choose(emu, choice)
    assert preserved(emu) == before
    if choice != 'YES':
        emu.walk('DOWN', 1)
    assert emu.location() == (POST if choice == 'YES' else AMIENS), emu.location()


def nora(emu):
    assert emu.location() == AMIENS
    emu.walk('UP', 1)
    emu.walk('LEFT', 4)
    emu.walk('UP', 6)
    assert emu.location()[2:] == (6, 9)
    before = preserved(emu)
    emu.press('UP')
    emu.press('A', 180)
    emu.frames(180)
    emu.screenshot(ROOT / f'test-output/amiens-nora-{emu.var(STORY)}.png')
    for _ in range(40):
        if emu.task_active('Task_YesNoMenu_HandleInput'):
            emu.frames(60)
            emu.press('B', 180)
            emu.finish_dialogue()
            break
        if not emu.read('sLockFieldControls', 1):
            break
        emu.press('A', 90)
    assert not emu.read('sLockFieldControls', 1)
    assert preserved(emu) == before
    emu.walk('DOWN', 6)
    emu.walk('RIGHT', 4)
    emu.walk('DOWN', 1)


def notice(emu):
    assert emu.location() == AMIENS
    emu.walk('RIGHT', 7)
    emu.walk('UP', 10)
    assert emu.location()[2:] == (17, 6)
    before = preserved(emu)
    emu.press('UP')
    emu.press('A', 180)
    emu.frames(180)
    emu.screenshot(ROOT / 'test-output/amiens-notice.png')
    emu.finish_dialogue()
    assert preserved(emu) == before
    emu.walk('DOWN', 10)
    emu.walk('LEFT', 7)


def reach_post(emu):
    if emu.location() == GARDEN:
        leave_garden(emu)
    if emu.location() == RECEPTION:
        return_service(emu)
    if emu.location() == PRESENT:
        cross(emu)
    if emu.location() == ARRIVAL:
        visit_post(emu)
    assert emu.location() == POST


def finish_arrival(emu):
    if emu.location() != AMIENS:
        reach_post(emu)
        board(emu)
    if emu.var(STORY) < 2:
        nora(emu)
    if emu.var(STORY) == 2:
        notice(emu)
    nora(emu)
    assert emu.var(STORY) == 4


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true')
    args = parser.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'garden-found', args.legacy)
        reach_post(emu)
        dispatcher(emu)
        assert emu.location() == POST and emu.var(STORY) == 0
        load_checkpoint(emu, 'garden-complete', args.legacy)
        reach_post(emu)
        emu.state(ROOT / 'test-output/amiens-ready.state')
        for choice in ('B', 'NO'):
            board(emu, choice)
            assert emu.var(STORY) == 0
        board(emu)
        assert emu.var(STORY) == 1
        emu.state(ROOT / 'test-output/amiens-arrival.state')
        emu.screenshot(ROOT / 'test-output/amiens-arrival.png')
        inspect(emu, 25, 127, 'amiens-arrival')
        notice(emu)
        assert emu.var(STORY) == 1  # Read early: do not skip Nora's welcome.
        for choice in ('B', 'NO'):
            leave(emu, choice)
        leave(emu)
        board(emu)
        assert emu.var(STORY) == 1
        nora(emu)
        nora(emu)
        assert emu.var(STORY) == 2
        emu.state(ROOT / 'test-output/amiens-briefed.state')
        inspect(emu, 26, 127, 'amiens-briefed')
        cross(emu)
        assert emu.var(STORY) == 2
        emu.state(ROOT / 'test-output/amiens-returned.state')
        reach_post(emu)
        board(emu)
        notice(emu)
        notice(emu)
        assert emu.var(STORY) == 3
        emu.state(ROOT / 'test-output/amiens-notice.state')
        inspect(emu, 27, 127, 'amiens-notice')
        nora(emu)
        nora(emu)
        assert emu.var(STORY) == 4
        emu.state(ROOT / 'test-output/amiens-complete.state')
        inspect(emu, 28, 255, 'amiens-complete')
        open_key_item(emu, 361)
        wait_task(emu, 'Task_EuropeMap')
        assert emu.read('sEuropeMapPast', 1) and emu.read('sEuropeMapCurrent', 1) == 4
        emu.screenshot(ROOT / 'test-output/amiens-map.png')
        emu.press('B', 180)
        emu.press('B', 180)
        emu.press('B', 90)
        leave(emu)
        board(emu)
        notice(emu)
        assert emu.var(STORY) == 4
        leave(emu)
        board_train(emu)
        return_service(emu)
        board(emu)
        assert emu.var(STORY) == 4
        print('PASS: reunion gate, boarding/return No/B, early notice, welcome, confirmation and repeat visits', flush=True)
        print('PASS: unfinished departure/re-entry, Celebi detour, map context and four journal leads/eighth milestone', flush=True)
        load_checkpoint(emu, 'evac-booking', args.legacy)
        assert emu.var(0x40F7) != 0
        # Unlock fixture on a checkpoint with a genuinely booked modern journey.
        save = emu.read('gSaveBlock1Ptr')
        for var in (0x40E2, 0x40E3):
            emu.write(save + 0x1000 + (var - 0x4000) * 2, 3, 2)
        booking = emu.var(0x40F7)
        reach_post(emu)
        board(emu)
        nora(emu)
        cross(emu)
        assert emu.var(0x40F7) == booking
        resume_booking(emu)
        print('PASS: Beauvais board stays usable; Amiens and Celebi preserve an actual modern rail booking', flush=True)
    finally:
        emu.close()
