"""Amiens reunion: report ordering, verification, relocation and journal."""
import argparse
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_amiens import AMIENS, board, leave, reach_post
from test_garden import choose
from test_time import preserved, cross
from test_journal import inspect
STORY = 0x40E0

def visible(emu, local_id):
    for i in range(16):
        obj = emu.symbols['gObjectEvents'] + i * 36
        if (emu.read(obj, 1) & 1 and emu.read(obj + 8, 1) == local_id
                and emu.read(obj + 9, 1) == 33 and emu.read(obj + 10, 1) == 43):
            return True
    return False

def talk(emu, who, choice='YES'):
    assert emu.location() == AMIENS
    paths = {'nora': [('UP',1),('LEFT',4),('UP',6)],
             'mira': [('RIGHT',3),('UP',7)], 'porter': [('RIGHT',8),('UP',3)],
             'waiting': [('RIGHT',9),('UP',3)], 'home': [('RIGHT',4),('UP',7)]}
    path = paths[who]
    for direction, tiles in path: emu.walk(direction, tiles)
    if who in ('waiting', 'home'):
        assert visible(emu, 6 if who == 'waiting' else 7)
    before = preserved(emu)
    emu.press('UP'); emu.press('A',180)
    assert emu.read('sLockFieldControls',1), (who, emu.location())
    if who == 'nora' and emu.var(STORY) == 0 and emu.var(0x40E1) == 4:
        choose(emu,choice)
    elif who == 'nora' and emu.var(STORY) == 6:
        choose(emu, 'B')  # Reunion regression must not heal the party.
    else:
        emu.finish_dialogue()
    assert preserved(emu) == before
    opposite={'UP':'DOWN','RIGHT':'LEFT','LEFT':'RIGHT'}
    for direction, tiles in reversed(path): emu.walk(opposite[direction],tiles)
    assert emu.location() == AMIENS

def relocated(emu):
    emu.walk('RIGHT',4); emu.walk('UP',7)
    assert visible(emu,7)
    emu.screenshot(ROOT/'test-output/reunion-home.png')
    emu.walk('DOWN',7); emu.walk('RIGHT',5); emu.walk('UP',3)
    assert not visible(emu,6)
    emu.walk('DOWN',3); emu.walk('LEFT',9)

def finish_reunion(emu):
    if emu.location() != AMIENS:
        reach_post(emu); board(emu)
    if emu.var(STORY) == 0: talk(emu,'nora')
    if emu.var(STORY) in (1,3): talk(emu,'mira')
    if emu.var(STORY) == 2: talk(emu,'porter')
    if emu.var(STORY) == 4: talk(emu,'nora')
    if emu.var(STORY) == 5: talk(emu,'mira')
    assert emu.var(STORY) == 6
    relocated(emu)

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(emu,'amiens-arrival',args.legacy)
        talk(emu,'mira');talk(emu,'porter');talk(emu,'nora')
        assert emu.var(STORY)==0 and emu.var(0x40E1)==2
        load_checkpoint(emu,'amiens-complete',args.legacy)
        for choice in ('NO','B'):
            talk(emu,'nora',choice);assert emu.var(STORY)==0
        talk(emu,'nora');assert emu.var(STORY)==1
        emu.state(ROOT/'test-output/reunion-active.state');inspect(emu,29,255,'reunion-active')
        talk(emu,'waiting');talk(emu,'mira');talk(emu,'mira');talk(emu,'nora')
        assert emu.var(STORY)==2
        emu.state(ROOT/'test-output/reunion-mira.state');inspect(emu,30,255,'reunion-mira')
        talk(emu,'porter');assert emu.var(STORY)==4
        emu.state(ROOT/'test-output/reunion-both.state');inspect(emu,32,255,'reunion-both')
        talk(emu,'mira');talk(emu,'porter');assert emu.var(STORY)==4
        talk(emu,'nora');talk(emu,'nora');assert emu.var(STORY)==5
        emu.state(ROOT/'test-output/reunion-verified.state');inspect(emu,33,255,'reunion-verified')
        cross(emu);emu.state(ROOT/'test-output/reunion-returned.state')
        finish_reunion(emu)
        emu.state(ROOT/'test-output/reunion-complete.state');inspect(emu,34,511,'reunion-complete')
        for who in ('home','nora','mira','porter'): talk(emu,who)
        leave(emu);board(emu);relocated(emu);assert emu.var(STORY)==6
        emu.state(ROOT/'test-output/reunion-active.state',load=True)
        talk(emu,'porter');talk(emu,'porter');talk(emu,'nora');assert emu.var(STORY)==3
        emu.state(ROOT/'test-output/reunion-porter.state');inspect(emu,31,255,'reunion-porter')
        leave(emu);board(emu);assert emu.var(STORY)==3
        finish_reunion(emu)
        print('PASS: arrival gate, No/B, both report orders, repeated witnesses, verification and reunion')
        print('PASS: six journal leads, ninth milestone, both returns and persistent Meowth relocation')
    finally: emu.close()
