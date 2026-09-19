"""Amiens account: actual Oxford journey, optional archive and persistent record."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, return_to_ada, visit_forest, researcher, report
from test_time import cross, preserved
from test_garden import choose
from test_journal import inspect
from test_amiens import reach_post, board
from test_amiens_care import rest
from test_reunion import relocated
ACCOUNT=0x40DF

def archive(emu, choice='YES'):
    before=preserved(emu)
    progress=tuple(emu.var(v) for v in range(0x40E0,0x4100))
    researcher(emu)
    if emu.var(ACCOUNT)==0:choose(emu,choice)
    else:emu.finish_dialogue()
    assert preserved(emu)==before
    assert tuple(emu.var(v) for v in range(0x40E0,0x4100))==progress
    assert not emu.read('sLockFieldControls',1)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'reunion-verified',args.legacy)
        cross(emu);return_to_ada(emu);report(emu)
        assert emu.var(ACCOUNT)==0 and emu.var(0x40E0)==5
        load_checkpoint(emu,'reunion-complete',args.legacy)
        inspect(emu,34,511,'account-ready')
        cross(emu);return_to_ada(emu)
        for choice in ('NO','B'):
            archive(emu,choice);assert emu.var(ACCOUNT)==0
        emu.state(ROOT/'test-output/amiens-account-ready.state')
        archive(emu);assert emu.var(ACCOUNT)==1
        archive(emu)
        inspect(emu,35,1023,'account-complete')
        emu.state(ROOT/'test-output/amiens-account-complete.state')
        visit_forest(emu);reach_post(emu);board(emu)
        relocated(emu);rest(emu)
        assert emu.var(ACCOUNT)==1
        print('PASS: reunion prerequisite, real Oxford journey, No/B, archive and repeat report',flush=True)
        print('PASS: journal leads and tenth milestone; party/items/progress preserved; Amiens revisit and care',flush=True)
    finally:emu.close()
