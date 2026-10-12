"""Native evolution apples, purchases, guards and cold-save QA."""
import argparse,json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture,ids
from test_shadow_runtime import monfield,go
from test_continent_runtime import world
from test_gym_ui import start_action
from test_navigation import wait_task
from test_country import wait_menu
from test_shops import confirm_purchase
from test_trainers import money
from test_oxford_gym import count_pocket
from tm_teaching_test_helpers import field
parser=argparse.ArgumentParser();parser.add_argument('--shop-only',action='store_true');parser.add_argument('--cases-only',action='store_true');args=parser.parse_args()
def count(e,item):return count_pocket(e,item,0x310,42)
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

if not args.cases_only:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
        party=[monfield(e,i,0,0)&65535 for i in range(6)]
        go(e,(30,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
        stock=e.symbols['Shadow_ShopItems'];items=[]
        while e.read(stock+2*len(items),2):items.append(e.read(stock+2*len(items),2))
        shop=e.symbols['sShopData']
        for item in (89,90,91):
            index=items.index(item)
            for _ in range(80):
                cur=e.read(shop+12,2)+e.read(shop+14,2)
                if cur==index:break
                e.press('DOWN' if cur<index else 'UP',30)
            assert cur==index;before=(money(e),count(e,item));confirm_purchase(e,1);e.press('A',180)
            wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
            assert money(e)==before[0]-2100 and count(e,item)==before[1]+1
            e.press('A',90);wait_menu(e,'Task_BuyMenu');print('PASS: native apple purchase',item,2100,flush=True)
        e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
        assert party==[monfield(e,i,0,0)&65535 for i in range(6)]
    finally:e.close()
if args.shop_only:raise SystemExit(0)
cases=[('APPLIN','FLAPPLE',89,0,0),('APPLIN','APPLETUN',90,0,0),('APPLIN','DIPPLIN',91,0,0),
 ('APPLIN','APPLIN',95,0,0),('SQUIRTLE','SQUIRTLE',89,0,0),('APPLIN','APPLIN',89,0,1),('APPLIN','APPLIN',90,195,0),('DIPPLIN','DIPPLIN',91,0,0),('APPLIN','DIPPLIN',91,87,0)]
for n,(species,target,item,held,shadow) in enumerate(cases):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,species,255,held,shadow)
        sb=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
        e.write(sb+0x310,item,2);e.write(sb+0x312,2^key,2);use(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
        assert count(e,item)==(1 if species!=target else 2) and monfield(e,0,0,0)>>16==held
        print('PASS:',n,species,'->',target,'item',item,flush=True)
        if n==2:
            start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/'test-output/apples-dipplin.sav')
    finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'apples-dipplin',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_DIPPLIN'] and count(e,91)==1
    extra=ids['SPECIES_DIPPLIN']-440;mask=1<<(extra%8);sb=e.read('gSaveBlock2Ptr')
    assert e.read(sb+0xb20+extra//8,1)&mask and e.read(sb+0xb70+extra//8,1)&mask
    print('PASS: Dipplin, remaining Syrupy Apple and seen/caught flags survive Save/cold Continue',flush=True)
finally:e.close()
