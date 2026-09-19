"""Exercise every directed journey plus B, Exit, and same-station selection."""
from emulator import Emulator, ROOT
from europe_test_data import STOPS, CITIES, arrival_state
from rail_test_helpers import BOOKING, complete_journey

EXIT = len(STOPS)
emu = Emulator(ROOT / "pokefirered.gba")
try:
    for origin, country in enumerate(STOPS):
        state = arrival_state(country)
        emu.state(ROOT / f"test-output/{state}.state", True)
        home_country = emu.var(0x40F0)
        emu.walk("RIGHT", 8)
        emu.walk("UP", 5)
        emu.frames(180)
        assert emu.location()[:2] == (43, origin * 4 + 2)
        emu.walk("UP", 1)
        emu.walk("RIGHT", 3)
        emu.press("UP")
        emu.press("A", 180)
        for _ in range(10):
            if emu.task_active("Task_MultichoiceMenu_HandleInput"):
                break
            emu.press("A", 90)
        assert emu.task_active("Task_MultichoiceMenu_HandleInput"), CITIES[origin]
        menu = ROOT / f"test-output/train-menu-{country}.state"
        emu.state(menu)
        emu.screenshot(ROOT / f"test-output/train-menu-{country}.png")
        for destination in (-1, EXIT, origin) + tuple(i for i in range(len(STOPS)) if i != origin):
            emu.state(menu, True)
            if destination not in (-1, EXIT, origin):
                complete_journey(emu, origin, destination)
            elif destination == -1:
                emu.press("B", 90)
            else:
                for _ in range(destination):
                    emu.press("DOWN")
                emu.press("A", 180)
            emu.finish_dialogue()
            expected = origin if destination in (-1, EXIT) else destination
            assert emu.location()[:2] == (43, expected * 4 + 2), (origin, destination, emu.location())
            assert emu.var(0x40F0) == home_country, "Travel changed home country"
            assert emu.read("gPlayerPartyCount", 1) == 1
            assert emu.var(BOOKING) == 0
            assert not emu.read("sLockFieldControls", 1)
            if destination in (-1, EXIT, origin):
                print(f"PASS: {CITIES[origin]} menu option {destination} stays put and releases controls", flush=True)
            else:
                emu.screenshot(ROOT / f"test-output/train-{origin}-to-{destination}.png")
                emu.state(ROOT / f"test-output/train-{origin}-to-{destination}.state")
                emu.walk("DOWN", 2)
                emu.frames(180)
                assert emu.location()[:2] == (43, destination * 4)
                print(f"PASS: {CITIES[origin]} -> {CITIES[destination]}; destination exit works; home country preserved", flush=True)
finally:
    emu.close()
