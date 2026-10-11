"""Native purchases and stone evolutions; species and inventory fixtures are explicit."""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world
from test_shadow_runtime import go, monfield
from test_eclipse_friendship import fixture, ids
from test_eclipse_gender_evolution import gender_fixture
from test_gym_ui import start_action
from test_navigation import wait_task
from test_country import wait_menu
from test_shops import confirm_purchase
from test_trainers import money
from test_oxford_gym import count_pocket
from tm_teaching_test_helpers import field
from eclipse_evolutions import project

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

import argparse
parser=argparse.ArgumentParser();parser.add_argument('--cases');args=parser.parse_args()
if args.cases is None:
    # Purchase all four stones with earned money, keeping the original party intact.
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
        before_party=[monfield(e,i,0,0)&65535 for i in range(6)]
        go(e,(30,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
        stock=e.symbols['Shadow_ShopItems'];items=[]
        while e.read(stock+2*len(items),2):items.append(e.read(stock+2*len(items),2))
        shop=e.symbols['sShopData']
        for item in (52,53,54,55):
            index=items.index(item)
            for _ in range(60):
                cur=e.read(shop+12,2)+e.read(shop+14,2)
                if cur==index:break
                e.press('DOWN' if cur<index else 'UP',30)
            assert cur==index;before=(money(e),count(e,item));confirm_purchase(e,1);e.press('A',180)
            wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
            assert money(e)==before[0]-2100 and count(e,item)==before[1]+1
            e.press('A',90);wait_menu(e,'Task_BuyMenu')
            print('PASS: native shop purchase of stone',item,'costs 2100',flush=True)
        e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
        assert before_party==[monfield(e,i,0,0)&65535 for i in range(6)]
    finally:e.close()

cases=[('TOGETIC','TOGEKISS',52,False,0,0),('ROSELIA','ROSERADE',52,False,0,0),
 ('MURKROW','HONCHKROW',53,False,0,0),('MISDREAVUS','MISMAGIUS',53,False,0,0),
 ('KIRLIA','GALLADE',54,False,0,0),('SNORUNT','FROSLASS',54,True,0,0),
 ('EEVEE','LEAFEON',98,False,0,0),('EEVEE','GLACEON',55,False,0,0),
 ('MINCCINO','CINCCINO',52,False,0,0),('LAMPENT','CHANDELURE',53,False,0,0),
 ('FLOETTE','FLORGES',52,True,0,0),('DOUBLADE','AEGISLASH',53,False,0,0),
 ('CRABRAWLER','CRABOMINABLE',55,False,0,0),('CETODDLE','CETITAN',55,False,0,0),
 ('KIRLIA','KIRLIA',54,True,0,0),('SNORUNT','SNORUNT',54,False,0,0),
 ('TOGETIC','TOGETIC',53,False,0,0),('TOGETIC','TOGETIC',52,False,195,0),
 ('TOGETIC','TOGETIC',52,False,0,1),
 ('EEVEE','FLAREON',95,False,0,0),('EEVEE','JOLTEON',96,False,0,0),('EEVEE','VAPOREON',97,False,0,0)]
selected=set(map(int,args.cases.split(','))) if args.cases else set(range(len(cases)))
for n,(species,target,item,female,held,shadow) in enumerate(cases):
    if n not in selected:continue
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True)
        fixture(e,species,255,held,shadow);gender_fixture(e,female)
        p=e.read('gSaveBlock1Ptr')+0x310;k=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
        e.write(p,item,2);e.write(p+2,2^k,2);use(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,target,monfield(e,0,0,0)&65535)
        assert count(e,item)==(1 if species!=target else 2),(n,count(e,item))
        print('PASS:',n,species,'->',target,'stone',item,'consumption',2-count(e,item),flush=True)
        if n==13:
            start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/'test-output/stone-cetitan.sav')
    finally:e.close()
if 13 in selected:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'stone-cetitan',True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_CETITAN'] and count(e,55)==1
        print('PASS: evolved Cetitan and remaining Ice Stone survive Save/cold Continue')
    finally:e.close()
body='.evolutions = EVOLUTION({EVO_ITEM, ITEM_DAWN_STONE, SPECIES_GALLADE, CONDITIONS({IF_GENDER, MON_MALE})}),'
assert project(body,set(ids),{'ITEM_DAWN_STONE'})[0]==[('EVO_ITEM_MALE','ITEM_DAWN_STONE','SPECIES_GALLADE')]
assert not project(body.replace('{IF_GENDER, MON_MALE}','{IF_GENDER, MON_MALE},{IF_TIME, TIME_NIGHT}'),set(ids),{'ITEM_DAWN_STONE'})[0]
print('PASS: conditional stone projection retains gender and rejects extra conditions')
