"""Native Earthquake spread damage and partner weather suppression."""
from emulator import Emulator,ROOT
from dragon_cheer_test_helpers import setup,turn
from test_eclipse_move_evolution import moves
e=Emulator(ROOT/'pokefirered.gba')
try:
    b=setup(e);base=ROOT/'test-output/sand-force-doubles.state';e.state(base)
    for suppressor in (0,13,77):
        results=[]
        for ability in (0,93):
            e.state(base,True);e.write('gBattleWeather',8,2);e.write(e.symbols['gWishFutureKnock']+40,5,1);e.write('gRngValue',1)
            for battler in range(4):
                q=b+88*battler;e.write(q+46,0,2);e.write(q+76,0);e.write(q+80,0)
                e.write(q+32,ability if battler==0 else suppressor if battler==2 else 0,1)
                e.write(q+33,5,1);e.write(q+34,5,1);e.write(q+42,50,1)
                for stat in (2,4,6,8,10):e.write(q+stat,100,2)
                for stat in range(8):e.write(q+24+stat,6,1)
                for slot in range(4):e.write(q+12+2*slot,moves['MOVE_SPLASH'],2);e.write(q+36+slot,40,1)
            e.write(b+12,moves['MOVE_EARTHQUAKE'],2);e.write(b+36,10,1)
            turn(e);results.append([1000-e.read(b+88*j+40,2) for j in (1,2,3)])
        normal,force=results
        assert all(f>n for n,f in zip(normal,force)) if suppressor==0 else normal==force,(suppressor,results)
        print('PASS: spread damage/partner weather suppression',suppressor,normal,force,flush=True)
finally:e.close()
