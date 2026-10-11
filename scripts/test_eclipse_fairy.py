"""Native Dragon immunity against imported Fairy species, with explicit combat fixtures."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world,var,battle_start
from test_shadow_runtime import ensure_visible,go
from test_eclipse_natural import first_symbol

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-league-20-complete',True)
    world(e,0);ensure_visible(e);go(e,(40,25));var(e,0x40a0,753)
    battle_start(e,(40,25));b=e.symbols['gBattleMons']
    assert e.read(b+88+33,1)==18 and e.read(b+88+34,1)==18
    action=first_symbol('HandleInputChooseAction')
    for _ in range(100):
        if e.read('gBattlerControllerFuncs')&~1==action:break
        e.press('A',30)
    assert e.read('gBattlerControllerFuncs')&~1==action
    hp=e.read(b+88+40,2)
    e.write(b+12,82,2);e.write(b+36,40,1)
    for slot in range(4):e.write(b+88+12+slot*2,150,2);e.write(b+88+36+slot,40,1)
    e.press('UP',2);e.press('LEFT',2);e.press('A',90)
    e.press('UP',2);e.press('LEFT',2);e.press('A',90)
    for _ in range(100):
        if e.read('gBattlerControllerFuncs')&~1==action:break
        e.press('A',30)
    assert e.read(b+88+40,2)==hp,(hp,e.read(b+88+40,2))
    e.screenshot(ROOT/'test-output/roster-fairy-immunity.png')
    print('PASS: native Fairy typing and Dragon Rage immunity')
finally:e.close()
