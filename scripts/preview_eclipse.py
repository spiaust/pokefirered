from emulator import Emulator,ROOT
from test_continent_runtime import world
from test_shadow_runtime import go,talk
from test_gym_ui import open_key_item
from test_navigation import wait_task

e=Emulator(ROOT/'pokefirered.gba')
try:
 e.state(ROOT/'test-output/continent-ready.state',True);world(e,2);go(e,(17,9));e.screenshot(ROOT/'test-output/eclipse-berlin-present.png');talk(e,(18,31),'YES');go(e,(17,9));e.screenshot(ROOT/'test-output/eclipse-berlin-past.png');open_key_item(e,361);wait_task(e,'Task_EuropeMap');e.screenshot(ROOT/'test-output/eclipse-passport-preview.png')
finally:e.close()
