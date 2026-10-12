"""Native Tough Claws slots and Kingdra cold-save summary QA."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture,ids,orders
from test_shadow_runtime import monfield,go,ensure_visible
from test_continent_runtime import world,var,battle_start
from test_gym_ui import start_action
from test_navigation import wait_task
from tm_teaching_test_helpers import field

def ability_slot(e,slot):
    p=e.symbols['gPlayerParty'];person=e.read(p);key=person^e.read(p+4)
    raw=bytearray().join((e.read(p+32+4*i)^key).to_bytes(4,'little') for i in range(12))
    offset=12*orders[person%24][3]+4;iv=int.from_bytes(raw[offset:offset+4],'little')
    raw[offset:offset+4]=((iv&~(1<<31))|(slot<<31)).to_bytes(4,'little')
    e.write(p+28,sum(int.from_bytes(raw[i:i+2],'little') for i in range(0,48,2))&65535,2)
    for i in range(12):e.write(p+32+4*i,int.from_bytes(raw[4*i:4*i+4],'little')^key)

from test_eclipse_friendship import candy
from test_eclipse_move_evolution import moves_fixture
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-circuit-complete',True);fixture(e,'BINACLE',255,0,0);ability_slot(e,0);moves_fixture(e,'MOVE_TACKLE')
    e.write(e.symbols['gPlayerParty']+0x54,38,1);candy(e);field(e)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_BARBARACLE'] and not ((monfield(e,0,3,4)>>31)&1)
    world(e,0);ensure_visible(e);go(e,(40,25));var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
    assert e.read(e.symbols['gBattleMons']+32,1)==104
    print('PASS: native Binacle/Barbaracle evolution preserves Tough Claws',flush=True)
finally:e.close()
