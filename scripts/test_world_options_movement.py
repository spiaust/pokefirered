"""Registered World Options and cycling sprite regression, real Bag controls."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'world-options-custom',True)
    loc=e.location();identity=e.read('gSaveBlock2Ptr')
    who=bytes(e.read(identity+i,1) for i in range(14))
    open_key_item(e,360);e.frames(120)
    assert e.read('gPlayerAvatar',1)&2
    open_key_item(e,363);wait_task(e,'Task_EuropeMap')
    e.press('DOWN');e.press('LEFT');assert e.var(0x40D3)==1
    e.press('B',180);wait_task(e,'Task_BagMenu_HandleInput')
    e.press('A',90);e.press('DOWN');e.press('A',90)
    assert e.read(e.read('gSaveBlock1Ptr')+0x296,2)==363
    e.press('B',180);e.press('B',90)
    assert e.read('gPlayerAvatar',1)&2
    assert e.read(e.symbols['gPlayerAvatar']+7,1)==0
    e.press('SELECT',180);wait_task(e,'Task_EuropeMap')
    assert e.read('sWorldOptions',1)
    e.press('DOWN');e.press('RIGHT');assert e.var(0x40D3)==2
    e.press('START',180)
    assert not e.task_active('Task_EuropeMap') and not e.read('sLockFieldControls',1)
    assert e.read('gPlayerAvatar',1)&2
    assert e.read(e.symbols['gPlayerAvatar']+7,1)==1
    assert e.location()==loc
    assert bytes(e.read(e.read('gSaveBlock2Ptr')+i,1) for i in range(14))==who
    e.screenshot(ROOT/'test-output/world-options-bike.png')
    open_key_item(e,360);e.frames(120)
    assert not e.read('gPlayerAvatar',1)&2
    assert e.read(e.symbols['gPlayerAvatar']+7,1)==1
    e.walk('LEFT',1);e.walk('RIGHT',1);assert e.location()==loc
    print('PASS: real registration, SELECT/START return, cycling avatar continuity, dismount and unchanged identity',flush=True)
finally:e.close()

