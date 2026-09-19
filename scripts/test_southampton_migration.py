"""A genuine v0.43 save beside the future ferry clerk boards on the new ROM."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_garden import choose
from test_southampton import SOUTH,host
old=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v0.43.gba')
try:
    load_checkpoint(old,'port-return-arrived',True)
    old.walk('UP',2);old.walk('LEFT',2);assert old.location()==(43,35,6,3)
    start_action(old,4)
    for _ in range(5):old.press('A',150)
    old.battery(ROOT/'test-output/southampton-old-adjacent.sav')
finally:old.close()
new=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(new,'southampton-old-adjacent',True)
    assert new.location()==(43,35,6,3)
    new.press('LEFT');new.press('A',180);choose(new)
    assert new.location()==SOUTH and new.var(0x40D8)==1
    host(new);assert new.var(0x40D8)==2
    print('PASS: genuine v0.43 adjacent save immediately boards with the new clerk',flush=True)
finally:new.close()
