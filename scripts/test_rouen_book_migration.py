"""Create an archived v0.35 save beside Leon, then use the new quest immediately."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_garden import choose
from test_rouen_book import book,STORY
old=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v0.35.gba')
try:
    load_checkpoint(old,'rouen-complete',True)
    old.walk('UP',1);old.walk('LEFT',4);old.walk('UP',6)
    assert old.location()==(43,34,6,9)
    start_action(old,4)
    for _ in range(5):old.press('A',150)
    old.battery(ROOT/'test-output/book-old-adjacent.sav')
finally:old.close()
new=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(new,'book-old-adjacent',True)
    assert new.location()==(43,34,6,9)
    new.press('UP');new.press('A',180);choose(new)
    assert new.var(STORY)==1
    new.walk('DOWN',6);new.walk('RIGHT',4);new.walk('DOWN',1)
    book(new)
    print('PASS: genuine v0.35 adjacent save immediately offers the quest and spawns a collectible route book')
finally:new.close()
