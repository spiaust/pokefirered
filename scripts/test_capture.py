"""Catch a wild Pokemon via the normal battle Bag, with no catch-rate edits."""
from emulator import Emulator, ROOT

emu = Emulator(ROOT / "pokefirered.gba")
try:
    emu.state(ROOT / "test-output/england-battle.state", True)
    for _ in range(4):
        emu.press("A", 90)
    emu.press("B")         # Return from moves to the battle action menu.
    emu.press("RIGHT")
    emu.press("A", 180)    # Bag
    emu.press("RIGHT", 60)
    emu.press("RIGHT", 60) # Poke Balls
    emu.press("A", 90)
    emu.press("A", 400)
    for _ in range(180):
        if emu.read("gPlayerPartyCount", 1) == 2:
            break
        emu.press("A", 180)
        if emu.read(emu.symbols["gMain"] + 4) & ~1 == emu.symbols["CB2_NamingScreen"]:
            emu.press("START")
            emu.press("A", 180)
    assert emu.read("gPlayerPartyCount", 1) == 2, "Capture did not add a party member"
    for _ in range(12):
        if not emu.in_battle():
            break
        emu.press("A", 120)
    assert not emu.in_battle()
    emu.frames(180)
    assert emu.location()[:2] == (43, 1)
    emu.screenshot(ROOT / "test-output/capture-complete.png")
    emu.state(ROOT / "test-output/capture-complete.state")
    print("PASS: a wild Pokemon is caught, added to the party, and gameplay resumes", flush=True)
finally:
    emu.close()
