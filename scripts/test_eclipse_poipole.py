"""Native Dragon Pulse evolution, free lesson and cold-save QA."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture,candy,ids
from test_eclipse_move_evolution import moves_fixture,moves
from test_shadow_runtime import monfield
from test_continent_runtime import world
from test_eclipse_reminder import lesson,bag,money
from test_gym_ui import start_action
from tm_teaching_test_helpers import field
for n,(move,held,shadow,target) in enumerate([('MOVE_DRAGON_PULSE',0,0,'NAGANADEL'),('MOVE_DRAGON_BREATH',0,0,'POIPOLE'),('MOVE_DRAGON_PULSE',195,0,'POIPOLE'),('MOVE_DRAGON_PULSE',0,1,'POIPOLE')]):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'POIPOLE',255,held,shadow);moves_fixture(e,move,3);candy(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
        print('PASS:',n,'Poipole ->',target,move,flush=True)
    finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0);fixture(e,'POIPOLE',255,0,0);moves_fixture(e,'MOVE_TACKLE')
    before=bag(e);cash=money(e);lesson(e,'MOVE_DRAGON_PULSE')
    assert bag(e)==before and money(e)==cash;candy(e)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_NAGANADEL']
    field(e);start_action(e,4)
    for _ in range(8):e.press('A',240)
    e.battery(ROOT/'test-output/poipole-naganadel.sav')
    print('PASS: free level-1 Dragon Pulse reminder, then native Naganadel evolution',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'poipole-naganadel',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_NAGANADEL'] and moves['MOVE_DRAGON_PULSE'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
    extra=ids['SPECIES_NAGANADEL']-440;mask=1<<(extra%8);sb=e.read('gSaveBlock2Ptr')
    assert e.read(sb+0xb20+extra//8,1)&mask and e.read(sb+0xb70+extra//8,1)&mask
    print('PASS: Naganadel, Dragon Pulse and seen/caught flags survive Save/cold Continue',flush=True)
finally:e.close()
