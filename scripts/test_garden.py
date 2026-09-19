"""Beauvais garden access, Pidgey reunion, object persistence and both exits."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, visit_forest
from test_relief import to_reception, rest
from test_evac import RECEPTION, elise
from test_time import cross, preserved, PRESENT
from test_country import wait_menu
from test_gym_ui import open_key_item
from test_navigation import wait_task

STORY = 0x40E2
GARDEN = (43, 32, 10, 16)


def choose(emu, choice='YES'):
    wait_menu(emu, 'Task_YesNoMenu_HandleInput')
    emu.frames(60)
    if choice == 'NO':
        emu.press('DOWN')
    emu.press('B' if choice == 'B' else 'A', 180)
    emu.finish_dialogue()
    emu.frames(90)


def enter(emu, choice='YES'):
    assert emu.location() == RECEPTION
    emu.walk('RIGHT', 3)
    emu.press('UP')
    before = preserved(emu)
    emu.press('A', 180)
    choose(emu, choice)
    assert preserved(emu) == before
    if choice != 'YES':
        emu.walk('LEFT', 3)
    assert emu.location() == (GARDEN if choice == 'YES' else RECEPTION)


def leave(emu, choice='YES'):
    assert emu.location() == GARDEN
    emu.walk('UP', 1)
    emu.press('UP')
    before = preserved(emu)
    emu.press('A', 180)
    choose(emu, choice)
    assert preserved(emu) == before
    if choice != 'YES':
        emu.walk('DOWN', 1)
    assert emu.location() == (RECEPTION if choice == 'YES' else GARDEN)


def visible(emu, local_id):
    for i in range(16):
        obj = emu.symbols['gObjectEvents'] + i * 36
        if (emu.read(obj, 1) & 1 and emu.read(obj + 8, 1) == local_id
                and emu.read(obj + 9, 1) == 32 and emu.read(obj + 10, 1) == 43):
            return True
    return False


def luc(emu, choice='YES'):
    assert emu.location() == GARDEN
    emu.walk('UP', 1)
    emu.walk('LEFT', 4)
    emu.walk('UP', 6)
    assert emu.location()[2:] == (6, 9), emu.location()
    before = preserved(emu)
    first = emu.var(STORY) == 0
    emu.press('UP')
    emu.press('A', 180)
    if first:
        choose(emu, choice)
    else:
        emu.finish_dialogue()
    assert preserved(emu) == before
    assert visible(emu, 5) == (emu.var(STORY) == 3)
    emu.walk('DOWN', 6)
    emu.walk('RIGHT', 4)
    emu.walk('DOWN', 1)
    assert emu.location() == GARDEN


def pidgey(emu):
    assert emu.location() == GARDEN
    emu.walk('RIGHT', 7)
    emu.walk('UP', 10)
    assert emu.location()[2:] == (17, 6), emu.location()
    before = preserved(emu)
    assert visible(emu, 4) == (emu.var(STORY) < 2)
    if emu.var(STORY) < 2:
        emu.press('UP')
        emu.press('A', 180)
        emu.finish_dialogue()
    assert preserved(emu) == before
    assert visible(emu, 4) == (emu.var(STORY) < 2)
    emu.screenshot(ROOT / ('test-output/garden-bird-' + str(emu.var(STORY)) + '.png'))
    emu.walk('DOWN', 10)
    emu.walk('LEFT', 7)
    assert emu.location() == GARDEN


def home_bird(emu):
    assert emu.location() == GARDEN and emu.var(STORY) == 3
    emu.walk('UP', 1)
    emu.walk('LEFT', 3)
    emu.walk('UP', 6)
    assert emu.location()[2:] == (7, 9)
    assert visible(emu, 5)
    before = preserved(emu)
    emu.press('UP')
    emu.press('A', 180)
    emu.frames(120)
    emu.screenshot(ROOT / 'test-output/garden-reunited.png')
    emu.finish_dialogue()
    assert preserved(emu) == before
    emu.walk('DOWN', 6)
    emu.walk('RIGHT', 3)
    emu.walk('DOWN', 1)


def finish_garden(emu):
    if emu.location() != GARDEN:
        to_reception(emu)
        enter(emu)
    if emu.var(STORY) == 0:
        luc(emu)
    pidgey(emu)
    luc(emu)
    assert emu.var(STORY) == 3
    home_bird(emu)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true')
    args = parser.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'message-complete', args.legacy)
        visit_forest(emu)
        to_reception(emu)
        elise(emu)
        assert emu.location() == RECEPTION and emu.var(STORY) == 0
        load_checkpoint(emu, 'relief-complete', args.legacy)
        for choice in ('NO', 'B'):
            enter(emu, choice)
            assert emu.var(STORY) == 0
        enter(emu)
        emu.screenshot(ROOT / 'test-output/garden-arrival.png')
        emu.state(ROOT / 'test-output/garden-ready.state')
        pidgey(emu)  # Cannot be collected before learning the tune.
        assert emu.var(STORY) == 0
        for choice in ('NO', 'B'):
            luc(emu, choice)
            assert emu.var(STORY) == 0
            leave(emu, choice)
        luc(emu)
        luc(emu)
        assert emu.var(STORY) == 1
        emu.state(ROOT / 'test-output/garden-active.state')
        pidgey(emu)
        assert emu.var(STORY) == 2
        emu.state(ROOT / 'test-output/garden-found.state')
        leave(emu)
        rest(emu)
        emu.state(ROOT / 'test-output/garden-reception.state')
        enter(emu)
        pidgey(emu)  # The bird does not respawn after leaving the garden.
        cross(emu)
        assert emu.location() == PRESENT and emu.var(STORY) == 2
        emu.state(ROOT / 'test-output/garden-returned.state')
        finish_garden(emu)
        emu.state(ROOT / 'test-output/garden-complete.state')
        open_key_item(emu, 361)
        wait_task(emu, 'Task_EuropeMap')
        assert emu.read('sEuropeMapPast', 1) and emu.read('sEuropeMapCurrent', 1) == 4
        emu.screenshot(ROOT / 'test-output/garden-map.png')
        emu.press('B', 180)
        emu.press('B', 180)
        emu.press('B', 90)
        home_bird(emu)
        cross(emu)
        finish_garden(emu)
        assert emu.var(0x40E3) == 3 and emu.var(0x40E4) == 4 and emu.var(0x40E5) == 2
        print('PASS: relief gate, entry/return No/B, shy bird, Luc No/B, tune, pickup and reunion', flush=True)
        print('PASS: both exits, reception rest, era detour, repeat visits, relocated bird and historical Town Map', flush=True)
    finally:
        emu.close()
