"""Verify the completed campaign's native save on the final compiled ROM."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'eclipse-finished',True)
    assert e.var(0x408C)==21 and e.var(0x408D)==1 and e.location()[:2]==(44,40)
    f=e.read('gSaveBlock1Ptr')+0xEE0
    for flag in list(range(0x820,0x828))+[0x82c]:assert e.read(f+flag//8,1)&(1<<(flag%8)),hex(flag)
    open_key_item(e,361);wait_task(e,'Task_EuropeMap');e.press('SELECT',90)
    e.screenshot(ROOT/'test-output/eclipse-champion-journal.png');e.press('A',90);e.screenshot(ROOT/'test-output/eclipse-completed-records.png')
    print('PASS: final ROM cold Continue retains chapter 21, eight badges, game-clear and completed journal',flush=True)
finally:e.close()
