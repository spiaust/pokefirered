"""Circuit kit capacity/retry rules using explicit TM quantity fixtures."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import talk
from test_eclipse_legendaries import flag
from test_oxford_gym import count_pocket
from test_landmark_cases import save

def quantity(e,item,qty):
 p=e.read('gSaveBlock1Ptr')+0x464;k=e.read(e.read('gSaveBlock2Ptr')+0xF20,2)
 slot=next((i for i in range(58) if e.read(p+4*i,2)==item),None)
 if slot is None:slot=next(i for i in range(58) if not e.read(p+4*i,2))
 e.write(p+4*slot,item,2);e.write(p+4*slot+2,qty^k,2)

def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-league-20-complete',True)
  assert e.var(0x40BF)==0 and not any(flag(e,n) for n in (0x8DE,0x8DF,0x8E0))
  quantity(e,312,999);talk(e,(5,6),'NO')
  assert e.var(0x40BF)==0 and not any(flag(e,n) for n in (0x8DE,0x8DF,0x8E0))
  talk(e,(5,6),'YES')
  assert flag(e,0x8DE) and not flag(e,0x8DF) and not flag(e,0x8E0)
  assert count_pocket(e,341,0x464,58)==1 and count_pocket(e,312,0x464,58)==999 and e.var(0x40BF)==1
  save(e,'circuit-kit-pending-fixture');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'circuit-kit-pending-fixture',True)
  assert flag(e,0x8DE) and not flag(e,0x8DF)
  quantity(e,312,998);talk(e,(5,6))
  assert all(flag(e,n) for n in (0x8DE,0x8DF,0x8E0)) and count_pocket(e,341,0x464,58)==1 and count_pocket(e,312,0x464,58)==999 and count_pocket(e,323,0x464,58)==1
  talk(e,(5,6));assert count_pocket(e,312,0x464,58)==999 and count_pocket(e,323,0x464,58)==1
  print('PASS: native training kit partial gift, capacity failure, cold pending retry and unique awards.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
