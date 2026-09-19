"""Elise's message, reply, present-day account and capacity-safe reward."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, return_to_ada, report
from test_evac import RECEPTION, return_service, board_train, elise
from test_departure import back_to_refuge, visit_post
from test_time import cross, ARRIVAL, keeper, preserved
from test_country import wait_menu

MESSAGE = 0x40E4


def luxury_balls(emu):
    bag = emu.read('gSaveBlock1Ptr') + 0x430
    key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
    return sum(emu.read(bag + i * 4 + 2, 2) ^ key for i in range(13)
               if emu.read(bag + i * 4, 2) == 11)


def offer(emu):
    assert emu.location() == RECEPTION
    emu.walk('RIGHT', 3)
    emu.press('UP')
    emu.press('A', 180)
    wait_menu(emu, 'Task_YesNoMenu_HandleInput')
    emu.frames(60)


def to_keeper(emu):
    return_service(emu)
    back_to_refuge(emu)


def to_elise(emu):
    assert emu.location() == ARRIVAL
    visit_post(emu)
    board_train(emu)


def finish_account(emu):
    if emu.location() == (43, 12, 18, 14):
        report(emu)
        return
    if emu.var(MESSAGE) == 1:
        to_keeper(emu)
        keeper(emu)
    if emu.var(MESSAGE) == 2:
        to_elise(emu)
        elise(emu)
    assert emu.var(MESSAGE) == 3
    cross(emu)
    return_to_ada(emu)
    report(emu)


def free_ball_slot(emu):
    save = emu.read('gSaveBlock1Ptr')
    key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
    emu.write(save + 0x430, 0, 2)
    emu.write(save + 0x432, key, 2)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--legacy', action='store_true')
    args = p.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'evac-arrival', args.legacy)
        elise(emu)
        assert emu.var(MESSAGE) == 0
        load_checkpoint(emu, 'evac-complete', args.legacy)
        assert emu.var(MESSAGE) == 0
        baseline = luxury_balls(emu)
        start = ROOT / 'test-output/message-ready.state'
        emu.state(start)
        for choice in ('B', 'NO'):
            emu.state(start, True)
            offer(emu)
            if choice == 'NO':
                emu.press('DOWN')
                emu.press('A', 180)
            else:
                emu.press('B', 180)
            emu.finish_dialogue()
            assert emu.var(MESSAGE) == 0
        emu.state(start, True)
        offer(emu)
        emu.press('A', 180)
        emu.finish_dialogue()
        emu.walk('LEFT', 3)
        assert emu.var(MESSAGE) == 1
        elise(emu)
        emu.state(ROOT / 'test-output/message-active.state')
        # Present-day Ada cannot skip the delivery and reply.
        cross(emu)
        return_to_ada(emu)
        report(emu)
        assert emu.var(MESSAGE) == 1 and luxury_balls(emu) == baseline
        from test_celebi import visit_forest
        visit_forest(emu)
        cross(emu)
        keeper(emu)
        assert emu.var(MESSAGE) == 2
        keeper(emu)
        assert emu.var(MESSAGE) == 2
        emu.state(ROOT / 'test-output/message-delivered.state')
        to_elise(emu)
        elise(emu)
        assert emu.var(MESSAGE) == 3
        elise(emu)
        assert emu.var(MESSAGE) == 3
        emu.state(ROOT / 'test-output/message-acknowledged.state')
        cross(emu)
        return_to_ada(emu)
        emu.state(ROOT / 'test-output/message-report.state')
        before = preserved(emu)
        report(emu)
        assert emu.var(MESSAGE) == 4 and luxury_balls(emu) == baseline + 1
        after = preserved(emu)
        assert before[:3] == after[:3] and before[4:] == after[4:]
        report(emu)
        assert preserved(emu) == after and luxury_balls(emu) == baseline + 1
        emu.state(ROOT / 'test-output/message-complete.state')
        # Revisit the past after archival; neither NPC can roll progress back.
        visit_forest(emu)
        cross(emu)
        keeper(emu)
        to_elise(emu)
        elise(emu)
        assert emu.var(MESSAGE) == 4 and luxury_balls(emu) == baseline + 1
        print('PASS: check-in gate, No/B, delivery, reply, era detour, no early archive, one reward and repeat visits', flush=True)

        emu.state(ROOT / 'test-output/message-report.state', True)
        save = emu.read('gSaveBlock1Ptr')
        key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
        for i in range(13):
            emu.write(save + 0x430 + i * 4, 4, 2)
            emu.write(save + 0x432 + i * 4, 999 ^ key, 2)
        report(emu)
        assert emu.var(MESSAGE) == 3 and luxury_balls(emu) == 0
        emu.state(ROOT / 'test-output/message-pending.state')
        free_ball_slot(emu)
        report(emu)
        report(emu)
        assert emu.var(MESSAGE) == 4 and luxury_balls(emu) == 1
        print('PASS: full Poke Balls pocket preserves the account; freeing a slot grants exactly one Luxury Ball', flush=True)
    finally:
        emu.close()
