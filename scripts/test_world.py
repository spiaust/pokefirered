"""Play every city's clinic, route, battle, and defeat-recovery tests."""
import re
import sys
from emulator import Emulator, ROOT

country = sys.argv[1] if len(sys.argv) > 1 else "england"
index = ("england", "france", "germany").index(country)
base = index * 4
rosters = (("PIDGEY", "RATTATA", "MAREEP", "ODDISH"),
           ("CATERPIE", "ODDISH", "ROSELIA", "RALTS"),
           ("SENTRET", "HOOTHOOT", "TEDDIURSA", "PINECO"))
species_ids = {name: int(value) for name, value in re.findall(
    r"^#define SPECIES_(\w+)\s+(\d+)\s*$", (ROOT / "include/constants/species.h").read_text(), re.M)}
start_state = ROOT / f"test-output/start-{country}.state"
emu = Emulator(ROOT / "pokefirered.gba")
try:
    emu.state(start_state, True)
    assert emu.location() == (43, base, 15, 14)
    assert emu.read("gPlayerPartyCount", 1) == 1
    emu.walk("LEFT", 9)
    emu.walk("UP", 4)
    assert emu.location() == (43, base, 6, 10)
    emu.walk("UP", 1)
    emu.frames(180)
    assert emu.location()[:2] == (43, base + 3)
    emu.walk("UP", 4)
    emu.walk("RIGHT", 1)
    emu.press("UP")
    # Controlled injury fixture; the nurse must restore the actual party HP.
    party = emu.symbols["gPlayerParty"]
    max_hp = emu.read(party + 0x58, 2)
    emu.write(party + 0x56, 1, 2)
    emu.press("A", 180)
    emu.finish_dialogue()
    assert emu.read(party + 0x56, 2) == max_hp
    emu.screenshot(ROOT / f"test-output/{country}-healed.png")
    emu.walk("DOWN", 5)
    emu.frames(180)
    assert emu.location()[:2] == (43, base)
    print(f"PASS: {country}: clinic entry, nurse restores HP, and exit", flush=True)

    emu.state(start_state, True)
    emu.walk("RIGHT", 8)
    emu.walk("UP", 5)
    emu.frames(180)
    assert emu.location()[:2] == (43, base + 2), emu.location()
    emu.screenshot(ROOT / f"test-output/{country}-station.png")
    emu.walk("DOWN", 1)
    emu.frames(180)
    assert emu.location()[:2] == (43, base)
    print(f"PASS: {country}: station entry and exit", flush=True)

    emu.state(start_state, True)
    emu.walk("UP", 15)
    assert emu.location()[:2] == (43, base + 1), emu.location()
    emu.screenshot(ROOT / f"test-output/{country}-route.png")
    emu.state(ROOT / f"test-output/{country}-route.state")
    emu.walk("DOWN", 1)
    assert emu.location()[:2] == (43, base), emu.location()
    emu.state(ROOT / f"test-output/{country}-route.state", True)
    # Enter the French grass from below the study marker at (13, 16).
    # The clear main path remains at x=15; walking left at y=16 hits the sign.
    emu.walk("UP", 6 if country == "france" else 7)
    for key in ["LEFT", "UP", "DOWN", "RIGHT"] * 30:
        for _ in range(48):
            if emu.in_battle():
                break
            emu.frames(1, key)
        if emu.in_battle():
            break
    assert emu.in_battle(), "No countryside encounter"
    emu.frames(300)
    enemy = emu.read(emu.symbols["gBattleMons"] + 0x58, 2)
    assert enemy in [species_ids[name] for name in rosters[index]], enemy
    emu.screenshot(ROOT / f"test-output/{country}-battle.png")
    emu.state(ROOT / f"test-output/{country}-battle.state")
    for _ in range(140):
        if not emu.in_battle():
            break
        emu.press("A", 90)
    assert not emu.in_battle(), "Battle did not finish"
    emu.frames(180)
    assert emu.location()[:2] == (43, base + 1)
    emu.screenshot(ROOT / f"test-output/{country}-after-battle.png")
    print(f"PASS: {country}: route connects both ways; encounter species {enemy}; battle finishes", flush=True)

    emu.state(ROOT / f"test-output/{country}-battle.state", True)
    battle = emu.symbols["gBattleMons"]
    # A controlled defeat fixture exercises the real blackout/respawn path.
    emu.write(party + 0x56, 1, 2)
    emu.write(battle + 0x28, 1, 2)
    emu.write(battle + 0x06, 1, 2)
    emu.write(battle + 0x02, 1, 2)
    for _ in range(160):
        if not emu.in_battle():
            break
        emu.press("A", 90)
    assert not emu.in_battle(), "Defeat did not finish"
    emu.frames(180)
    emu.finish_dialogue()
    assert emu.location()[:2] == (43, base + 3), emu.location()
    assert emu.read(party + 0x56, 2) > 1
    emu.screenshot(ROOT / f"test-output/{country}-blackout.png")
    print(f"PASS: {country}: defeat recovers at the correct clinic with healed party", flush=True)
finally:
    emu.close()
