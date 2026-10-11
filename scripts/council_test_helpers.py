"""Council native-input helpers. No progression, stats or party injection."""
import json,shutil
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_tour import travel,item_count
from test_country import wait_menu
from test_time import preserved
from key_item_test_helpers import reload
MAPS=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
HALL=MAPS.index('EuropeCouncilHall');READING=MAPS.index('EuropeLondonReadingRoom')
STAGE=0x40cd;TITLE=0x40ce

def history(e):return tuple(e.var(v) for v in range(0x40c0,0x4100) if v not in (STAGE,TITLE))
def council(e):return e.var(STAGE),e.var(TITLE)
def baseline(e,country):
 name='council-input-'+country;shutil.copy2(ROOT/f'artifacts/releases/v3.2-evidence/release-{country}-all-accounts.sav',ROOT/f'test-output/{name}.sav');load_checkpoint(e,name,True)
 assert e.var(0x40cc)==1 and council(e)==(0,0)
def answer(e,key='YES'):
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
 if key=='NO':e.press('DOWN',60);e.press('A',180)
 elif key=='B':e.press('B',180)
 else:e.press('A',180)
def npc(e,p):go(e,p);e.press('UP',60);e.press('A',180)
def enter(e):
 if e.location()[1]!=0:go(e,(16,14));travel(e,0)
 talk(e,(55,33),choice='YES');assert e.location()==(43,READING,5,7)
 npc(e,(5,4));answer(e);e.finish_dialogue();assert e.location()==(43,HALL,5,7)
def exit_hall(e):
 go(e,(5,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,READING,5,7)
def nurse(e):
 before=preserved(e);h=history(e);s=council(e);npc(e,(2,7));e.finish_dialogue()
 assert history(e)==h and council(e)==s and preserved(e)[1:]==before[1:]
 for i in range(e.read('gPlayerPartyCount',1)):
  p=e.symbols['gPlayerParty']+100*i;assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0

def begin(e,p,trainer):
 npc(e,p);answer(e)
 for _ in range(35):
  if e.in_battle():break
  e.press('A',90)
 assert e.in_battle(),('no battle',e.location(),council(e));e.frames(300);assert e.read('gTrainerBattleOpponent_A',2)==trainer

def battle(e,lose=False,trace=False,limit=2600):
 """Choose real moves and ordinary Potion use; optionally waste turns for defeat."""
 action=next(int(line.split()[0],16) for line in (ROOT/'pokefirered.sym').read_text().splitlines() if line.split()[-1:]==['HandleInputChooseAction'])
 waitmon=next(int(line.split()[0],16) for line in (ROOT/'pokefirered.sym').read_text().splitlines() if line.split()[-1:]==['WaitForMonSelection'])
 mon=e.symbols['gBattleMons'];movefn=e.symbols['HandleInputChooseMove'];damage=[33,10,22,75,71,145,55,189,84,98,44,16,17,2,85,352]
 for turn in range(limit):
  if not e.in_battle():break
  instr=e.read('gBattlescriptCurrInstr');opcode=e.read(instr,1)
  # Use real No/Yes choices to retain damaging moves when offered status moves.
  learning=e.read('gMoveToLearn',2)
  if learning<355 and e.read(e.symbols['gBattleMoves']+12*learning+1,1)==0:
   if opcode==0x5a:e.press('B',30);continue
   if opcode==0x5b:e.press('A',30);continue
  fn=e.read('gBattlerControllerFuncs')&~1
  if trace and turn%40==0:
   names=[n for n,a in e.symbols.items() if a==fn]
   tasks=[t for t in ('Task_BagMenu_HandleInput','Task_HandleChooseMonInput','Task_HandleSelectionMenuInput','Task_PartyMenuPrintRun') if t in e.symbols and e.task_active(t)]
   print('TRACE',turn,names,[(e.read(mon+88*i,2),e.read(mon+88*i+0x28,2)) for i in (0,1)],'active',e.read('gBattlerPartyIndexes',2),'menu',e.read(e.symbols['gPartyMenu']+9,1),'tasks',tasks,'script',hex(instr),hex(opcode),'controllers',[hex(e.read(e.symbols['gBattlerControllerFuncs']+4*i)) for i in (0,1)],'exec',hex(e.read('gBattleControllerExecFlags')),'comm',[e.read(e.symbols['gBattleCommunication']+i,1) for i in (0,1)],flush=True)
   e.screenshot(ROOT/'test-output/council-diagnostic.png')
  if fn==waitmon and e.task_active('Task_HandleChooseMonInput'):
   count=e.read('gPlayerPartyCount',1);living=[i for i in range(count) if e.read(e.symbols['gPlayerParty']+100*i+86,2)]
   assert living,'no living party member'
   current=e.read('gBattlerPartyIndexes',2)
   if battle_ui_index(e,current) in living:
    # Cancel the optional trainer switch prompt entered by generic A presses.
    e.press('B',180);e.frames(180);continue
   select_party(e,living[0],ui=True);e.press('A',180);e.press('A',180);e.frames(300);continue
  if fn==action:
   e.press('UP',2);e.press('LEFT',2)
   if not lose and e.read('gPlayerPartyCount',1)>1:
    from test_country import party_species
    types=[e.read(mon+0x21+j,1) for j in range(2)];enemytypes=[e.read(mon+88+0x21+j,1) for j in range(2)]
    current=e.read('gBattlerPartyIndexes',2);target=None
    if (12 in enemytypes or 6 in enemytypes) and (12 in types or 4 in types):
     target=next((i for i in range(e.read('gPlayerPartyCount',1)) if party_species(e,index=i)==17 and e.read(e.symbols['gPlayerParty']+100*i+86,2)),None)
    elif 13 in enemytypes and 2 in types:
     target=next((i for i in range(e.read('gPlayerPartyCount',1)) if party_species(e,index=i)!=17 and e.read(e.symbols['gPlayerParty']+100*i+86,2)),None)
    if target is not None and target!=current:
     e.press('DOWN',60);e.press('A',180)
     from test_navigation import wait_task
     wait_task(e,'Task_HandleChooseMonInput');select_party(e,target);e.press('A',180);e.press('A',180);e.frames(300);continue
   if not lose and e.read(mon+0x28,2)<=e.read(mon+0x2c,2)//2+3 and (item_count(e,22) or item_count(e,13)):
    e.press('RIGHT',2);e.press('A',180)
    from test_navigation import wait_task
    wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
    for _ in range(5):
     if e.read(bag+6,2)==0:break
     e.press('LEFT',90)
    base=e.read('gSaveBlock1Ptr');item=22 if item_count(e,22) else 13;target=next(i for i in range(42) if e.read(base+0x310+i*4,2)==item)
    for _ in range(45):
     current=e.read(bag+8,2)+e.read(bag+14,2)
     if current==target:break
     e.press('DOWN' if current<target else 'UP',10)
    assert current==target;e.press('A',90);e.press('A',180)
    if e.task_active('Task_HandleChooseMonInput'):select_party(e,e.read('gBattlerPartyIndexes',2))
    e.press('A',180);continue
  elif fn==movefn:
   moves=[e.read(mon+0xc+2*i,2) for i in range(4)];pp=[e.read(mon+0x24+i,1) for i in range(4)]
   enemy_types=[e.read(mon+88+0x21+i,1) for i in range(2)]
   # Seed is helpful in extended Council matches; never try it twice.
   priority=([73] if not e.read(e.symbols['gStatuses3']+4)&4 and 12 not in enemy_types else [])+[189,75,22,55,71,44,98,33,10]
   if lose:
    assert 45 in moves and pp[moves.index(45)],('Growl unavailable for genuine loss',moves,pp)
    slot=moves.index(45)
   else:
    chart={};a=e.symbols['gTypeEffectiveness']
    for j in range(0,0x150,3):
     atk,defend,mult=(e.read(a+j+k,1) for k in range(3))
     if atk>=254:break
     chart[atk,defend]=mult/10
    own_types=[e.read(mon+0x21+i,1) for i in range(2)]
    def score(i):
     if not pp[i]:return -1
     data=e.symbols['gBattleMoves']+12*moves[i];power=e.read(data+1,1);typ=e.read(data+2,1)
     attack=e.read(mon+(8 if typ>=10 else 2),2);defense=e.read(mon+88+(10 if typ>=10 else 4),2)
     value=power*attack/max(1,defense)*(1.5 if typ in own_types else 1)
     for target_type in set(enemy_types):value*=chart.get((typ,target_type),1)
     return value
    if 73 in moves and pp[moves.index(73)] and not e.read(e.symbols['gStatuses3']+4)&4 and 12 not in enemy_types:slot=moves.index(73)
    else:slot=max(range(4),key=score)
   e.press('UP',2);e.press('LEFT',2)
   if slot&1:e.press('RIGHT',2)
   if slot&2:e.press('DOWN',2)
  e.press('A',30)
 else:raise AssertionError(('battle stuck',e.location(),council(e),hex(e.read('gBattlerControllerFuncs')),e.read('gBattleOutcome',1)))
 e.frames(180);e.finish_dialogue();e.frames(300)

def practice(e,target=25):
 count=0;h=history(e);state=council(e)
 while e.read(e.symbols['gPlayerParty']+84,1)<target:
  begin(e,(6,7),758);battle(e);assert e.location()[:2]==(43,HALL),'practice blackout'
  assert history(e)==h and council(e)==state;count+=1;assert count<55
  print('Practice',count,'level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
  if count%5==0:e=reload(e,'council-training-'+str(e.var(0x40f0)))
 return e

def stock(e,quantity=12):
 from test_shops import confirm_purchase
 from test_trainers import money
 npc(e,(4,7));wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
 before=preserved(e);cash=money(e);count=item_count(e,22)
 assert cash>=700*quantity,(cash,quantity)
 confirm_purchase(e,1);e.press('B',90);wait_menu(e,'Task_BuyMenu');assert preserved(e)==before
 confirm_purchase(e,quantity);e.press('A',180);wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
 assert money(e)==cash-700*quantity and item_count(e,22)==count+quantity
 e.press('A',90);e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
 assert not e.read('sLockFieldControls',1)

def battle_ui_index(e,target):
 # Native party screens put the active battler first, then restore stored order.
 for i in range(6):
  value=e.read(e.symbols['gBattlePartyCurrentOrder']+i//2,1)
  original=(value&15) if i&1 else value>>4
  if original==target:return i
 raise AssertionError(('battle party order',target))

def select_party(e,target,ui=False):
 if e.in_battle() and not ui:target=battle_ui_index(e,target)
 for _ in range(8):
  slot=e.read(e.symbols['gPartyMenu']+9,1)
  if slot==target:return
  if target==0:e.press('LEFT',60)
  elif slot==0:e.press('RIGHT',60)
  else:e.press('DOWN' if slot<target else 'UP',60)
 raise AssertionError(('party cursor',slot,target))
