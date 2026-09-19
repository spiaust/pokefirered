"""Coaches to Dover/Calais, Channel crossing, return exits and saved rail detours."""
from emulator import Emulator,ROOT
from test_country import wait_menu
from test_tour import travel
from test_trainers import money
from test_ride import party
from test_ferry import sail,city
from test_gym_ui import open_key_item
from test_navigation import wait_task
from rail_test_helpers import BOOKING,finish_saved_journey

PORTS=(27,28)

def coach(emu):
    assert emu.location()[1] in (0,4) and emu.location()[2:]==(16,14),emu.location()
    emu.walk('RIGHT',7);emu.walk('UP',5);emu.frames(180);emu.walk('UP',3)
    assert emu.location()[2:]==(4,5),emu.location()

def prompt(emu,is_port=False):
    emu.press('DOWN' if is_port else 'UP');emu.press('A',180)
    wait_menu(emu,'Task_YesNoMenu_HandleInput');emu.frames(60)

def accept(emu,destination):
    before=party(emu),money(emu),emu.var(BOOKING),emu.var(0x40F0)
    emu.press('A',180);emu.finish_dialogue();emu.frames(90)
    assert emu.location()==(43,destination,8,5),emu.location()
    assert (party(emu),money(emu),emu.var(BOOKING),emu.var(0x40F0))==before
    assert not emu.read('sLockFieldControls',1)

def crossing(emu):
    destination=28 if emu.location()[1]==27 else 27
    prompt(emu,True);accept(emu,destination)

def leave_port(emu):
    city_map=0 if emu.location()[1]==27 else 4
    emu.walk('UP',3);emu.frames(180)
    assert emu.location()==(43,city_map,23,10),emu.location()

def finish_coastal_booking(emu):
    leave_port(emu);emu.walk('UP',1);emu.frames(180);emu.walk('UP',1)
    assert emu.location()[2:]==(4,7),emu.location()
    finish_saved_journey(emu)

def decline_checks(emu,port=False):
    origin=emu.location();prompt(emu,port)
    path=ROOT/'test-output/coast-prompt.state';emu.state(path)
    before=money(emu),emu.var(BOOKING)
    for choice in ('B','NO'):
        emu.state(path,True)
        if choice=='NO':emu.press('DOWN');emu.press('A',180)
        else:emu.press('B',180)
        emu.finish_dialogue()
        assert emu.location()==origin and (money(emu),emu.var(BOOKING))==before
    emu.state(path,True)

if __name__=='__main__':
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        emu.state(ROOT/'test-output/electric-gym-complete.state',True)
        emu.walk('DOWN',10);emu.frames(180);emu.walk('DOWN',4);emu.walk('RIGHT',1);travel(emu,0)
        base=ROOT/'test-output/coast-city-ready.state';emu.state(base)
        for destination,city_id in [(27,0),(28,1)]:
            emu.state(base,True)
            if city_id:travel(emu,city_id)
            coach(emu)
            ready=ROOT/'test-output/coast-coach-ready.state';emu.state(ready)
            addr=emu.read('gSaveBlock1Ptr')+0xEE0+0x822//8
            emu.write(addr,emu.read(addr,1)&~(1<<(0x822%8)),1)
            emu.press('UP');emu.press('A',180);emu.finish_dialogue()
            assert emu.location()[2:]==(4,5) and not emu.task_active('Task_YesNoMenu_HandleInput')
            emu.state(ready,True);decline_checks(emu);accept(emu,destination)
            label='dover' if destination==27 else 'calais'
            emu.state(ROOT/f'test-output/coast-{label}.state')
            emu.screenshot(ROOT/f'test-output/coast-{label}.png')
            addr=emu.read('gSaveBlock1Ptr')+0xEE0+0x822//8
            emu.write(addr,emu.read(addr,1)&~(1<<(0x822%8)),1)
            emu.press('DOWN');emu.press('A',180);emu.finish_dialogue()
            assert emu.location()==(43,destination,8,5)
            assert not emu.task_active('Task_YesNoMenu_HandleInput')
            emu.state(ROOT/f'test-output/coast-{label}.state',True)
            open_key_item(emu,361);wait_task(emu,'Task_EuropeMap')
            assert emu.read('sEuropeMapCurrent',1)==destination-21
            assert emu.read('sEuropeMapSelection',1)==destination-21
            emu.screenshot(ROOT/f'test-output/coast-{label}-map.png')
            emu.press('A',60);emu.screenshot(ROOT/f'test-output/coast-{label}-info.png')
            emu.press('B',180);emu.press('B',180);emu.press('B',90)
            decline_checks(emu,True);accept(emu,55-destination)
            crossing(emu);leave_port(emu)
            assert emu.location()[1]==city_id*4
            emu.state(ROOT/'test-output/coast-return.state')
            print(f'PASS: {label}: coach badge gate and declines, named port map, free round-trip ferry and city return',flush=True)
        emu.state(ROOT/'test-output/ferry-booking.state',True)
        sail(emu,0);city(emu);coach(emu);prompt(emu);accept(emu,27)
        crossing(emu);assert emu.var(BOOKING)==3
        emu.state(ROOT/'test-output/coast-booking.state')
        finish_coastal_booking(emu)
        assert emu.location()[:2]==(43,10) and emu.var(BOOKING)==0
        print('PASS: coach and Channel crossing preserve real rail booking; Paris clerk finishes Berlin trip',flush=True)
    finally:emu.close()
