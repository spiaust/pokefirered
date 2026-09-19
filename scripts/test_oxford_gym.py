"""Oxford Gym: real leader fight, immediate badge, capacity recovery and UI."""
from emulator import Emulator, ROOT
from test_country import wait_menu, party_species
from test_tour import travel, item_count
from test_england_story import heal_oxford
from test_trainers import defeated, money, fight
from test_navigation import wait_task

TM_REWARD = 0x40FC
BADGE = 0x820

def badge(emu):
    return bool(emu.read(emu.read('gSaveBlock1Ptr') + 0xEE0 + BADGE // 8, 1) & (1 << (BADGE % 8)))

def count_pocket(emu, item, offset, slots):
    bag = emu.read('gSaveBlock1Ptr') + offset
    key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
    return sum(emu.read(bag + i*4+2,2)^key for i in range(slots) if emu.read(bag+i*4,2)==item)

def tm_count(emu): return count_pocket(emu,327,0x464,58)

def enter(emu):
    assert emu.location() == (43,12,15,14), emu.location()
    emu.walk('UP',5);emu.frames(180)
    assert emu.location()==(43,24,6,14),emu.location()

def leader(emu):
    assert emu.location()==(43,24,6,6),emu.location()
    emu.press('UP');emu.press('A',180)

def complete_talk(emu):
    leader(emu);emu.finish_dialogue()
    assert not emu.in_battle()

def gym_fight(emu):
    action=next(int(line.split()[0],16) for line in (ROOT/'pokefirered.sym').read_text().splitlines()
                if line.split()[-1:]==['HandleInputChooseAction'])
    mon=emu.symbols['gBattleMons']
    for _ in range(1100):
        if not emu.in_battle(): break
        fn=emu.read('gBattlerControllerFuncs') & ~1
        move=emu.symbols['HandleInputChooseMove']
        hp=emu.read(mon+0x28,2)
        if fn in (action,move) and hp<=emu.read(mon+0x2C,2)//2+3 and item_count(emu,13):
            if fn==move: emu.press('B')
            emu.press('UP');emu.press('LEFT');emu.press('RIGHT');emu.press('A',180)
            emu.press('A',90);emu.press('A',180);emu.press('A',180)
        else:
            if fn==action:
                emu.press('UP');emu.press('LEFT')
            elif fn==move:
                moves=[emu.read(mon+0xC+i*2,2) for i in range(4)]
                priorities=[22,71,145,55]
                if not emu.read(emu.symbols['gStatuses3']+4)&4:
                    priorities.append(73)
                priorities.append(33)
                slot=next((moves.index(m) for m in priorities if m in moves and emu.read(mon+0x24+moves.index(m),1)),0)
                emu.press('UP');emu.press('LEFT')
                if slot & 1: emu.press('RIGHT')
                if slot & 2: emu.press('DOWN')
            emu.press('A',30)
    emu.screenshot(ROOT/'test-output/gym-fight-end.png')
    assert not emu.in_battle(),'Gym battle stuck'
    emu.frames(180);emu.finish_dialogue()

if __name__=='__main__':
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        # Visitors can enter, hear advice and leave before the story is done.
        emu.state(ROOT/'test-output/start-england.state',True)
        emu.walk('RIGHT',1);travel(emu,3);emu.walk('LEFT',1)
        enter(emu)
        entrance=ROOT/'test-output/gym-entrance.state';emu.state(entrance)
        emu.walk('UP',1);emu.walk('RIGHT',1);emu.press('UP');emu.press('A',180);emu.finish_dialogue()
        emu.walk('LEFT',1);emu.walk('UP',7)
        complete_talk(emu)
        assert not badge(emu) and not defeated(emu,7)
        assert not emu.task_active('Task_YesNoMenu_HandleInput')
        emu.state(entrance,True);emu.walk('DOWN',2);emu.frames(180)
        assert emu.location()==(43,12,15,10),emu.location()
        emu.walk('DOWN',4)
        print('PASS: Gym entrance, guide, locked leader and exit before field-study completion',flush=True)

        # Winning the rival match alone is not enough: the report must be delivered.
        emu.state(ROOT/'test-output/story-report-ready.state',True)
        emu.walk('RIGHT',6);travel(emu,3);emu.walk('LEFT',1);enter(emu)
        emu.walk('UP',8);complete_talk(emu)
        assert not badge(emu) and not defeated(emu,7) and emu.var(0x40FB)==1
        assert not emu.task_active('Task_YesNoMenu_HandleInput')
        print('PASS: leader waits for the report even after the rival victory',flush=True)

        emu.state(ROOT/'test-output/story-complete.state',True)
        emu.walk('RIGHT',6);travel(emu,3);heal_oxford(emu)
        emu.walk('RIGHT',5);enter(emu)
        emu.walk('UP',8)
        assert not badge(emu)
        leader(emu);wait_menu(emu,'Task_YesNoMenu_HandleInput')
        prompt=ROOT/'test-output/gym-prompt.state';emu.state(prompt)
        before=money(emu)
        for decline in ('B','NO'):
            emu.state(prompt,True)
            if decline=='NO': emu.press('DOWN');emu.press('A',180)
            else: emu.press('B',180)
            emu.finish_dialogue()
            assert not badge(emu) and not defeated(emu,7) and money(emu)==before
        emu.state(prompt,True);emu.press('A',180)
        for _ in range(30):
            if emu.in_battle(): break
            emu.press('A',90)
        assert emu.in_battle()
        emu.frames(300)
        assert emu.read('gTrainerBattleOpponent_A',2)==750
        assert tuple(party_species(emu,'gEnemyParty',i) for i in range(2))==(74,95)
        battle=ROOT/'test-output/gym-battle.state';emu.state(battle)
        emu.screenshot(ROOT/'test-output/gym-battle.png')
        gym_fight(emu)
        assert defeated(emu,7) and badge(emu),'Win must award badge immediately'
        assert tm_count(emu)==1 and emu.var(TM_REWARD)==1
        assert count_pocket(emu,364,0x3B8,30)==1,'Missing TM Case'
        assert money(emu)>before
        prize=money(emu)
        complete_talk(emu)
        assert tm_count(emu)==1 and money(emu)==prize
        emu.state(ROOT/'test-output/gym-complete.state')
        print('PASS: leader declines, real Rock-team victory, immediate badge, TM Case/TM39, no repeat payout',flush=True)

        # A saturated TM stack and a full Key Items pocket are separate fixtures.
        for case in ('tm','key'):
            emu.state(battle,True)
            save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
            if case=='tm':
                emu.write(save+0x464,327,2);emu.write(save+0x466,999^key,2)
                emu.write(save+0x3B8+12,364,2);emu.write(save+0x3BA+12,1^key,2)
            else:
                for i in range(30):
                    emu.write(save+0x3B8+i*4,360,2);emu.write(save+0x3BA+i*4,1^key,2)
            gym_fight(emu)
            assert badge(emu) and defeated(emu,7) and emu.var(TM_REWARD)==0
            emu.state(ROOT/f'test-output/gym-pending-{case}.state')
            save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
            if case=='tm':
                emu.write(save+0x466,998^key,2)
            else:
                emu.write(save+0x3B8,0,2);emu.write(save+0x3BA,key,2)
            complete_talk(emu)
            assert emu.var(TM_REWARD)==1 and tm_count(emu)==(999 if case=='tm' else 1)
            complete_talk(emu)
            assert tm_count(emu)==(999 if case=='tm' else 1)
            print(f'PASS: full {case} capacity keeps badge and pending TM; retry awards once',flush=True)

        emu.state(battle,True)
        mon=emu.symbols['gBattleMons'];party=emu.symbols['gPlayerParty']
        emu.write(party+0x56,1,2);emu.write(mon+0x28,1,2);emu.write(mon+0x04,1,2);emu.write(mon+0x02,1,2)
        fight(emu)
        assert emu.location()[:2]==(43,15),emu.location()
        assert not badge(emu) and not defeated(emu,7) and emu.var(TM_REWARD)==0
        emu.walk('DOWN',5);emu.frames(180)
        emu.walk('RIGHT',9);emu.walk('UP',1);emu.frames(180)
        assert emu.location()==(43,24,6,14),emu.location()
        emu.walk('UP',8);leader(emu);wait_menu(emu,'Task_YesNoMenu_HandleInput')
        emu.press('B',180);emu.finish_dialogue()
        assert not badge(emu) and not defeated(emu,7)
        print('PASS: Gym loss heals in Oxford without badge or reward; leader can be challenged again',flush=True)
    finally: emu.close()

