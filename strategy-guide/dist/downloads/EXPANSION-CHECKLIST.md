# Expansion checklist

The defined main game is finished in v3.0. Its release, ending, walkthrough and verification evidence remain the baseline. Expansion work proceeds in this order.

- [x] Expand World Options scenery controls. First: independent flower motion control, native saving, reset defaults and unchanged terrain/progression.
- [x] Expand character customization with coherent walking/bicycle previews and saved preferences.
- [x] Add custom mount visuals and verify travel, dismounting and saved games.
- [x] Define and implement the next Celebi story chapter, including objectives, locations and its own conclusion.
- [x] Run fresh-game and existing-save regression tests, update the walkthrough and publish a verified expansion build.
- [x] Add the European Council championship described in [EUROPEAN-COUNCIL.md](EUROPEAN-COUNCIL.md): four Council battles followed by the Champion, unlocked after the existing main ending.
- [ ] Coordinate USA companion transfer after a companion game is created and supplies its engine, save format and transfer requirements. Deferred: the user confirmed on 2026-10-10 that no companion folder/repository exists yet.

## Release requirements

Preserve the original player saves. Keep v3.0 archived. Publish only tested expansion builds; report partial coverage and unfinished features accurately.

## First expansion release

Version v3.1 adds the independent flower motion control. Sixteen native checks and a copied Austin Save/Continue check passed. The complete v3.0 journeys remain baseline evidence; the full story was not replayed for this cosmetic-only release. Character customization was the next item after v3.1.

## Verified local expansion release

Version v3.2 completes the four remaining local expansion items: saved skin/accent customization, original Lapras riding frames, the optional Letters for Tomorrow chapter and release regression/package validation. 207 passing checks plus Austin's copied Save/Continue check cover this exact ROM. Three fresh country journeys reached the main ending; both archive country orders reached the expansion ending. Original player saves and the finished v3.0 release are unchanged.

USA transfer is deferred: the user confirmed that the companion game has no folder/repository yet. Its engine, save format and protocol must be defined before integration. See [USA-TRANSFER-REQUIREMENTS.md](USA-TRANSFER-REQUIREMENTS.md). Additional hair geometry, mount species, countries and wartime districts remain possible future scope rather than implemented features in v3.2.

## European Council release

v3.3 completes the local expansion checklist with four Council members, Champion Rowan, free care, repeatable training, a supply shop, saved victories and a permanent title. 252 check results plus the copied Austin Save/Continue verification passed. Every starting country reached the main ending on this ROM; all three country teams completed the Council using native training and battles. Full-bag recovery, defeat/retry, withdrawal and a complete replay passed. Original saves remain unchanged. USA transfer is deferred because the companion project does not exist yet. See [Council walkthrough](EUROPEAN-COUNCIL.md) and [release verification](artifacts/releases/v3.3-VERIFICATION.json).
