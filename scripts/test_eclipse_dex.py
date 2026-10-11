"""Native Dex navigation with explicit complete-Dex flags for UI boundary QA."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_navigation import wait_task

def data(e):return e.read('sPokedexScreenData')
def fixture_flags(e):
    sb1=e.read('gSaveBlock1Ptr');sb2=e.read('gSaveBlock2Ptr')
    for i in range(49):
        for p in (sb2+0x28,sb2+0x5c,sb1+0x5f8,sb1+0x3a18):e.write(p+i,255,1)
    for i in range(80):
        e.write(sb2+0xb20+i,255,1);e.write(sb2+0xb70+i,255,1)

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-league-20-complete',True)
    fixture_flags(e)
    start_action(e,0);e.frames(180)
    e.screenshot(ROOT/'test-output/dex-expanded-menu.png')
    e.press('A',180);wait_task(e,'Task_DexScreen_NumericalOrder')
    e.press('A',180);wait_task(e,'Task_DexScreen_ShowMonPage')
    p=data(e);assert e.read(p+90,2)==1
    e.screenshot(ROOT/'test-output/dex-info.png')
    for mode in range(1,4):
        e.press('SELECT',60);assert e.read(p+92,1)==mode
        e.screenshot(ROOT/f'test-output/dex-tab-{mode}.png')
        e.press('RIGHT',60)
        page=e.read(p+93,1)
        e.press('LEFT',60);assert e.read(p+93,1)==0
        for _ in range(20):e.press('RIGHT',4)
        assert e.read(p+93,1)<16
        for _ in range(20):e.press('LEFT',4)
        assert e.read(p+93,1)==0
    e.press('SELECT',60);assert e.read(p+92,1)==0
    e.press('A',120);e.press('B',120)
    assert e.read(p+92,1)==0
    e.press('B',120);wait_task(e,'Task_DexScreen_NumericalOrder')
    e.press('B',120);wait_task(e,'Task_PokedexScreen')
    e.press('DOWN',60);e.press('A',180);wait_task(e,'Task_DexScreen_NumericalOrder')
    # Native National list supports all 1025 entries, including four-digit numbers.
    e.frames(180);p=data(e);print('National count / mode',e.read(p+72,2),e.read(p+66,1),flush=True);assert e.read(p+72,2)==1025
    e.frames(180)
    e.frames(12000,'DOWN');e.frames(180)
    e.press('A',180);wait_task(e,'Task_DexScreen_ShowMonPage')
    assert e.read(p+90,2)==1078,e.read(p+90,2)
    e.screenshot(ROOT/'test-output/dex-pecharunt-info.png')
    e.press('SELECT',60);assert e.read(p+92,1)==1
    e.screenshot(ROOT/'test-output/dex-pecharunt-levels.png')
    print('PASS: native Dex tabs/pages, area/back, 1025-entry National list and Pecharunt sprites/moves')
finally:e.close()
