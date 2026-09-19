"""Verify the Gym badge on the Trainer Card, TM Case access, and Gym map context."""
from emulator import Emulator,ROOT
from test_navigation import wait_task
from test_chantilly_gym import badge,tm_count

def start_action(emu, action):
    emu.press('START',60)
    count=emu.read('sNumStartMenuItems',1)
    order=[emu.read(emu.symbols['sStartMenuOrder']+i,1) for i in range(count)]
    cursor=emu.read('sStartMenuCursorPos',1)
    for _ in range((order.index(action)-cursor)%count): emu.press('DOWN')
    emu.press('A',180)

def open_key_item(emu,item):
    start_action(emu,2)
    wait_task(emu,'Task_BagMenu_HandleInput')
    bag=emu.symbols['gBagMenuState']
    for _ in range(3):
        if emu.read(bag+6,2)==1: break
        emu.press('RIGHT',90)
    assert emu.read(bag+6,2)==1
    save=emu.read('gSaveBlock1Ptr')
    target=next(i for i in range(30) if emu.read(save+0x3B8+i*4,2)==item)
    for _ in range(35):
        current=emu.read(bag+10,2)+emu.read(bag+16,2)
        if current==target: break
        emu.press('DOWN' if current<target else 'UP')
    assert current==target
    emu.press('A',90);emu.press('A',180)

if __name__=='__main__':
    emu=Emulator(ROOT/'pokefirered.gba')
    try:
        for state,expected in [('water-gym-entrance',0),('water-gym-complete',1)]:
            emu.state(ROOT/f'test-output/{state}.state',True)
            start_action(emu,3);wait_task(emu,'Task_TrainerCard');emu.frames(180)
            card=emu.read('sTrainerCardDataPtr')
            assert [emu.read(card+17+i,1) for i in range(8)]==[1,expected,0,0,0,0,0,0]
            emu.screenshot(ROOT/f'test-output/{state}-card.png')
            emu.press('B',180);emu.press('B',90)
            assert emu.location()[:2]==(43,25)
        emu.state(ROOT/'test-output/water-gym-complete.state',True)
        open_key_item(emu,361)
        wait_task(emu,'Task_EuropeMap')
        assert emu.read('sEuropeMapCurrent',1)==4
        emu.press('B',180);emu.press('B',180);emu.press('B',90)
        assert not emu.read('sLockFieldControls',1)
        assert emu.location()==(43,25,8,7)
        emu.state(ROOT/'test-output/water-gym-complete.state',True)
        open_key_item(emu,364);emu.frames(180)
        assert emu.read('sTMCaseDynamicResources')!=0
        assert tm_count(emu)==1
        emu.screenshot(ROOT/'test-output/water-gym-tm-case.png')
        emu.press('B',180);emu.press('B',180);emu.press('B',90)
        assert emu.location()==(43,25,8,7) and badge(emu)
        assert not emu.read('sLockFieldControls',1)
        print('PASS: Trainer Card shows both earned badges; Gym map shows Chantilly; awarded TM opens in TM Case',flush=True)
    finally: emu.close()

