"""Rouen riverside walking, water collision, old-map save compatibility."""
import argparse
import sys
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_rouen import ROUEN, leon
from test_gym_ui import start_action

def return_from_bank(emu):
    assert emu.location()==(43,34,33,10)
    emu.walk('LEFT',21);emu.walk('DOWN',6);emu.walk('LEFT',2)
    assert emu.location()==ROUEN

def walk_riverside(emu):
    assert emu.location()==ROUEN
    emu.walk('RIGHT',15);assert emu.location()==(43,34,25,16)
    emu.walk('RIGHT',2);assert emu.location()==(43,34,25,16)
    emu.screenshot(ROOT/'test-output/rouen-riverside-south.png')
    emu.walk('UP',6);emu.walk('RIGHT',8)
    assert emu.location()==(43,34,33,10)
    emu.walk('RIGHT',2);assert emu.location()==(43,34,33,10)
    emu.walk('UP',4);emu.walk('LEFT',1)
    assert emu.location()==(43,34,32,6)
    emu.walk('LEFT',2);assert emu.location()==(43,34,32,6)
    emu.screenshot(ROOT/'test-output/rouen-riverside-north.png')
    emu.walk('RIGHT',1);emu.walk('DOWN',4)
    emu.screenshot(ROOT/'test-output/rouen-riverside-crossing.png')
    emu.state(ROOT/'test-output/riverside-bank.state')
    return_from_bank(emu);leon(emu)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'rouen-complete',args.legacy)
        walk_riverside(emu)
        print('PASS: both banks, paved crossing, water and forest collision, return to Leon',flush=True)
    finally:emu.close()
    if not args.legacy:sys.exit(0)
    old=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v0.34.gba')
    try:
        load_checkpoint(old,'rouen-complete',True)
        old.walk('RIGHT',11);assert old.location()==(43,34,21,16)
        start_action(old,4)
        for _ in range(5):old.press('A',150)
        old.battery(ROOT/'test-output/riverside-old-edge.sav')
    finally:old.close()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'riverside-old-edge',True)
        assert emu.location()==(43,34,21,16)
        emu.walk('RIGHT',4);assert emu.location()==(43,34,25,16)
        emu.walk('LEFT',15);assert emu.location()==ROUEN
        print('PASS: genuine v0.34 save at old eastern edge loads on safe ground and reaches expanded bank',flush=True)
    finally:emu.close()
