"""Southampton crossing, arrival, returns and seventeenth journal record."""
import argparse
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_le_havre import PORT
from test_port_return import destination
from test_dock_care import rest
from test_time import PRESENT,cross,cancel_checks,preserved,resume_booking
from test_garden import choose
from test_journal import inspect
from test_journal_pages import inspect_pages
from test_gym_ui import open_key_item
from test_navigation import wait_task

STORY=0x40D8
SOUTH=(43,36,8,5)

def clerk(emu,choice='YES'):
    assert emu.location()==PORT
    emu.walk('UP',2);emu.walk('LEFT',2)
    before=preserved(emu);emu.press('LEFT');emu.press('A',180)
    if emu.var(0x40DA)==3:choose(emu,choice)
    else:emu.finish_dialogue()
    assert preserved(emu)==before
    if emu.location()!=SOUTH:
        emu.walk('RIGHT',2);emu.walk('DOWN',2);assert emu.location()==PORT
    return emu.location()

def host(emu,choice='B'):
    assert emu.location()==SOUTH
    before=preserved(emu);emu.press('DOWN');emu.press('A',180);choose(emu,choice)
    assert preserved(emu)==before
    assert emu.location()==(PORT if choice=='YES' else SOUTH)

def finish_southampton(emu):
    if emu.location()==PRESENT:destination(emu)
    if emu.location()==PORT:clerk(emu)
    host(emu);assert emu.var(STORY)==2

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--legacy',action='store_true');args=p.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'le-havre-complete',args.legacy)
        clerk(emu);assert emu.var(STORY)==0
        load_checkpoint(emu,'port-return-arrived',args.legacy)
        for choice in ('NO','B'):clerk(emu,choice);assert emu.var(STORY)==0
        emu.state(ROOT/'test-output/southampton-ready.state');inspect(emu,50,65535,'southampton-ready')
        clerk(emu);assert emu.var(STORY)==1
        emu.state(ROOT/'test-output/southampton-arrival.state');inspect(emu,51,65535,'southampton-arrival')
        emu.screenshot(ROOT/'test-output/southampton-arrival.png')
        open_key_item(emu,361);wait_task(emu,'Task_EuropeMap')
        assert emu.read('sEuropeMapPast',1) and emu.read('sEuropeMapCurrent',1)==0
        emu.screenshot(ROOT/'test-output/southampton-map.png')
        emu.press('B',180);emu.press('B',180);emu.press('B',90)
        cancel_checks(emu);cross(emu);assert emu.var(STORY)==1
        emu.state(ROOT/'test-output/southampton-returned.state')
        destination(emu);clerk(emu);host(emu,'NO');assert emu.var(STORY)==2
        emu.state(ROOT/'test-output/southampton-complete.state')
        inspect(emu,52,131071,'southampton-complete');inspect_pages(emu,131071,'southampton-complete')
        host(emu);host(emu,'YES');rest(emu);clerk(emu);assert emu.var(STORY)==2
        emu.walk('UP',3);assert emu.location()==(43,36,8,3)
        emu.walk('DOWN',2);assert emu.location()==SOUTH
        print('PASS: dock-clearance gate, crossing No/B, arrival, host welcome, repeats and closed entrance',flush=True)
        print('PASS: both returns, re-entry, care, England map context and seventeenth journal milestone',flush=True)
        load_checkpoint(emu,'evac-booking',args.legacy)
        if emu.location()!=PRESENT:cross(emu)
        booking=emu.var(0x40F7);assert booking
        save=emu.read('gSaveBlock1Ptr')
        for var,value in ((0x40D9,1),(0x40DA,3),(0x40DB,2)):
            emu.write(save+0x1000+(var-0x4000)*2,value,2)
        destination(emu);clerk(emu);host(emu);cross(emu)
        assert emu.var(0x40F7)==booking;resume_booking(emu)
        print('PASS: real modern rail booking survives Southampton journey and resumes',flush=True)
    finally:emu.close()
