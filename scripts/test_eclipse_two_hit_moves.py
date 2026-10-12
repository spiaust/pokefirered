"""Exactly two native damaging hits and one PP for the two added moves."""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world, var, battle_start
from test_eclipse_natural import first_symbol
from test_eclipse_move_evolution import moves
for name in ('MOVE_DOUBLE_HIT','MOVE_TWIN_BEAM'):
    passed=False
    for attempt in range(3):
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'natural-league-20-complete',True);world(e,0);var(e,0x40a0,753);e.frames(120*attempt);battle_start(e,(40,25))
            b=e.symbols['gBattleMons'];action=first_symbol('HandleInputChooseAction')
            for _ in range(100):
                if e.read('gBattlerControllerFuncs')&~1==action:break
                e.press('A',30)
            assert e.read('gBattlerControllerFuncs')&~1==action
            e.write(b+12,moves[name],2);e.write(b+36,10,1)
            e.write(b+88+40,1000,2);e.write(b+88+44,1000,2)
            for slot in range(4):e.write(b+88+12+slot*2,moves['MOVE_SPLASH'],2);e.write(b+88+36+slot,40,1)
            e.press('UP',2);e.press('LEFT',2);e.press('A',90);e.press('UP',2);e.press('LEFT',2)
            hp=1000;hits=[];counters=set();started=False;e.frames(2,'A')
            for n in range(3600):
                current=e.read(b+88+40,2)
                if current<hp:hits.append(hp-current)
                hp=current
                if e.read(b+36,1)==9:started=True;counters.add(e.read('gMultiHitCounter',1))
                if started and e.read('gBattlerControllerFuncs')&~1==action:break
                e.frames(1,'A' if n%60==0 else 0)
            assert started and e.read(b+36,1)==9
            if not hits:
                print('Observed natural accuracy miss; retry',name,attempt,flush=True);continue
            assert len(hits)==2 and 2 in counters and 1 in counters,(name,hits,counters)
            e.screenshot(ROOT/('test-output/'+name.lower()+'-two-hit.png'))
            print('PASS:',name,'exactly two damage events',hits,'and one PP; animation finishes',flush=True)
            passed=True;break
        finally:e.close()
    assert passed,name
