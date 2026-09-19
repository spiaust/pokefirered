"""Le Havre travel, welcome, return choices, journal and modern booking."""
import argparse
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_rouen import ROUEN,board as board_rouen
from test_amiens import AMIENS,reach_post,board as board_amiens
from test_time import preserved,cross,cancel_checks,resume_booking
from test_garden import choose
from test_journal import inspect
from test_gym_ui import open_key_item
from test_navigation import wait_task
PORT=(43,35,8,5)
STORY=0x40DB

def clerk(emu,choice='YES'):
    assert emu.location()==ROUEN
    emu.walk('RIGHT',8);emu.walk('UP',1)
    before=preserved(emu);emu.press('UP');emu.press('A',180)
    if emu.var(0x40DC)==3:choose(emu,choice)
    else:emu.finish_dialogue()
    assert preserved(emu)==before
    if emu.location()[:2]==(43,34):emu.walk('DOWN',1);emu.walk('LEFT',8)
    return emu.location()

def captain(emu,choice='B'):
    assert emu.location()==PORT
    before=preserved(emu);emu.press('DOWN');emu.press('A',180);choose(emu,choice)
    assert preserved(emu)==before and emu.var(STORY)==2
    assert emu.location()==(ROUEN if choice=='YES' else PORT)

def finish_port(emu):
    if emu.location()!=PORT:
        if emu.location()!=ROUEN:
            if emu.location()!=AMIENS:reach_post(emu);board_amiens(emu)
            board_rouen(emu)
        clerk(emu)
    captain(emu)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'route-book-active',args.legacy)
        assert clerk(emu)==ROUEN and emu.var(STORY)==0
        load_checkpoint(emu,'route-book-complete',args.legacy)
        for choice in ('NO','B'):assert clerk(emu,choice)==ROUEN and emu.var(STORY)==0
        emu.state(ROOT/'test-output/le-havre-ready.state');inspect(emu,44,8191,'le-havre-ready')
        assert clerk(emu)==PORT and emu.var(STORY)==1
        emu.state(ROOT/'test-output/le-havre-arrival.state')
        emu.screenshot(ROOT/'test-output/le-havre-arrival.png');inspect(emu,45,8191,'le-havre-arrival')
        open_key_item(emu,361);wait_task(emu,'Task_EuropeMap')
        assert emu.read('sEuropeMapPast',1) and emu.read('sEuropeMapCurrent',1)==4
        emu.screenshot(ROOT/'test-output/le-havre-map.png')
        emu.press('B',180);emu.press('B',180);emu.press('B',90)
        cancel_checks(emu);cross(emu);emu.state(ROOT/'test-output/le-havre-returned.state')
        finish_port(emu)
        for choice in ('NO','B'):captain(emu,choice)
        emu.state(ROOT/'test-output/le-havre-complete.state');inspect(emu,46,16383,'le-havre-complete')
        captain(emu,'YES');clerk(emu);captain(emu)
        emu.walk('UP',3);assert emu.location()==(43,35,8,3)
        emu.walk('DOWN',2);assert emu.location()==PORT
        print('PASS: route-book gate, boarding/return No/B, welcome, blocked north exit and repeat visits',flush=True)
        print('PASS: Celebi choices, unfinished re-entry, journal and Le Havre map context',flush=True)
        load_checkpoint(emu,'evac-booking',args.legacy)
        booking=emu.var(0x40F7);assert booking
        save=emu.read('gSaveBlock1Ptr')
        for var,value in ((0x40E3,3),(0x40E2,3),(0x40E1,4),(0x40E0,6),(0x40DF,1),(0x40DE,4),(0x40DD,2),(0x40DC,3)):
            emu.write(save+0x1000+(var-0x4000)*2,value,2)
        finish_port(emu);cross(emu);assert emu.var(0x40F7)==booking
        resume_booking(emu)
        print('PASS: actual modern rail booking survives Le Havre travel and resumes afterward',flush=True)
    finally:emu.close()
