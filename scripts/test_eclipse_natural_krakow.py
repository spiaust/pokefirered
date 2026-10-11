"""Restore Krakow with an earned wartime choice and purchased materials."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk
from test_continent_runtime import world,battle_start,bit
from test_eclipse_legendaries import flag
from test_eclipse_krakow import tile,actor,count
from natural_supplies_test_helpers import buy
from natural_capture_test_helpers import boxed_records
from test_landmark_cases import save

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-nordic-complete',True)
  talk(e,(43,31),'YES');talk(e,(10,16),'YES');assert e.location()[:2]==(44,40)
  buy(e,((85,1,550),(22,2,700),(97,1,2100)))
  world(e,13);talk(e,(12,31));talk(e,(18,31),'YES');assert e.location()[:2]==(45,27)
  battle_start(e,(15,19));result,turns=natural.natural_battle(e,healing_item=21,healing_limit=count(e,21),fallback_species=31,trace=True)
  assert result==1 and bit(e,0x40AF,13)
  talk(e,(27,29),'YES');assert bit(e,0x40A5,13) and bit(e,0x40A2,13)
  talk(e,(18,31),'YES');assert e.location()[:2]==(45,26)
  talk(e,(34,13),'YES');assert e.location()[:2]==(46,0)
  talk(e,(15,13),'YES');assert e.var(0x40BE)==1
  for pos,item,qty,f in (((9,13),85,1,0x8D6),((24,13),22,2,0x8D7),((39,13),97,1,0x8D8)):
   before=count(e,item);talk(e,pos,'NO');assert count(e,item)==before and not flag(e,f)
   talk(e,pos,'YES');assert count(e,item)==before-qty and flag(e,f)
  assert e.var(0x40BE)==2 and tile(e,7,16)==0x165 and tile(e,22,16)==0x165 and tile(e,37,16)==4 and actor(e,5)
  before=count(e,197);talk(e,(15,13));assert e.var(0x40BE)==3 and count(e,197)==before+1
  before_box=boxed_records(e,133);talk(e,(24,25),'YES');assert flag(e,0x8DC) and e.read('gPlayerPartyCount',1)==6
  records=boxed_records(e,133);assert len(records)==len(before_box)+1
  talk(e,(24,25));assert boxed_records(e,133)==records
  save(e,'natural-krakow-complete');e.screenshot(ROOT/'test-output/natural-krakow-complete.png')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-krakow-complete',True)
  assert e.var(0x40BE)==3 and flag(e,0x8DC) and count(e,197)==before+1 and boxed_records(e,133)==records and actor(e,5)
  assert tile(e,37,16)==4 and bit(e,0x40A2,13) and e.var(0x40BD)==5
  print('PASS: earned Warsaw operation, garden timeline, material donations, Lucky Egg and native boxed Eevee adoption survive cold Continue.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
