"""Native weather evolution with real World Gear settings and isolated mon fixtures.
Thunderstorm/downpour/fog use explicit saved-overworld-weather fixtures in the bag.
"""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture, candy, ids
from test_shadow_runtime import monfield
from test_continent_runtime import world, menu_row
from test_gym_ui import open_key_item, start_action
from test_navigation import wait_task
from tm_teaching_test_helpers import field

def setting(e, value):
    open_key_item(e,363);wait_task(e,'Task_EuropeMap');menu_row(e,11)
    for _ in range(4):
        if e.var(0x40d0)==value:break
        e.press('RIGHT',60)
    assert e.var(0x40d0)==value
    field(e);e.frames(600)
    assert e.read(e.read('gSaveBlock1Ptr')+0x2e,1)=={1:2,2:3,3:4}[value]

def weather_candy(e,kind):
    # The bag pauses field-environment updates. This represents a saved map's
    # weather and deliberately leaves battle weather unrelated to evolution.
    start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput')
    bag=e.symbols['gBagMenuState']
    for _ in range(5):
        if e.read(bag+6,2)==0:break
        e.press('LEFT',90)
    for _ in range(45):
        if e.read(bag+8,2)+e.read(bag+14,2)==0:break
        e.press('UP',30)
    e.write(e.read('gSaveBlock1Ptr')+0x2e,kind,1)
    for _ in range(3):e.press('A',180)
    for _ in range(90):e.press('A',90)

cases=[('rain',2,49,0,0,None,True),('clear',1,49,0,0,None,False),
 ('snow',3,49,0,0,None,False),('below level',2,48,0,0,None,False),
 ('Everstone',2,49,195,0,None,False),('shadow',2,49,0,1,None,False),
 ('thunderstorm',2,49,0,0,5,True),('downpour',2,49,0,0,13,True),
 ('horizontal fog',1,49,0,0,6,True),('diagonal fog',1,49,0,0,9,True),
 ('battle rain only',1,49,0,0,None,False)]
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
    e.state(ROOT/'test-output/weather-evolution-base.state')
    for n,(name,mode,level,held,shadow,kind,evolves) in enumerate(cases):
        e.state(ROOT/'test-output/weather-evolution-base.state',True)
        setting(e,mode);fixture(e,'SLIGGOO',255,held,shadow)
        e.write(e.symbols['gPlayerParty']+0x54,level,1)
        if n==10:e.write('gBattleWeather',3,2)
        if kind is None:candy(e)
        else:weather_candy(e,kind)
        expected=ids['SPECIES_GOODRA' if evolves else 'SPECIES_SLIGGOO']
        assert monfield(e,0,0,0)&65535==expected,(name,monfield(e,0,0,0)&65535,expected)
        assert e.read(e.symbols['gPlayerParty']+0x54,1)==level+1
        assert (monfield(e,0,0,2)&65535)==held
        print('PASS:',name,'evolves' if evolves else 'stays Sliggoo',flush=True)
        if n==0:
            field(e);start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/'test-output/weather-goodra.sav')
            e.screenshot(ROOT/'test-output/weather-goodra-save.png')
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'weather-goodra',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_GOODRA']
    assert e.var(0x40d0)==2
    sb=e.read('gSaveBlock2Ptr');extra=ids['SPECIES_GOODRA']-440
    for offset in (0xb20,0xb70):assert e.read(sb+offset+extra//8,1)&(1<<(extra%8))
    print('PASS: native Save/cold Continue preserves Goodra, rain setting and seen/caught flags',flush=True)
finally:e.close()
