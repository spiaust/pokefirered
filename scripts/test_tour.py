"""Complete the tour in every order using guides and actual train journeys."""
from itertools import permutations
from emulator import Emulator, ROOT
from rail_test_helpers import complete_journey

COUNTRIES = ("england", "france", "germany")
STAMPS = (0x40F2, 0x40F3, 0x40F4)
REWARDED = 0x40F5
EXP_SHARE = 182


def item_count(emu, item):
    bag = emu.read("gSaveBlock1Ptr") + 0x310
    key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20, 2)
    return sum(emu.read(bag + i * 4 + 2, 2) ^ key
               for i in range(42) if emu.read(bag + i * 4, 2) == item)


def guide(emu):
    # Stand immediately north of the stationary city guide.
    assert emu.location()[2:] == (16, 14), emu.location()
    emu.press("DOWN")
    emu.press("A", 180)
    assert emu.read("sLockFieldControls", 1), "Guide did not start dialogue"
    emu.finish_dialogue()


def travel(emu, destination):
    emu.walk("RIGHT", 7)
    emu.walk("UP", 5)
    emu.frames(180)
    emu.walk("UP", 1)
    emu.walk("RIGHT", 3)
    emu.press("UP")
    emu.press("A", 180)
    for _ in range(10):
        if emu.task_active("Task_MultichoiceMenu_HandleInput"):
            break
        emu.press("A", 90)
    assert emu.task_active("Task_MultichoiceMenu_HandleInput")
    complete_journey(emu, emu.location()[1] // 4, destination)
    emu.walk("DOWN", 2)
    emu.frames(180)
    assert emu.location()[:2] == (43, destination * 4)
    emu.walk("DOWN", 4)
    emu.walk("LEFT", 7)


if __name__ == "__main__":
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        for order in permutations(range(3)):
            emu.state(ROOT / f"test-output/start-{COUNTRIES[order[0]]}.state", True)
            emu.walk("RIGHT", 1)
            seen = set()
            for index, city in enumerate(order):
                if index:
                    travel(emu, city)
                guide(emu)
                seen.add(city)
                assert [emu.var(v) for v in STAMPS] == [int(i in seen) for i in range(3)]
                assert emu.var(REWARDED) == int(index == 2)
                assert item_count(emu, EXP_SHARE) == int(index == 2)
                guide(emu)
                assert item_count(emu, EXP_SHARE) == int(index == 2), "Duplicate reward"
                assert emu.var(0x40F0) == order[0] + 1
                if order == (0, 1, 2) and index in (0, 2):
                    label = "partial" if index == 0 else "complete"
                    emu.state(ROOT / f"test-output/tour-{label}.state")
                    emu.screenshot(ROOT / f"test-output/tour-{label}.png")
            print(f"PASS: tour order {order}: three unique stamps, one reward, repeat guides safe", flush=True)

        # Capacity fixture: leave only the last stamp to collect, fill the Items
        # pocket, then free a slot and claim the still-pending reward normally.
        emu.state(ROOT / "test-output/tour-partial.state", True)
        travel(emu, 1)
        guide(emu)
        travel(emu, 2)
        bag = emu.read("gSaveBlock1Ptr") + 0x310
        key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20, 2)
        for i in range(42):
            emu.write(bag + i * 4, 13, 2)  # Potion slots; no room for another item.
            emu.write(bag + i * 4 + 2, 99 ^ key, 2)
        guide(emu)
        assert [emu.var(v) for v in STAMPS] == [1, 1, 1]
        assert emu.var(REWARDED) == 0
        assert item_count(emu, EXP_SHARE) == 0
        guide(emu)
        assert emu.var(REWARDED) == 0
        emu.write(bag, 0, 2)
        emu.write(bag + 2, key, 2)
        guide(emu)
        assert emu.var(REWARDED) == 1
        assert item_count(emu, EXP_SHARE) == 1
        print("PASS: full Bag preserves stamps and pending reward; freeing space allows one claim", flush=True)
    finally:
        emu.close()
