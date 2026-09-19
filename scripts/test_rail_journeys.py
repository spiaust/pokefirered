"""Exercise preview cancellation, saved transfers, detours, and destination arrival."""
from emulator import Emulator, ROOT
from test_country import wait_menu
from rail_test_helpers import BOOKING, choose_destination, board, speak_from_arrival

emu = Emulator(ROOT / "pokefirered.gba")
try:
    # Longest route: Oxford -> London -> Paris -> Berlin -> Oranienburg.
    emu.state(ROOT / "test-output/oxford-arrival.state", True)
    emu.walk("RIGHT", 8)
    emu.walk("UP", 5)
    emu.frames(180)
    emu.walk("UP", 1)
    speak_from_arrival(emu)
    choose_destination(emu, 5)
    assert emu.read("gSpecialVar_0x8006", 2) == 0
    emu.screenshot(ROOT / "test-output/rail-preview.png")
    preview = ROOT / "test-output/rail-preview.state"
    emu.state(preview)
    for decline in ("B", "NO"):
        emu.state(preview, True)
        if decline == "NO":
            emu.press("DOWN")
            emu.press("A", 180)
        else:
            emu.press("B", 180)
        emu.finish_dialogue()
        assert emu.location() == (43, 14, 7, 7)
        assert emu.var(BOOKING) == 0
    print("PASS: No/B on itinerary preview does not board or create a booking", flush=True)
    emu.state(preview, True)
    for index, (stop, label) in enumerate(((0, "london"), (1, "paris"), (2, "berlin"), (5, "oranienburg"))):
        if index:
            speak_from_arrival(emu)
        board(emu, stop, 5)
        if stop != 5:
            emu.state(ROOT / f"test-output/rail-transfer-{label}.state")
    print("PASS: Oxford to Oranienburg stops in London, Paris, and Berlin; final arrival clears booking", flush=True)

    emu.state(ROOT / "test-output/rail-transfer-paris.state", True)
    speak_from_arrival(emu)
    wait_menu(emu, "Task_YesNoMenu_HandleInput")
    emu.screenshot(ROOT / "test-output/rail-resume.png")
    resume = ROOT / "test-output/rail-resume.state"
    emu.state(resume)
    for decline in ("B", "NO"):
        emu.state(resume, True)
        emu.press("B", 180)  # Defer continuing; cancellation needs confirmation.
        wait_menu(emu, "Task_YesNoMenu_HandleInput")
        if decline == "NO":
            emu.press("DOWN")
            emu.press("A", 180)
        else:
            emu.press("B", 180)
        emu.finish_dialogue()
        assert emu.var(BOOKING) == 6
        assert emu.location() == (43, 6, 7, 7)
    emu.state(resume, True)
    emu.press("B", 180)
    wait_menu(emu, "Task_YesNoMenu_HandleInput")
    emu.press("A", 180)
    emu.finish_dialogue()
    assert emu.var(BOOKING) == 0
    assert emu.location() == (43, 6, 7, 7)
    emu.press("A", 180)
    wait_menu(emu, "Task_MultichoiceMenu_HandleInput")
    choose_destination(emu, 4)
    board(emu, 4, 4)
    print("PASS: keep or explicitly cancel a saved journey, then book a different destination", flush=True)

    # Leaving the station does not lose the itinerary.
    emu.state(ROOT / "test-output/rail-transfer-berlin.state", True)
    emu.walk("DOWN", 2)
    emu.frames(180)
    assert emu.location() == (43, 8, 23, 10)
    assert emu.var(BOOKING) == 6
    emu.state(ROOT / "test-output/rail-paused-outside.state")
    emu.walk("DOWN", 4)
    emu.walk("LEFT", 8)
    from test_oranienburg import walk_to_oranienburg
    walk_to_oranienburg(emu)
    emu.walk("RIGHT", 8)
    emu.walk("UP", 5)
    emu.frames(180)
    emu.walk("UP", 1)
    speak_from_arrival(emu)
    emu.finish_dialogue()
    assert emu.var(BOOKING) == 0
    assert emu.location() == (43, 22, 7, 7)
    print("PASS: station exit preserves booking; reaching the destination on foot clears it at the clerk", flush=True)

    # A walking detour to another station recalculates the next connection.
    emu.state(ROOT / "test-output/rail-transfer-paris.state", True)
    emu.walk("DOWN", 2)
    emu.frames(180)
    emu.walk("DOWN", 4)
    emu.walk("LEFT", 8)
    from test_chantilly import walk_to_chantilly
    walk_to_chantilly(emu)
    emu.walk("RIGHT", 8)
    emu.walk("UP", 5)
    emu.frames(180)
    emu.walk("UP", 1)
    speak_from_arrival(emu)
    board(emu, 1, 5)
    assert emu.var(BOOKING) == 6
    print("PASS: walking to Chantilly during a booked trip recalculates the next stop as Paris", flush=True)

    # Malformed legacy data must never be used as an array index.
    for invalid in (7, 65535):
        emu.state(ROOT / "test-output/rail-transfer-paris.state", True)
        emu.write(emu.read("gSaveBlock1Ptr") + 0x1000 + (BOOKING - 0x4000) * 2, invalid, 2)
        speak_from_arrival(emu)
        wait_menu(emu, "Task_MultichoiceMenu_HandleInput")
        assert emu.var(BOOKING) == 0
        emu.press("B", 180)
        emu.finish_dialogue()
        assert emu.location() == (43, 6, 7, 7)
    print("PASS: invalid saved destinations are cleared safely", flush=True)
finally:
    emu.close()
