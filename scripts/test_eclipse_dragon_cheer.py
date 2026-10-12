"""Dragon Cheer in real native doubles and singles with explicit move/type fixtures."""
from emulator import Emulator,ROOT
from dragon_cheer_test_helpers import setup,turn,flags,CHEER,FOCUS,wait_action
from test_eclipse_move_evolution import moves
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--case',type=int);args=parser.parse_args()
cases=[False,True,False,True]
for n,dragon in enumerate(cases):
    if args.case is not None and n!=args.case:continue
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        b=setup(e,dragon)
        if n==2:e.write(e.symbols['gStatuses3']+8,CHEER)
        if n==3:e.write(b+176+80,FOCUS)
        before=flags(e,2);turn(e)
        expected=(0,FOCUS) if dragon else (CHEER,0)
        assert flags(e,2)==expected and flags(e,0)==(0,0) and flags(e,1)==(0,0) and flags(e,3)==(0,0),(n,flags(e,2))
        assert e.read(b+36,1)==14
        if n>=2:assert before==flags(e,2)
        e.screenshot(ROOT/f'test-output/dragon-cheer-doubles-{n}.png')
        print('PASS:',n,'native doubles Dragon ally' if dragon else 'native doubles non-Dragon ally','critical boost flags',flags(e,2),'one PP',flush=True)
        if n==0:
            turn(e);assert flags(e,2)==(CHEER,0) and e.read(b+36,1)==13
            # A Focus Energy attempt by the cheered ally cannot add a second boost.
            e.write(b+12,moves['MOVE_SPLASH'],2);e.write(b+36,40,1)
            e.write(b+176+12,moves['MOVE_FOCUS_ENERGY'],2);e.write(b+176+36,30,1)
            turn(e);assert flags(e,2)==(CHEER,0) and e.read(b+176+36,1)==29
            print('PASS: repeated Cheer and Focus Energy do not stack on a cheered ally',flush=True)
    finally:e.close()
