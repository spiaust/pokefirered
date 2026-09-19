"""Rental Lapras: unchanged party, free steering, shore exit and rail booking."""
from emulator import Emulator,ROOT
from test_country import wait_menu
from test_trainers import money
from test_gym_ui import open_key_item
from test_ferry import resume_rail_from_landing
from rail_test_helpers import BOOKING

SURF=8

def party(emu):
    n=emu.read('gPlayerPartyCount',1)
    return n,bytes(emu.read(emu.symbols['gPlayerParty']+i,1) for i in range(n*100))

def attendant(emu):
    assert emu.location()[2:]==(26,16),emu.location()
    emu.press('DOWN');emu.press('A',180)

def ride(emu):
    before=party(emu),money(emu),emu.var(BOOKING),emu.var(0x40F0)
    town=emu.location()[1]
    attendant(emu);wait_menu(emu,'Task_YesNoMenu_HandleInput');emu.frames(60)
    emu.press('A',180);emu.finish_dialogue();emu.frames(120)
    assert emu.location()==(43,town,26,19),emu.location()
    assert emu.read('gPlayerAvatar',1)&SURF,hex(emu.read('gPlayerAvatar',1))
    assert (party(emu),money(emu),emu.var(BOOKING),emu.var(0x40F0))==before
    assert not emu.read('sLockFieldControls',1)

def steps(emu,direction,count):
    # Surf movement is faster than the walking helper; release after each tile.
    for _ in range(count):
        old=emu.location()
        for _ in range(120):
            emu.frames(1,direction)
            if emu.location()!=old:break
        assert emu.location()!=old,(direction,old)
        emu.frames(32)

def dismount(emu):
    assert emu.location()[2:]==(26,19),emu.location()
    steps(emu,'LEFT',1);steps(emu,'UP',2);emu.frames(120)
    assert emu.location()[2:]==(25,17),emu.location()
    assert not emu.read('gPlayerAvatar',1)&SURF
    assert not emu.read('sLockFieldControls',1)

if __name__=='__main__':
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        for town in ('london','oxford'):
            emu.state(ROOT/f'test-output/ferry-{town}.state',True)
            emu.walk('RIGHT',2)
            ready=ROOT/f'test-output/ride-{town}-ready.state';emu.state(ready)
            addr=emu.read('gSaveBlock1Ptr')+0xEE0+0x822//8
            emu.write(addr,emu.read(addr,1)&~(1<<(0x822%8)),1)
            attendant(emu);emu.finish_dialogue()
            assert emu.location()[2:]==(26,16) and not emu.read('gPlayerAvatar',1)&SURF
            assert not emu.task_active('Task_YesNoMenu_HandleInput')
            emu.state(ready,True);attendant(emu);wait_menu(emu,'Task_YesNoMenu_HandleInput');emu.frames(60)
            prompt=ROOT/f'test-output/ride-{town}-prompt.state';emu.state(prompt)
            for decline in ('B','NO'):
                emu.state(prompt,True)
                if decline=='NO':emu.press('DOWN');emu.press('A',180)
                else:emu.press('B',180)
                emu.finish_dialogue();assert emu.location()[2:]==(26,16)
            emu.state(ready,True);ride(emu)
            emu.state(ROOT/f'test-output/ride-{town}.state')
            emu.screenshot(ROOT/f'test-output/ride-{town}.png')
            # Free steering on water, then approach a clear shoreline.
            steps(emu,'LEFT',2);assert emu.location()[2:]==(24,19),emu.location()
            steps(emu,'RIGHT',2);assert emu.location()[2:]==(26,19)
            assert emu.read('gPlayerAvatar',1)&SURF
            dismount(emu);emu.state(ROOT/'test-output/ride-bank.state')
            emu.walk('UP',1);emu.walk('RIGHT',1);ride(emu);dismount(emu)
            print(f'PASS: {town}: badge gate, No/B, free rental, identical party, steering, shore dismount and repeat ride',flush=True)
        emu.state(ROOT/'test-output/ride-oxford-ready.state',True)
        open_key_item(emu,360);emu.frames(120)
        assert emu.read('gPlayerAvatar',1)&2
        ride(emu);assert not emu.read('gPlayerAvatar',1)&2
        dismount(emu)
        print('PASS: Bicycle rider mounts rental and returns to walking on shore',flush=True)
        emu.state(ROOT/'test-output/ferry-booking.state',True);emu.walk('RIGHT',2)
        assert emu.var(BOOKING)==3
        ride(emu);emu.state(ROOT/'test-output/ride-booking.state')
        dismount(emu);emu.walk('UP',1);emu.walk('LEFT',1)
        resume_rail_from_landing(emu)
        assert emu.location()[:2]==(43,10) and emu.var(BOOKING)==0
        print('PASS: rented ride preserves real rail booking; shore exit and rail clerk complete Berlin trip',flush=True)
    finally:emu.close()
