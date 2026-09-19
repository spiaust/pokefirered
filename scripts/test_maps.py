"""Validate map links, door approaches, and reachable encounter areas."""
from collections import deque
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


def reachable(layout, start):
    width, height = layout["width"], layout["height"]
    raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
    assert len(raw) == width * height * 2
    tiles = struct.unpack(f"<{width * height}H", raw)
    # These outdoor prototypes share General/Pallet Town. Water is not a
    # walking route even when its map-block collision bits are zero.
    attr_data = (ROOT / "data/tilesets/primary/general/metatile_attributes.bin").read_bytes()
    secondary = "island_harbor" if layout["secondary_tileset"] == "gTileset_IslandHarbor" else "pallet_town"
    attr_data += (ROOT / f"data/tilesets/secondary/{secondary}/metatile_attributes.bin").read_bytes()
    attrs = struct.unpack(f"<{len(attr_data) // 4}I", attr_data)
    def walkable(block):
        behavior = attrs[block & 0x3FF] & 0x1FF
        return not block & 0xC00 and behavior not in (0x10, 0x11, 0x12, 0x13, 0x15, 0x19, 0x1A, 0x1B)
    seen, queue = {start}, deque([start])
    while queue:
        x, y = queue.popleft()
        for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if (0 <= xx < width and 0 <= yy < height and (xx, yy) not in seen
                    and walkable(tiles[yy * width + xx])):
                seen.add((xx, yy))
                queue.append((xx, yy))
    return seen


layouts = {item["id"]: item for item in load("data/layouts/layouts.json")["layouts"] if "id" in item}
groups = load("data/maps/map_groups.json")
maps = {name: load(f"data/maps/{name}/map.json") for name in groups["gMapGroup_Europe"]}
by_id = {value["id"]: value for value in maps.values()}
for name, value in maps.items():
    layout = layouts[value["layout"]]
    for event in value["warp_events"] + value["object_events"] + value["bg_events"]:
        assert 0 <= event["x"] < layout["width"], (name, event)
        assert 0 <= event["y"] < layout["height"], (name, event)
    for event in value["warp_events"]:
        destination = by_id[event["dest_map"]]
        assert 0 <= int(event["dest_warp_id"]) < len(destination["warp_events"]), (name, event)
    for connection in value["connections"] or []:
        destination = by_id[connection["map"]]
        assert any(back["map"] == value["id"] for back in destination["connections"]), name
    if name in ("EuropeBeauvaisGarden", "EuropeAmiensPast", "EuropeRouenPast", "EuropeLondonPast"):
        accessible = reachable(layout, (10, 16))
        for point in ((10, 16), (10, 15), (6, 9), (17, 6), (7, 9), (14, 15)):
            assert point in accessible, (name, "garden path unreachable", point)
        if name == "EuropeRouenPast":
            # Every formerly reachable tile remains safe for old battery saves.
            assert reachable(layouts["LAYOUT_EUROPE_AMIENS_PAST"], (10,16)) <= accessible
            for point in ((25,16),(25,9),(28,9),(33,9),(33,16),(33,6)):
                assert point in accessible, (name, point)
            for point in ((26,6),(29,12),(31,15)):
                assert point not in accessible, (name, "water walkable", point)
        if name == "EuropeAmiensPast":
            for point in ((13,9),(18,13),(19,13),(14,9)):
                assert point in accessible, (name, point)
        assert any(e["script"] == "EuropeTime_Return" for e in value["object_events"])
        assert any(e["script"] in ("EuropeGarden_Return", "EuropeAmiens_Return", "EuropeRouen_Return", "EuropeLondonPast_Return") for e in value["object_events"])
        assert not value["allow_cycling"] and not value["allow_escaping"]
    elif name in ("EuropeLeHavrePast", "EuropeSouthamptonPast"):
        accessible = reachable(layout, (8,5))
        assert (9,4) in accessible and (6,3) in accessible and (8,3) in accessible and (7,5) in accessible and (9,3) in accessible
        assert (8,2) not in accessible
        assert not value["warp_events"] and not value["allow_cycling"]
    elif name in ("EuropeChantillyPast", "EuropeChantillyPastPost"):
        accessible = reachable(layout, (5, 10))
        for point in ((5, 10), (5, 7), (8, 7), (11, 5), (12, 9)):
            assert point in accessible, (name, "past refuge path unreachable", point)
        assert any(e["script"] == "EuropeTime_Return" for e in value["object_events"])
        assert not value["allow_cycling"] and not value["allow_escaping"]
    elif value["map_type"] == "MAP_TYPE_TOWN":
        accessible = reachable(layout, (15, 14))
        exit_y = 23 if name in ("EuropeOxford", "EuropeChantilly", "EuropeOranienburg") else 0
        for point in ((6, 10), (23, 10), (15, exit_y), (19, 12), (12, 15), (15, 21)):
            assert point in accessible, (name, "unreachable", point)
        if name == "EuropeOxford":
            assert (18, 14) in accessible, "Celebi researcher is unreachable"
        if name in ("EuropeLondon", "EuropeOxford"):
            assert (24,16) in accessible and (22,15) in accessible and (26,16) in accessible and (25,17) in accessible, "Riverboat landing/sign unreachable"
        if name in ("EuropeOxford", "EuropeChantilly", "EuropeOranienburg"):
            assert (15, 10) in accessible, "Gym door is unreachable"
    elif value["map_type"] == "MAP_TYPE_ROUTE":
        accessible = reachable(layout, (15, layout["height"] - 1))
        assert (12, 16) in accessible and (20, 16) in accessible, name
        assert (17, 19) in accessible, (name, "trainer is unreachable")
        if name == "EuropeParisCountryside":
            assert (13, 17) in accessible, "Garden study marker is unreachable"
        if name == "EuropeChantillyTrail":
            assert (13, 21) in accessible, "Forest study marker is unreachable"
            assert (15, 24) in accessible, "Celebi sighting is unreachable"
        if name in ("EuropeLondonCountryside", "EuropeOxfordTrail",
                    "EuropeParisCountryside", "EuropeChantillyTrail",
                    "EuropeBerlinCountryside", "EuropeOranienburgTrail"):
            assert (15, 0) in accessible, (name, "northbound path is unreachable")
    print(f"PASS: {name}: links, event bounds, and required paths")
