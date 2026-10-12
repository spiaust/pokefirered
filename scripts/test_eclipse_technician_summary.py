"""Final-ROM cold-save and single-line Technician description rendering."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_navigation import wait_task
from test_shadow_runtime import monfield
from test_eclipse_friendship import ids
from tm_teaching_test_helpers import field
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'technician-scizor',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_SCIZOR'] and (monfield(e,0,3,4)>>31)&1
    start_action(e,1);wait_task(e,'Task_HandleChooseMonInput');e.press('A',60)
    wait_task(e,'Task_HandleSelectionMenuInput');e.press('A',240);e.press('RIGHT',120)
    assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_RunPokemonSummaryScreen']&~1
    e.screenshot(ROOT/'test-output/technician-scizor-summary-final.png');field(e)
    print('PASS: final ROM cold Continue and Technician skills/description UI returns to field',flush=True)
finally:e.close()
