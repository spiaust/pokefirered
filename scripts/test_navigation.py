"""Use the European map from the Bag and registered-item field shortcut."""
from emulator import Emulator, ROOT
from europe_test_data import STOPS, arrival_state


MAP_STOP_COUNT = 8  # Six rail cities and the two coastal ports.

def wait_task(emu, task):
    for _ in range(30):
        if emu.task_active(task):
            return
        emu.frames(30)
    raise AssertionError(task)


if __name__ == "__main__":
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        for index, country in enumerate(STOPS):
            state = arrival_state(country)
            emu.state(ROOT / f"test-output/{state}.state", True)
            location = emu.location()
            emu.press("START", 60)
            emu.press("DOWN")
            emu.press("DOWN")
            emu.press("A", 180)
            emu.press("RIGHT", 90)
            emu.press("DOWN")  # Town Map follows Bicycle in Key Items.
            emu.press("A", 90)
            emu.press("A", 180)
            wait_task(emu, "Task_EuropeMap")
            assert emu.read("sEuropeMapCurrent", 1) == index
            assert emu.read("sEuropeMapSelection", 1) == index
            emu.screenshot(ROOT / f"test-output/navigation-{country}.png")
            for direction, delta in (("RIGHT", 1), ("LEFT", -1)):
                for step in range(1, MAP_STOP_COUNT + 1):
                    emu.press(direction)
                    assert emu.read("sEuropeMapSelection", 1) == (index + delta * step) % MAP_STOP_COUNT
            emu.press("A")
            emu.screenshot(ROOT / f"test-output/navigation-{country}-rail-info.png")
            emu.press("B", 180)
            wait_task(emu, "Task_BagMenu_HandleInput")
            # Register the same map through the normal item menu.
            emu.press("A", 90)
            emu.press("DOWN")
            emu.press("A", 90)
            assert emu.read(emu.read("gSaveBlock1Ptr") + 0x296, 2) == 361
            emu.press("B", 180)
            emu.press("B", 90)
            emu.press("SELECT", 180)
            wait_task(emu, "Task_EuropeMap")
            emu.press("START", 180)
            assert not emu.task_active("Task_EuropeMap")
            assert emu.location() == location
            assert not emu.read("sLockFieldControls", 1)
            emu.state(ROOT / f"test-output/navigation-{country}.state")
            emu.walk("DOWN", 1)
            assert emu.location()[3] == location[3] + 1
            for context in ("route", "station", "clinic"):
                emu.state(ROOT / f"test-output/navigation-{country}.state", True)
                if context == "route":
                    emu.walk("DOWN", 10) if index >= 3 else emu.walk("UP", 15)
                else:
                    emu.walk("RIGHT" if context == "station" else "LEFT", 8 if context == "station" else 9)
                    emu.walk("UP", 5)
                    emu.frames(180)
                before = emu.location()
                emu.press("SELECT", 180)
                wait_task(emu, "Task_EuropeMap")
                assert emu.read("sEuropeMapCurrent", 1) == index
                emu.press("B", 180)
                assert emu.location() == before
                assert not emu.read("sLockFieldControls", 1)
            print(f"PASS: {country}: Bag map, city browsing, rail info, registered map and both exit keys", flush=True)
    finally:
        emu.close()
