"""Native Iron Fist slot loading, free Drain Punch reminder, evolution and cold-save QA."""
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

from test_eclipse_move_evolution import moves_fixture,moves
from test_eclipse_reminder import lesson,bag,money
from test_eclipse_friendship import candy
SLOTS=[('HITMONCHAN',1),('GOLETT',0),('GOLURK',0),('PANCHAM',0),('PANGORO',0),('CRABRAWLER',1),('CRABOMINABLE',1),('MELMETAL',0)]
for species,slot in SLOTS:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
        fixture(e,species,255,0,0);ability_slot(e,slot)
        ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
        assert e.read(e.symbols['gBattleMons']+32,1)==80,species
        print('PASS: native regular Iron Fist slot',species,slot,flush=True)
    finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
    fixture(e,'HITMONCHAN',255,0,0);ability_slot(e,1);moves_fixture(e,'MOVE_TACKLE')
    before=bag(e);cash=money(e);lesson(e,'MOVE_DRAIN_PUNCH')
    assert bag(e)==before and money(e)==cash
    start_action(e,4)
    for _ in range(8):e.press('A',240)
    e.battery(ROOT/'test-output/iron-fist-hitmonchan.sav')
    print('PASS: native free Hitmonchan Drain Punch recall and Save',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'iron-fist-hitmonchan',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_HITMONCHAN'] and (monfield(e,0,3,4)>>31)&1
    assert moves['MOVE_DRAIN_PUNCH'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
    start_action(e,1);wait_task(e,'Task_HandleChooseMonInput');e.press('A',60)
    wait_task(e,'Task_HandleSelectionMenuInput');e.press('A',240);e.press('RIGHT',120)
    assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_RunPokemonSummaryScreen']&~1
    e.screenshot(ROOT/'test-output/iron-fist-hitmonchan-summary.png');e.press('RIGHT',120)
    e.screenshot(ROOT/'test-output/iron-fist-hitmonchan-moves.png');field(e)
    world(e,0);ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
    assert e.read(e.symbols['gBattleMons']+32,1)==80 and moves['MOVE_DRAIN_PUNCH'] in [e.read(e.symbols['gBattleMons']+12+2*j,2) for j in range(4)]
    print('PASS: cold Continue, skills/moves UI and next battle preserve Hitmonchan Iron Fist and Drain Punch',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'GOLETT',255,0,0);ability_slot(e,0);moves_fixture(e,'MOVE_TACKLE')
    e.write(e.symbols['gPlayerParty']+0x54,42,1);candy(e);field(e)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_GOLURK'] and not (monfield(e,0,3,4)>>31)&1
    world(e,0);ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
    assert e.read(e.symbols['gBattleMons']+32,1)==80
    print('PASS: native Golett/Golurk evolution preserves Iron Fist',flush=True)
finally:e.close()
