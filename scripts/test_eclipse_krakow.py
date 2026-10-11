"""Native restoration, timeline branches, consumption and persistence.
Progress, country memory and bag fixtures isolate quest rules, not campaign balance.
"""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import talk,go,monfield,setstage
from test_continent_runtime import world,var
from test_eclipse_legendaries import flag
from test_landmark_cases import save
from test_oxford_gym import count_pocket


def count(e,item):return count_pocket(e,item,0x310,42)
def supply(e,item,qty):
 p=e.read('gSaveBlock1Ptr')+0x310;k=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
 matches=[i for i in range(42) if e.read(p+4*i,2)==item]
 slot=matches[0] if matches else next(i for i in range(42) if e.read(p+4*i,2)==0)
 for i in matches[1:]:e.write(p+4*i,0,2);e.write(p+4*i+2,k,2)
 e.write(p+4*slot,item,2);e.write(p+4*slot+2,qty^k,2)
def tile(e,x,y):return e.read(e.read(e.symbols['VMap']+8)+2*((y+7)*e.read('VMap')+x+7),2)&1023
def actor(e,local):
 return any(e.read(e.symbols['gObjectEvents']+36*i,1)&1 and e.read(e.symbols['gObjectEvents']+36*i+8,1)==local and e.read(e.symbols['gObjectEvents']+36*i+10,1)==46 for i in range(16))


def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-nordic-complete',True);e.write('sWildEncountersDisabled',1,1)
  world(e,13);setstage(e,20);talk(e,(34,13));assert e.location()[:2]==(45,26)
  setstage(e,21);talk(e,(34,13),'NO');assert e.location()[:2]==(45,26)
  talk(e,(34,13),'YES');assert e.location()[:2]==(46,0)
  var(e,0x40a5,e.var(0x40a5)&~(1<<13));talk(e,(15,13));assert e.var(0x40be)==0
  assert not actor(e,5) and not actor(e,6)
  talk(e,(9,13));assert not flag(e,0x8d6)
  save(e,'krakow-unstarted')
  for garden in (True,False):
   e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'krakow-unstarted',True);e.write('sWildEncountersDisabled',1,1)
   var(e,0x40a5,e.var(0x40a5)|(1<<13));var(e,0x40a2,(e.var(0x40a2)|(1<<13)) if garden else (e.var(0x40a2)&~(1<<13)))
   talk(e,(15,13),'NO');assert e.var(0x40be)==0
   talk(e,(15,13),'YES');assert e.var(0x40be)==1
   supply(e,85,1);supply(e,22,2);supply(e,97 if garden else 96,1)
   before=count(e,85);talk(e,(9,13),'NO');assert count(e,85)==before and not flag(e,0x8d6)
   talk(e,(9,13),'YES');assert count(e,85)==before-1 and flag(e,0x8d6) and tile(e,7,16)==0x165
   talk(e,(9,13));assert count(e,85)==before-1
   save(e,'krakow-partial');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'krakow-partial',True)
   assert e.var(0x40be)==1 and flag(e,0x8d6) and tile(e,7,16)==0x165 and not actor(e,5) and not actor(e,6), (e.var(0x40be),flag(e,0x8d6),tile(e,7,16),actor(e,5),actor(e,6))
   before=count(e,22);talk(e,(24,13),'YES');assert count(e,22)==before-2 and flag(e,0x8d7) and tile(e,22,16)==0x165
   stone=97 if garden else 96;supply(e,stone,0)
   talk(e,(39,13),'YES');assert not flag(e,0x8d8) and e.var(0x40be)==1
   supply(e,stone,1);talk(e,(39,13),'YES');assert count(e,stone)==0 and flag(e,0x8d8) and e.var(0x40be)==2
   assert tile(e,37,16)==(4 if garden else 0x165) and actor(e,5 if garden else 6) and not actor(e,6 if garden else 5)
   e.screenshot(ROOT/('test-output/eclipse-krakow-garden.png' if garden else 'test-output/eclipse-krakow-archive.png'))
   ready=ROOT/'test-output/krakow-ready.state';e.state(ready)
   p=e.read('gSaveBlock1Ptr')+0x310;k=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
   for i in range(42):e.write(p+4*i,197,2);e.write(p+4*i+2,999^k,2)
   talk(e,(15,13));assert not flag(e,0x8d9) and e.var(0x40be)==2
   e.state(ready,True);before=count(e,197);talk(e,(15,13));assert flag(e,0x8d9) and e.var(0x40be)==3 and count(e,197)==before+1
   talk(e,(15,13));assert count(e,197)==before+1
   pos=(24,25) if garden else (27,25);n=e.read('gPlayerPartyCount',1)
   talk(e,pos,'NO');assert not flag(e,0x8dc)
   talk(e,pos,'YES');assert flag(e,0x8dc) and e.read('gPlayerPartyCount',1)==n+1
   assert monfield(e,n,0,0)&0xffff==(133 if garden else 100) and e.read(e.symbols['gPlayerParty']+100*n+84,1)==30
   talk(e,pos);assert e.read('gPlayerPartyCount',1)==n+1
   name='krakow-garden-complete' if garden else 'krakow-archive-complete';save(e,name);e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,name,True)
   assert e.var(0x40be)==3 and flag(e,0x8dc) and count(e,197)==before+1 and actor(e,5 if garden else 6)
   talk(e,(15,29),'YES');assert e.location()[:2]==(45,26)
   talk(e,(34,13),'YES');assert e.location()[:2]==(46,0) and e.var(0x40be)==3
   print('PASS:', 'garden/EEVEE' if garden else 'archive/VOLTORB','native travel, materials, changed terrain, adoption, full-bag retry and cold persistence.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
