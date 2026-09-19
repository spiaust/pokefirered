"""Carry one team through all three trail trainers using trains and clinics."""
from emulator import Emulator, ROOT
from test_country import wait_menu
from test_trainers import defeated, talk, fight
from test_tour import travel

emu = Emulator(ROOT / "pokefirered.gba")
try:
    emu.state(ROOT / "test-output/trainer-england-won.state", True)
    for country in (1, 2):
        # Return from the previous trainer to the city and board the train.
        emu.walk("DOWN", 5)
        emu.walk("DOWN", 14)
        emu.walk("LEFT", 1)
        assert emu.location()[2:] == (16, 14), emu.location()
        travel(emu, country)
        # Heal normally before challenging the next trainer.
        emu.walk("LEFT", 10)
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
        emu.walk("UP", 4)
        emu.walk("RIGHT", 2)
        assert emu.location() == (43, country * 4 + 1, 17, 19), emu.location()
        talk(emu)
        wait_menu(emu, "Task_YesNoMenu_HandleInput")
        emu.press("A", 180)
        for _ in range(30):
            if emu.in_battle():
                break
            emu.press("A", 90)
        assert emu.in_battle()
        emu.frames(300)
        fight(emu)
        assert defeated(emu, country)
    assert all(defeated(emu, i) for i in range(3))
    # Standard trainer battles return to the field; talk again for the report.
    talk(emu)
    emu.finish_dialogue()
    assert emu.read("gSpecialVar_0x8005", 2) == 3
    emu.state(ROOT / "test-output/trainer-all-won.state")
    emu.screenshot(ROOT / "test-output/trainer-all-won.png")
    print("PASS: one team completes all three trail trainers through normal trains and clinic healing; progress reports 3/3", flush=True)
finally:
    emu.close()
