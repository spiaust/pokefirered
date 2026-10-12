"""Native Dragon Pulse damage, no paralysis, PP and Fairy immunity checks."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world,var,battle_start
from test_shadow_runtime import go,ensure_visible
from test_eclipse_natural import first_symbol
from test_eclipse_move_evolution import moves,ids
for species,immune in [('PIKACHU',False),('SYLVEON',True)]:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-league-20-complete',True);world(e,0);ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_'+species]);battle_start(e,(40,25))
        b=e.symbols['gBattleMons'];assert e.read(b+88,2)==ids['SPECIES_'+species]
        if immune:assert e.read(b+88+33,1)==18 and e.read(b+88+34,1)==18
        action=first_symbol('HandleInputChooseAction')
        for _ in range(100):
            if e.read('gBattlerControllerFuncs')&~1==action:break
            e.press('A',30)
        assert e.read('gBattlerControllerFuncs')&~1==action
        e.write(b+12,moves['MOVE_DRAGON_PULSE'],2);e.write(b+36,10,1)
        e.write(b+88+40,1000,2);e.write(b+88+44,1000,2);e.write(b+88+76,0)
        for slot in range(4):e.write(b+88+12+slot*2,moves['MOVE_SPLASH'],2);e.write(b+88+36+slot,40,1)
        e.press('UP',2);e.press('LEFT',2);e.press('A',90);e.press('UP',2);e.press('LEFT',2);e.frames(2,'A')
        hp=1000;hits=[];started=False
        for n in range(3600):
            current=e.read(b+88+40,2)
            if current<hp:hits.append(hp-current)
            hp=current
            if e.read(b+36,1)==9:started=True
            if started and e.read('gBattlerControllerFuncs')&~1==action:break
            e.frames(1,'A' if n%60==0 else 0)
        assert started and e.read(b+36,1)==9 and len(hits)==(0 if immune else 1),(species,hits)
        assert e.read(b+88+76)==0
        print('PASS: Dragon Pulse vs',species,'damage events',hits,'one PP, no paralysis, animation completes',flush=True)
    finally:e.close()
