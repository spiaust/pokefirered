"""Use a Rare Candy to verify non-Kanto starters can actually evolve.

Fixture: one Rare Candy in Items and the party's cached level just below the
evolution threshold. The normal item handler sets EXP for the new level,
recalculates stats, and runs the game's evolution scene.
"""
from emulator import Emulator, ROOT
from test_country import party_species

for case, level, target in (("england-1", 13, 156), ("germany-0", 15, 278)):
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        emu.state(ROOT / f"test-output/start-{case}.state", True)
        bag = emu.read("gSaveBlock1Ptr") + 0x310
        key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20, 2)
        emu.write(bag, 68, 2)
        emu.write(bag + 2, 1 ^ key, 2)
        emu.write(emu.symbols["gPlayerParty"] + 0x54, level, 1)
        emu.press("START", 60)
        emu.press("DOWN")
        emu.press("DOWN")
        emu.press("A", 180)
        emu.press("A", 90)
        emu.press("A", 180)
        for _ in range(80):
            emu.press("A", 90)
            if party_species(emu) == target:
                break
        emu.screenshot(ROOT / f"test-output/evolution-{case}.png")
        assert party_species(emu) == target, (case, party_species(emu))
        print(f"PASS: {case}: normal Rare Candy flow evolves the regional starter into {target}", flush=True)
    finally:
        emu.close()
