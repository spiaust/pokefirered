"""London/Oxford riverboat: gates, round trips, bicycle, rail detours and UI."""
from emulator import Emulator,ROOT
from test_country import wait_menu,party_species
from test_tour import travel,item_count
from test_trainers import money
from test_oranienburg_gym import badge
from test_gym_ui import open_key_item
from test_navigation import wait_task
from rail_test_helpers import BOOKING,choose_destination,board,finish_saved_journey

def landing(emu):
    assert emu.location()[2:]==(16,14),emu.location()
    emu.walk('RIGHT',8);emu.walk('DOWN',2)
    assert emu.location()[2:]==(24,16),emu.location()

def city(emu):
    emu.walk('UP',2);emu.walk('LEFT',8)
    assert emu.location()[2:]==(16,14),emu.location()

def captain(emu):
    assert emu.location()[2:]==(24,16),emu.location()
    emu.press('DOWN');emu.press('A',180)

def sail(emu,dest):
    before=money(emu),emu.var(BOOKING),emu.var(0x40F0),party_species(emu),emu.var(0x40FF),item_count(emu,208)
    captain(emu);wait_menu(emu,'Task_YesNoMenu_HandleInput');emu.frames(60)
    emu.press('A',180);emu.finish_dialogue()
    assert emu.location()==(43,dest,24,16),emu.location()
    assert not emu.read('sLockFieldControls',1)
    assert (money(emu),emu.var(BOOKING),emu.var(0x40F0),party_species(emu),emu.var(0x40FF),item_count(emu,208))==before

def resume_rail_from_landing(emu):
    city(emu);emu.walk('RIGHT',7);emu.walk('UP',5);emu.frames(180);emu.walk('UP',1)
    assert emu.location()[2:]==(4,7)
    finish_saved_journey(emu)

if __name__=='__main__':
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        emu.state(ROOT/'test-output/electric-gym-complete.state',True)
        emu.walk('DOWN',10);emu.frames(180);emu.walk('DOWN',4);emu.walk('RIGHT',1)
        travel(emu,0);landing(emu)
        ready=ROOT/'test-output/ferry-ready.state';emu.state(ready)
        for origin,dest in [(0,12),(12,0)]:
            checkpoint=ROOT/f'test-output/ferry-{origin}-ready.state';emu.state(checkpoint)
            # Both captains gate on the badge; cleared-badge fixture preserves other progress.
            addr=emu.read('gSaveBlock1Ptr')+0xEE0+0x822//8
            emu.write(addr,emu.read(addr,1)&~(1<<(0x822%8)),1)
            captain(emu);emu.finish_dialogue()
            assert emu.location()==(43,origin,24,16) and not emu.task_active('Task_YesNoMenu_HandleInput')
            emu.state(checkpoint,True)
            captain(emu);wait_menu(emu,'Task_YesNoMenu_HandleInput');emu.frames(60)
            prompt=ROOT/'test-output/ferry-prompt.state';emu.state(prompt)
            for decline in ('B','NO'):
                emu.state(prompt,True)
                if decline=='NO':emu.press('DOWN');emu.press('A',180)
                else:emu.press('B',180)
                emu.finish_dialogue();assert emu.location()==(43,origin,24,16)
            emu.state(checkpoint,True)
            # Landing sign can be read without blocking the approach.
            emu.walk('UP',1);emu.walk('LEFT',2);emu.press('DOWN');emu.press('A',180);emu.finish_dialogue()
            emu.walk('RIGHT',2);emu.walk('DOWN',1)
            sail(emu,dest)
            label='oxford' if dest==12 else 'london'
            emu.state(ROOT/f'test-output/ferry-{label}.state')
            emu.frames(60);emu.screenshot(ROOT/f'test-output/ferry-{label}.png')
            open_key_item(emu,361);wait_task(emu,'Task_EuropeMap')
            assert emu.read('sEuropeMapCurrent',1)==(3 if dest==12 else 0)
            emu.press('B',180);emu.press('B',180);emu.press('B',90)
            print(f'PASS: {origin}->{dest}: badge gate, No/B, sign, free trip, map context and retained progress',flush=True)
        # Board while mounted: normal land movement is restored after arrival.
        emu.state(ready,True);open_key_item(emu,360);emu.frames(120)
        assert emu.read('gPlayerAvatar',1)&2
        sail(emu,12);emu.state(ROOT/'test-output/ferry-bicycle.state')
        emu.frames(32,'UP');emu.frames(16);assert emu.location()[3]<16,emu.location()
        print('PASS: boarding with Bicycle returns to controllable outdoor movement',flush=True)
        # Book Oxford -> Berlin, then detour by boat after the first train to London.
        emu.state(ROOT/'test-output/ferry-oxford.state',True);city(emu)
        emu.walk('RIGHT',7);emu.walk('UP',5);emu.frames(180);emu.walk('UP',1);emu.walk('RIGHT',3)
        emu.press('UP');emu.press('A',180);choose_destination(emu,2);board(emu,0,2)
        emu.walk('DOWN',2);emu.frames(180);emu.walk('DOWN',4);emu.walk('LEFT',7);landing(emu)
        assert emu.var(BOOKING)==3
        sail(emu,12);emu.state(ROOT/'test-output/ferry-booking.state')
        resume_rail_from_landing(emu)
        assert emu.location()[:2]==(43,10) and emu.var(BOOKING)==0
        print('PASS: boat detour retains actual rail booking; next clerk recalculates and finishes Berlin journey',flush=True)
    finally:emu.close()

