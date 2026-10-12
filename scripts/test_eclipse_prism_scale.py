"""Native Prism Scale purchases, Give, evolution guards, Beauty and cold-save QA."""
import argparse, json
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture, ids
from test_shadow_runtime import monfield, go
from test_continent_runtime import world
from test_gym_ui import start_action
from test_navigation import wait_task
from test_country import wait_menu
from test_shops import confirm_purchase
from test_trainers import money
from test_oxford_gym import count_pocket
from tm_teaching_test_helpers import field
def count(e,item):return count_pocket(e,item,0x310,42)
def use(e):
    start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');p=e.symbols['gBagMenuState']
    for _ in range(5):
        if e.read(p+6,2)==0:break
        e.press('LEFT',90)
    bag=e.read('gSaveBlock1Ptr')+0x310
    target=next(i for i in range(42) if e.read(bag+4*i,2)==59)
    for _ in range(60):
        cur=e.read(p+8,2)+e.read(p+14,2)
        if cur==target:break
        e.press('DOWN' if cur<target else 'UP',30)
    assert cur==target
    e.press('A',90);e.press('A',180);wait_task(e,'Task_HandleChooseMonInput');e.press('A',180)
    for _ in range(60):e.press('A',90)
    field(e)

from natural_preparation_test_helpers import give
from test_eclipse_friendship import candy,orders

def beauty(e,value):
    p=e.symbols['gPlayerParty'];person=e.read(p);key=person^e.read(p+4)
    raw=bytearray().join((e.read(p+32+4*i)^key).to_bytes(4,'little') for i in range(12))
    raw[12*orders[person%24][2]+7]=value
    e.write(p+28,sum(int.from_bytes(raw[i:i+2],'little') for i in range(0,48,2))&65535,2)
    for i in range(12):e.write(p+32+4*i,int.from_bytes(raw[4*i:4*i+4],'little')^key)

def cable_bag(e):
    sb=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
    e.write(sb+0x310,59,2);e.write(sb+0x312,2^key,2)

def shop(e,item):
    go(e,(30,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
    stock=e.symbols['Shadow_ShopItems'];items=[]
    while e.read(stock+2*len(items),2):items.append(e.read(stock+2*len(items),2))
    index=items.index(item);q=e.symbols['sShopData']
    for _ in range(100):
        cur=e.read(q+12,2)+e.read(q+14,2)
        if cur==index:break
        e.press('DOWN' if cur<index else 'UP',30)
    assert cur==index;before=(money(e),count(e,item));confirm_purchase(e,1);e.press('A',180)
    wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
    assert money(e)==before[0]-2100 and count(e,item)==before[1]+1
    if item==105:e.screenshot(ROOT/'test-output/prism-scale-shop.png')
    e.press('A',90);wait_menu(e,'Task_BuyMenu');e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue();field(e)

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0);fixture(e,'FEEBAS',255,0,0);beauty(e,0)
    party=[monfield(e,i,0,0) for i in range(6)]
    shop(e,59);shop(e,105)
    assert party==[monfield(e,i,0,0) for i in range(6)]
    give(e,ids['SPECIES_FEEBAS'],105)
    assert count(e,105)==0 and count(e,59)==1 and count(e,68)==1
    use(e)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_MILOTIC'] and monfield(e,0,0,0)>>16==0
    assert count(e,59)==0 and count(e,105)==0
    start_action(e,4)
    for _ in range(8):e.press('A',240)
    e.battery(ROOT/'test-output/prism-milotic.sav')
    print('PASS: native shop purchases, Give Prism Scale and Link Cable evolve zero-Beauty Feebas; both items consumed',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'prism-milotic',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_MILOTIC'] and monfield(e,0,0,0)>>16==0
    assert count(e,59)==0 and count(e,105)==0
    sb=e.read('gSaveBlock2Ptr');index=350-1;mask=1<<(index%8)
    assert e.read(sb+0x28+index//8,1)&mask and e.read(sb+0x5c+index//8,1)&mask
    print('PASS: native cold Continue preserves Milotic, consumed items and seen/caught Dex flags',flush=True)
finally:e.close()

for species,held,shadow in [('FEEBAS',0,0),('FEEBAS',201,0),('FEEBAS',195,0),('FEEBAS',105,1),('MAGIKARP',105,0),('MILOTIC',105,0)]:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,species,255,held,shadow);beauty(e,0);cable_bag(e)
        use(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+species] and monfield(e,0,0,0)>>16==held
        assert count(e,59)==2
        print('PASS: cable guard',species,'held',held,'shadow',shadow,flush=True)
    finally:e.close()
for value,held,target in [(169,0,'FEEBAS'),(170,0,'MILOTIC'),(170,105,'MILOTIC')]:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'FEEBAS',255,held,0);beauty(e,value)
        candy(e);field(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target] and monfield(e,0,0,0)>>16==held
        print('PASS: native Beauty boundary',value,'->',target,'held item retained',held,flush=True)
    finally:e.close()
