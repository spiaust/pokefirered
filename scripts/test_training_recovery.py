"""Heal genuine post-battle teams and verify HP, status, PP and saved victories."""
import re,struct
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_trainers import defeated
from test_time import preserved
from key_item_test_helpers import reload

orders={int(m[1]):tuple(map(int,m.groups()[1:])) for m in re.finditer(r'SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)',(ROOT/'src/pokemon.c').read_text())}
def mon(e,i=0):
 p=e.symbols['gPlayerParty']+100*i;personality=e.read(p);key=personality^e.read(p+4)
 data=[b''.join(struct.pack('<I',e.read(p+32+slot*12+j)^key) for j in (0,4,8)) for slot in orders[personality%24]]
 moves=struct.unpack('<4H',data[1][:8]);pp=tuple(data[1][8:])
 bonuses=data[0][8]
 maximum=tuple(e.read(e.symbols['gBattleMoves']+12*move+4,1)*(5+((bonuses>>(2*n))&3))//5 if move else 0 for n,move in enumerate(moves))
 return {'species':struct.unpack_from('<H',data[0])[0],'hp':e.read(p+86,2),'maxhp':e.read(p+88,2),
  'status':e.read(p+80),'pp':pp,'maximum':maximum,'identity':(e.read(p),e.read(p+4),data[0],data[1][:8],data[2],data[3]),'moves':moves}

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,city in enumerate(['London','Paris','Berlin']):
  load_checkpoint(e,'training-intro-'+city+'-won',True)
  assert e.location()==(43,index*4+1,17,19) and defeated(e,index)
  wounded=mon(e);state=preserved(e)[1:]
  assert wounded['hp']<wounded['maxhp'] and any(p<m for p,m in zip(wounded['pp'],wounded['maximum'])),wounded
  e=reload(e,'training-recovery-'+city+'-worn')
  assert mon(e)==wounded and defeated(e,index)
  print('PASS: '+city+' genuine victory has natural HP damage and spent move PP; cold Continue retains both and trainer defeat',flush=True)
  e.walk('LEFT',2);e.walk('DOWN',5);e.frames(180)
  assert e.location()==(43,index*4,15,0)
  go(e,(6,10));e.walk('UP',1);e.frames(180)
  e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
  healed=mon(e)
  assert healed['hp']==healed['maxhp'] and healed['status']==0 and healed['pp']==healed['maximum'],healed
  assert healed['identity']==wounded['identity'] and defeated(e,index) and preserved(e)[1:]==state
  e.screenshot(ROOT/f'test-output/training-recovery-{city}-clinic.png')
  before=preserved(e);e.press('UP');e.press('A',180);e.finish_dialogue();assert preserved(e)==before
  print('PASS: '+city+' nurse fully restores naturally lost HP and PP for free; species/moves/experience/items/victory remain intact and repeat care is safe',flush=True)
  e=reload(e,'training-recovery-'+city+'-healed');assert mon(e)==healed and defeated(e,index)
  e.walk('DOWN',5);e.frames(180)
  assert e.location()==(43,index*4,6,10) and preserved(e)[1:]==state
  print('PASS: '+city+' healed-state cold Continue and clinic exit retain full recovery and the earned victory',flush=True)
finally:e.close()
