"""Oranienburg Gym: real leader fight, immediate badge, capacity recovery and UI."""
from emulator import Emulator, ROOT
from test_country import wait_menu, party_species
from test_tour import travel, item_count
from test_england_story import heal_oxford
from test_trainers import defeated, money, fight
from test_navigation import wait_task
from test_shops import confirm_purchase

TM_REWARD = 0x40EF
BADGE = 0x822

def badge(emu):
    return bool(emu.read(emu.read('gSaveBlock1Ptr') + 0xEE0 + BADGE // 8, 1) & (1 << (BADGE % 8)))

def count_pocket(emu, item, offset, slots):
    bag = emu.read('gSaveBlock1Ptr') + offset
    key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
    return sum(emu.read(bag + i*4+2,2)^key for i in range(slots) if emu.read(bag+i*4,2)==item)

def tm_count(emu): return count_pocket(emu,322,0x464,58)

def enter(emu):
    assert emu.location() == (43,20,15,14), emu.location()
    emu.walk('UP',5);emu.frames(180)
    assert emu.location()==(43,26,6,14),emu.location()

def approach(emu):
    emu.walk('UP',8)
    assert emu.location()==(43,26,6,6),emu.location()

def leader(emu):
    assert emu.location()==(43,26,6,6),emu.location()
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
            wait_task(emu,'Task_BagMenu_HandleInput')
            bag=emu.symbols['gBagMenuState']
            for _ in range(5):
                if emu.read(bag+6,2)==0:break
                emu.press('LEFT',90)
            assert emu.read(bag+6,2)==0
            save=emu.read('gSaveBlock1Ptr')
            target=next(i for i in range(42) if emu.read(save+0x310+i*4,2)==13)
            for _ in range(45):
                current=emu.read(bag+8,2)+emu.read(bag+14,2)
                if current==target:break
                emu.press('DOWN' if current<target else 'UP')
            assert current==target
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
    emu.screenshot(ROOT/'test-output/electric-gym-fight-end.png')
    assert not emu.in_battle(),'Gym battle stuck'
    emu.frames(180);emu.finish_dialogue()

if __name__=='__main__':
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        emu.state(ROOT/'test-output/germany-complete.state',True)
        emu.walk('RIGHT',6);travel(emu,5)
        # Buy supplies with earned money; earlier Gyms exhausted the starting Potions.
        emu.walk('RIGHT',7);emu.walk('UP',5);emu.frames(180)
        emu.walk('UP',1);emu.walk('LEFT',3);emu.press('UP');emu.press('A',180)
        wait_menu(emu,'Task_ShopMenu');emu.press('A',180);wait_menu(emu,'Task_BuyMenu')
        before_cash=money(emu);before_potions=item_count(emu,13)
        emu.press('DOWN');confirm_purchase(emu,5);emu.press('A',180)
        wait_menu(emu,'Task_ReturnToItemListAfterItemPurchase')
        assert money(emu)==before_cash-1500 and item_count(emu,13)==before_potions+5
        emu.press('A',90);emu.press('B',180);wait_menu(emu,'Task_ShopMenu')
        emu.press('B',180);emu.finish_dialogue()
        emu.walk('RIGHT',3);emu.walk('DOWN',2);emu.frames(180)
        emu.walk('DOWN',4);emu.walk('LEFT',7)
        # Heal through the clinic's normal dialogue before entering.
        emu.walk('LEFT',10);emu.walk('UP',5);emu.frames(180)
        emu.walk('UP',4);emu.walk('RIGHT',1);emu.press('UP');emu.press('A',180);emu.finish_dialogue()
        emu.walk('DOWN',5);emu.frames(180)
        emu.walk('RIGHT',9);emu.walk('DOWN',4);enter(emu)
        entrance=ROOT/'test-output/electric-gym-entrance.state';emu.state(entrance)
        emu.walk('UP',1);emu.walk('RIGHT',1);emu.press('UP');emu.press('A',180);emu.finish_dialogue()
        emu.state(entrance,True);emu.walk('DOWN',2);emu.frames(180)
        assert emu.location()==(43,20,15,10),emu.location()
        emu.state(entrance,True);approach(emu)
        ready=ROOT/'test-output/electric-gym-ready.state';emu.state(ready)
        # Boundary fixtures: every unfinished survey state must stay locked.
        for stage in range(3):
            emu.state(ready,True)
            emu.write(emu.read('gSaveBlock1Ptr')+0x1000+(0xFF)*2,stage,2)
            complete_talk(emu)
            assert not badge(emu) and not defeated(emu,9)
            assert not emu.task_active('Task_YesNoMenu_HandleInput')
        emu.state(ready,True)
        print('PASS: Gym route, guide, exit and all three unfinished delivery gates',flush=True)
        leader(emu);wait_menu(emu,'Task_YesNoMenu_HandleInput');emu.frames(60)
        prompt=ROOT/'test-output/electric-gym-prompt.state';emu.state(prompt)
        before=money(emu)
        for decline in ('B','NO'):
            emu.state(prompt,True)
            if decline=='NO': emu.press('DOWN');emu.press('A',180)
            else: emu.press('B',180)
            emu.finish_dialogue()
            assert not badge(emu) and not defeated(emu,9) and money(emu)==before
        emu.state(prompt,True);emu.press('A',180)
        for _ in range(30):
            if emu.in_battle(): break
            emu.press('A',90)
        assert emu.in_battle()
        emu.frames(300)
        assert emu.read('gTrainerBattleOpponent_A',2)==752
        assert tuple(party_species(emu,'gEnemyParty',i) for i in range(2))==(100,25)
        battle=ROOT/'test-output/electric-gym-battle.state';emu.state(battle)
        emu.screenshot(ROOT/'test-output/electric-gym-battle.png')
        gym_fight(emu)
        assert defeated(emu,9) and badge(emu),'Win must award badge immediately'
        assert tm_count(emu)==1 and emu.var(TM_REWARD)==1
        assert count_pocket(emu,364,0x3B8,30)==1,'Missing TM Case'
        assert money(emu)>before
        prize=money(emu)
        complete_talk(emu)
        assert tm_count(emu)==1 and money(emu)==prize
        emu.state(ROOT/'test-output/electric-gym-complete.state')
        print('PASS: leader declines, real Electric-team victory, immediate badge, TM Case/TM34, no repeat payout',flush=True)

        # A saturated TM stack and a full Key Items pocket are separate fixtures.
        for case in ('tm','key'):
            emu.state(battle,True)
            save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
            if case=='tm':
                emu.write(save+0x46C,322,2);emu.write(save+0x46E,999^key,2)
            else:
                for i in range(30):
                    emu.write(save+0x3B8+i*4,360,2);emu.write(save+0x3BA+i*4,1^key,2)
            gym_fight(emu)
            assert badge(emu) and defeated(emu,9) and emu.var(TM_REWARD)==0
            emu.state(ROOT/f'test-output/electric-gym-pending-{case}.state')
            save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
            if case=='tm':
                emu.write(save+0x46E,998^key,2)
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
        assert emu.location()[:2]==(43,23),emu.location()
        assert not badge(emu) and not defeated(emu,9) and emu.var(TM_REWARD)==0
        emu.walk('DOWN',5);emu.frames(180)
        emu.walk('RIGHT',9);emu.walk('UP',1);emu.frames(180)
        assert emu.location()==(43,26,6,14),emu.location()
        approach(emu);leader(emu);wait_menu(emu,'Task_YesNoMenu_HandleInput');emu.frames(60)
        emu.press('B',180);emu.finish_dialogue()
        assert not badge(emu) and not defeated(emu,9)
        print('PASS: Gym loss heals in Oranienburg without badge or reward; leader can be challenged again',flush=True)
    finally: emu.close()


