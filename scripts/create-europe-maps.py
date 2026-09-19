"""Author the initial prototype maps from FireRed's existing metatiles.

Run once per new country. Existing maps are not overwritten; subsequent map
edits belong in data/maps and data/layouts (or Porymap).
"""
import copy
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2) + "\n")


def text(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value)


def object_event(script, x, y, graphic="MAN"):
    return dict(type="object", graphics_id="OBJ_EVENT_GFX_" + graphic,
                x=x, y=y, elevation=3, movement_type="MOVEMENT_TYPE_FACE_DOWN",
                movement_range_x=0, movement_range_y=0, trainer_type="TRAINER_TYPE_NONE",
                trainer_sight_or_berry_tree_id="0", script=script, flag="0")


def warp(x, y, destination, warp_id, elevation=0):
    return dict(x=x, y=y, elevation=elevation, dest_map=destination, dest_warp_id=str(warp_id))


def generate(city, country, route_name, species):
    name = "Europe" + city
    const = "EUROPE_" + city.upper()
    if (ROOT / f"data/maps/{name}/map.json").exists():
        raise SystemExit(f"{city} already exists; refusing to overwrite map edits")
    groups = read("data/maps/map_groups.json")
    if "gMapGroup_Europe" not in groups["group_order"]:
        groups["group_order"].append("gMapGroup_Europe")
        groups["gMapGroup_Europe"] = []
    names = [name, name + "Countryside", name + "Station", name + "Center"]
    groups["gMapGroup_Europe"].extend(names)
    write("data/maps/map_groups.json", groups)

    sections = read("src/data/region_map/region_map_sections.json")
    for suffix, title in [("", city.upper()), ("_COUNTRYSIDE", route_name.upper())]:
        sections["map_sections"].append(dict(id="MAPSEC_" + const + suffix, name=title,
                                           x=5, y=5, width=1, height=1))
    write("src/data/region_map/region_map_sections.json", sections)

    layouts = read("data/layouts/layouts.json")
    pallet = struct.unpack("<480H", (ROOT / "data/layouts/PalletTown/map.bin").read_bytes())
    for suffix in ("", "Countryside"):
        width, height = 32, 24
        tiles = [[0x3296 if not suffix else 0x3010 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                if x < 2 or x >= width - 2 or y < 2 or y >= height - 2:
                    tiles[y][x] = 0x400 | ((0x14 if y % 2 else 0x1C) + x % 2)
        # A broad, unobstructed path joins city and route.
        for y in (range(0, 3) if not suffix else range(height - 3, height)):
            for x in range(14, 18):
                tiles[y][x] = 0x3010
        if not suffix:
            # A health clinic and station ticket office, using existing house/lab art.
            for sx, sy, w, h, dx, dy in [(5, 3, 5, 5, 5, 5), (13, 9, 7, 5, 20, 5)]:
                for yy in range(h):
                    for xx in range(w):
                        tiles[dy + yy][dx + xx] = pallet[(sy + yy) * 24 + sx + xx]
            for x, y in [(5, 11), (22, 11), (14, 4)]:
                tiles[y][x] = 0x402
            # Flower beds make the central square distinct from Pallet Town.
            for y in (17, 18):
                for x in list(range(5, 11)) + list(range(22, 28)):
                    tiles[y][x] = 0x3004
        else:
            for y in range(5, 17):
                for x in list(range(5, 13)) + list(range(20, 28)):
                    tiles[y][x] = 0x300D
        # Finish exposed forest edges rather than showing cut interior tiles.
        forest_tiles = {0x14, 0x15, 0x1C, 0x1D}
        original = [row[:] for row in tiles]
        def forest(x, y):
            return (x < 0 or x >= width or y < 0 or y >= height
                    or original[y][x] & 0x3FF in forest_tiles)
        for y in range(height):
            for x in range(width):
                tile = original[y][x] & 0x3FF
                if tile not in forest_tiles:
                    continue
                right = tile in (0x15, 0x1D)
                if tile in (0x1C, 0x1D) and not forest(x, y - 1):
                    tile = 0x0F if right else 0x0E
                elif tile in (0x14, 0x15) and not forest(x, y + 1):
                    tile = 0x25 if right else 0x24
                if tile in (0x14, 0x1C, 0x24) and not forest(x - 1, y):
                    tile += 2
                if tile in (0x15, 0x1D, 0x25) and not forest(x + 1, y):
                    tile += 2
                tiles[y][x] = (original[y][x] & ~0x3FF) | tile
        layout_name = name + suffix
        layout_const = const + ("_COUNTRYSIDE" if suffix else "")
        folder = ROOT / f"data/layouts/{layout_name}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "map.bin").write_bytes(struct.pack("<768H", *(tile for row in tiles for tile in row)))
        (folder / "border.bin").write_bytes(struct.pack("<4H", 0x41C, 0x41D, 0x414, 0x415))
        layouts["layouts"].append(dict(id="LAYOUT_" + layout_const, name=layout_name + "_Layout",
            width=width, height=height, border_width=2, border_height=2,
            primary_tileset="gTileset_General", secondary_tileset="gTileset_PalletTown",
            border_filepath=f"data/layouts/{layout_name}/border.bin",
            blockdata_filepath=f"data/layouts/{layout_name}/map.bin"))
    write("data/layouts/layouts.json", layouts)

    town = read("data/maps/PalletTown/map.json")
    town.update(id="MAP_" + const, name=name, layout="LAYOUT_" + const,
                region_map_section="MAPSEC_" + const, music="MUS_PALLET",
                connections=[dict(map="MAP_" + const + "_COUNTRYSIDE", offset=0, direction="up")],
                object_events=[object_event(name + "_Guide", 16, 15, "WOMAN_1")],
                warp_events=[warp(6, 9, "MAP_" + const + "_CENTER", 0),
                             warp(23, 9, "MAP_" + const + "_STATION", 0)],
                coord_events=[], bg_events=[])
    for x, y, script in [(5, 11, "ClinicSign"), (22, 11, "StationSign"), (14, 4, "RouteSign")]:
        town["bg_events"].append(dict(type="sign", x=x, y=y, elevation=0,
            player_facing_dir="BG_EVENT_PLAYER_FACING_ANY", script=name + "_" + script))
    write(f"data/maps/{name}/map.json", town)
    route = copy.deepcopy(town)
    route.update(id="MAP_" + const + "_COUNTRYSIDE", name=name + "Countryside",
        layout="LAYOUT_" + const + "_COUNTRYSIDE", region_map_section="MAPSEC_" + const + "_COUNTRYSIDE",
        music="MUS_ROUTE1", map_type="MAP_TYPE_ROUTE", object_events=[], warp_events=[], bg_events=[],
        connections=[dict(map="MAP_" + const, offset=0, direction="down")])
    write(f"data/maps/{name}Countryside/map.json", route)
    station = read("data/maps/PalletTown_RivalsHouse/map.json")
    station.update(id="MAP_" + const + "_STATION", name=name + "Station",
        region_map_section="MAPSEC_" + const, object_events=[object_event(name + "Station_Clerk", 7, 6, "GENTLEMAN")],
        warp_events=[warp(x, 8, "MAP_" + const, 1, 3) for x in (4, 5, 3)], bg_events=[])
    write(f"data/maps/{name}Station/map.json", station)
    center = read("data/maps/ViridianCity_PokemonCenter_1F/map.json")
    center.update(id="MAP_" + const + "_CENTER", name=name + "Center",
        region_map_section="MAPSEC_" + const,
        object_events=[object_event(name + "Center_Nurse", 7, 2, "NURSE")],
        warp_events=[warp(x, 8, "MAP_" + const, 0, 3) for x in (6, 7, 8)], bg_events=[])
    write(f"data/maps/{name}Center/map.json", center)
    text(f"data/maps/{name}/scripts.inc", f'''{name}_MapScripts::
\tmap_script MAP_SCRIPT_ON_TRANSITION, {name}_OnTransition
\t.byte 0

{name}_OnTransition::
\tsetrespawn HEAL_LOCATION_{const}
\tend

{name}_Guide::
\tmsgbox {name}_Text_Welcome, MSGBOX_NPC
\tend

{name}_ClinicSign::
\tmsgbox {name}_Text_Clinic, MSGBOX_SIGN
\tend

{name}_StationSign::
\tmsgbox {name}_Text_Station, MSGBOX_SIGN
\tend

{name}_RouteSign::
\tmsgbox {name}_Text_Route, MSGBOX_SIGN
\tend

{name}_Text_Welcome::
\t.string "Welcome to {city.upper()}!\\n"
\t.string "The countryside lies to the north.\\p"
\t.string "Visit the clinic to heal, or stop\\n"
\t.string "by the station for a train.$"

{name}_Text_Clinic::
\t.string "POKEMON CLINIC\\nFree care for traveling partners.$"

{name}_Text_Station::
\t.string "{city.upper()} STATION\\nEuropean rail ticket office.$"

{name}_Text_Route::
\t.string "NORTH: {route_name.upper()}\\nWild POKEMON live in the tall grass.$"
''')
    text(f"data/maps/{name}Countryside/scripts.inc", f"{name}Countryside_MapScripts::\n\t.byte 0\n")
    text(f"data/maps/{name}Station/scripts.inc", f'''{name}Station_MapScripts::
\t.byte 0

{name}Station_Clerk::
\tmsgbox {name}Station_Text_Closed, MSGBOX_NPC
\tend

{name}Station_Text_Closed::
\t.string "Welcome to the rail ticket office!\\p"
\t.string "International services are being\\n"
\t.string "prepared. Please explore {city.upper()}.$"
''')
    text(f"data/maps/{name}Center/scripts.inc", f'''{name}Center_MapScripts::
\tmap_script MAP_SCRIPT_ON_TRANSITION, {name}Center_OnTransition
\tmap_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
\t.byte 0

{name}Center_OnTransition::
\tsetrespawn HEAL_LOCATION_{const}
\tend

{name}Center_Nurse::
\tlock
\tfaceplayer
\tcall EventScript_PkmnCenterNurse
\trelease
\tend
''')
    events = ROOT / "data/event_scripts.s"
    with events.open("a") as output:
        for map_name in names:
            output.write(f'\n\t.include "data/maps/{map_name}/scripts.inc"\n')
    heals = read("src/data/heal_locations.json")
    heals["heal_locations"].append(dict(id="HEAL_LOCATION_" + const, map="MAP_" + const,
        x=6, y=10, respawn_map="MAP_" + const + "_CENTER", respawn_npc="1"))
    write("src/data/heal_locations.json", heals)
    encounters = read("src/data/wild_encounters.json")
    encounters["wild_encounter_groups"][0]["encounters"].append(dict(map="MAP_" + const + "_COUNTRYSIDE",
        base_label="s" + name + "Countryside", land_mons=dict(encounter_rate=21,
        mons=[dict(min_level=2, max_level=4, species="SPECIES_" + species[i % len(species)]) for i in range(12)])))
    write("src/data/wild_encounters.json", encounters)


if __name__ == "__main__":
    choices = {
        "London": ("England", "ENGLISH MEADOW", ["PIDGEY", "RATTATA", "MAREEP", "ODDISH"]),
        "Paris": ("France", "FRENCH GARDENS", ["CATERPIE", "ODDISH", "ROSELIA", "RALTS"]),
        "Berlin": ("Germany", "GERMAN WOODLAND", ["SENTRET", "HOOTHOOT", "TEDDIURSA", "PINECO"]),
    }
    city = sys.argv[1]
    generate(city, *choices[city])
