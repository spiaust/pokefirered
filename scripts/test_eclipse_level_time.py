"""Native level/time evolutions, local RTC fixtures, overrides and cold saves."""
import argparse
from datetime import datetime,timezone
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture,candy,ids
from test_eclipse_move_evolution import moves_fixture
from test_continent_runtime import var
from test_shadow_runtime import monfield
from test_gym_ui import start_action
from tm_teaching_test_helpers import field
parser=argparse.ArgumentParser();parser.add_argument('--cases');args=parser.parse_args()
cases=[('TYRUNT','TYRANTRUM',38,12,0,0,0),('AMAURA','AURORUS',38,22,0,0,0),('YUNGOOS','GUMSHOOS',19,12,0,0,0),('ROCKRUFF','LYCANROC',24,12,0,0,0),('FOMANTIS','LURANTIS',33,12,0,0,0),('GREAVARD','HOUNDSTONE',29,22,0,0,0),('COSMOEM','SOLGALEO',52,12,0,0,0),('COSMOEM','LUNALA',52,22,0,0,0),
 ('TYRUNT','TYRUNT',38,22,0,0,0),('AMAURA','AMAURA',38,12,0,0,0),('YUNGOOS','YUNGOOS',19,22,0,0,0),('ROCKRUFF','ROCKRUFF',24,22,0,0,0),('FOMANTIS','FOMANTIS',33,22,0,0,0),('GREAVARD','GREAVARD',29,12,0,0,0),('COSMOEM','COSMOEM',51,12,0,0,0),('COSMOEM','COSMOEM',51,22,0,0,0),
 ('COSMOEM','SOLGALEO',52,22,1,0,0),('COSMOEM','LUNALA',52,12,2,0,0),('TYRUNT','TYRUNT',38,12,0,195,0),('AMAURA','AMAURA',38,22,0,0,1),('TYRUNT','TYRUNT',37,12,0,0,0),('GREAVARD','GREAVARD',28,22,0,0,0)]
selected=set(map(int,args.cases.split(','))) if args.cases else set(range(len(cases)))
for n,(species,target,level,hour,mode,held,shadow) in enumerate(cases):
    if n not in selected:continue
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True)
        e.rtc(int(datetime(2026,10,11,hour,tzinfo=timezone.utc).timestamp()));e.frames(120);var(e,0x40d1,mode)
        fixture(e,species,255,held,shadow);moves_fixture(e,'MOVE_TACKLE');e.write(e.symbols['gPlayerParty']+0x54,level,1);candy(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,target)
        print('PASS:',n,species,'->',target,'level',level+1,'hour',hour,'mode',mode,flush=True)
        if n in (6,7):
            field(e);start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/('test-output/time-'+target.lower()+'.sav'))
    finally:e.close()
for n,target in ((6,'SOLGALEO'),(7,'LUNALA')):
    if n not in selected:continue
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'time-'+target.lower(),True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target]
        extra=ids['SPECIES_'+target]-440;mask=1<<(extra%8);sb=e.read('gSaveBlock2Ptr')
        assert e.read(sb+0xb20+extra//8,1)&mask and e.read(sb+0xb70+extra//8,1)&mask
        print('PASS:',target,'and seen/caught entries survive Save/cold Continue',flush=True)
    finally:e.close()
