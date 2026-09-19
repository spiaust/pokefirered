"""Real-button rail helpers; expected routes come from an independent graph."""
from collections import deque
from emulator import ROOT
from test_country import wait_menu

BOOKING = 0x40F7
EDGES = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0,), 4: (1,), 5: (2,)}


def route(origin, destination):
    queue = deque([(origin, [])])
    seen = {origin}
    while queue:
        current, path = queue.popleft()
        if current == destination:
            return path
        for neighbor in EDGES[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    raise AssertionError((origin, destination))


def speak_from_arrival(emu):
    assert emu.location()[2:] == (4, 7), emu.location()
    emu.walk("RIGHT", 3)
    emu.press("UP")
    emu.press("A", 180)


def choose_destination(emu, destination):
    wait_menu(emu, "Task_MultichoiceMenu_HandleInput")
    for _ in range(destination):
        emu.press("DOWN")
    emu.press("A", 180)
    wait_menu(emu, "Task_YesNoMenu_HandleInput")


def board(emu, next_stop, destination):
    wait_menu(emu, "Task_YesNoMenu_HandleInput")
    origin = emu.location()[1] // 4
    # FireRed's text encoding starts numeric digits at 0xA1 (see charmap.txt).
    assert emu.read("gStringVar3", 1) == 0xA1 + len(route(origin, destination))
    assert emu.read("gSpecialVar_0x8006", 2) == next_stop
    emu.press("A", 180)
    emu.finish_dialogue()
    assert emu.location() == (43, next_stop * 4 + 2, 4, 7), emu.location()
    assert emu.var(BOOKING) == (0 if next_stop == destination else destination + 1)
    assert not emu.read("sLockFieldControls", 1)


def complete_journey(emu, origin, destination):
    choose_destination(emu, destination)
    for index, next_stop in enumerate(route(origin, destination)):
        if index:
            speak_from_arrival(emu)
        board(emu, next_stop, destination)


def finish_saved_journey(emu):
    destination = emu.var(BOOKING) - 1
    origin = emu.location()[1] // 4
    for next_stop in route(origin, destination):
        speak_from_arrival(emu)
        board(emu, next_stop, destination)
