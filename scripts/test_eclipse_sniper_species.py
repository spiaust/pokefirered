"""Native Sniper slots and Kingdra cold-save summary QA."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture,ids,orders
from test_shadow_runtime import monfield,go,ensure_visible
from test_continent_runtime import world,var,battle_start
from test_gym_ui import start_action
from test_navigation import wait_task
from tm_teaching_test_helpers import field

def ability_slot(e,slot):
    p=e.symbols['gPlayerParty'];person=e.read(p);key=person^e.read(p+4)
    raw=bytearray().join((e.read(p+32+4*i)^key).to_bytes(4,'little') for i in range(12))
    offset=12*orders[person%24][3]+4;iv=int.from_bytes(raw[offset:offset+4],'little')
    raw[offset:offset+4]=((iv&~(1<<31))|(slot<<31)).to_bytes(4,'little')
    e.write(p+28,sum(int.from_bytes(raw[i:i+2],'little') for i in range(0,48,2))&65535,2)
    for i in range(12):e.write(p+32+4*i,int.from_bytes(raw[4*i:4*i+4],'little')^key)

SLOTS=[(s,1) for s in ('HORSEA','SEADRA','KINGDRA','REMORAID','OCTILLERY','SKORUPI','DRAPION','BINACLE','BARBARACLE')]
for species,slot in SLOTS:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0);fixture(e,species,255,0,0);ability_slot(e,slot)
        ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
        assert e.read(e.symbols['gBattleMons']+32,1)==87,species
        print('PASS: native regular Sniper slot',species,slot,flush=True)
    finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'KINGDRA',255,0,0);ability_slot(e,1)
    start_action(e,4)
    for _ in range(8):e.press('A',240)
    e.battery(ROOT/'test-output/sniper-kingdra.sav')
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'sniper-kingdra',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_KINGDRA'] and (monfield(e,0,3,4)>>31)&1
    start_action(e,1);wait_task(e,'Task_HandleChooseMonInput');e.press('A',60)
    wait_task(e,'Task_HandleSelectionMenuInput');e.press('A',240);e.press('RIGHT',120)
    assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_RunPokemonSummaryScreen']&~1
    e.screenshot(ROOT/'test-output/sniper-kingdra-summary.png');field(e)
    world(e,0);ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
    assert e.read(e.symbols['gBattleMons']+32,1)==87
    print('PASS: cold Continue, skills UI and next battle preserve Kingdra Sniper',flush=True)
finally:e.close()
from test_eclipse_friendship import candy
from test_eclipse_move_evolution import moves_fixture
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'SKORUPI',255,0,0);ability_slot(e,1);moves_fixture(e,'MOVE_TACKLE')
    e.write(e.symbols['gPlayerParty']+0x54,39,1);candy(e);field(e)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_DRAPION'] and (monfield(e,0,3,4)>>31)&1
    world(e,0);ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
    assert e.read(e.symbols['gBattleMons']+32,1)==87
    print('PASS: native Skorupi/Drapion evolution preserves Sniper',flush=True)
finally:e.close()
