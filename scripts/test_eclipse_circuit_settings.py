"""Native World Gear changes during a saved circuit and classic rival regression."""
from test_eclipse_circuit import *
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_continent_runtime import menu_row


def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-circuit-partial',True);assert e.var(0x40bf)==6
  open_key_item(e,363);wait_task(e,'Task_EuropeMap');menu_row(e,8)
  for mode in (1,2,0):e.press('A',60);assert e.var(0x4090)==mode and e.var(0x40bf)==6
  for _ in range(3):e.press('B',180)
  assert not e.read('sLockFieldControls',1)
  print('PASS: native World Gear changes Easy/Hard/Normal mid-circuit without changing its saved card.',flush=True)
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'eclipse-finished',True);var(e,0x408c,0);
  n=0x500+100;p=e.read('gSaveBlock1Ptr')+0xee0+n//8;e.write(p,e.read(p,1)&~(1<<(n%8)),1)
  e.write('sWildEncountersDisabled',1,1)
  talk(e,(6,7));talk(e,(10,16),'YES');assert e.location()[:2]==(44,0)
  before=ROOT/'test-output/circuit-classic-rival.state';e.state(before)
  for starter,(evolved,kind) in COUNTERS.items():
   e.state(before,True);var(e,0x40f6,SPECIES['SPECIES_'+starter]);battle_start(e,(6,4))
   baby={'CHARIZARD':'CHARMANDER','BLASTOISE':'SQUIRTLE','VENUSAUR':'BULBASAUR','TYPHLOSION':'CYNDAQUIL','FERALIGATR':'TOTODILE','MEGANIUM':'CHIKORITA','BLAZIKEN':'TORCHIC','SWAMPERT':'MUDKIP','SCEPTILE':'TREECKO'}[evolved]
   assert monfield(e,0,0,0,'gEnemyParty')&0xffff==SPECIES['SPECIES_'+baby]
   assert e.read(e.symbols['gEnemyParty']+84,1)==6
   assert [monfield(e,0,1,k,'gEnemyParty')&0xffff for k in (2,4,6)]==[0,0,0]
  print('PASS: all nine original opening rivals retain their level-six baby counter-starter and single attack.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
