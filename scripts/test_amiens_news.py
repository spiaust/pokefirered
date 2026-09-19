"""Amiens bulletin: prerequisite, checked news, return routes and saves."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, visit_forest
from test_amiens import AMIENS, board, leave, reach_post, notice
from test_reunion import talk
from test_time import preserved, cross
from test_garden import choose
from test_journal import inspect
STORY=0x40DE

def porter(emu,choice='YES'):
    assert emu.location()==AMIENS
    emu.walk('RIGHT',8);emu.walk('UP',3)
    before=preserved(emu);emu.press('UP');emu.press('A',180)
    if emu.var(STORY)==0 and emu.var(0x40DF)==1:choose(emu,choice)
    elif emu.var(STORY)==4:choose(emu,'B')
    else:emu.finish_dialogue()
    assert preserved(emu)==before
    emu.walk('DOWN',3);emu.walk('LEFT',8)
    assert emu.location()==AMIENS

def finish_news(emu):
    if emu.location()!=AMIENS:
        reach_post(emu);board(emu)
    if emu.var(STORY)==0:porter(emu)
    if emu.var(STORY)==1:notice(emu)
    if emu.var(STORY)==2:porter(emu)
    if emu.var(STORY)==3:talk(emu,'nora')
    assert emu.var(STORY)==4

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'reunion-complete',args.legacy)
        porter(emu);notice(emu);assert emu.var(STORY)==0
        load_checkpoint(emu,'amiens-account-complete',args.legacy)
        visit_forest(emu);reach_post(emu);board(emu)
        for choice in ('NO','B'):
            porter(emu,choice);assert emu.var(STORY)==0
        notice(emu);assert emu.var(STORY)==0
        emu.state(ROOT/'test-output/amiens-news-ready.state')
        inspect(emu,35,1023,'news-ready')
        porter(emu);porter(emu);assert emu.var(STORY)==1
        talk(emu,'nora');assert emu.var(STORY)==1
        emu.state(ROOT/'test-output/amiens-news-active.state')
        inspect(emu,36,1023,'news-active')
        notice(emu);notice(emu);assert emu.var(STORY)==2
        talk(emu,'nora');assert emu.var(STORY)==2
        emu.state(ROOT/'test-output/amiens-news-board.state')
        inspect(emu,37,1023,'news-board')
        cross(emu);emu.state(ROOT/'test-output/amiens-news-returned.state')
        reach_post(emu);board(emu);porter(emu);porter(emu)
        assert emu.var(STORY)==3
        emu.state(ROOT/'test-output/amiens-news-checked.state')
        inspect(emu,38,1023,'news-checked')
        talk(emu,'nora');assert emu.var(STORY)==4
        emu.state(ROOT/'test-output/amiens-news-complete.state')
        inspect(emu,39,2047,'news-complete')
        notice(emu);porter(emu);talk(emu,'nora')
        leave(emu);board(emu);assert emu.var(STORY)==4
        print('PASS: account prerequisite, early board/Nora gates, No/B, notice, porter verification and Nora report',flush=True)
        print('PASS: repeats, both return routes, five journal leads and unchanged party/items/modern progress',flush=True)
    finally:emu.close()
