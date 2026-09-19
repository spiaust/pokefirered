"""Celebi prologue: badge gate, consent, sighting, report and one-time reward."""
import argparse
from emulator import Emulator, ROOT
from test_country import wait_menu
from test_tour import travel, item_count
from test_trainers import money
from test_ride import party

STORY = 0x40EE
CANDY = 68


def load_checkpoint(emu, name, legacy=False):
    if not legacy:
        emu.state(ROOT / f'test-output/{name}.state', True)
        return
    emu.battery(ROOT / f'test-output/{name}.sav', True)
    emu.frames(600)
    emu.press('START', 480)
    emu.press('START', 180)
    emu.press('A', 300)
    emu.frames(300)
    emu.press('B', 90)
    emu.finish_dialogue()


def researcher(emu):
    assert emu.location() == (43, 12, 18, 14), emu.location()
    emu.press('DOWN')
    emu.press('A', 180)


def report(emu):
    researcher(emu)
    emu.finish_dialogue()
    assert not emu.read('sLockFieldControls', 1)


def forest(emu):
    assert emu.location() == (43, 17, 15, 24), emu.location()
    emu.press('LEFT')
    emu.press('A', 180)


def visit_forest(emu):
    assert emu.location() == (43, 12, 18, 14), emu.location()
    emu.walk('LEFT', 2)
    travel(emu, 4)
    emu.walk('LEFT', 1)
    emu.walk('DOWN', 10)
    emu.walk('DOWN', 24)
    assert emu.location() == (43, 17, 15, 24), emu.location()


def return_to_ada(emu):
    assert emu.location() == (43, 17, 15, 24), emu.location()
    emu.walk('UP', 25)
    emu.walk('UP', 9)
    emu.walk('RIGHT', 1)
    travel(emu, 3)
    emu.walk('RIGHT', 2)


def invariant(emu):
    return (party(emu), money(emu), emu.var(0x40F0),
            tuple(emu.var(v) for v in (0x40FB, 0x40FD, 0x40FF)),
            emu.var(0x40F7))


def accept_sighting(emu):
    forest(emu)
    wait_menu(emu, 'Task_YesNoMenu_HandleInput')
    emu.frames(60)
    emu.press('A', 180)
    emu.finish_dialogue()
    assert emu.var(STORY) == 2
    assert not emu.read('sLockFieldControls', 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true', help='Cold-load existing battery saves.')
    args = parser.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'start-england', args.legacy)
        emu.walk('RIGHT', 1)
        travel(emu, 3)
        emu.walk('RIGHT', 2)
        report(emu)
        assert emu.var(STORY) == 0
        visit_forest(emu)
        forest(emu)
        emu.finish_dialogue()
        assert emu.var(STORY) == 0 and not emu.in_battle()
        print('PASS: pre-badge researcher and early Celebi visit cannot advance the chapter', flush=True)

        load_checkpoint(emu, 'electric-gym-complete', args.legacy)
        assert emu.var(STORY) == 0, 'Existing progress must initialize the prologue as unstarted'
        emu.walk('DOWN', 10)
        emu.frames(180)
        emu.walk('DOWN', 4)
        emu.walk('RIGHT', 1)
        travel(emu, 3)
        emu.walk('RIGHT', 2)
        before = invariant(emu)
        candy = item_count(emu, CANDY)
        researcher(emu)
        wait_menu(emu, 'Task_YesNoMenu_HandleInput')
        emu.frames(60)
        prompt = ROOT / 'test-output/celebi-offer.state'
        emu.state(prompt)
        for decline in ('B', 'NO'):
            emu.state(prompt, True)
            if decline == 'NO':
                emu.press('DOWN')
                emu.press('A', 180)
            else:
                emu.press('B', 180)
            emu.finish_dialogue()
            assert emu.var(STORY) == 0 and invariant(emu) == before
        emu.state(prompt, True)
        emu.press('A', 180)
        emu.finish_dialogue()
        assert emu.var(STORY) == 1
        report(emu)
        assert emu.var(STORY) == 1 and item_count(emu, CANDY) == candy
        emu.state(ROOT / 'test-output/celebi-active.state')
        print('PASS: earned Thunderbadge unlocks offer; No/B, acceptance, and repeat directions work', flush=True)

        visit_forest(emu)
        emu.frames(60)
        emu.screenshot(ROOT / 'test-output/celebi-forest.png')
        emu.state(ROOT / 'test-output/celebi-forest.state')
        forest(emu)
        wait_menu(emu, 'Task_YesNoMenu_HandleInput')
        emu.frames(60)
        emu.state(prompt)
        for decline in ('B', 'NO'):
            emu.state(prompt, True)
            if decline == 'NO':
                emu.press('DOWN')
                emu.press('A', 180)
            else:
                emu.press('B', 180)
            emu.finish_dialogue()
            assert emu.var(STORY) == 1 and invariant(emu) == before
        emu.state(ROOT / 'test-output/celebi-forest.state', True)
        accept_sighting(emu)
        forest(emu)
        emu.finish_dialogue()
        assert emu.var(STORY) == 2 and invariant(emu) == before
        emu.state(ROOT / 'test-output/celebi-sighting.state')
        return_to_ada(emu)
        emu.state(ROOT / 'test-output/celebi-report.state')
        report(emu)
        assert emu.var(STORY) == 3 and item_count(emu, CANDY) == candy + 1
        report(emu)
        assert item_count(emu, CANDY) == candy + 1 and invariant(emu) == before
        emu.state(ROOT / 'test-output/celebi-complete.state')
        visit_forest(emu)
        forest(emu)
        wait_menu(emu, 'Task_YesNoMenu_HandleInput')
        emu.frames(60)
        emu.press('B', 180)
        emu.finish_dialogue()
        assert emu.var(STORY) == 3 and emu.location() == (43, 17, 15, 24)
        print('PASS: optional sighting, report, one reward and repeat visits preserve team and regional progress', flush=True)

        emu.state(ROOT / 'test-output/celebi-report.state', True)
        save = emu.read('gSaveBlock1Ptr')
        key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
        for i in range(42):
            emu.write(save + 0x310 + i * 4, 13, 2)
            emu.write(save + 0x312 + i * 4, 999 ^ key, 2)
        report(emu)
        assert emu.var(STORY) == 2 and item_count(emu, CANDY) == 0
        emu.state(ROOT / 'test-output/celebi-pending.state')
        emu.write(save + 0x310, 0, 2)
        emu.write(save + 0x312, key, 2)
        report(emu)
        report(emu)
        assert emu.var(STORY) == 3 and item_count(emu, CANDY) == 1
        print('PASS: full Bag preserves report; freeing space permits exactly one reward', flush=True)
    finally:
        emu.close()
