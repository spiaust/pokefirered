"""Train an earned non-legendary party using repeatable native route battles."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from test_eclipse_circuit import shelter
from test_landmark_cases import save
from natural_team_test_helpers import lead
from tm_teaching_test_helpers import field
from test_eclipse_natural_league import party_record
import json,sys
from natural_preparation_test_helpers import give
from test_oxford_gym import count_pocket
original=natural.natural_battle
def battle(e):return original(e,learn_moves=(58,85,53,56,352),limit=1200,learn_slot=2,trace=True)
natural.natural_battle=battle
test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
e=Emulator(ROOT/'pokefirered.gba');rows=[]
try:
 load_checkpoint(e,next((x.split('=',1)[1] for x in sys.argv if x.startswith('--checkpoint=')),'balance-nonlegendary-natural-circuit-kit-trained'),True)
 field(e);shelter(e,'ShadowChampion');talk(e,(2,4))
 if count_pocket(e,197,0x310,42):give(e,131,197)
 index=next(i for i in range(6) if monfield(e,i,0,0)&65535==131)
 if index:lead(e,index)
 field(e)
 for n in range(100):
  levels={monfield(e,i,0,0)&65535:e.read(e.symbols['gPlayerParty']+100*i+84,1) for i in range(6)}
  if levels[131]>=60 and levels[26]>=60:break
  talk(e,(10,7));battle_start(e,(21,18));result,turns=battle(e)
  row=dict(practice=n+1,outcome=result,turns=turns,levels=levels);rows.append(row);print(row,flush=True)
  if result!=1:
   save(e,'balance-training-loss');raise AssertionError(row)
  talk(e,(15,20));talk(e,(2,4))
  if (n+1)%5==0:
   save(e,'balance-training-progress');field(e)
 else:raise AssertionError('training cap')
 print('Prepared native levels',levels,flush=True)
 save(e,'balance-nonlegendary-trained');record=party_record(e)
 e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'balance-nonlegendary-trained',True)
 assert party_record(e)==record
 (ROOT/'test-output/balance-training.json').write_text(json.dumps(rows,indent=2)+'\n')
 print('PASS: native repeatable training and exact party survive cold Continue.',flush=True)
finally:e.close()
