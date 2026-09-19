"""Visit both French survey sites in either order and deliver the reviewed report."""
from emulator import Emulator,ROOT
from test_tour import travel,item_count
from test_country import wait_menu
from test_oxford_gym import badge

SURVEY=0x40FD
SEED=205

def npc(emu):
    assert emu.location()[2:]==(10,14),emu.location()
    emu.press('DOWN');emu.press('A',180)

def talk(emu):
    npc(emu);emu.finish_dialogue()
    assert not emu.task_active('Task_YesNoMenu_HandleInput')

def marker(emu):
    emu.press('UP');emu.press('A',180);emu.finish_dialogue()
    assert not emu.read('sLockFieldControls',1)

def gardens(emu,checkpoint=False):
    assert emu.location()==(43,4,16,14),emu.location()
    emu.walk('LEFT',1);emu.walk('UP',15);emu.walk('UP',6);emu.walk('LEFT',2)
    assert emu.location()==(43,5,13,17),emu.location()
    marker(emu)
    if checkpoint: emu.state(ROOT/'test-output/france-gardens.state')
    state=emu.var(SURVEY);marker(emu);assert emu.var(SURVEY)==state
    emu.walk('RIGHT',2);emu.walk('DOWN',7);emu.walk('DOWN',14);emu.walk('RIGHT',1)
    assert emu.location()==(43,4,16,14),emu.location()

def forest(emu,checkpoint=False):
    assert emu.location()==(43,16,16,14),emu.location()
    emu.walk('LEFT',1);emu.walk('DOWN',10);emu.walk('DOWN',21);emu.walk('LEFT',2)
    assert emu.location()==(43,17,13,21),emu.location()
    marker(emu)
    if checkpoint: emu.state(ROOT/'test-output/france-forest.state')
    state=emu.var(SURVEY);marker(emu);assert emu.var(SURVEY)==state
    emu.walk('RIGHT',2);emu.walk('UP',22);emu.walk('UP',9);emu.walk('RIGHT',1)
    assert emu.location()==(43,16,16,14),emu.location()

def to_paris_from_gym(emu):
    emu.walk('DOWN',8);emu.walk('DOWN',2);emu.frames(180)
    emu.walk('DOWN',4);emu.walk('RIGHT',1);travel(emu,1)

if __name__=='__main__':
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        # A France start cannot skip the first badge, but travel stays open.
        emu.state(ROOT/'test-output/start-france.state',True)
        emu.walk('LEFT',5);talk(emu)
        assert emu.var(SURVEY)==0 and not badge(emu)
        emu.walk('RIGHT',6);gardens(emu)
        assert emu.var(SURVEY)==0
        travel(emu,4);forest(emu);emu.walk('LEFT',6);talk(emu)
        assert emu.var(SURVEY)==0 and item_count(emu,SEED)==0
        print('PASS: first badge required; pre-quest markers and Remy preserve unstarted survey and travel',flush=True)

        emu.state(ROOT/'test-output/gym-complete.state',True)
        to_paris_from_gym(emu);emu.walk('LEFT',6);npc(emu)
        wait_menu(emu,'Task_YesNoMenu_HandleInput')
        prompt=ROOT/'test-output/france-offer.state';emu.state(prompt)
        for decline in ('B','NO'):
            emu.state(prompt,True)
            if decline=='NO':emu.press('DOWN');emu.press('A',180)
            else:emu.press('B',180)
            emu.finish_dialogue();assert emu.var(SURVEY)==0
        emu.state(prompt,True);emu.press('A',180);emu.finish_dialogue()
        assert emu.var(SURVEY)==1 and badge(emu)
        active=ROOT/'test-output/france-active.state';emu.state(active)
        talk(emu);assert emu.var(SURVEY)==1
        print('PASS: earned badge unlocks offer; No/B decline, acceptance and repeat directions work',flush=True)

        for order in (('gardens','forest'),('forest','gardens')):
            emu.state(active,True);emu.walk('RIGHT',6)
            for i,site in enumerate(order):
                dest=1 if site=='gardens' else 4
                if emu.location()[1]//4!=dest:travel(emu,dest)
                (gardens if site=='gardens' else forest)(emu,checkpoint=(i==0))
                assert emu.var(SURVEY)==(4 if i else (2 if site=='gardens' else 3))
                if i==0:
                    # Neither reviewer nor reward-giver can skip the second site.
                    if dest!=4:travel(emu,4)
                    emu.walk('LEFT',6);talk(emu);emu.walk('RIGHT',6)
                    assert emu.var(SURVEY)==(2 if site=='gardens' else 3)
                    travel(emu,1);emu.walk('LEFT',6);talk(emu);emu.walk('RIGHT',6)
                    assert item_count(emu,SEED)==0
            # Paris requires Remy's review even when both observations are done.
            if emu.location()[1]//4!=1:travel(emu,1)
            emu.walk('LEFT',6);talk(emu);emu.walk('RIGHT',6)
            assert emu.var(SURVEY)==4 and item_count(emu,SEED)==0
            travel(emu,4);emu.walk('LEFT',6)
            emu.state(ROOT/'test-output/france-both.state')
            talk(emu);assert emu.var(SURVEY)==5
            talk(emu);assert emu.var(SURVEY)==5
            emu.walk('RIGHT',6);travel(emu,1);emu.walk('LEFT',6)
            emu.state(ROOT/'test-output/france-report.state')
            talk(emu);assert emu.var(SURVEY)==6 and item_count(emu,SEED)==1
            talk(emu);assert item_count(emu,SEED)==1
            assert emu.var(0x40FB)==2 and badge(emu) and emu.var(0x40F0)==1
            emu.state(ROOT/'test-output/france-complete.state')
            # Revisit all participants and markers after completion: no rollback.
            emu.walk('RIGHT',6);gardens(emu);travel(emu,4);forest(emu)
            emu.walk('LEFT',6);talk(emu)
            assert emu.var(SURVEY)==6 and item_count(emu,SEED)==1
            print(f'PASS: {order}: two unique notes, no early review/reward, reviewed report, one seed, repeat visits safe',flush=True)

        emu.state(ROOT/'test-output/france-report.state',True)
        save=emu.read('gSaveBlock1Ptr');key=emu.read(emu.read('gSaveBlock2Ptr')+0xF20,2)
        for i in range(42):
            emu.write(save+0x310+i*4,13,2);emu.write(save+0x312+i*4,999^key,2)
        talk(emu);assert emu.var(SURVEY)==5 and item_count(emu,SEED)==0
        emu.state(ROOT/'test-output/france-pending.state')
        emu.write(save+0x310,0,2);emu.write(save+0x312,key,2)
        talk(emu);assert emu.var(SURVEY)==6 and item_count(emu,SEED)==1
        talk(emu);assert item_count(emu,SEED)==1
        print('PASS: full Items pocket preserves reviewed report; making room permits exactly one reward',flush=True)
    finally:emu.close()
