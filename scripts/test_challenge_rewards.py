"""Regional guide requirements, one-time rewards, and bag capacity recovery."""
from emulator import Emulator, ROOT
from test_tour import guide, item_count

CANDY = 68

def reach_guide(emu):
    # New trainer stands at (17,18); walk around her on the main path.
    emu.walk('LEFT', 2)
    emu.walk('UP', 20)
    emu.walk('UP', 9)
    emu.walk('RIGHT', 1)

def set_win(emu, trainer, won):
    flag = 0x500 + trainer
    addr = emu.read('gSaveBlock1Ptr') + 0xEE0 + flag // 8
    old = emu.read(addr, 1)
    emu.write(addr, old | (1 << (flag % 8)) if won else old & ~(1 << (flag % 8)), 1)

if __name__ == '__main__':
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        for i, country in enumerate(('england', 'france', 'germany')):
            emu.state(ROOT / f'test-output/challenge-{country}-won.state', True)
            reach_guide(emu)
            ready = ROOT / f'test-output/challenge-{country}-ready.state'
            emu.state(ready)
            # Remove each victory in isolation: neither match alone earns a reward.
            for trainer in (743 + i, 746 + i):
                emu.state(ready, True)
                set_win(emu, trainer, False)
                guide(emu)
                assert emu.var(0x40F8 + i) == 0
                assert item_count(emu, CANDY) == 0
            emu.state(ready, True)
            guide(emu)
            assert emu.var(0x40F8 + i) == 1
            assert item_count(emu, CANDY) == 1
            guide(emu)
            assert item_count(emu, CANDY) == 1
            emu.state(ROOT / f'test-output/challenge-{country}-reward.state')
            # Full pocket fixture: victories must remain claimable after making room.
            emu.state(ready, True)
            bag = emu.read('gSaveBlock1Ptr') + 0x310
            key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
            for slot in range(42):
                emu.write(bag + slot * 4, 13, 2)
                emu.write(bag + slot * 4 + 2, 99 ^ key, 2)
            guide(emu)
            assert emu.var(0x40F8 + i) == 0 and item_count(emu, CANDY) == 0
            emu.state(ROOT / f'test-output/challenge-{country}-pending.state')
            emu.write(bag, 0, 2)
            emu.write(bag + 2, key, 2)
            guide(emu)
            assert emu.var(0x40F8 + i) == 1 and item_count(emu, CANDY) == 1
            print(f'PASS: {country}: both victories required, one reward, repeat safe, full Bag retry', flush=True)
    finally:
        emu.close()
