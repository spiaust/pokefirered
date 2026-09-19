"""Amiens party care: reunion gate, choices, healing, travel and old saves."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_amiens import AMIENS, leave, board, reach_post
from test_reunion import talk, relocated
from test_relief import health, tire_party, assert_healed, decoded_mon
from test_time import preserved, cross
from test_country import wait_menu
from test_journal import inspect

def identity(emu):
    result=[]
    for i in range(emu.read('gPlayerPartyCount',1)):
        mon, _, data, _, attacks = decoded_mon(emu,i)
        data[attacks+8:attacks+12]=bytes(4)
        result.append((bytes(emu.read(mon+j,1) for j in range(28)),bytes(data)))
    return result

def rest(emu,choice='YES'):
    assert emu.location()==AMIENS
    emu.walk('UP',1);emu.walk('LEFT',4);emu.walk('UP',6)
    emu.press('UP');emu.press('A',180)
    wait_menu(emu,'Task_YesNoMenu_HandleInput');emu.frames(60)
    before=preserved(emu); ids=identity(emu); tired=health(emu)
    progress=tuple(emu.var(v) for v in range(0x40E0,0x4100))
    emu.screenshot(ROOT/'test-output/amiens-care-offer.png')
    if choice=='NO':emu.press('DOWN')
    emu.press('B' if choice=='B' else 'A',180)
    emu.finish_dialogue()
    assert not emu.read('sLockFieldControls',1)
    assert preserved(emu)[1:]==before[1:]
    assert identity(emu)==ids
    assert tuple(emu.var(v) for v in range(0x40E0,0x4100))==progress
    if choice=='YES': assert_healed(emu)
    else:
        assert health(emu)==tired and preserved(emu)==before
    emu.walk('DOWN',6);emu.walk('RIGHT',4);emu.walk('DOWN',1)
    assert emu.location()==AMIENS

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'reunion-verified',args.legacy)
        tire_party(emu);before=health(emu);talk(emu,'nora')
        assert health(emu)==before and emu.var(0x40E0)==5
        talk(emu,'mira');assert emu.var(0x40E0)==6 and health(emu)==before
        emu.state(ROOT/'test-output/amiens-care-tired.state')
        rest(emu,'NO');rest(emu,'B');rest(emu);rest(emu)
        emu.state(ROOT/'test-output/amiens-care-rested.state')
        inspect(emu,34,511,'amiens-care')
        leave(emu);board(emu);tire_party(emu);rest(emu);relocated(emu)
        cross(emu);reach_post(emu);board(emu);tire_party(emu);rest(emu)
        print('PASS: reunion gate; No/B preserve health; repeat free HP/status/PP care; both return routes',flush=True)
        load_checkpoint(emu,'reunion-complete',args.legacy)
        tire_party(emu);rest(emu)
        print('PASS: existing completed reunion save unlocks care without restarting the quest',flush=True)
        # Six-member health fixture, including a fainted slot, and full Items pocket.
        mon=emu.symbols['gPlayerParty'];sample=bytes(emu.read(mon+j,1) for j in range(100))
        for i in range(1,6):
            for j,value in enumerate(sample):emu.write(mon+i*100+j,value,1)
        emu.write('gPlayerPartyCount',6,1);tire_party(emu)
        emu.write(mon+500+0x56,0,2)
        save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
        for i in range(42):
            emu.write(save+0x310+i*4,13,2);emu.write(save+0x312+i*4,999^key,2)
        rest(emu);assert len(health(emu))==6
        print('PASS: six party slots including fainted Pokemon; full Bag; identities, items and progress preserved',flush=True)
    finally:emu.close()
