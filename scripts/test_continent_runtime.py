"""Native settings, travel, era palettes and country choices. Explicit progress fixtures skip grinding."""
from emulator import Emulator,ROOT
from test_shadow_runtime import go,talk,setstage,monfield
from test_country import wait_menu
from test_navigation import wait_task
from test_gym_ui import open_key_item
from test_landmark_cases import save
from test_celebi import load_checkpoint
import json,sys
DATA=json.loads((ROOT/'data/continent-campaign.json').read_text());D=DATA['countries'];REGIONS=DATA['regions']
def var(e,v,n):e.write(e.read('gSaveBlock1Ptr')+0x1000+2*(v-0x4000),n,2)
def visible(e):
 g,m,_,_=e.location();lid=6 if g==45 else len(json.loads((ROOT/f'data/maps/{("ShadowOxfordRoute" if m==1 else "ShadowParisRoute")}/map.json').read_text())['object_events'])
 return any(e.read(e.symbols['gObjectEvents']+36*i,1)&1 and e.read(e.symbols['gObjectEvents']+36*i+8,1)==lid and e.read(e.symbols['gObjectEvents']+36*i+9,1)==m and e.read(e.symbols['gObjectEvents']+36*i+10,1)==g for i in range(16))
def menu_row(e,row):
 fn=e.symbols['Task_EuropeMap']&~1;t=e.symbols['gTasks'];slot=next(i for i in range(16) if e.read(t+40*i,4)&~1==fn and e.read(t+40*i+4,1));p=t+slot*40+10
 for _ in range(12):
  if e.read(p,2)==row:return
  e.press('DOWN',15)
 raise AssertionError(('settings row',row))
def world(e,country):
 loc=e.location();go(e,(4,7) if loc[0]==44 else (15,29));e.press('UP');e.press('A',180);wait_menu(e,'Task_MultichoiceMenu_HandleInput')
 region=next(k for k,rr in enumerate(REGIONS) if country in rr)
 for _ in range(region):e.press('DOWN')
 e.press('A',180);wait_task(e,'Task_MultichoiceMenu_HandleInput')
 for _ in range(REGIONS[region].index(country)):e.press('DOWN')
 e.press('A',180);e.finish_dialogue();e.frames(240)
 assert e.location()[:2]==(45,country*2),(country,e.location())
def battle_start(e,target):
 go(e,target);e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A',180)
 for _ in range(35):
  if e.in_battle():break
  e.press('A',60)
 assert e.in_battle();e.frames(420)
def accelerated_win(e):
 # Real victory callbacks; fixture damage avoids a long balancing playthrough.
 action=next(int(t.split()[0],16)&~1 for t in (ROOT/'pokefirered.sym').read_text().splitlines() if t.split()[-1:]==['HandleInputChooseAction']);move=e.symbols['HandleInputChooseMove']&~1
 for _ in range(1800):
  if not e.in_battle():break
  b=e.symbols['gBattleMons'];fn=e.read('gBattlerControllerFuncs')&~1
  if fn in (action,move):
   ix=e.read('gBattlerPartyIndexes',1);hp=e.read(e.symbols['gPlayerParty']+100*ix+0x58,2);e.write(b+0x28,hp,2);e.write(b+0x2c,hp,2)
   for off in (4,6,10):e.write(b+off,30000,2)
   e.write(b+88+0x28,1,2);e.write(b+0xc,82,2);e.write(b+0x24,40,1);e.press('UP',2);e.press('LEFT',2)
  e.press('B' if e.read(e.read('gBattlescriptCurrInstr'),1)==0x5a else 'A',30)
 else:raise AssertionError('battle fixture stalled')
 for _ in range(35):e.press('B',45);e.press('A',45)
 e.finish_dialogue();e.frames(180)
def bit(e,base,country):return bool(e.var(base+country//16)&(1<<(country%16)))
def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  e.state(ROOT/'test-output/start-england.state',True);talk(e,(10,16));e.write('sWildEncountersDisabled',1,1)
  assert e.var(0x4090)==0 and e.var(0x4091)==0 and e.var(0x4092)==0
  open_key_item(e,363);wait_task(e,'Task_EuropeMap');menu_row(e,8)
  for val in (1,2,0):e.press('A',60);assert e.var(0x4090)==val
  menu_row(e,9);e.press('A',60);assert e.var(0x4091)==1;e.press('A',60);assert e.var(0x4091)==0
  menu_row(e,10);e.press('A',60);assert e.var(0x4092)==1;e.press('A',60);assert e.var(0x4092)==0
  e.screenshot(ROOT/'test-output/eclipse-gameplay-settings.png')
  for _ in range(3):e.press('B',180)
  setstage(e,12);e.state(ROOT/'test-output/continent-ready.state')
  print('PASS: native World Gear cycles Easy/Hard/Normal and independently toggles Nuzlocke and wild sprites.',flush=True)
  for i,d in enumerate(D):
   world(e,i);e.write('sWildEncountersDisabled',1,1);go(e,(22,13));e.press('UP');e.press('A',180);e.finish_dialogue()
   e.screenshot(ROOT/f'test-output/continent-{i:02}-present.png')
   pal=e.symbols['gPlttBufferUnfaded']+7*32;modern=tuple(e.read(pal+2*j,2) for j in range(16))
   talk(e,(18,31),'YES');assert e.location()[:2]==(45,2*i+1)
   old=tuple(e.read(pal+2*j,2) for j in range(16));assert old!=modern,(i,'historical palette did not change')
   go(e,(22,13));e.screenshot(ROOT/f'test-output/continent-{i:02}-past.png')
   # Inject only the cleared-operation bit here to isolate choice scripts and map mutations.
   var(e,0x40AF+i//16,e.var(0x40AF+i//16)|(1<<(i%16)))
   choice='NO' if i==1 else 'YES';talk(e,(27,29),choice)
   assert bit(e,0x40A5,i) and bit(e,0x40A2,i)==(choice=='YES')
   talk(e,(18,31),'YES');assert e.location()[:2]==(45,2*i)
   restored=tuple(e.read(pal+2*j,2) for j in range(16));assert restored==modern,(i,'modern palette not restored')
   # Read the actual virtual map; saved decisions must modify tiles, rather than only text.
   w=e.read('VMap');grid=e.read(e.symbols['VMap']+8);offset=((15+7)*w+20+7)*2
   assert e.read(grid+offset,2)&1023==(4 if choice=='YES' else 0x165),(i,'timeline tile consequence')
   talk(e,(27,29));print('PASS:',i+1,d['country'],'travel both eras, landmark, palette restoration and saved future choice',flush=True)
  save(e,'continent-choices');before=e.location();e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'continent-choices',True)
  assert e.location()==before and all(bit(e,0x40A5,i) for i in range(39));assert not bit(e,0x40A2,1)
  e.screenshot(ROOT/'test-output/eclipse-country-save.png')
  print('PASS: native Save and cold Continue retain all 39 decisions and the alternate archive outcome.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
