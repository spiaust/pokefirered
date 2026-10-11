"""Naturally spawn an imported reserve partner and enter its matching wild battle."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world,battle_start
from test_shadow_runtime import ensure_visible,go,monfield

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-league-20-complete',True)
    for country in range(12):
        world(e,country);ensure_visible(e)
        if e.var(0x40a0)>=440:break
    else:raise AssertionError('No naturally selected new reserve partner')
    species=e.var(0x40a0)
    assert e.var(0x4010)==200,e.var(0x4010)
    go(e,(40,25));e.screenshot(ROOT/'test-output/roster-overworld.png')
    battle_start(e,(40,25));assert monfield(e,0,0,0,'gEnemyParty')&0xffff==species
    e.screenshot(ROOT/'test-output/roster-natural-reserve-battle.png')
    print('PASS: natural reserve selection, native icon-derived overworld sprite and matching wild battle',species)
finally:e.close()
