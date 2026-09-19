"""Mount the starting bicycle through the Bag and check faster movement."""
from emulator import Emulator, ROOT

emu = Emulator(ROOT / "pokefirered.gba")
try:
    emu.state(ROOT / "test-output/start-england.state", True)
    emu.walk("UP", 4)
    walking_y = emu.location()[3]
    emu.state(ROOT / "test-output/start-england.state", True)
    emu.press("START", 60)
    emu.press("DOWN")
    emu.press("DOWN")
    emu.press("A", 180)
    emu.press("RIGHT", 90)  # Key Items
    emu.press("A", 90)
    emu.press("A", 180)    # Use Bicycle
    assert emu.read("gPlayerAvatar", 1) & 2
    emu.frames(64, "UP")
    emu.frames(16)
    assert emu.location()[3] < walking_y, (emu.location(), walking_y)
    emu.screenshot(ROOT / "test-output/bicycle.png")
    print("PASS: Bicycle is usable from Key Items and moves faster than walking", flush=True)
finally:
    emu.close()
