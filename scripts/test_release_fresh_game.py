"""Play the documented route from a fresh game using normal controls."""
import sys
from emulator import Emulator, ROOT
from test_country import start_new_game, wait_menu, party_species
from test_landmark_cases import go as go_map, save
from test_tour import travel, guide, item_count
from test_trainers import defeated, fight
from test_challenges import fight_with_supplies
from test_garden import choose
from test_celebi import researcher, visit_forest, accept_sighting, return_to_ada, report, load_checkpoint
from test_time import cross, child, keeper
from test_departure import visit_post, notice, dispatcher, back_to_refuge
from test_evac import board_train, host
from test_message import offer, finish_account
from test_relief import to_reception, finish_relief
from test_garden import enter as enter_garden, luc, pidgey
from test_amiens import finish_arrival
from test_reunion import finish_reunion
from test_amiens_account import archive
from test_amiens_news import finish_news
from test_rouen import board as to_rouen, leon
from test_rouen_book import finish_book
from test_le_havre import clerk as to_port, captain
from test_dock_check import finish_check
from test_southampton import clerk as to_south, host as south_host
from test_luggage import finish_luggage
from test_london_past import clerk as to_london, rose
from test_oxford_gym import gym_fight as rock_fight, badge as badge1
from test_chantilly_gym import approach as water_approach, gym_fight as water_fight, badge as badge2
from test_oranienburg_gym import gym_fight as electric_fight, badge as badge3
from test_france_story import gardens, forest
from test_shops import confirm_purchase


def go(e, target):
    if e.location()[1] not in (1, 13):
        return go_map(e, target)
    # Both English routes have an uninterrupted central lane at x=15.
    group,index,x,y=e.location()
    if x!=15:e.walk('LEFT' if x>15 else 'RIGHT',abs(x-15))
    if y!=target[1]:e.walk('UP' if y>target[1] else 'DOWN',abs(y-target[1]))
    if target[0]!=15:e.walk('RIGHT' if target[0]>15 else 'LEFT',abs(target[0]-15))
    assert e.location()==(group,index,*target)


def long_report(e):
    researcher(e)
    for _ in range(160):
        if not e.read('sLockFieldControls',1):return
        e.press('A',90)
    raise AssertionError('Ada conclusion did not finish')


def speak(e, point=(10, 14), facing='DOWN', yes=False):
    go(e, point); e.press(facing); e.press('A', 180)
    if yes: choose(e)
    else: e.finish_dialogue()


def town(e, destination):
    go(e, (16, 14)); travel(e, destination)


def heal(e):
    go(e, (6, 10)); e.walk('UP', 1); e.frames(180)
    e.walk('UP', 4); e.walk('RIGHT', 1); e.press('UP'); e.press('A', 180); e.finish_dialogue()
    e.walk('DOWN', 5); e.frames(180)


def battle(e, method):
    wait_menu(e, 'Task_YesNoMenu_HandleInput'); e.press('A', 180)
    for _ in range(30):
        if e.in_battle(): break
        e.press('A', 90)
    assert e.in_battle(); e.frames(300); method(e)


def supplies(e, quantity=5):
    go(e, (23, 10)); e.walk('UP', 1); e.frames(180); e.walk('UP', 1)
    go(e, (1, 7)); e.press('UP'); e.press('A', 180)
    wait_menu(e, 'Task_ShopMenu'); e.press('A', 180); wait_menu(e, 'Task_BuyMenu')
    e.press('DOWN'); confirm_purchase(e, quantity); e.press('A', 180)
    wait_menu(e, 'Task_ReturnToItemListAfterItemPurchase'); e.press('A', 90); e.press('B', 180)
    wait_menu(e, 'Task_ShopMenu'); e.press('B', 180); e.finish_dialogue()
    go(e, (4, 7)); e.walk('DOWN', 2); e.frames(180)


def train_mudkip(e):
    def enter_grass():
        go(e,(15,23));e.walk('DOWN',1);e.frames(120)
        assert e.location()[:2]==(43,21)
        e.walk('DOWN',10);e.walk('LEFT',2)
    def return_to_clinic():
        while e.location()[2]<15:
            e.frames(8,'RIGHT')
            if e.in_battle():e.frames(300);rock_fight(e);e.frames(180)
        e.walk('UP',e.location()[3]);e.walk('UP',1);e.frames(120)
        assert e.location()[:2]==(43,20)
        heal(e)
    heal(e);enter_grass();count=0
    while e.read(e.symbols['gPlayerParty']+84,1)<16:
        for _ in range(3000):
            if e.in_battle():break
            x=e.location()[2];e.frames(8,'LEFT' if x>11 else 'RIGHT')
        assert e.in_battle(),'No training encounter'
        e.frames(300);rock_fight(e);e.frames(180)
        count+=1;assert count<80
        print('Training encounter',count,'level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
        if count%6==0 and e.read(e.symbols['gPlayerParty']+84,1)<16:
            return_to_clinic();save(e,'walkthrough-germany-training');enter_grass()
    for _ in range(80):
        if party_species(e)==284:break
        e.press('A',90)
    assert party_species(e)==284,'Mudkip did not evolve to Marshtomp'
    return_to_clinic()


country_option = sys.argv[sys.argv.index('--country')+1] if '--country' in sys.argv else 'england'
assert country_option in ('england','france','germany')
selected_country = ('england','france','germany').index(country_option)
assert '--country' in sys.argv
PREFIX = 'release-'+country_option+'-'
STARTS = [(0,0),(1,0),(2,2)] if '--country' not in sys.argv else [(selected_country,2 if selected_country==2 else 0)]

e = Emulator(ROOT / 'pokefirered.gba')
try:
    if '--resume-ending' in sys.argv:
        load_checkpoint(e, PREFIX + 'london-ending', True)
    else:
        start_new_game(e)
        # Each selection starts from the genuine, newly initialized country menu.
        for country, starter in STARTS:
            for _ in range(country): e.press('DOWN')
            e.press('A', 180); wait_menu(e, 'Task_MultichoiceMenu_HandleInput')
            for _ in range(starter): e.press('DOWN')
            e.press('A', 180); choose(e)
            assert e.location() == (43, country * 4, 15, 14)
            if country: town(e, 0)
            speak(e, yes=True); assert e.var(0x40FB) == 1 and e.var(0x40F0) == country + 1
            print('PASS: fresh country '+str(country)+' reaches London and accepts the field study', flush=True)

        assert e.var(0x40F0)==selected_country+1
        assert party_species(e)==(1,152,283)[selected_country]
        # Prepare ordinary Potions before Oliver; use native clinic care.
        supplies(e,5);heal(e)
        # Oliver, then Alice, with ordinary clinic healing between battles.
        go(e, (15, 1)); e.walk('UP', 2); e.frames(90)
        go(e, (17, 19)); e.press('UP'); e.press('A', 180); battle(e, fight_with_supplies)
        assert defeated(e, 0),(e.location(),e.read(e.symbols['gPlayerParty']+84,1))
        go(e, (15, 23)); e.walk('DOWN', 1); e.frames(90); heal(e)
        go(e, (15, 1)); e.walk('UP', 2); e.frames(90)
        go(e, (15, 0)); e.walk('UP', 1); e.frames(90)
        go(e, (17, 19)); e.press('UP'); e.press('A', 180); battle(e, fight_with_supplies)
        assert defeated(e, 3)
        go(e, (15, 0)); e.walk('UP', 1); e.frames(90); heal(e)
        go(e, (10, 14)); e.press('DOWN'); e.press('A', 180); battle(e, fight_with_supplies)
        assert defeated(e, 6)
        town(e, 0); speak(e); assert e.var(0x40FB) == 2
        town(e, 3); heal(e); go(e, (15, 10)); e.walk('UP', 1); e.frames(180)
        e.walk('UP', 8); e.press('UP'); e.press('A', 180); battle(e, rock_fight)
        assert badge1(e); e.walk('DOWN', 10); e.frames(180)
        save(e, PREFIX + 'badge-one')
        print('PASS: fresh '+country_option+' route wins Oliver, Alice, rival and Ellis, reports to Oak aide and earns badge one', flush=True)

        town(e, 1); speak(e, yes=True); assert e.var(0x40FD) == 1
        go(e, (16, 14)); gardens(e); town(e, 4); forest(e)
        speak(e); assert e.var(0x40FD) == 5
        town(e, 1); speak(e); assert e.var(0x40FD) == 6
        town(e, 4); heal(e); go(e, (15, 10)); e.walk('UP', 1); e.frames(180)
        water_approach(e); e.press('UP'); e.press('A', 180); battle(e, water_fight)
        assert badge2(e)
        from test_germany_story import leave_gym
        leave_gym(e); save(e, PREFIX + 'badge-two')
        print('PASS: fresh route records both survey sites, gets Remy review and Celine reward, and beats Marine', flush=True)

        town(e, 2); speak(e, yes=True); assert e.var(0x40FF) == 1
        town(e, 5); speak(e); assert e.var(0x40FF) == 2
        town(e, 2); speak(e); assert e.var(0x40FF) == 3
        town(e, 5); supplies(e,10 if selected_country==2 else 5); heal(e)
        if selected_country==2:train_mudkip(e)
        go(e, (15, 10)); e.walk('UP', 1); e.frames(180); e.walk('UP', 8)
        e.press('UP'); e.press('A', 180); battle(e, electric_fight)
        assert badge3(e); e.walk('DOWN', 10); e.frames(180)
        save(e, PREFIX + 'badge-three')
        print('PASS: fresh route delivers Karl parcel, returns Lena report and beats Conrad for badge three', flush=True)

        town(e, 3); go(e, (18, 14)); researcher(e); choose(e)
        visit_forest(e); accept_sighting(e); return_to_ada(e); report(e)
        assert e.var(0x40EE) == 3
        visit_forest(e); cross(e); child(e); keeper(e); child(e); assert e.var(0x40ED) == 4
        visit_post(e); notice(e); dispatcher(e); back_to_refuge(e); keeper(e)
        assert e.var(0x40EC) == 4
        visit_post(e); board_train(e); host(e); offer(e); choose(e); e.walk('LEFT', 3)
        finish_account(e); assert e.var(0x40E4) == 4
        save(e, PREFIX + 'first-account')
        print('PASS: fresh route listens to Celebi, helps Elise, verifies departures, carries both messages and records Ada account', flush=True)

        visit_forest(e); to_reception(e); finish_relief(e)
        enter_garden(e); luc(e); pidgey(e); luc(e); assert e.var(0x40E2) == 3
        finish_arrival(e); finish_reunion(e)
        cross(e); return_to_ada(e); archive(e); assert e.var(0x40DF) == 1
        visit_forest(e); finish_news(e); to_rouen(e); leon(e); finish_book(e)
        assert e.var(0x40DC) == 3
        to_port(e); captain(e); finish_check(e); to_south(e); south_host(e); finish_luggage(e)
        to_london(e); rose(e); assert e.var(0x40D5) == 2
        save(e, PREFIX + 'london-ending')
        print('PASS: fresh route completes supplies, both reunions, Amiens account/news, Rouen book, dock and luggage clearance and Rose ending', flush=True)

    cross(e); return_to_ada(e); long_report(e)
    save(e, PREFIX + 'complete')
    e.screenshot(ROOT / f'test-output/{PREFIX}ada-ending.png')
finally:
    e.close()

e = Emulator(ROOT / 'pokefirered.gba')
try:
    load_checkpoint(e, PREFIX + 'complete', True)
    assert e.var(0x40F0)==selected_country+1
    assert e.var(0x40D5) == 2 and badge1(e) and badge2(e) and badge3(e)
    long_report(e); assert not e.read('sLockFieldControls', 1) and e.var(0x40CC)==1
    print('PASS: fresh-route ending save cold Continues with all three badges and repeatable Ada conclusion', flush=True)
finally:
    e.close()
