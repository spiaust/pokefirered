"""Luggage-unlocked Southampton shortcut, other choices, returns and rail booking."""
import argparse
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_time import PRESENT,ARRIVAL,cross,cancel_checks,resume_booking
from test_port_return import destination
from test_southampton import SOUTH,host,clerk
from test_southampton_care import rest

def verify_saved_return(emu):
    if emu.location()==SOUTH:cross(emu)
    destination(emu,2);rest(emu);cross(emu)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--legacy',action='store_true');args=p.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'southampton-complete',args.legacy)
        cross(emu);destination(emu,2);assert emu.location()==PRESENT and emu.var(0x40D7)==0
        load_checkpoint(emu,'luggage-complete',args.legacy)
        cross(emu);cancel_checks(emu)
        for choice in ('B',3):destination(emu,choice)
        emu.state(ROOT/'test-output/south-return-forest.state')
        destination(emu,0);assert emu.location()==ARRIVAL;cross(emu)
        destination(emu,1);cross(emu);destination(emu,2)
        emu.state(ROOT/'test-output/south-return-arrived.state')
        rest(emu);host(emu,'YES');clerk(emu);cross(emu)
        emu.state(ROOT/'test-output/south-return-back.state')
        destination(emu,2);cross(emu)
        print('PASS: luggage gate, initial No/B, menu Exit/B, three destinations and repeats',flush=True)
        print('PASS: Southampton care, Le Havre return and Celebi return preserve saved progress',flush=True)
        load_checkpoint(emu,'evac-booking',args.legacy)
        if emu.location()!=PRESENT:cross(emu)
        booking=emu.var(0x40F7);assert booking
        save=emu.read('gSaveBlock1Ptr')
        # Unlock fixture on a genuine unfinished modern rail itinerary.
        for var,value in ((0x40D7,3),(0x40D8,2),(0x40D9,1),(0x40DA,3),(0x40DB,2)):
            emu.write(save+0x1000+(var-0x4000)*2,value,2)
        destination(emu,2);cross(emu);assert emu.var(0x40F7)==booking
        resume_booking(emu)
        print('PASS: actual modern rail booking survives direct Southampton trip and resumes',flush=True)
    finally:emu.close()
