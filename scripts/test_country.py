"""Exercise all country choices from a real new game, using button inputs."""
from pathlib import Path
from emulator import Emulator, ROOT


def start_new_game(emu):
    seen = set()

    def press(key, wait=30):
        emu.press(key, wait)
        for task, label in (("Task_OakSpeech_ThisWorld", "professor-welcome"),
                            ("Task_OakSpeech_IStudyPokemon", "professor-eevee")):
            if emu.task_active(task):
                seen.add(label)
                emu.screenshot(ROOT / f"test-output/{label}.png")

    emu.frames(600)
    press("START", 480)
    press("START", 180)
    for _ in range(18):
        press("A", 90)
    for _ in range(15):
        press("A", 150)
    press("START", 20)
    press("A", 180)
    for _ in range(12):
        press("A", 150)
    press("START", 20)
    press("A", 180)
    for _ in range(20):
        if emu.task_active("Task_MultichoiceMenu_HandleInput"):
            break
        press("A", 150)
    assert emu.task_active("Task_MultichoiceMenu_HandleInput"), "Country menu did not open"
    assert emu.var(0x40F0) == 0
    emu.screenshot(ROOT / "test-output/country-menu.png")
    emu.state(ROOT / "test-output/country-menu.state")

    assert seen == {"professor-welcome", "professor-eevee"}, seen


STARTERS = ((1, 155, 158), (152, 280, 7), (277, 4, 283))


def wait_menu(emu, task):
    for _ in range(30):
        if emu.task_active(task):
            return
        emu.press("A", 90)
    raise AssertionError(f"Menu did not open: {task}")


def party_species(emu, party="gPlayerParty", index=0):
    import re
    source = (ROOT / "src/pokemon.c").read_text()
    slots = {int(n): int(slot) for n, slot in re.findall(
        r"SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),", source)}
    mon = emu.symbols[party] + 100 * index
    personality, trainer = emu.read(mon), emu.read(mon + 4)
    return (emu.read(mon + 32 + slots[personality % 24] * 12) ^ personality ^ trainer) & 0xFFFF


if __name__ == "__main__":
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        start_new_game(emu)
        for choice, country in enumerate(("england", "france", "germany")):
            emu.state(ROOT / "test-output/country-menu.state", True)
            emu.press("B")
            assert emu.task_active("Task_MultichoiceMenu_HandleInput")
            assert emu.var(0x40F0) == 0
            for _ in range(choice):
                emu.press("DOWN")
            emu.press("A", 180)
            wait_menu(emu, "Task_MultichoiceMenu_HandleInput")
            menu = ROOT / f"test-output/starters-{country}.state"
            emu.state(menu)
            emu.screenshot(ROOT / f"test-output/starters-{country}.png")
            # Back from the starter list allows a different country, no gifts.
            emu.press("B", 180)
            wait_menu(emu, "Task_MultichoiceMenu_HandleInput")
            assert emu.var(0x40F0) == 0
            assert emu.var(0x40F6) == 0
            assert emu.read("gPlayerPartyCount", 1) == 0
            for starter, species in enumerate(STARTERS[choice]):
                emu.state(menu, True)
                for _ in range(starter):
                    emu.press("DOWN")
                emu.press("A", 180)
                wait_menu(emu, "Task_YesNoMenu_HandleInput")
                preview = ROOT / f"test-output/preview-{country}-{starter}.state"
                emu.state(preview)
                emu.screenshot(ROOT / f"test-output/preview-{country}-{starter}.png")
                for decline in ("B", "NO"):
                    emu.state(preview, True)
                    if decline == "NO":
                        emu.press("DOWN")
                        emu.press("A", 180)
                    else:
                        emu.press("B", 180)
                    wait_menu(emu, "Task_MultichoiceMenu_HandleInput")
                    assert emu.read("gPlayerPartyCount", 1) == 0
                    assert emu.var(0x40F6) == 0
                emu.state(preview, True)
                emu.press("A", 180)
                emu.finish_dialogue()
                assert emu.var(0x40F0) == choice + 1
                assert emu.var(0x40F6) == species
                assert party_species(emu) == species
                assert emu.location() == (43, choice * 4, 15, 14)
                assert emu.read("gPlayerPartyCount", 1) == 1
                assert emu.read(emu.symbols["gPlayerParty"] + 0x54, 1) == 8
                assert emu.var(0x404E) == 0x6258  # National Dex permits non-Kanto evolution.
                assert emu.read(emu.read("gSaveBlock2Ptr") + 0x1B, 1) == 0xB9
                emu.state(ROOT / f"test-output/start-{country}-{starter}.state")
                if starter == 0:
                    emu.screenshot(ROOT / f"test-output/start-{country}.png")
                    emu.state(ROOT / f"test-output/start-{country}.state")
                print(f"PASS: {country} starter {species}: preview, No/B retry, exact party species, city and level", flush=True)
            print(f"PASS: {country}: B returns to country selection without giving a Pokemon", flush=True)
    finally:
        emu.close()
