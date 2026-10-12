"""Native paired Link Cable use, counterpart guards and cold-save QA."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from paired_trade_test_helpers import pair
from test_eclipse_friendship import ids
from test_shadow_runtime import monfield
from test_gym_ui import start_action
from test_navigation import wait_task
from test_oxford_gym import count_pocket
from tm_teaching_test_helpers import field

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

cases=[('KARRABLAST','ESCAVALIER','SHELMET',1,False,False,0,0,0),
 ('SHELMET','ACCELGOR','KARRABLAST',1,False,False,0,0,0),
 ('KARRABLAST','KARRABLAST',None,1,False,False,0,0,0),
 ('SHELMET','SHELMET','SQUIRTLE',1,False,False,0,0,0),
 ('KARRABLAST','KARRABLAST','SHELMET',1,True,False,0,0,0),
 ('SHELMET','SHELMET','KARRABLAST',1,False,False,195,0,0),
 ('KARRABLAST','KARRABLAST','SHELMET',1,False,False,0,195,0),
 ('KARRABLAST','KARRABLAST','SHELMET',1,False,False,0,0,1),
 ('KARRABLAST','ESCAVALIER','SHELMET',1,False,True,0,0,0),
 ('SHELMET','ACCELGOR','KARRABLAST',5,False,False,199,0,0),
 ('KARRABLAST','KARRABLAST','SHELMET',1,False,False,0,0,0)]
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--cases');args=parser.parse_args()
selected=set(map(int,args.cases.split(','))) if args.cases else set(range(len(cases)))
for n,(species,target,partner,slot,egg,fainted,held,buddyheld,shadow) in enumerate(cases):
    if n not in selected:continue
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True)
        pair(e,species,partner,slot,egg,fainted,held,buddyheld,shadow)
        if n==10:
            storage=e.read('gPokemonStoragePtr')+4;p=e.symbols['gPlayerParty']+100
            for i in range(20):e.write(storage+4*i,e.read(p+4*i))
            for i in range(25):e.write(p+4*i,0)
            e.write('gPlayerPartyCount',1,1)
        sb=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
        e.write(sb+0x310,59,2);e.write(sb+0x312,2^key,2)
        before=monfield(e,slot,0,0) if partner else None
        use(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,species,target)
        assert monfield(e,0,0,0)>>16==held
        assert count_pocket(e,59,0x310,42)==(1 if species!=target else 2)
        if partner:assert monfield(e,slot,0,0)==before
        print('PASS: paired cable',n,species,'->',target,'partner unchanged',flush=True)
        if n<2:
            start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/f'test-output/paired-cable-{target.lower()}.sav')
    finally:e.close()
for target,partner in ([('ESCAVALIER','SHELMET'),('ACCELGOR','KARRABLAST')] if args.cases is None else []):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'paired-cable-'+target.lower(),True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
        assert monfield(e,1,0,0)&65535==ids['SPECIES_'+partner]
        assert count_pocket(e,59,0x310,42)==1
        print('PASS: paired cable Save/cold Continue',target,'and unchanged counterpart',flush=True)
    finally:e.close()
