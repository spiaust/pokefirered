"""Historical London transport, arrival, return paths and twentieth record."""
import argparse
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_southampton import SOUTH
from test_southampton_care import rest
from test_port_return import destination
from test_time import PRESENT,cross,cancel_checks,preserved,resume_booking
from test_garden import choose
from test_journal import inspect
from test_journal_pages import inspect_pages
from test_gym_ui import open_key_item
from test_navigation import wait_task
LONDON=(43,37,10,16)
STORY=0x40D5

def clerk(emu,choice='YES'):
    assert emu.location()==SOUTH
    emu.walk('UP',1);emu.walk('RIGHT',1)
    before=preserved(emu);emu.press('RIGHT');emu.press('A',180)
    if emu.var(0x40D6)==1:choose(emu,choice)
    else:emu.finish_dialogue()
    assert preserved(emu)==before
    if emu.location()!=LONDON:
        emu.walk('LEFT',1);emu.walk('DOWN',1);assert emu.location()==SOUTH

def rose(emu):
    assert emu.location()==LONDON
    emu.walk('UP',1);emu.walk('LEFT',4);emu.walk('UP',6)
    before=preserved(emu);emu.press('UP');emu.press('A',180);emu.finish_dialogue()
    assert preserved(emu)==before and emu.var(STORY)==2
    emu.walk('DOWN',6);emu.walk('RIGHT',4);emu.walk('DOWN',1)
    assert emu.location()==LONDON

def leave(emu,choice='YES'):
    assert emu.location()==LONDON
    emu.walk('UP',1);before=preserved(emu);emu.press('UP');emu.press('A',180);choose(emu,choice)
    assert preserved(emu)==before
    if choice!='YES':emu.walk('DOWN',1)
    assert emu.location()==(SOUTH if choice=='YES' else LONDON)

def finish_london(emu):
    if emu.location()==PRESENT:destination(emu,2)
    if emu.location()==SOUTH:clerk(emu)
    rose(emu)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--legacy',action='store_true');args=p.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'luggage-complete',args.legacy)
        clerk(emu);assert emu.var(STORY)==0
        load_checkpoint(emu,'south-account-returned',args.legacy)
        for choice in ('NO','B'):clerk(emu,choice);assert emu.var(STORY)==0
        emu.state(ROOT/'test-output/london-past-ready.state');inspect(emu,56,524287,'london-ready')
        clerk(emu);assert emu.var(STORY)==1
        emu.state(ROOT/'test-output/london-past-arrival.state');inspect(emu,57,524287,'london-arrival')
        emu.screenshot(ROOT/'test-output/london-past-arrival.png')
        open_key_item(emu,361);wait_task(emu,'Task_EuropeMap')
        assert emu.read('sEuropeMapPast',1) and emu.read('sEuropeMapCurrent',1)==0
        emu.screenshot(ROOT/'test-output/london-past-map.png')
        emu.press('B',180);emu.press('B',180);emu.press('B',90)
        for choice in ('NO','B'):leave(emu,choice);assert emu.var(STORY)==1
        cancel_checks(emu);cross(emu);emu.state(ROOT/'test-output/london-past-returned.state')
        finish_london(emu);rose(emu)
        emu.state(ROOT/'test-output/london-past-complete.state')
        inspect(emu,58,1048575,'london-complete');inspect_pages(emu,1048575,'london-complete')
        leave(emu);rest(emu);clerk(emu);assert emu.var(STORY)==2
        print('PASS: account gate, boarding/return No/B, arrival, Rose welcome and repeated visits',flush=True)
        print('PASS: both exits, unfinished re-entry, care, London map context and twentieth milestone',flush=True)
        load_checkpoint(emu,'evac-booking',args.legacy)
        if emu.location()!=PRESENT:cross(emu)
        booking=emu.var(0x40F7);assert booking
        save=emu.read('gSaveBlock1Ptr')
        for var,value in ((0x40D6,1),(0x40D7,3),(0x40D8,2),(0x40D9,1),(0x40DA,3),(0x40DB,2)):
            emu.write(save+0x1000+(var-0x4000)*2,value,2)
        destination(emu,2);clerk(emu);rose(emu);cross(emu)
        assert emu.var(0x40F7)==booking;resume_booking(emu)
        print('PASS: genuine modern rail booking survives historical London trip and resumes',flush=True)
    finally:emu.close()
