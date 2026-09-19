"""New transport clerk works immediately beside an archived v0.38 save."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_garden import choose
old=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v0.38.gba')
try:
    load_checkpoint(old,'route-book-complete',True)
    old.walk('RIGHT',8);old.walk('UP',1)
    assert old.location()==(43,34,18,15)
    start_action(old,4)
    for _ in range(5):old.press('A',150)
    old.battery(ROOT/'test-output/le-havre-old-adjacent.sav')
finally:old.close()
new=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(new,'le-havre-old-adjacent',True)
    assert new.location()==(43,34,18,15)
    new.press('UP');new.press('A',180);choose(new)
    assert new.location()==(43,35,8,5) and new.var(0x40DB)==1
    print('PASS: archived v0.38 save beside the new clerk can immediately board to Le Havre')
finally:new.close()
