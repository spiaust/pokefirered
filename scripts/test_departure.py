"""Historical station news: gated travel, verified notice, report and return."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, return_to_ada, report
from test_time import ARRIVAL, PRESENT, PAST, preserved, cross, keeper, child, resume_booking
from test_country import wait_menu
from test_gym_ui import open_key_item
from test_navigation import wait_task

NEWS = 0x40EC
POST = (43, 30, 5, 10)


def guide_prompt(emu, returning=False):
    assert emu.location() == (POST if returning else ARRIVAL), emu.location()
    if returning:
        emu.walk('UP', 3)
    else:
        emu.walk('RIGHT', 7)
        emu.walk('UP', 1)
    emu.press('UP')
    emu.press('A', 180)


def visit_post(emu):
    before = preserved(emu), emu.var(PAST)
    guide_prompt(emu)
    wait_menu(emu, 'Task_YesNoMenu_HandleInput')
    emu.frames(60)
    emu.press('A', 180)
    emu.finish_dialogue()
    assert emu.location() == POST, emu.location()
    assert (preserved(emu), emu.var(PAST)) == before


def back_to_refuge(emu):
    guide_prompt(emu, True)
    wait_menu(emu, 'Task_YesNoMenu_HandleInput')
    emu.frames(60)
    emu.press('A', 180)
    emu.finish_dialogue()
    assert emu.location() == (43, 29, 12, 9), emu.location()
    emu.walk('LEFT', 7)
    emu.walk('DOWN', 1)
    assert emu.location() == ARRIVAL


def notice(emu):
    assert emu.location() == POST
    emu.walk('RIGHT', 6)
    emu.walk('UP', 5)
    emu.press('UP')
    emu.press('A', 180)
    # A completed report turns the notice into a boarding offer; this helper
    # only inspects it, leaving actual boarding to the historical train tests.
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
    emu.walk('DOWN', 5)
    emu.walk('LEFT', 6)
    assert emu.location() == POST


def dispatcher(emu):
    assert emu.location() == POST
    emu.walk('RIGHT', 3)
    emu.walk('UP', 3)
    emu.press('UP')
    emu.press('A', 180)
    emu.finish_dialogue()
    emu.walk('DOWN', 3)
    emu.walk('LEFT', 3)
    assert emu.location() == POST


def cancellations(emu, returning=False):
    before = preserved(emu), emu.var(NEWS), emu.var(PAST)
    origin = ROOT / 'test-output/departure-cancel-start.state'
    emu.state(origin)
    for choice in ('B', 'NO'):
        emu.state(origin, True)
        guide_prompt(emu, returning)
        wait_menu(emu, 'Task_YesNoMenu_HandleInput')
        emu.frames(60)
        location = emu.location()
        if choice == 'NO':
            emu.press('DOWN')
            emu.press('A', 180)
        else:
            emu.press('B', 180)
        emu.finish_dialogue()
        assert emu.location() == location
        assert (preserved(emu), emu.var(NEWS), emu.var(PAST)) == before
        assert not emu.read('sLockFieldControls', 1)
    emu.state(origin, True)


def finish_news(emu):
    if emu.location() == PRESENT:
        cross(emu)
    if emu.var(NEWS) < 4:
        if emu.location() == ARRIVAL:
            visit_post(emu)
        if emu.var(NEWS) < 2:
            notice(emu)
        if emu.var(NEWS) < 3:
            dispatcher(emu)
        back_to_refuge(emu)
    keeper(emu)
    assert emu.var(NEWS) == 4 and emu.var(PAST) == 4
    cross(emu)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true')
    args = parser.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'time-arrival', args.legacy)
        guide_prompt(emu)
        emu.finish_dialogue()
        assert emu.location() == (43, 29, 12, 9) and emu.var(NEWS) == 0
        assert not emu.task_active('Task_YesNoMenu_HandleInput')
        load_checkpoint(emu, 'time-complete', args.legacy)
        assert emu.var(NEWS) == 0 and emu.var(PAST) == 4
        before = preserved(emu)
        keeper(emu)
        assert emu.var(NEWS) == 0
        cancellations(emu)
        visit_post(emu)
        assert emu.var(NEWS) == 1
        emu.state(ROOT / 'test-output/departure-active.state')
        cancellations(emu, True)
        dispatcher(emu)
        assert emu.var(NEWS) == 1
        back_to_refuge(emu)
        keeper(emu)
        assert emu.var(NEWS) == 1
        visit_post(emu)
        print('PASS: blanket gate, No/B on both guides and no premature report or confirmation', flush=True)

        notice(emu)
        notice(emu)
        assert emu.var(NEWS) == 2
        emu.state(ROOT / 'test-output/departure-notice.state')
        cross(emu)
        cross(emu)
        visit_post(emu)
        assert emu.var(NEWS) == 2
        dispatcher(emu)
        dispatcher(emu)
        notice(emu)
        assert emu.var(NEWS) == 3
        emu.state(ROOT / 'test-output/departure-confirmed.state')
        open_key_item(emu, 361)
        wait_task(emu, 'Task_EuropeMap')
        assert emu.read('sEuropeMapPast', 1) and emu.read('sEuropeMapCurrent', 1) == 4
        emu.screenshot(ROOT / 'test-output/departure-map.png')
        emu.press('B', 180)
        emu.press('B', 180)
        emu.press('B', 90)
        cross(emu)
        emu.state(ROOT / 'test-output/departure-returned.state')
        cross(emu)
        keeper(emu)
        child(emu)
        keeper(emu)
        assert emu.var(NEWS) == 4 and emu.var(PAST) == 4 and preserved(emu) == before
        emu.state(ROOT / 'test-output/departure-delivered.state')
        visit_post(emu)
        notice(emu)
        dispatcher(emu)
        back_to_refuge(emu)
        assert emu.var(NEWS) == 4 and preserved(emu) == before
        cross(emu)
        return_to_ada(emu)
        # Walking can update friendship. Compare party bytes around the actual
        # conversation, while checking the other invariants across the journey.
        at_ada = preserved(emu)
        assert at_ada[1:] == before[1:]
        report(emu)
        assert emu.var(NEWS) == 4 and preserved(emu) == at_ada
        print('PASS: notice then confirmation, resumable era detours, delivery, repeat visits and Ada acknowledgement', flush=True)

        # Preserve an actual saved booking; only completed blanket progress is
        # supplied as a setup fixture to exercise the new map on that journey.
        load_checkpoint(emu, 'time-booking', args.legacy)
        emu.write(emu.read('gSaveBlock1Ptr') + 0x1000 + (PAST - 0x4000) * 2, 4, 2)
        visit_post(emu)
        emu.state(ROOT / 'test-output/departure-booking.state')
        cross(emu)
        resume_booking(emu)
        print('PASS: station-post return preserves an actual pending rail booking that completes in Oxford', flush=True)
    finally:
        emu.close()
