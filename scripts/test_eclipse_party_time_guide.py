"""Native optional researcher dialogue, decline, saved partners and boot compatibility."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world
from test_shadow_runtime import go,monfield
from test_country import wait_menu
from test_eclipse_reminder import bag,money
from tm_teaching_test_helpers import field
from test_eclipse_friendship import ids
for accept in (False,True):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
        party=[monfield(e,i,0,0) for i in range(6)];before=bag(e);cash=money(e)
        go(e,(11,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A' if accept else 'B',180)
        if accept:
            e.screenshot(ROOT/'test-output/party-time-researcher.png')
            for _ in range(60):
                if not e.read('sLockFieldControls',1):break
                e.press('A',90)
            else:raise AssertionError('Researcher did not finish dialogue')
        field(e)
        assert party==[monfield(e,i,0,0) for i in range(6)] and bag(e)==before and money(e)==cash
        print('PASS: native researcher','tips' if accept else 'decline','preserves party/items/money and returns field control',flush=True)
    finally:e.close()
for checkpoint,species in [('party-pangoro','PANGORO'),('time-solgaleo','SOLGALEO'),('time-lunala','LUNALA')]:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,checkpoint,True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+species]
        print('PASS: final build cold-continues',species,flush=True)
    finally:e.close()
