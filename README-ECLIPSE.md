# Pokemon Europe: Eclipse

A separate native FireRed GBA campaign in `S:/pokemon-europe-shadow`. Play
`Pokemon-Europe-Eclipse.gba` in a GBA emulator and start a NEW GAME. Original
European Tour saves are not supported by this campaign. The original folder
and its player saves are preserved.

## Starting your journey

Choose England, France or Germany, then one of that country's three starters.
Speak to Oak's aide in London, the Paris guide, or the Berlin guide to enter
Eclipse. They also resume your chapter after a blackout. Germany's story uses
a resistance double-agent cover; nationality does not determine allegiance.

The 21-chapter campaign has eight badge battles, a recurring rival who chooses
and evolves a counter-starter, Team Eclipse, WWII resistance operations, four
League council members, a champion match and credits. Six shadow partners can
be rescued and purified. The opening rival uses one level-six counter-starter
with a basic attack; later rival battles use full teams and moves. Route trainers and rival practice matches are repeatable.

Each shelter provides a nurse, mission opponent, previous/next chapter porters,
route guide, shop, rescue partner, purification keeper and storage attendant.
Every country district also offers native storage access in both eras. Catch
partners in route grass and swap teams locally. Save normally
through the Start menu. Town Map, SELECT opens chapter guidance; A shows records.

## Gym technique rewards

Each badge leader also gives one themed TM. The native TM Case is supplied
with your first TM. Talk to a previously defeated leader to claim a missing
reward; if your bag cannot accept it, make space and return. Used TMs cannot
be reclaimed from the leader.

| Gym | TM reward |
| --- | --- |
| London | Rock Tomb |
| Paris | Water Pulse |
| Brussels | Bullet Seed |
| Amsterdam | Shock Wave |
| Berlin | Brick Break |
| Vienna | Calm Mind |
| Rome | Overheat |
| Madrid | Earthquake |

## Countries and time travel

The station attendant at the shelter's lower left opens a six-region destination
menu. There are 39 European destinations with their own compact city district,
landmark, present and wartime map, local trainers and services. These add 78 maps
to the campaign's 42 maps and bring the new trainer-team total to 276. Country
Town Maps show a scrollable passport with cities, landmarks and memory status.

After chapter 12 unlocks the time anchors, speak to Celebi in a country district
to switch eras in either direction. Wartime scenery and people use sepia colors.
Win that district's wartime operation, then ask its keeper to choose a refuge
garden or research archive. Returning to the present changes dialogue, ground
tiles, an eastern shortcut and an encounter slot. The choice persists and is
made once per country. Complete all 39 memories and visit Ada in the champion
shelter for the rescue-network epilogue and a one-time Master Ball.

Neutral-country historical operations are friendly keeper battles. Other
operations oppose fictional Nazi infiltrators; their presence is not a claim
that every represented city was occupied. Contemporary country names make
navigation clear; WWII-era Soviet and Yugoslav regions are discussed as such.
The story protects communities without claiming to erase real WWII history.
The USA is reserved for a later expansion.

## World Gear settings

The campaign contact gives you WORLD GEAR and a Town Map. World Gear controls
appearance and these gameplay settings at any time:

- Normal is the default. Easy lowers new campaign trainer levels by four;
  Hard raises them by five. Rival partner IVs also change with difficulty.
- Nuzlocke is optional and independent of difficulty. Only the first wild
  encounter in a European area permits capture; both country eras share an
  allowance. Rejected capture attempts explain the rule and refund the Ball.
  Fainted partners are marked retired and cannot be healed while
  enabled, including after a blackout or PC storage. Gifts and rescues are
  allowed. Disabling the mode allows healing; re-enabling retires marked
  partners again. This variant does not force nicknames or release partners.
- Visible wild encounters default ON. Native encounter weights and rates
  choose their species and level. Walking retries absent spawns every eight
  steps. Switch them OFF for classic grass encounters. Actors occupy defined
  encounter points rather than roaming; interact to start a real wild battle.

Visible sprites cover all 62 species in the new encounter tables, using native
sprites and original small adaptations of the base's Pokemon icons.

Amsterdam's leader explains how a Belgian NIDORAN can become NIDORINA
and then evolve with a Moon Stone into a Ground-type NIDOQUEEN. Country
travel and the shared shops let you prepare a team before challenging the gym.

Berlin's leader recommends Flying or Psychic moves against her Fighting team.
The earlier Brussels routes remain available for training a Flying partner
until it learns a stronger attack.

## Supplies and evolution

Every campaign shelter and country shop sells all six evolution stones at
2,100 each, plus the complete set of status cures, Max Potions and Full Restores.
Native item-use and evolution rules apply: a shadow partner refuses a stone
without consuming it, and a purified partner can evolve normally.

## Shadow partners

Six rescue rewards require a free party slot. Shadow status persists through
PC storage and saves, adds 25% outgoing and incoming base damage, blocks
evolution and gives a purple battle palette. Care adds ten friendship per
session; at 120 friendship the keeper purifies the partner and awards the
purification ribbon. Normal friendship events also help. SHADOW and HEALED
nicknames identify rescue status. Snagging and a new Shadow move type are not
part of this ruleset.

## Scandinavian remnant hunt

After the League ending, meet Ada northeast of Copenhagen's landmark. Accept
her investigation, defeat Vex in Copenhagen, Rime in Oslo and Boreal in Stockholm,
then return to Ada. Their three relays threaten the northern rescue network and
its guardians. Opponents have three, three and four shadow partners at Normal
levels 62, 64 and 66, with curated four-move sets, held items and stronger AI.
Easy lowers levels by four; Hard raises them by five without replacing movesets.

The hunt saves each victory independently and leaves the main ending complete.
Declining does not advance it. Defeated commanders cannot be farmed. Ada gives
one Shadow Ball TM; a full TM stack leaves it pending until there is room.
Completed saves retain the hunt, reward and open League/travel facilities.

## Legendary guardians

Guardians appear as native overworld Pokemon in the present-day country districts.
Their landmark signs describe the location and unlock condition. These are real
wild battles with normal catch rates and moves. Declining, fleeing or knocking
out a guardian leaves it available for another attempt; a successful catch
removes it permanently through a saved flag. Full-party catches go to the PC.
Optional Nuzlocke still uses that country's first-encounter allowance, shared
with its historical era. Repeat attempts can be caught after disabling Nuzlocke.
Celebi remains the time-travel guide so catching a guardian cannot break travel.

| Phase | Guardian | Destination | Level | Unlock |
| --- | --- | --- | --- | --- |
| Before League | Articuno | Reykjavik, Iceland | 40 | Sixth badge, Vienna completed |
| Before League | Zapdos | Oslo, Norway | 45 | Seventh badge, Rome completed |
| Before League | Moltres | Rome, Italy | 45 | Eight badges, Madrid completed |
| Postgame | Suicune | Helsinki, Finland | 60 | League ending |
| Postgame | Lugia | Valletta, Malta | 65 | League ending |
| Postgame | Ho-Oh | Vienna, Austria | 65 | League ending and three purified rescues |
| Postgame | Mewtwo | Berlin, Germany | 70 | League ending and all six purified rescues |

The postgame production roadmap is tracked in [TODO-ECLIPSE.md](TODO-ECLIPSE.md).
It includes the Scandinavian Eclipse-remnant hunt, Krakow sanctuary restoration
and a true champion rematch circuit. The hunt is implemented; Krakow restoration and the rematch circuit remain planned.

## Build and verification

Run `powershell -File scripts/build-windows.ps1` with the base WSL/agbcc tools.
The native build produces a 16 MiB ROM and the Eclipse release alias. Read
STORY-ECLIPSE.md for the campaign and country roster, RESEARCH-ECLIPSE.md for
repository provenance, and TESTING-ECLIPSE.md for actual validation and limits.
The districts are compact, with stylized landmarks and shared League shelters.
A full natural-level balancing playthrough remains a release-quality check.
