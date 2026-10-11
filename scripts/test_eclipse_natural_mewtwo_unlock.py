"""Unlock Mewtwo with six earned rescues and native PC deposits."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_country import wait_menu
from test_navigation import wait_task
from test_landmark_cases import save
from natural_capture_test_helpers import boxed

def deposit(e,species):
 count=e.read('gPlayerPartyCount',1);before=boxed(e).count(species)
 index=next(i for i in range(count) if monfield(e,i,0,0)&65535==species)
 natural.natural_go(e,(3,6));e.press('UP');e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A',180)
 wait_task(e,'Task_PCMainMenu');e.frames(90);e.press('DOWN',15);e.press('A',240)
 wait_task(e,'Task_PokeStorageMain');e.frames(120)
 for _ in range(index):e.press('DOWN',30)
 assert e.read('sCursorPosition',1)==index
 e.press('A',90);e.press('A',120);e.press('A',240);e.frames(180)
 for _ in range(16):
  if e.task_active('Task_PCMainMenu'):break
  e.press('B',120);e.press('A',120)
 wait_task(e,'Task_PCMainMenu');e.press('B',180);e.finish_dialogue();e.frames(180)
 assert e.read('gPlayerPartyCount',1)==count-1 and boxed(e).count(species)==before+1
 print('PASS: native PC deposit',species,flush=True)

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-prepared-timer-legendaries',True)
  assert e.var(0x408F)==3 and e.var(0x408C)==21
  deposit(e,159)
  for chapter in range(19,7,-1):
   talk(e,(2,7));assert e.location()[:2]==(44,chapter*2)
  for chapter,species,to_box in ((8,133,17),(12,179,133),(14,147,179)):
   while e.location()[1]<chapter*2:talk(e,(10,4))
   before=e.var(0x408F);talk(e,(8,4))
   assert e.read('gPlayerPartyCount',1)==6 and any(monfield(e,i,0,0)&65535==species for i in range(6))
   for _ in range(20):
    if e.var(0x408F)>before:break
    talk(e,(4,4))
   assert e.var(0x408F)==before+1
   print('PASS: earned rescue and purification',species,'total',e.var(0x408F),flush=True)
   if chapter!=14:deposit(e,to_box)
  assert e.var(0x408E)==63 and e.var(0x408F)==6
  talk(e,(2,4));save(e,'natural-mewtwo-unlocked')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-mewtwo-unlocked',True)
  assert e.var(0x408E)==63 and e.var(0x408F)==6 and e.var(0x408C)==21 and e.read('gPlayerPartyCount',1)==6
  assert {monfield(e,i,0,0)&65535 for i in range(6)}=={31,26,229,131,179,147}
  assert all(not monfield(e,i,3,8)&(1<<27) for i in range(6))
  assert all(boxed(e).count(species)==1 for species in (159,17,133))
  print('PASS: six-purification Mewtwo unlock persists after cold Continue.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
