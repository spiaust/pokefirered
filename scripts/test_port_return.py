"""Unlocked Celebi destination choice, cancellation, preservation and rail booking."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, visit_forest
from test_time import PRESENT, ARRIVAL, cross, cancel_checks, portal_prompt, preserved, resume_booking
from test_country import wait_menu
from test_le_havre import PORT, captain, clerk
from test_dock_care import rest


def destination(emu, choice=1):
    assert emu.location() == PRESENT and emu.var(0x40D9) == 1
    before=preserved(emu)
    progress=tuple(emu.var(v) for v in range(0x40D7,0x4100))
    portal_prompt(emu);emu.press('A',180)
    wait_menu(emu,'Task_MultichoiceMenu_HandleInput');emu.frames(60)
    menu_name='south-return-menu' if emu.var(0x40D7)==3 else 'port-return-menu'
    emu.screenshot(ROOT/f'test-output/{menu_name}.png')
    if choice=='B':emu.press('B',180)
    else:
        for _ in range(choice):emu.press('DOWN')
        emu.press('A',180)
    emu.finish_dialogue();emu.frames(90)
    assert emu.location()==(PORT if choice==1 else ARRIVAL if choice==0 else (43,36,8,5) if choice==2 and emu.var(0x40D7)==3 else PRESENT)
    assert preserved(emu)==before
    assert tuple(emu.var(v) for v in range(0x40D7,0x4100))==progress
    assert not emu.read('sLockFieldControls',1)


def verify_saved_return(emu):
    if emu.location()==PORT:cross(emu)
    destination(emu)
    rest(emu)
    cross(emu)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--legacy',action='store_true');args=p.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'dock-check-complete',args.legacy)
        cross(emu);cancel_checks(emu);cross(emu)
        assert emu.location()==ARRIVAL and emu.var(0x40D9)==0
        load_checkpoint(emu,'port-account-complete',args.legacy)
        visit_forest(emu);cancel_checks(emu)
        for choice in ('B',2):destination(emu,choice)
        emu.state(ROOT/'test-output/port-return-forest.state')
        destination(emu,0);cross(emu);destination(emu)
        emu.state(ROOT/'test-output/port-return-arrived.state')
        rest(emu);captain(emu,'YES');clerk(emu);cross(emu)
        emu.state(ROOT/'test-output/port-return-back.state')
        destination(emu);cross(emu)
        print('PASS: account gate, original refuge route, No/B, destination Exit/B and direct port visits',flush=True)
        print('PASS: care, Rouen return, Celebi return, repeat visits and all quest/party/item preservation',flush=True)
        load_checkpoint(emu,'evac-booking',args.legacy)
        if emu.location()!=PRESENT:cross(emu)
        booking=emu.var(0x40F7);assert booking
        save=emu.read('gSaveBlock1Ptr')
        # Historical unlock fixture on a real, uncompleted modern rail itinerary.
        for var,value in ((0x40D9,1),(0x40DA,3),(0x40DB,2)):
            emu.write(save+0x1000+(var-0x4000)*2,value,2)
        destination(emu);cross(emu);assert emu.var(0x40F7)==booking
        resume_booking(emu)
        print('PASS: genuine modern rail booking survives direct travel and resumes afterward',flush=True)
    finally:emu.close()
