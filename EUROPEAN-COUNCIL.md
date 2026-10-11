# European Council championship

Status: released in v3.3. All implementation items below are complete; see artifacts/releases/v3.3-VERIFICATION.json for exact coverage and limits.

The European Council is the tour's Elite Four equivalent. Four fictional Council members represent England, France, Germany and the shared European journey. A separate Council Champion is the fifth and final opponent. Country representatives may use ceremonial titles such as Crown, Regent or Warden; these are fictional tournament roles rather than claims about real governments.

This expands the earlier idea of three national opponents plus a Champion into a full four-member Council followed by a Champion.

## Defined finish

After reading Ada's main-story conclusion, the player can enter a clearly marked Council Hall. Defeating all four members in order and then the Champion records EUROPEAN COUNCIL CHAMPION in the save and shows an explicit championship conclusion. The existing main ending and Letters for Tomorrow remain independently complete and accessible.

## Implementation checklist

- [x] Create an accessible Council Hall with entry directions, a preparation area, free healing and a clear exit.
- [x] Add four distinct fictional Council members and a separate Champion, with teams balanced against the current game's available training and supplies.
- [x] Explain the battle order, difficulty, healing rules and defeat behavior before starting; allow declining entry.
- [x] Implement and save championship progress without reusing existing story, appearance or archive state.
- [x] Define defeat recovery and voluntary withdrawal so players can retry without losing existing quest progress.
- [x] Record the championship conclusion and a single completion reward; define repeat challenges separately.
- [x] Test entry gates, declining, all five victories, defeat/retry, withdrawal, rewards and native Save/Continue between stages.
- [x] Test compatibility using copies of existing player saves and check every starting country's access.
- [x] Update the walkthrough and publish the verified ROM with release evidence.

## Hall and opponents

London's reading room is the reception. From the outdoor door at (55,33), face UP, press A and enter. Inside, speak to the receptionist from (5,4), facing UP. After reading Ada's main conclusion, choose YES to enter the Hall. Older completed saves can unlock it by rereading Ada in Oxford.

The north row is the battle order, left to right:

| Match | Representative | Team and levels |
| --- | --- | --- |
| 1 | Alfred, England's Crown of the Skies | Pidgeotto 18, Noctowl 18, Furret 19 |
| 2 | Solene, France's Garden Regent | Butterfree 19, Weepinbell 19, Skiploom 20 |
| 3 | Otmar, Germany's Iron Warden | Magnemite 20, Voltorb 20, Machop 21 |
| 4 | Elara, Alliance River Guardian | Psyduck 21, Poliwhirl 21, Horsea 22 |
| 5 | Champion Rowan | Eevee 22, Pidgeotto 22, Ivysaur 22, Pikachu 23 |

Speak from (2,4), (4,4), (6,4), (8,4) and (10,4), respectively, facing UP. NO or B declines each match. An opponent later in the order directs you to the next available match.

## Preparation and recovery

Speak to nurse from (2,7), facing UP, for free HP, status and PP recovery. Speak to Coach Ivo from (6,7), facing UP, for repeatable practice against Sentret 14, Mareep 15 and Eevee 16. Practice heals before the match and after a victory, awards normal experience and trainer prize money, and leaves Council progress unchanged. Build a team around levels 22-25; the Hall shop at (4,7), facing UP, sells Super Potions for 700 each and status medicine at normal prices. Practice prize money helps fund supplies. Super Potions restore 50 HP; use BAG during battle. Bring partners with different types, especially a flying partner to cover a grass weakness.

A practical supporting partner is Pidgey, found in the grass of London's northern countryside. Catch it with an earned or purchased Poke Ball or Great Ball. The London, Paris and Berlin guides (approach from (16,14), facing DOWN) award the existing three-stamp tour's EXP. SHARE. Give that item to Pidgey through BAG, ITEMS, GIVE, then repeat Coach Ivo battles with your stronger starter leading. Shared experience trains Pidgey without requiring it to defeat the coach alone; it evolves into Pidgeotto at level 18. Train it further for the Council and let the nurse restore the whole party before matches.

Keep partners with different types. A flying partner helps against Solene's garden team and Rowan's Ivysaur; switch through the battle's POKEMON command. A water/ground starter has a severe grass weakness, so avoid leaving it against Ivysaur. Return to that starter against Pikachu, whose electric attacks cannot hit a ground type. A grass starter handles water opponents well. You can leave, catch partners and train midway through the circuit without losing victories.

The steward, approached from (10,7), facing UP, explains the rules and names the next opponent. Items work normally in battle. Losing sends the player to London's clinic under normal blackout rules, including money loss. Cleared matches survive; return through reception to retry the current match.

Save normally after any victory. Both south doorway tiles return to reception; its south doorway returns to London. Leaving pauses the circuit without erasing wins. Save/Continue also works in the Hall.

## Championship and replay

The fifth victory displays EUROPEAN COUNCIL CHAMPION and records a permanent title. The first championship awards one Rare Candy. With a full Bag, the title and fifth victory are already recorded; make space and speak to the steward to claim the pending candy without another battle.

After claiming that prize, the steward offers another five-match circuit. NO or B leaves the finished circuit unchanged. YES starts again with Alfred while retaining the permanent title and claimed-prize record. Battles award normal experience and trainer money during replays, but the championship candy is awarded only once.

Save state uses two previously unused persistent variables: 0x40CD stores circuit victories 0-5, and 0x40CE stores no title / title with pending prize / title with claimed prize as 0/1/2. Six trainer IDs 753-758 are appended within the existing 768-trainer flag allocation. The Hall is appended after every preexisting European map, preserving their saved IDs. No save-block size changes are required.
