"""Native held-item evolution and cancellation QA using explicit isolated fixtures."""
from datetime import datetime, timezone
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture, candy, ids
from test_eclipse_move_evolution import moves_fixture
from test_shadow_runtime import monfield, go
from test_continent_runtime import world, var
from test_gym_ui import start_action
from test_navigation import wait_task
from test_country import wait_menu
from test_shops import confirm_purchase
from test_trainers import money
from test_oxford_gym import count_pocket
from natural_preparation_test_helpers import give
from tm_teaching_test_helpers import field
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--cases');args=parser.parse_args()

def count(e,item):return count_pocket(e,item,0x310,42)
def clock(e,hour,mode=0):
    e.rtc(int(datetime(2026,10,11,hour,tzinfo=timezone.utc).timestamp()));e.frames(120);var(e,0x40d1,mode)

if args.cases is None:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
        party=[monfield(e,i,0,0)&65535 for i in range(6)]
        go(e,(30,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
        stock=e.symbols['Shadow_ShopItems'];items=[]
        while e.read(stock+2*len(items),2):items.append(e.read(stock+2*len(items),2))
        shop=e.symbols['sShopData']
        for item in (56,57,58):
            index=items.index(item)
            for _ in range(60):
                cur=e.read(shop+12,2)+e.read(shop+14,2)
                if cur==index:break
                e.press('DOWN' if cur<index else 'UP',30)
            assert cur==index;before=(money(e),count(e,item));confirm_purchase(e,1);e.press('A',180)
            wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
            assert money(e)==before[0]-2100 and count(e,item)==before[1]+1
            e.press('A',90);wait_menu(e,'Task_BuyMenu')
            print('PASS: native shop purchase of held evolution item',item,'costs 2100',flush=True)
        e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
        assert party==[monfield(e,i,0,0)&65535 for i in range(6)]
    finally:e.close()

cases=[('HAPPINY','CHANSEY',56,12,0,0),('SNEASEL','WEAVILE',57,22,0,0),('GLIGAR','GLISCOR',58,22,0,0),
       ('HAPPINY','HAPPINY',56,22,0,0),('SNEASEL','SNEASEL',57,12,0,0),('GLIGAR','GLIGAR',58,12,0,0),
       ('HAPPINY','HAPPINY',57,12,0,0),('SNEASEL','SNEASEL',57,22,0,1),('GLIGAR','GLIGAR',0,22,0,0),
       ('HAPPINY','CHANSEY',56,22,1,0),('GLIGAR','GLISCOR',58,12,2,0),
       ('BULBASAUR','IVYSAUR',58,12,0,0)]
selected=set(map(int,args.cases.split(','))) if args.cases else set(range(len(cases)))
for n,(species,target,item,hour,mode,shadow) in enumerate(cases):
    if n not in selected:continue
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);clock(e,hour,mode)
        fixture(e,species,255,0 if n==0 else item,shadow);moves_fixture(e,'MOVE_TACKLE')
        if n==0:
            sb=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
            e.write(sb+0x314,item,2);e.write(sb+0x316,1^key,2)
            give(e,ids['SPECIES_'+species],item)
        candy(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,target)
        assert monfield(e,0,0,0)>>16==(0 if species!=target and species in ('HAPPINY','SNEASEL','GLIGAR') else item),(n,'held item consumption')
        print('PASS:',n,species,'->',target,'hour',hour,'override',mode,'held item',item,flush=True)
        if n==2:
            field(e);start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/'test-output/held-gliscor.sav')
    finally:e.close()
if args.cases is not None:raise SystemExit(0)

# Cancel at the native cancellable sprite-cycle state, then retry successfully.
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);clock(e,22)
    fixture(e,'GLIGAR',255,58,0);moves_fixture(e,'MOVE_TACKLE')
    start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');p=e.symbols['gBagMenuState']
    for _ in range(5):
        if e.read(p+6,2)==0:break
        e.press('LEFT',90)
    for _ in range(45):
        if e.read(p+8,2)+e.read(p+14,2)==0:break
        e.press('UP',30)
    e.press('A',90);e.press('A',180);e.press('A',180)
    task=None
    for _ in range(1600):
        for i in range(16):
            q=e.symbols['gTasks']+40*i
            if e.read(q+4,1) and e.read(q)&~1==e.symbols['Task_EvolutionScene']&~1 and e.read(q+8,2)==8:task=q
        if task is not None:break
        e.frames(1,'A' if _%60==0 else 0)
    assert task is not None,'Did not reach cancellable native evolution'
    e.frames(2,'B')
    for _ in range(60):e.press('A',90)
    field(e)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_GLIGAR'] and monfield(e,0,0,0)>>16==58
    assert count(e,68)==0
    print('PASS: cancelling evolution keeps Gligar and its Razor Fang; the used Rare Candy stays consumed',flush=True)
    key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2);sb=e.read('gSaveBlock1Ptr')
    e.write(sb+0x310,68,2);e.write(sb+0x312,1^key,2);candy(e)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_GLISCOR'] and monfield(e,0,0,0)>>16==0
    print('PASS: next successful level-up consumes the preserved Razor Fang',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'held-gliscor',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_GLISCOR'] and monfield(e,0,0,0)>>16==0
    extra=ids['SPECIES_GLISCOR']-440;mask=1<<(extra%8);sb=e.read('gSaveBlock2Ptr')
    assert e.read(sb+0xb20+extra//8,1)&mask and e.read(sb+0xb70+extra//8,1)&mask
    print('PASS: Gliscor, consumed held item and seen/caught entries survive native Save/cold Continue',flush=True)
finally:e.close()
