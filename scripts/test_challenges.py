"""Play the three extended route trainers after the local trainer and clinic."""
from emulator import Emulator, ROOT
from test_country import wait_menu, party_species


from test_trainers import money, talk, fight, defeated as local_defeated

def defeated(emu, index):
    return local_defeated(emu, index + 3)


def fight_with_supplies(emu):
    """Use supplied Potions through the real Bag; never alter battle stats."""
    from test_tour import item_count
    # Several controllers have a static function with this name. The player
    # controller is the first one in link order; the general symbol dict keeps
    # the last duplicate (the tutorial controller).
    action = next(int(line.split()[0], 16) for line in
                  (ROOT / "pokefirered.sym").read_text().splitlines()
                  if line.split()[-1:] == ["HandleInputChooseAction"])
    for _ in range(700):
        if not emu.in_battle():
            break
        fn = emu.read("gBattlerControllerFuncs") & ~1
        move = emu.symbols["HandleInputChooseMove"]
        hp = emu.read(emu.symbols["gBattleMons"] + 0x28, 2)
        if fn in (action, move) and hp <= 15 and item_count(emu, 13):
            if fn == move:
                emu.press("B")
            emu.press("UP")
            emu.press("LEFT")
            emu.press("RIGHT")
            emu.press("A", 180)
            emu.press("A", 90)
            emu.press("A", 180)
            emu.press("A", 180)
        else:
            if fn == action:
                emu.press("UP")
                emu.press("LEFT")
            emu.press("A", 30)
    emu.screenshot(ROOT / "test-output/supplies-end.png")
    assert not emu.in_battle(), "Supplied trainer battle did not finish"
    emu.frames(180)
    emu.finish_dialogue()


if __name__ == "__main__":
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        for index, country in enumerate(("england", "france", "germany")):
            emu.state(ROOT / f"test-output/trainer-{country}-won.state", True)
            emu.walk("DOWN", 5)
            emu.walk("DOWN", 14)
            emu.walk("LEFT", 11)
            emu.walk("UP", 5)
            emu.frames(180)
            emu.walk("UP", 4)
            emu.walk("RIGHT", 1)
            emu.press("UP")
            emu.press("A", 180)
            emu.finish_dialogue()
            emu.walk("DOWN", 5)
            emu.frames(180)
            emu.walk("RIGHT", 9)
            emu.walk("UP", 11)
            emu.walk("UP", 24)
            emu.walk("UP", 20)
            emu.walk("RIGHT", 2)
            assert emu.location() == (43, index * 4 + 13, 17, 19), emu.location()
            talk(emu)
            wait_menu(emu, "Task_YesNoMenu_HandleInput")
            prompt = ROOT / f"test-output/challenge-{country}-prompt.state"
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
            assert emu.read("gTrainerBattleOpponent_A", 2) == 746 + index
            expected_teams = ((16, 179), (10, 43), (161, 163))
            # Trainer setup fills party slots without updating gEnemyPartyCount.
            assert tuple(party_species(emu, "gEnemyParty", i) for i in range(2)) == expected_teams[index]
            assert emu.read(emu.symbols["gEnemyParty"] + 200 + 0x54, 1) == 0
            state = ROOT / f"test-output/challenge-{country}-battle.state"
            emu.state(state)
            emu.screenshot(ROOT / f"test-output/challenge-{country}-battle.png")
            fight_with_supplies(emu)
            assert defeated(emu, index), "Victory was not recorded"
            assert money(emu) > before_money, "No prize money"
            assert emu.location()[:2] == (43, index * 4 + 13)
            prize_money = money(emu)
            talk(emu)
            emu.finish_dialogue()
            assert not emu.in_battle() and defeated(emu, index)
            assert money(emu) == prize_money, "Repeated talk duplicated prize money"
            emu.state(ROOT / f"test-output/challenge-{country}-won.state")
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

