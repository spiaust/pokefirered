"""A v0.48 save beside the future Southampton clerk can board immediately."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_garden import choose
from test_london_past import LONDON,rose
old=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v0.48.gba')
try:
    load_checkpoint(old,'south-account-returned',True)
    old.walk('UP',1);old.walk('RIGHT',1);assert old.location()==(43,36,9,4)
    start_action(old,4)
    for _ in range(5):old.press('A',150)
    old.battery(ROOT/'test-output/london-old-adjacent.sav')
finally:old.close()
new=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(new,'london-old-adjacent',True)
    assert new.location()==(43,36,9,4)
    new.press('RIGHT');new.press('A',180);choose(new)
    assert new.location()==LONDON and new.var(0x40D5)==1
    rose(new)
    print('PASS: genuine v0.48 adjacent save immediately boards to London and checks in',flush=True)
finally:new.close()
