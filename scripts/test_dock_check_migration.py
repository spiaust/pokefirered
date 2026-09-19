"""A v0.39 save beside the future dockworker can start the new task immediately."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_garden import choose
from test_dock_check import notice
from test_le_havre import captain
old=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v0.39.gba')
try:
    load_checkpoint(old,'le-havre-complete',True)
    old.walk('UP',2);old.walk('RIGHT',1)
    assert old.location()==(43,35,9,3)
    start_action(old,4)
    for _ in range(5):old.press('A',150)
    old.battery(ROOT/'test-output/dock-check-old-adjacent.sav')
finally:old.close()
new=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(new,'dock-check-old-adjacent',True)
    assert new.location()==(43,35,9,3)
    new.press('RIGHT');new.press('A',180);choose(new)
    assert new.var(0x40DA)==1
    new.walk('LEFT',1);new.walk('DOWN',2);notice(new);captain(new)
    assert new.var(0x40DA)==3
    print('PASS: genuine v0.39 adjacent save immediately sees the dockworker and completes the task')
finally:new.close()
