"""Exercise every victory callback using explicit accelerated battle fixtures.

Battle HP and moves are injected only to test chapter/badge transitions quickly.
This is not a natural-level balancing playthrough.
"""
from emulator import Emulator,ROOT
from test_country import wait_menu
from test_shadow_runtime import go,talk,monfield
from test_landmark_cases import save
import json
import sys
START_STAGE=int(sys.argv[1]) if len(sys.argv)>1 else 0
C=json.loads((ROOT/'data/shadow-campaign.json').read_text())['chapters']
e=Emulator(ROOT/'pokefirered.gba')
try:
    e.state(ROOT/'test-output/start-germany.state',True)
    m=json.loads((ROOT/'data/maps/EuropeBerlin/map.json').read_text());o=next(o for o in m['object_events'] if o['script']=='Shadow_Entrance');talk(e,(o['x'],o['y']+1))
    if START_STAGE: e.state(ROOT/f'test-output/eclipse-stage-{START_STAGE:02d}.state',True)
    for stage,c in enumerate(C[START_STAGE:],START_STAGE):
        assert e.var(0x408C)==stage and e.location()[:2]==(44,stage*2)
        talk(e,(2,4))
        e.state(ROOT/f'test-output/eclipse-stage-{stage:02d}.state')
        go(e,(6,4));e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A',180)
        for _ in range(30):
            if e.in_battle():break
            e.press('A',60)
        assert e.in_battle(),(stage,'battle did not begin')
        e.frames(240)
        if c['kind'] in ('enemy','nazi'):
            assert monfield(e,0,3,8,'gEnemyParty')&(1<<27),(stage,'enemy shadow bit')
        e.screenshot(ROOT/f'test-output/eclipse-battle-{stage:02d}.png')
        action=e.symbols['HandleInputChooseAction']&~1;move=e.symbols['HandleInputChooseMove']&~1
        for turn in range(1800):
            if not e.in_battle():break
            b=e.symbols['gBattleMons']
            # Apply fixtures only while a command menu is waiting. Rewriting HP
            # during the faint animation would incorrectly revive the opponent.
            fn=e.read('gBattlerControllerFuncs')&~1
            if fn in (action,move):
                hp=e.read(e.symbols['gPlayerParty']+0x58,2)
                e.write(b+0x28,hp,2);e.write(b+0x2c,hp,2)
                e.write(b+4,30000,2);e.write(b+6,30000,2);e.write(b+10,30000,2)
                e.write(b+88+0x28,1,2)
                e.write(b+0xc,82,2);e.write(b+0x24,40,1)
                e.press('UP',2);e.press('LEFT',2)
            opcode=e.read(e.read('gBattlescriptCurrInstr'),1)
            if opcode==0x5a:e.press('B',30)
            else:e.press('A',30)
        else:
            e.screenshot(ROOT/'test-output/eclipse-stalled.png')
            e.state(ROOT/'test-output/eclipse-stalled.state')
            raise AssertionError((stage,'battle stalled',hex(e.read('gBattlerControllerFuncs')),hex(e.read('gBattlescriptCurrInstr')),e.read('gBattleOutcome',1)))
        for _ in range(40):e.press('B',60);e.press('A',60)
        e.finish_dialogue();e.frames(240)
        assert e.var(0x408C)==stage+1,(stage,'victory did not advance',e.var(0x408C),e.location())
        print('PASS: chapter',stage+1,c['city'],'actual battle victory callback',flush=True)
        if stage<len(C)-1:talk(e,(10,4))
    flags=e.read('gSaveBlock1Ptr')+0xEE0
    source=(ROOT/'include/constants/flags.h').read_text()
    import re
    for i in range(1,9):
        flag=0x800+0x20+i-1
        assert e.read(flags+flag//8,1)&(1<<(flag%8)),i
    flag=0x800+0x2C
    assert e.read(flags+flag//8,1)&(1<<(flag%8))
    e.screenshot(ROOT/'test-output/eclipse-ending.png')
    save(e,'eclipse-finished')
    print('PASS: all eight native badge flags and game-clear flag after 21 battle victories',flush=True)
finally:e.close()
