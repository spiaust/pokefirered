"""Reach Chantilly through both countryside maps and exercise its local services."""
from emulator import Emulator, ROOT
from test_tour import STAMPS, REWARDED


def walk_to_chantilly(emu):
    for steps, expected in ((15, (43, 5, 15, 23)),
                            (24, (43, 17, 15, 39)),
                            (40, (43, 16, 15, 23)),
                            (9, (43, 16, 15, 14))):
        emu.walk("UP", steps)
        assert emu.location() == expected, (emu.location(), expected)


if __name__ == "__main__":
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        emu.state(ROOT / "test-output/start-france.state", True)
        walk_to_chantilly(emu)
        assert not emu.in_battle()
        assert emu.var(0x40F0) == 2
        emu.state(ROOT / "test-output/chantilly-arrival.state")
        emu.screenshot(ROOT / "test-output/chantilly-arrival.png")
        for steps, expected in ((10, (43, 17, 15, 0)),
                                (40, (43, 5, 15, 0)),
                                (24, (43, 4, 15, 0)),
                                (14, (43, 4, 15, 14))):
            emu.walk("DOWN", steps)
            assert emu.location() == expected, (emu.location(), expected)
        print("PASS: Paris -> Gardens -> Chantilly Forest -> Chantilly and back on foot", flush=True)

        emu.state(ROOT / "test-output/start-france.state", True)
        emu.press("START", 60)
        emu.press("DOWN")
        emu.press("DOWN")
        emu.press("A", 180)
        emu.press("RIGHT", 90)
        emu.press("A", 90)
        emu.press("A", 180)
        assert emu.read("gPlayerAvatar", 1) & 2
        visited = set()
        for _ in range(2400):
            visited.add(emu.location()[1])
            if emu.location()[1] == 16 and emu.location()[3] <= 14:
                break
            emu.frames(1, "UP")
        else:
            raise AssertionError(("Cycling did not reach Chantilly", emu.location()))
        emu.frames(32)
        assert {4, 5, 17, 16} <= visited
        assert emu.read("gPlayerAvatar", 1) & 2
        assert not emu.in_battle()
        emu.screenshot(ROOT / "test-output/chantilly-cycling.png")
        for _ in range(2400):
            if emu.location()[1] == 4 and emu.location()[3] >= 14:
                break
            emu.frames(1, "DOWN")
        else:
            raise AssertionError(("Cycling did not return to Paris", emu.location()))
        emu.frames(32)
        assert emu.read("gPlayerAvatar", 1) & 2
        assert not emu.in_battle()
        print("PASS: Bicycle crosses both routes in both directions without forced encounters", flush=True)

        emu.state(ROOT / "test-output/chantilly-arrival.state", True)
        stamps = [emu.var(v) for v in (*STAMPS, REWARDED)]
        emu.walk("RIGHT", 1)
        emu.press("DOWN")
        emu.press("A", 180)
        emu.finish_dialogue()
        assert [emu.var(v) for v in (*STAMPS, REWARDED)] == stamps
        emu.state(ROOT / "test-output/chantilly-arrival.state", True)
        emu.walk("LEFT", 9)
        emu.walk("UP", 5)
        emu.frames(180)
        assert emu.location()[:2] == (43, 19)
        emu.walk("UP", 4)
        emu.walk("RIGHT", 1)
        emu.press("UP")
        party = emu.symbols["gPlayerParty"]
        max_hp = emu.read(party + 0x58, 2)
        emu.write(party + 0x56, 1, 2)
        emu.press("A", 180)
        emu.finish_dialogue()
        assert emu.read(party + 0x56, 2) == max_hp
        emu.walk("DOWN", 5)
        emu.frames(180)
        assert emu.location()[:2] == (43, 16)
        print("PASS: Chantilly guide preserves the stamp quest; clinic heals and exits", flush=True)

        emu.state(ROOT / "test-output/chantilly-arrival.state", True)
        emu.walk("RIGHT", 8)
        emu.walk("UP", 5)
        emu.frames(180)
        assert emu.location()[:2] == (43, 18)
        emu.state(ROOT / "test-output/chantilly-station.state")
        emu.walk("DOWN", 1)
        emu.frames(180)
        assert emu.location()[:2] == (43, 16)
        print("PASS: Chantilly station entry and exit", flush=True)

        emu.state(ROOT / "test-output/chantilly-arrival.state", True)
        emu.walk("DOWN", 10)
        emu.state(ROOT / "test-output/chantilly-trail.state")
        for y in (4, 37):
            emu.state(ROOT / "test-output/chantilly-trail.state", True)
            emu.walk("DOWN", y)
            emu.walk("LEFT", 2)
            emu.press("UP")
            emu.press("A", 180)
            assert emu.read("sLockFieldControls", 1)
            emu.screenshot(ROOT / f"test-output/chantilly-trail-sign-{y}.png")
            emu.finish_dialogue()
            assert emu.location() == (43, 17, 13, y)
        print("PASS: both Chantilly Forest direction signs work and release controls", flush=True)
        emu.state(ROOT / "test-output/chantilly-trail.state", True)
        emu.walk("DOWN", 9)
        for key in ["LEFT", "UP", "DOWN", "RIGHT"] * 30:
            for _ in range(48):
                if emu.in_battle():
                    break
                emu.frames(1, key)
            if emu.in_battle():
                break
        assert emu.in_battle(), "No Chantilly Forest encounter"
        emu.frames(300)
        enemy = emu.read(emu.symbols["gBattleMons"] + 0x58, 2)
        assert enemy in (10, 43, 392, 363), enemy
        emu.state(ROOT / "test-output/chantilly-battle.state")
        emu.screenshot(ROOT / "test-output/chantilly-battle.png")
        for _ in range(160):
            if not emu.in_battle():
                break
            emu.press("A", 90)
        assert not emu.in_battle()
        emu.frames(180)
        assert emu.location()[:2] == (43, 17)
        emu.state(ROOT / "test-output/chantilly-battle.state", True)
        battle = emu.symbols["gBattleMons"]
        emu.write(party + 0x56, 1, 2)
        emu.write(battle + 0x28, 1, 2)
        emu.write(battle + 0x06, 1, 2)
        emu.write(battle + 0x02, 1, 2)
        for _ in range(160):
            if not emu.in_battle():
                break
            emu.press("A", 90)
        assert not emu.in_battle()
        emu.frames(180)
        emu.finish_dialogue()
        assert emu.location()[:2] == (43, 19), emu.location()
        assert emu.read(party + 0x56, 2) > 1
        print("PASS: Chantilly Forest encounters use the local roster; defeat returns to Chantilly clinic", flush=True)
    finally:
        emu.close()
