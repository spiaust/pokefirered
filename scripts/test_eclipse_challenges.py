"""Exercise actual faint retirement and repeated encounter enforcement with low-HP and escape-speed fixtures."""
from emulator import Emulator,ROOT
from test_shadow_runtime import talk,go,monfield,ensure_visible
from test_continent_runtime import var,battle_start,world,menu_row
from test_gym_ui import open_key_item
from test_navigation import wait_task

def toggle(e,row):
 open_key_item(e,363);wait_task(e,'Task_EuropeMap');menu_row(e,row);e.press('A',60)
 for _ in range(3):e.press('B',180)
def flee(e):
 action=next(int(t.split()[0],16)&~1 for t in (ROOT/'pokefirered.sym').read_text().splitlines() if t.split()[-1:]==['HandleInputChooseAction'])
 for _ in range(220):
  if not e.in_battle():break
  if e.read('gBattlerControllerFuncs')&~1==action:
   e.press('UP',2);e.press('LEFT',2);e.press('DOWN',2);e.press('RIGHT',2);e.press('A',90)
  else:e.press('A',30)
 assert not e.in_battle(),'flee failed'
 e.finish_dialogue();e.frames(240)
def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  e.state(ROOT/'test-output/start-england.state',True);talk(e,(10,16));toggle(e,9);assert e.var(0x4091)==1
  e.write(e.symbols['gPlayerParty']+0x56,1,2);battle_start(e,(6,4))
  for _ in range(400):
   if not e.in_battle():break
   e.press('A',45)
  assert not e.in_battle();e.finish_dialogue();e.frames(240)
  assert monfield(e,0,3,8)&(1<<28),'actual faint did not retire partner'
  assert e.read(e.symbols['gPlayerParty']+0x56,2)==0,'blackout revived retired partner'
  toggle(e,9);assert e.var(0x4091)==0
  if e.location()[0]==43:
   if e.location()[1]!=0:
    for _ in range(8):
     if e.location()[1]==0:break
     e.walk('DOWN',1);e.frames(90)
    assert e.location()[1]==0,e.location()
   talk(e,(10,16))
  talk(e,(2,4));assert e.read(e.symbols['gPlayerParty']+0x56,2)>0
  toggle(e,9);assert e.read(e.symbols['gPlayerParty']+0x56,2)==0
  print('PASS: real battle faint retires partner; blackout/nurse cannot revive; OFF allows healing; ON restores retirement.',flush=True)
  e.state(ROOT/'test-output/continent-ready.state',True);e.write(e.symbols['gPlayerParty']+0x5e,30000,2);toggle(e,9);world(e,0);ensure_visible(e);battle_start(e,(40,25));assert e.var(0x4094)==0
  species=monfield(e,0,0,0,'gEnemyParty')&0xffff;assert species==e.var(0x40A0)
  flee(e);ensure_visible(e);battle_start(e,(40,25));assert e.var(0x4094)==1;flee(e)
  talk(e,(18,31),'YES');ensure_visible(e);battle_start(e,(40,25));assert e.var(0x4094)==1;flee(e)
  toggle(e,9);ensure_visible(e);battle_start(e,(40,25));assert e.var(0x4094)==0;flee(e)
  toggle(e,10);assert e.var(0x4092)==1;e.walk('LEFT',1);e.walk('RIGHT',1)
  # A disabled actor cannot start a battle; ON resumes the rate-based field spawning.
  go(e,(40,25));e.press('UP');e.press('A',90);assert not e.in_battle();toggle(e,10);ensure_visible(e)
  print('PASS: matching visible species, first-encounter allowance, both eras share limit, optional mode and spawn toggles.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
