"""Native Sharpness slots and Gallade cold-save summary QA."""
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


from test_eclipse_move_evolution import moves_fixture,moves
from test_eclipse_reminder import lesson,bag,money
from test_eclipse_gender_evolution import gender_fixture
from test_oxford_gym import count_pocket

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0);fixture(e,'GALLADE',255,0,0);ability_slot(e,1);moves_fixture(e,'MOVE_TACKLE')
    before=bag(e);cash=money(e)
    for move in ('MOVE_SLASH','MOVE_LEAF_BLADE','MOVE_FURY_CUTTER'):lesson(e,move)
    assert bag(e)==before and money(e)==cash
    start_action(e,4)
    for _ in range(8):e.press('A',240)
    e.battery(ROOT/'test-output/sharpness-gallade-recall.sav')
    print('PASS: free Gallade slicing recall preserves bag/money',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'sharpness-gallade-recall',True)
    learned=[monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
    assert all(moves[m] in learned for m in ('MOVE_SLASH','MOVE_LEAF_BLADE','MOVE_FURY_CUTTER'))
    world(e,0);ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
    assert e.read(e.symbols['gBattleMons']+32,1)==103
    print('PASS: recalled slicing moves and Sharpness persist through cold Continue',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'KIRLIA',255,0,0);gender_fixture(e,False);ability_slot(e,1);moves_fixture(e,'MOVE_TACKLE')
    p=e.read('gSaveBlock1Ptr')+0x310;k=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
    e.write(p,54,2);e.write(p+2,2^k,2);use(e)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_GALLADE'] and ((monfield(e,0,3,4)>>31)&1)
    assert count_pocket(e,54,0x310,42)==1
    world(e,0);ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
    assert e.read(e.symbols['gBattleMons']+32,1)==103
    print('PASS: male Kirlia Dawn Stone evolution retains slot and gains Sharpness',flush=True)
finally:e.close()
