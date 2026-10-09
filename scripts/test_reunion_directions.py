"""Both native witness orders and saved Amiens Meowth reunion."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_reunion import STORY,talk,relocated
from test_time import preserved
from key_item_test_helpers import reload
from test_country import wait_menu

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/reunion-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

def nora_pages(e,count,label,accept=False):
 e.walk('UP',1);e.walk('LEFT',4);e.walk('UP',6);before=preserved(e)
 e.press('UP');e.press('A',180)
 if accept:
  wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180)
 pages(e,count,label);assert preserved(e)==before
 e.walk('DOWN',6);e.walk('RIGHT',4);e.walk('DOWN',1)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'amiens-directions-returned',True);assert e.var(STORY)==0 and e.var(0x40E1)==4
 for choice in ['B','NO']:talk(e,'nora',choice);assert e.var(STORY)==0
 nora_pages(e,3,'active',True);assert e.var(STORY)==1
 e=reload(e,'reunion-directions-active');talk(e,'nora');assert e.var(STORY)==1
 print('PASS: optional reunion No/B preserve unaccepted quest; three witness-direction pages and cold Continue retain real acceptance',flush=True)
 for first,second,stage in [('mira','porter',2),('porter','mira',3)]:
  if first=='porter':
   e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'reunion-directions-active',True)
  talk(e,first);talk(e,first);assert e.var(STORY)==stage
  e=reload(e,'reunion-directions-'+first);talk(e,'nora');assert e.var(STORY)==stage
  talk(e,second);assert e.var(STORY)==4;e=reload(e,'reunion-directions-both-'+first)
  talk(e,'nora');assert e.var(STORY)==5;nora_pages(e,2,'verified-'+first)
  e=reload(e,'reunion-directions-verified-'+first);talk(e,'nora');assert e.var(STORY)==5
  talk(e,'mira');assert e.var(STORY)==6;relocated(e)
  e=reload(e,'reunion-directions-complete-'+first);relocated(e)
  for who in ['home','mira','porter','nora']:talk(e,who)
  assert e.var(STORY)==6 and e.var(0x40E1)==4
  print('PASS: '+first+'-first native reports, repeated witnesses and saved verification lead to real reunion; cold Continue retains relocated Meowth and optional rest decline',flush=True)
finally:e.close()
