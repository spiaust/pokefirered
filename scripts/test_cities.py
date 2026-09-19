"""Walk city landmarks, map boards, and London's bridge using actual controls."""
from emulator import Emulator, ROOT
from europe_test_data import STOPS, arrival_state
from test_navigation import wait_task


def maps_in_bag(emu):
    bag = emu.read("gSaveBlock1Ptr") + 0x3B8
    key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20, 2)
    return sum(emu.read(bag + i * 4 + 2, 2) ^ key for i in range(30)
               if emu.read(bag + i * 4, 2) == 361)


if __name__ == "__main__":
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        for index, country in enumerate(STOPS):
            state = arrival_state(country)
            start = ROOT / f"test-output/{state}.state"
            emu.state(start, True)
            emu.walk("DOWN", 1)
            emu.walk("LEFT", 3)
            assert emu.location()[2:] == (12, 15)
            emu.press("DOWN")
            emu.press("A", 180)
            emu.screenshot(ROOT / f"test-output/landmark-{country}.png")
            emu.finish_dialogue()
            assert not emu.read("sLockFieldControls", 1)
            emu.state(start, True)
            emu.walk("DOWN", 7)
            assert emu.location()[2:] == (15, 21), emu.location()
            emu.screenshot(ROOT / f"test-output/city-{country}.png")
            emu.walk("UP", 7)
            assert emu.location()[2:] == (15, 14)
            if index == 0:
                emu.walk("LEFT", 4)
                emu.walk("DOWN", 5)
                assert emu.location()[3] == 17, "Player walked into the Thames"
            emu.state(start, True)
            # Simulate an older player's inventory: no Town Map yet.
            bag = emu.read("gSaveBlock1Ptr") + 0x3B8
            key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20, 2)
            for i in range(30):
                if emu.read(bag + i * 4, 2) == 361:
                    emu.write(bag + i * 4, 0, 2)
                    emu.write(bag + i * 4 + 2, key, 2)
            assert maps_in_bag(emu) == 0
            emu.walk("RIGHT", 4)
            emu.walk("UP", 2)
            assert emu.location()[2:] == (19, 12)
            for visit in range(2):
                emu.press("UP")
                emu.press("A", 180)
                for _ in range(30):
                    if emu.task_active("Task_EuropeMap"):
                        break
                    emu.press("A", 90)
                wait_task(emu, "Task_EuropeMap")
                assert maps_in_bag(emu) == 1, "Board duplicated or failed to grant the map"
                assert emu.read("sEuropeMapCurrent", 1) == index
                emu.press("B", 180)
                emu.finish_dialogue()
                assert emu.location() == (43, index * 4, 19, 12)
                assert not emu.read("sLockFieldControls", 1)
            print(f"PASS: {country}: landmark, southern walk, board map, legacy inventory gift and repeat use", flush=True)
    finally:
        emu.close()
