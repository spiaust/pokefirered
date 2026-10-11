"""Eight leader rewards, duplicates, cold persistence and explicit full-stack fixtures."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import talk
from test_oxford_gym import count_pocket
from test_landmark_cases import save
import json
C=json.loads((ROOT/'data/shadow-campaign.json').read_text())['chapters']
def flag(e,n):return bool(e.read(e.read('gSaveBlock1Ptr')+0xee0+n//8,1)&(1<<(n%8)))
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'eclipse-finished',True)
 collected=[]
 for stage in range(20,0,-1):
  assert e.location()[:2]==(44,stage*2)
  c=C[stage]
  if c['kind']=='gym':
   tm=288+c['tm_reward'];f=int(c['tm_reward_flag'],16);before=count_pocket(e,tm,0x464,58)
   assert not flag(e,f);talk(e,(6,4));assert flag(e,f) and count_pocket(e,tm,0x464,58)==before+1
   talk(e,(6,4));assert count_pocket(e,tm,0x464,58)==before+1
   collected.append((tm,f,before+1));print('PASS:',c['city'],'themed TM and duplicate protection',flush=True)
  if stage>1:talk(e,(2,7))
 assert len(collected)==8 and count_pocket(e,364,0x3b8,30)==1
 save(e,'eclipse-eight-tms');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'eclipse-eight-tms',True)
 for tm,f,count in collected:assert flag(e,f) and count_pocket(e,tm,0x464,58)==count
 print('PASS: all eight claimed reward flags, TMs and TM Case survive cold Continue.',flush=True)
 e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-first-badge',True)
 f=0x8c6;p=e.read('gSaveBlock1Ptr')+0x464;key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
 e.write(p,327,2);e.write(p+2,999^key,2) # isolate native capacity failure
 talk(e,(6,4));assert not flag(e,f) and count_pocket(e,327,0x464,58)==999
 e.write(p+2,998^key,2);talk(e,(6,4));assert flag(e,f) and count_pocket(e,327,0x464,58)==999
 talk(e,(6,4));assert count_pocket(e,327,0x464,58)==999
 print('PASS: full TM stack keeps reward unclaimed; making space permits exactly one retry reward.',flush=True)
finally:e.close()
