"""Use the normal Save/Continue menus, with a fresh emulator per reload."""
import argparse
from emulator import Emulator, ROOT
from test_tour import STAMPS, REWARDED, EXP_SHARE, guide, item_count
from test_country import party_species
from test_trainers import defeated, money, talk
from test_shops import balls
from test_cities import maps_in_bag
from test_navigation import wait_task
from rail_test_helpers import BOOKING, finish_saved_journey

cases = [f"start-{country}" for country in ("england", "france", "germany")]
cases.append("train-0-to-2")
cases.extend(("tour-partial", "tour-complete"))
cases.extend(f"start-{country}-{choice}" for country in ("england", "france", "germany") for choice in range(3))
cases.extend(f"trainer-{country}-won" for country in ("england", "france", "germany"))
cases.extend(f"shop-{country}-bought" for country in ("england", "france", "germany"))
cases.append("trainer-all-won")
cases.extend(f"navigation-{country}" for country in ("england", "france", "germany"))
cases.extend(("oxford-arrival", "oxford-trail", "oxford-station",
              "navigation-oxford", "shop-oxford-bought", "train-0-to-3", "train-3-to-1"))
cases.extend(("chantilly-arrival", "chantilly-trail", "chantilly-station",
              "navigation-chantilly", "shop-chantilly-bought", "train-1-to-4", "train-4-to-2"))
cases.extend(("oranienburg-arrival", "oranienburg-trail", "oranienburg-station",
              "navigation-oranienburg", "shop-oranienburg-bought", "train-2-to-5", "train-5-to-0"))
cases.extend(("rail-transfer-london", "rail-transfer-paris", "rail-transfer-berlin", "rail-paused-outside"))
cases.extend(f"challenge-{country}-{stage}" for country in ("england", "france", "germany")
             for stage in ("won", "reward", "pending"))
cases.extend(("story-active", "story-rival-won", "story-report-ready", "story-complete", "story-pending"))
cases.extend(("gym-entrance", "gym-complete", "gym-pending-tm", "gym-pending-key"))
cases.extend(f"france-{stage}" for stage in ("active", "gardens", "forest", "both", "report", "complete", "pending"))
cases.extend(("water-gym-entrance", "water-gym-complete", "water-gym-pending-tm", "water-gym-pending-key"))
cases.extend(f"germany-{stage}" for stage in ("active", "delivered", "report", "complete", "pending"))
cases.extend(("electric-gym-entrance", "electric-gym-complete", "electric-gym-pending-tm", "electric-gym-pending-key"))
cases.extend(("ferry-london", "ferry-oxford", "ferry-bicycle", "ferry-booking"))
cases.extend(("ride-london", "ride-oxford", "ride-bank", "ride-booking"))
cases.extend(("coast-dover", "coast-calais", "coast-return", "coast-booking"))
cases.extend(f"celebi-{stage}" for stage in ("active", "forest", "sighting", "report", "complete", "pending"))
cases.extend(f"time-{stage}" for stage in ("ready", "arrival", "child", "blanket", "returned", "complete", "booking"))
cases.extend(f"departure-{stage}" for stage in ("active", "notice", "confirmed", "returned", "delivered", "booking"))
cases.extend(f"evac-{stage}" for stage in ("ready", "arrival", "complete", "returned", "booking"))
cases.extend(f"message-{stage}" for stage in ("active", "delivered", "acknowledged", "report", "complete", "pending"))
cases.extend(f"relief-{stage}" for stage in ("ready", "active", "parcel", "returned", "complete", "tired"))
cases.extend(f"garden-{stage}" for stage in ("ready", "active", "found", "reception", "returned", "complete"))
cases.extend(('journal-pending', 'journal-complete'))
cases.extend(('tour-journal-pending', 'tour-journal-complete'))
cases.extend(f"amiens-{stage}" for stage in ('ready', 'arrival', 'briefed', 'notice', 'returned', 'complete'))
cases.extend(f"reunion-{stage}" for stage in ("active", "mira", "porter", "both", "verified", "returned", "complete"))
cases.extend(('amiens-care-tired', 'amiens-care-rested'))
cases.extend(('amiens-account-ready', 'amiens-account-complete'))
cases.extend(f'amiens-news-{stage}' for stage in ('ready','active','board','returned','checked','complete'))
cases.extend(f'rouen-{stage}' for stage in ('ready','arrival','returned','complete'))
cases.append('riverside-bank')
cases.extend(f'route-book-{stage}' for stage in ('ready','active','found','returned','complete'))
cases.extend(('rouen-care-tired','rouen-care-rested'))
cases.extend(('journal-pages-empty','journal-pages-complete'))
cases.extend(f'le-havre-{stage}' for stage in ('ready','arrival','returned','complete'))
cases.extend(f'dock-check-{stage}' for stage in ('ready','active','notice','returned','complete'))
cases.extend(('dock-care-tired', 'dock-care-rested'))
cases.extend(('port-account-ready', 'port-account-complete', 'port-account-returned'))
cases.extend(('port-return-forest', 'port-return-arrived', 'port-return-back'))
cases.extend(f'southampton-{s}' for s in ('ready','arrival','returned','complete'))
cases.extend(f'luggage-{s}' for s in ('ready','active','found','returned','complete'))
cases.extend(('south-care-tired','south-care-rested'))
cases.extend(('south-return-forest','south-return-arrived','south-return-back'))
cases.extend(('south-account-ready','south-account-complete','south-account-returned'))
cases.extend(f'london-past-{s}' for s in ('ready','arrival','returned','complete'))
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--case', action='append', choices=cases, help='Run selected checkpoints only; default is all.')
selected = parser.parse_args().case
if selected:
    cases = selected
for case in cases:
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        emu.state(ROOT / f"test-output/{case}.state", True)
        expected_location = emu.location()
        expected_country = emu.var(0x40F0)
        expected_party = emu.read("gPlayerPartyCount", 1)
        expected_tour = [emu.var(v) for v in (*STAMPS, REWARDED)]
        expected_reward = item_count(emu, EXP_SHARE)
        expected_starter = emu.var(0x40F6)
        expected_species = party_species(emu)
        expected_victories = [defeated(emu, i) for i in range(10)]
        expected_supplies = money(emu), balls(emu), item_count(emu, 13)
        expected_map_count = maps_in_bag(emu)
        expected_registered = emu.read(emu.read("gSaveBlock1Ptr") + 0x296, 2)
        expected_booking = emu.var(BOOKING)
        expected_challenges = [emu.var(v) for v in (0x40F8, 0x40F9, 0x40FA)]
        expected_candy = item_count(emu, 68)
        expected_story = emu.var(0x40FB)
        expected_bell = item_count(emu, 184)
        from test_oxford_gym import badge, tm_count, complete_talk
        expected_badge = badge(emu)
        expected_tm = tm_count(emu)
        expected_tm_reward = emu.var(0x40FC)
        from test_chantilly_gym import badge as badge2, tm_count as water_tm, complete_talk as marine_talk
        expected_water = badge2(emu), water_tm(emu), emu.var(0x40FE)
        expected_germany = emu.var(0x40FF), item_count(emu, 208)
        from test_oranienburg_gym import badge as badge3, tm_count as electric_tm, complete_talk as conrad_talk
        expected_electric = badge3(emu), electric_tm(emu), emu.var(0x40EF)
        expected_surfing = bool(emu.read("gPlayerAvatar",1)&8)
        from test_message import luxury_balls
        expected_message = emu.var(0x40E4)
        expected_relief = emu.var(0x40E3)
        expected_garden = emu.var(0x40E2)
        if case.startswith('south-care-'):
            from test_relief import health
            expected_south_health = health(emu)
        if case.startswith('dock-care-'):
            from test_relief import health
            expected_dock_health = health(emu)
        if case.startswith('rouen-care-'):
            from test_relief import health
            expected_rouen_health = health(emu)
        expected_london_past = emu.var(0x40D5)
        expected_south_account = emu.var(0x40D6)
        expected_luggage = emu.var(0x40D7)
        expected_southampton = emu.var(0x40D8)
        expected_port_account = emu.var(0x40D9)
        expected_dock_check = emu.var(0x40DA)
        expected_le_havre = emu.var(0x40DB)
        expected_route_book = emu.var(0x40DC)
        expected_rouen = emu.var(0x40DD)
        expected_amiens_news = emu.var(0x40DE)
        expected_account = emu.var(0x40DF)
        expected_reunion = emu.var(0x40E0)
        expected_amiens = emu.var(0x40E1)
        if case.startswith('amiens-care-'):
            from test_relief import health
            expected_care_health = health(emu)
        if case.startswith('relief-'):
            from test_relief import health, finish_relief, rest
            expected_health = health(emu)
        expected_luxury = luxury_balls(emu)
        expected_evac = emu.var(0x40E5)
        expected_news = emu.var(0x40EC)
        expected_past = emu.var(0x40ED)
        expected_celebi = emu.var(0x40EE)
        expected_survey = emu.var(0x40FD)
        expected_seed = item_count(emu, 205)
        emu.press("START", 60)
        count = emu.read("sNumStartMenuItems", 1)
        order = [emu.read(emu.symbols["sStartMenuOrder"] + i, 1) for i in range(count)]
        target = order.index(4)  # STARTMENU_SAVE
        cursor = emu.read("sStartMenuCursorPos", 1)
        for _ in range((target - cursor) % count):
            emu.press("DOWN")
        emu.press("A", 150)
        for _ in range(5):
            emu.press("A", 150)
        emu.screenshot(ROOT / f"test-output/{case}-saved.png")
        emu.battery(ROOT / f"test-output/{case}.sav")
    finally:
        emu.close()
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        emu.battery(ROOT / f"test-output/{case}.sav", True)
        emu.frames(600)
        emu.press("START", 480)
        emu.press("START", 180)
        emu.screenshot(ROOT / f"test-output/{case}-continue.png")
        emu.press("A", 300)
        emu.frames(300)
        emu.press("B", 90)  # Skip any optional quest-log playback.
        emu.finish_dialogue()
        assert emu.location() == expected_location, (case, emu.location(), expected_location)
        assert emu.var(0x40F0) == expected_country
        assert emu.read("gPlayerPartyCount", 1) == expected_party
        assert [emu.var(v) for v in (*STAMPS, REWARDED)] == expected_tour
        assert item_count(emu, EXP_SHARE) == expected_reward
        assert emu.var(0x40F6) == expected_starter
        assert party_species(emu) == expected_species
        assert [defeated(emu, i) for i in range(10)] == expected_victories
        assert (money(emu), balls(emu), item_count(emu, 13)) == expected_supplies
        assert maps_in_bag(emu) == expected_map_count
        assert emu.read(emu.read("gSaveBlock1Ptr") + 0x296, 2) == expected_registered
        assert emu.var(BOOKING) == expected_booking
        assert [emu.var(v) for v in (0x40F8, 0x40F9, 0x40FA)] == expected_challenges
        assert item_count(emu, 68) == expected_candy
        assert emu.var(0x40E4) == expected_message
        assert emu.var(0x40E3) == expected_relief
        assert emu.var(0x40E2) == expected_garden
        assert emu.var(0x40DA) == expected_dock_check
        assert emu.var(0x40DB) == expected_le_havre
        assert emu.var(0x40DC) == expected_route_book
        assert emu.var(0x40DD) == expected_rouen
        assert emu.var(0x40DE) == expected_amiens_news
        assert emu.var(0x40DF) == expected_account
        assert emu.var(0x40E0) == expected_reunion
        assert emu.var(0x40E1) == expected_amiens
        if case.startswith('relief-'):
            assert health(emu) == expected_health
        assert luxury_balls(emu) == expected_luxury
        assert emu.var(0x40E5) == expected_evac
        assert emu.var(0x40EC) == expected_news
        assert emu.var(0x40ED) == expected_past
        assert emu.var(0x40EE) == expected_celebi
        assert emu.var(0x40FB) == expected_story
        assert item_count(emu, 184) == expected_bell
        assert badge(emu) == expected_badge
        assert tm_count(emu) == expected_tm
        assert emu.var(0x40FC) == expected_tm_reward
        assert (badge2(emu), water_tm(emu), emu.var(0x40FE)) == expected_water
        assert (emu.var(0x40FF), item_count(emu,208)) == expected_germany
        assert emu.var(0x40D5) == expected_london_past
        if case.startswith('london-past-'):
            from test_london_past import finish_london
            finish_london(emu)
        assert emu.var(0x40D6) == expected_south_account
        if case.startswith('south-account-'):
            from test_south_account import finish_account
            finish_account(emu)
        assert emu.var(0x40D7) == expected_luggage
        if case.startswith('luggage-'):
            from test_luggage import finish_luggage
            finish_luggage(emu)
        assert emu.var(0x40D8) == expected_southampton
        if case.startswith('southampton-'):
            from test_southampton import finish_southampton
            finish_southampton(emu)
        assert emu.var(0x40D9) == expected_port_account
        if case.startswith('port-return-'):
            from test_port_return import verify_saved_return
            verify_saved_return(emu)
        if case.startswith('port-account-'):
            from test_port_account import finish_account
            finish_account(emu)
        if case.startswith('south-return-'):
            from test_south_return import verify_saved_return
            verify_saved_return(emu)
        if case.startswith('south-care-'):
            from test_southampton_care import rest
            assert health(emu) == expected_south_health
            rest(emu)
        if case.startswith('dock-care-'):
            from test_dock_care import rest
            assert health(emu) == expected_dock_health
            rest(emu)
        if case.startswith('dock-check-'):
            from test_dock_check import finish_check
            finish_check(emu)
        if case.startswith('le-havre-'):
            from test_le_havre import finish_port
            finish_port(emu)
        if case.startswith('route-book-'):
            from test_rouen_book import finish_book
            finish_book(emu)
        if case == 'riverside-bank':
            from test_rouen_riverside import return_from_bank
            return_from_bank(emu)
        if case.startswith('rouen-care-'):
            from test_rouen_care import rest
            assert health(emu) == expected_rouen_health
            rest(emu)
        elif case.startswith('rouen-'):
            from test_rouen import finish_rouen
            finish_rouen(emu)
        if case.startswith('reunion-'):
            from test_reunion import finish_reunion
            finish_reunion(emu)
        if case.startswith('amiens-care-'):
            from test_amiens_care import rest
            assert health(emu) == expected_care_health
            rest(emu)
        elif case.startswith('amiens-account-'):
            from test_amiens_account import archive
            archive(emu)
            assert emu.var(0x40DF) == 1
        elif case.startswith('amiens-news-'):
            from test_amiens_news import finish_news
            finish_news(emu)
        elif case.startswith('amiens-'):
            from test_amiens import finish_arrival
            finish_arrival(emu)
        if case.startswith('tour-journal-'):
            from test_tour_journal import inspect as inspect_tour
            inspect_tour(emu, 6 if case == 'tour-journal-pending' else 24)
        if case.startswith('journal-pages-'):
            from test_journal_pages import inspect_pages
            inspect_pages(emu, 0 if case.endswith('empty') else 8191)
        elif case.startswith('journal-'):
            from test_journal import inspect
            inspect(emu, 17 if case == 'journal-pending' else 24,
                    15 if case == 'journal-pending' else 127)
        if case.startswith('garden-'):
            from test_garden import finish_garden
            finish_garden(emu)
        if case.startswith('relief-'):
            finish_relief(emu)
            rest(emu)
            assert emu.var(0x40E4) == expected_message
        if case.startswith('germany-'):
            from test_france_story import talk as courier_talk
            if case in ('germany-report','germany-pending'):
                if case.endswith('pending'):
                    courier_talk(emu)
                    assert emu.var(0x40FF)==2 and item_count(emu,208)==0
                    save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
                    emu.write(save+0x310,0,2);emu.write(save+0x312,key,2)
                courier_talk(emu);courier_talk(emu)
                assert emu.var(0x40FF)==3 and item_count(emu,208)==1
            else:
                courier_talk(emu)
                assert (emu.var(0x40FF),item_count(emu,208))==expected_germany
        assert (badge3(emu), electric_tm(emu), emu.var(0x40EF)) == expected_electric
        if case == "electric-gym-complete":
            conrad_talk(emu)
            assert electric_tm(emu)==expected_electric[1] and money(emu)==expected_supplies[0]
        if case.startswith('electric-gym-pending-'):
            conrad_talk(emu)
            assert badge3(emu) and emu.var(0x40EF)==0
            save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
            if case.endswith('tm'):
                slot=next(i for i in range(58) if emu.read(save+0x464+i*4,2)==322)
                emu.write(save+0x466+slot*4,998^key,2)
            else:
                emu.write(save+0x3B8,0,2);emu.write(save+0x3BA,key,2)
            conrad_talk(emu);conrad_talk(emu)
            assert badge3(emu) and emu.var(0x40EF)==1
            assert electric_tm(emu)==(999 if case.endswith('tm') else 1)
        if case == "water-gym-complete":
            marine_talk(emu)
            assert water_tm(emu) == expected_water[1] and money(emu) == expected_supplies[0]
        if case.startswith("water-gym-pending-"):
            marine_talk(emu)
            assert badge2(emu) and emu.var(0x40FE) == 0
            save = emu.read('gSaveBlock1Ptr'); key = emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
            if case.endswith('tm'):
                slot = next(i for i in range(58) if emu.read(save+0x464+i*4,2)==291)
                emu.write(save+0x466+slot*4,998^key,2)
            else:
                emu.write(save+0x3B8,0,2);emu.write(save+0x3BA,key,2)
            marine_talk(emu);marine_talk(emu)
            assert badge2(emu) and emu.var(0x40FE)==1
            assert water_tm(emu)==(999 if case.endswith('tm') else 1)
        assert emu.var(0x40FD) == expected_survey
        assert item_count(emu, 205) == expected_seed
        if case.startswith("france-"):
            from test_france_story import talk as survey_talk, marker
            if case in ("france-gardens", "france-forest"):
                marker(emu)
                assert emu.var(0x40FD) == expected_survey
            elif case == "france-both":
                survey_talk(emu)
                assert emu.var(0x40FD) == 5 and item_count(emu, 205) == 0
            elif case in ("france-active", "france-complete"):
                survey_talk(emu)
                assert emu.var(0x40FD) == expected_survey
                assert item_count(emu, 205) == expected_seed
            elif case in ("france-report", "france-pending"):
                if case == "france-pending":
                    survey_talk(emu)
                    assert emu.var(0x40FD) == 5 and item_count(emu, 205) == 0
                    bag = emu.read("gSaveBlock1Ptr") + 0x310
                    key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20, 2)
                    emu.write(bag, 0, 2)
                    emu.write(bag + 2, key, 2)
                survey_talk(emu)
                assert emu.var(0x40FD) == 6 and item_count(emu, 205) == 1
                survey_talk(emu)
                assert item_count(emu, 205) == 1
        if case == "gym-complete":
            complete_talk(emu)
            assert tm_count(emu) == expected_tm and money(emu) == expected_supplies[0]
        if case.startswith("gym-pending-"):
            complete_talk(emu)
            assert emu.var(0x40FC) == 0 and badge(emu)
            save = emu.read("gSaveBlock1Ptr")
            key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20, 2)
            if case.endswith("tm"):
                emu.write(save + 0x466, 998 ^ key, 2)
            else:
                emu.write(save + 0x3B8, 0, 2)
                emu.write(save + 0x3BA, key, 2)
            complete_talk(emu)
            expected_count = 999 if case.endswith("tm") else 1
            assert emu.var(0x40FC) == 1 and tm_count(emu) == expected_count
            complete_talk(emu)
            assert tm_count(emu) == expected_count and badge(emu)
        if case in ("story-active", "story-rival-won", "story-complete"):
            from test_england_story import finished_talk
            finished_talk(emu)
            assert emu.var(0x40FB) == expected_story
            assert item_count(emu, 184) == expected_bell
            assert money(emu) == expected_supplies[0]
        if case in ("story-report-ready", "story-pending"):
            from test_england_story import finished_talk
            if case == "story-pending":
                finished_talk(emu)
                assert emu.var(0x40FB) == 1 and item_count(emu, 184) == 0
                bag = emu.read("gSaveBlock1Ptr") + 0x310
                key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20, 2)
                emu.write(bag, 0, 2)
                emu.write(bag + 2, key, 2)
            finished_talk(emu)
            assert emu.var(0x40FB) == 2 and item_count(emu, 184) == 1
            finished_talk(emu)
            assert item_count(emu, 184) == 1
        if case.startswith("challenge-") and case.endswith("reward"):
            guide(emu)
            assert item_count(emu, 68) == expected_candy
        if case.startswith("challenge-") and case.endswith("pending"):
            guide(emu)
            assert item_count(emu, 68) == 0
            bag = emu.read("gSaveBlock1Ptr") + 0x310
            key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20, 2)
            emu.write(bag, 0, 2)
            emu.write(bag + 2, key, 2)
            guide(emu)
            assert item_count(emu, 68) == 1
            guide(emu)
            assert item_count(emu, 68) == 1
        assert not emu.task_active("Task_MultichoiceMenu_HandleInput")
        emu.screenshot(ROOT / f"test-output/{case}-reloaded.png")
        if case in ("tour-partial", "tour-complete"):
            guide(emu)
            assert [emu.var(v) for v in (*STAMPS, REWARDED)] == expected_tour
            assert item_count(emu, EXP_SHARE) == expected_reward
        if case.startswith("trainer-"):
            talk(emu)
            emu.finish_dialogue()
            assert not emu.in_battle()
            assert money(emu) == expected_supplies[0]
        if case.startswith("navigation-"):
            emu.press("SELECT", 180)
            wait_task(emu, "Task_EuropeMap")
            assert emu.read("sEuropeMapCurrent", 1) == expected_location[1] // 4
            emu.press("B", 180)
            assert emu.location() == expected_location
            assert not emu.read("sLockFieldControls", 1)
        if case.startswith('message-'):
            from test_message import finish_account, free_ball_slot, MESSAGE
            if case == 'message-pending':
                from test_celebi import report
                report(emu)
                assert emu.var(MESSAGE) == 3 and luxury_balls(emu) == 0
                free_ball_slot(emu)
            finish_account(emu)
            assert emu.var(MESSAGE) == 4
            assert luxury_balls(emu) == expected_luxury + (case != 'message-complete')
        if case.startswith('evac-'):
            if case == 'evac-booking':
                from test_time import cross, resume_booking
                cross(emu)
                resume_booking(emu)
            else:
                from test_evac import finish_reception
                finish_reception(emu)
        if case.startswith('departure-'):
            from test_departure import finish_news
            if case == 'departure-booking':
                from test_time import cross, resume_booking
                cross(emu)
                resume_booking(emu)
            else:
                finish_news(emu)
        if case.startswith('time-'):
            from test_time import cross, finish_visit, resume_booking, PRESENT, PAST
            if case == 'time-booking':
                cross(emu)
                resume_booking(emu)
            else:
                if emu.location() == PRESENT:
                    cross(emu)
                finish_visit(emu)
                assert emu.location() == PRESENT and emu.var(PAST) == 4
        if case.startswith('celebi-'):
            from test_celebi import report, accept_sighting, return_to_ada, visit_forest, STORY
            if case == 'celebi-active':
                report(emu)
                visit_forest(emu)
                accept_sighting(emu)
            elif case == 'celebi-forest':
                accept_sighting(emu)
            elif case == 'celebi-sighting':
                return_to_ada(emu)
                report(emu)
                assert emu.var(STORY) == 3 and item_count(emu, 68) == expected_candy + 1
            elif case == 'celebi-complete':
                report(emu)
                assert emu.var(STORY) == 3 and item_count(emu, 68) == expected_candy
            else:
                if case == 'celebi-pending':
                    report(emu)
                    assert emu.var(STORY) == 2 and item_count(emu, 68) == 0
                    save = emu.read('gSaveBlock1Ptr')
                    key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
                    emu.write(save + 0x310, 0, 2)
                    emu.write(save + 0x312, key, 2)
                report(emu)
                report(emu)
                assert emu.var(STORY) == 3 and item_count(emu, 68) == expected_candy + 1
        if case.startswith('coast-'):
            from test_coast import crossing, leave_port, finish_coastal_booking
            if case=='coast-booking':
                finish_coastal_booking(emu)
                assert emu.location()[:2]==(43,10) and emu.var(BOOKING)==0
            elif case!='coast-return':
                crossing(emu);crossing(emu);leave_port(emu)
                assert emu.location()[1]==(0 if case=='coast-dover' else 4)
        if case.startswith('ride-'):
            from test_ride import dismount, ride
            assert bool(emu.read('gPlayerAvatar',1)&8)==expected_surfing
            if case=='ride-bank':
                emu.walk('UP',1);emu.walk('RIGHT',1);ride(emu);dismount(emu)
            else:
                dismount(emu)
                if case=='ride-booking':
                    from test_ferry import resume_rail_from_landing
                    emu.walk('UP',1);emu.walk('LEFT',1);resume_rail_from_landing(emu)
                    assert emu.location()[:2]==(43,10) and emu.var(BOOKING)==0
        if case.startswith('ferry-'):
            from test_ferry import sail, resume_rail_from_landing
            if case=='ferry-booking':
                resume_rail_from_landing(emu)
                assert emu.location()[:2]==(43,10) and emu.var(BOOKING)==0
            else:
                sail(emu,12 if expected_location[1]==0 else 0)
        if case.startswith("rail-"):
            if case == "rail-paused-outside":
                emu.walk("UP", 1)
                emu.frames(180)
                emu.walk("UP", 1)
            finish_saved_journey(emu)
            assert emu.location()[:2] == (43, (expected_booking - 1) * 4 + 2)
            assert emu.var(BOOKING) == 0
        print(f"PASS: {case}: Save -> cold boot -> Continue preserves city, coordinates, home country, party, and rail booking", flush=True)
    finally:
        emu.close()
