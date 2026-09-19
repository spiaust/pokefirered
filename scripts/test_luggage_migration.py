"""Real v0.44 save beside the new worker can start and finish the luggage task."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_garden import choose
from test_luggage import bag,worker
old=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v0.44.gba')
try:
    load_checkpoint(old,'southampton-complete',True)
    old.walk('UP',2);old.walk('RIGHT',1);assert old.location()==(43,36,9,3)
    start_action(old,4)
    for _ in range(5):old.press('A',150)
    old.battery(ROOT/'test-output/luggage-old-adjacent.sav')
finally:old.close()
new=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(new,'luggage-old-adjacent',True)
    assert new.location()==(43,36,9,3)
    new.press('RIGHT');new.press('A',180);choose(new)
    assert new.var(0x40D7)==1
    new.walk('LEFT',1);new.walk('DOWN',2);bag(new);worker(new)
    assert new.var(0x40D7)==3
    print('PASS: genuine v0.44 adjacent save immediately starts and completes luggage task',flush=True)
finally:new.close()
