"""Historical train, reception check-in, persistent relocation and return paths."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, return_to_ada, report
from test_time import cross, preserved, ARRIVAL, keeper, resume_booking
from test_departure import POST, NEWS, notice, visit_post
from test_country import wait_menu
from test_gym_ui import open_key_item
from test_navigation import wait_task

EVAC = 0x40E5
RECEPTION = (43, 31, 4, 7)


def prompt(emu):
    assert emu.location() == POST
    emu.walk('RIGHT', 6)
    emu.walk('UP', 5)
    emu.press('UP')
    emu.press('A', 180)
    wait_menu(emu, 'Task_YesNoMenu_HandleInput')
    emu.frames(60)


def board_train(emu):
    prompt(emu)
    before = preserved(emu)
    emu.press('A', 180)
    emu.finish_dialogue()
    emu.frames(90)
    assert emu.location() == RECEPTION, emu.location()
    assert preserved(emu) == before


def host(emu):
    assert emu.location() == RECEPTION
    emu.walk('UP', 2)
    assert emu.location()[2:] == (4, 5), emu.location()
    before = preserved(emu)
    emu.press('UP')
    emu.press('A', 180)
    emu.finish_dialogue()
    assert preserved(emu) == before
    emu.walk('DOWN', 2)
    assert emu.location() == RECEPTION


def elise(emu):
    assert emu.location() == RECEPTION
    emu.walk('RIGHT', 3)
    before = preserved(emu)
    emu.press('UP')
    emu.press('A', 180)
    # Keep reception checks independent of the optional follow-up message.
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
    emu.walk('LEFT', 3)
    assert emu.location() == RECEPTION


def return_service(emu):
    assert emu.location() == RECEPTION
    emu.walk('DOWN', 2)
    emu.frames(180)
    assert emu.location()[:2] == (43, 30), emu.location()
    if emu.location()[2:] == (5, 11):
        emu.walk('UP', 1)
    assert emu.location() == POST, emu.location()


def assert_relocated(emu):
    assert emu.location() == ARRIVAL
    # Walk near Elise's old position so an offscreen object cannot hide a bug.
    emu.walk('RIGHT', 3)
    emu.walk('UP', 3)
    for i in range(16):
        obj = emu.symbols['gObjectEvents'] + i * 36
        assert not (emu.read(obj, 1) & 1 and emu.read(obj + 8, 1) == 2
                    and emu.read(obj + 9, 1) == 29 and emu.read(obj + 10, 1) == 43)
    emu.walk('DOWN', 3)
    emu.walk('LEFT', 3)


def finish_reception(emu):
    if emu.location() == ARRIVAL:
        assert_relocated(emu)
        visit_post(emu)
    if emu.location() == POST:
        board_train(emu)
    host(emu)
    elise(emu)
    assert emu.var(EVAC) == 2
    cross(emu)


def check_unfinished_return(emu):
    emu.state(ROOT / 'test-output/evac-arrival.state', True)
    cross(emu)
    cross(emu)
    assert_relocated(emu)
    assert emu.var(EVAC) == 1
    visit_post(emu)
    board_train(emu)
    assert emu.var(EVAC) == 1
    host(emu)
    assert emu.var(EVAC) == 2
    print('PASS: leaving before check-in preserves relocation and permits a later completed reception', flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--legacy', action='store_true')
    args = p.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'departure-confirmed', args.legacy)
        notice(emu)
        assert emu.location() == POST and emu.var(EVAC) == 0
        load_checkpoint(emu, 'departure-delivered', args.legacy)
        assert emu.var(EVAC) == 0
        visit_post(emu)
        ready = ROOT / 'test-output/evac-ready.state'
        emu.state(ready)
        for choice in ('B', 'NO'):
            emu.state(ready, True)
            prompt(emu)
            if choice == 'NO':
                emu.press('DOWN')
                emu.press('A', 180)
            else:
                emu.press('B', 180)
            emu.finish_dialogue()
            assert emu.location() == (43, 30, 11, 5) and emu.var(EVAC) == 0
        emu.state(ready, True)
        board_train(emu)
        assert emu.var(EVAC) == 1
        emu.state(ROOT / 'test-output/evac-arrival.state')
        emu.screenshot(ROOT / 'test-output/evac-reception.png')
        before = preserved(emu)
        elise(emu)
        assert emu.var(EVAC) == 1
        host(emu)
        host(emu)
        elise(emu)
        assert emu.var(EVAC) == 2 and preserved(emu)[1:] == before[1:]
        emu.state(ROOT / 'test-output/evac-complete.state')
        print('PASS: delivered-report gate, No/B, first train, host check-in and repeat conversations', flush=True)

        open_key_item(emu, 361)
        wait_task(emu, 'Task_EuropeMap')
        assert emu.read('sEuropeMapPast', 1)
        emu.screenshot(ROOT / 'test-output/evac-map.png')
        emu.press('B', 180)
        emu.press('B', 180)
        emu.press('B', 90)
        return_service(emu)
        board_train(emu)
        assert emu.var(EVAC) == 2
        cross(emu)
        cross(emu)
        assert_relocated(emu)
        keeper(emu)
        emu.state(ROOT / 'test-output/evac-returned.state')
        cross(emu)
        return_to_ada(emu)
        before = preserved(emu)
        report(emu)
        assert emu.var(EVAC) == 2 and preserved(emu) == before
        print('PASS: reception exit, repeat train, Celebi return, relocated Elise, era map and Ada acknowledgement', flush=True)

        load_checkpoint(emu, 'departure-booking', args.legacy)
        # This checkpoint has an actual booked Oxford trip; delivered news is
        # a setup fixture for testing the historical train on that itinerary.
        emu.write(emu.read('gSaveBlock1Ptr') + 0x1000 + (NEWS - 0x4000) * 2, 4, 2)
        board_train(emu)
        emu.state(ROOT / 'test-output/evac-booking.state')
        cross(emu)
        resume_booking(emu)
        print('PASS: historical train and Celebi return preserve an actual pending Oxford rail journey', flush=True)
        check_unfinished_return(emu)
    finally:
        emu.close()
