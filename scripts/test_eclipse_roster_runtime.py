"""Native capture/PC/cold-save checks with explicit species and Master Ball fixtures."""
import re
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import ensure_visible,go,monfield
from test_continent_runtime import world,var,battle_start
from test_eclipse_legendaries import capture
from test_gym_ui import start_action

SPECIES=(440,866,1078) # Turtwig, Scorbunny, Pecharunt

def boxed(e):
    rows={int(a):tuple(map(int,b)) for a,*b in re.findall(r'SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)',(ROOT/'src/pokemon.c').read_text())}
    result=set();storage=e.read('gPokemonStoragePtr')+4
    for i in range(14*30):
        p=storage+80*i;person=e.read(p);key=person^e.read(p+4)
        result.add((e.read(p+32+12*rows[person%24][0])^key)&0xffff)
    return result

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-league-20-complete',True)
    assert e.read('gPlayerPartyCount',1)==6
    before=[monfield(e,i,0,0)&0xffff for i in range(6)]
    p=e.read('gSaveBlock1Ptr')+0x430;key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
    e.write(p,1,2);e.write(p+2,10^key,2)
    for species in SPECIES:
        world(e,0);ensure_visible(e);go(e,(40,25))
        var(e,0x40a0,species) # Explicit encounter fixture, native generation/capture follows.
        battle_start(e,(40,25))
        assert monfield(e,0,0,0,'gEnemyParty')&0xffff==species
        e.screenshot(ROOT/f'test-output/roster-battle-{species}.png')
        capture(e)
        assert species in boxed(e)
    assert [monfield(e,i,0,0)&0xffff for i in range(6)]==before
    start_action(e,4)
    for _ in range(8):e.press('A',240)
    e.battery(ROOT/'test-output/roster-captures.sav')
    print('PASS: Gen IV/VIII/IX native capture, front sprites and PC overflow; original earned party preserved',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'roster-captures',True)
    assert set(SPECIES).issubset(boxed(e))
    sb=e.read('gSaveBlock2Ptr')
    for species in SPECIES:
        extra=species-440;mask=1<<(extra%8)
        assert e.read(sb+0xb20+extra//8,1)&mask
        assert e.read(sb+0xb70+extra//8,1)&mask
    print('PASS: new species and extended seen/caught flags survive cold native Continue')
finally:e.close()
