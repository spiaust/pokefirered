"""Migration check using the archived v0.21 ROM and a real adjacent battery save."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,visit_forest
from test_time import cross
from test_gym_ui import start_action
old=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v0.21.gba')
try:
 load_checkpoint(old,'celebi-complete',True);visit_forest(old);cross(old)
 old.walk('RIGHT',7);old.walk('UP',1)
 assert old.location()==(43,29,12,9)
 start_action(old,4)
 for _ in range(5):old.press('A',150)
 old.battery(ROOT/'test-output/departure-old-adjacent.sav')
finally:old.close()
new=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(new,'departure-old-adjacent',True)
 assert new.location()==(43,29,12,9)
 new.press('UP');new.press('A',180)
 assert new.read('sLockFieldControls',1), ('Guide unavailable immediately after old adjacent save',new.location())
 new.finish_dialogue();assert new.location()==(43,29,12,9)
 print('PASS: save created on v0.21 beside the future guide loads with the new guide immediately available')
finally:new.close()
