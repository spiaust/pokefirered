"""Southampton care: luggage-task gate, healing, persistence and return routes."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_luggage import worker, finish_luggage
from test_southampton import SOUTH, host, clerk, finish_southampton
from test_relief import health, tire_party, assert_healed
from test_rouen_care import identity
from test_time import preserved, cross
from test_country import wait_menu
from test_journal import inspect


def rest(emu, choice='YES'):
    assert emu.location() == SOUTH
    emu.walk('UP', 2); emu.walk('RIGHT', 1)
    emu.press('RIGHT'); emu.press('A', 180)
    wait_menu(emu, 'Task_YesNoMenu_HandleInput'); emu.frames(60)
    before = preserved(emu); ids = identity(emu); tired = health(emu)
    progress = tuple(emu.var(v) for v in range(0x40D7, 0x4100))
    emu.screenshot(ROOT / 'test-output/south-care-offer.png')
    if choice == 'NO': emu.press('DOWN')
    emu.press('B' if choice == 'B' else 'A', 180)
    emu.finish_dialogue()
    assert not emu.read('sLockFieldControls', 1)
    assert preserved(emu)[1:] == before[1:]
    assert identity(emu) == ids
    assert tuple(emu.var(v) for v in range(0x40D7, 0x4100)) == progress
    if choice == 'YES': assert_healed(emu)
    else: assert health(emu) == tired and preserved(emu) == before
    emu.walk('LEFT', 1); emu.walk('DOWN', 2)
    assert emu.location() == SOUTH


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true'); args = parser.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'luggage-active', args.legacy)
        tire_party(emu); tired = health(emu); worker(emu)
        assert emu.var(0x40D7) == 1 and health(emu) == tired
        finish_luggage(emu); assert health(emu) == tired
        emu.state(ROOT / 'test-output/south-care-tired.state')
        rest(emu, 'NO'); rest(emu, 'B'); rest(emu); rest(emu)
        emu.state(ROOT / 'test-output/south-care-rested.state')
        inspect(emu, 55, 262143, 'south-care')
        host(emu, 'YES'); clerk(emu); tire_party(emu); rest(emu)
        cross(emu); finish_southampton(emu); tire_party(emu); rest(emu)
        print('PASS: luggage-task gate, no automatic healing, No/B, repeat care and both return routes', flush=True)
        load_checkpoint(emu, 'luggage-complete', args.legacy)
        tire_party(emu); rest(emu)
        print('PASS: existing completed luggage-task save unlocks care immediately', flush=True)
        mon = emu.symbols['gPlayerParty']
        sample = bytes(emu.read(mon + j, 1) for j in range(100))
        for i in range(1, 6):
            for j, value in enumerate(sample): emu.write(mon + i * 100 + j, value, 1)
        emu.write('gPlayerPartyCount', 6, 1); tire_party(emu)
        emu.write(mon + 500 + 0x56, 0, 2)
        save = emu.read('gSaveBlock1Ptr')
        key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
        for i in range(42):
            emu.write(save + 0x310 + i * 4, 13, 2)
            emu.write(save + 0x312 + i * 4, 999 ^ key, 2)
        rest(emu); assert len(health(emu)) == 6
        print('PASS: six-member party, fainted slot, full Bag, identity and progress preserved', flush=True)
    finally: emu.close()
