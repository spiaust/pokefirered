"""Boot the European title and enter the main menu with either accepted key."""
from emulator import Emulator, ROOT

for key in ("START", "A"):
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        emu.frames(600)
        assert emu.task_active("Task_EuropeTitle"), "European title did not appear"
        emu.screenshot(ROOT / "test-output/europe-title.png")
        emu.press(key, 240)
        emu.screenshot(ROOT / "test-output/europe-main-menu.png")
        assert emu.read(emu.symbols["gMain"] + 4) & ~1 == emu.symbols["CB2_NewGameScene"] & ~1, "New game did not open"
        print(f"PASS: European title boots and {key} opens the new-game flow", flush=True)
    finally:
        emu.close()
