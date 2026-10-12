"""Native Europe standard-form adaptations with explicit species/level/item fixtures."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture,candy,ids
from test_eclipse_move_evolution import moves_fixture,moves
from test_shadow_runtime import monfield
from test_continent_runtime import world,menu_row
from test_gym_ui import start_action,open_key_item
from test_navigation import wait_task
from tm_teaching_test_helpers import field
from test_oxford_gym import count_pocket

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


cases=[('DEWOTT','SAMUROTT',35,0,0),('DARTRIX','DECIDUEYE',33,0,0),
 ('GOOMY','SLIGGOO',39,0,0),('BERGMITE','AVALUGG',36,0,0),('RUFFLET','BRAVIARY',53,0,0),
 ('DEWOTT','DEWOTT',34,0,0),('DARTRIX','DARTRIX',32,0,0),('GOOMY','GOOMY',38,0,0),
 ('MIME_JR','MR_MIME',31,0,0),('MIME_JR','MIME_JR',49,0,0),
 ('DEWOTT','DEWOTT',35,195,0),('DARTRIX','DARTRIX',33,0,1)]
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--chain-only',action='store_true');args=parser.parse_args()
saved=[('europe-route-samurott','SAMUROTT'),('europe-route-decidueye','DECIDUEYE'),('europe-route-mr_mime','MR_MIME')] if args.chain_only else []
for n,(species,target,level,held,shadow) in enumerate([] if args.chain_only else cases):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True)
        fixture(e,species,255,held,shadow);moves_fixture(e,'MOVE_TACKLE')
        e.write(e.symbols['gPlayerParty']+0x54,level,1);candy(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,species,target)
        assert e.read(e.symbols['gPlayerParty']+0x54,1)==level+1
        if n==8:assert moves['MOVE_MIMIC'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
        print('PASS:',n,species,'->',target,'level',level+1,flush=True)
        if n in (0,1,8):
            field(e);start_action(e,4)
            for _ in range(8):e.press('A',240)
            checkpoint='europe-route-'+target.lower();e.battery(ROOT/f'test-output/{checkpoint}.sav');saved.append((checkpoint,target))
    finally:e.close()
for item,target in ([] if args.chain_only else [(93,'LILLIGANT'),(94,'PETILIL')]):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'PETILIL',255,0,0)
        sb=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
        e.write(sb+0x310,item,2);e.write(sb+0x312,2^key,2);use(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
        assert count_pocket(e,item,0x310,42)==(1 if target=='LILLIGANT' else 2)
        print('PASS: PETILIL item',item,'->',target,'exact consumption',flush=True)
    finally:e.close()
# Both Goomy stages evolve natively; levels and Rare Candy stock are explicit fixtures.
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
    open_key_item(e,363);wait_task(e,'Task_EuropeMap');menu_row(e,11)
    for _ in range(4):
        if e.var(0x40d0)==2:break
        e.press('RIGHT',60)
    field(e);e.frames(600);assert e.read(e.read('gSaveBlock1Ptr')+0x2e,1)==3
    fixture(e,'GOOMY',255,0,0);moves_fixture(e,'MOVE_TACKLE')
    e.write(e.symbols['gPlayerParty']+0x54,39,1);candy(e)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_SLIGGOO']
    field(e);e.write(e.symbols['gPlayerParty']+0x54,49,1)
    key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2);e.write(e.read('gSaveBlock1Ptr')+0x310,68,2);e.write(e.read('gSaveBlock1Ptr')+0x312,1^key,2)
    candy(e);assert monfield(e,0,0,0)&65535==ids['SPECIES_GOODRA']
    field(e);start_action(e,4)
    for _ in range(8):e.press('A',240)
    e.battery(ROOT/'test-output/europe-route-goodra.sav');saved.append(('europe-route-goodra','GOODRA'))
    print('PASS: native GOOMY -> SLIGGOO -> GOODRA chain with real World Gear rain',flush=True)
finally:e.close()
for checkpoint,target in saved:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,checkpoint,True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
        print('PASS: native cold Continue preserves',target,flush=True)
    finally:e.close()
