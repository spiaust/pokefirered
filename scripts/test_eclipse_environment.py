"""Native World Gear, weather sprites, lighting composition and cold-save QA.
Only clock fixtures are written; settings, travel and saving use game inputs.
"""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import menu_row, world, var
from test_gym_ui import open_key_item, start_action
from test_navigation import wait_task
from test_landmark_cases import save
from test_shadow_runtime import go, talk

def options(e):
    open_key_item(e,363);wait_task(e,'Task_EuropeMap')
def close(e):
    for _ in range(3):e.press('B',180)
    assert not e.read('sLockFieldControls',1)
def setting(e,row,ident,value):
    options(e);menu_row(e,row)
    for _ in range(4):
        if e.var(ident)==value:break
        e.press('RIGHT',60)
    assert e.var(ident)==value
    close(e);e.frames(300)
def clock(e,minutes,seconds=0):
    p=e.read('gSaveBlock2Ptr');e.write(p+14,0,2);e.write(p+16,minutes,1);e.write(p+17,seconds,1);e.write(p+18,0,1)
    e.frames(5)
def palettes(e):
    return ([e.read(e.symbols['gPlttBufferFaded']+i*2,2) for i in range(512)],
            [e.read(0x05000000+i*2,2) for i in range(512)])
def tint(c,d=12):
    return ((c&31)*(32-d)//32)|((((c>>5)&31)*(32-d)//32)<<5)|((((c>>10)&31)*(32-d//3)//32)<<10)
def lighting(e,d=12):
    a,b=palettes(e)
    expect=[c if 208<=i<256 else tint(c,d) for i,c in enumerate(a)]
    assert b==expect,[(i,x,y) for i,(x,y) in enumerate(zip(b,expect)) if x!=y][:8]
    assert any(x!=y for x,y in zip(a,b)) if d else a==b
    e.frames(60)
    a,b=palettes(e);assert b==[c if 208<=i<256 else tint(c,d) for i,c in enumerate(a)]
def weather(e,kind):
    e.frames(600)
    p=e.read('gWeatherPtr')
    assert e.read(e.read('gSaveBlock1Ptr')+0x2e,1)==kind
    assert e.read(p+0x6d0,1)==kind,(kind,e.read(p+0x6d0,1))
    if kind==3:assert e.read(p+0x6da,1)>0
    if kind==4:
        assert e.read(p+0x6e4,1)==16
        e.frames(1200)
        assert any(e.read(e.read(p+96+4*i)+0x1c)&~1==e.symbols['UpdateSnowflakeSprite']&~1 for i in range(16)), 'snow must keep respawning'

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-league-20-complete',True)
    setting(e,11,0x40d0,2);setting(e,12,0x40d1,1)
    world(e,0);weather(e,3);lighting(e,0)
    e.screenshot(ROOT/'test-output/environment-rain-day.png')
    setting(e,12,0x40d1,2);lighting(e)
    e.screenshot(ROOT/'test-output/environment-rain-night.png')
    setting(e,11,0x40d0,3);weather(e,4);lighting(e)
    e.screenshot(ROOT/'test-output/environment-snow-night.png')
    start_action(e,4)
    for _ in range(8):e.press('A',240)
    e.battery(ROOT/'test-output/environment-settings.sav')
    e.press('B',180);e.press('B',180);location=e.location()
    print('PASS: native World Gear rain/snow, animated particle counts, day/night tint and stable palettes',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'environment-settings',True)
    assert e.location()==location and e.var(0x40d0)==3 and e.var(0x40d1)==2,(e.location(),location,e.var(0x40d0),e.var(0x40d1))
    weather(e,4);lighting(e)
    setting(e,11,0x40d0,0);setting(e,12,0x40d1,0)
    clock(e,0);weather(e,2);lighting(e,0)
    clock(e,24);weather(e,2);lighting(e)
    clock(e,45);lighting(e,6)
    clock(e,21);lighting(e,6)
    clock(e,23,59);e.frames(180);lighting(e)
    clock(e,11,59);e.frames(180);weather(e,3)
    world(e,16);clock(e,0);weather(e,4)
    e.screenshot(ROOT/'test-output/environment-norway-regional.png')
    talk(e,(18,31),choice='YES');weather(e,4)
    setting(e,12,0x40d1,2);lighting(e)
    e.screenshot(ROOT/'test-output/environment-past-snow-night.png')
    # Return to present, London, and the indoor champion shelter through native travel.
    talk(e,(18,31),choice='YES');world(e,0)
    talk(e,(43,31),choice='YES');talk(e,(10,16),choice='YES')
    assert e.location()[:2]==(44,40),e.location()
    setting(e,11,0x40d0,2);weather(e,0);lighting(e,0)
    e.screenshot(ROOT/'test-output/environment-indoor.png')
    options(e);menu_row(e,13);e.press('A',60);e.press('A',60)
    assert e.var(0x40d0)==0 and e.var(0x40d1)==0
    close(e)
    print('PASS: cold saved settings, clock phases/live boundaries, regional Norway snow, historical palette composition, indoor clear and defaults',flush=True)
finally:e.close()
