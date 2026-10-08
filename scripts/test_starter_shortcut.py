"""Read the new starter-help page and follow it from each fresh country."""
from emulator import Emulator,ROOT
from test_country import start_new_game,wait_menu,party_species
from test_time import preserved
from key_item_test_helpers import toggle_registration,registered,reload
from test_oxford_gym import count_pocket

e=Emulator(ROOT/'pokefirered.gba')
try:
    start_new_game(e)
    for choice,city,species in [(0,'England',1),(1,'France',152),(2,'Germany',277)]:
        e.state(ROOT/'test-output/country-menu.state',True)
        for _ in range(choice):e.press('DOWN')
        e.press('A',180);wait_menu(e,'Task_MultichoiceMenu_HandleInput')
        e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput')
        e.press('A',900)
        e.press('A',900);e.press('A',900)
        e.screenshot(ROOT/f'test-output/starter-shortcut-{city}.png')
        e.finish_dialogue()
        assert e.location()==(43,choice*4,15,14) and party_species(e)==species
        assert e.read('gPlayerPartyCount',1)==1 and e.read(e.symbols['gPlayerParty']+84,1)==8
        assert count_pocket(e,4,0x430,13)==10 and count_pocket(e,13,0x310,42)==5
        assert count_pocket(e,360,0x3B8,30)==1 and count_pocket(e,361,0x3B8,30)==1
        before=preserved(e);toggle_registration(e,360)
        assert registered(e)==360 and preserved(e)==before
        e.press('SELECT',180);assert e.read('gPlayerAvatar',1)&2
        e=reload(e,'starter-shortcut-'+city)
        assert registered(e)==360 and e.read('gPlayerAvatar',1)&2
        e.press('SELECT',180);assert not e.read('gPlayerAvatar',1)&2
        assert preserved(e)==before and e.var(0x40F0)==choice+1 and e.var(0x40F6)==species
        print('PASS: '+city+' fresh starter help, exact supplies, normal REGISTER/SELECT and riding cold Continue retain correct starter and country',flush=True)
finally:e.close()
