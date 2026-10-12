"""Native Dragon Cheer evolution, free lesson and cold-save QA."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture,candy,ids
from test_eclipse_move_evolution import moves_fixture,moves
from test_shadow_runtime import monfield
from test_continent_runtime import world
from test_eclipse_reminder import lesson,bag,money
from test_gym_ui import start_action
from tm_teaching_test_helpers import field
for n,(move,held,shadow,target) in enumerate([('MOVE_DRAGON_CHEER',0,0,'HYDRAPPLE'),('MOVE_DRAGON_PULSE',0,0,'DIPPLIN'),('MOVE_DRAGON_CHEER',195,0,'DIPPLIN'),('MOVE_DRAGON_CHEER',0,1,'DIPPLIN')]):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'DIPPLIN',255,held,shadow);moves_fixture(e,move,3);candy(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
        print('PASS:',n,'Dipplin ->',target,move,flush=True)
    finally:e.close()
for level,target in ((38,'DIPPLIN'),(39,'HYDRAPPLE')):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'DIPPLIN',255,0,0);moves_fixture(e,'MOVE_TACKLE')
        e.write(e.symbols['gPlayerParty']+0x54,level,1);candy(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
        if level==39:assert moves['MOVE_DRAGON_CHEER'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
        print('PASS: native level',level+1,'Dipplin ->',target,flush=True)
    finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);world(e,0);fixture(e,'DIPPLIN',255,0,0);moves_fixture(e,'MOVE_TACKLE')
    before=bag(e);cash=money(e);lesson(e,'MOVE_DRAGON_CHEER')
    assert bag(e)==before and money(e)==cash;candy(e)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_HYDRAPPLE']
    field(e);start_action(e,4)
    for _ in range(8):e.press('A',240)
    e.battery(ROOT/'test-output/cheer-hydrapple.sav')
    print('PASS: free level-40 Dragon Cheer reminder, then native Hydrapple evolution',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'cheer-hydrapple',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_HYDRAPPLE'] and moves['MOVE_DRAGON_CHEER'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
    extra=ids['SPECIES_HYDRAPPLE']-440;mask=1<<(extra%8);sb=e.read('gSaveBlock2Ptr')
    assert e.read(sb+0xb20+extra//8,1)&mask and e.read(sb+0xb70+extra//8,1)&mask
    print('PASS: Hydrapple, Dragon Cheer and seen/caught flags survive Save/cold Continue',flush=True)
finally:e.close()
