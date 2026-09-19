"""Rouen route book: optional request, pickup, return, persistence and full Bag."""
import argparse
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_rouen import ROUEN,leon,board,leave
from test_amiens import AMIENS,reach_post,board as board_amiens
from test_time import cross,preserved
from test_journal import inspect
STORY=0x40DC

def visible(emu):
    for i in range(16):
        obj=emu.symbols['gObjectEvents']+i*36
        if (emu.read(obj,1)&1 and emu.read(obj+8,1)==4
            and emu.read(obj+9,1)==34 and emu.read(obj+10,1)==43):return True
    return False

def book(emu,collect=True):
    assert emu.location()==ROUEN
    emu.walk('RIGHT',15);emu.walk('UP',6);emu.walk('RIGHT',8);emu.walk('UP',4)
    assert emu.location()==(43,34,33,6)
    assert visible(emu)==(emu.var(STORY)==1)
    if collect:
        before=preserved(emu)
        emu.press('LEFT');emu.press('A',180)
        assert emu.read('sLockFieldControls',1)
        emu.screenshot(ROOT/'test-output/route-book-found.png')
        emu.finish_dialogue()
        assert emu.var(STORY)==2 and not visible(emu)
        assert preserved(emu)==before
    emu.walk('DOWN',4);emu.walk('LEFT',21);emu.walk('DOWN',6);emu.walk('LEFT',2)
    assert emu.location()==ROUEN

def finish_book(emu):
    if emu.location()!=ROUEN:
        if emu.location()!=AMIENS:reach_post(emu);board_amiens(emu)
        board(emu)
    if emu.var(STORY)==0:leon(emu,'YES')
    if emu.var(STORY)==1:book(emu)
    if emu.var(STORY)==2:leon(emu)
    assert emu.var(STORY)==3
    book(emu,False)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'rouen-arrival',args.legacy)
        book(emu,False);leon(emu);assert emu.var(STORY)==0
        emu.state(ROOT/'test-output/route-book-ready.state')
        for choice in ('NO','B'):leon(emu,choice);assert emu.var(STORY)==0
        inspect(emu,41,4095,'book-ready')
        leon(emu,'YES');leon(emu);assert emu.var(STORY)==1
        emu.state(ROOT/'test-output/route-book-active.state')
        inspect(emu,42,4095,'book-active')
        leave(emu);board(emu);book(emu)
        emu.state(ROOT/'test-output/route-book-found.state')
        inspect(emu,43,4095,'book-found')
        cross(emu);emu.state(ROOT/'test-output/route-book-returned.state')
        finish_book(emu);leon(emu)
        emu.state(ROOT/'test-output/route-book-complete.state')
        inspect(emu,44,8191,'book-complete')
        leave(emu);board(emu);book(emu,False)
        print('PASS: welcome gate, No/B, request, reminder, far-bank pickup and return',flush=True)
        print('PASS: pickup visibility, repeat interactions, both return routes and four journal leads',flush=True)
        emu.state(ROOT/'test-output/route-book-active.state',True)
        save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
        for i in range(42):
            emu.write(save+0x310+i*4,13,2);emu.write(save+0x312+i*4,999^key,2)
        finish_book(emu)
        print('PASS: full Items pocket does not block collection or consume items',flush=True)
    finally:emu.close()
