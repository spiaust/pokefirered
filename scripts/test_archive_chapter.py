"""Two native routes through the optional archive chapter; no injected progression."""
import json,shutil
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,researcher
from test_landmark_cases import go,talk,save
from test_tour import travel
from test_country import wait_menu
from test_time import preserved
from key_item_test_helpers import reload
from walking_test_helpers import assert_walk_preserved
MAPS=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
ROOMS={3:('EuropeRadcliffeVisitor',(38,10)),4:('EuropeChateauVisitor',(51,11)),5:('EuropePalaceVisitor',(48,9))}

def quest(e):return tuple(e.var(v) for v in range(0x40c8,0x40cc))
def old_history(e):return tuple(e.var(v) for v in range(0x40c0,0x4100) if not 0x40c8<=v<=0x40cc)
def enter(e,dest):
 if e.location()[1]!=dest*4:
  go(e,(16,14));travel(e,dest)
 name,door=ROOMS[dest];go(e,door);talk(e,door,choice='YES')
 assert e.location()==(43,MAPS.index(name),5,7)
 go(e,(6,4))
def npc(e):e.press('UP',60);e.press('A',180)
def answer(e,key='YES'):
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
 if key=='NO':e.press('DOWN',60);e.press('A',180)
 elif key=='B':e.press('B',180)
 else:e.press('A',180)
def leave(e,dest):
 go(e,(5,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,dest*4,*ROOMS[dest][1])
def bag(e):
 base=e.read('gSaveBlock1Ptr');key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2);result={}
 for i in range(0x310,0x5f8,4):
  item=e.read(base+i,2);quantity=e.read(base+i+2,2)^key
  if item:result[item]=result.get(item,0)+quantity
 return result

shutil.copy2(ROOT/'artifacts/releases/v3.0-evidence/release-england-all-accounts.sav',ROOT/'test-output/archive-original-ending.sav')
for order in ((4,5),(5,4)):
 e=Emulator(ROOT/'pokefirered.gba');tag='-'.join(map(str,order))
 try:
  load_checkpoint(e,'archive-original-ending',True)
  assert e.var(0x40d5)==2 and quest(e)==(0,0,0,0)
  assert e.var(0x40cc)==0
  original=preserved(e)[1:];history=old_history(e)
  enter(e,3);before=preserved(e);npc(e);e.finish_dialogue()
  assert quest(e)==(0,0,0,0) and preserved(e)==before
  leave(e,3);go(e,(18,14));researcher(e);e.finish_dialogue();assert e.var(0x40cc)==1
  enter(e,3)
  for refusal in ('NO','B'):
   before=preserved(e);npc(e);answer(e,refusal);e.finish_dialogue()
   assert quest(e)==(0,0,0,0) and preserved(e)==before
  npc(e);answer(e);answer(e,'NO');e.finish_dialogue();assert quest(e)==(1,0,0,0)
  npc(e);answer(e,'B');e.finish_dialogue();assert quest(e)==(1,0,0,0)
  npc(e);answer(e);e.finish_dialogue();assert quest(e)==(1,1,0,0)
  before=preserved(e);npc(e);e.finish_dialogue();assert quest(e)==(1,1,0,0) and preserved(e)==before
  e.screenshot(ROOT/f'test-output/archive-{tag}-oxford.png')
  e=reload(e,'archive-'+tag+'-oxford');assert quest(e)==(1,1,0,0)
  leave(e,3);go(e,(18,14));before=preserved(e);researcher(e);e.finish_dialogue()
  assert quest(e)==(1,1,0,0) and preserved(e)==before
  assert old_history(e)==history and preserved(e)[1:]==original
  print(f'PASS: {tag} main-conclusion gate, offer No/B, question No/B, Oxford note, repeat talk, incomplete Ada and cold Continue',flush=True)
  for dest in order:
   enter(e,dest);before=preserved(e);npc(e);answer(e,'NO');e.finish_dialogue();assert preserved(e)==before
   var=0x40ca if dest==4 else 0x40cb;assert e.var(var)==0
   npc(e);answer(e);e.finish_dialogue();assert e.var(var)==1 and preserved(e)==before
   npc(e);e.finish_dialogue();assert e.var(var)==1 and preserved(e)==before
   e.screenshot(ROOT/f'test-output/archive-{tag}-town-{dest}.png')
   e=reload(e,f'archive-{tag}-town-{dest}');assert e.var(var)==1 and old_history(e)==history
   leave(e,dest)
  assert quest(e)==(1,1,1,1)
  go(e,(16,14));travel(e,3);go(e,(18,14))
  before=preserved(e);items=bag(e);researcher(e);e.frames(900)
  e.screenshot(ROOT/f'test-output/archive-{tag}-ada.png');e.finish_dialogue();assert quest(e)==(2,1,1,1)
  after=bag(e);expected=dict(items);expected[69]=expected.get(69,0)+1;assert after==expected
  assert preserved(e)[0:3]==before[0:3] and preserved(e)[4:]==before[4:]
  assert old_history(e)==history
  e=reload(e,'archive-'+tag+'-complete');assert quest(e)==(2,1,1,1) and bag(e)==expected
  before=preserved(e);researcher(e);e.finish_dialogue();assert preserved(e)==before and bag(e)==expected
  enter(e,3);before=preserved(e);npc(e);e.finish_dialogue();assert preserved(e)==before and quest(e)==(2,1,1,1)
  leave(e,3);go(e,(18,14));save(e,'archive-'+tag+'-final')
  print(f'PASS: {tag} both country notes, saved interior exits, final Celebi chapter, exactly one PP UP, completed replays and cold Continue',flush=True)
 except Exception:
  e.screenshot(ROOT/f'test-output/archive-{tag}-failure.png');raise
 finally:e.close()
