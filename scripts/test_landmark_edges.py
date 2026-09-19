"""Full reward pockets and a real catchable Ghost Pokemon encounter."""
from emulator import Emulator,ROOT
from test_landmark_cases import DATA,go,talk,save
from test_celebi import load_checkpoint
from test_country import wait_menu,party_species
from test_navigation import wait_task
from test_time import preserved
for row,reward,count,offset,slots in zip(DATA,[213,68,3],[1,1,3],[0x310,0x310,0x430],[42,42,13]):
 tag,city,country,index,inside,door,var,selection=row;e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'case-'+tag.lower()+'-clues',True)
  e.write(e.read('gSaveBlock1Ptr')+0x1000+(var-0x4000)*2,1,2)
  talk(e,(4,6));assert e.var(var)==2
  talk(e,(15,8));assert e.var(var)==4
  print(f'PASS: {tag} clues also combine in forward order',flush=True)
  load_checkpoint(e,'case-'+tag.lower()+'-resolved',True);assert e.var(var)==5
  base=e.read('gSaveBlock1Ptr')+offset;key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
  for i in range(slots):e.write(base+4*i,13 if offset==0x310 else 4,2);e.write(base+4*i+2,999^key,2)
  before=preserved(e);talk(e,(8,15));assert e.var(var)==5 and preserved(e)==before
  e.write(base,0,2);e.write(base+2,key,2);talk(e,(8,15));assert e.var(var)==6
  # Inventory must change only once, even if the curator is asked again.
  before=preserved(e);talk(e,(8,15));assert preserved(e)==before
  print(f'PASS: {tag} full reward pocket retains resolved case; freeing space grants one reward',flush=True)
 finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'case-notredame-complete',True);talk(e,(10,5),choice='NO');assert not e.in_battle()
 base=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
 # A Master Ball makes the capture test deterministic; only the test save changes.
 e.write(base+0x430,1,2);e.write(base+0x432,1^key,2)
 e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);e.frames(300)
 e.screenshot(ROOT/'test-output/notredame-gastly-start.png')
 assert e.in_battle() and party_species(e,'gEnemyParty',0)==92,(e.in_battle(),party_species(e,'gEnemyParty',0))
 assert e.read(e.symbols['gEnemyParty']+0x54,1)==12
 e.screenshot(ROOT/'test-output/notredame-gastly-battle.png')
 e.press('A',180);e.press('A',180);e.press('B',180)
 e.press('RIGHT');e.press('A',180);wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
 for _ in range(5):
  if e.read(bag+6,2)==2:break
  e.press('RIGHT',90)
 assert e.read(bag+6,2)==2
 for _ in range(15):
  if e.read(bag+12,2)+e.read(bag+18,2)==0:break
  e.press('UP')
 e.press('A',90);e.press('A',180)
 for _ in range(150):
  if not e.in_battle():break
  e.press('B',90)
 assert not e.in_battle(),'capture did not finish'
 e.frames(180);e.finish_dialogue();assert e.var(0x40c0)==6
 assert e.read('gPlayerPartyCount',1)==2 and party_species(e,'gPlayerParty',1)==92
 save(e,'notredame-gastly-caught')
 print('PASS: optional level-12 Gastly battle allows real capture without changing completed case',flush=True)
finally:e.close()
