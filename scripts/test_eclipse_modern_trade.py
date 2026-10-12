"""Native modern trade-item paths, purchases, guards and cold-save QA."""
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
parser=argparse.ArgumentParser();parser.add_argument('--cases');parser.add_argument('--shop-only',action='store_true');parser.add_argument('--chain-only',action='store_true');args=parser.parse_args()
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
if args.cases is None and not args.chain_only:
    # Split earned-money checkpoints: each has 8,544, below all seven prices.
    for purchase_group in ((60,61,62,72),(82,87,88)):
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
            party=[monfield(e,i,0,0)&65535 for i in range(6)]
            go(e,(30,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
            stock=e.symbols['Shadow_ShopItems'];items=[]
            while e.read(stock+2*len(items),2):items.append(e.read(stock+2*len(items),2))
            shop=e.symbols['sShopData'];metadata=json.loads((ROOT/'src/data/items.json').read_text())['items']
            for item in purchase_group:
                index=items.index(item)
                for _ in range(70):
                    cur=e.read(shop+12,2)+e.read(shop+14,2)
                    if cur==index:break
                    e.press('DOWN' if cur<index else 'UP',30)
                assert cur==index;before=(money(e),count(e,item))
                base=e.read('gSaveBlock1Ptr')+0x310
                print('Purchase resources',item,'money',before[0],'empty bag slots',sum(e.read(base+4*j,2)==0 for j in range(42)),flush=True)
                confirm_purchase(e,1);e.press('A',180)
                wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
                assert money(e)==before[0]-metadata[item]['price'] and count(e,item)==before[1]+1
                e.press('A',90);wait_menu(e,'Task_BuyMenu')
                print('PASS: native purchase',metadata[item]['english'],metadata[item]['price'],flush=True)
            e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
            assert party==[monfield(e,i,0,0)&65535 for i in range(6)]
        finally:e.close()
if args.shop_only:raise SystemExit(0)
if args.chain_only:
    from natural_preparation_test_helpers import give
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'PORYGON',255,218,0)
        sb=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
        e.write(sb+0x310,59,2);e.write(sb+0x312,2^key,2)
        e.write(sb+0x314,72,2);e.write(sb+0x316,1^key,2)
        use(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_PORYGON2'] and monfield(e,0,0,0)>>16==0 and count(e,59)==1
        give(e,ids['SPECIES_PORYGON2'],72);use(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_PORYGON_Z'] and monfield(e,0,0,0)>>16==0 and count(e,59)==0
        start_action(e,4)
        for _ in range(8):e.press('A',240)
        e.battery(ROOT/'test-output/modern-porygon-chain.sav')
        print('PASS: native Porygon -> Porygon2, Give Dubious Disc -> Porygon-Z; exactly two cables and both held items consumed',flush=True)
    finally:e.close()
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'modern-porygon-chain',True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_PORYGON_Z'] and monfield(e,0,0,0)>>16==0 and count(e,59)==0 and count(e,72)==0
        print('PASS: completed Porygon chain and exact inventory survive native Save/cold Continue',flush=True)
    finally:e.close()
    raise SystemExit(0)
cases=[('ELECTABUZZ','ELECTIVIRE',60,0),('MAGMAR','MAGMORTAR',61,0),('RHYDON','RHYPERIOR',62,0),
 ('PORYGON2','PORYGON_Z',72,0),('DUSCLOPS','DUSKNOIR',82,0),('SPRITZEE','AROMATISSE',87,0),('SWIRLIX','SLURPUFF',88,0)]
cases += [(species,species,0,0) for species,target,held,shadow in cases]
cases += [('SPRITZEE','SPRITZEE',88,0),('SWIRLIX','SWIRLIX',87,0),('DUSCLOPS','DUSCLOPS',82,1),('ELECTABUZZ','ELECTABUZZ',195,0),('EEVEE','EEVEE',60,0)]
selected=set(map(int,args.cases.split(','))) if args.cases else set(range(len(cases)))
for n,(species,target,held,shadow) in enumerate(cases):
    if n not in selected:continue
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,species,255,held,shadow)
        sb=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
        e.write(sb+0x310,59,2);e.write(sb+0x312,2^key,2)
        use(e);success=species!=target
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,target)
        assert count(e,59)==(1 if success else 2),(n,'cable consumption')
        assert monfield(e,0,0,0)>>16==(0 if success else held),(n,'held consumption')
        print('PASS:',n,species,'->',target,'held',held,flush=True)
        if n==3:
            start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/'test-output/modern-porygon-z.sav')
    finally:e.close()
if 3 in selected:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'modern-porygon-z',True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_PORYGON_Z'] and monfield(e,0,0,0)>>16==0 and count(e,59)==1
        extra=ids['SPECIES_PORYGON_Z']-440;mask=1<<(extra%8);sb=e.read('gSaveBlock2Ptr')
        assert e.read(sb+0xb20+extra//8,1)&mask and e.read(sb+0xb70+extra//8,1)&mask
        print('PASS: Porygon-Z, cable/held consumption and seen/caught flags survive native Save/cold Continue',flush=True)
    finally:e.close()
