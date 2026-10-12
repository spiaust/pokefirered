"""Native Drain Punch level lessons, free reminder and Dex display."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture,candy,ids
from test_eclipse_move_evolution import moves_fixture,moves
from test_shadow_runtime import monfield
from test_eclipse_reminder import lesson,bag,money
from test_continent_runtime import world
from test_gym_ui import start_action
from test_navigation import wait_task
from tm_teaching_test_helpers import field
for species,level in [('MIENFOO',34),('KORAIDON',20)]:
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,species,255,0,0);moves_fixture(e,'MOVE_TACKLE')
        e.write(e.symbols['gPlayerParty']+0x54,level,1);candy(e);field(e)
        assert moves['MOVE_DRAIN_PUNCH'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+species]
        print('PASS: native Drain Punch level lesson',species,level+1,flush=True)
    finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0);fixture(e,'SEISMITOAD',255,0,0);moves_fixture(e,'MOVE_TACKLE')
    before=bag(e);cash=money(e);lesson(e,'MOVE_DRAIN_PUNCH')
    assert bag(e)==before and money(e)==cash
    print('PASS: native free Seismitoad Drain Punch recall',flush=True)
finally:e.close()
# Complete-Dex flag fixture, but all navigation and page rendering use native UI.
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True)
    sb1=e.read('gSaveBlock1Ptr');sb2=e.read('gSaveBlock2Ptr')
    for i in range(49):
        for p in (sb2+0x28,sb2+0x5c,sb1+0x5f8,sb1+0x3a18):e.write(p+i,255,1)
    for i in range(80):e.write(sb2+0xb20+i,255,1);e.write(sb2+0xb70+i,255,1)
    start_action(e,0);e.press('DOWN',60);e.press('A',180);wait_task(e,'Task_DexScreen_NumericalOrder')
    p=e.read('sPokedexScreenData');assert e.read(p+72,2)==1025
    task=e.read(p+65,1);listdata=e.symbols['gTasks']+40*task+8
    for _ in range(10000):
        index=e.read(listdata+24,2)+e.read(listdata+26,2)
        if index==618:break
        assert index<618,index
        e.frames(1,'DOWN')
    else:raise AssertionError('Could not reach native Mienfoo Dex row')
    e.frames(30);e.press('A',180);wait_task(e,'Task_DexScreen_ShowMonPage')
    assert e.read(p+90,2)==ids['SPECIES_MIENFOO']
    e.press('SELECT',60);assert e.read(p+92,1)==1
    row=next(r for r in json.loads((ROOT/'data/eclipse-roster.json').read_text())['species'] if r['token']=='SPECIES_MIENFOO')
    page=next(i for i,(_,m) in enumerate(row['moves']) if m=='MOVE_DRAIN_PUNCH')//4
    for _ in range(page):e.press('RIGHT',60)
    assert e.read(p+93,1)==page
    e.screenshot(ROOT/'test-output/dex-mienfoo-drain-punch.png')
    print('PASS: native National Dex navigation renders Mienfoo new level-up lesson',flush=True)
finally:e.close()
