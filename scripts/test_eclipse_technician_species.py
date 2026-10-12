"""Native ability creation, evolution, summary display and cold-save QA."""
import json
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

def use(e):
    start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');p=e.symbols['gBagMenuState']
    for _ in range(5):
        if e.read(p+6,2)==0:break
        e.press('LEFT',90)
    for _ in range(45):
        if e.read(p+8,2)+e.read(p+14,2)==0:break
        e.press('UP',30)
    e.press('A',90);e.press('A',180);wait_task(e,'Task_HandleChooseMonInput');e.press('A',180)
    for _ in range(60):e.press('A',90)
    field(e)

# Encounter species is explicit; generation, regular ability choice and battle loading are native.
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--slots-only',action='store_true');args=parser.parse_args()
rows={r['token'][8:]:r for r in json.loads((ROOT/'data/eclipse-roster.json').read_text())['species']}
abilities={'ABILITY_TECHNICIAN':78,'ABILITY_PICKUP':53,'ABILITY_CUTE_CHARM':56,'ABILITY_NONE':0}
for species in (() if args.slots_only else ('AMBIPOM','MINCCINO','CINCCINO','MARSHADOW')):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0);ensure_visible(e);go(e,(40,25))
        var(e,0x40a0,ids['SPECIES_'+species]);battle_start(e,(40,25))
        slot=(monfield(e,0,3,4,'gEnemyParty')>>31)&1
        expected=abilities[rows[species]['abilities'][slot]]
        assert e.read(e.symbols['gBattleMons']+88+32,1)==expected,(species,slot,expected)
        print('PASS: native generated regular ability',species,'slot',slot,'ability',expected,flush=True)
    finally:e.close()
# Six classic source species gain their later-generation second regular slot.
slots=[(s,1) for s in ('MEOWTH','PERSIAN','SCYTHER','SCIZOR','SMEARGLE','HITMONTOP')]+[('AMBIPOM',0),('MINCCINO',1),('CINCCINO',1),('MARSHADOW',0)]
for species,slot in (slots[6:] if args.slots_only else slots):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
        fixture(e,species,255,0,0);ability_slot(e,slot)
        ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
        assert e.read(e.symbols['gBattleMons']+32,1)==78,species
        print('PASS: native regular Technician slot',species,flush=True)
    finally:e.close()
if not args.slots_only:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True)
        fixture(e,'SCYTHER',255,199,0);ability_slot(e,1)
        sb=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
        e.write(sb+0x310,59,2);e.write(sb+0x312,1^key,2);use(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_SCIZOR']
        assert monfield(e,0,0,0)>>16==0 and (monfield(e,0,3,4)>>31)&1
        start_action(e,1);wait_task(e,'Task_HandleChooseMonInput');e.press('A',60)
        wait_task(e,'Task_HandleSelectionMenuInput');e.press('A',240);e.press('RIGHT',120)
        assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_RunPokemonSummaryScreen']&~1
        e.screenshot(ROOT/'test-output/technician-scizor-summary.png');field(e)
        start_action(e,4)
        for _ in range(8):e.press('A',240)
        e.battery(ROOT/'test-output/technician-scizor.sav')
        print('PASS: native Scyther/Scizor evolution preserves ability slot and summary UI',flush=True)
    finally:e.close()
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'technician-scizor',True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_SCIZOR'] and (monfield(e,0,3,4)>>31)&1
        world(e,0);ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
        assert e.read(e.symbols['gBattleMons']+32,1)==78
        print('PASS: native cold Continue and next battle preserve Scizor Technician',flush=True)
    finally:e.close()
