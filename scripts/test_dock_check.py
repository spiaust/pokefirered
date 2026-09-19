"""Le Havre dock instructions: gates, choices, confirmation and persistence."""
import argparse
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_le_havre import PORT,clerk,captain,finish_port
from test_garden import choose
from test_time import preserved,cross
from test_journal import inspect
from test_journal_pages import inspect_pages
STORY=0x40DA

def worker(emu,choice='YES'):
    assert emu.location()==PORT
    emu.walk('UP',2);emu.walk('RIGHT',1)
    before=preserved(emu);emu.press('RIGHT');emu.press('A',180)
    if emu.var(STORY)==3:choose(emu,'B')
    elif emu.var(STORY)==0 and emu.var(0x40DB)==2:choose(emu,choice)
    else:emu.finish_dialogue()
    assert preserved(emu)==before
    emu.walk('LEFT',1);emu.walk('DOWN',2)
    assert emu.location()==PORT

def notice(emu):
    assert emu.location()==PORT
    emu.walk('UP',2);before=preserved(emu)
    emu.press('UP');emu.press('A',180);emu.frames(180)
    assert emu.read('sLockFieldControls',1)
    emu.screenshot(ROOT/'test-output/dock-notice.png');emu.finish_dialogue()
    assert preserved(emu)==before
    emu.walk('DOWN',2);assert emu.location()==PORT

def finish_check(emu):
    if emu.location()!=PORT:finish_port(emu)
    if emu.var(STORY)==0:worker(emu)
    if emu.var(STORY)==1:notice(emu)
    if emu.var(STORY)==2:captain(emu)
    assert emu.var(STORY)==3

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'le-havre-arrival',args.legacy)
        worker(emu);notice(emu);assert emu.var(STORY)==0
        captain(emu);assert emu.var(STORY)==0
        emu.state(ROOT/'test-output/dock-check-ready.state')
        inspect(emu,46,16383,'dock-ready')
        for choice in ('NO','B'):worker(emu,choice);assert emu.var(STORY)==0
        worker(emu);worker(emu);assert emu.var(STORY)==1
        captain(emu);assert emu.var(STORY)==1
        emu.state(ROOT/'test-output/dock-check-active.state');inspect(emu,47,16383,'dock-active')
        cross(emu);emu.state(ROOT/'test-output/dock-check-returned.state')
        finish_port(emu);assert emu.var(STORY)==1
        notice(emu);notice(emu);worker(emu);assert emu.var(STORY)==2
        emu.state(ROOT/'test-output/dock-check-notice.state');inspect(emu,48,16383,'dock-notice')
        captain(emu,'NO');assert emu.var(STORY)==3
        emu.state(ROOT/'test-output/dock-check-complete.state');inspect(emu,49,32767,'dock-complete')
        inspect_pages(emu,32767,'dock-complete')
        worker(emu);notice(emu);captain(emu)
        captain(emu,'YES');clerk(emu);assert emu.var(STORY)==3
        print('PASS: welcome gate, early notice/captain, No/B, request, posted notice and confirmation',flush=True)
        print('PASS: repeats, both return routes, four journal leads, fifteenth milestone and paging',flush=True)
    finally:emu.close()
