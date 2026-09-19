"""Germany courier mission: real travel, gates, delivery, reward and retries."""
from emulator import Emulator, ROOT
from test_tour import travel, item_count
from test_country import wait_menu
from test_france_story import npc, talk
from test_oxford_gym import badge as badge1
from test_chantilly_gym import badge as badge2

STORY=0x40FF
MAGNET=208

def leave_gym(emu):
    assert emu.location()==(43,25,8,7),emu.location()
    for direction,tiles in [('RIGHT',4),('DOWN',3),('LEFT',8),('DOWN',3),('RIGHT',5),('DOWN',3),('LEFT',1),('DOWN',4)]:
        emu.walk(direction,tiles)
    emu.frames(180)
    assert emu.location()==(43,16,15,10),emu.location()
    emu.walk('DOWN',4);emu.walk('RIGHT',1)

def next_town(emu,dest):
    emu.walk('RIGHT',6);travel(emu,dest);emu.walk('LEFT',6)

def snapshot(emu,stage):
    emu.state(ROOT/f'test-output/germany-{stage}.state')

if __name__=='__main__':
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        emu.state(ROOT/'test-output/water-gym-complete.state',True)
        leave_gym(emu);travel(emu,2);emu.walk('LEFT',6)
        ready=ROOT/'test-output/germany-ready.state';emu.state(ready)
        assert badge1(emu) and badge2(emu) and emu.var(STORY)==0
        # Each badge is independently required; test fixture clears one at a time.
        for flag in (0x820,0x821):
            emu.state(ready,True);addr=emu.read('gSaveBlock1Ptr')+0xEE0+flag//8
            emu.write(addr,emu.read(addr,1)&~(1<<(flag%8)),1)
            talk(emu);assert emu.var(STORY)==0 and item_count(emu,MAGNET)==0
        emu.state(ready,True)
        next_town(emu,5);talk(emu)
        assert emu.var(STORY)==0 and item_count(emu,MAGNET)==0
        next_town(emu,2)
        npc(emu);wait_menu(emu,'Task_YesNoMenu_HandleInput')
        prompt=ROOT/'test-output/germany-prompt.state';emu.state(prompt)
        for decline in ('B','NO'):
            emu.state(prompt,True)
            if decline=='NO':emu.press('DOWN');emu.press('A',180)
            else:emu.press('B',180)
            emu.finish_dialogue();assert emu.var(STORY)==0
        emu.state(prompt,True);emu.press('A',180);emu.finish_dialogue()
        assert emu.var(STORY)==1
        snapshot(emu,'active');talk(emu)
        assert emu.var(STORY)==1 and item_count(emu,MAGNET)==0
        print('PASS: each badge required, Karl cannot start quest, No/B declines, acceptance and directions',flush=True)
        next_town(emu,5);talk(emu)
        assert emu.var(STORY)==2 and item_count(emu,MAGNET)==0
        snapshot(emu,'delivered');talk(emu);assert emu.var(STORY)==2
        next_town(emu,2);snapshot(emu,'report')
        talk(emu);assert emu.var(STORY)==3 and item_count(emu,MAGNET)==1
        snapshot(emu,'complete');talk(emu);assert item_count(emu,MAGNET)==1
        next_town(emu,5);talk(emu)
        assert emu.var(STORY)==3 and item_count(emu,MAGNET)==1
        assert badge1(emu) and badge2(emu) and emu.var(0x40FD)==6
        print('PASS: normal trains deliver parts and return report; exactly one Magnet; both NPC repeats safe',flush=True)
        emu.state(ROOT/'test-output/germany-report.state',True)
        save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
        for i in range(42):
            emu.write(save+0x310+i*4,13,2);emu.write(save+0x312+i*4,999^key,2)
        talk(emu);assert emu.var(STORY)==2 and item_count(emu,MAGNET)==0
        snapshot(emu,'pending')
        emu.write(save+0x310,0,2);emu.write(save+0x312,key,2)
        talk(emu);talk(emu)
        assert emu.var(STORY)==3 and item_count(emu,MAGNET)==1
        emu.frames(60);emu.screenshot(ROOT/'test-output/germany-complete.png')
        print('PASS: full Items pocket keeps report pending; free space grants one reward',flush=True)
    finally:emu.close()
