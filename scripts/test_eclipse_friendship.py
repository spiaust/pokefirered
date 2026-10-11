"""Native Rare Candy evolution with explicit species/friendship/held-item fixtures.
No personal saves are used. Rules, cancellation guards, RTC and overrides are checked.
"""
import re
from datetime import datetime, timezone
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_navigation import wait_task
from test_shadow_runtime import monfield
from test_continent_runtime import var
from eclipse_evolutions import project

constants=(ROOT/'include/constants/species.h').read_text()
ids={a:int(b) for a,b in re.findall(r'#define (SPECIES_\w+)\s+(\d+)',constants)}
orders={int(a):tuple(map(int,b)) for a,*b in re.findall(r'SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)',(ROOT/'src/pokemon.c').read_text())}

def fixture(e,species,friendship,held,shadow):
    p=e.symbols['gPlayerParty']; person=e.read(p);key=person^e.read(p+4)
    raw=bytearray().join((e.read(p+32+4*i)^key).to_bytes(4,'little') for i in range(12))
    order=orders[person%24];growth=12*order[0];misc=12*order[3]
    raw[growth:growth+2]=ids['SPECIES_'+species].to_bytes(2,'little')
    raw[growth+2:growth+4]=held.to_bytes(2,'little');raw[growth+9]=friendship
    ribbons=int.from_bytes(raw[misc+8:misc+12],'little')
    raw[misc+8:misc+12]=((ribbons&~(1<<27)) | (shadow<<27)).to_bytes(4,'little')
    e.write(p+28,sum(int.from_bytes(raw[i:i+2],'little') for i in range(0,48,2))&65535,2)
    for i in range(12):e.write(p+32+4*i,int.from_bytes(raw[4*i:4*i+4],'little')^key)
    e.write(p+0x54,50,1);e.write('gPlayerPartyCount',1,1)
    bag=e.read('gSaveBlock1Ptr')+0x310;k=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
    for i in range(42):e.write(bag+4*i,0)
    e.write(bag,68,2);e.write(bag+2,1^k,2)

def candy(e,stale=False):
    start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
    if stale: e.write('sEclipseLocalMinute',0 if e.read('sEclipseLocalMinute',2)>=360 and e.read('sEclipseLocalMinute',2)<1200 else 720,2)
    for _ in range(5):
        if e.read(bag+6,2)==0:break
        e.press('LEFT',90)
    for _ in range(45):
        if e.read(bag+8,2)+e.read(bag+14,2)==0:break
        e.press('UP',30)
    e.press('A',90);e.press('A',180);e.press('A',180)
    for _ in range(90):e.press('A',90)

def main():
    cases=[('RIOLU','LUCARIO',12,0,255,0,0),('RIOLU','RIOLU',22,0,255,0,0),
     ('SNOM','FROSMOTH',22,0,255,0,0),('SNOM','SNOM',12,0,255,0,0),
     ('BUDEW','ROSELIA',12,0,255,0,0),('CHINGLING','CHIMECHO',22,0,255,0,0),
     ('BUNEARY','LOPUNNY',12,0,255,0,0),('MUNCHLAX','SNORLAX',22,0,255,0,0),
     ('EEVEE','ESPEON',12,0,255,0,0),('EEVEE','UMBREON',22,0,255,0,0),
     ('RIOLU','LUCARIO',22,1,255,0,0),('SNOM','FROSMOTH',12,2,255,0,0),
     ('RIOLU','RIOLU',12,0,0,0,0),('RIOLU','RIOLU',12,0,255,195,0),
     ('RIOLU','RIOLU',12,0,255,0,1)]
    cases += [('WOOBAT','SWOOBAT',12,0,255,0,0),('SWADLOON','LEAVANNY',12,0,255,0,0),('TYPE_NULL','SILVALLY',12,0,255,0,0),
     ('RIOLU','RIOLU',5,0,255,0,0),('RIOLU','LUCARIO',6,0,255,0,0),('RIOLU','LUCARIO',19,0,255,0,0),('RIOLU','RIOLU',20,0,255,0,0),('RIOLU','LUCARIO',12,0,255,0,0),('SNOM','FROSMOTH',22,0,255,0,0)]
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--cases');args=parser.parse_args()
    selected=set(map(int,args.cases.split(','))) if args.cases else set(range(len(cases)))
    for n,(species,target,hour,mode,friendship,held,shadow) in enumerate(cases):
        if n not in selected: continue
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'natural-circuit-complete',True)
            # mGBA RTC fixture uses UTC TZ, making its host-local RTC deterministic.
            e.rtc(int(datetime(2026,10,11,hour,0,tzinfo=timezone.utc).timestamp()));e.frames(120)
            assert e.read('sEclipseLocalMinute',2)//60==hour
            var(e,0x40d1,mode);fixture(e,species,friendship,held,shadow);candy(e,n>=22)
            actual=monfield(e,0,0,0)&65535
            assert actual==ids['SPECIES_'+target],(n,species,target,actual)
            assert e.read(e.symbols['gPlayerParty']+0x54,1)==51
            if n == 17:
                from tm_teaching_test_helpers import field
                field(e);e.screenshot(ROOT/'test-output/friendship-silvally.png')
                start_action(e,4)
                for _ in range(8):e.press('A',240)
                e.battery(ROOT/'test-output/friendship-silvally.sav')
            print('PASS:',n,species,'->',target,'RTC',hour,'override',mode,flush=True)
        finally:e.close()

    if 17 in selected:
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'friendship-silvally',True)
            assert monfield(e,0,0,0)&65535==ids['SPECIES_SILVALLY']
            assert e.read(e.symbols['gPlayerParty']+0x54,1)==51
            print('PASS: evolved Silvally survives native Save and cold Continue',flush=True)
        finally:e.close()

if __name__ == '__main__':
    main()
