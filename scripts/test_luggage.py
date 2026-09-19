"""Southampton luggage: welcome gate, optional search, returns and persistence."""
import argparse
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_southampton import SOUTH,host,clerk,finish_southampton
from test_time import cross,preserved
from test_garden import choose
from test_journal import inspect
from test_journal_pages import inspect_pages
STORY=0x40D7

def visible(emu):
    for i in range(16):
        obj=emu.symbols['gObjectEvents']+i*36
        if (emu.read(obj,1)&1 and emu.read(obj+8,1)==5
            and emu.read(obj+9,1)==36 and emu.read(obj+10,1)==43):return True
    return False

def worker(emu,choice='YES'):
    assert emu.location()==SOUTH
    emu.walk('UP',2);emu.walk('RIGHT',1)
    before=preserved(emu);emu.press('RIGHT');emu.press('A',180)
    if emu.var(STORY)==3:choose(emu,'B')
    elif emu.var(STORY)==0 and emu.var(0x40D8)==2:choose(emu,choice)
    else:emu.finish_dialogue()
    assert preserved(emu)==before
    emu.walk('LEFT',1);emu.walk('DOWN',2);assert emu.location()==SOUTH

def bag(emu,collect=True):
    assert emu.location()==SOUTH
    emu.walk('UP',2);emu.walk('LEFT',2)
    assert visible(emu)==(emu.var(STORY)==1)
    if collect:
        before=preserved(emu);emu.press('LEFT');emu.press('A',180)
        assert emu.read('sLockFieldControls',1)
        emu.screenshot(ROOT/'test-output/luggage-found.png');emu.finish_dialogue()
        assert emu.var(STORY)==2 and not visible(emu)
        assert preserved(emu)==before
    emu.walk('RIGHT',2);emu.walk('DOWN',2);assert emu.location()==SOUTH

def finish_luggage(emu):
    if emu.location()!=SOUTH:finish_southampton(emu)
    if emu.var(STORY)==0:worker(emu)
    if emu.var(STORY)==1:bag(emu)
    if emu.var(STORY)==2:worker(emu)
    assert emu.var(STORY)==3
    bag(emu,False)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--legacy',action='store_true');args=p.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'southampton-arrival',args.legacy)
        worker(emu);bag(emu,False);assert emu.var(STORY)==0
        host(emu);emu.state(ROOT/'test-output/luggage-ready.state')
        for choice in ('NO','B'):worker(emu,choice);assert emu.var(STORY)==0
        inspect(emu,52,131071,'luggage-ready')
        worker(emu);worker(emu);assert emu.var(STORY)==1
        emu.state(ROOT/'test-output/luggage-active.state');inspect(emu,53,131071,'luggage-active')
        host(emu,'YES');clerk(emu);bag(emu)
        emu.state(ROOT/'test-output/luggage-found.state');inspect(emu,54,131071,'luggage-found')
        cross(emu);emu.state(ROOT/'test-output/luggage-returned.state')
        finish_luggage(emu);worker(emu)
        emu.state(ROOT/'test-output/luggage-complete.state')
        inspect(emu,55,262143,'luggage-complete');inspect_pages(emu,262143,'luggage-complete')
        host(emu,'YES');clerk(emu);bag(emu,False)
        print('PASS: welcome gate, No/B, request, reminder, pickup and return',flush=True)
        print('PASS: visibility, repeats, both returns, four leads and eighteenth journal milestone',flush=True)
        emu.state(ROOT/'test-output/luggage-active.state',True)
        save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
        for i in range(42):
            emu.write(save+0x310+i*4,13,2);emu.write(save+0x312+i*4,999^key,2)
        bag(emu);worker(emu);assert emu.var(STORY)==3
        print('PASS: full Bag pickup and return preserve inventory and party',flush=True)
    finally:emu.close()
