"""Native coach doubles turn order and partner weather suppression."""
from emulator import Emulator,ROOT
from dragon_cheer_test_helpers import setup,turn
from test_eclipse_move_evolution import moves
e=Emulator(ROOT/'pokefirered.gba')
try:
    b=setup(e);base=ROOT/'test-output/slush-rush-doubles.state';e.state(base)
    for suppressor,expected in [(0,0),(13,1),(77,1)]:
        e.state(base,True);e.write('gBattleWeather',128,2);e.write(e.symbols['gWishFutureKnock']+40,5,1)
        for battler,speed in enumerate((60,100,80,70)):
            q=b+88*battler;e.write(q+6,speed,2);e.write(q+46,0,2);e.write(q+76,0);e.write(q+80,0)
            e.write(q+32,91 if battler==0 else suppressor if battler==2 else 0,1)
            e.write(q+33,15,1);e.write(q+34,15,1)
            for stat in range(8):e.write(q+24+stat,6,1)
            for slot in range(4):e.write(q+12+2*slot,moves['MOVE_SPLASH'],2);e.write(q+36+slot,40,1)
        turn(e);assert e.read('gBattlerByTurnOrder',1)==expected,(suppressor,e.read('gBattlerByTurnOrder',1))
        print('PASS: native doubles Slush Rush/partner suppression',suppressor,expected,flush=True)
finally:e.close()
