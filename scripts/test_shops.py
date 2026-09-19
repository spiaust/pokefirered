"""Buy supplies in every station and verify money, cancellation and zero funds."""
from emulator import Emulator, ROOT
from europe_test_data import STOPS, arrival_state
from test_country import wait_menu
from test_tour import item_count
from test_trainers import money


def balls(emu):
    bag = emu.read("gSaveBlock1Ptr") + 0x430
    key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20, 2)
    return sum(emu.read(bag + i * 4 + 2, 2) ^ key for i in range(13)
               if emu.read(bag + i * 4, 2) == 4)


def confirm_purchase(emu, quantity=1):
    emu.press("A", 180)
    wait_menu(emu, "Task_BuyHowManyDialogueHandleInput")
    for _ in range(quantity - 1):
        emu.press("UP")
    emu.press("A", 180)
    wait_menu(emu, "Task_CallYesOrNoCallback")


if __name__ == "__main__":
    emu = Emulator(ROOT / "pokefirered.gba")
    try:
        for index, country in enumerate(STOPS):
            state = arrival_state(country)
            emu.state(ROOT / f"test-output/{state}.state", True)
            emu.walk("RIGHT", 8)
            emu.walk("UP", 5)
            emu.frames(180)
            emu.walk("UP", 1)
            emu.walk("LEFT", 3)
            assert emu.location()[2:] == (1, 7), emu.location()
            emu.press("UP")
            emu.press("A", 180)
            wait_menu(emu, "Task_ShopMenu")
            emu.press("A", 180)
            wait_menu(emu, "Task_BuyMenu")
            emu.screenshot(ROOT / f"test-output/shop-{country}.png")
            menu = ROOT / f"test-output/shop-{country}-menu.state"
            emu.state(menu)
            before = money(emu), balls(emu), item_count(emu, 13)
            confirm_purchase(emu, 2)
            emu.press("B", 90)
            wait_menu(emu, "Task_BuyMenu")
            assert (money(emu), balls(emu), item_count(emu, 13)) == before
            confirm_purchase(emu, 2)
            emu.press("A", 180)
            wait_menu(emu, "Task_ReturnToItemListAfterItemPurchase")
            assert balls(emu) == before[1] + 2
            assert money(emu) == before[0] - 400
            emu.press("A", 90)
            emu.press("DOWN")
            confirm_purchase(emu)
            emu.press("A", 180)
            wait_menu(emu, "Task_ReturnToItemListAfterItemPurchase")
            assert item_count(emu, 13) == before[2] + 1
            assert money(emu) == before[0] - 700
            emu.press("A", 90)
            emu.press("B", 180)
            wait_menu(emu, "Task_ShopMenu")
            emu.press("B", 180)
            emu.finish_dialogue()
            assert not emu.read("sLockFieldControls", 1)
            emu.state(ROOT / f"test-output/shop-{country}-bought.state")
            emu.walk("RIGHT", 3)
            emu.walk("DOWN", 2)
            emu.frames(180)
            assert emu.location()[:2] == (43, index * 4)
            print(f"PASS: {country}: cancel, buy two Balls and a Potion, exact prices, exit station", flush=True)

            emu.state(menu, True)
            key = emu.read(emu.read("gSaveBlock2Ptr") + 0xF20)
            emu.write(emu.read("gSaveBlock1Ptr") + 0x290, key)
            emu.press("A", 180)
            wait_menu(emu, "Task_BuyMenu")
            assert money(emu) == 0 and balls(emu) == before[1]
            print(f"PASS: {country}: insufficient funds cannot purchase supplies", flush=True)
    finally:
        emu.close()
