"""Port account: real Oxford trip, optional report and sixteenth record."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, return_to_ada, visit_forest, researcher, report
from test_time import cross, preserved, PRESENT
from test_garden import choose
from test_journal import inspect
from test_journal_pages import inspect_pages
from test_le_havre import PORT, finish_port
from test_dock_care import rest

ACCOUNT = 0x40D9
ADA = (43, 12, 18, 14)


def archive(emu, choice='YES'):
    assert emu.location() == ADA
    before = preserved(emu)
    progress = tuple(emu.var(v) for v in range(0x40DA, 0x4100))
    researcher(emu)
    if emu.var(ACCOUNT) == 0: choose(emu, choice)
    else: emu.finish_dialogue()
    assert preserved(emu) == before
    assert tuple(emu.var(v) for v in range(0x40DA, 0x4100)) == progress
    assert not emu.read('sLockFieldControls', 1)


def finish_account(emu):
    if emu.location() == PORT: cross(emu)
    if emu.location() == PRESENT: return_to_ada(emu)
    archive(emu)
    assert emu.var(ACCOUNT) == 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true'); args = parser.parse_args()
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        load_checkpoint(emu, 'dock-check-active', args.legacy)
        cross(emu); return_to_ada(emu); report(emu)
        assert emu.var(ACCOUNT) == 0 and emu.var(0x40DA) == 1
        load_checkpoint(emu, 'dock-check-complete', args.legacy)
        inspect(emu, 49, 32767, 'port-account-ready')
        cross(emu); return_to_ada(emu)
        for choice in ('NO', 'B'):
            archive(emu, choice); assert emu.var(ACCOUNT) == 0
        emu.state(ROOT / 'test-output/port-account-ready.state')
        archive(emu); assert emu.var(ACCOUNT) == 1
        archive(emu)
        inspect(emu, 50, 65535, 'port-account-complete')
        inspect_pages(emu, 65535, 'port-account-complete')
        emu.state(ROOT / 'test-output/port-account-complete.state')
        visit_forest(emu); finish_port(emu); rest(emu)
        assert emu.var(ACCOUNT) == 1
        emu.state(ROOT / 'test-output/port-account-returned.state')
        finish_account(emu)
        print('PASS: dock prerequisite, real Oxford journey, No/B, archive and repeated report', flush=True)
        print('PASS: sixteenth record, mask 65535 paging, read-only journal, Le Havre revisit and care', flush=True)
    finally: emu.close()
