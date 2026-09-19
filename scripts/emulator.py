"""Run deterministic button sequences in a headless mGBA core.

Usage: python3 scripts/emulator.py ROM actions.json
Actions: frames, press, screenshot, save_state, load_state, read, assert.
Addresses may be hex strings or symbols from the ROM's .sym file.
The runner never opens the player's .sav file.
"""
import ctypes
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
KEYS = {"A": 1, "B": 2, "SELECT": 4, "START": 8,
        "RIGHT": 16, "LEFT": 32, "UP": 64, "DOWN": 128,
        "R": 256, "L": 512}


class Emulator:
    def __init__(self, rom):
        self.lib = ctypes.CDLL(str(ROOT / ".local-tools/emulator_bridge.so"))
        self.lib.emulator_read.restype = ctypes.c_uint32
        self.symbols = {}
        for line in Path(rom).with_suffix(".sym").read_text().splitlines():
            parts = line.split()
            if len(parts) >= 3:
                try:
                    self.symbols[parts[-1]] = int(parts[0], 16)
                except ValueError:
                    pass
        assert self.lib.emulator_open(str(rom).encode()), "Could not load ROM"

    def address(self, value):
        return self.symbols[value] if value in self.symbols else int(value, 0)

    def read(self, address, size=4):
        if isinstance(address, str):
            address = self.address(address)
        return self.lib.emulator_read(address, size)

    def frames(self, count=1, keys=0):
        if isinstance(keys, str):
            keys = sum(KEYS[k] for k in keys.split("+") if k)
        self.lib.emulator_frames(keys, count)

    def press(self, key, wait=30):
        self.frames(2, key)
        self.frames(wait)

    def task_active(self, name):
        expected = self.symbols[name] & ~1
        base = self.symbols["gTasks"]
        return any(self.read(base + i * 40 + 4, 1)
                   and self.read(base + i * 40) & ~1 == expected
                   for i in range(16))

    def var(self, var_id):
        save = self.read("gSaveBlock1Ptr")
        return self.read(save + 0x1000 + (var_id - 0x4000) * 2, 2)

    def location(self):
        save = self.read("gSaveBlock1Ptr")
        return (self.read(save + 4, 1), self.read(save + 5, 1),
                self.read(save, 2), self.read(save + 2, 2))

    def write(self, address, value, size=4):
        if isinstance(address, str):
            address = self.address(address)
        self.lib.emulator_write(address, value, size)

    def walk(self, direction, tiles):
        self.frames(16 * tiles, direction)
        self.frames(16)

    def finish_dialogue(self):
        for _ in range(40):
            if not self.read("sLockFieldControls", 1):
                return
            self.press("A", 90)
        raise AssertionError("Dialogue did not release player controls")

    def in_battle(self):
        return bool(self.read(self.symbols["gMain"] + 0x439, 1) & 2)

    def screenshot(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        assert self.lib.emulator_screenshot(str(path).encode())

    def state(self, path, load=False):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        assert self.lib.emulator_state(str(path).encode(), int(load))

    def battery(self, path, load=False):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        assert self.lib.emulator_battery(str(path).encode(), int(load))

    def close(self):
        self.lib.emulator_close()


if __name__ == "__main__":
    emu = Emulator(Path(sys.argv[1]))
    try:
        for action in json.loads(Path(sys.argv[2]).read_text()):
            if "load_state" in action:
                emu.state(action["load_state"], True)
            if "frames" in action:
                emu.frames(action["frames"], action.get("keys", 0))
            if "press" in action:
                for _ in range(action.get("repeat", 1)):
                    emu.press(action["press"], action.get("wait", 30))
            if "read" in action:
                value = emu.read(action["read"], action.get("size", 4))
                print(action["read"], hex(value), flush=True)
                if "assert" in action:
                    assert value == action["assert"], action
            if "screenshot" in action:
                emu.screenshot(action["screenshot"])
            if "save_state" in action:
                emu.state(action["save_state"])
    finally:
        emu.close()
