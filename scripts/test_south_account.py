"""Southampton account: real Oxford trip, optional report and nineteenth record."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, return_to_ada, visit_forest, researcher, report
from test_time import cross, preserved, PRESENT
from test_garden import choose
from test_journal import inspect
from test_journal_pages import inspect_pages
from test_southampton import SOUTH
from test_port_return import destination
from test_southampton_care import rest

ACCOUNT = 0x40D6
ADA = (43, 12, 18, 14)


def archive(emu, choice='YES'):
    assert emu.location() == ADA
    before = preserved(emu)
    progress = tuple(emu.var(v) for v in range(0x40D7, 0x4100))
    researcher(emu)
    if emu.var(ACCOUNT) == 0: choose(emu, choice)
    else: emu.finish_dialogue()
    assert preserved(emu) == before
    assert tuple(emu.var(v) for v in range(0x40D7, 0x4100)) == progress
    assert not emu.read('sLockFieldControls', 1)


def finish_account(emu):
    if emu.location() == SOUTH: cross(emu)
    if emu.location() == PRESENT: return_to_ada(emu)
    archive(emu)
    assert emu.var(ACCOUNT) == 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true'); args = parser.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'luggage-active', args.legacy)
        cross(emu); return_to_ada(emu); report(emu)
        assert emu.var(ACCOUNT) == 0 and emu.var(0x40D7) == 1
        load_checkpoint(emu, 'luggage-complete', args.legacy)
        inspect(emu, 55, 262143, 'south-account-ready')
        cross(emu); return_to_ada(emu)
        for choice in ('NO', 'B'):
            archive(emu, choice); assert emu.var(ACCOUNT) == 0
        emu.state(ROOT / 'test-output/south-account-ready.state')
        archive(emu); assert emu.var(ACCOUNT) == 1
        archive(emu)
        inspect(emu, 56, 524287, 'south-account-complete')
        inspect_pages(emu, 524287, 'south-account-complete')
        emu.state(ROOT / 'test-output/south-account-complete.state')
        visit_forest(emu); destination(emu,2); rest(emu)
        assert emu.var(ACCOUNT) == 1
        emu.state(ROOT / 'test-output/south-account-returned.state')
        finish_account(emu)
        print('PASS: luggage prerequisite, real Oxford journey, No/B, archive and repeated report', flush=True)
        print('PASS: nineteenth record, mask 524287 paging, read-only journal, Southampton revisit and care', flush=True)
    finally: emu.close()
