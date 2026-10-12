"""Native four-battler Fake Out only activates the flinched defender."""
from emulator import Emulator,ROOT
from dragon_cheer_test_helpers import setup,turn
from test_eclipse_move_evolution import moves
e=Emulator(ROOT/'pokefirered.gba')
try:
    b=setup(e)
    for battler in range(4):
        q=b+88*battler;e.write(q+32,96 if battler else 0,1);e.write(q+46,0,2);e.write(q+76,0);e.write(q+80,0)
        e.write(q+6,100 if battler==0 else 40,2)
        for stat in range(8):e.write(q+24+stat,6,1)
        for slot in range(4):e.write(q+12+2*slot,moves['MOVE_SPLASH'],2);e.write(q+36+slot,40,1)
    e.write(b+12,moves['MOVE_FAKE_OUT'],2);e.write(b+36,10,1)
    turn(e)
    hit=[j for j in (1,3) if e.read(b+88*j+40,2)<1000]
    assert len(hit)==1,hit
    for battler in (1,2,3):
        q=b+88*battler
        assert e.read(q+27,1)==(7 if battler in hit else 6)
        assert sum(e.read(q+36+j,1) for j in range(4))==(160 if battler in hit else 159)
    print('PASS: native doubles flinched defender only raises Speed and loses action',hit,flush=True)
finally:e.close()
