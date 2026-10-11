"""Native adoption overflow/retry with explicit full-party/storage fixtures."""
import re
from test_eclipse_krakow import *
from test_country import wait_menu
from test_navigation import wait_task


def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'krakow-garden-complete',True)
  n=0x8dc;p=e.read('gSaveBlock1Ptr')+0xee0+n//8;e.write(p,e.read(p,1)&~(1<<(n%8)),1)
  var(e,0x4091,1);var(e,0x4097,e.var(0x4097)|4)
  party=e.symbols['gPlayerParty'];copy=[e.read(party+4*i) for i in range(25)]
  for j in range(6):
   for i,v in enumerate(copy):e.write(party+100*j+4*i,v)
  e.write('gPlayerPartyCount',6,1)
  ready=ROOT/'test-output/krakow-adoption-capacity.state';e.state(ready)
  storage=e.read('gPokemonStoragePtr')+4
  for j in range(420):
   for i,v in enumerate(copy[:20]):e.write(storage+80*j+4*i,v)
  talk(e,(24,25),'YES');assert not flag(e,0x8dc) and e.read('gPlayerPartyCount',1)==6
  e.state(ready,True)
  rows={int(a):tuple(map(int,b)) for a,*b in re.findall(r'SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)',(ROOT/'src/pokemon.c').read_text())}
  def boxed():
   result=[]
   for j in range(420):
    p=storage+80*j;person=e.read(p);key=person^e.read(p+4)
    result.append((e.read(p+32+12*rows[person%24][0])^key)&0xffff)
   return result
  before=boxed().count(133);talk(e,(24,25),'YES');assert flag(e,0x8dc) and e.read('gPlayerPartyCount',1)==6 and boxed().count(133)==before+1
  talk(e,(24,25));assert boxed().count(133)==before+1
  save(e,'krakow-boxed-adoption');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'krakow-boxed-adoption',True);storage=e.read('gPokemonStoragePtr')+4
  assert flag(e,0x8dc) and e.var(0x4091)==1 and boxed().count(133)==before+1
  e.write(e.symbols['gPlayerParty']+86,1,2);talk(e,(12,31));assert e.read(e.symbols['gPlayerParty']+86,2)==e.read(e.symbols['gPlayerParty']+88,2)
  go(e,(30,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
  go(e,(9,31));e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A',180);wait_task(e,'Task_PCMainMenu')
  e.press('DOWN',15);e.press('DOWN',15);e.press('A',240);wait_task(e,'Task_PokeStorageMain');e.frames(120);e.screenshot(ROOT/'test-output/eclipse-krakow-storage.png')
  for _ in range(16):
   if e.task_active('Task_PCMainMenu'):break
   e.press('B',120);e.press('A',120)
  wait_task(e,'Task_PCMainMenu');e.press('B',180);e.finish_dialogue();assert not e.read('sLockFieldControls',1)
  print('PASS: Krakow nurse heals, shop opens, and native Move Pokemon storage returns safely.',flush=True)
  print('PASS: full party/PC leaves adoption pending; native PC overflow, unique adoption and cold persistence work with Nuzlocke enabled.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
