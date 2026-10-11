"""Custom uniform palette alongside weather, visible partners and battle return.
Uses native World Gear inputs; remnant order and battle damage are explicit QA fixtures.
"""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world,var,menu_row
from test_shadow_runtime import go,ensure_visible
from test_gym_ui import open_key_item,start_action
from test_navigation import wait_task
from test_eclipse_villains import field_check,enter_battle,bytes_at
import json

def setting(e,row,ident,value):
 open_key_item(e,363);wait_task(e,'Task_EuropeMap');menu_row(e,row)
 for _ in range(4):
  if e.var(ident)==value:break
  e.press('A',60)
 assert e.var(ident)==value
 for _ in range(3):e.press('B',180)
 e.frames(600)

def win(e):
 # Resolve every static symbol alias; preserve native HP sizes for HUD updates.
 handlers={int(t.split()[0],16)&~1 for t in (ROOT/'pokefirered.sym').read_text().splitlines() if t.split()[-1:] in [['HandleInputChooseAction'],['HandleInputChooseMove']]}
 observed=set()
 for _ in range(900):
  if not e.in_battle():break
  if e.task_active('Task_HandleChooseMonInput'):
   e.press('B',180);continue
  fn=e.read('gBattlerControllerFuncs')&~1;observed.add(fn)
  if fn in handlers:
   b=e.symbols['gBattleMons'];ix=e.read('gBattlerPartyIndexes',1);hp=e.read(e.symbols['gPlayerParty']+100*ix+0x58,2)
   e.write(b+40,hp,2);e.write(b+44,hp,2)
   for off in (4,6,10):e.write(b+off,30000,2)
   e.write(b+76,0,4);e.write(b+88+40,1,2);e.write(b+12,82,2);e.write(b+36,40,1)
   e.press('UP',2);e.press('LEFT',2)
  e.press('B' if e.read(e.read('gBattlescriptCurrInstr'),1)==0x5a else 'A',30)
 if e.in_battle() or e.read('gBattleOutcome',1)!=1:
  e.screenshot(ROOT/'test-output/villain-rime-return-stalled.png');e.state(ROOT/'test-output/villain-rime-return-stalled.state')
  raise AssertionError(('return fixture',e.in_battle(),e.read('gBattleOutcome',1),[hex(f) for f in observed],[hex(f) for f in handlers]))
 e.finish_dialogue();e.frames(240)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'natural-league-20-complete',True);var(e,0x40bd,2)
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Continent']
 world(e,groups.index('ContinentOslo')//2);e.write('sWildEncountersDisabled',1,1)
 m=json.loads((ROOT/'data/maps/ContinentOslo/map.json').read_text());o=next(o for o in m['object_events'] if o['script']=='EclipseNordic_Rime');target=(o['x'],o['y']+1)
 wild_local=next(i+1 for i,o in enumerate(m['object_events']) if o['graphics_id']=='OBJ_EVENT_GFX_VAR_0')
 setting(e,12,0x40d1,1);setting(e,11,0x40d0,2);go(e,target);pal=field_check(e,'rime')
 w=e.read('gWeatherPtr');assert e.read(w+0x6d0,1)==3 and e.read(w+0x6da,1)>0
 e.screenshot(ROOT/'test-output/villain-rime-rain.png')
 setting(e,11,0x40d0,3);setting(e,12,0x40d1,2);assert e.read(w+0x6d0,1)==4 and e.read(w+0x6e4,1)==16
 field_check(e,'rime');e.screenshot(ROOT/'test-output/villain-rime-snow-night.png')
 ensure_visible(e)
 # Each city has a different river layout; find a reachable shared view.
 candidates=sorted([(x,y) for x in range(32,41) for y in range(17,20)],key=lambda p:abs(p[0]-36)+abs(p[1]-18))
 for point in candidates:
  try:go(e,point);break
  except AssertionError:continue
 else:raise AssertionError('No reachable view of the two actors')
 rime_pal=field_check(e,'rime',visible=False)
 objects=e.symbols['gObjectEvents']
 for i in range(16):
  p=objects+36*i
  if e.read(p,1)&1 and e.read(p+8,1)==wild_local:
   sid=e.read(p+4,1);wild_pal=e.read(e.symbols['gSprites']+68*sid+5,1)>>4
   assert wild_pal!=rime_pal,('wild partner palette collision',wild_pal,rime_pal)
   break
 else:raise AssertionError('No visible partner beside Rime')
 e.screenshot(ROOT/'test-output/villain-rime-visible-partner.png')
 enter_battle(e,target,377,'rime');e.state(ROOT/'test-output/villain-rime-return-ready.state');win(e)
 go(e,target);field_check(e,'rime');assert e.var(0x40bd)==3
 e.screenshot(ROOT/'test-output/villain-rime-battle-return.png')
 print('PASS: custom uniform palette survives rain, night snow, visible partner coexistence and native battle return',flush=True)
 start_action(e,4)
 for _ in range(8):e.press('A',240)
 e.battery(ROOT/'test-output/villain-uniforms.sav');e.press('B',180);e.press('B',180)
 location=e.location();e.close();e=Emulator(ROOT/'pokefirered.gba')
 load_checkpoint(e,'villain-uniforms',True)
 assert e.location()==location and e.var(0x40bd)==3 and e.var(0x40d0)==3 and e.var(0x40d1)==2,(e.location(),location,e.var(0x40bd),e.var(0x40d0),e.var(0x40d1))
 field_check(e,'rime');e.screenshot(ROOT/'test-output/villain-rime-continue.png')
 print('PASS: native Save and cold Continue restore the custom actor, uniform colors, night snow and remnant progress',flush=True)
finally:e.close()
