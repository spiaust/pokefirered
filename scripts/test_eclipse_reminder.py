"""Native free reminder, move-dependent evolution, cancellation and cold-save QA.
Species, cached level, moves and Rare Candy are isolated fixtures; all learning uses NPC inputs.
"""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world
from test_shadow_runtime import go, monfield
from test_eclipse_friendship import fixture, candy, ids
from test_eclipse_move_evolution import moves_fixture, moves
from test_navigation import wait_task
from test_country import wait_menu
from tm_teaching_test_helpers import field
from test_gym_ui import start_action

def advance(e,predicate):
    for _ in range(60):
        if predicate():return
        e.press('A',60)
    e.screenshot(ROOT/'test-output/reminder-failure.png')
    raise AssertionError('Reminder UI did not reach expected state')

def offer(e):
    go(e,(10,31));e.press('UP');e.press('A',180)
    wait_menu(e,'Task_YesNoMenu_HandleInput')

def lesson(e,move):
    offer(e);e.press('A',180)
    advance(e,lambda:e.task_active('Task_HandleChooseMonInput'))
    e.press('A',180)
    advance(e,lambda:e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_MoveRelearner']&~1)
    e.frames(300);p=e.read('sMoveRelearner');assert e.read(p,1)==4
    count=e.read(p+0x1a,1);values=[e.read(p+0xe8+2*i,2) for i in range(count-1)]
    assert moves[move] in values,(move,values)
    for _ in range(values.index(moves[move])):e.press('DOWN',30)
    e.screenshot(ROOT/f'test-output/reminder-menu-{move.lower()}.png')
    e.press('A',180);assert e.read(p,1)==9;e.press('A',180)
    advance(e,lambda:e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_Overworld']&~1)
    e.finish_dialogue();field(e)
    assert moves[move] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]

def bag(e):
    p=e.read('gSaveBlock1Ptr')+0x310
    key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
    return [(e.read(p+4*i,2),e.read(p+4*i+2,2)^key) for i in range(42) if e.read(p+4*i,2)]

def money(e):
    return e.read(e.read('gSaveBlock1Ptr')+0x290)^e.read(e.read('gSaveBlock2Ptr')+0xf20)

import argparse
parser=argparse.ArgumentParser();parser.add_argument('--only-long',action='store_true');args=parser.parse_args()
for species,required,target in ([] if args.only_long else [('PILOSWINE','MOVE_ANCIENT_POWER','MAMOSWINE'),('BONSLY','MOVE_MIMIC','SUDOWOODO')]):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
        fixture(e,species,255,0,0);moves_fixture(e,'MOVE_TACKLE')
        before=bag(e);cash=money(e)
        lesson(e,required)
        assert bag(e)==before and money(e)==cash
        e.screenshot(ROOT/f'test-output/reminder-{species.lower()}.png')
        candy(e);assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
        print('PASS: free native reminder then level-up evolves',species,'into',target,flush=True)
        if species=='PILOSWINE':
            field(e);start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/'test-output/reminder-mamoswine.sav')
        old=[monfield(e,0,1,j)&65535 for j in (0,2,4,6)];before=bag(e)
        field(e);offer(e);e.press('B',180);field(e)
        assert old==[monfield(e,0,1,j)&65535 for j in (0,2,4,6)] and bag(e)==before
        offer(e);e.press('A',180);advance(e,lambda:e.task_active('Task_HandleChooseMonInput'));e.press('B',180);field(e)
        assert old==[monfield(e,0,1,j)&65535 for j in (0,2,4,6)] and bag(e)==before
        print('PASS: offer and party cancellation preserve moves and inventory',flush=True)
    finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
    fixture(e,'MR_RIME',255,0,0)
    old=[monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
    assert all(old)
    e.write(e.symbols['gPlayerParty']+0x54,100,1)
    before=bag(e);cash=money(e);lesson(e,'MOVE_TEETER_DANCE')
    assert bag(e)==before and money(e)==cash
    old[0]=moves['MOVE_TEETER_DANCE']
    assert [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]==old
    print('PASS: imported roster maximum-length learnset pages to its final move and replaces slot one',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'reminder-mamoswine',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_MAMOSWINE']
    assert moves['MOVE_ANCIENT_POWER'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
    extra=ids['SPECIES_MAMOSWINE']-440;mask=1<<(extra%8);sb=e.read('gSaveBlock2Ptr')
    assert e.read(sb+0xb20+extra//8,1)&mask
    assert e.read(sb+0xb70+extra//8,1)&mask
    print('PASS: reminder-learned Ancient Power and Mamoswine survive Save/cold Continue')
finally:e.close()
