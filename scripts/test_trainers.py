"""Play optional trainer wins, declines, repeated talks, and blackout recovery."""
from emulator import Emulator, ROOT
from test_country import wait_menu, party_species


def defeated(emu, index):
    flag = 0x500 + 743 + index
    return bool(emu.read(emu.read("gSaveBlock1Ptr") + 0xEE0 + flag // 8, 1) & (1 << (flag % 8)))


def money(emu):
    return emu.read(emu.read("gSaveBlock1Ptr") + 0x290) ^ emu.read(emu.read("gSaveBlock2Ptr") + 0xF20)


def talk(emu):
    emu.press("UP")
    emu.press("A", 180)


def fight(emu):
    for _ in range(200):
        if not emu.in_battle():
            break
        emu.press("A", 90)
    assert not emu.in_battle(), "Trainer battle did not finish"
    emu.frames(180)
    emu.finish_dialogue()


if __name__ == "__main__":
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        for index, country in enumerate(("england", "france", "germany")):
            emu.state(ROOT / f"test-output/start-{country}.state", True)
            emu.walk("UP", 15)
            emu.walk("UP", 4)
            emu.walk("RIGHT", 2)
            assert emu.location() == (43, index * 4 + 1, 17, 19), emu.location()
            talk(emu)
            wait_menu(emu, "Task_YesNoMenu_HandleInput")
            prompt = ROOT / f"test-output/trainer-{country}-prompt.state"
            emu.state(prompt)
            before_money = money(emu)
            for decline in ("B", "NO"):
                emu.state(prompt, True)
                if decline == "NO":
                    emu.press("DOWN")
                    emu.press("A", 180)
                else:
                    emu.press("B", 180)
                emu.finish_dialogue()
                assert not emu.in_battle() and not defeated(emu, index)
                assert money(emu) == before_money
                assert not emu.read("sLockFieldControls", 1)
            emu.state(prompt, True)
            emu.press("A", 180)
            for _ in range(30):
                if emu.in_battle():
                    break
                emu.press("A", 90)
            assert emu.in_battle(), "Trainer battle did not start"
            emu.frames(300)
            assert emu.read("gTrainerBattleOpponent_A", 2) == 743 + index
            expected_teams = ((16, 179), (10, 43), (161, 163))
            # Trainer setup fills party slots without updating gEnemyPartyCount.
            assert tuple(party_species(emu, "gEnemyParty", i) for i in range(2)) == expected_teams[index]
            assert emu.read(emu.symbols["gEnemyParty"] + 200 + 0x54, 1) == 0
            state = ROOT / f"test-output/trainer-{country}-battle.state"
            emu.state(state)
            emu.screenshot(ROOT / f"test-output/trainer-{country}-battle.png")
            fight(emu)
            assert defeated(emu, index), "Victory was not recorded"
            assert money(emu) > before_money, "No prize money"
            assert emu.location()[:2] == (43, index * 4 + 1)
            prize_money = money(emu)
            talk(emu)
            emu.finish_dialogue()
            assert not emu.in_battle() and defeated(emu, index)
            assert money(emu) == prize_money, "Repeated talk duplicated prize money"
            emu.state(ROOT / f"test-output/trainer-{country}-won.state")
            print(f"PASS: {country}: No/B decline, two-mon victory, prize money, persistent defeat and repeat talk", flush=True)

            emu.state(state, True)
            party = emu.symbols["gPlayerParty"]
            battle = emu.symbols["gBattleMons"]
            emu.write(party + 0x56, 1, 2)
            emu.write(battle + 0x28, 1, 2)
            emu.write(battle + 0x06, 1, 2)
            emu.write(battle + 0x02, 1, 2)
            fight(emu)
            assert not defeated(emu, index), "Losing awarded a trainer victory"
            assert emu.location()[:2] == (43, index * 4 + 3), emu.location()
            assert emu.read(party + 0x56, 2) > 1
            print(f"PASS: {country}: loss returns to local clinic without awarding victory", flush=True)
    finally:
        emu.close()
