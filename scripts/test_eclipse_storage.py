"""Native storage access at shelters and in both country eras, using cold saves."""
from emulator import Emulator,ROOT
from test_shadow_runtime import talk,go,monfield
from test_continent_runtime import world
from test_country import wait_menu
from test_navigation import wait_task
from test_celebi import load_checkpoint

def open_storage(e,target,label):
 go(e,target);e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A',180)
 wait_task(e,'Task_PCMainMenu');e.frames(90)
 count=e.read('gPlayerPartyCount',1);species=monfield(e,0,0,0)&0xffff
 e.press('DOWN',15);e.press('DOWN',15);e.press('A',240)
 wait_task(e,'Task_PokeStorageMain');e.frames(120)
 e.screenshot(ROOT/f'test-output/eclipse-storage-{label}.png')
 for _ in range(16):
  if e.task_active('Task_PCMainMenu'):break
  e.press('B',120);e.press('A',120)
 wait_task(e,'Task_PCMainMenu');e.press('B',180);e.finish_dialogue();e.frames(180)
 assert not e.read('sLockFieldControls',1)
 assert e.read('gPlayerPartyCount',1)==count and monfield(e,0,0,0)&0xffff==species
 print('PASS: native Move Pokemon storage opens and returns safely at',label,flush=True)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'eclipse-purified',True)
 talk(e,(10,7));talk(e,(15,20)) # refresh saved object templates for this build
 talk(e,(3,6),'NO');assert not e.task_active('Task_PCMainMenu')
 open_storage(e,(3,6),'shelter')
 e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'eclipse-finished',True)
 world(e,0);open_storage(e,(9,31),'present')
 talk(e,(18,31),'YES');assert e.location()[:2]==(45,1)
 open_storage(e,(9,31),'past')
finally:e.close()
