"""Native Sylveon evolution, obtainable Fairy lesson and cold-save QA.
Species/friendship/moves are explicit isolated fixtures; UI learning/evolution/save are native.
"""
from datetime import datetime, timezone
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture, candy, ids
from test_eclipse_move_evolution import moves_fixture, moves
from test_shadow_runtime import monfield
from test_continent_runtime import world, var
from test_eclipse_reminder import lesson, bag, money
from tm_teaching_test_helpers import field
from test_gym_ui import start_action

cases=[(12,255,0,0,'MOVE_BABY_DOLL_EYES',0,'SYLVEON'),
       (22,255,0,0,'MOVE_BABY_DOLL_EYES',3,'SYLVEON'),
       (12,0,0,0,'MOVE_BABY_DOLL_EYES',0,'EEVEE'),
       (12,255,195,0,'MOVE_BABY_DOLL_EYES',0,'EEVEE'),
       (22,255,0,1,'MOVE_BABY_DOLL_EYES',0,'EEVEE'),
       (12,255,0,0,'MOVE_TACKLE',0,'ESPEON'),
       (22,255,0,0,'MOVE_TACKLE',0,'UMBREON'),
       (12,255,0,0,'MOVE_FAIRY_WIND',2,'SYLVEON'),
       (12,255,0,0,'MOVE_BABY_DOLL_EYES',1,'SYLVEON')]
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--cases');args=parser.parse_args()
selected=set(map(int,args.cases.split(','))) if args.cases else set(range(len(cases)))
for n,(hour,friendship,held,shadow,move,slot,target) in enumerate(cases):
    if n not in selected:continue
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True)
        e.rtc(int(datetime(2026,10,11,hour,tzinfo=timezone.utc).timestamp()));e.frames(120)
        var(e,0x40d1,0);fixture(e,'EEVEE',friendship,held,shadow);moves_fixture(e,move,slot)
        candy(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,target)
        print('PASS:',n,'Eevee ->',target,'hour',hour,'move',move,'slot',slot,flush=True)
    finally:e.close()

if args.cases is not None:raise SystemExit(0)

for level,reminder in ((14,False),(50,True)):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);world(e,0)
        fixture(e,'EEVEE',255,0,0);moves_fixture(e,'MOVE_TACKLE')
        e.write(e.symbols['gPlayerParty']+0x54,level,1)
        if reminder:
            before=bag(e);cash=money(e);lesson(e,'MOVE_BABY_DOLL_EYES')
            assert before==bag(e) and cash==money(e)
        candy(e)
        assert moves['MOVE_BABY_DOLL_EYES'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
        assert monfield(e,0,0,0)&65535==ids['SPECIES_SYLVEON']
        print('PASS: obtainable Baby-Doll Eyes via', 'free reminder' if reminder else 'level 15', 'then native Sylveon evolution',flush=True)
        if reminder:
            field(e);start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/'test-output/sylveon.sav')
    finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'sylveon',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_SYLVEON']
    assert moves['MOVE_BABY_DOLL_EYES'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
    extra=ids['SPECIES_SYLVEON']-440;mask=1<<(extra%8);sb=e.read('gSaveBlock2Ptr')
    assert e.read(sb+0xb20+extra//8,1)&mask and e.read(sb+0xb70+extra//8,1)&mask
    print('PASS: Sylveon, Fairy move and seen/caught entries survive native Save/cold Continue',flush=True)
finally:e.close()
