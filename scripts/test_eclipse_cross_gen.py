"""Native cross-generation evolution, move learning and reminder QA."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture, candy, ids
from test_eclipse_move_evolution import moves_fixture, moves
from test_shadow_runtime import monfield
from test_continent_runtime import world
from test_gym_ui import start_action
from test_navigation import wait_task
from test_oxford_gym import count_pocket
from test_eclipse_reminder import lesson, bag, money
from tm_teaching_test_helpers import field
parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['stones','moves','reminders']);args=parser.parse_args()
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
if args.mode=='stones':
    cases=[('MAGNETON','MAGNEZONE',96,0,0),('NOSEPASS','PROBOPASS',96,0,0),('CHARJABUG','VIKAVOLT',96,0,0),
     ('EEVEE','JOLTEON',96,0,0),('MAGNETON','MAGNETON',97,0,0),('NOSEPASS','NOSEPASS',96,195,0),('CHARJABUG','CHARJABUG',96,0,1),('MAGNETON','MAGNETON',96,0,1)]
    for n,(species,target,item,held,shadow) in enumerate(cases):
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'natural-circuit-complete',True);fixture(e,species,255,held,shadow)
            sb=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
            e.write(sb+0x310,item,2);e.write(sb+0x312,2^key,2);use(e)
            assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
            assert count_pocket(e,item,0x310,42)==(1 if species!=target else 2)
            print('PASS:',n,species,'->',target,'stone',item,flush=True)
        finally:e.close()
if args.mode=='moves':
    cases=[('LICKITUNG','LICKILICKY','MOVE_ROLLOUT',50,0,0,0),('AIPOM','AMBIPOM','MOVE_DOUBLE_HIT',50,0,0,0),('GIRAFARIG','FARIGIRAF','MOVE_TWIN_BEAM',50,0,0,3),
     ('GIRAFARIG','GIRAFARIG','MOVE_DOUBLE_HIT',50,0,0,0),('LICKITUNG','LICKITUNG','MOVE_TACKLE',50,0,0,0),('AIPOM','AIPOM','MOVE_DOUBLE_HIT',50,195,0,0),('GIRAFARIG','GIRAFARIG','MOVE_TWIN_BEAM',50,0,1,0),
     ('LICKITUNG','LICKILICKY','MOVE_TACKLE',5,0,0,0),('AIPOM','AMBIPOM','MOVE_TACKLE',31,0,0,0),('GIRAFARIG','FARIGIRAF','MOVE_TACKLE',31,0,0,0)]
    for n,(species,target,move,level,held,shadow,slot) in enumerate(cases):
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'natural-circuit-complete',True);fixture(e,species,255,held,shadow);moves_fixture(e,move,slot)
            e.write(e.symbols['gPlayerParty']+0x54,level,1);candy(e)
            assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,target)
            if n>=7:
                learned=['MOVE_ROLLOUT','MOVE_DOUBLE_HIT','MOVE_TWIN_BEAM'][n-7]
                assert moves[learned] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
            print('PASS:',n,species,'->',target,'level',level+1,'known',move,flush=True)
            if n==9:
                field(e);start_action(e,4)
                for _ in range(8):e.press('A',240)
                e.battery(ROOT/'test-output/cross-gen-farigiraf.sav')
        finally:e.close()
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'cross-gen-farigiraf',True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_FARIGIRAF'] and moves['MOVE_TWIN_BEAM'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
        extra=ids['SPECIES_FARIGIRAF']-440;mask=1<<(extra%8);sb=e.read('gSaveBlock2Ptr')
        assert e.read(sb+0xb20+extra//8,1)&mask and e.read(sb+0xb70+extra//8,1)&mask
        print('PASS: Farigiraf, Twin Beam and seen/caught flags survive native Save/cold Continue',flush=True)
    finally:e.close()
if args.mode=='reminders':
    for species,move,target in [('LICKITUNG','MOVE_ROLLOUT','LICKILICKY'),('AIPOM','MOVE_DOUBLE_HIT','AMBIPOM'),('GIRAFARIG','MOVE_TWIN_BEAM','FARIGIRAF')]:
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'natural-circuit-complete',True);world(e,0);fixture(e,species,255,0,0);moves_fixture(e,'MOVE_TACKLE')
            before=bag(e);cash=money(e);lesson(e,move)
            assert before==bag(e) and cash==money(e);candy(e)
            assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
            print('PASS: free native reminder',species,move,'then',target,flush=True)
        finally:e.close()
