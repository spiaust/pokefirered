"""Beauvais supply run and repeatable healing; real travel and dialogue input."""
import argparse
import re
import struct
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, visit_forest
from test_time import cross, preserved, PRESENT, ARRIVAL
from test_evac import RECEPTION, board_train, return_service, host
from test_departure import POST, visit_post, dispatcher
from test_country import wait_menu

RELIEF = 0x40E3
SLOTS = {int(n): (int(g), int(a)) for n, g, a in re.findall(
    r'SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),\s*(\d+),',
    (ROOT / 'src/pokemon.c').read_text())}


def host_prompt(emu):
    assert emu.location() == RECEPTION
    emu.walk('UP', 2)
    emu.press('UP')
    emu.press('A', 180)


def host_choice(emu, choice='YES'):
    host_prompt(emu)
    wait_menu(emu, 'Task_YesNoMenu_HandleInput')
    emu.frames(60)
    if choice == 'NO':
        emu.press('DOWN')
    emu.press('B' if choice == 'B' else 'A', 180)
    emu.finish_dialogue()
    emu.walk('DOWN', 2)
    assert emu.location() == RECEPTION


def to_reception(emu):
    if emu.location() == PRESENT:
        cross(emu)
    if emu.location() == ARRIVAL:
        visit_post(emu)
    if emu.location() == POST:
        board_train(emu)
    assert emu.location() == RECEPTION


def finish_relief(emu):
    if emu.var(RELIEF) < 2:
        to_reception(emu)
        if emu.var(RELIEF) == 0:
            host_choice(emu)
        return_service(emu)
        dispatcher(emu)
    to_reception(emu)
    if emu.var(RELIEF) == 2:
        host(emu)
    assert emu.var(RELIEF) == 3


def decoded_mon(emu, index):
    mon = emu.symbols['gPlayerParty'] + index * 100
    personality = emu.read(mon)
    key = personality ^ emu.read(mon + 4)
    data = bytearray().join((emu.read(mon + 32 + i) ^ key).to_bytes(4, 'little')
                           for i in range(0, 48, 4))
    growth, attacks = (s * 12 for s in SLOTS[personality % 24])
    return mon, key, data, growth, attacks


def health(emu):
    result = []
    for i in range(emu.read('gPlayerPartyCount', 1)):
        mon, _, data, growth, attacks = decoded_mon(emu, i)
        moves = struct.unpack_from('<4H', data, attacks)
        bonuses = data[growth + 8]
        max_pp = tuple(emu.read(emu.symbols['gBattleMoves'] + move * 12 + 4, 1)
                       * (5 + ((bonuses >> (j * 2)) & 3)) // 5
                       for j, move in enumerate(moves))
        result.append((emu.read(mon + 0x56, 2), emu.read(mon + 0x58, 2),
                       emu.read(mon + 0x50), tuple(data[attacks + 8:attacks + 12]), max_pp))
    return tuple(result)


def tire_party(emu):
    # A targeted health fixture: damage/status/empty PP; species and moves stay intact.
    for i in range(emu.read('gPlayerPartyCount', 1)):
        mon, key, data, _, attacks = decoded_mon(emu, i)
        emu.write(mon + 0x56, 1, 2)
        emu.write(mon + 0x50, 0x10)  # Burn, which has no overworld step damage.
        data[attacks + 8:attacks + 12] = bytes(4)
        emu.write(mon + 28, sum(struct.unpack('<24H', data)) & 0xFFFF, 2)
        for offset in range(0, 48, 4):
            emu.write(mon + 32 + offset, int.from_bytes(data[offset:offset + 4], 'little') ^ key)


def assert_healed(emu):
    assert all(hp == maximum and status == 0 and pp == max_pp
               for hp, maximum, status, pp, max_pp in health(emu)), health(emu)


def rest(emu):
    # Check non-health identity before the two walking steps can alter friendship.
    host_prompt(emu)
    wait_menu(emu, 'Task_YesNoMenu_HandleInput')
    emu.frames(60)
    before = preserved(emu)[1:]
    identity = []
    for i in range(emu.read('gPlayerPartyCount', 1)):
        mon, _, data, _, attacks = decoded_mon(emu, i)
        data[attacks + 8:attacks + 12] = bytes(4)
        identity.append((bytes(emu.read(mon + j, 1) for j in range(28)), bytes(data)))
    emu.press('A', 180)
    emu.finish_dialogue()
    assert_healed(emu)
    assert preserved(emu)[1:] == before
    for i, expected in enumerate(identity):
        mon, _, data, _, attacks = decoded_mon(emu, i)
        data[attacks + 8:attacks + 12] = bytes(4)
        assert (bytes(emu.read(mon + j, 1) for j in range(28)), bytes(data)) == expected
    emu.walk('DOWN', 2)
    assert emu.location() == RECEPTION and emu.var(RELIEF) == 3


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true')
    args = parser.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'evac-complete', args.legacy)
        host(emu)
        assert emu.var(RELIEF) == 0
        return_service(emu)
        dispatcher(emu)
        assert emu.var(RELIEF) == 0
        load_checkpoint(emu, 'message-complete', args.legacy)
        visit_forest(emu)
        to_reception(emu)
        emu.state(ROOT / 'test-output/relief-ready.state')
        for choice in ('NO', 'B'):
            host_choice(emu, choice)
            assert emu.var(RELIEF) == 0
        host_choice(emu)
        assert emu.var(RELIEF) == 1
        host(emu)  # Reminder cannot deliver a parcel not yet collected.
        assert emu.var(RELIEF) == 1
        emu.state(ROOT / 'test-output/relief-active.state')
        return_service(emu)
        before = preserved(emu)[1:]
        dispatcher(emu)
        assert emu.var(RELIEF) == 2 and preserved(emu)[1:] == before
        dispatcher(emu)
        assert emu.var(RELIEF) == 2
        emu.state(ROOT / 'test-output/relief-parcel.state')
        cross(emu)
        assert emu.var(RELIEF) == 2
        emu.state(ROOT / 'test-output/relief-returned.state')
        to_reception(emu)
        host(emu)
        assert emu.var(RELIEF) == 3 and emu.var(0x40E4) == 4
        emu.state(ROOT / 'test-output/relief-complete.state')
        tire_party(emu)
        tired = health(emu)
        emu.state(ROOT / 'test-output/relief-tired.state')
        for choice in ('NO', 'B'):
            host_choice(emu, choice)
            assert health(emu) == tired
        rest(emu)
        rest(emu)
        return_service(emu)
        dispatcher(emu)
        assert emu.var(RELIEF) == 3
        board_train(emu)
        rest(emu)
        print('PASS: archive gate, No/B, request, parcel, era detour, delivery and repeat visits', flush=True)
        print('PASS: repeatable free rest restores HP, status and PP; No/B preserves tired party', flush=True)
        emu.state(ROOT / 'test-output/relief-active.state', True)
        save = emu.read('gSaveBlock1Ptr')
        key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
        for i in range(42):
            emu.write(save + 0x310 + i * 4, 13, 2)
            emu.write(save + 0x312 + i * 4, 999 ^ key, 2)
        before = preserved(emu)[1:]
        finish_relief(emu)
        assert preserved(emu)[1:] == before
        print('PASS: a full Items pocket does not block or consume the quest parcel', flush=True)
        # A six-member fixture catches partial-party healing, including a fainted slot.
        mon = emu.symbols['gPlayerParty']
        sample = bytes(emu.read(mon + j, 1) for j in range(100))
        for i in range(1, 6):
            for j, value in enumerate(sample):
                emu.write(mon + i * 100 + j, value, 1)
        emu.write('gPlayerPartyCount', 6, 1)
        tire_party(emu)
        emu.write(mon + 5 * 100 + 0x56, 0, 2)
        rest(emu)
        assert len(health(emu)) == 6
        print('PASS: all six party slots heal, including a fainted Pokemon', flush=True)
    finally:
        emu.close()
