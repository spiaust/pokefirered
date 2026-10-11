"""Native combat checks. Battle fixtures accelerate victories; they do not assert balance."""
from emulator import Emulator,ROOT
from test_shadow_runtime import talk,go,monfield,ensure_visible
from test_continent_runtime import world,var,battle_start,accelerated_win,bit,D
from test_country import party_species
from test_gym_ui import open_key_item
from test_navigation import wait_task
import json,sys

def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  for country,expected in [('england',[4,158,152]),('france',[155,283,1]),('germany',[280,7,277])]:
   city={'england':'London','france':'Paris','germany':'Berlin'}[country]
   m=json.loads((ROOT/f'data/maps/Europe{city}/map.json').read_text());o=next(o for o in m['object_events'] if o['script']=='Shadow_Entrance')
   for i,species in enumerate(expected):
    e.state(ROOT/f'test-output/start-{country}-{i}.state',True);talk(e,(o['x'],o['y']+1));battle_start(e,(6,4))
    assert monfield(e,0,0,0,'gEnemyParty')&0xffff==species,(country,i,species)
   print('PASS:',country,'all three rival counter-starters',flush=True)
  for mode,level in [(0,16),(1,12),(2,21)]:
   e.state(ROOT/'test-output/continent-ready.state',True);var(e,0x4090,mode);world(e,0);battle_start(e,(15,19))
   assert e.read(e.symbols['gEnemyParty']+0x54,1)==level,(mode,level)
  print('PASS: Normal/Easy/Hard create real opponent levels 16/12/21.',flush=True)
  if '--opening-only' in sys.argv:return
  e.state(ROOT/'test-output/continent-ready.state',True)
  for i,d in enumerate(D):
   world(e,i);talk(e,(12,31));talk(e,(18,31),'YES');battle_start(e,(15,19));accelerated_win(e)
   assert bit(e,0x40AF,i),(i,'wartime victory not recorded')
   talk(e,(27,29),'YES');assert bit(e,0x40A5,i);talk(e,(18,31),'YES')
   print('PASS:',d['country'],'actual wartime victory unlocks its saved future choice',flush=True)
  e.state(ROOT/'test-output/continent-battles.state')
  # The country passport must be usable and show independent destinations.
  open_key_item(e,361);wait_task(e,'Task_EuropeMap');e.screenshot(ROOT/'test-output/eclipse-passport.png');e.press('DOWN',60);e.press('SELECT',60);e.press('B',180);e.press('B',180);e.press('B',180)
 finally:e.close()
if __name__=='__main__':main()
