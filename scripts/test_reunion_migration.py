"""Migration check using the archived v0.29 ROM and a real adjacent battery save."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,visit_forest
from test_time import cross
from test_gym_ui import start_action
old=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v0.29.gba')
try:
 load_checkpoint(old,'amiens-complete',True)
 old.walk('RIGHT',3);old.walk('UP',7)
 assert old.location()==(43,33,13,9)
 start_action(old,4)
 for _ in range(5):old.press('A',150)
 old.battery(ROOT/'test-output/reunion-old-adjacent.sav')
finally:old.close()
new=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(new,'reunion-old-adjacent',True)
 assert new.location()==(43,33,13,9)
 new.press('UP');new.press('A',180)
 assert new.read('sLockFieldControls',1), ('Mira unavailable immediately after old adjacent save',new.location())
 new.finish_dialogue();assert new.location()==(43,33,13,9)
 print('PASS: save created on v0.29 beside the future Mira loads with the Mira immediately available')
finally:new.close()
