"""Rouen onward travel, arrival, return routes and historical map context."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_amiens import AMIENS, board as board_amiens, reach_post, notice as amiens_notice
from test_amiens_news import porter
from test_garden import choose
from test_time import preserved, cross, cancel_checks, resume_booking
from test_journal import inspect
from test_gym_ui import open_key_item
from test_navigation import wait_task
ROUEN=(43,34,10,16)
STORY=0x40DD

def board(emu,choice='YES'):
    assert emu.location()==AMIENS
    emu.walk('RIGHT',8);emu.walk('UP',3)
    before=preserved(emu);emu.press('UP');emu.press('A',180);choose(emu,choice)
    assert preserved(emu)==before
    if choice!='YES':emu.walk('DOWN',3);emu.walk('LEFT',8)
    assert emu.location()==(ROUEN if choice=='YES' else AMIENS),emu.location()

def leave(emu,choice='YES'):
    assert emu.location()==ROUEN
    emu.walk('UP',1);before=preserved(emu)
    emu.press('UP');emu.press('A',180);choose(emu,choice)
    assert preserved(emu)==before
    if choice!='YES':emu.walk('DOWN',1)
    assert emu.location()==(AMIENS if choice=='YES' else ROUEN)

def leon(emu,choice='B'):
    emu.walk('UP',1);emu.walk('LEFT',4);emu.walk('UP',6)
    before=preserved(emu);emu.press('UP');emu.press('A',180)
    emu.frames(180);emu.screenshot(ROOT/'test-output/rouen-leon.png')
    for _ in range(40):
        if emu.task_active('Task_YesNoMenu_HandleInput'):
            choose(emu,choice)
            break
        if not emu.read('sLockFieldControls',1):break
        emu.press('A',90)
    assert not emu.read('sLockFieldControls',1)
    assert preserved(emu)==before
    emu.walk('DOWN',6);emu.walk('RIGHT',4);emu.walk('DOWN',1)
    assert emu.location()==ROUEN and emu.var(STORY)==2

def finish_rouen(emu):
    if emu.location()!=ROUEN:
        if emu.location()!=AMIENS:reach_post(emu);board_amiens(emu)
        board(emu)
    leon(emu)

def booking_check(emu, legacy):
    load_checkpoint(emu, 'evac-booking', legacy)
    booking = emu.var(0x40F7)
    assert booking != 0
    # Unlock fixture over an actual, previously booked modern rail journey.
    save = emu.read('gSaveBlock1Ptr')
    for var, value in ((0x40E3,3),(0x40E2,3),(0x40E1,4),(0x40E0,6),(0x40DF,1),(0x40DE,4)):
        emu.write(save + 0x1000 + (var - 0x4000) * 2, value, 2)
    reach_post(emu);board_amiens(emu);board(emu);leon(emu);cross(emu)
    assert emu.var(0x40F7) == booking
    resume_booking(emu)
    print('PASS: Rouen and Celebi preserve and resume an actual modern rail booking', flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'amiens-news-checked',args.legacy)
        porter(emu);assert emu.var(STORY)==0 and emu.location()==AMIENS
        load_checkpoint(emu,'amiens-news-complete',args.legacy)
        for choice in ('NO','B'):board(emu,choice);assert emu.var(STORY)==0
        amiens_notice(emu)
        emu.state(ROOT/'test-output/rouen-ready.state')
        inspect(emu,39,2047,'rouen-ready')
        board(emu);assert emu.var(STORY)==1
        emu.state(ROOT/'test-output/rouen-arrival.state')
        emu.screenshot(ROOT/'test-output/rouen-arrival.png')
        inspect(emu,40,2047,'rouen-arrival')
        open_key_item(emu,361);wait_task(emu,'Task_EuropeMap')
        assert emu.read('sEuropeMapPast',1) and emu.read('sEuropeMapCurrent',1)==4
        emu.screenshot(ROOT/'test-output/rouen-map.png')
        emu.press('B',180);emu.press('B',180);emu.press('B',90)
        for choice in ('NO','B'):leave(emu,choice)
        cancel_checks(emu)
        cross(emu);emu.state(ROOT/'test-output/rouen-returned.state')
        finish_rouen(emu);leon(emu)
        emu.state(ROOT/'test-output/rouen-complete.state')
        inspect(emu,41,4095,'rouen-complete')
        leave(emu);board(emu);assert emu.var(STORY)==2
        print('PASS: bulletin gate, boarding/return No/B, arrival and repeat welcome',flush=True)
        print('PASS: Celebi No/B and return, unfinished re-entry, journal and Rouen map context',flush=True)
        booking_check(emu,args.legacy)
    finally:emu.close()
