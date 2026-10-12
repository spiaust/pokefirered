"""Native solo trade evolution, matching held items and shop purchase QA."""
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
parser=argparse.ArgumentParser();parser.add_argument('--cases');parser.add_argument('--shop-only',action='store_true');args=parser.parse_args()
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
if args.cases is None:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
        party=[monfield(e,i,0,0)&65535 for i in range(6)]
        go(e,(30,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
        stock=e.symbols['Shadow_ShopItems'];items=[]
        while e.read(stock+2*len(items),2):items.append(e.read(stock+2*len(items),2))
        shop=e.symbols['sShopData'];metadata=json.loads((ROOT/'src/data/items.json').read_text())['items']
        for item in (59,187,199,201,218,192,193):
            index=items.index(item)
            for _ in range(70):
                cur=e.read(shop+12,2)+e.read(shop+14,2)
                if cur==index:break
                e.press('DOWN' if cur<index else 'UP',30)
            assert cur==index;before=(money(e),count(e,item));confirm_purchase(e,1);e.press('A',180)
            wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
            assert money(e)==before[0]-metadata[item]['price'] and count(e,item)==before[1]+1
            e.press('A',90);wait_menu(e,'Task_BuyMenu')
            print('PASS: native purchase',metadata[item]['english'],metadata[item]['price'],flush=True)
        e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
        assert party==[monfield(e,i,0,0)&65535 for i in range(6)]
    finally:e.close()
if args.shop_only:raise SystemExit(0)
cases=[('KADABRA','ALAKAZAM',0,0),('MACHOKE','MACHAMP',0,0),('GRAVELER','GOLEM',0,0),('HAUNTER','GENGAR',0,0),
 ('BOLDORE','GIGALITH',0,0),('GURDURR','CONKELDURR',0,0),('PHANTUMP','TREVENANT',0,0),('PUMPKABOO','GOURGEIST',0,0),
 ('POLIWHIRL','POLITOED',187,0),('ONIX','STEELIX',199,0),('SLOWPOKE','SLOWKING',187,0),('SEADRA','KINGDRA',201,0),
 ('SCYTHER','SCIZOR',199,0),('PORYGON','PORYGON2',218,0),('CLAMPERL','HUNTAIL',192,0),('CLAMPERL','GOREBYSS',193,0),
 ('ONIX','ONIX',0,0),('ONIX','ONIX',201,0),('KADABRA','KADABRA',195,0),('KADABRA','KADABRA',0,1),('EEVEE','EEVEE',0,0),
 ('MACHOKE','MACHAMP',58,0)]
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
        assert monfield(e,0,0,0)>>16==(0 if success and 8<=n<=15 else held),(n,'held consumption')
        print('PASS:',n,species,'->',target,'held',held,flush=True)
        if n==9:
            start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/'test-output/link-steelix.sav')
    finally:e.close()
if 9 in selected:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'link-steelix',True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_STEELIX'] and monfield(e,0,0,0)>>16==0 and count(e,59)==1
        print('PASS: Steelix and exact cable/held-item consumption survive native Save/cold Continue',flush=True)
    finally:e.close()
