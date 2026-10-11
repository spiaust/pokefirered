"""Catch and train a supporting Pidgey using normal balls and EXP. SHARE."""
import struct
from council_test_helpers import *
from test_country import party_species
from test_tour import guide
from test_oxford_gym import count_pocket
from test_navigation import wait_task
from test_gym_ui import start_action
from battle_recovery_test_helpers import orders

def field(e):
 for _ in range(5):e.press('B',180)
 assert not e.read('sLockFieldControls',1)
def action(e):
 fn=next(int(line.split()[0],16) for line in (ROOT/'pokefirered.sym').read_text().splitlines() if line.split()[-1:]==['HandleInputChooseAction'])
 return e.read('gBattlerControllerFuncs')&~1==fn

def throw(e):
 e.press('UP');e.press('LEFT');e.press('RIGHT');e.press('A',180);wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
 for _ in range(5):
  if e.read(bag+6,2)==2:break
  e.press('RIGHT',90)
 ball=3 if count_pocket(e,3,0x430,13) else 4
 assert count_pocket(e,ball,0x430,13)>0
 base=e.read('gSaveBlock1Ptr')+0x430;target=next(i for i in range(13) if e.read(base+4*i,2)==ball)
 for _ in range(30):
  cursor=e.read(bag+12,2)+e.read(bag+18,2)
  if cursor==target:break
  e.press('DOWN' if cursor<target else 'UP')
 assert cursor==target;e.press('A',90);e.press('A',180)

def held(e,index):
 p=e.symbols['gPlayerParty']+100*index;pid=e.read(p);key=pid^e.read(p+4);slot=orders[pid%24][0]
 return struct.unpack('<I',struct.pack('<I',e.read(p+32+slot*12)^key))[0]>>16

def give_share(e):
 assert item_count(e,182)
 start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
 for _ in range(5):
  if e.read(bag+6,2)==0:break
  e.press('LEFT',90)
 base=e.read('gSaveBlock1Ptr');target=next(i for i in range(42) if e.read(base+0x310+i*4,2)==182)
 for _ in range(45):
  current=e.read(bag+8,2)+e.read(bag+14,2)
  if current==target:break
  e.press('DOWN' if current<target else 'UP')
 assert current==target;e.press('A',90);e.press('DOWN',60);e.press('A',180);wait_task(e,'Task_HandleChooseMonInput');e.press('RIGHT',60);e.press('A',180)
 for _ in range(6):e.press('A',90)
 field(e);assert held(e,1)==182 and not item_count(e,182)

def capture_support(e):
 assert e.location()[:2]==(43,HALL) and e.read('gPlayerPartyCount',1)==1
 stage=council(e);originalmain=tuple(e.var(v) for v in range(0x40c8,0x40ef))
 exit_hall(e);go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 # Three stamps are an existing, optional native reward, not an injected item.
 if not item_count(e,182):
  for dest in (0,1,2):
   if e.location()[1]!=dest*4:go(e,(16,14));travel(e,dest)
   go(e,(16,14));guide(e)
  assert item_count(e,182)
 if e.location()[1]!=0:go(e,(16,14));travel(e,0)
 go(e,(15,1));e.walk('UP',2);assert e.location()[:2]==(43,1)
 e.walk('UP',6);e.walk('LEFT',9);e.walk('UP',2)
 encounters=0;throws=0
 for _ in range(60):
  for _ in range(600):
   if e.in_battle():break
   x=e.location()[2];e.walk('RIGHT' if x<=6 else 'LEFT',1)
  assert e.in_battle();e.frames(300);encounters+=1
  if party_species(e,'gEnemyParty')!=16:
   for _ in range(150):
    if not e.in_battle():break
    if action(e):e.press('DOWN');e.press('RIGHT');e.press('A',90)
    else:e.press('B',60)
   assert not e.in_battle();e.frames(180);continue
  for _ in range(1800):
   if not e.in_battle() and e.read('gPlayerPartyCount',1)==2:break
   if e.in_battle() and action(e):throw(e);throws+=1
   else:e.press('B',60)
  assert e.read('gPlayerPartyCount',1)==2 and not e.in_battle();break
 assert party_species(e,index=1)==16;e.frames(180);e.finish_dialogue()
 # Follow the paved central lane back without manipulating encounter state.
 while e.location()[2]<15:
  e.frames(8,'RIGHT')
  if e.in_battle():
   for _ in range(150):
    if not e.in_battle():break
    if action(e):e.press('DOWN');e.press('RIGHT');e.press('A',90)
    else:e.press('B',60)
   assert not e.in_battle();e.frames(180)
 e.walk('DOWN',23-e.location()[3]);e.walk('DOWN',1);e.frames(180);assert e.location()[:2]==(43,0)
 give_share(e);enter(e);assert council(e)==stage
 assert tuple(e.var(v) for v in range(0x40c8,0x40ef))==originalmain
 print('PASS: native stamp reward, '+str(encounters)+' wild encounters and '+str(throws)+' real ball throws earn Pidgey and give it EXP. SHARE; main/archive/Council progress stays intact',flush=True)
 return e

def train_support(e,country,target=22):
 h=history(e);state=council(e);count=0
 while e.read(e.symbols['gPlayerParty']+100+84,1)<target:
  begin(e,(6,7),758);battle(e);assert e.location()[:2]==(43,HALL)
  assert history(e)==h and council(e)==state;count+=1;assert count<50
  print('Support practice',country,count,'levels',e.read(e.symbols['gPlayerParty']+84,1),e.read(e.symbols['gPlayerParty']+184,1),flush=True)
  if count%5==0:e=reload(e,'council-'+country+'-support-training')
 assert party_species(e,index=1)==17
 e=reload(e,'council-'+country+'-support-prepared')
 print('PASS: naturally shared practice XP evolves and trains Pidgeotto, restores both partners, and saves with the Council stage retained',flush=True)
 return e

def swap_lead(e):
 before=(party_species(e),party_species(e,index=1));start_action(e,1);wait_task(e,'Task_HandleChooseMonInput');e.frames(60)
 e.press('RIGHT',60);e.press('A',180);e.press('DOWN',60);e.press('A',180);e.press('LEFT',60);e.press('A',180);field(e)
 assert (party_species(e),party_species(e,index=1))==before[::-1]
