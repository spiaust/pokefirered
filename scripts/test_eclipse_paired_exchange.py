"""Actual native paired exchange scenes, decline/cancel/wrong-mon guards and save."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world
from paired_trade_test_helpers import pair,offer,choose,finish
from test_eclipse_friendship import ids
from test_shadow_runtime import monfield
from test_gym_ui import start_action
from test_eclipse_reminder import bag,money
for kind in ('decline','cancel','wrong','everstone','both'):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
        pair(e,'SQUIRTLE' if kind=='wrong' else 'KARRABLAST','SHELMET',ownheld=195 if kind=='everstone' else 0)
        before=[monfield(e,i,0,0) for i in range(2)];stock=bag(e);cash=money(e)
        offer(e)
        if kind=='decline':e.press('B',180);e.press('B',180);finish(e)
        elif kind=='cancel':choose(e,cancel=True)
        else:
            choose(e);finish(e)
            if kind=='wrong':assert before==[monfield(e,i,0,0) for i in range(2)]
            elif kind=='everstone':assert monfield(e,0,0,0)&65535==ids['SPECIES_SHELMET']
            else:
                assert monfield(e,0,0,0)&65535==ids['SPECIES_ACCELGOR']
                assert monfield(e,1,0,0)&65535==ids['SPECIES_SHELMET']
                offer(e,second=True);choose(e,slot=1);finish(e)
                assert monfield(e,0,0,0)&65535==ids['SPECIES_ACCELGOR']
                assert monfield(e,1,0,0)&65535==ids['SPECIES_ESCAVALIER']
                e.screenshot(ROOT/'test-output/paired-exchange-both.png')
                start_action(e,4)
                for _ in range(8):e.press('A',240)
                e.battery(ROOT/'test-output/paired-exchange-both.sav')
        assert bag(e)==stock and money(e)==cash
        if kind in ('decline','cancel'):assert before==[monfield(e,i,0,0) for i in range(2)]
        print('PASS: native paired exchange',kind,'without bag/money changes',flush=True)
    finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'paired-exchange-both',True)
    for i,target in enumerate(('ACCELGOR','ESCAVALIER')):
        assert monfield(e,i,0,0)&65535==ids['SPECIES_'+target]
        extra=ids['SPECIES_'+target]-440;sb=e.read('gSaveBlock2Ptr')
        for offset in (0xb20,0xb70):assert e.read(sb+offset+extra//8,1)&(1<<(extra%8))
    print('PASS: both native traded evolutions and seen/caught entries survive cold Continue',flush=True)
finally:e.close()
