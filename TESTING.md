# Prototype verification — 2026-09-18

## London architecture: next facade scope and baseline

Two fresh baseline PASS results from test_london_facade_static.py confirm the current eastern roof remap retains every tile attribute/native artwork and shared palettes, with distinct roof shades and transparency. This is pre-change baseline evidence for the planned western-home facade, not verification of new artwork. Four original player saves and the canonical v1.71 ROM remain unchanged.

## v1.71: player-save compatibility and current limitations

Current v1.71 player-save compatibility revalidated with test_current_user_save.py. Original 131088-byte battery copied into test-output only; native Continue loads Austin in Paris at (43,4,10,42), Chikorita species152 level10 and money3176. Party and Bag menus preserve state; normal Save and cold Continue retain exact party, inventory, money and location on the isolated copy. Original SHA256 remains 6d5d0a61107e998cc71da49570f3db09de562dc00822a16d2155e092ef76a674. All four protected original saves and all current ROM copies retain their hashes. This confirms emulator-core compatibility and normal save pairing; it does not claim a desktop emulator is currently running. Documentation limitations reconciled with completed releases; no gameplay changes or rebuild.

## v1.71: completed map and journal navigation verification

21 fresh runtime PASS results in test_current_navigation.py. Genuine current-services-complete travels normally through all six modern towns, then Celebi refuge, Le Havre, Southampton and London 1940. Ten sites check current map selection and era, map selection after eight LEFT/RIGHT inputs, complete historical lead58/mask1048575, both history pages, completed tour lead24/checklist, topic switching/reset and read-only exits. Registered SELECT shortcut opens the map and exits journal records with both B and START while restoring field controls. Native saves/cold Continue retain exact party, inventory, money, variables 40C0..40FF and location at each site; modern site checks explicitly retain registered item361, and historical shortcut behavior is exercised after preceding reloads. Final native historical return, saved Ada ending and complete cumulative state remain intact. No memory writes, inventory edits, progression injection or emulator state loads. ROM, symbols and four original player saves remain unchanged. Full fresh-game walkthrough evidence remains v1.15.

## v1.71: completed station shops and clinics verification

19 fresh runtime PASS results in test_current_services.py. The genuine current-interiors-complete journey travels normally through London, Paris, Berlin, Oxford, Chantilly and Oranienburg. Each station verifies purchase-confirmation B leaves exact saved state unchanged; two Poke Balls cost 400 and one Potion costs 300, with exact inventory deltas and unchanged party and variables 40C0..40FF. Each shop purchase saves/cold Continues indoors and exits to the correct town. Each clinic saves/cold Continues indoors, provides free full-HP/status care while retaining party identity, money, inventory and completed progress, saves/cold Continues after healing and exits correctly. Final native rail return to Oxford, saved Continue and repeated Ada conclusion retain the cumulative purchases and completed activities. No memory writes, inventory edits, progression injections or emulator state loads. This checks native care on the genuine current party; it does not inject damage/status or claim a new battle-recovery test. ROM, symbols and four original player saves remain unchanged. Full fresh-game walkthrough evidence remains v1.15.

## v1.71: completed Bicycle and visitor interiors verification

35 fresh runtime PASS results: Bicycle 3, capital homes 10 and remaining visitor interiors 22. Genuine current-lapras-complete continues through current-bicycle-complete, current-rooms-complete and current-interiors-complete, with native controls and battery cold Continue only. Bicycle riding persists after saving; normal Key Items use dismounts and saves walking correctly. Three capital homes and seven reading/garden/landmark visitor rooms retain exact saved location, party, inventory and all variables 40C0..40FF. Entry No/B, host/notebook/display readings, both front exit tiles and re-entry are checked. Each suite returns normally to Oxford and repeats Ada conclusion without changing completed progress. Stationary checks compare exact party; walking may legitimately change friendship. No memory writes, progress injections, inventory edits or emulator state loads. ROM, symbols and four original player saves remain unchanged. Full fresh-game walkthrough evidence remains v1.15.

## v1.71: completed stamp tour and transport verification

32 fresh runtime PASS results: stamps 9, coast 9, riverboat 6, Lapras 8. Native controls continue current-landmarks-all-complete through current-stamps-complete, current-coast-complete, current-riverboat-complete and current-lapras-complete without state loads, memory writes, inventory edits or progression injections. All three city stamps save/cold Continue; the third grants one Exp. Share and repeats grant none. Journal tour checklist is read-only. Both coach/Channel-ferry directions retain progress and report correct port maps; both London/Oxford riverboat directions retain exact state and permit mounted boarding. Both Lapras rentals preserve party identity, remain surfing after cold Continue, allow steering/shore dismount/repeated rental and handle Bicycle boarding. Every transport suite verifies all variables 40C0..40FF after final native save/cold Continue and repeat Ada ending; stamps guard every variable except the four intentionally advanced stamp/reward variables. Walking may legitimately change friendship; stationary checks compare exact party bytes. Four original player saves, ROM and symbols are unchanged. Full fresh-game walkthrough evidence remains v1.15.

## v1.71: cumulative ending and walkthrough recovery verification

Ten fresh runtime PASS results rerun test_current_journey_ending.py (three) and test_current_landmark_completion.py (seven) on unchanged v1.71. Genuine saved final journey reaches Ada through native travel, retains all twenty historical journal milestones (mask1048575), and remains playable through direct Southampton and historical London revisits/free care/cold Continue. The same cumulative player then completes all three optional cases with native rail travel, both clue orders, No/B, exact one-time Spell Tag/Rare Candy/three Great Balls rewards, repeated ledger/curator and saved state. Shared synthesis appears at curator/ledger/Ada without resetting completed historical progress. No memory writes, inventory edits, party substitutions or progress injections occur in these cumulative suites. Walkthrough reward-recovery section is based on separately archived v1.71 boundary-fixture native Bag tests; full New Game evidence remains v1.15. Current ending/synthesis screenshots visually inspected. ROM, symbols, four user saves and all previously archived release evidence remain unchanged.

## v1.71: Landmark reward pocket recovery and Gastly choices

Nineteen fresh PASS results: exact shared pending-reward text addition/native font width (two), fifteen native recovery checks across five boundaries (Notre-Dame and Westminster Items full and reward stack999, Reichstag Great Ball stack999 requiring three spaces), and two native optional Gastly checks (No/B/cold Continue and actual level12 encounter/ordinary Run/saved repeat). Separate fixture generator explicitly edits only the named pocket on genuinely resolved current-landmarks case batteries, preserving all other pockets, party, money and progression. Five fixtures are labelled FIXTURE rather than PASS; no earned stages are injected. Runtime capacity and Gastly scripts perform no memory writes. Each capacity case checks four help pages, unchanged pending reward/repeats/cold Continue, native Toss B cancellation, exact removal of one or three, saved room and actual one-time reward without duplication. Great Ball test covers stack capacity; no full unique-ball pocket is claimed. Gastly is encountered and escaped normally; no capture is claimed. New help and battle screens visually inspected. Full historical ending evidence remains v1.15; fresh cumulative ending/landmark evidence remains v1.70, and music/splash evidence remains v1.25. All four user saves and archived v1.70 ROM remain unchanged.

## v1.70: optional landmark completion and ending verification

Seven fresh runtime PASS results in test_current_landmark_completion.py use genuine current-ending-revisited battery and native rail travel to all three landmarks. Each case tests entry/request No/B, early attendant gates, both real clue orders (with a saved accepted baseline for the alternative branch), repeated clues and cold Continue. Native peaceful resolution No/B then Yes earns one Spell Tag, one Rare Candy or three Great Balls, with only the expected pocket count change and exact stationary party/money/progress. Saved curator/ledger repetitions and exit/re-entry duplicate no reward. The same final player journey retains all three completed cases, shared synthesis at curator/ledger/Ada and read-only final journal lead 58/mask1048575 with page/topic controls. Native Oxford return and cold Continue preserve all historical variables and the ending. No memory writes, inventory edits, party substitutions or progress injections. Optional cases are recorded in the landmark field-notes ledger; the separate historical journal retains its twenty completed records. This is cumulative post-ending optional-case verification, not a new full New Game run. Synthesis and Ada ending screenshots visually inspected. Current/archived v1.70 ROM, matching symbols and all four user saves remain unchanged.

## v1.70: final journey ending and player-save verification

Three fresh runtime PASS results in test_current_journey_ending.py use genuine v1.70 london-directions-report-ready battery, both port accounts already normally recorded. Actual Celebi return/Chantilly/Oxford travel reaches Ada; five conclusion pages repeat after native Save/cold Continue with exact party/items/money and all variables 40C0..40FF unchanged. Journal lead 58 and all twenty historical milestones (mask 1048575) pass read-only page/topic controls and cold Continue. Native direct Southampton return, free care and historical London revisit remain playable; actual return to Ada and cold Continue preserve the ending. No memory writes, inventory edits, party substitutions or progress injections. This is final-chapter verification from the genuine cumulative journey, not a new full New Game run. Additionally test_current_user_save.py loads a copy of the original player battery on v1.70, verifies native Continue/Party/Bag, saves the copy and cold-continues with exact state; original remains unchanged. Ending and player-save screenshots visually inspected. Current/archived v1.70 ROM, matching symbols and all four user saves remain unchanged.

## v1.70: Historical London arrival and report return directions

Five fresh PASS results: exact London journey/completed reminder additions and native font width (two), actual missing-luggage travel gate and completed luggage boarding No/B/cold Continue (one), three journey pages and actual London arrival/saved state/return No/B and actual Southampton round trip before registration (one), actual Rose welcome/saved registration/six completed reminder pages/exact stationary party-items-money/saved repeated talks (one). Sources are genuine v1.66 south-directions-returned and v1.69 south-account-directions-returned batteries. No memory writes, inventory edits, party substitutions or progress injections. New instruction pages visually inspected. The final Oxford report is the next milestone; no full historical ending rerun is claimed here. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25. All four user saves and archived v1.69 ROM remain unchanged.

## v1.69: Southampton account and direct-return directions

Five fresh PASS results: exact luggage-unlocked/account reminder additions and native font width (two), real luggage hand-in/seven hand-in-care-report pages/native Oxford trip/optional Le Havre report then Southampton No/B/cold Continue (one), native Southampton report/eight record-reminder pages/exact stationary party-items-money/saved repeated archive (one), Celebi initial No/B/menu B-Exit/all three destinations/actual free care/repeated direct Southampton/cold Continue with luggage absent (one). Source is genuine v1.67 luggage-directions-found battery, with neither port account recorded. No memory writes, inventory edits, party substitutions or progress injections. Care validates identity, full HP/status/PP and unchanged inventory/money/progress without tired-party fixtures. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.68 ROM remain unchanged.

## v1.68: Port account and direct Le Havre return directions

Five fresh PASS results: exact dock-unlocked/account reminder additions and native font width (two), real captain confirmation/eight confirmation-care-return pages/native Oxford trip/archive No/B/cold Continue (one), native Ada report/seven record-reminder pages/exact stationary party-items-money/saved repeated archive (one), unlocked Celebi initial No/B/menu B-Exit/refuge/direct Le Havre/actual free care/repeated direct travel/cold Continue (one). Source is genuine v1.65 dock-directions-noted battery, before Southampton/luggage. No memory writes, inventory edits, party substitutions or progress injections. Care validates identity, full HP/status/PP and unchanged inventory/money/progress without tired-party fixtures. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.67 ROM remain unchanged.

## v1.67: Southampton luggage recovery directions

Five fresh PASS results: exact two luggage reminder additions and native font width (two), absent luggage/No/B/actual acceptance/two active pages/cold Continue (one), actual west-quay pickup/three return pages/exact stationary inventory/saved removed object (one), actual worker hand-in, care/return No/B, actual free care and saved repeated care plus Le Havre round trip with luggage absent (one). Source is genuine v1.66 south-directions-returned battery. No memory writes, inventory edits, party substitutions or progress injections. Care validates identity, full HP/status/PP and unchanged inventory/money/progress without tired-party fixtures. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.66 ROM remain unchanged.

## v1.66: Southampton crossing and arrival directions

Five fresh PASS results: exact crossing/welcome additions and native font width (two), actual unconfirmed dock gate and confirmed crossing No/B/cold Continue (one), three crossing pages and actual arrival/saved host prerequisite with early worker and absent bag (one), four host welcome pages and return B, saved welcome, luggage search/return No/B, actual Le Havre round trip and cold Continue without forced luggage acceptance (one). Sources are genuine v1.65 dock-directions-active and dock-directions-rested batteries. No memory writes, inventory edits, party substitutions or progress injections. Exact stationary party/items/money comparisons accompany crossing and welcome. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.65 ROM remain unchanged.

## v1.65: Le Havre dock-notice directions

Five fresh PASS results: exact two dock reminder additions and native font width (two), early notice/No/B/actual request/two active direction pages/cold Continue and early captain gate (one), actual posted-notice reading/six notice-ready pages/repeated worker and notice/cold Continue (one), actual captain confirmation, care/return No/B, actual free care and saved repeated care plus Rouen round trip (one). Source is genuine v1.64 havre-directions-returned battery. No memory writes, inventory edits, party substitutions or progress injections. Exact stationary party/items/money comparisons accompany request and notice; care validates identity, full HP/status/PP and unchanged inventory/money/progress without tired-party fixtures. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.64 ROM remain unchanged.

## v1.64: Le Havre departure and arrival directions

Five fresh PASS results: exact journey/welcome additions and native font width (two), actual unreturned-book travel gate and completed-book boarding No/B/cold Continue (one), three journey pages and actual arrival/saved captain prerequisite with early worker and notice (one), four captain welcome pages and return B, saved welcome, dock request/return No/B, actual Rouen round trip and cold Continue without forced dock acceptance (one). Sources are genuine v1.63 book-directions-active and book-directions-rested batteries. No memory writes, inventory edits, party substitutions or progress injections. Exact stationary party/items/money comparisons accompany journey and welcome. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.63 ROM remain unchanged.

## v1.63: Rouen route-book recovery directions

Five fresh PASS results: exact search/pickup reminder additions and native font width (two), absent book before request, optional No/B, real acceptance/four search pages/cold Continue (one), actual paved crossing/far-bank pickup/three return pages/exact stationary inventory and saved removal (one), native Leon hand-in, rest No/B, actual free care/repeated care after cold Continue, saved completion and actual Amiens round trip with book absent (one). Source is genuine v1.62 rouen-directions-book-offer battery. No memory writes, inventory edits, party substitutions or progress injections; native care checks identity, full health/PP and unchanged inventory/money/progress without tiring-party fixtures. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.62 ROM remain unchanged.

## v1.62: Rouen onward journey and arrival directions

Five fresh PASS results: exact journey/welcomed text additions and native font width (two), real checked-but-undelivered bulletin gate plus delivered departure notice/No/B/cold Continue (one), three journey pages and actual boarding/saved arrival/return No/B and actual Amiens round trip before registration (one), six Leon welcome pages registering arrival and introducing the book, repeated optional search No/B and cold Continue without acceptance (one). Sources are genuine v1.61 news-directions-checked and news-directions-returned batteries. No memory writes, inventory edits, party substitutions or progress injections. Exact stationary party/items/money comparisons accompany journey and welcome. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.61 ROM remain unchanged.

## v1.61: Amiens bulletin and checked-news directions

Five fresh PASS results: exact two reminder-only additions and native font width (two), two active reminder pages/early Nora gate/cold Continue (one), actual notice reading/saved copied instructions/early Nora gate/four verification-reminder pages/saved repeated checked news (one), actual Nora delivery with optional rest and return declines, persistent reunited Meowth, actual station round trip and cold Continue (one). Source is genuine v1.60 account-directions-news-active battery. No memory writes, inventory edits, party substitutions or progress injections. Exact stationary party/items/money comparisons accompany reminder and verification. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.60 ROM remain unchanged.

## v1.60: Amiens reunion account and news unlock

Five fresh PASS results: exact two completion/reminder-only additions and native font width (two), six Mira completion pages and actual Celebi/Chantilly/Oxford journey with archive No/B and cold Continue (one), native Ada acceptance and six record/reminder pages plus repeated saved archive with exact stationary party/items/money (one), actual return to Amiens, persistent relocated Meowth, account prerequisite, porter No/B and actual bulletin acceptance with cold Continue (one). Source is genuine v1.59 reunion-directions-complete-mira battery. No memory writes, inventory edits, party substitutions or progress injections. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.59 ROM remain unchanged.

## v1.59: Amiens Meowth reunion directions

Five fresh PASS results: exact two reminder-only additions and native font width (two), optional reunion No/B, real acceptance/three direction pages and cold Continue (one), Mira-first (one) and porter-first (one) native reports, repeated witnesses, saved intermediate and verified stages, two verified-reminder pages, actual Mira reunion and cold Continue with relocated Meowth. Completed Nora rest is declined. Source is genuine v1.58 amiens-directions-returned battery. No memory writes, inventory edits, party substitutions or progress injections. New instruction pages visually inspected. A too-long line was shortened before building; final static check passes. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.58 ROM remain unchanged.

## v1.58: Amiens arrival and meeting directions

Five fresh PASS results: exact two text-block-only additions and native font width (two), optional boarding plus three arrival pages and saved early-notice gate (one), actual Nora welcome and six meeting-notice pages including return reminder with saved notes (one), actual Nora confirmation and optional return choices, round trip and cold Continue (one). Source is genuine v1.57 garden-directions-amiens-offer battery. No memory writes, inventory edits, party substitutions or progress injections. Original task stages and gates remain intact; repeated completed Nora conversations decline the separate reunion offer. New instruction pages visually inspected. Full historical ending evidence remains v1.15 and music/splash evidence remains v1.25; neither full suite rerun is claimed. All four user saves and archived v1.57 ROM remain unchanged.

## v1.57: Garden reunion and onward directions

Six fresh PASS results: exact garden carry/completed-reminder-only text additions and native font width (two), optional garden/Luc No/B with actual search acceptance/repeats/cold Continue (one), genuine northeast Pidgey interaction/two carry pages/saved carrying state and removed wild object (one), native return to Luc/four onward pages/repeated Luc and home-bird interactions/cold Continue with reunited object present and wild object absent (one), normal garden guide/reception return service to dispatcher and Amiens No/B/cold Continue (one). Source is genuine v1.56 relief-directions-rested battery. No memory writes, inventory edits, party substitutions or progress injections. Garden stages 1, 2 and 3 follow acceptance, actual bird interaction and Luc reunion. Onward journey stays unstarted on declines. An initial driver checked an offscreen bird from the entrance; checks now inspect bird visibility at the tree and beside Luc. Walking comparisons permit native friendship changes while other progression state stays exact; stationary and saved checks remain exact. Final runtime reran from the genuine source. All six instruction pages visually inspected. No full historical ending rerun is claimed; full-story evidence remains v1.15 and music/splash evidence remains v1.25. All four user saves and archived v1.56 ROM remain unchanged.

## v1.56: Beauvais relief directions

Five fresh PASS results: exact two-relief-direction text additions and native font width (two), normal travel back to Beauvais with host No/B/real acceptance and three route pages/repeats/cold Continue (one), actual south return service/dispatcher collection with two boarding-and-host pages/repeats/cold Continue (one), normal board/train/host delivery and care-corner No/B/native Yes/repeated free full-HP/PP rest/cold Continue (one). Source is genuine v1.54 message-directions-claimed battery. No memory writes, inventory edits, health fixtures, party substitutions or progress injections. Relief stage 1 follows acceptance, 2 follows parcel collection, and 3 follows actual host delivery. Native rest preserves non-health identity, money, items, badges and present story state; healed state saves exactly. The parcel is carried through the existing quest stage with no Bag addition or charge. All five instruction pages visually inspected. This suite does not rerun the full historical ending; full-story evidence remains v1.15 and music/splash evidence remains v1.25. All four user saves and archived v1.55 ROM remain unchanged.

## v1.55: Pending Luxury Ball guidance

Five fresh PASS results: exact pending-Luxury-Ball-only text addition and native font width (two), capped-stack four-page reminder/repeats/cold Continue (one), native Poke Balls pocket Toss cancellation/confirmation and saved room (one), actual Ada reward claim/stage completion/repeats/cold Continue (one). Separate fixture generator starts from genuine v1.54 message-directions-account, returns normally through Celebi and the Oxford train, then explicitly edits only 13 Poke Balls slots to Luxury Ball 999 with other ball slots empty. All other pockets, account stage, party, money and badges remain unchanged. This is an isolated inventory boundary fixture, not naturally collecting 999 balls. Runtime recovery performs no memory writes. Native Toss B cancellation preserves the stack; confirming removes one ball, and stage 3 plus space survive saved reload. Actual Ada talk returns the stack to 999 and sets message stage 4; repeats/reloads add no duplicate. Text mentions Give, but this suite exercises Toss. Four message pages visually inspected. No full-pocket or full-ending claim is made. All four user saves and archived v1.54 ROM remain unchanged. Full-story evidence remains v1.15 and music/splash evidence remains v1.25.

## v1.54: Elise message and reply directions

Six fresh PASS results: exact three message-direction additions plus two keeper-pronoun corrections and native font width (two), native Elise No/B/real acceptance with three delivery pages/repeats/cold Continue (one), normal return service/guide and actual keeper delivery with four reply-route pages/repeats/cold Continue (one), normal boarding back to Elise and actual reply handoff with three Ada-return pages/repeats/cold Continue (one), native Celebi return/Oxford train to Ada and one-time Luxury Ball/repeats/cold Continue (one). Source is genuine v1.53 beauvais-directions-checked-in battery. No memory writes, inventory edits, party substitutions or progress injections. Message stages 1, 2, 3 and 4 are earned normally; no early Ball is granted. All ten instruction pages visually inspected. The keeper is an old-woman character and original message dialogue uses she/her; two recently added him instructions were corrected. Current player save remains protected by hash checks; the separate v1.53 validation previously confirmed Austin's level-10 Chikorita save can Continue, use Party/Bag and save/reload a copy. No new full historical ending run is claimed; full-story evidence remains v1.15 and music/splash evidence remains v1.25. All four user saves and archived v1.53 ROM remain unchanged.

## v1.53: Beauvais boarding directions

Five fresh PASS results: exact keeper completed-report-only text addition and native font width (two), four-page keeper boarding lead/repeats/cold Continue (one), normal station guide/boarding board with No/B and saved readiness followed by actual Beauvais arrival, host-gated check-in/repeats/cold Continue and optional Elise follow-up decline (one), normal south-exit train return, refuge guide, Celebi return and saved home state (one). Source is genuine v1.52 departure-directions-reported battery. No memory writes, inventory edits, party substitutions or progress injections. Evacuation stage 0 remains unchanged on declines, actual boarding sets stage 1 and host check-in sets 2. Elise's follow-up stays unaccepted. Refuge help and confirmed news remain complete. Walking comparisons permit native friendship changes; money, inventory, badges and present report state remain exact. All four keeper instruction pages visually inspected. No full historical ending rerun is claimed; full-story evidence remains v1.15 and music/splash evidence remains v1.25. All four user saves and archived v1.52 ROM remain unchanged.

## v1.52: Departure-news directions

Five fresh PASS results: exact two-message-only scope and native font width (two), native guide arrival and dispatcher-before-notice gate followed by actual notice/two new instruction pages/saved notes/repeat reading (one), actual dispatcher confirmation/three reminder pages/repeats/cold Continue and return-guide No/B (one), native guide return and keeper report/repeats/cold Continue (one). Source is the genuine v1.51 refuge-reminder-complete battery. No memory writes, inventory edits, party substitutions or progress injections. Departure stages 1, 2, 3 and 4 are earned by guide travel, reading, verification and delivery. Historical refuge help remains completed. Walking comparisons permit native friendship changes while money, inventory, badges and present report state remain exact; saved and stationary state checks remain exact. All five new instruction pages visually inspected. This suite does not board the Beauvais train or rerun the full ending; full-story evidence remains v1.15 and music/splash evidence remains v1.25. All four user saves and archived v1.51 ROM remain unchanged.

## v1.51: Refuge task reminders

Five fresh PASS results: exact three-reminder-only text additions and native font width (two), three welcome pages and keeper repeats/cold Continue without skipping child request (one), actual Elise/Eevee request with two keeper-direction pages/repeats/cold Continue (one), actual keeper blanket with two delivery-direction pages/saved carrying state, native Elise delivery, repeats/completion cold Continue and Celebi return (one). Uses genuine v1.50 celebi-refuge-arrived battery. No memory writes, inventory edits, party substitutions or progress injections. Past-stage assertions verify 1 before child request, 2 after request, 3 while carrying and 4 after delivery. Money, inventory, badges and report state remain exact throughout. Walking repeat comparisons permit native party friendship changes; stationary dialogue, cold Continue and portal comparisons remain exact. An initial strict walking comparison observed that native change; a separate read-only audit confirmed friendship increased while other growth fields stayed unchanged, and the final suite reran from the genuine source. The blanket is handled by the existing quest stage rather than added to Bag. All seven reminder pages visually inspected. This suite covers first refuge help, not departure news or full ending; full-story evidence remains v1.15 and music/splash evidence remains v1.25. All four user saves and archived v1.50 ROM remain unchanged.

## v1.50: Ada onward-refuge directions

Six fresh PASS results: exact Ada completed-report-only text addition and native font width (two), six-page onward message/repeats/cold Continue (one), normal forest route with No/B departure and cold Continue (one), actual Yes refuge arrival with optional return No/B/cold Continue and keeper-before-child gate (one), normal child/keeper/child completion, saved help, native Celebi return to present and normal return to Ada/repeats/cold Continue (one). Uses the genuine v1.48 celebi-return-claimed battery. No memory writes, inventory edits, party substitutions or progress injections. First native arrival sets past stage 1; child request, keeper blanket and child delivery advance it to 2, 3 and 4. Present-day party, money, inventory, badges and report state remain preserved across portal travel. Ada does not duplicate the vision reward. Six instruction pages visually inspected. This suite covers the first refuge help, not the whole historical ending; full-story evidence remains v1.15 and music/splash evidence remains v1.25. All four user saves and archived v1.49 ROM remain unchanged.

## v1.49: Ada pending report reward guidance

Eight fresh PASS results: exact Ada pending-message-only scope and native font width (two), pending four-page messages/repeats/cold Continue (two), native Bag Toss cancellation/confirmation and saved room (two), actual one-time Candy claims/completion/repeats/cold Continue (two). Separate fixture generation loads the genuine v1.48 celebi-return-ready battery and walks/travels normally to Ada. It then explicitly changes only the 42 Items slots: either 42 distinct valid items excluding Candy, or a 999-Candy stack with other Items slots empty. These are isolated inventory capacity fixtures, not naturally collected inventories; earned vision, party, money and badges are unchanged. Runtime recovery performs no memory writes. Cancelling Toss keeps state intact; confirming removes one Potion from the full pocket or one Candy from the capped stack. Pending stage 2 and room survive native Save/cold Continue. Normal Ada talk adds exactly one Candy and advances to stage 3; repeats/reloads duplicate nothing. Text mentions Use/Give, but this fresh suite exercises Toss. All pending instruction pages visually inspected. All four user saves and archived v1.48 ROM remain unchanged. Full-story evidence remains v1.15 and music/splash evidence remains v1.25.

## v1.48: Celebi report-return directions

Five fresh PASS results: exact first/repeated forest return text additions and native font width (two), genuine vision with three first-return pages and four repeated reminder pages/repeats/cold Continue (one), normal northward forest walk/train route to Ada with one-time Candy/repeats/cold Continue (one), normal completed-story forest revisit and optional time-travel No/B plus cold Continue (one). Uses the genuine gym-ada-forest battery from v1.47. No memory writes, inventory edits, party substitutions or progress injections. Native sighting sets report-ready stage 2 without a battle or early reward; actual Ada hand-in sets stage 3 and adds exactly one Candy. Post-report forest interaction offers optional departure; declines remain in the present and preserve the earned reward. All seven instruction pages visually inspected. This suite does not rerun the historical journey or full ending; full-story evidence remains v1.15 and music/splash evidence remains v1.25. All four user saves and archived v1.47 ROM remain unchanged.

## v1.47: Third-Gym lead to Ada

Six fresh PASS results: exact completed-third-Gym-only text scope and native font width (two), seven-page leader reminder/repeats/cold Continue (one), normal station/train route to Ada east of Oxford guide and No/B offer declines/cold Continue (one), genuine acceptance and normal Chantilly train/forest route with sighting No/B and saved active state (one), actual Celebi vision and saved sighting followed by normal return to Ada and exactly one report Candy with repeats/cold Continue (one). Source is the genuine gym-defeat-Oranienburg-retry-won battery, refreshed by the v1.46 native Gym defeat/retry suite. No memory writes, item edits, party substitutions or progress injections. Both the researcher task and forest sighting remain optional; early declines grant no progress or reward. Seven leader pages visually inspected. Full historical story ending is not rerun by this suite; full-story evidence remains v1.15 and music/splash evidence remains v1.25. All four user saves and archived v1.46 ROM remain unchanged.

## v1.46: all three Gym defeat and retry verification

Nine fresh runtime PASS results rerun test_gym_defeat_recovery.py on v1.46. Genuine story-complete, water-gym-entrance and electric-gym-entrance batteries provide normally earned chapter readiness. Normal clinic visits prepare the team, and native non-damaging move choices cause actual losses against Ellis, Marine and Conrad. Each loss applies the expected badge/level-based fee, restores party HP/status and first-mon move PP in the local clinic, preserves quest/inventory state, and grants no badge, TM or trainer victory. Normal Save/cold Continue and walking back retain the optional B-declined retry. Actual accepted retry battles earn each badge and one TM; repeat leader dialogue and cold Continue duplicate neither reward. No memory writes, inventory edits, party substitutions or progress injections occur. These are fresh current-ROM repetitions of the established genuine defeat suite, not a new full-story run. Existing Chantilly preparation, clinic, shop and Paris report directions were reviewed and need no text change. Recovery screenshots visually inspected. Current and archived v1.46 ROM, matching symbols and all four user saves remain unchanged.

## v1.46: genuine rival defeat and retry verification

Four fresh runtime PASS results on v1.46 use the genuine rival-prep-returned battery. Normal non-damaging battle commands cause a real defeat without changing stats, party or progress artificially. Native blackout returns to Oxford clinic, restores HP/status and first party member moves/PP, applies a loss fee and grants no rival win, report or Bell. Both earlier trail victories remain earned. Cold Continue, normal return, No/B and journal preserve readiness. Actual retry victory uses earned Potions through the native Bag, pays prize money once, and unlocks report journal lead 4. Repeats/cold Continue preserve completion. Normal train return to London and Oak aide grants one Soothe Bell, stage 2 and Gym journal lead 5; repeats/cold Continue duplicate nothing. No memory writes, inventory edits or progress injections occur. An initial strict slot comparison caught normal Bag compaction after the final Potion was consumed; the victory comparison now checks identical item/quantity multisets and all other state exactly. The final suite reran from the genuine source. No new ROM build or full-story run is claimed. Current and archived v1.46 ROM, symbols and all four user saves remain unchanged.

## v1.46: Oxford rival preparation

Five fresh PASS results: exact offer/decline text scope and native font width (two), genuinely earned two-trail-win readiness plus No/B/read-only repeats/cold Continue/journal (one), normal clinic walk/free healing/cold Continue/return (one), actual accepted rival battle against Pidgey and Eevee (one). Uses the genuine regional-guide-Oxford-claimed battery and accepts Oak's study normally if not already active, preserving earlier victories. No memory writes, inventory edits, trainer-win or progress injections. Clinic verifies all party members have full HP and no status, and retains money, items and progress. Battle-start check verifies trainer 749 and species 16/133 without granting a premature victory or Bell. This suite does not claim a fresh completed rival victory or full-story run. Offer/decline pages visually inspected. All preserved user saves and archived v1.45 ROM remain unchanged. Full-story evidence remains v1.15; music/splash evidence remains v1.25.

## v1.45: England active-study reminders

Eight fresh PASS results: exact three-message-only scope and native font width (two), aide/missing-Oliver/missing-Alice full-page reminders with repeats/journals/cold Continue (three), actual walking directions to the corresponding required trainer with B declines/cold Continue (three). Uses genuine v1.44 active-study and rival batteries and v1.26 training-intro-London-won; the last contains a real Oliver victory, and the test accepts the study normally if needed before travelling to Oxford. No memory writes, item edits or trainer-win/progress injections. No fresh accepted trainer battle or report hand-in is claimed. A static check initially caught exclamation-ending message terminators before the new rival pages; these were corrected before the final scope check and runtime verification. All reminder pages visually inspected. All four user saves and archived v1.44 ROM remain unchanged. Full-story evidence remains v1.15; music/splash evidence remains v1.25.

## v1.44: England accepted-study directions

Six fresh PASS results: exact accepted-text-only scope and native font width (two), native unstarted-study B/No declines and real Yes acceptance with six message pages plus active-study repeat/journal/cold Continue (one), actual northward walking route to Oliver and native B decline/reload (one), onward walking route to Alice and native B decline/reload (one), onward walk to Oxford rival with missing-Oliver gate/repeat/journal/cold Continue (one). Uses the genuine start-england battery. No memory writes, inventory changes, trainer-win or progress injections. No fresh accepted trainer battles or report hand-ins are claimed by this suite. Accepted instructions are visually inspected. Four user saves and archived v1.43 ROM remain unchanged. Full-story evidence remains v1.15; music/splash evidence remains v1.25.

## v1.43: England report-return directions

Six fresh PASS results: exact text-only scope and font width (two), four-page earned-report reminder/repeat/cold Continue and journal (one), locked Gym plus actual train hand-in/repeat/cold Continue (one), completed rival and unlocked Gym B/No declines across cold Continue (one), actual walking return through Oxford Trail and English Meadow with one-time hand-in/repeat/cold Continue (one). Uses the genuine story-report-ready battery, originally in London; the test travels normally to Oxford before reading the rival. An initial driver assumed the source was already Oxford and was corrected; final runtime reran all cases. No memory writes, inventory edits, progress injections or fresh accepted Gym battle. Four new message pages visually checked. Full-story evidence remains v1.15; music/splash evidence remains v1.25. Three user saves and archived v1.42 ROM remain unchanged.

## v1.42 country reward Bag recovery (2026-10-08)

Twenty fresh PASS results: exact pending-text-only scope/font (two), pending
message/repeat/cold Continue (six), native Toss cancellation/confirmation
and room-state cold Continue (six), one-time claims/repeats/claimed-state
cold Continue (six). England's Soothe Bell, France's Miracle Seed and
Germany's Magnet each use two explicit inventory fixtures: 42 distinct
valid Items excluding the reward, or one reward stack of 999 with other
Items slots empty. The separate fixture generator edits only those 42
Items slots, based on genuinely earned report-ready batteries. Reports,
wins, party, money and badges are never injected. These are capacity
fixtures, not claims of naturally collecting all those items. The runtime
recovery test performs no memory writes. Native Toss B cancellation keeps
tested state intact; confirming removes one Potion from a full pocket or
one reward item from a capped stack. The saved room and pending report
survive normal Save/cold Continue. Normal contact talk then adds one earned
reward and completes the report, with repeats/cold Continue unable to
duplicate it. Party, money and badges remain unchanged during room-making.
Use/Give are mentioned by the text, but this new capacity suite exercises
Toss specifically. Four instruction pages per country are visually inspected.
An initial runtime check caught the old French message terminator before
the added pages; it was corrected and the final build reran all cases.
Removing the additions restores previous scripts byte-for-byte. All three
user saves and archived v1.41 ROM remain unchanged. Full-story evidence
remains v1.15; music/splash evidence remains v1.25.

## v1.41 completed country quest-to-Gym routes (2026-10-08)

Eight fresh runtime PASS results use genuinely earned v1.41 French/German
report-claimed and returned-contact batteries. No memory writes, item edits,
party substitutions or progress injections occur. Celine and Remy completed
reminders identify Marine at Chantilly Gym; Lena and Karl identify Conrad
at Oranienburg Gym. Each reminder repeats and cold Continues without
changing tested state; the read-only journal names the correct Gym (13/18).
Normal town paths and, where needed, station trains/interchanges reach the
north-square Gym and its leader. The earned report reward has unlocked
the optional battle offer. Native B cancellation retains exact arrival
state. After normal Save/cold Continue, native No selection likewise keeps
all tested state and does not begin battle, grant the next badge or record
its TM reward. Travel comparisons permit native party friendship changes.
Screenshots are inspected. Fresh accepted Gym victories and pre-hand-in
gates are separate earlier evidence, not new claims in this suite. No ROM
fix was needed. Current and archived v1.41 ROMs, matching symbols and all
three user saves remain unchanged.

## v1.41 reviewed-report return routes (2026-10-08)

Eight fresh PASS results: exact report-return text-only scope/font (two),
earned report reminder/repeat/cold Continue and journal (two), normal train
return to capital with actual one-time hand-in/repeat/cold Continue (two),
and return to original report contact/repeat/cold Continue (two). France
starts from a genuinely played v1.40 Gardens-first battery, visits the
forest normally and obtains Remy's actual review before checking the new
reminder. Germany starts from the genuine v1.40 Karl delivery battery.
No memory writes, item edits, party substitutions or progress injections
occur. Three report pages are visually inspected in each country. New
directions reach Celine in Paris and Lena in Berlin; actual hand-ins award
one Miracle Seed/Magnet and advance the corresponding journal to the Gym.
Repeat hand-ins, cold Continue and normal train returns to Remy/Karl grant
no duplicate rewards. Stationary reminders and journals retain exact tested
state; travel comparisons permit native party friendship changes. Removing
the additions restores previous scripts byte-for-byte. No fresh accepted
Gym battles or full-story run are claimed; full-story evidence remains
v1.15 and music/splash evidence remains v1.25. All three user saves and
archived v1.40 ROM remain unchanged.

## v1.40 saved partial-quest reminders (2026-10-08)

Six fresh runtime PASS results use genuinely played v1.40 partial survey
and courier batteries. No memory writes, inventory edits, party substitutions
or progress injections occur. Both Celine and Remy are visited normally after
the Gardens-first and Forest-first observations. Each three-page reminder
names the missing site; repeat talk and normal Save/cold Continue preserve
exact tested state and do not skip the second observation or grant review
or Miracle Seed. The regional journal selects the corresponding missing
observation (9 or 10), and topic/checklist switching remains read-only.
Lena's three-page packed-parcel reminder names Karl and northward walking/
train options. Karl's two-page delivered-report reminder names Lena and
the southward Havel Trail/German Woodland route. Repeats and normal Save/
cold Continue preserve stages 1/2 and grant no premature Magnet. Journals
retain delivery/return leads 16/17. Screenshots are visually inspected.
Actual remaining-route completion has separate v1.40 release evidence;
this suite verifies recovery reminders and state preservation. No ROM
change was needed. Current and archived v1.40 ROMs, matching symbols and
all three user saves are verified unchanged.

## v1.40 accepted survey/courier routes (2026-10-08)

Ten fresh PASS results: exact accepted-text-only scope/native font (two),
French acceptance/repeat/cold Continue and journal (one), first observation
and withheld review/reward for both orders (two), second observation with
actual Remy review/Celine hand-in and saved completion for both orders
(two), German acceptance/repeat/cold Continue/journal (one), actual Karl
delivery by train with saved report (one), and walking return through
Havel Trail/German Woodland with one Magnet and saved completion (one).
Sources are genuine earned-Gym contact batteries from v1.39. No memory
writes, inventory edits, party substitutions or progress injections occur.
French marker paths are walked normally, with no encounter manipulation.
Repeating first markers and visiting both contacts cannot skip the second
observation or award a reward. Both observations still require Remy's review
before Celine grants exactly one Miracle Seed. German cargo remains outside
the Bag; the train reaches Karl west of the Oranienburg guide, and clear
southward paths return his report to Lena for one Magnet. Repeat contacts
and normal Save/cold Continue preserve one-time rewards. Read-only journal
checks follow each milestone and name the proper next objective or Gym.
Instruction pages are visually inspected. Removing additions restores the
previous scripts byte-for-byte. No fresh accepted Gym battles or full-story
run are claimed; full-story evidence remains v1.15 and music/splash remains
v1.25. All three user saves and archived v1.39 ROM remain unchanged.

## v1.39 post-Gym journal compatibility (2026-10-08)

Fifteen fresh runtime PASS results: claimed/pending regional journal lead,
earned checklist and read-only topic switching (six), normal Save/cold
Continue of each state (six), and actual next-step journal transitions with
another cold Continue (three). Claimed sources are genuinely earned v1.27
retry victories revisited in v1.39. Pending sources are explicit v1.27
999-TM capacity fixtures revisited in v1.38; their victories are genuine,
but their inventories are synthetic. No memory writes or inventory, party,
wins or progress injections occur in this new suite. Oxford's claimed TM
points to Celine (lead 7), while the pending TM takes priority (lead 6).
Chantilly selects Lena (15) or Water Pulse collection (14). Oranienburg
selects optional London stamp collection (20) or Shock Wave collection (19).
Saved badges/stamps are checked independently of the menu's checklist.
Normal train routes reach Celine and Lena; accepting their tasks through
native Yes advances the journal to both survey habitats (8) or Karl's
delivery (16). Each acceptance, correct journal and tested saved state
survive cold Continue. After Oranienburg, native London guide talk records
its optional stamp once; the journal then names the missing Paris stamp
(21). Repeating guide talk and cold Continue grant no duplicate reward.
Map/lead/records and Celebi-topic switching retain tested state, allowing
native Bag compaction/sorting without item loss. Screenshots are inspected.
No new Gym battles, full-story run, or completion of newly accepted tasks
is claimed. No ROM fix was needed. Current and archived v1.39 ROMs, symbols
and all three user saves remain unchanged.

## v1.39 completed Gym onward travel (2026-10-08)

Eleven fresh PASS results: exact completed-text-only scope/font (two),
claimed leader message/repeat/cold Continue (three), normal onward travel
and destination cold Continue (three), then return journeys and claimed
leader cold Continue (three). Genuine v1.27 recovered/retry-victory batteries
contain normally earned badges, TMs and prizes; no party, inventory, wins
or progress are injected. Oxford directions reach Celine in Paris; Chantilly
directions reach Lena in Berlin. B-declining each next task, repeating and
cold Continuing grant no unearned story progress. Oranienburg directions
reach Oxford's river landing by normal trains/interchanges. Captain B
cancellation, free Oxford-London-Oxford sailing and a cold Continue at each
landing retain exact tested state. Returning by normal trains and revisiting
all three leaders duplicates no badge, TM or prize. Stationary dialogue and
boat comparisons are exact; walking comparisons permit native friendship
changes. Instruction pages are visually inspected. Removing the additions
restores previous scripts byte-for-byte. No fresh accepted Gym battles or
full new-game runs are claimed; full-story evidence remains v1.15 and
music/splash evidence remains v1.25. Three user saves and archived v1.38
ROM remain unchanged.

## v1.38 pending Gym TM instructions (2026-10-08)

Fourteen fresh PASS results: exact text-only scope/font (two), four-page
pending message/repeat/cold Continue at all Gyms in TM-stack and Key Items
capacity modes (six), native Give cancellation/confirmation and room-state
cold Continue (three), then exactly one reward claim/repeat/claimed-state
cold Continue (three). Source batteries are explicit v1.27 inventory
capacity fixtures: 999 copies of the target TM, or thirty distinct Key Items
without a TM Case. Their Gym wins were earned in real battles. This suite
performs no memory writes or inventory, party or progress injections.
The Key Items fixtures verify pending text and preservation only; they do
not claim native Key Items room-making. In capped-stack cases native TM
Case Give transfers exactly one existing copy to an empty-handed Bulbasaur,
leaving 998 bag copies; cancellation leaves exact tested state unchanged.
After normal Save/cold Continue, leader talk grants exactly one waiting
copy, records collection, retains the held copy and starts no rematch.
Repeats/cold Continue grant nothing further. Money, story and badges stay
unchanged during room-making. The text mentions Use as well as Give; normal
Use teaching has separate v1.37 compatibility evidence, not a new capped-
stack Use case here. All four message pages are visually inspected. Removing
the additions restores the previous scripts byte-for-byte. All three user
saves and archived v1.37 ROM remain unchanged. Full-story evidence remains
v1.15; music/splash evidence remains v1.25. No fresh Gym victories are
claimed by this text/recovery suite.

## v1.37 taught Rock Tomb/Water Pulse battle compatibility (2026-10-08)

Six fresh runtime PASS results load the genuine Marshtomp teaching batteries
from the previous v1.37 TM suite. Those batteries inherit a normally played
Germany/Mudkip full story and normally consumed earned Gym rewards. No
memory writes, item edits, party substitutions or progress injections occur.
Normal train/walking routes reach London countryside grass. Each taught move
executes against a real wild Rattata and reduces its HP. Rock Tomb spends
two PP before first observed damage; Water Pulse spends one. Other move
slots and their PP remain unchanged. This is not a claim that Rock Tomb
always hits, nor a measurement of its secondary effect. Natural battle HP
and experience changes are allowed. Money, inventory, story and badges
remain unchanged, and the consumed TM remains absent. Normal Save/cold
Continue retains learned moves and spent PP. Clear paths lead back to the
London clinic; native free care restores full HP and all move PP without
charging money or returning either TM. A further normal Save/cold Continue
retains healed PP and consumed rewards. Screenshots are inspected. This
suite does not isolate Water Pulse confusion, Rock Tomb speed reduction,
type-matchup balance, or accuracy probabilities. No ROM change was needed.
Current and archived v1.37 ROMs, matching symbols and three user saves are
verified unchanged.

## v1.37 Shock Wave compatible teaching and battle (2026-10-08)

Four fresh runtime PASS results start from the genuine v1.15 Germany/Mudkip
full-story battery with its earned TM34 and existing ball supplies. Normal
train travel reaches London, then normal walking through countryside grass
finds Mareep on the third wild encounter. The first two encounters are
escaped normally. Four normal ball throws catch a level-three Mareep and
add it to the party; no catch rates, RNG, items, party or progress are edited.
Money and saved journey variables remain unchanged through the capture.
The native Save/cold Continue retains the captured partner. Canceling the
compatible partner selection retains exact tested state, including TM34.
Accepting teaching fills Mareep's first empty move slot with Shock Wave
and 20 PP; other moves and their PP stay unchanged. Exactly one earned
TM34 is consumed, while money, journey variables and badges stay unchanged.
Normal teaching friendship changes are allowed. A normal Save/cold Continue
retains the learned move, PP and consumption. Native party switching puts
Mareep in the lead; a real wild Oddish battle executes move 351, decreases
the target's HP and spends exactly one PP. The battle is escaped normally;
a further Save/cold Continue retains 19 PP and the consumed TM. Screenshots
are inspected. This does not cover Shock Wave accuracy under evasion boosts,
Ground immunity, or competitive balance. Rock Tomb and Water Pulse battle
use remain separate follow-up coverage. No ROM fix was needed; current and
archived v1.37 ROMs, symbols and all three user saves remain unchanged.

## v1.37 Gym TM teaching compatibility (2026-10-08)

Nine fresh runtime PASS results use genuinely earned v1.27 Gym-retry
victory batteries and the v1.15 Germany/Mudkip full-walkthrough battery.
No memory writes, party substitutions, inventory edits or progress
injections occur. Bulbasaur rejects Rock Tomb, Water Pulse and Shock Wave
without consuming the TM or changing tested party, money, story, badges
or inventory; each rejected attempt survives a normal Save/cold Continue.
Native TM Case sorting is allowed while item quantities remain identical.
Marshtomp party-selection cancellation and declining four-move replacement
both preserve exact tested state for Rock Tomb and Water Pulse. Accepted
teaching replaces only slot zero, preserves the other three moves and PP,
assigns the new move's native full PP and consumes exactly one earned TM.
Money, story and badges stay unchanged; native teaching friendship changes
are allowed. Learned moves, PP and consumption persist through normal
Save/cold Continue. This suite does not yet cover teaching Shock Wave to
a compatible partner, teaching into an empty move slot, or battle use of
these newly taught moves. Diagnostic failures were test-driver assumptions
about a freed menu pointer and advancing multi-page native prompts; final
coverage uses active tasks and normal A presses. Screenshots are inspected.
No ROM change was needed. The current and archived v1.37 ROMs, matching
symbols and all three user saves are verified unchanged.

## v1.37 completed regional challenge travel (2026-10-07)

Eleven fresh PASS results: exact shared-text addition/font fit (two), claimed
guide repeats and cold Continue (three), normal trains/interchanges visiting
both other guide towns with cold Continue (three), and return journeys with
claimed-guide repeat/Continue (three). Starting batteries contain genuinely
earned v1.35 trainer victories and a single claimed regional reward. No party,
inventory, wins or progress are injected. Other guides grant no unearned
Candy or completion; revisiting the original guide duplicates no reward.
Stationary conversations preserve exact state; travel comparisons permit
normal party friendship changes from walking. Instruction pages are visually
inspected. Removing the added text restores the previous shared script exactly.
All three user saves and archived v1.36 ROM remain unchanged. Fresh battles
and a full new-game story run are not part of this text/navigation suite;
full-story evidence remains v1.15 and music/splash evidence remains v1.25.

## v1.36 pending regional reward Bag instructions (2026-10-07)

Twenty fresh PASS results: exact shared-text addition and font fit (two),
pending message/repeat/cold Continue (six), native Bag Toss cancellation,
confirmation and room-state cold Continue (six), one-time claims/repeats
and claimed-state cold Continue (six). All three branch guides are tested
with a full 42-slot Items pocket lacking Candy and a capped 999-Candy stack.
Existing v1.27 reward-capacity pending batteries are explicit synthetic
inventory fixtures built on genuinely earned trainer victories. These are
not claims of naturally obtaining all items. This new test performs no
memory writes: all room-making uses actual Bag controls, and wins, money,
party and progress are never injected. Canceling Toss retains exact tested
state; confirming discards exactly one Potion or Candy. Party, money, story
and badges remain unchanged, and the pending reward stays unclaimed until
normal guide talk can grant it. The claim adds exactly one Candy, records
completion and cannot repeat through the tested visits/Continues. The text
also mentions Use/Give, but those actions are not new runtime coverage in
this suite. Native instruction pages are visually inspected. All previous
shared commands and text restore byte-for-byte after removing the additions.
All three user saves and archived v1.35 ROM remain unchanged. Full-story
runtime evidence remains v1.15; music/splash remains v1.25.

## v1.35 remaining regional trainer guidance (2026-10-07)

Seventeen fresh PASS results: source-scope/reward-gate preservation and
native font fit (two), zero-win guides with repeat/cold Continue (three),
normal extended-first wins and missing-local messages (three), genuine
local-first states and missing-extended messages (three), normal reverse-
order second victories and one Candy (three), claimed repeats/cold Continue
(three). Genuine country-specific training-intro ready and training-recovery
healed batteries are loaded through Continue. Extended-first victories and
subsequent local wins use normal battle controls and existing Potions if
needed. No trainer flags, items, party stats, money or progress are injected;
no savestates are used. Normal walking follows the guide's southward path
through the extended trail into the local countryside. One-win messages
are visually checked for the correct missing opponent and count, repeat
without grants and survive cold Continue. Both earned wins still trigger
the original reward branch first, and already-claimed rewards still skip
all progress branches. Full-bag handling is preserved by source restoration;
its earlier v1.27 capacity suite is not a fresh runtime check here. All
original script bytes restore exactly after removing only the two new
read-only branch instructions and dialogue blocks. Native lines fit the
message window. All three user saves and archived v1.34 ROM remain unchanged.
Full-story evidence remains v1.15; music/splash remains v1.25.

## v1.34 extended-victory reward return (2026-10-07)

Eleven fresh PASS results: exact additions and native font fit (two),
earned-victory text/repeat/cold Continue without prizes or changes (three),
clear north walks to free clinic care and square guides with one Candy,
repeat and cold Continue protection (three), defeated-trainer revisits,
revisit cold Continue and another guide return without duplicated rewards
(three). Genuine long-trail won batteries from the v1.27 normal-battle
suite contain both earned wins and an unclaimed regional reward. They are
loaded through Continue, with no party, inventory, money or progress
injections and no savestates. These runs test the already-won trainer's
native after-battle dialogue; accepted extended battles were last rerun
on v1.33 and are not counted as fresh battle checks here. Clinic care
restores full HP and clear status while money/items/story remain unchanged.
Normal guide talk grants exactly one Candy, records completion, and never
duplicates it through the tested visits/Continues. Source restoration
proves original text, opponents, battle commands and reward eligibility
are unchanged. Native new pages are visually inspected. All three user
saves and archived v1.33 ROM remain unchanged. Full-story evidence remains
v1.15; music/splash remains v1.25.

## v1.33 local-victory onward directions (2026-10-07)

Eleven fresh PASS results: exact text additions and font fit (two),
post-victory advice/repeat/cold Continue (three), walking north to named
extended opponents, B-declined matches, branch guide withholding rewards
before the second win, free clinic preparation and cold Continue (three),
correct extended teams with normal victory, prize-once repeat and one
regional Rare Candy through guide repeats/cold Continue (three). Genuine
country-specific training-intro won batteries are loaded through Continue.
No party, item, money or progress injection and no savestates are used.
The real post-local-battle team receives native clinic care before the
extended match; existing Potions are used through the Bag if needed.
New advice never repeats trainer prize money. Named paths reach the stated
trainer and branch town through normal walking. Native messages are
visually inspected. Source restoration proves previous text, teams,
battle commands, reports, gates and rewards are unchanged. All three user
saves and archived v1.32 ROM remain unchanged. Full-story runtime evidence
remains v1.15; music/splash remains v1.25.

## v1.32 route entrance training and services (2026-10-07)

Eleven fresh PASS results: exact source additions and font fit (two),
six-page entrance signs/repeats/cold Continue (three), reaching the named
local trainer via the clear north route, B decline and safe southward
return (three), free clinic care and station Potion purchases with indoor
Continue and return to the sign (three). Genuine country-specific
training-intro ready batteries are loaded through Continue; the player
walks south from the undecided trainer to read its city's sign. No party,
item, money or progress injection and no savestates are used. The trainer
stays unbeaten, and declining grants no battle, victory or prize. Walking
may change friendship. Free nurse care preserves already prepared teams;
naturally damaged healing is prior separate evidence. Normal shop inputs
add one Potion and deduct exactly 300; indoor cold Continue retains it.
All new sign pages are visually inspected. Exact source restoration proves
prior destinations, visitor-room advice, gates, battles and rewards are
unchanged. All three user saves and archived v1.31 ROM remain unchanged.
Full-story evidence remains v1.15; music/splash remains v1.25.

## v1.31 trail signs and service routes (2026-10-07)

Eleven fresh PASS results: exact additions and font fit (two), both ends'
four-page signs with repeats and cold Continue (three), normal north-town
walks to free clinic care and station-shop Potion purchases with indoor
Continue (three), southward trail/countryside crossings to each capital's
free clinic and cold Continue (three). Genuine v1.26 country-specific
post-local-trainer healed batteries are loaded through Continue. No party,
item, money or progress injection and no savestates are used. Central clear
paths and adjacent sign approaches avoid random battles in these runs.
Already healed teams remain prepared through free nurse care; naturally
damaged healing is earlier evidence, not claimed anew. Normal shop input
buys one Potion for exactly 300 and saves it through indoor Continue.
Southward travel retains supplies, money, badges and story progress;
walking may legitimately change friendship. Source restoration proves all
prior messages, trainers, battles and rewards are unchanged. Native signs
are visually inspected. All three user saves and archived v1.30 ROM remain
unchanged. Full-story evidence remains v1.15; music/splash remains v1.25.

## v1.30 Gym guide preparation routes (2026-10-07)

Eleven fresh PASS results: exact text additions and native font fit (two),
complete advice/repeat/indoor cold Continue (three), west-square free clinic
care with indoor cold Continue (three), east-side station-shop cancellation,
one-Potion purchase for exactly 300, indoor cold Continue and return to the
guide (three). The genuine v1.26 healed London local-trainer battery is
loaded through Continue for each branch visit; trains, walks, conversations,
shop inputs and saves use normal controls. No inventory, party, money or
story injection and no savestates are used. The already prepared team stays
at full HP/PP during nurse care and money is unchanged; healing naturally
damaged teams is earlier separate evidence, not claimed anew here. Canceling
a purchase leaves tested state unchanged, a confirmed purchase adds exactly
one Potion and deducts 300, while party, story variables and badges remain
unchanged. Native advice pages and purchase screens are visually inspected.
Exact source restoration proves type/story advice, gates, battles and
rewards are unchanged. All three user saves and archived v1.29 ROM remain
unchanged. Full-story evidence remains v1.15, music/splash v1.25, accepted
Gym battles v1.28 and readiness hand-ins v1.29.

## v1.29 locked-Gym story directions (2026-10-07)

Eleven fresh PASS results: exact additions and native font fit (two),
unstarted locked Gyms/cold Continue plus named capital/contact approaches
(three), report-ready locks/repeated dialogue/cold Continue (three), and
normal earned report hand-ins, one-time rewards and unlocked optional
leader offers after return/cold Continue (three). Genuine v1.26 healed
local-trainer batteries and existing story-report-ready, france-report and
germany-report batteries are loaded through Continue. No inventory, party,
stat, money or story fixtures and no savestates are used. Early visits grant
no battle, badge or TM; walking out and taking normal trains reaches each
named contact west of its capital's guide. The unstarted England offer is
declined, while France/Germany retain their prior-badge gates. Report-ready
states still require actual hand-in; each normal hand-in awards its story
item once and permits the leader's optional offer. Declining that offer
and cold Continue grant no unearned badge. Chantilly's added REMY location
is text/scope/font checked; this suite does not repeat the full survey route.
Native pages are visually inspected. Exact source restoration proves gates,
battles, rewards and prior text are unchanged. All three user saves and the
archived v1.28 ROM remain unchanged. Full-story runtime evidence remains
v1.15, music/splash v1.25, and accepted-Gym-battle evidence v1.28.

## v1.28 Gym preparation and clinic help (2026-10-07)

Eleven fresh PASS results: exact text-only scope and font fit (two), three
No/B and introduction checks, three clinic route/indoor Continue/return
checks, and three correct leader/team battles with normal victory, badge,
one TM, prize-once repeat and cold Continue. Genuine recovered batteries
from the v1.27 Gym defeat suite are loaded through Continue; no inventory,
party, money or progress injections and no savestates are used. Normal
walking follows each Gym's exit path, including Chantilly's winding route,
and reaches the free clinic west of the square. Existing Potions are used
through the Bag if needed during normal accepted battles. The source-scope
check reconstructs all three original v1.27 Gym scripts byte-for-byte after
removing only the new text. Native messages are visually inspected, and
matching ROM symbols are built explicitly. All three user saves and the
archived v1.27 ROM remain unchanged. Full-story walkthrough evidence remains
v1.15; music/splash evidence remains v1.25. Earlier v1.27 defeat and capacity
checks are separate evidence, not new checks on this release.

## v1.27 Gym reward capacity and UI (2026-10-07)

Twelve additional PASS results on the unchanged ROM: two inventory-boundary
wins and two corresponding UI checks per Gym. Genuine recovered batteries
from test_gym_defeat_recovery.py are loaded through Continue and the player
walks back to each leader. Only inventory capacity is arranged artificially:
a 999-stack of the target TM with a TM Case, or thirty distinct valid Key
Items excluding the TM Case. These are synthetic inventories, not claims
that every item was naturally acquired or that all related item side effects
are initialized. No story/trainer/badge flags, party stats or money are
injected. The existing party wins each battle through normal controls and
uses existing Potions if needed. Each victory awards its badge and money
but leaves the blocked TM unclaimed; repeat leader visits and pending-state
cold Continue retain exact progress and inventory. A separate inventory
fixture edit reduces the stack to 998 or frees a Key Item slot; native
room-making UI is not claimed. Normal leader talk awards the TM and supplies
the TM Case if missing, then records completion. Repeat talk and claimed-state
cold Continue cannot duplicate rewards. The Trainer Card displays exactly
the earned badges, and normal Bag controls open/close the TM Case with the
expected TM quantity. TM Case slot sorting is allowed while all item
quantities, party, money, badges and story progress must stay unchanged.
All three user saves and canonical/archived ROMs remain
unchanged. Full-story runtime evidence remains v1.15; music/splash v1.25.

## v1.27 natural Gym defeat and retry (2026-10-07)

Nine additional PASS results on the unchanged ROM: natural loss and clinic
recovery (three), recovered cold Continue and declined retry (three), normal
retry victory with one-time badge/TM and won-state cold Continue (three).
The existing story-complete, water-gym-entrance and electric-gym-entrance
batteries are loaded through Continue. Normal walking and clinic care
prepare each battle. The starter selects its existing Growl until the
opponent wins, without stat/HP/item injections or savestates. Zero, one and
two earned prior badges give native loss multipliers 2, 4 and 6; exact loss
is highest party level times four times that multiplier, capped by money.
The single-partner batteries recover full HP/PP and clear status at their
local branch clinic. Losing grants no target badge, TM, reward variable or
trainer victory; inventory, existing badges and story variables stay intact.
Fainting can change friendship. Recovered-state Save/Continue preserves the
exact tested state. Walking back allows B to decline a retry safely. Normal
retry battles use existing Potions through the Bag if needed and earn the
badge, one TM and prize money. Repeat leader talk and won-state cold
Continue cannot duplicate rewards. User saves and canonical/archived ROMs
remain unchanged. Scope is these three prepared single-partner batteries;
all possible party compositions or last-heal locations are not claimed.
Full-story evidence remains v1.15; music/splash remains v1.25.

## v1.27 regional reward capacity fixtures (2026-10-07)

Nine additional PASS results on the unchanged ROM, three per branch guide.
The base batteries contain genuinely earned local and extended trainer
victories from test_long_trail.py, with each regional reward still unclaimed.
Only the 42-slot items pocket is edited in isolated emulator instances to
arrange capacity boundaries. These are synthetic inventory fixtures, not
claims of naturally acquiring 42 items or using the Bag UI to make room.
No trainer/story flags, money or party stats are injected; user saves are
never loaded or modified. All pocket contents use native quantity encryption.
Full pockets without Candy and capped 999-Candy stacks retain their exact
inventory/progress on repeated guide visits and pending-state cold Continue.
A separate fixture edit frees one slot or reduces the stack to 998. The
normal guide interaction grants one Candy and records completion. Repeated
visits and claimed-state cold Continue cannot duplicate it. A full pocket
with a 998-Candy stack grants the reward directly, proving empty slots are
not required when the existing stack has room. Earned trainer wins remain
set throughout. Native pending dialogue is visually inspected. Six additional normal-control checks load the explicit capacity-fixture
batteries and perform no memory writes: canceling Toss leaves inventory
unchanged, confirming Toss removes exactly one item, and room-making
persists through Save/Continue. The guide then awards one Candy, with
repeat and claimed-state cold Continue protection. Party, money, story
variables and badges are preserved while tossing. All three
user saves and canonical/archived v1.27 ROMs remain unchanged. These nine
checks are separate from prior release and defeat suites. Full-story
runtime evidence remains v1.15; music/splash evidence remains v1.25.

## v1.27 natural longer-trail defeat and retry (2026-10-07)

Nine additional PASS results on the unchanged v1.27 ROM: natural loss and
branch-town clinic recovery (three), recovered cold Continue and B-declined
retry (three), normal retry victory/prize-once repeat and won-state cold
Continue (three). Genuine long-trail clinic batteries from the v1.27 route
suite are loaded through Continue. The player walks back to the trainer
and selects the starter's existing Growl or Leer until the opponent wins.
No HP/stat/item writes, artificial knockout fixtures or savestates are used.
The exact native zero-badge money loss is checked against starter level
(level times eight, capped by current money). Full HP and the original full
PP are restored, status is clear, and no victory, prize or items are granted
for losing. Story variables, inventory and badges are preserved; fainting
may change friendship. Cold Continue preserves the exact tested state.
Normal retry battles use existing Potions through the Bag if needed. A real
victory earns one prize; repeat talk and another cold Continue cannot grant
another. The clinic was deliberately visited before battle; recovery from
every possible last-heal location is not claimed. All three user saves and
both canonical/archived ROMs remain unchanged. These nine checks are
separate from the fourteen release checks. Full-story evidence remains
v1.15 and music/splash evidence remains v1.25.

## v1.27 longer trail help, clinics and rewards (2026-10-07)

Fourteen fresh PASS results: exact intended source scope and font fit
(two); optional help/No/B (three), northward clinic route/indoor Continue
and return (three), correct accepted battle/normal victory/prize-once
repeat/cold Continue (three), and one regional Rare Candy after both local
and extended wins with repeat/cold Continue protection (three). Genuine
v1.26 post-local-victory healed batteries are loaded through Continue.
Normal trains reach the branch towns, and normal walking follows their
clear paths. Supplied Potions are used through the real Bag if needed;
no memory or item edits, artificial damage or savestates are used. Guides
award nothing before the second victory. Battle teams, prizes and reward
commands remain unchanged. Native texts are visually checked and matching
ROM symbols are generated explicitly. All three user saves and archived
v1.26 ROM remain unchanged. Full story evidence remains v1.15; music/splash
evidence remains v1.25. Natural extended-trainer loss is a separate next
check, not a claim made by this suite.

## v1.26 natural trainer defeat and retry (2026-10-07)

Nine additional PASS results on the unchanged v1.26 ROM: each country's
natural loss and local clinic recovery (three), recovered cold Continue
and B-declined retry (three), normal retry victory/prize-once repeat plus
won-state cold Continue (three). Genuine ready-for-battle batteries from
test_training_intro.py are loaded with Continue. Normal Fight menu inputs
select the starter's existing Growl or Leer until the opponent wins; no
HP/stat/item writes, artificial knockout fixtures or savestates are used.
The trainer remains unbeaten and no prize/items are awarded for losing.
With level-eight starters and zero badges, the native loss formula charges
exactly 64 money; clinic recovery restores full HP, status clear and each
move's original full PP. Story variables, inventory and badges remain
unchanged. Fainting may legitimately change friendship. Cold Continue
itself retains exact tested party/state. A normal retry battle uses the
existing supplied Potions through the Bag if needed, earns a real victory
and one prize, and repeat talk cannot duplicate it. All three user saves,
canonical ROM and archived v1.26 ROM remain unchanged. These nine checks
are separate from the original 17 release checks and the nine post-battle
healing checks; full story walkthrough evidence remains v1.15.

## v1.26 natural post-battle recovery (2026-10-07)

Nine additional PASS results on the unchanged v1.26 ROM: genuine worn-down
victory teams and cold Continue (three), normal clinic recovery and repeat
care (three), healed-state cold Continue and clinic exit (three). Sources
are the normal battles saved by test_training_intro.py: Bulbasaur,
Chikorita and Treecko. Each begins this suite below maximum HP and with at
least one move below maximum PP. Only reads decrypt the Pokemon's ordered
substructures; no memory or item writes, stat fixtures or savestates are
used. Maximum PP comes from the actual move table and native PP-Up formula.
Nurse care restores full HP and every move's PP; status is clear afterward.
The test does not induce a status ailment or claim to verify curing one.
Species, personality, trainer ID, held item, experience, moves, PP bonuses,
EVs and other boxed data remain exact across healing. Earned defeat flags,
money, inventory and story state persist. Every cold Continue retains the
exact tested party/state. Repeating care changes none of that state.
All three user saves, canonical ROM and archived v1.26 ROM are unchanged.
The release's original 17 checks and v1.15 full-story evidence remain
separate; this suite verifies recovery after genuine normal battles.

## v1.26 optional training introduction (2026-10-07)

Seventeen fresh PASS results: exact one-page scope and native font fit
(two); each country's new introduction with No/B, cold Continue followed
by Yes/correct two-partner battle, and normal victory/prize-once repeat
plus won-state cold Continue (nine); existing No/B clinic-return and
indoor Continue suite on the new ROM (six). Genuine fresh-start batteries
are loaded through Continue. Battles use normal controls and, if needed,
the supplied Potions through the Bag; no memory/item edits are used. The
three first-choice starters are Bulbasaur, Chikorita and Treecko at level
eight before battle. All battle, decline, report and reward commands are
byte-identical; only the added help page changes. Matching ROM symbols
are explicitly built. All three user saves and the archived v1.25 ROM
remain unchanged. Full story runtime evidence remains v1.15; soundtrack
and splash evidence remains the separate v1.25 verification.

## v1.25 music transitions (2026-10-07)

Nineteen additional PASS results on the unchanged v1.25 ROM: station,
clinic and countryside round trips in each of six towns (eighteen), plus
final cold Continue (one). Every destination is saved through the normal
menu and cold-continued; actual M4A song headers, active tracks and clock
progress match each map. Station/clinic/route music restores the correct
custom town theme outdoors; nurse fanfares return to clinic music. Towns
and routes are reached by normal trains and walking on the clear paths.
Completed story variables, money, inventory and badges remain exact;
walking can legitimately change party friendship, and nurse care can
restore health/PP, so those are not compared as unchanged across visits.
Each Save/Continue itself retains exact party and state. No memory/item
edits or emulator-state fixtures are used. All three user saves, canonical
ROM and archived v1.25 ROM hashes remain unchanged. The original v1.25
release's 27 checks and the v1.15 full-story evidence remain separate.

## v1.25 original soundtrack and animated splash (2026-10-07)

Twenty-seven fresh PASS results on the final ROM with matching symbols:
three static checks, twelve presentation checks and twelve country checks.
Static checks preserve all 347 existing song IDs, change only music fields
on six town maps, verify exact score regeneration and 768-tick alignment
for all 28 tracks, and check native title text fit and entry points.
Presentation checks run one complete six-town 24-second animation cycle,
verify Celebi motion, record seven native stereo scores for roughly fifty
seconds each, check nonzero unclipped samples and active playback beyond
two loop boundaries, verify Start and three B/A menu return cycles, travel
by normal trains through all six themes, and cold Continue at Oranienburg.
The twelve country checks cover all nine starter choices and No/B retries
plus country-menu cancellation. Genuine completed-game batteries preserve
party, money, inventory, badges and story progress. No memory/item edits.
All three user saves and the archived v1.24 ROM remain unchanged. Full
story walkthrough runs remain the v1.15 evidence; no full story rerun is
claimed here. Audio signal checks do not substitute for listening review.
Save-clear and Berry Fix entry points remain in source but are not invoked
by these runtime checks. Matching symbols are explicitly generated with
make pokefirered.gba pokefirered.sym for this release.

## v1.24 trail-to-clinic directions (2026-10-07)

Eight fresh PASS results: exact text-only scope and native font fit (two),
No/B decline with the new page and exact saved state retained in all three
countries (three), and each clear southward route to the west-side clinic
with indoor cold Continue, nurse care and outdoor return (three). Genuine
v1.23 fresh-start batteries are loaded with Continue; no memory or item
edits. All three starter/country choices, inventory, money and progress
remain correct and no trainer defeat is awarded by declining. The teams
begin at full health; this verifies access and service results rather than
restoration of battle damage. No battle/reward commands change. All three
user saves and the archived v1.23 ROM remain unchanged. Full story runtime
evidence remains v1.15; this is focused route and dialogue verification.

## v1.23 clinic directions (2026-10-07)

Nine fresh PASS results: text-only scope and generator/font checks (two),
fresh country sign/repeat checks (three), following each sign to the nurse
with indoor cold Continue, free care and outdoor return (three), and an
older completed-game battery reading the new page with exact retained
state (one). Screenshots show the added page in each capital. All input
uses normal controls and genuine saves; no memory or item edits. Fresh
starters already have full health; these checks verify service access and
full-health/status results, not restoration of battle damage. All three
user saves and the archived v1.22 ROM remain unchanged. Full story runs
remain the v1.15 evidence, not a new full-story run for this release.

## v1.22 new-player Bicycle shortcut (2026-10-07)

Seventeen fresh PASS results: exact one-page change and native font fit
(two), full country-selection suite (twelve: all nine starters plus three
country-menu cancellation checks), and new shortcut instructions from
three fresh country starts (three). Screenshots show the added help page.
Normal Bag REGISTER and field SELECT work; riding cold Continue retains
registration, exact party/items, country and starter. Each fresh start
has exactly ten Poke Balls, five Potions, one Bicycle and one Town Map.
Starter level eight, preview/No/B retry, National Dex and capital arrival
remain correct. No memory/item edits are used. All user saves and archived
v1.21 ROM remain unchanged. Full story runs remain the v1.15 evidence;
this release reruns the new-game flow, not all historical chapters.

## v1.21 travel-board shortcut introduction (2026-10-07)

Eleven fresh PASS results: exact text-only scope and native font fit (two),
normal missing World Options item grant (one), all six town-board
dialogues/map returns (six), following normal REGISTER
and field/map SELECT instructions (one), and new v1.21 cold Continue (one).
Screenshots show both new pages at each board. Correct current-town maps,
field callbacks, existing registration, party, inventory and completed
story/case/stamp variables remain intact. The source checkpoint is the
completed map-select save; no memory edits are used. Board item-grant and
map-opening commands are byte-identical. The missing World Options item is granted normally once; repeat
boards grant no duplicate. Full-pocket grants are outside this run. All user saves and archived
v1.20 ROM remain unchanged; full walkthrough runtime evidence remains v1.15.

## v1.20 Town Map registration and SELECT (2026-10-07)

Six fresh checks register Town Map through normal Bag controls from
bicycle-select-complete.sav. Field SELECT opens the European map, including
Rooms and story controls, and exits directly to the field with exact state.
Riding map use and cold Continue retain Bicycle mode and map registration.
Indoor map use and Continue retain the correct London label, party and
progress. Registering Bicycle replaces the map shortcut; indoor cycling
refusal and outdoor SELECT work after Continue. Registering map again,
then DESELECTing, retains no registered item after cold Continue. No memory
or item edits are used. ROM and three user saves remain unchanged. Scope
is Oxford outdoors and London sitting room, not every map or registered item.

## v1.20 Bicycle registration and SELECT (2026-10-07)

Six fresh checks use normal Bag REGISTER/DESELECT actions and field SELECT
from the completed case-bike save. REGISTER assigns Bicycle without changing
party/items/quests; SELECT mounts and dismounts; riding cold Continue keeps
registration and functional dismount. Indoor SELECT cannot mount and leaves
registration intact; interior Continue retains exact state. Outdoor SELECT
works after exiting; normal Oxford return retains Ada's conclusion and all
completed activities. DESELECT sets the registered item to none, retained
by cold Continue. Registration is read at native SaveBlock1 offset 0x296;
no memory writes or item injection are used. No defect was found. ROM and
three user saves are unchanged. This run covers one indoor restriction,
not every no-cycling area or other registered Key Items.

## v1.20 Bicycle landmark-case compatibility (2026-10-07)

Seven fresh normal-control checks use visitor-bike-complete.sav and normal
trains to Westminster, Notre Dame and Reichstag. Each verifies mounted
No/B entrance declines, automatic dismount, completed curator and ledger
repeat safety, exact indoor cold Continue and the south exit. Rewards,
case synthesis variables, inventory and main-story progress remain intact.
Normal return to Oxford, final cold Continue and Ada's conclusion retain
the captured party and all completed activities. No memory edits are used.
No defect was found; ROM v1.20 and all three user saves remain unchanged.
This run does not test unfinished cases or pending rail bookings.

## v1.20 Bicycle visitor-room compatibility (2026-10-07)

Eleven fresh normal-control checks cover all ten capital visitor interiors:
London sitting/reading rooms and Eye gallery; Paris sketch/garden rooms
and Eiffel room; Berlin sitting/reading/garden rooms and Gate room. Each
checks mounted No/B declines, automatic indoor dismount, exact cold
Continue indoors, outdoor exit and continued controllable walking.
Money, items and all completed story/case/stamp variables remain intact.
Normal return to Oxford retains Ada's conclusion. Source checkpoints are
the genuine completed western-room saves; no memory or item edits are used.
No gameplay defect was found, so ROM v1.20 is unchanged. User saves are
unchanged. These checks do not cover optional case-room interiors or
pending rail bookings. The finished walkthrough remains unchanged.

## v1.20 landmark-guide city-service directions (2026-10-07)

Nine fresh PASS results: exact three-guide source/generator scope and
native font fit (two), old completed-save guide talks and service routes
with new cold Continue (seven). Original two-page dialogue is retained,
followed by exit/return and station/clinic pages. Screenshots verify both
new pages in each capital. Each actual south exit and northward walk
reaches the station, then free clinic. Healing restores party HP while
money, inventory and completed story/case/stamp variables remain intact.
Repeated guide talks preserve exact party/state; new v1.20 Continue
retains exact post-healing state. User saves and archived v1.19 ROM stay
unchanged. Full walkthrough evidence remains v1.15 with focused later checks.

## v1.19 neighborhood landmark-return signs (2026-10-07)

Nine fresh PASS results: exact sign/generator scope and native font fit
(two), old completed-save sign reading, repeat safety, actual landmark
visits and new cold Continue (seven). London and Berlin add a final page;
Paris's existing final line now names Eiffel and bridges. Earlier room
listings and native commands remain intact. Screenshots show each return
page; normal walking reaches Eye, Eiffel and Gate visitor rooms and their
exits. Party, inventory and completed case/story/stamp state remain intact.
All three user saves and the v1.18 archived ROM remain unchanged. The full
walkthrough is finished with its v1.15 full-run evidence retained.

## v1.18 eastern host landmark directions (2026-10-07)

Nine fresh PASS results: exact source/generator scope and native font fit
(two), old completed-save host conversations and actual landmark visits
(seven). The original two host pages remain intact before a new third page.
London reaches the Eye gallery, Paris the Eiffel visitor room, Berlin the
Gate visitor room. Repeat dialogue, reading and exits retain party, items
and all completed case/story/stamp variables. New v1.18 cold Continue
retains exact state. Screenshots verify all three added direction pages.
Commands, maps and rewards remain unchanged; full walkthrough evidence
remains on v1.15 with later focused checks. All three user saves and the
archived v1.17 ROM remain unchanged.

## v1.17 host exploration directions (2026-10-07)

Eleven fresh PASS results: exact host-page/generator scope (one), existing
native dialogue/tree/interior static checks (three), and actual host
conversations with neighboring-room visits on old indoor saves (seven).
Each original two-page conversation remains intact before the new third
page. London directions reach the reading room, Paris the garden workroom,
and Berlin the middle reading room. Repeats, reading and exits retain
party, inventory and all completed case/story/stamp variables. A new v1.17
save cold Continues with exact state. Screenshots check all three new pages.
Commands, maps and rewards remain unchanged; the full walkthrough remains
verified on v1.15, with later focused compatibility checks. Three user saves
and archived v1.16 ROM remain unchanged.

## v1.16 Rooms entry/exit guidance (2026-10-07)

Nine fresh focused PASS results: exact three-line source change (one),
native font fit (one), existing Rooms control/old indoor-save suite (three),
and completed v1.15 save guidance/new v1.16 cold Continue (four). Three
capital screenshots verify readable entry and south-door exit instructions.
L, B, map selection, help controls, location, party, inventory and quest
state remain intact; new Continue retains the repeatable Ada conclusion.
All map/input/save logic is byte-identical to the v1.15 source snapshot.
The full story and optional walkthrough suites were run on v1.15; they
were not rerun wholesale for this three-line display change. The current
guide retains those versioned evidence limits. Three user saves and the
archived v1.15 ROM remain unchanged.

## v1.15 remaining visitor interiors and walkthrough closure (2026-10-07)

Twenty-two fresh checks cover seven remaining optional interiors: London
reading room and Eye gallery, Paris garden workroom and Eiffel room,
Berlin reading room, garden workroom and Gate room. Normal controls check
No/B, entry, every listed reading, exact interior cold Continue, both exits,
re-entry and normal return to Ada. Captured party and completed activities
remain intact. No ROM or user saves changed. Together with the earlier
western-home checks, every capital visitor interior now has exact guide
instructions and completed-save runtime coverage. The walkthrough is done;
future game changes receive focused regression checks, not more walkthrough
expansion unless needed for changed behavior. Prior audit snapshots remain
unchanged; this suite is separately recorded.

## v1.15 completed-save western visitor homes (2026-10-07)

Ten fresh checks visit London sitting room, Paris sketch room and Berlin
sitting room using normal trains and controls from the Bicycle completion
save. Each covers No/B declines, entrance approach, host, notebook, local
display, exact-state interior cold Continue, both exit tiles and re-entry.
A normal train return to Oxford retains Ada's conclusion, captured party,
items, money and completed story/case/stamp history. No ROM or user saves
change. This run covers three western homes, not every visitor interior.
The prior final audit remains a snapshot; these checks are separate.

## v1.15 completed-save Bicycle walkthrough (2026-10-07)

Three fresh checks use walkthrough-gastly-complete.sav with normal controls.
Key Items Bicycle use mounts in Oxford, movement remains controllable,
cold Continue retains riding and exact saved party/inventory/progress,
and using the item again restores walking. A second cold Continue and
Ada's repeatable conclusion retain the captured party and all completed
activities. The initial diagnostic used walking-speed timing and overshot;
the clean rerun uses the existing tile-aware movement helper. No ROM or
user saves changed. This run does not test every terrain or indoor gate.
The earlier final audit remains a snapshot of its nine preceding suites;
these three new runtime checks are recorded separately.

## v1.15 final walkthrough evidence audit (2026-10-07)

All nine versioned walkthrough guides match their recorded SHA256 hashes
and the same v1.15 ROM. Their clean logs contain 72 PASS results in total;
this is an aggregate of previously run checks, not new emulator runs or
72 independent playthroughs. Full fresh routes cover England/Bulbasaur,
France/Chikorita and Germany/Mudkip. Completed-save checks cover cases,
stamps, coast, riverboat, rental Lapras and normal Gastly capture.

Eight later manifests have matching archived verification script copies.
The original England manifest retains logs and script hashes but its two
exact script versions were not archived and no matching copies were found.
Current scripts have since changed; they do not replace that missing
historical source evidence. Older guide snapshots remain unchanged.

Corrected the current guide's route label to German Woodland, matching the
in-game map, and its station-notice version reference to v1.15. No ROM or
user save changes. The final audit JSON indexes manifests, logs, script
copies and the missing historical sources.

## v1.15 optional Gastly with normal capture items (2026-10-07)

Five fresh checks use the completed Germany save after optional rentals.
The Paris shop sells ten Poke Balls for exactly 2000; three Great Balls
from the Reichstag reward are retained. Completed Notre Dame's attendant
honors No/B declines, then offers a real level-12 Gastly. Normal battle Bag
inputs catch it with two earned Great Balls at full HP; no Master Ball,
catch-rate edit, stat edit or inventory injection is used. The capture adds
Gastly to the party while all case/story variables and money remain intact.
Cold Continue retains exact captured party/inventory, and returning to Ada
shows the main conclusion again. This is one real capture run, not a catch
probability guarantee or full-party/PC transfer test. No ROM or user saves
change during verification.

## v1.15 completed-save rental Lapras walkthrough (2026-10-07)

Eight fresh checks use the completed Germany save after optional travel.
London and Oxford rentals honor No/B declines and board free with the exact
party/inventory/progress retained. Water saves at (26,19) cold Continue with
surfing active and controllable steering. Both clear-bank dismounts restore
walking, and repeat rentals preserve rewards. Bicycle boarding clears the
bike state and returns to walking on shore. Final shore Continue retains
all cases, stamps, inventory and Ada's ending. This run has no pending rail
booking and does not retest pre-badge gates. No ROM or user saves change.

## v1.15 completed-save riverboat walkthrough (2026-10-07)

Six fresh checks use the completed Germany save after cases, stamps and
coast trips. Both London/Oxford captains honor No/B declines without state
changes, and free sailings preserve the exact party/inventory/progress.
Each landing cold Continues with exact state, correct present-day map and
controllable movement. Boarding with the Bicycle also permits a round trip
and subsequent movement. A final Oxford cold Continue retains all case
stages, rewards and Ada's ending. This run has no pending rail booking and
does not retest the pre-badge gate or rental Lapras. No ROM or user saves
change during verification.

## v1.15 present-day coast walkthrough checks (2026-10-07)

Nine fresh checks use the completed Germany save after all cases and tour
stamps. Actual travel covers London coach to Dover, Dover ferry to Calais,
Calais north return to Paris, Paris coach to Calais, reverse ferry to Dover
and north return to London. No/B declines preserve exact state. Each coach
and ferry arrival cold Continues with exact party/inventory/progress, and
both port map anchors are correct and present-day. All trips are free, case
stages remain rewarded, and the final cold Continue retains Ada's ending.
The fresh run starts with no pending rail booking and does not test a
booking detour or pre-badge gates. No ROM bytes or user saves change.

## v1.15 optional tour stamps after completion (2026-10-07)

Nine fresh checks use the genuine completed Germany walkthrough save after
all landmark cases. Actual train journeys collect Berlin, London and Paris
stamps in that order. Each stamp is unique, the third guide grants exactly
one Exp. Share, repeated talks grant nothing further, and each save cold
Continues with exact party/inventory/progress. The tour journal shows its
completed lead and all seven milestones. Revisits to all three guides are
safe. A final cold Continue retains stamps, Exp. Share, historical ending,
all cases and Ada's repeatable conclusion. This run does not fill the Items
pocket; full-pocket recovery is prior test coverage, not fresh here. No ROM
bytes or artifact user saves change.

## v1.15 optional-case walkthrough verification (2026-10-07)

Nine fresh checks use the completed Germany/Mudkip walkthrough's genuine
all-accounts battery, then visit all three cases sequentially by normal
train travel. They verify curator acceptance at (8,15), both side clues,
peaceful attendant resolution at (10,5), exact one-time rewards, case cold
Continue and exit/re-entry, all four combined synthesis pages in the ledger,
Ada's ending plus synthesis, and final cold Continue with all case stages
and historical progress retained. Exact rewards are Spell Tag, Rare Candy
and three Great Balls. The prior optional guide had swapped curator and
attendant approaches and incorrectly listed the Reichstag reward as Magnet;
those guide errors are now corrected. This run does not test the optional
Gastly encounter or full reward pockets. No ROM bytes or user saves change.

## v1.15 Germany/Mudkip full walkthrough (2026-10-07)

Eight additional fresh checks complete the documented route from a new
Germany/Mudkip game: London field-study acceptance, all three regional
quests and report-backs, rival and leader battles, historical chapters,
Rose's London ending, Ada's conclusion, cold Continue with Germany still
recorded as home, and both deferred accounts. All three starting countries
now have one separately completed fresh team: England/Bulbasaur,
France/Chikorita and Germany/Mudkip. This does not cover all nine starter
teams or optional cases. The Germany verification manifest records script
and ROM hashes. Country-specific checkpoints retain earlier evidence.
The initial level-14 Mudkip attempt lost to Conrad. The clean fresh rerun
trains in Havel Trail grass to level 16, evolves normally to Marshtomp,
returns to the free clinic every six encounters to restore HP and PP,
then uses Mud-Slap with ordinary Potions. The training verifier handles
depleted PP and returns via the clear central lane. No Pokemon stats,
experience, inventory or quest variables are edited. No ROM or user saves
change during this verification.

## v1.15 France/Chikorita full walkthrough (2026-10-07)

Eight additional fresh checks complete the documented route from a new
France/Chikorita game: London study acceptance, all three regional quests
and report-backs, all three leader battles, historical chapters, Rose's
London ending, Ada's conclusion, exact home-country cold Continue, and
both deferred accounts. These add a second complete starting team to the
prior England/Bulbasaur run. Germany/Mudkip remains a starting-connection
check, not a complete run; optional cases and other teams are not added.
An initial diagnostic run lost to Ellis because the test's battle chooser
omitted Razor Leaf and selected Tackle. Adding Razor Leaf to the normal
button-driven move priorities enabled a clean fresh rerun. No battle stats,
quest variables or inventory were edited. Country-specific checkpoints keep
the prior England evidence intact. The ROM and all three user saves remain
unchanged. See the France verification manifest for scripts and ROM hashes.

## v1.15 walkthrough revalidation (2026-10-07)

Ten additional fresh walkthrough checks passed on the released v1.15 ROM.
A fresh England/Bulbasaur route completes all three regional studies,
required report-backs, rival/leader battles, historical chapters, Rose's
London welcome and Ada's conclusion. The ending cold Continues with all
three badges. Deferred Le Havre and Southampton accounts can then be
filed, and Ada's conclusion repeats. Fresh France/Chikorita and Germany/
Mudkip starts reach London and accept the field study; they are not separate
full story playthroughs. Optional landmark cases and other starter teams
are outside this fresh run. The verification manifest records exact scope.
English/French route names and directional order were also checked against
the route and town signs; no text correction was needed. No ROM bytes or
user saves change during this documentation and verification update.

## v1.15 German route-name consistency (2026-10-07)

Fourteen fresh focused checks: one exact-change static check, three dialogue/
tree/landmark checks, four delivery-direction compatibility checks and six
inactive-contact regressions. Genuine v1.14 saves at LENA's active delivery
and KARL's delivered-report stage cover every direction page, repeated talks,
new Save/cold Continue and station entry. Stationary reads retain exact
party/inventory/progress and grant no rewards. Only three text lines change;
quest commands, cargo tracking, gates and rewards remain exact. This tests
the revised dialogue and compatibility, not a fresh full walking delivery.
The v1.14 ROM and all three user saves are retained. Walkthrough playthrough
evidence remains v1.09.

## v1.14 inactive quest contacts (2026-10-07)

Sixteen fresh focused checks: one exact-change static check, three dialogue/
tree/landmark checks, six inactive-contact compatibility checks and six
journal hand-in regressions. Preparation uses the retained v1.13 ROM,
cold-loads an England start and takes actual trains to each branch town
before saving by its contact. Old batteries and new cold Continue checks
cover all dialogue pages, repeats, unchanged quest stages/inventory/party,
no battle or automatic acceptance, and normal station entry afterward.
The rival's substituted seven-character player/rival names fit the text
window. Only three inactive text blocks change; quest gates, acceptance,
active dialogue, battles and rewards remain exact. The v1.13 ROM and all
three user saves are retained. Walkthrough playthrough evidence stays v1.09.

## v1.13 regional journal hand-ins (2026-10-07)

Thirty-seven fresh focused checks: one exact-change/font-width check, six
old-save and cold Continue report-back checks, and thirty regional journal
checks. Genuine v1.12 batteries cover the England rival report, reviewed
French survey and delivered German parcel; each lead is read repeatedly,
then saved and cold loaded with exact state. The regional suite cold-loads
28 legacy checkpoint batteries, including full-pocket pending rewards and
all three starter countries. Two additional tests use explicitly targeted
trainer-win and stamp fixtures to distinguish intermediate leads. Journal
reads and topic/record switching preserve inventory, progress and location.
Only three text lines change. The v1.12 ROM is retained and all three user
saves are unchanged. The walkthrough's v1.09 playthrough is prior evidence.

## v1.12 exterior Gym guidance (2026-10-07)

Sixteen fresh focused checks: one exact-change static check, three font/tree/
landmark checks, six Gym-sign emulator checks and six station entrance sign
regressions. Genuine v1.11 outdoor batteries exercise all three Gym signs,
three pages, repeated reads, station entry/exit, local approaches and new
cold Continue saves. Exact-change checks retain indoor statue text, leader
quest gates, badge/reward scripts, maps and rail commands. Stationary reads
preserve exact state; walking preserves inventory/progress. The v1.11 ROM
is retained and all three artifact user saves are unchanged. Prior walkthrough
playthrough evidence remains v1.09; it was not rerun for these text changes.

## v1.11 branch-town exterior signs (2026-10-07)

Sixteen fresh focused checks: one exact-change static check, three font/tree/
landmark checks, six exterior-sign emulator checks and six station-notice
regressions. Genuine v1.09 indoor batteries cover all three towns, both sign
pages, repeat reads, station entry/exit, Gym/contact approaches and new cold
Continue saves. Stationary reads preserve exact party/inventory/progress;
walking preserves inventory/progress. Only three text blocks change.
The v1.10 ROM is retained and all three artifact user saves are unchanged.
The walkthrough's ten v1.09 checks remain prior evidence, not fresh v1.11 runs.

## v1.10 branch-station verification - 2026-10-07

19 fresh focused PASS results: branch static (2), retained capital-board
static (2), native widths/landmark generation (3), branch old-save and
cold Continue runtime (6), and capital old-save/Continue runtime (6).
Each branch notice adds exactly one background event on the existing
solid framed wall picture. The complete prior map data and staff scripts
are retained in branch-station-v109.json; terrain, staff, services, exits,
shared rail script and map IDs remain unchanged. The generator is stable.
Genuine v1.09 indoor batteries were made before the change using normal
Save. Each reads both pages twice, exits, reaches the Gym and named-contact
approaches, re-enters, saves, cold Continues with exact state and reads again.
Stationary reads preserve exact party, money, inventory and progress;
walking checks preserve all inventory and progress. No booking is lost.
The three capital-board batteries repeat the same existing regression checks.
All six stations' notice lines pass native-font width checks. Screenshots
verify new notice pages. Packaging retains v1.09 and all three user saves.
The walkthrough's ten v1.09 checks remain prior evidence, not fresh v1.10
checks; v1.10 only adds these optional wall notices to the same story route.

## Complete walkthrough verification - 2026-10-07

WALKTHROUGH.md covers the unchanged v1.09 ROM, SHA256
`a564453864fc43991120195b6af0847cde4489fa0c3a33f947e7aeee86372ff8`.
Run `python3 scripts/test_walkthrough.py` then
`python3 scripts/test_walkthrough_ending.py` through the existing WSL mGBA
bridge. Ten fresh PASS results cover three newly initialized country starts,
the full England/Bulbasaur main route and the ending account follow-up.
France/Chikorita and Germany/Mudkip starts independently reach London and
accept the study. The England party then wins Oliver, Alice, the rival and
all three Gym leaders using real battles and normal clinic/shop controls.
It completes every regional report, the Celebi vision, refuge blanket,
departure news, Beauvais message/account, care supplies, Pidgey reunion,
Amiens reception/reunion/account/bulletin, Rouen book, dock instructions,
Southampton luggage, Rose welcome and Ada conclusion. No quest variables,
party stats, money or battle outcomes are fabricated. Normal in-game saves
are made at each badge, the first account and the ending; cold Continue
checks the completed ending. Deferred port and Southampton accounts are
filed after Rose and Ada's conclusion is read again. Its screenshot shows
"Your account is complete." The conclusion test allows more dialogue inputs
than the short-conversation helper because it also offers a deferred report.
The first diagnostic run's helper timeout is retained separately; the final
full run and ending follow-up must both finish cleanly before packaging.

Other starter teams and complete France/Germany battle playthroughs are not
separate fresh runs in this check. The guide supplies their starting routes
and shared quest order. Optional landmark case instructions are checked
against current scripts and map events, not counted as fresh runtime checks.
The package includes exact coverage, script hashes and guide/ROM hashes in
`artifacts/releases/v1.09-WALKTHROUGH-VERIFICATION.json`, clean logs and the
conclusion screenshot. The ROM and all three artifact user saves stay exact.

## v1.09 walking-detour verification - 2026-10-07

34 fresh focused PASS results: detour static (1), detour runtime (4),
completion static (1), walking arrivals/return trips (6), resume static (1),
transfer static (2), clerk compatibility (2), station compatibility (2),
native widths/landmark generation (3), resume choices (2), exploration and
Continue (2), and clerk runtime (8). Restoring the Resume text block gives
the complete v1.08 source byte-for-byte; only one dialogue line changed.
Genuine v1.08 batteries were created by walking to Oxford and Chantilly
with Oranienburg still booked. Cold Continue shows the correct next capital
and remaining train count from the independent route graph. Keeping the
booking preserves exact party, money, inventory, flags, progress and location.
Boarding rejoins the capital line; another Save/Continue retains exact state,
then the trip completes at Oranienburg and clears only the booking. Native
font checks and screenshots verify the revised prompt. All focused rail
regressions run anew. Packaging retains v1.08 and all three user saves.
The broad v1.02 baseline remains retained, not counted as newly run.

## v1.08 walking-arrival verification - 2026-10-06

29 fresh focused PASS results: completion static (1), walking arrivals and
cold Continue/return trips (6), resume static (1), transfer static (2),
clerk compatibility (2), station compatibility (2), native widths and
landmark generation (3), resume decisions (2), exploration/Continue (2),
and prior clerk runtime checks (8). Restoring only completion dialogue
reproduces the complete v1.07 rail source byte-for-byte. The compatibility
helper now restores exact byte blocks, including mixed line endings.
Three genuine v1.07 batteries were created through normal train travel,
walking and Save at Oxford, Chantilly and Oranienburg. Each cold Continues,
shows the correct destination and zero trains remaining, clears only the
booking, stays at the clerk and releases controls. Speaking again opens
the fresh stop list. Saving completion and cold Continuing preserves exact
state and permits a normal return train. Native-width checks include the
longest destination name; completion screenshots are visually checked.
All prior focused rail checks run anew. Packaging preserves v1.07 and all
three user saves. The broad v1.02 baseline is retained, not counted anew.

## v1.07 saved-trip choices verification - 2026-10-06

22 fresh focused PASS results: resume text/static (1), transfer static (2),
clerk compatibility (2), station compatibility (2), native widths and
landmark generation (3), resume decisions (2), exploration/cold Continue
(2), and prior clerk runtime checks (8). Restoring only resume dialogue
reproduces the complete v1.06 rail script byte-for-byte. All commands,
routing, booking state, cancellation and warps remain exact.
Genuine old London transfer and saved Paris exploration batteries cold
Continue and show all three resume pages. NO and B open cancellation;
NO there retains exact party, money, inventory, flags and progress. YES
boards the expected train. The Paris garden/save/resume/final-arrival
journey and six-station previews/cancellations also pass anew.
Native font widths include maximum station-name substitutions; screenshots
verify the resume pages. Packaging preserves v1.06 and all three user saves.
The broad v1.02 baseline is retained, not counted among fresh checks.

## v1.06 intermediate rail guidance verification - 2026-10-06

19 fresh focused PASS results: transfer text/static (2), clerk compatibility
(2), station compatibility (2), native widths/landmark generation (3),
exploration and cold Continue (2), and existing clerk runtime checks (8).
Restoring only the intermediate boarding text reproduces v1.05 byte-for-byte.
The independent route graph confirms every intermediate stop has a wall notice.
A genuine v1.04 saved London transfer visits the Paris notice and garden room,
saves outside, cold Continues, then resumes via Berlin to Oranienburg.
Final arrival clears the booking; money, inventory, quest state and home country
remain intact. Stationary decisions also preserve exact party data.
Native text widths include the longest destination substitution. Screenshots
cover all three boarding pages and local exploration. Packaging retains v1.05
and verifies all three user saves unchanged. These are focused checks; the
previous broad v1.02 release baseline is retained, not counted as newly run.

## v1.05 rail-clerk cue verification - 2026-10-06

17 focused PASS results: rail cue static (2), station compatibility (2),
wall-notice compatibility (2), native widths/landmark generation (3),
six-station cancellation checks (6), retained-transfer decisions (1),
and retained-transfer completion (1). Only the welcome and same-station
text blocks change. Every booking, cancellation, routing and warp command,
and every preview/resume/boarding text block, matches the v1.04 source.
Retained arrival batteries at all six stations exercise B, Exit, selecting
the current station, and No/B on a route preview. Exact party, money,
inventory, progress and location remain unchanged. Preview next-stop and
remaining-train values are checked against the independent route graph.
A genuine v1.04 London-to-Oranienburg transfer keeps its booking on No/B,
clears it only on confirmed cancellation, and can instead complete through
Paris and Berlin. Final arrival clears the booking and retains inventory,
quest state and home country. Native cue screenshots were checked.
Packaging retains v1.04 and verifies all three user saves unchanged.

## v1.04 station wall-notice verification - 2026-10-06

25 focused PASS results: notice static (2), station-sign static (2), arrival
static (2), Places widths (1), native dialogue/landmark generation (3),
wall-notice old saves and cold Continue (6), station sign visits/saves (6),
and Rooms controls in retained capital saves (3). Genuine v1.03 batteries
were created beside the existing framed wall picture in all three stations.
They read the new notice twice, exit/re-enter, read again and create new
saves. Cold Continue retains position and progress, rereads and exits.
Each read retains exact party/progress data; walks retain inventory, money
and quest state. Exact room grids, staff, service scripts, exits and IDs
are retained. Existing station compatibility checks permit only the new
background event and appended notice script; the dedicated static check
independently requires those additions. Native widths and notice screenshots
were checked. The broader v1.02 baseline remains archived. Packaging retains
v1.03 and verifies all three user saves unchanged.

## v1.03 station-sign verification - 2026-10-06

23 focused PASS results: station static (2), northern arrival static (2),
Places widths (1), native dialogue/landmark generation (3), station visits
and cold saves (6), northern arrival visits/saves (6), and Rooms controls
in retained capital saves (3). The broader 190-check v1.02 baseline remains
archived; this release changes only three station-sign text blocks.
Each city enters its station at native threshold (4,8), steps inward and
uses the two-step exit. New cold saves read the sign again and use the
side approach to the marked station exit. All sign pages are read twice,
and every neighborhood
room approach is reachable. Each reading retains exact party/progress;
walks retain money, inventory and quest state. Full outdoor maps, station
maps/scripts, staff, warps, map IDs and shared train script match v1.02.
Source generation and native widths pass; all three station-sign screenshots
were checked. Packaging retains v1.02 and verifies three user saves unchanged.

## v1.02 visible Berlin-marker verification - 2026-10-06

190 focused PASS results: the preceding 184 plus two marker static checks,
two marker emulator checks and two retained Gate static checks. Berlin (14,4) alone changes from pavement
0x3165 to native solid sign 0x402. All other terrain, event definitions,
objects, IDs and encounters are retained. Three adjacent lane columns
remain open. Older terrain checks explicitly normalize only this one
known tile before comparison; the marker check independently requires it.
A genuine v1.01 battery saved on (14,4) cold-loads at the same position,
refreshes the sign tile, steps down safely, reads twice, circles the sign
and retains progress. A new save cold-loads, rereads and crosses both ways
between Berlin and its countryside. The Gate generator explicitly owns its background events and excludes
the library catalog inherited through its template. Native sign screenshots
were checked.
Packaging retains v1.01 and verifies all three user saves unchanged.

## v1.01 northern arrival-sign verification - 2026-10-06

184 focused PASS results: the preceding 176 plus two arrival static checks
and six arrival emulator checks. Old starting batteries walk north into
each countryside and back, read all four arrival-sign pages twice, save,
cold Continue, reread and return to the countryside. Each reading retains
exact party and progress data. Walking retains inventory, money and quest
state. Full capital/countryside terrain, events, IDs and wild encounter
data match the v1.00 fixtures. Existing countryside text remains first.
All three signs regenerate identically and the native font check covers
the added lines. Arrival-page screenshots were checked. Packaging retains
v1.00 and verifies all three user saves unchanged.

## v1.00 capital Rooms-page verification - 2026-10-06

176 focused PASS results: the preceding 173 plus three Rooms emulator
checks. Retained London, Paris and Berlin batteries browse the new pages,
toggle L, reset on stop changes, ignore L at noncapital stops and preserve
R/B/START/A/story controls. Exact party, money, inventory, quest state,
preferences, player location and native Help enabled/R-toggle states are retained on exit.
The Places font check covers all 50 strings, including the new headings,
shortcut hints and room lines. Screenshots of all three room pages and
noncapital fallback were checked. Existing map/event generators and all
city interactions remain covered. Packaging retains v0.99 and verifies
all three user saves unchanged. The display state is transient; no new
save variables, map IDs, terrain or events are introduced.

## v0.99 Berlin courtyard-notice verification - 2026-10-06

173 focused PASS results: the preceding 169 plus two notice static checks
and two notice emulator checks. The retained v0.98 courtyard battery reads
all four pages twice, walks to each room approach and loops around the
courtyard. A new save cold-loads at the sign, reads again and returns to
the countryside. Each read preserves exact party and progress data; the
walking route preserves money, inventory, quest variables and flags.
The full Berlin map, event definitions, objects and map IDs stay exact.
Generator stability, native font widths and sign screenshots were checked.
Packaging retains v0.98 and verifies all three user saves unchanged.

## v0.98 Berlin garden-note verification - 2026-10-06

169 focused PASS results: the preceding 166 plus two bench static checks
and one retained v0.97 garden-room battery check. The old indoor save reads
both workbenches from north and south and exits without changing progress.
Each read checks exact party bytes and progress before/after dialogue.
Walking can trigger the native friendship step update; the full walking
route separately checks money, inventory, quest variables and flags.
Normal visits read both notes; cold Continue and both exits remain covered.
All eight existing solid bench cells support background interactions. Exact
room terrain, objects, exits and map IDs are retained. Generator stability,
native font widths and screenshots were checked. The garden generator also
removes the unused catalog script copied from its library template.
Packaging retains v0.97 and verifies all three user saves unchanged.

## v0.97 Berlin library catalog verification - 2026-10-06

166 focused PASS results: the preceding 164 plus two catalog static checks.
Normal visits and the retained v0.66 indoor save read the catalog; the old
save reads from north and south without changing progress. Cold Continue,
both exits and countryside return remain covered. Exact room terrain,
objects and map IDs are retained. Library background events belong to the
catalog and the garden workroom has no inherited sitting-room events.
Native font widths and catalog screenshots were checked. Packaging retains
v0.96 and verifies all three user saves unchanged.

## v0.96 Berlin guestbook verification - 2026-10-06

164 focused PASS results: the preceding 144 plus guestbook static (2),
Berlin neighborhood static (2), facades (2), sitting room (3), library (3),
garden workroom (2), companion (2), Berlin (2) and Reichstag (2).
Normal visits and retained v0.65 indoor saves read the table from north
and south; normal Save/Continue and both exits remain covered. Exact room
terrain, objects, exits and map IDs are retained. Native dialogue widths
and room screenshots were checked. Packaging retains v0.95 and verifies
all three user saves unchanged.

## v0.95 Paris workbench-plan verification - 2026-10-06

144 focused PASS results: the preceding 141 checks plus two plan static
checks and one pre-change workroom battery check. The v0.94 battery reads
both benches from north and south and exits without changing progress.
Normal visits also read both plans. All eight existing solid bench cells
support background interactions, while exact room terrain, walking space,
objects, exits and map IDs stay unchanged. Font widths and screenshots
were checked. Packaging retains v0.94 and verifies all three user saves.

## v0.94 Paris sketch-display verification - 2026-10-06

141 focused PASS results: the preceding 138 checks plus two display static
checks and one pre-change indoor battery check. Only four solid wall cells
change artwork; every walking cell and existing object/exit stays intact.
The v0.93 battery refreshes the complete indoor grid at its original saved
position, reads the display and exits without changing progress. Normal
visit and cold-save checks include the display and full-grid comparison.
Native dialogue widths and screenshots were inspected. Packaging retains
v0.93 and verifies all three user artifact saves unchanged.

## v0.93 Paris roof-detail verification - 2026-10-06

138 focused PASS results: the preceding 136 checks plus two Paris facade
static checks. Only the eastern roof art changes. Native artwork copies
retain flip bits, transparency and behavior; four roof shades map to an
existing blue-gray palette. Shared palettes and every other outdoor tile
are unchanged. Assets regenerate identically. The full-grid lane old-save
and cold-save checks and both room checks pass. Roof screenshots were
inspected. Packaging retains v0.92 and verifies all three user saves.

## v0.92 Paris garden-workroom verification - 2026-10-06

136 focused PASS results: the preceding 131 checks plus the appended map,
two workroom static and two interaction/save checks. No/B cancellation,
entry, gardener/notebook, reentry, both exits and normal Save/cold Continue
pass. The indoor map identifies France; return to the countryside works.
All earlier map IDs and exact outdoor terrain remain unchanged. Generation
and dialogue-width checks pass. Workroom and travel-map screenshots were
inspected. Packaging retains v0.91 and verifies three user saves unchanged.

## v0.91 Paris sketch-room verification - 2026-10-06

131 focused PASS results: the previous 126 checks plus the appended map,
two sketch-room static and two interaction/save checks. No/B cancellation,
entry, host/sketchbook, reentry, both exits and normal Save/cold Continue
pass. The indoor travel map identifies France; return to the countryside
works. Exact outdoor terrain and every preceding map ID are retained.
Generation and native dialogue-width checks pass. Interior and travel-map
screenshots were inspected. Packaging retains v0.90 and verifies all three
user artifact saves unchanged.

## v0.90 Paris side-lane verification - 2026-10-06

126 focused PASS results: the previous 122 checks plus two side-lane static
and two walking/save checks. Paris grows to 64x46 within the map buffer.
Old walkable tiles, objects, entrances and IDs are retained; only the lane
mouth opens the previous tree boundary. Both private home approaches,
flower-bed circuit and signs are reachable from an older battery. The
complete loaded grid matches generated terrain. Save/cold Continue at
(60,43) retains position and progress; return through the old district to
the countryside works. Native front/sign screenshots and text widths were
checked. Packaging retains v0.89 and verifies three user saves unchanged.

## v0.89 Paris promenade sketcher verification - 2026-10-06

122 focused PASS results: the previous 107 checks plus two sketcher static,
two sketcher interaction/save, one Paris garden static, two garden, two
promenade static, two Paris walking/save, two Eiffel visitor and two
Notre-Dame case checks. An old Paris battery restores the sketcher without
reentry. Three greetings, collision, promenade routes, normal Save/cold
Continue and countryside return retain progress. All Paris tiles, earlier
objects, entrances and map IDs are unchanged. Sketcher screenshots were
inspected; native dialogue-width checks pass. Packaging retains v0.88 and
verifies all three user artifact saves unchanged.

## v0.88 London photo album verification - 2026-10-06

107 focused PASS results: the previous 104 checks plus two album static
checks and one pre-change sitting-room battery check. The album occupies
an existing solid table tile. Exact indoor/outdoor grids, prior objects,
exits and map IDs are retained. The v0.87 battery reaches the album and
exits without changing progress; normal visit checks read it alongside
the host and notebook. Both home cold-save checks, generation and dialogue
width checks pass. Album screenshots were inspected. Packaging retains
v0.87 and verifies all three user artifact saves unchanged.

## v0.87 London reading-room furnishings - 2026-10-06

104 focused PASS results: the previous 101 checks plus two furnishings
static checks and one pre-change indoor battery check. Every old walkable
position remains open at the same elevation. Objects, exits, map IDs and
the full outdoor district remain unchanged. A v0.86 battery reaches the
new cabinet and exits while retaining progress. The normal visit checks
read the cabinet alongside the host and notebook. Both exit tiles and
Save/cold Continue pass. Interior and cabinet-dialogue screenshots were
inspected. Packaging retains v0.86 and verifies all three user saves.

## v0.86 London home roof verification - 2026-10-06

101 focused PASS results: the previous 99 checks plus two facade static
checks. Only the eastern roof metatiles change; each copy preserves native
artwork, flip bits and behavior attributes. Four roof shades map to slate
blue using existing palette 8; shared palettes remain unchanged. All paths,
doors, map IDs and interiors are intact.
Both homes retain invitation, conversation, exit and cold-save behavior.
The lane test checks the complete loaded grid and its cold-save refresh.
Roof screenshots are inspected. Packaging retains v0.85 and verifies all
three user artifact saves unchanged.

## v0.85 London reading room verification - 2026-10-06

99 focused PASS results: the previous 94 checks plus the appended map,
2 reading-room static and 2 interaction/save checks. Declining with No/B,
entry, both conversations, reentry, both front exits, indoor Save/cold
Continue, London country and return to the countryside pass. All prior map
IDs and outdoor tiles are unchanged. The western home checks also pass.
Dialogue widths and screenshots are checked. Packaging retains v0.84 and
verifies all three user artifact saves unchanged.

## v0.84 London sitting room verification - 2026-10-06

94 focused PASS results: the previous 89 checks plus the appended map,
2 home static and 2 home interaction/save checks. Yes/No and B cancellation,
conversations, reentry, both exits, indoor Save/cold Continue, London map
country and countryside return pass. Every outdoor tile and previous map
ID is unchanged. Generation and dialogue-width checks pass. Interior and
travel-map screenshots were inspected. Packaging retains v0.83 and
verifies all three user artifact saves unchanged.

## v0.83 London lane verification - 2026-10-06

89 focused PASS results: the prior 71 focused checks plus 2 street static,
2 street walking/save, 3 London walking/save, 2 waterfront generation,
2 Eye static, 2 Westminster case, 2 Eye gallery, 1 garden static and
2 garden interaction/save checks. The v0.82 footprint retains old walkable
positions and terrain except four grass-to-paving cells. Only the new
lane mouth removes old boundary collision. Both homes are solid and both
approaches, the full public circuit and signs are reachable from an older
battery save. Save/cold Continue at x60 retains player position, full map
grid and progress; return to the Eye, both bridges and countryside works.
Earlier entrances, objects, map IDs and historical London are retained.
Generation is stable and the expanded grid fits hardware limits. Native
building fronts and residential sign screenshots were inspected. Packaging
retains v0.82 and verifies user artifact save hashes.

## v0.82 Purple outfit verification - 2026-10-06

71 focused PASS results: the 69 previous focused checks plus 2 Purple
outfit checks. Red and Leaf use the selected Purple ramp while every
non-clothing palette entry matches the native Classic palette. Walking,
cycling and dismount retain the color. A turned cycling preview was
inspected along with the Purple menu. Normal Save/cold Continue retains
Purple and avatar selection with identity, party, inventory, progress and
location unchanged. A wraps Purple to the exact Classic palette. Existing
Blue and Green coverage passes with Green-to-Purple-to-Classic cycling.
Restore confirmation cancellation preserves Purple; confirmation restores
all defaults. Four-direction preview, Places, field Help restoration and
older indoor map labels still pass. Packaging retains v0.81 and verifies
user artifact save hashes.

## v0.81 avatar direction verification - 2026-10-06

69 focused PASS results: 47 map/path, 3 capital layout, 3 static checks,
2 World Options, 1 movement, 1 live preview, 4 indoor map locations,
2 Places navigation, 1 font-fit, 1 preview-facing, 2 defaults and 2 outfit
checks. R cycles all four native standing animations for every avatar in
both walking and cycling poses. Four turns wrap; pose/avatar changes
retain direction. Restore confirmation ignores R, cancellation restores
the view, and reopening resets to front. Party, inventory, progress,
preferences and field location remain unchanged. The previous native Help
R-button reservation is restored after options close. Side-view bicycle
and back-view walking screenshots were inspected. Both preview control
hints fit the native font. Packaging retains v0.80 and verifies user
artifact save hashes.

## v0.80 Places guide verification - 2026-10-06

64 focused PASS results: 47 map/path, 3 capital layout, 3 static checks,
2 World Options, 1 movement, 1 live preview, 4 indoor map locations,
2 Places navigation and 1 Places font-fit check. Present-day and historical
battery saves browse all eight stops with wrapped D-pad selection. R/B/START
return to the map, A shows routes, and SELECT opens the journal. Journal
navigation ignores R. The native Help R-button reservation is restored on
exit. Party, inventory, story progress, cosmetic preferences and location
remain unchanged. All 35 Places lines and the map shortcut hint fit the
actual native font and screen margins. Berlin directions and returned map
screenshots were inspected. Packaging retains v0.79 and verifies user
artifact save hashes.

## v0.79 London garden verification - 2026-10-06

104 focused PASS results: the prior 92 release checks plus 1 London resident
static check, 2 garden interaction/save, 2 waterfront generation, 3 London
walking/save, 2 Westminster case and 2 Eye gallery checks. Every v0.78
London tile and all four original city objects are unchanged. An older
London battery immediately restores the visitor and Jigglypuff. Repeated
dialogue releases controls and preserves the full party across each
interaction, with inventory and story progress unchanged throughout the
walk. Garden loops, gallery approach and bridge routes remain reachable.
Normal Save/cold Continue retains location and party, supports another
greeting and returns to the countryside. Waterfront artwork regenerates
identically using the bundled image-enabled Python runtime; generated JSON
line endings are normalized. Visitor and companion screenshots were
inspected. Packaging retains v0.78 and verifies user artifact save hashes.

## v0.78 Paris garden verification - 2026-10-06

92 focused PASS results: the prior 81 release checks plus 1 Paris resident
static check, 2 garden interaction/save, 2 promenade generation, 2 Paris
walking/save, 2 Notre-Dame case and 2 Eiffel visitor-room checks. Every
v0.77 Paris tile and both original city objects are unchanged. An older
Paris battery restores the observer and Psyduck immediately. Three rounds
of dialogue release controls and preserve the complete party across each
interaction, with inventory and progress unchanged throughout the walk.
Normal walking friendship gains are allowed between interactions. Existing
promenade loops and landmark approaches remain reachable. Normal Save/cold
Continue retains the location and party, supports another greeting and
returns to the countryside. New dialogue fits the window; garden dialogue
screenshots were inspected. Packaging retains v0.77 and verifies user
artifact save hashes.

## v0.77 Gate visitor-room verification - 2026-10-05

81 focused PASS results: 47 map/path, 3 capital layout, 3 static checks,
2 World Options, 1 movement, 2 flower, 2 defaults, 2 outfit, 1 live preview,
4 earlier indoor map locations, 2 neighborhood generation, 2 companion,
2 Berlin walking/save, 2 garden-room, 2 Reichstag case, 2 Gate static and
2 Gate visit/save checks. No/B decline the invitation at the west pillar.
The guide and both displays release controls without changing progress,
inventory or party; both front exits return to the same approach. Normal
Save/cold Continue retains the indoor position, and the regional map shows
Germany. The complete v0.76 Berlin tile map and every preceding Europe map
ID are identical. Gate/Capital regeneration is stable and the central
passage remains open. Interior and country-map screenshots were inspected.
Packaging retains v0.76 and verifies user artifact save hashes.

## v0.76 Berlin companion verification - 2026-10-05

76 focused PASS results: 46 map/path, 3 capital layout, 3 static checks,
2 World Options, 1 movement, 2 flower, 2 defaults, 2 outfit, 1 live preview,
4 indoor map locations, 2 neighborhood generation, 2 companion, 2 Berlin
capital walking/save, 2 garden-room and 2 Reichstag case checks. An older
courtyard battery spawns the new companion immediately. Its occupied cell
blocks entry, three greetings release controls and preserve party,
inventory and progress, and all visitor approaches remain reachable.
Normal Save/cold Continue retains the player location; another greeting
and countryside return pass. The new stationary save-template restoration
leaves the original city NPCs intact. Outdoor tiles and IDs are retained.
Courtyard and dialogue screenshots were inspected. Packaging retains
v0.75 and verifies user artifact save hashes.

## v0.75 walking/cycling preview verification - 2026-10-05

66 focused PASS results: 46 map/path, 3 capital layout, 3 static checks,
2 World Options, 1 movement, 2 flower, 2 defaults, 2 outfit, 1 live preview
and 4 indoor map location checks. SELECT displays the native bicycle pose
with green Leaf clothing and retains every saved preference. Twelve avatar
changes preserve the cycling preview and clothing colors. SELECT returns
to WALK; closing and reopening begins at WALK with field position and
progress unchanged. Reset confirmation and regional map cleanup still pass.
The cycling preview screenshot was inspected. Packaging retains v0.74
and verifies user artifact save hashes.

## v0.74 live preview and indoor map verification - 2026-10-05

66 focused PASS results: 46 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 World Options checks,
1 registered/cycling control check, 2 flower checks, 2 defaults checks,
2 outfit checks, 1 live preview check and 4 indoor map location checks.
The preview displays blue Red and green Leaf and survives twelve repeated
avatar changes with the selected clothing palette. Restore confirmation
hides it, cancellation restores it, and confirmation displays defaults.
Closing options destroys the preview; opening the regional map afterward
leaves no preview sprite. Existing Eiffel visitor and three Berlin room
saves select the correct country and return with location and progress
unchanged. Preview, confirmation and Eiffel map screenshots were inspected.
Packaging retains v0.73 and verifies user artifact save hashes.

## v0.73 outfit color verification - 2026-10-05

61 focused PASS results: 46 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 World Options checks,
1 registered/cycling control check, 2 flower checks, 2 defaults checks
and 2 outfit checks. Real input selects blue Red and green Leaf outfits.
Tests compare all sixteen player palette entries: only clothing entries
8, 11 and 12 change. Cycling and dismount retain the chosen palette.
Normal Save/cold Continue retains both avatar and outfit; A wraps from
green to the exact classic palette. Trainer identity, party, inventory,
progress and location remain unchanged. Restore Defaults clears the new
outfit preference along with the original settings. Six-row menu and
both outfit/cycling screenshots were inspected. Packaging retains v0.72
and verifies user artifact save hashes.

## v0.72 World Options defaults verification - 2026-10-05

59 focused PASS results: 46 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 World Options checks,
1 registered/cycling control check, 2 flower-decoration checks and
2 restore-defaults checks. The fifth row wraps from the first via UP.
Left/Right on the restore row leave preferences unchanged. B and START
both cancel the confirmation without leaving the options menu. A confirms
all four defaults. Field return restores the original avatar while trainer
identity, party, inventory, story progress and position remain identical.
A normal save cold-loads with all defaults and progress intact. Original
option controls, cycling continuity and flower restoration still pass.
Confirmation and five-row menu screenshots were inspected. Packaging
retains v0.71 and verifies user artifact save hashes.

## v0.71 flower decoration verification - 2026-10-05

57 focused PASS results: 46 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 World Options checks,
1 registered/cycling control check and 2 flower-decoration checks.
The fourth menu row wraps from the first via UP and accepts Left/Right/A.
The test compares the complete loaded map grid before and after toggling,
walks across the flower beds, saves the lawn preference and cold-loads at
the same location with matching party, inventory, progress and identity.
Restoring flowers leaves the grid and progress identical. The original
avatar, map settings, registration and cycling behavior still pass.
Menu, flowers-on, lawn, cold-load and restored-flower screenshots were
inspected. Packaging retains v0.70 and verifies user artifact save hashes.

## v0.70 London Eye gallery verification - 2026-10-04

61 focused PASS results: 46 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 gallery terrain/generation
checks, 2 gallery visit/save checks, 3 London walking/save checks and
2 Westminster investigation/save checks. Gallery No/B cancellation,
attendant, both displays, both exits, re-entry and indoor Save/cold Continue
use emulator button input. The outdoor London map is byte-identical to
v0.69. The new gallery is appended after the Eiffel visitor room, retaining
prior map IDs. The newly added entrance event was normalized into the
London generator's existing ordering; repeated generation is stable.
Windows, open floor, exhibits and dialogue were inspected in-game.
Packaging retains v0.69 and verifies user artifact save hashes.

## v0.69 Eiffel visitor room verification - 2026-10-04

59 focused PASS results: 45 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 Eiffel terrain/generation
checks, 2 Eiffel visit/save checks, 2 Paris walking/save checks and
2 Notre-Dame investigation/save checks. Eiffel No/B cancellation,
guide, both exhibits, front exits, re-entry and indoor Save/cold Continue
use emulator button input. Progress and inventory remain unchanged.
The Paris outdoor map is byte-identical to v0.68, including every saved
position and landmark approach. The new map is appended after existing
indoor rooms. Generators retain both Paris visitor entrances. In-game
room and dialogue images were inspected. Packaging retains v0.68 and
verifies user artifact save hashes.

## v0.68 Berlin roof variety verification - 2026-10-04

66 focused PASS results: 44 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 neighborhood checks,
2 roof compatibility/generation checks, 2 Berlin walking/save checks,
3 home checks, 3 reading-room checks, 2 workroom checks and 2 Reichstag
case/save checks. Exactly 30 solid roof cells change; every tile's
collision, elevation and behavior is identical to the v0.67 fixture.
The three door tiles are unchanged. The green palette slot was unused
in the previous map. Regeneration is byte-stable and the tileset stays
within hardware limits. Terracotta, green and slate roof colors were
inspected in-game. All three room visits, old indoor saves, courtyard
walking and save reloads are exercised. Packaging retains v0.67 and
verifies user artifact save hashes.

## v0.67 Berlin garden workroom verification - 2026-10-04

64 focused PASS results: 44 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 neighborhood checks,
2 Berlin walking/save checks, 2 Reichstag case/save checks, 3 home checks,
3 reading-room checks and 2 workroom checks. Workroom entrance No/B,
gardener, tool notes, planting plan, both front exits, re-entry and indoor
Save/cold Continue use emulator button input. Older v0.65 sitting-room and
v0.66 reading-room battery saves retain their map IDs and progress.
All three rooms return to their own courtyard doorway and onward routes.
The workroom benches, dialogue and records were inspected in-game.
Outdoor terrain and resident positions are unchanged; generator results
are repeatable. Packaging retains v0.66 and verifies artifact save hashes.

## v0.66 Berlin reading room verification - 2026-10-04

60 focused PASS results: 43 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 neighborhood checks,
2 Berlin walking/save checks, 2 Reichstag case/save checks, 3 sitting-room
checks and 2 reading-room checks. Both reading-room records and the
librarian open dialogue and release controls. Entrance No/B, both exits,
re-entry, indoor Save/cold Continue and countryside return use emulator
button input. A retained v0.65 sitting-room battery save loads at its
original position, preserves progress, and supports conversation, exit
and re-entry. Existing map IDs and exterior terrain are unchanged.
The new room and dialogue images were inspected. Room generation is
repeatable. Packaging retains v0.65 and verifies artifact save hashes.

## v0.65 Berlin sitting room verification - 2026-10-04

56 focused PASS results: 42 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 neighborhood checks,
2 Berlin walking/save checks, 2 Reichstag case/save checks and 2 home
visit/save checks. Entrance No/B cancellation, host and notebook dialogue,
exit/re-entry and both southern exit tiles use real emulator input.
A save inside the room cold-loads with matching progress and inventory,
then exits through Berlin to the countryside. Room generation is stable;
all previous map IDs and exterior tile data are retained. Dialogue fits
the text window. Final room and conversation images were inspected; unused
stair artwork was replaced with matching wall and floor tiles and the
home checks rerun. Packaging preserves v0.64 and artifact saves by SHA256.

## v0.64 Berlin courtyard residents verification - 2026-10-04

53 focused PASS results: 41 map/path checks, 3 capital layout checks,
3 static dialogue/tree/regeneration checks, 2 neighborhood checks,
2 Berlin emulator walking/save checks and 2 Reichstag case/save checks.
Neighborhood assertions cover both resident positions, unique scripts,
lock/faceplayer/release behavior and generator stability. Emulator input
opens and closes both conversations from an older Berlin battery save,
then saves in the court and cold-loads before returning to the countryside.
The old-save template refresh restores only the two new stationary NPCs.
Existing quest progress and inventory remain unchanged. Dialogue screenshots
were inspected. Packaging retains v0.63 and verifies artifact save hashes.

## v0.63 Berlin neighborhood verification - 2026-10-04

53 focused PASS results: 41 map/path checks, 3 capital layout checks,
3 dialogue/tree/regeneration checks, 2 neighborhood compatibility checks,
2 Berlin emulator walking/save checks and 2 Reichstag investigation/save
checks. The new courtyard, both side lanes, southern loop, signs and a
solid residential doorway are exercised with button input. A save made
inside the extension cold-loads at the same position with its progress,
then returns through the original hub to the countryside.

The full v0.62 Berlin footprint is checked: old walkable tiles are unchanged
except for the paved grass approach, and only the boundary opening loses
collision. New buildings are outside that footprint. The map buffer fits
hardware limits. The previous v0.62 ROM and all artifact saves are checked
by SHA256 during packaging. In-game street artwork was inspected.

## v0.62 London waterfront verification - 2026-10-04

57 focused PASS results: 41 map checks, 3 capital layout checks, 3 static
text/tree/generator checks, 2 waterfront preservation/generation checks,
1 historical layout check, 3 modern London walking/save checks, 2
Westminster case/save checks and 2 historical London walking/save checks.

Both rows of each bridge are crossed in both directions with real emulator
input. The garden loop, four signs, clinic, station, map menu and cold saves
are exercised. The longer walking loop correctly increases friendship;
the test verifies that only friendship and its checksum can change in the
party, while inventory and story progress stay identical. The Westminster
case is completed and reloaded. Historical London is tested separately.

The town/interior generator ordering issue was corrected and regeneration
is byte-stable. In-game rail and garden images were inspected. Packaging
checks the previous v0.61 hash and preserves every user artifact save.

## v0.61 Paris promenade verification - 2026-09-19

53 focused PASS results on the updated build and its generated map data:
41 map/path checks, 3 capital compatibility checks, 3 dialogue/tree/
regeneration checks, 2 full-map Paris preservation/generation checks,
2 emulator walking/save checks and 2 Notre-Dame investigation/save checks.

The walking test visits both garden approaches, the garden loop and the
promenade toward the island. It reads the signs, saves and cold-loads the
new district, checks the loaded terrain and returns through the hub to the
countryside. The Notre-Dame test checks entry cancellation, clues, peaceful
resolution, one-time rewards, exit/re-entry and cold saves inside.
Every v0.60 Paris map cell retains its collision, elevation and land/water
type. Previous v0.60 ROM and user saves are hash-verified during packaging.

## v0.60 landmark, story and visual verification - 2026-09-19

109 focused PASS results across staged build-and-test passes. Each gameplay
stage was built and tested before moving on; the final Notre-Dame visual
correction was followed by another complete case test, the edge-case suite
and the revised story test.

- 41 map/path checks; 7 layout/terrain compatibility checks.
- 3 static checks for dialogue widths, complete tree silhouettes and
  deterministic interior/case generation.
- 8 case play-through/save results, including the final Notre-Dame recheck.
- 7 edge cases: both clue orders in each room, all three full reward pockets,
  and a real, catchable level-12 Gastly battle. Rewards do not repeat.
- 12 new-game country/starter results and 4 Celebi chapter checks.
- 10 story/travel results: deferred reports, Ada's ending, case synthesis,
  Southampton and London travel, journal state and modern rail bookings.
- 11 walking/save results: Paris, Berlin, London, Oranienburg and historical
  London. Berlin's new garden paths and entrance signs were exercised.
- 6 deliberately stale route-save tree caches refresh correctly on cold
  Continue, preserving the player position, team and existing progress.

In-game building, garden, interior and Ghost encounter screenshots were
inspected. Testing uses disposable test-output saves. The package keeps
v0.59, verifies its SHA256, and hashes user artifact saves before and after
copying the new ROM. Existing emulator save states are not upgrade fixtures.

## v0.59 historical London verification - 2026-09-19

52 focused checks passed on the final build:

- 2 landmark walking/save checks: complete loaded terrain, four signs,
  both bridges, cold Continue, historical map and Southampton/Celebi returns.
- 9 story checks: London travel/welcome/journal/booking (3), v0.48 adjacent
  save migration (1), Oxford prerequisite report (2), Southampton travel (3).
- 38 map checks, old terrain/layout compatibility (1), sign widths (1),
  deterministic generation and absence of modern London Eye tiles (1).

In-game palace and river-crossing screenshots were inspected. All original
walkable terrain/elevations and story characters are preserved. Historical
and modern London layouts remain separate. Final logs/screenshots are
archived with v0.59; packaging verifies the previous v0.58 ROM hash. User
saves are not used or changed.

## v0.58 historical Southampton verification - 2026-09-19

59 focused checks passed on the final build:

- 2 landmark walking/save checks: reception bypass, complete loaded terrain,
  four signs, wall-side lanes, pier, cold Continue, map and ferry/Celebi returns.
- 16 story checks: Southampton travel (3), luggage (3), care (3), Oxford
  report (2), London travel (3), v0.44/v0.48 adjacent-save migrations (2).
- 38 map checks, original harbor art/layout compatibility (1), sign widths
  (1), deterministic asset/map generation (1).

All original walkable terrain remains unchanged. Three formerly blocked
edge cells bypass both workers; the original northern exit stays closed.
In-game screenshots of Bargate, Tudor House, walls and quay were inspected.
Final build and test logs are archived with v0.58. Packaging verifies the
previous v0.57 ROM hash; user saves are not used or changed.

## v0.57 historical Le Havre verification - 2026-09-19

59 focused checks passed on the final build:

- 2 landmark walking/save checks: all loaded terrain, four signs, crossings,
  cold Continue in the new district, historical map and Rouen/Celebi returns.
- 16 story checks: Le Havre travel (3), dock task (2), care (3), direct port
  return (3), Southampton travel (3), old dockworker/ferry-clerk saves (2).
- 38 map checks, original harbor art/layout compatibility (1), sign widths
  (1), and deterministic asset/map generation (1).

Initial walking exposed the dockworker blocking the eastbound terminal
path. A two-cell boardwalk bypass resolved it; every old walkable position
and the blocked northern exit are preserved. In-game screenshots of both
landmarks and basin crossings were inspected. The final build and regression
logs are archived with v0.57. The v0.56 ROM hash is checked during packaging;
user saves are never touched by the tests or release script.

## v0.56 Amiens and Rouen verification - 2026-09-19

64 focused checks passed on the final build:

- 4 new walking/save checks: both districts, every loaded terrain cell,
  bridges, signs, preserved quests, cold Continue, Town Map and train/Celebi returns.
- 17 existing quest/travel checks: Amiens (3), bulletin (2), Rouen (3),
  route book (3), riverside (2), v0.35 book migration (1), Le Havre (3).
- 38 map checks, 2 original-terrain/layout checks, 2 dialogue-width checks
  and 1 deterministic-generation check.

The riverside migration test now boots its genuine v0.34 edge battery in
the archived ROM. Its previous setup incorrectly loaded a later cached-map
battery backwards into that ROM. The old-edge fixture and new-ROM migration
both pass. User saves were not used or changed.

Final logs and screenshots are archived with v0.56 in artifacts/releases.
The v0.55 ROM is retained and its SHA256 checked during packaging.

## v0.55 station and Beauvais verification - 2026-09-19

Each district was built and tested before the next. Final coverage is 61
focused checks:

- 4 station/Beauvais walking checks: migrated old batteries, full loaded terrain,
  signs, landmark approaches, Save/cold Continue, era maps and original exits.
- 3 station-post story, 4 evacuation, 2 garden reunion, 3 onward Amiens checks
  and 2 refuge walking/story checks, including real pending rail itineraries.
- 38 static map checks, 2 old-coordinate/layout-isolation checks, 2 sign-width
  checks and 1 byte-for-byte generation check.

A test battery was produced by normal walking/Save in the actual v0.54 ROM
at the expanded post coordinate (26,20), then loaded in this build. Its new
station layout and complete runtime terrain are verified. This addresses
v0.54's shared refuge/post layout, which had spread estate scenery to the post.
A permanent assertion now requires independent layouts for these maps.
All old on-foot coordinates retain elevation/behavior; the inaccessible moat
becomes forecourt. Beauvais keeps its original garden quest area and reception.
New artwork was inspected through actual mGBA screenshots. Logs/screenshots
are archived under artifacts/releases/v0.55-*. Previous ROM and player saves
are retained. This is focused regression, not the entire project test suite.

## v0.54 historical Chantilly verification - 2026-09-19

The expanded refuge/estate passes 55 focused checks:

- 2 new mGBA checks: old battery terrain, landmark/sign walking, preserved
  progress, district Save/cold Continue, historical map, Celebi round trip
  and completion of the original blanket quest.
- 5 original time-travel checks, 3 station-post checks and 4 evacuation checks,
  covering gates, No/B choices, unfinished visits, relocated characters and
  actual pending rail journeys.
- 38 static map checks, 2 old-position/hardware/reproducibility checks and
  1 dialogue-width check.

The 16x14 refuge expands east to 56x32. All formerly walkable coordinates
retain their elevation and terrain behavior. Cached refuge terrain clears on
load; story character flags remain controlled by the original map scripts.
Chateau/stables sprites are reused because these structures predate 1940.
The source history and reconstruction limits are in
 data/geography/HISTORICAL-CHANTILLY.md.
Screenshots were inspected in mGBA. Logs and screenshots are retained under
artifacts/releases/v0.54-*. The previous ROM and player saves are preserved.
This is focused regression coverage, not every project test.

## v0.53 coastal landmark verification - 2026-09-19

Dover and Calais were built and tested sequentially. The final combined ROM
passes 68 focused checks:

- 4 port walking/save checks: old batteries, full terrain comparison, landmark
  paths, signs, cold Continue, regional map return, ferry rounds and coach exits.
- 3 transport checks: badge gating, No/B, coach entry, ferry returns and an old
  genuine coastal rail booking resumed through Paris to Berlin.
- 13 walking/save checks across the six previously expanded modern towns.
- 3 historical London checks for gates, returns and saved rail detours.
- 38 static map checks, 2 port compatibility/hardware checks, 2 sign-width checks.
- 3 generation checks proving all eight modern landmark districts reproduce.

The first old Dover battery exposed the saved Island Harbor layout ID. Port
load now migrates that ID to the new individual layout before terrain loading,
while retaining every original terminal tile and player coordinate. Actual
mGBA screenshots were inspected for castle, cliff face, town hall and lighthouse.
The previous v0.52 ROM is retained; player battery saves are untouched.
Build/test logs and screenshots are archived under artifacts/releases/v0.53-*.
This is focused regression coverage, not a rerun of every project test.

## v0.52 regional landmark verification - 2026-09-19

Oxford, Chantilly and Oranienburg were implemented, built and tested in order.
The final combined ROM passes 67 focused checks:

- 6 regional walking/save checks: old batteries, all loaded terrain, landmarks,
  signs, bridges, cold Continue, map return, service approaches and trail links.
- 2 Oxford transport checks: old surfing battery/dismount and riverboat return.
- 7 capital district checks covering London, Paris and Berlin.
- 3 World Options checks including saved settings, registration and cycling.
- 3 historical London checks including old progress and onward/return travel.
- 38 static map checks, 3 old-coordinate/hardware checks and 3 text-width checks.
- 2 byte-for-byte generation checks covering all six landmark districts.

The pathfinder now excludes elevation-1 shoreline tiles even when their
behavior is normal; mGBA correctly blocks walking onto those water edges.
Regional sprite crops ignore alpha below 128 to prevent faint stray pixels
from shrinking visible architecture. Capital generation remains identical.
Build, test logs and screenshots are archived under artifacts/releases/v0.52-*.
This is a focused regression, not a rerun of the complete project suite.
Player saves are untouched; update with normal in-game Save and CONTINUE.

## Baseline

Upstream: `pret/pokefirered` commit
`c75f352304d529f6ba92d4f74b9cf8b5c3810788`.

The untouched FireRed build passed `make compare` with SHA-1
`41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`. Its ROM, symbols, and checksum are
preserved locally in `artifacts/baseline`. A full new game was also exercised
through the original introduction to the bedroom in mGBA.

## Verified gameplay

The modified ROM was exercised in the mGBA 0.10.5 core using actual emulated
button presses. Each gameplay stage was built and tested before proceeding.

- The custom European title boots and accepts Start or A into a new game.
  The rewritten Oak introduction and Eevee demonstration reach country selection.
- All nine regional starter choices lead to the correct city with exactly one
  level-8 partner. Tests decrypt the party species, check the saved choice,
  exercise No/B on every preview, and return from each list to country selection.
  B cannot bypass the initial country menu.
- Cyndaquil and Treecko evolve through the normal Rare Candy flow into Quilava
  and Grovyle, confirming that non-Kanto evolution is enabled.
- All twenty-four map files have valid event coordinates, reciprocal connections,
  door destinations, and reachable required paths.
- Every clinic can be entered/exited, heals the party, and handles a defeat
  without sending the player back to Kanto.
- Each countryside route connects back to its city, produces an encounter from
  its own roster, and allows the battle to finish.
- All thirty directed train journeys between six stations work. B, Exit, and selecting the current
  station leave the player in place with controls released. Arrival doors work,
  and travel preserves the original home country and party. Each journey now
  verifies every intermediate stop against an independent graph search.
- Normal Save -> fresh emulator -> Continue preserves the city, coordinates,
  home country, starter species, and party for all nine starter choices, all
  three standard starts, and a London-to-Berlin journey.
- The Bicycle can be used from Key Items and moves faster than walking.
- The European map opens from the Bag and from the registered SELECT shortcut
  at all six towns/cities. All twenty-four Europe maps retain the correct country indicator
  and return to the original position with controls released.
  Selection wraps, A shows rail information, and B/START return safely.
- Each city's landmark sign is reachable, and the southern paths can be walked
  in both directions. London's river blocks walking outside the crossing.
  Map boards grant a missing Town Map once and work on repeated visits.
- The Town Map and its registration survive Save -> fresh emulator -> Continue
  at all six stops; SELECT still opens the map after loading.
- A wild Pokemon can be caught through the normal battle Bag; it joins the party
  and play resumes on the countryside route.
- The three-city guide quest works in all six visit orders, using actual train
  journeys. Every city stamps once; only the third distinct stamp unlocks the
  single EXP. SHARE reward. Repeated conversations do not duplicate it.
- A full Items pocket leaves all stamps and the unclaimed reward intact.
  After a slot is freed, the guide awards the item exactly once.
- Partial and completed tours survive Save -> fresh emulator -> Continue.
  Speaking to the guide after reloading preserves progress and reward quantity.
- All three local trainers accept No/B without battling, use their intended
  two-Pokemon teams, award prize money on victory, and remember defeat.
  Repeated conversations do not restart battles or pay again. Losing heals the
  player at the correct clinic without awarding victory.
- A single team completes all three trainer challenges through normal train
  travel and clinic healing, with the progress report reaching 3/3.
- Every station supply shop supports cancellation, buys two Poke Balls for 400
  and one Potion for 300, and rejects purchases with zero funds. Inventory,
  money, control release, and the station exit are checked.
- All three individual trainer victories, combined 3/3 completion, and purchases
  in all six stations survive Save -> fresh emulator -> Continue. Talking to
  a defeated trainer after loading does not award another prize.

## London–Oxford extension

- The continuous London -> English Meadow -> Oxford Trail -> Oxford journey
  works in both directions on foot and by Bicycle, without forced encounters
  on the middle path. Oxford Trail is 40 tiles long, beyond the existing meadow.
  Both direction signs open and release controls; screenshots of the trail,
  Oxford, the rail menu, and the updated travel map were visually inspected.
- Oxford's clinic heals normally; its station doors and supply shop work.
  Its guide leaves the three-city stamp quest unchanged. The map board grants
  a missing Town Map once, and Oxford is selectable from every station.
- Oxford Trail produces its intended wild roster. A normal battle finishes
  back on the trail, and the controlled defeat test returns to Oxford's clinic
  with a healed party after visiting Oxford.
- Saving and cold-loading preserve progress in Oxford, on its trail, inside
  its station, after shopping, and after trains to Oxford and onward to Paris.
- A preserved v0.5 London battery save loaded in the new build with its starter,
  home country, and registered map intact, then walked to Oxford. This is one
  migration case, not a general compatibility guarantee for all earlier saves.

The walking extension was built and passed its tests before Oxford was added
to the train menu and travel-map selector. The final build reruns the existing
integration suite with four-city navigation, shops, and rail coverage.
The v0.6 integration run passed, including all twelve directed rail journeys
and 32 Save -> cold boot -> Continue cases.

## Paris–Chantilly extension

The Paris–Chantilly extension follows the same two-stage process: build and
verify the walking/cycling journey first, then add rail and map access.
`test_chantilly.py` exercises both directions through the French Gardens and
the 40-tile forest, town dialogue, clinic healing, station doors, direction
signs, encounters, battle completion, and defeat recovery at Chantilly.
The shared city checks include its shop, map board, and registered Town Map
in all four new maps. Save cases include the town, forest, station, shopping,
registered map, and journeys Paris -> Chantilly and Chantilly -> Berlin.

A preserved v0.6 Paris battery save also loaded and walked to Chantilly while
preserving Chikorita, home-country choice, and Town Map registration. Like the
earlier v0.5 case, this checks one known test save rather than every possible
old save or emulator configuration.

Screenshots of the new garden walk, forest signs, rail menu, and travel map
were visually inspected. Chantilly's map screen correctly identifies France.
The v0.7 integration run passed, including twenty directed rail journeys and
39 Save -> cold boot -> Continue cases. The release ROM matches the tested build.

## Berlin–Oranienburg extension

The Berlin–Oranienburg extension was built and tested before adding the sixth
rail destination. `test_oranienburg.py` verifies both directions on foot and
by Bicycle, park pond collision, clinic healing, station doors, unchanged stamp
progress, both trail signs, local encounters, battle completion, and defeat
recovery. Shared city checks cover its shop, map board, and Town Map access
from all four new maps. Save cases include town, trail, station, shopping,
registered map, and trains Berlin -> Oranienburg and Oranienburg -> London.

A preserved v0.7 Berlin battery save loaded in v0.8 and reached Oranienburg
with Treecko, the original home country, and map registration preserved. This
is one known migration case, not a general guarantee for all earlier saves.

The pond, park sign, and updated travel map were visually inspected. The
six-stop map keeps Oranienburg's country indicator set to Germany.
The seven-entry rail menu (six destinations plus Exit) was also inspected;
the greeting closes before it opens so the windows do not overlap.
The v0.8 integration run passed all thirty directed rail journeys and 46
Save -> cold boot -> Continue cases. The release ROM matches the tested build.

## Saved multi-stop rail journeys

The v0.9 railway uses the London–Paris–Berlin main line and branches to Oxford,
Chantilly, and Oranienburg. `test_rail_journeys.py` verifies No/B preview decline,
the four-train Oxford–Oranienburg journey, retaining or explicitly canceling a
booking, booking another destination, station exits, walking to the destination,
and recalculating the next connection after walking to a different station.
Malformed saved destination values 7 and 65535 are cleared safely.

`rail_test_helpers.py` derives expected paths from an independent adjacency
graph, then checks actual station arrivals, booking state, and the displayed
number of trains remaining. The train regression visits all thirty ordered
origin/destination pairs. Saved bookings use the previously unused variable
`0x40F7`; no save layout change is required.

Save tests include paused trips in London, Paris, and Berlin stations and
outside Berlin's station. After a cold restart they resume the booked journey
to completion. All existing save cases also check that booking state survives.
A preserved v0.8 Berlin battery save completed the new four-train journey from
Oranienburg to Oxford with its starter and home-country choice intact.

The destination/next-stop page and remaining-trains confirmation were inspected
visually. The final boarding flow avoids repeating the next-stop message.
The v0.9 integration run passed all thirty origin/destination routes and 50
Save -> cold boot -> Continue cases, including finishing each paused itinerary
after loading. The release ROM matches the tested build.

## Test details and limits

`scripts/run-tests.py` runs the checks in dependency order. The emulator never
opens a player's normal save file. Temporary states, isolated battery saves,
and screenshots are written under ignored `test-output`.

Healing and defeat tests deliberately set the test party's HP low in emulator
memory; the nurse and defeat recovery then run through the real game logic.
These fixtures are not modifications to the ROM. Capture uses normal catch
rates and retries when the Pokemon breaks free.

Map-board tests remove the Town Map from the test inventory to exercise the
gift path for continuing players; they do not claim a full old-release save
migration test. Outdoor path checks include tile behavior so water is not
mistaken for walkable ground. City screenshots were also visually inspected.

Trainer-loss tests use the same low-HP fixture as wild-battle recovery. Trainer
victories use the actual starter and ordinary attack inputs. Shop tests set
the test save's money to zero only for the insufficient-funds case.

Trainer team validation decrypts the actual enemy party slots: this engine's
trainer setup does not populate `gEnemyPartyCount`. The first test used that
unused count and was corrected. The initial French team proved too strong for
the basic fresh-starter test, so Ralts was replaced with a level-5 Oddish.
Trainer IDs 743-745 use existing reserved defeat flags; save layout is unchanged.

The Bag-capacity test fills the emulated Items pocket with Potion stacks, then
clears one slot. This isolates the reward's full-pocket and retry branches.
`test_tour.py` also checks the decrypted inventory quantity and persistent
stamp variables. The tour uses four previously unused saved variables
(`0x40F2` through `0x40F5`); home country remains at `0x40F0`.

The confirmed starter species is stored at `0x40F6`. Evolution tests insert one
Rare Candy and set the test party's cached level just below the evolution
threshold. The game's actual item handler updates experience and stats and
runs evolution. This fixture does not change normal starter levels or inventory.

Tests assert memory state as well as inspecting screenshots. A test-runner bug
initially checked the OAM flag instead of the battle flag; that was corrected
and all three country battle/recovery tests were rerun successfully.

These checks cover the first playable slice, not the entire inherited FireRed
game. Multiplayer, USA transfer, the original Kanto campaign, long-term save
compatibility, and future story features are not validated. The new map is a
schematic overview of the three implemented countries.
The normal desktop mGBA frontend has not been manually played in this session;
the gameplay checks use its emulation core headlessly.

## Earlier fixes and build verification

The v0.5 build uses a persistent Ubuntu cache under `~/.cache` and a
Windows-created archive for its initial source copy. Both initial and cached
builds succeeded; the final cached rebuild produced the same SHA-256 as the
ROM used for the gameplay tests. All nine starter paths, city/navigation
checks, and the existing gameplay regression checks passed before packaging.

- Removed an extra wait after the country menu that stalled script execution.
- Restored the clinic's standard Union Room initialization, required by the
  shared nurse dialogue, to prevent a healing-time memory overwrite.
- Bounded the original Sevii region lookup so new map sections cannot cause
  out-of-bounds reads when the original region map is requested.
- Corrected NPC IDs and starter-gift commands caught by the assembler.

The release ROM's SHA-256 is recorded beside it in `artifacts/SHA256SUMS.txt`.

## v0.10 regional challenge coverage

`test_challenges.py` walks from each existing trainer victory through a normal
clinic heal to the new trail trainer. It checks both decline inputs, exact
opponent species, wins and prize money, repeat conversations, and blackout
recovery. The starter-only playthrough uses the supplied Potions through the
normal battle Bag; it does not change player stats. Battle balance is checked
with the default Grass starter in each country, not every possible party.
Forced-loss cases deliberately reduce HP and battle stats.

`test_challenge_rewards.py` checks each regional guide's two-win requirement,
one Rare Candy, duplicate prevention, and full Items-pocket recovery. Missing
victory flags and full Bags are explicit fixtures; successful wins come from
the battle checks. `test_save.py` includes nine challenge cases: wins, claimed
rewards, and pending full-Bag rewards in each country. Reloaded pending rewards
remain claimable once after room is made; claimed rewards do not repeat.
All six trainer flags and the three reward variables are checked on reload.

An archived v0.9 Berlin battery save also loads with its partner, home country,
and registered map intact, then walks to Oranienburg and completes the rail
journey to Oxford. This verifies that particular migration case, not every
possible historical save. Trainer IDs 746–748 and variables 0x40F8–0x40FA use
reserved capacity without changing the save-block layout.

The v0.10 full integration suite passed, including all 59 cold Save/Continue
cases and all 30 directed train journeys. Release logs are preserved under
artifacts/releases/v0.10-tests.log and v0.10-legacy-save.log.

## v0.11 England story coverage

`test_england_story.py` checks mission acceptance and No/B declines for all
three home countries, directions before acceptance, both local trainer
prerequisites, and recognition of earlier real trail victories. The winning
playthrough carries the England challenge team through normal trains, clinic
healing, the Oxford rival battle, and the return report in London. It checks
the Pidgey/Eevee roster, prize money, battle declines, repeat conversations,
exactly one Soothe Bell, and full-Bag recovery. Missing prerequisite branches
use a trainer-flag fixture; forced-loss coverage reduces HP and battle stats.
The rival battle is balanced/tested with the trained Bulbasaur party and
normal Potion use, not every possible party or starter.

Five story save cases cover accepted mission, rival victory, report ready,
completed report, and pending full-Bag reward. Reloaded pending reports remain
claimable exactly once. The new trainer flag and variable 0x40FB use existing
reserved capacity, without resizing save blocks. A preserved v0.10 Oxford
battery save also keeps its partner, regional wins and reward, accepts the
new story, and unlocks the rival using those earlier wins. This migration
check covers that save, not every historical save state.

The v0.11 full integration suite passed, including all 64 cold Save/Continue
cases and all 30 directed train journeys. Release logs are preserved under
artifacts/releases/v0.11-tests.log and v0.11-legacy-save.log.

## v0.12 Oxford Gym coverage

`test_oxford_gym.py` exercises entrance/exit, advice, story prerequisites,
No/B declines, and a real leader victory using the completed story party.
The player uses Grass moves/Leech Seed and supplied Potions through normal
battle menus; no player stats are increased. The badge is checked immediately
after victory, along with TM39 and the automatically granted TM Case. Repeat
conversations cannot repeat money or the TM. Saturated-TM and full-Key-Items
fixtures check that the badge is retained and the TM remains claimable. Save
pointers are reacquired after battle before changing those fixtures.
Forced-loss coverage reduces HP and battle stats, checks clinic recovery,
and returns to the leader to verify the challenge remains available.

`test_gym_ui.py` opens the actual Trainer Card before and after the win,
checks that only the first badge appears, opens the TM Case, and opens the
European map inside the Gym (Oxford, not an inferred map-number grouping).
Four additional cold-save cases cover Gym entry, completion, and both kinds
of pending TM. They verify badge, leader defeat, TM quantity, reward variable,
and retry after making room. Battle balance is tested with the trained
Bulbasaur story party, not every possible starter/team.

The Gym is appended as Europe map 24, preserving previous map numbers.
Trainer 750, existing badge flag 0x820, and reserved variable 0x40FC preserve
the save layout. An existing v0.11 completed-story battery save can travel to
Oxford and challenge Ellis. Existing Gym tiles/art and first-badge engine
behavior are intentionally reused for this prototype.

The v0.12 full integration suite passed, including all 68 cold Save/Continue
cases and all 30 directed train journeys. Release logs are preserved under
artifacts/releases/v0.12-tests.log and v0.12-legacy-save.log.

## v0.13 French survey coverage

`test_france_story.py` verifies first-badge gating, No/B declines, and neutral
marker visits before the quest starts. It walks to both study sites in both
orders, checks that repeat visits cannot substitute for the other site,
requires both observations before Remy's review, and requires that review
before the Paris reward. Return visits to every participant and marker after
completion leave progress and the single Miracle Seed intact. A full Items
pocket is a capacity fixture; clearing one slot permits exactly one claim.
The normal winning Gym save supplies the first badge in the full suite.

Seven cold-save checkpoints cover accepted survey, each individual site,
both sites, reviewed report, completion, and a pending full-Bag reward.
Reopening each individual marker preserves its recorded state; Remy can
review reloaded notes, and Celine can reward a reloaded report once.

Reserved variable 0x40FD stores the survey state (0 unstarted, 1 accepted,
2 gardens only, 3 forest only, 4 both notes, 5 reviewed, 6 rewarded). No map
numbers or save-block sizes change. A preserved v0.12 completed-Gym battery
save also loads with its badge, TM and England story intact, and completes
the new survey in the focused migration playthrough.

The French wild-encounter check enters the grass below the new study marker.
Its previous scripted approach walked directly into the sign. After updating
that test route, encounter and blackout checks were rerun successfully; the
remaining regression checks continued on the unchanged ROM.

The v0.13 complete regression set passed, including all 75 cold Save/Continue
cases and all 30 directed train journeys. Consolidated results are preserved
in artifacts/releases/v0.13-tests.log; migration and focused survey results
are in v0.13-legacy-survey-tests.log.


## Chantilly Gym checks (v0.14)

The focused emulator playthrough imports a preserved v0.13 completed-survey
battery save, heals normally, walks the pool bridges, and defeats Marine using
the existing trained Bulbasaur and ordinary battle inputs. No stats are raised
for that victory. It checks Psyduck and Horsea, immediate Cascadebadge credit,
TM03, retained first badge/TM39, declines, and no repeated battle payout or TM.
The Trainer Card displays exactly two badges, the Town Map identifies Chantilly,
and the TM Case visibly lists Water Pulse alongside Rock Tomb.

Explicit fixtures cover all six unfinished survey states, a saturated TM03
stack, a missing TM Case with a full Key Items pocket, and a forced loss with
reduced player HP/defenses. These exercise locked challenges, pending rewards,
clinic recovery, and retry; they are not claims of unmodified difficulty runs.
Balance is verified with one trained starter, not every possible team.

Variable 0x40FE tracks the one-time TM03 reward. Trainer 751 stores Marine's
victory; map 25 is appended to the Europe group. Existing map numbers and save
block sizes remain unchanged. Four additional cold-save cases cover entering
the Gym, completion, and each pending reward condition. All save cases also
compare the second badge, TM03, its reward flag, and the new trainer flag.

The complete v0.14 regression suite passed on ROM SHA256
4327773638209b907d7b14654f46138c84c8ea5440660899069cf8733944b390,
including 79 cold Save/Continue cases and 30 directed train journeys.
Results are preserved in artifacts/releases/v0.14-tests.log, with the
v0.13 battery migration and focused Gym checks in v0.14-legacy-gym-tests.log.


## German courier chapter (v0.15)

A preserved v0.14 completed-Chantilly-Gym battery save loads with both badges,
claimed Water Pulse, and an unstarted courier mission. The focused check uses
normal buttons to leave the pool Gym, take trains to Berlin and Oranienburg,
accept and deliver the parcel, return the report, and receive one Magnet.
It tests No/B, Karl before acceptance, Lena before delivery, repeated visits
to both NPCs, and a full Items pocket followed by reward recovery.

Fixtures independently clear each required badge to check both prerequisites,
and fill the Items pocket to test deferred rewards. They do not award badges
or bypass travel in the normal completion playthrough. Walking routes retain
their existing integration checks; the courier completion uses trains.

Variable 0x40FF tracks 0 unstarted, 1 carrying parts, 2 carrying the report,
and 3 rewarded. No map IDs, trainer IDs, or save-block sizes change. Five new
cold-save checkpoints cover accepted, delivered, report-ready, completed, and
pending-reward progress. Every save case also compares this variable and its
Magnet count. Parcel and report are mission states, not inventory objects.


The v0.15 regression set passed on ROM SHA256
31cfd3f0a6a742248afa908c9fcfc7cb09c12758389552262ea80bcf8e334836,
including all 84 cold Save/Continue cases and all 30 directed train journeys.
The old 300-second runner limit interrupted the save suite after 83 passing
cases. The last pending-Magnet case and remaining bicycle/capture checks were
run separately on the unchanged ROM and passed. Future full save runs allow
420 seconds; --case can select an individual checkpoint for diagnosis.
Consolidated results are in artifacts/releases/v0.15-tests.log; the original
timeout and resumed output are also preserved alongside it. The focused
v0.14 battery migration results are in v0.15-legacy-courier-tests.log.


## Oranienburg Gym (v0.16)

The focused test loads a preserved v0.15 completed-courier battery save, travels
to Oranienburg, heals through the clinic, and challenges Conrad using ordinary
battle inputs and the existing level-14 trained starter. The test buys five
Potions with earned money at the station before the fight. An initial
unprepared run had no Potions left and lost; the prepared run wins without
raising stats. The driver explicitly selects Potion regardless of Bag cursor
position. Difficulty is checked with this team, not every starter. It checks the actual Voltorb
and Pikachu team, immediate third-badge credit, one Shock Wave TM, repeat-safe
payouts, and the Trainer Card, Town Map, and TM Case screens.

Fixtures cover all three incomplete delivery states, a saturated TM34 stack,
a missing TM Case with a full Key Items pocket, and forced loss through
reduced HP/defenses. These exercise gating, deferred rewards, and recovery;
they are separate from the ordinary victory playthrough. The decline test
waits for the Yes/No menu's input delay before sending its choice.

Unused variable 0x40EF records the TM claim. Repository search found no prior
use outside its definition. Trainer 752 and appended Europe map 26 leave
older map IDs and save-block sizes unchanged. Four additional cold-save cases
cover entry, completion, and both pending reward conditions. All save cases
compare the third badge, TM34, claim variable, and Conrad's victory flag.
The expanded 88-case save suite has a 450-second timeout.

The complete v0.16 regression suite passed without a timeout, including all
88 cold Save/Continue cases and all 30 directed train journeys. The tested ROM
SHA256 is 7a04dd3841aa04f18dea9f476656ce4e4036eb8b1162703d47d689660fcb6719.
Full results are in artifacts/releases/v0.16-tests.log; the preserved v0.15
battery migration and focused Gym tests are in v0.16-legacy-gym-tests.log.


## London�Oxford riverboats (v0.17)

A preserved v0.16 third-badge battery save loads on the boat build. Real-button
checks travel to both captains, read signs, reject boarding with No/B, and
complete free crossings in both directions. A fixture clears the third badge
at each landing to check locked service. The tests compare money, home country,
party species, courier progress, Magnet count, and rail booking across travel.
The Town Map identifies the destination correctly. Boarding while mounted on
the Bicycle returns to controllable outdoor movement; the movement check holds
the direction long enough for movement rather than using a two-frame tap.

A real Oxford-to-Berlin booking is made, then the player takes its first train
to London and detours back to Oxford by boat. The itinerary survives and the
Oxford clerk recalculates the remaining route and completes it to Berlin.
Four cold-save cases cover both landings, a mounted arrival, and a boat detour
with a pending rail journey; after reload they cross again or finish the booking.

No new map IDs, saved variables, or save structures are required. The new
captains use the existing third-badge flag. Static map checks verify that both
captains and their signs remain reachable. Visual inspection covers both
riverbank landings. Crossings use the normal warp transition, not boat animation.
The 92-case save suite has a 480-second timeout.

The complete v0.17 regression suite passed, including 92 cold Save/Continue
cases and all 30 directed train journeys. Both riverboat directions and a
rail detour work before and after reloading. Tested ROM SHA256:
c090b93deb70884fdf70e7bebf342b010137a67b86025181412e859172b25a81.
Results are preserved in artifacts/releases/v0.17-tests.log, with v0.16
battery migration and focused crossings in v0.17-legacy-ferry-tests.log.


## Rental Lapras riding (v0.18)

A preserved v0.17 battery save with the third badge loads on the riding build.
Focused tests reach both instructors through normal travel, check the badge
gate with a cleared-flag fixture, decline with No/B, and mount with normal
buttons. They compare the complete party byte-for-byte, money, home country,
and rail booking before/after rental. The player steers both ways on water,
dismounts onto clear ground, and repeats the rental. Bicycle-to-water-to-foot
transitions are also exercised. Surfing is faster than walking, so the test
releases direction input after each tile rather than assuming walking speed.

A real saved rail booking survives a rental and shoreline exit, then completes
to Berlin through the normal clerk. Four cold-save cases cover both water
locations, the bank after dismounting, and riding with a pending rail itinerary.
Reloaded riders retain Surf state, can dismount, and can complete the booking.
The existing ferry tests run alongside these checks.

No new saved variables, flags, map IDs, or party changes are introduced.
Arrival on the existing surfable tile initializes the engine's normal Surf
state; entering clear ground uses its existing dismount behavior. These are
short town-water rides, not a custom mount system or a long water route.
Visual inspection verifies the generic rider rendering. The 96-case save
suite has a 510-second timeout.

The complete v0.18 regression suite passed, including 96 cold Save/Continue
cases and all 30 directed train journeys. Reloaded riders retain Surf state,
dismount normally, and complete a pending rail trip. Tested ROM SHA256:
294bf8b83731f3231d003d3498fd2b837e2d78eb9dca5dffed58a031f9808066.
Results are in artifacts/releases/v0.18-tests.log, with the v0.17 battery
migration and focused rentals in v0.18-legacy-riding-tests.log.


## Coastal ferry destinations (v0.19)

A preserved v0.18 third-badge battery save loads on the coastal build.
Real-button tests take each station coach, decline with No/B, cross from both
ports and back, and use each north return exit. Cleared-badge fixtures check
both coaches and both captains. Travel compares the complete party bytes,
money, home country, and rail booking. Port Town Maps show the correct country,
selected destination, and ferry/coach information. Screenshots verify the
reused harbor artwork and both added travel-map nodes.

A real Oxford-to-Berlin booking survives a riverboat detour, London coach,
and Dover-to-Calais ferry. The return coach reaches Paris, whose normal rail
clerk finishes the saved journey to Berlin. Four cold-save cases cover Dover,
Calais, a return-city arrival, and Calais with the pending itinerary. Reloaded
port saves complete round trips and exits, or resume the booked train journey.

Europe map IDs 27 and 28 and region-map sections are appended. Existing IDs,
save layouts, and six-stop rail tables remain unchanged. The travel map now
has eight browsable destinations; navigation checks verify wraparound in both
directions. Ports have existing harbor layout/artwork, no encounters, and use
London/Paris clinic respawns. No new saved quest state is needed. The expanded
100-case save suite has a 540-second timeout.

The complete v0.19 regression suite passed, including 100 cold Save/Continue
cases, eight-destination map navigation, and all 30 directed rail journeys.
Reloaded port saves complete crossings, return coaches, and the Berlin rail
detour. Tested ROM SHA256:
eb9f366af7aa4ed18ca084e7a97bf31312f98c5cead5f43697159ffed06077c9.
Results are preserved in artifacts/releases/v0.19-tests.log; v0.18 battery
migration and focused crossings are in v0.19-legacy-coastal-tests.log.


## Tree edge correction (v0.19.1)

Replaced exposed interior forest metatiles with native canopy, side, and trunk
edges on all twelve European outdoor maps. Tile collision/elevation bits and
map coordinates are preserved. The initial map generator applies the same
edge finishing. Layout map.bin and border.bin files now explicitly invalidate
maps.o, so binary-only map edits rebuild the ROM correctly.

Six existing battery saves cold-booted successfully on the corrected ROM.
Real-button walks reached each town's southern and western forest boundaries;
emulator screenshots verified the finished edges. Static map/path checks,
all six city checks, and the Oxford, Chantilly, and Oranienburg route suites
passed, including walking/cycling both ways, clinics, stations, signs, local
encounters, and defeat respawns. This patch used focused regression checks;
the complete 100-case save suite was last run for v0.19.

Tested ROM SHA256: 8a59c7160d56a5a06c28593d349180152eb49ead67f3dbd57523f08a67bbe725.
Results: artifacts/releases/v0.19.1-tree-tests.log. Representative screenshots:
v0.19.1-london-trees.png and v0.19.1-chantilly-trees.png in the same directory.


## Celebi prologue (v0.20)

Ada in Oxford offers a Thunderbadge-gated investigation. Celebi beside the
Chantilly Forest path offers an optional dialogue vision, followed by a return
report and one Rare Candy. VAR_EUROPE_CELEBI_STORY aliases reserved 0x40EE;
no save structures or map IDs change. The sighting is not a battle, capture,
or time-travel warp. Historical maps and the larger WWII arc remain future work.

Real-button checks cover the badge gate, premature forest visit, No/B at both
prompts, acceptance, repeated directions, the picture opening/closing, recorded
sighting, return report, repeated visits, and full-Bag reward recovery. Existing
starter and third-Gym battery saves are cold-loaded on the new build. Party
bytes, money, home country, regional quests, and rail-booking value are compared
through the chapter. Six new normal Save/Continue checkpoints cover acceptance,
arrival at Celebi, the sighting, return report, completion, and a pending reward;
reloaded players can continue their quests or collect exactly one reward.

Adjacent regression checks cover all six town landmarks/map boards, the Oxford
and Chantilly walking/cycling routes, clinics, stations, signs, encounters and
respawns, both French survey orders, and booked rail transfers/cancellation/
detours. Tree-edge screenshots are retained during battery migration. These
checks passed before a final dialogue-width adjustment; chapter/save/map and
portrait checks were repeated on the final ROM. The complete suite was not
rerun for this release. Its runner now includes the prologue and 106 save cases
with a 570-second save-test timeout.

Final ROM SHA256: eb420253a145b60dd020fde209f0ab0fe1b022192495cb4d192f3249692b206c.
Release logs: v0.20-celebi-tests.log and v0.20-adjacent-regression.log in
artifacts/releases. Portrait and forest screenshots accompany the release.


## First historical visit (v0.21)

Celebi now transports players with a completed prologue to a fictional
Chantilly station-refuge courtyard in 1940. The fixed Celebi return NPC is
available before, during and after the blanket task. The historical map is
appended at Europe map ID 29, with a new layout and region section; existing
map IDs stay unchanged. Reserved variable 0x40ED tracks arrival, Elise's request,
the keeper's blanket and completion, separately from prologue variable 0x40EE
and all regional quests. No save structure changes are needed.

Real-button mGBA checks cover the unreviewed-report gate, No/B in both eras,
immediate round trips, returning midway and resuming, the sign, quest order,
repeat NPC conversations, and a one-way blanket handoff without Bag items.
Party bytes, decoded contents of every Bag pocket, money, all badge flags,
home country, rail booking and present quest variables remain intact through
crossings and the historical task. Raw encrypted inventory bytes can change
when the engine relocates save blocks, so tests compare decoded quantities.
Cycling becomes walking on arrival. A real Chantilly-to-Oxford rail itinerary
survives a walking/time-travel detour from Paris, then completes at its clerk.

Seven normal Save -> cold boot -> Continue cases cover departure readiness,
arrival, Elise's request, carrying the blanket, returning midway, completion,
and a booked train detour. Reloaded players finish the task and return, or
resume the train itinerary. The existing prologue tests and its six cold-save
cases also passed. All 30 Europe maps passed static bounds/link/path checks.
Six existing town battery saves loaded successfully; present-day map browsing,
registration, both exit keys, and town/route/station/clinic context passed.
The historical map UI labels France, 1940 and identifies its schematic as a
present-day reference with a Celebi return reminder. Visual checks cover the
courtyard, tree edges, Eevee portrait, blanket handoff and era-aware map.

This release used focused regression coverage, not a rerun of the entire
suite. The full runner includes test_time.py and now has 113 cold-save cases,
with a 630-second save-suite timeout. Existing artwork represents a compact
fictional refuge, not a reconstruction of a documented station. The wider
wartime story remains unfinished; this area has no battles or wild encounters.

Tested ROM SHA256: 698fe2b513d75b43748d9d79393a01201d22dac76acf11809273ec409decbaff.
Logs: artifacts/releases/v0.21-time-tests.log and v0.21-regression-tests.log.
Screenshots of the refuge, Eevee, handoff and map accompany the release.


## Historical station news (v0.22)

A guide at the 1940 refuge unlocks after the blanket task. The station post
is appended at Europe map ID 30 and reuses the existing courtyard layout.
Players read its notice, obtain dispatcher confirmation, and deliver the
message to the refuge keeper. Elise and present-day Ada acknowledge completion.
Reserved variable 0x40EC stores this task separately from 0x40ED (blanket) and
0x40EE (prologue); existing map IDs and save layouts remain unchanged. Both
historical areas retain a Celebi portal to the present-day forest. Re-entry
always arrives at the refuge and does not reset historical progress.

Real-button checks cover the blanket gate, No/B on both guides, attempted
early confirmation/report, repeated notice/dispatcher visits, leaving and
resuming across eras, delivered news, repeat completion, and Ada's dialogue.
Crossings preserve party bytes, decoded Bag contents, money, badges, home
country and present quests. A long walk can legitimately update friendship;
the Ada check compares party bytes immediately around her conversation and
other invariants across the journey. An actual saved Oxford rail itinerary
survives the station-post detour and completes afterward. That case uses a
setup fixture for completed blanket progress, not for the rail booking.

Six new normal Save/Continue cases cover acceptance, copied notice, confirmed
news, return to the present, delivered report and the pending train journey.
Reloaded players complete the task or train trip. The original refuge chapter
and its seven cold-save cases also pass on the final ROM. All 31 Europe maps
pass static checks. Visual inspection covers the post notice, refuge report
and the era-aware travel map. Six-town map navigation and legacy town battery
migration passed before the final refuge-only guide-spawn correction.

A v0.21 save inside the refuge originally retained its three-NPC template list.
Loading now restores the fourth stationary guide template, and a return-to-field
script spawns the guide immediately. scripts/test_departure_migration.py uses
the archived v0.21 ROM to create a battery save directly beside the future
guide; the final ROM loads it and can talk to him without a movement step.
This archived-ROM migration check is separate from the normal suite.

This release uses focused regressions, not a complete-suite rerun. The full
runner includes test_departure.py and 119 cold-save cases with a 690-second
save timeout. Historical train departure and larger wartime locations remain
unfinished; this milestone is a fictional information-gathering task.

Tested ROM SHA256: 224419f88cd34f6b0410b62524b756d0d4e5577da75586701b57e5d32476c390.
Release logs: v0.22-chapter-tests.log, v0.22-adjacent-regression.log, and
v0.22-legacy-migration.log in artifacts/releases. Notice, report and map
screenshots are stored alongside the release.


## Historical train and Beauvais reception (v0.23)

After the departure report, the station-post board offers a historical train
to Beauvais reception. Europe map ID 31 and its region section are appended;
the room reuses the rival-house interior. A host checks Elise and Eevee in,
and Celebi or the south return-service exit takes the player out. A return
warp is appended to the station post on an ordinary non-warp ground tile;
it serves as the reception exit's destination without auto-triggering travel.
Reserved 0x40E5 tracks not departed, arrived, and checked in. Existing variables,
map IDs and save structures are preserved.

Elise's refuge object uses a temporary hide flag, derived from saved arrival
progress on map transition/return to field. Her old location stays empty after
travel and after saving in the refuge. Reception keeps her available before
and after check-in; revisiting never resets progress. Ada acknowledges a
completed check-in. Town Map text identifies Beauvais, 1940 while retaining
the existing present-day diagram and Chantilly entry-point selection.

Real-button checks passed for the delivered-report gate, No/B, boarding,
arrival, host/Elise interactions in both stages, repeat conversations, the
south exit, repeat trips, direct Celebi return, Elise's relocation, Ada's
acknowledgement and an actual booked Oxford journey after the historical train.
The booking case uses a delivered-news setup fixture; the rail itinerary is
from the existing real-booking checkpoint. Transition and conversation checks
preserve party bytes, decoded Bag contents, money, badges and present quests;
long walking comparisons allow normal friendship changes. Leaving before
check-in, returning through the refuge and reboarding also completes normally.

Five new cold Save/Continue cases cover boarding readiness, arrival, completed
check-in, the old refuge after relocation and a pending present-day itinerary.
The six station-news cold-save cases and original refuge gameplay regression
also pass. All 32 Europe maps pass static link/bounds checks. Visual inspection
covers reception, welcome text, Eevee's portrait, the now-empty old location,
and the historical Town Map. Dialogue widths fit the standard text window.
The station-news notice helper now explicitly declines the boarding offer
when inspecting the board after completion.

This release used focused coverage, not a complete-suite rerun. The full
runner includes test_evac.py and 124 cold-save cases with a 720-second timeout.
The journey uses dialogue and a transition, not moving train artwork. The
interior is placeholder art; the wartime journey is fictional.

Tested ROM SHA256: 904dacff26d9c330979d3d1cb1393e1c357d3514b040ec223da875e30156cd58.
Logs: v0.23-train-tests.log, v0.23-regression-tests.log and
v0.23-unfinished-visit.log in artifacts/releases. Reception, portrait,
relocation and map screenshots accompany the release.

## v0.24 - A message home and Ada's first account

Elise offers an optional message after Beauvais check-in. The refuge keeper
replies, Elise acknowledges the reply, and Ada in Oxford records the account
and awards one Luxury Ball. VAR_0x40E4 tracks five saved stages without changing
the save layout. Completed visits retain appropriate dialogue and progress.

Focused real-button emulator checks passed for the check-in gate, No/B,
acceptance, delivery, reply, era detours, no early archive reward, repeat visits,
and a one-time reward. A full Poke Balls pocket leaves the reward pending;
freeing a slot grants exactly one ball. Party, money and earlier quest progress
remain intact across the checked conversations.

Six message Save -> cold boot -> Continue cases passed: active, delivered,
acknowledged, report-ready, complete, and full-pocket pending. Five train save
cases also passed: ready, arrival, complete, returned, and pending rail booking.
The train gameplay regression passed, including leaving before check-in,
returning later, Elise's relocation and preserving an actual Oxford itinerary.
Existing battery saves load through Continue. The Elise train helper declines
the optional message offer to keep the earlier quest checks independent.

Visual inspection passed for the offer, Ada's account, archived acknowledgement
and full-pocket dialogue. New text widths fit the standard dialogue window.
This release used focused coverage, not a complete-suite rerun. The full runner
now includes test_message.py and 130 cold-save cases with a 780-second timeout.

Tested ROM SHA256: 95934c5602043840e5505abd2a11a1b20f2eebec14676e6e60f31dd2ea89ad8a.
Logs: v0.24-message-tests.log and v0.24-regression-tests.log in artifacts/releases.
Dialogue screenshots accompany the release. The wider wartime story remains
in development.

## v0.25 - Beauvais relief supplies and repeatable rest

After Ada records the first account (message stage 4), the Beauvais host offers
an optional care-parcel request. The station dispatcher supplies it and the
host accepts delivery. VAR_0x40E3 stores 0 none, 1 requested, 2 parcel and
3 rest unlocked; no save format or map ordering changes. Ada points players
to the host after recording the account. The parcel occupies no Bag slot.

Real-button checks passed for the archive gate, No/B at acceptance, reminders,
collection, repeated dispatcher visits, delivery, a detour through Celebi,
and repeat visits after completion. Full Items-pocket fixture checks confirm
collection/delivery neither need space nor alter Bag contents. Rest is a
separate Yes/No interaction after delivery; declining with No/B preserves
health. Accepting restores HP, status and PP without charging money or changing
items, Pokemon identity, or earlier quest progress. Repeated rest works.
A damaged/burned/zero-PP fixture and a six-member fixture with one fainted slot
verify healing through the actual host interaction; fixture Pokemon are cloned
only inside the test emulator, never in player saves.

Six new normal Save -> cold boot -> Continue cases passed: ready, active,
parcel, returned to present, complete and tired party. Each can resume and use
the rest service. Earlier historical train and message gameplay regressions
passed, including relocation, unfinished check-in, real pending Oxford rail
travel, message refusal, one-time reward, full Poke Balls pocket and retry.
Three earlier cold-save cases passed: evac-complete, message-pending and
message-complete. Legacy mode loads existing battery saves through Continue.

New dialogue was measured with normal, male and female font tables; maximum
width 212 pixels within the 216-pixel limit. Visual inspection passed for the
parcel offer, rest offer and healed acknowledgement. This is a dialogue-based
care corner using the existing reception interior, without new room artwork.
The wider historical storyline remains in development.

This release used focused coverage, not a complete-suite rerun. The full
runner includes test_relief.py and 136 cold-save cases with an 840-second limit.
Tested ROM SHA256: 4c783910045076b0cd8b09c396fdce5a819330e97533dfe4b0a187ec47346afe.
Logs: v0.25-relief-tests.log, v0.25-save-tests.log and v0.25-regression-tests.log
in artifacts/releases. Supply and rest dialogue screenshots accompany them.

## v0.26 - Beauvais garden and Luc's Pidgey

After the supply parcel is delivered, Elise offers a garden visit. The new
24x20 map is appended as Europe map 32, retaining all earlier map identities.
It reuses existing General/Pallet tiles and sprites, with complete forest
edges, flower beds, a return guide and a Celebi anchor. The historical Town
Map recognizes the garden as Beauvais, 1940. Earlier exits are unchanged.

VAR_0x40E2 saves four reunion stages: none, learned whistle, Pidgey found and
reunited. The bird is shy before Luc's request; after pickup it disappears
from the trees, then appears beside Luc on reunion. Derived temporary flags
restore its proper location on transitions and return to field. This is a
scripted story companion, not an addition to the battle party or Bag.

Real-button checks passed for the relief prerequisite, No/B on entry, exit
and Luc's request, initial shy bird, hints, pickup and reunion. Both exits,
reception healing during the search, a present-day detour, repeat visits and
both bird locations passed. Conversation/transition checks preserve party,
money, Bag contents, badges and earlier quests; normal walking can change
friendship. Legacy mode boots existing battery saves through Continue.

Six garden normal Save -> cold boot -> Continue cases passed: ready, active,
found, reception, returned to present and complete. Each resumes the reunion
and verifies the bird's location. Earlier supply/healing and message gameplay
regressions passed, including full Bags, six-party healing and pending rewards.
Three earlier cold-save cases passed: relief-complete, relief-tired and
message-complete. All 33 Europe maps pass static link/bounds/path checks.

Visual inspection passed for the entrance/tree edges, northeast search area,
reunion dialogue and historical Town Map. New dialogue measures at most 204
pixels with all three standard Latin font-width tables, within 216 pixels.
The first test route was corrected to walk around Celebi's occupied tile.
This release used focused coverage, not a complete-suite rerun. The full runner
includes test_garden.py and 142 cold-save cases with a 900-second timeout.

Tested ROM SHA256: 305fef8bbddc293a02a891c80821273bd6ee794e2654e1993e432002ab0e44a3.
Logs: v0.26-garden-tests.log, v0.26-save-tests.log and v0.26-regression-tests.log
in artifacts/releases. Garden/reunion/map screenshots accompany the release.
The wider wartime story and further historical locations remain planned.

## v0.27 - Town Map story journal

SELECT on the European Town Map opens a Celebi journey journal. A switches
between the current lead and seven milestone records; SELECT returns to the
map and retains the selected destination. B/START closes either view through
the existing caller. Reopening starts on the map. The journal reads existing
quest variables and the Thunderbadge; it writes no new persistent state.

Twenty-five current leads cover the badge prerequisite, Ada and the vision,
refuge blanket, departure news, reception check-in, message/reply/account,
care parcel, garden search and reunion. Pending reward leads identify the
required Bag pocket. Milestones require the corresponding completed stage,
so a reward still awaiting Bag space is not shown as complete.

Real-button checks passed against 27 existing battery saves loaded through
Continue, covering every lead and both full-pocket pending rewards. Checks
verify the expected lead and milestone mask, both journal pages, SELECT
round-trip, ignored directional input in the journal, retained map selection,
existing map browsing/travel help and return to the Bag. Party bytes, money,
Bag contents, badges, quest variables and location remain unchanged.
Registered-map checks pass for B/START, fresh reopening and field movement.
Two new normal Save -> cold boot -> Continue cases reconstruct the pending
account and completed garden journal correctly. The garden gameplay regression
also passes, including both exits, healing, era detour, bird relocation and
historical Town Map context.

Visual inspection covers early/late leads, the pending vision reward, partial
and completed milestones. All map/journal strings fit the 226-pixel content
width; the widest is 214 pixels in FONT_SMALL. This release used focused
coverage, not a complete-suite rerun. The full runner includes test_journal.py
and 144 cold-save cases with a 900-second timeout. No new story chapter or
regional Gym/stamp journal is added in this release.

Tested ROM SHA256: 876cf8731e2eae8c4b3d99f47490f002323be2a070e862d1c08c61a855fb4944.
Logs: v0.27-journal-tests.log, v0.27-save-tests.log and v0.27-regression-tests.log
in artifacts/releases. Journal screenshots accompany the release.

## v0.28 - Regional journal topic

Up/Down inside the journal switches between the Celebi journey and Europe
tour while retaining the lead/milestones page. A changes pages; SELECT returns
to the map without changing its destination selection. Reopening the journal
starts on the Celebi lead. Map directions remain normal destination browsing.
Shoulder keys retain the original Help function; an initial shoulder-button
prototype was replaced after the emulator exposed the Help conflict.

The regional topic adds 25 leads covering the England study, trail opponents,
rival, France's either-order survey, Germany's delivery, three Gyms and their
pending TMs, missing city stamps, pending EXP. SHARE and completion. Seven
independent records show stamps, claimed tour reward and badges. Pending TMs
do not erase earned badges. Gym/story leads take priority over optional stamps;
stamps may still be collected at any point. No new save variables are used.

Real-button journal tests passed on 28 existing battery checkpoints loaded
through Continue. Two targeted trainer-win fixtures cover the remaining
England prerequisite branches; five stamp-variable fixtures cover missing
stamps, pending reward and completion. Full Key Items fixtures replace one
Bicycle with a Town Map while retaining all occupied slots and no TM Case.
Normal Bag compaction is allowed in inventory comparisons; item quantities,
party bytes, money, badges, quest variables and location remain unchanged.
The stamp fixture refreshes the save-block pointer after returning from Bag.

Checks cover both topic directions, switching on both pages, correct saved
records, returning to map, default topic on reopening and START exit to Bag.
All 27 existing Celebi journal checkpoints and registered-map B/START/field
controls passed again. Two new Save -> cold boot -> Continue cases verify
regional pending-TM and completed-tour views. The completed-tour checkpoint
uses the documented stamp-variable fixture, not a newly played full tour.

Visual checks passed for regional introductions, survey reminders, pending
story/Gym/tour rewards and completed records. All map/journal strings fit
226 pixels in FONT_SMALL (maximum 214). This release used focused coverage,
not a complete-suite rerun. The full runner includes test_tour_journal.py and
146 cold-save cases with a 900-second timeout. No new story chapter is added.

Tested ROM SHA256: d751e5fb100928f9eaa84840b13b35811bf1ad0bd65275586b4c2d281ecd6af6.
Logs: v0.28-tour-journal-tests.log, v0.28-save-tests.log and
v0.28-journal-regression.log in artifacts/releases, with selected screenshots.

## v0.29 - Onward to Amiens and meeting-point briefing

After the garden reunion, the Chantilly post dispatcher offers a free onward
train to Amiens. The old noticeboard still boards Beauvais. Amiens is appended
as Europe map 33; its new courtyard layout reuses the garden tiles/tree borders
with a lighter central area, a noticeboard, Nora, return guide and Celebi.
VAR_0x40E1 tracks none, arrived, briefed, notice read and confirmed. No earlier
map IDs or save layout change. The guide returns to the post; Celebi returns
to the present forest. The service is fictional, not a historical timetable.

Nora asks the player to read the meeting instructions and confirm them with
her. Reading before the briefing cannot skip it. Repeat conversations and
travel preserve completion. The journal adds four leads after the onward
invitation and an eighth historical milestone. The map labels Amiens, 1940;
a named location selector replaces the former nested location expression.

Real-button checks passed for the reunion gate, boarding and return No/B,
early notice, briefing, confirmation, repeats, leaving before briefing and
returning later, and a mid-task Celebi detour. The old Beauvais train remains
usable after unlocking Amiens. A separate unlock fixture on a checkpoint with
an actual modern Oxford booking verifies Amiens travel, Celebi return and
completion of that booked journey. The fixture sets garden/relief completion;
it does not fabricate the modern booking. Dialogue/transition checks preserve
party, money, Bag, badges and prior progress; normal walking may alter friendship.

Six normal Save -> cold boot -> Continue cases passed: ready, arrival, briefed,
notice, returned and complete. Every case can finish Nora's objective. Garden
gameplay and all 27 earlier journal checkpoints pass again, including registered
map controls. All 34 Europe maps pass static link/bounds/path checks. The new
journal leads and final 255-bitmask milestone display pass real UI checks.

Visual inspection covers the arrival, Nora, noticeboard, Amiens map label,
current lead and eight completed records. Dialogue widths fit 216 pixels
(maximum 210); map/journal text fits 226 pixels (maximum 214). No new battle,
item reward or historical train animation is introduced. Further Amiens story
remains planned. This release used focused coverage, not a complete-suite
rerun. The full runner includes test_amiens.py and 152 cold-save cases with a
960-second timeout.

Tested ROM SHA256: d30a25016eb7a64e5f0bee62eb1070892082a994fa675563a900426031393676.
Logs: v0.29-amiens-tests.log, v0.29-save-tests.log, v0.29-regression-tests.log
and v0.29-map-tests.log in artifacts/releases, with selected screenshots.


## v0.30 - Amiens reunion (2026-09-18)

Focused verification on the final ROM; the entire integration suite was not
rerun. Real mGBA button input passed the arrival prerequisite, Nora's No/B
choices, both witness orders, repeat conversations, early verification
checks, reunion and Meowth relocation. Party, money, Bag, badges and modern
quest state remain unchanged by the conversations. Checks cover the return
service and a Celebi detour, with six new journal leads and milestone bit 8.

Seven normal Save -> fresh boot -> Continue checkpoints cover active, Mira,
porter, both reports, verified, present-day detour and completed states. Each
resumed to completion and checked Meowth at its new position. A separate
migration check creates a real battery save using archived v0.29 beside the
future Mira, then verifies immediate interaction on the new ROM.

The v0.29 arrival regression passed, including its No/B choices, early notice,
repeat visits, Beauvais service and a genuinely booked modern rail journey.
All 27 earlier historical journal cases passed, including registered-map
B/START exits and field movement. Static checks passed for all 34 custom
maps, including access to the new characters. Dialogue fits the 216-pixel
text area (maximum 215); journal text fits 226 pixels (maximum 214).

Visual inspection caught a bool8 truncation of the ninth milestone's DONE
marker. The mask now uses u16 and completion is converted to an explicit
boolean. The final rebuild, reunion checks and seven cold saves were rerun;
the nine-row completed checklist was visually verified. An earlier journal
run overlapped the rebuild and failed; the full 27-case final-ROM rerun passed.
The full runner now includes reunion checks and 159 cold-save checkpoints.


## v0.31 - Amiens party care (2026-09-18)

Focused final-ROM mGBA tests passed; the full integration suite was not rerun.
Nora does not heal before the reunion. After reunion, Yes restores HP, status
and PP, while No/B preserves the complete tired party. Repeat care, return
service, Celebi travel and a v0.30 completed-reunion battery save passed.
A targeted six-member fixture includes depleted PP, burns and a fainted slot;
all members heal with a full Items pocket. Non-health Pokemon identity,
items, money, badges and all historical/present quest variables are checked
around the healing interaction. These health and capacity fixtures are
explicit setup edits; travel, dialogue and care use actual button input.

Two normal Save -> cold boot -> Continue cases preserve tired/rested health
and allow care afterward. The full reunion regression passes both report
orders, prerequisites, repeated dialogue, relocation, returns and journal
milestones. The old reunion helper explicitly declines Nora's new care offer
so its unchanged-party assertion still checks only reunion interactions.
The full runner now includes the care test and 161 cold-save checkpoints.

Dialogue widths remain at most 215/216 pixels; map/journal text is at most
215/226 pixels. Screenshots of Nora's choice and completed journal guidance
were visually inspected. No map layout or save-variable allocation changed.


## v0.32 - Ada's Amiens account (2026-09-18)

Focused mGBA verification, not a complete integration-suite rerun. The new
account test uses older battery saves and actual travel from Amiens through
Celebi and the regional railway to Oxford. Ada does not offer the account
before the reunion. Afterward, No/B leaves it unrecorded, Yes records it,
and repeat reports preserve party, Bag, money and other story progress.
The player revisits Amiens, checks Meowth's relocation and uses Nora's care
service after recording the account. No artificial quest unlock is needed.

Pending and completed report checkpoints passed normal Save -> cold boot ->
Continue and subsequent Ada interaction. The journal checks lead 34 before
recording, lead 35 afterward, and the tenth milestone (mask 1023). Earlier
journal cases also exercise topic switches and registered-map B/START exits.
The full runner includes the new account scenario and 163 cold-save cases.

Visual review caught clipped glyphs at ten-pixel row spacing. Historical
records retain eleven-pixel spacing and move their action hint down to fit
ten rows; screenshots of the final checklist and account lead are readable.
All new dialogue fits 216 pixels (215 maximum); journal text fits 226 pixels
(214 maximum). An initial test process exited without diagnostic output;
the return-trip diagnostic and full final-build scenario both passed on rerun.


## v0.33 - Checked Amiens travel bulletin (2026-09-18)

Focused final-ROM mGBA checks; the full suite was not rerun. Real button input
checks the archived-account prerequisite, porter's No/B choices, early board
and Nora interactions, reading the bulletin, porter verification, delivery
to Nora and repeated conversations. Five journal leads describe the actual
saved stage. The existing ten-milestone checklist is unchanged. Checks also
cover a Celebi detour midway and the return service after completion.

Six normal Save -> fresh boot -> Continue checkpoints cover ready, active,
board copied, present-day detour, checked and delivered states; each resumes
to completion. The save verifier now checks the new variable on every case.
The full runner includes this scenario and 169 cold-save checkpoints.

The prior Ada-account regression passed its prerequisite, Oxford journey,
No/B, repeat report, journal, Amiens revisit, Meowth relocation and party care.
Dialogue fits the 216-pixel text area (215 maximum); journal text fits 226
pixels (214 maximum). The checked-news and completed-waiting-plan journal
screenshots were visually inspected. The bulletin explicitly states that no
onward service is available yet; return travel remains usable. Map layouts,
NPC placement, inventory and rewards are unchanged.


## v0.34 - Onward Rouen journey (2026-09-18)

Focused verification, not a full integration-suite rerun. Real mGBA button
input passed the bulletin prerequisite, boarding and return No/B choices,
arrival, repeated Leon welcome, Celebi No/B and return, unfinished re-entry,
three journal leads and Rouen historical map context. A separate booking
check uses an actual booked modern journey plus explicit historical unlock
fixtures; after visiting Rouen and returning through Celebi, that original
rail booking resumes successfully. Conversation/travel checks preserve
party, money, inventory, badges and present-day quest state.

Four normal Save -> cold boot -> Continue cases cover ready, arrival,
present-day detour and welcomed states; each resumes to the welcome. The
save verifier checks Rouen progress for every case. The full runner includes
Rouen and now has 173 cold-save checkpoints. The prior Amiens bulletin test
passes with the new train explicitly declined in its repeat-porter helper.

All 35 custom maps pass event bounds, connections and path checks. Rouen
reuses the tested Amiens layout; its map ID and region section were appended
without renumbering existing entries. It has no cycling, running, escaping
or wild encounters, and uses the historical Chantilly respawn. The engine's
OLD_MAN_1 sprite constant corrected an initial link error before emulator
checks. Dialogue fits 216 pixels (215 maximum); journal text fits 226 pixels
(214 maximum). Arrival and historical-map screenshots were visually checked.


## v0.35 - Rouen riverside layout (2026-09-18)

Focused final-ROM verification; the complete integration suite was not rerun.
Rouen has a separate 36x20 layout, expanded east of the old 24x20 courtyard.
Static checks pass on all 35 custom maps and assert that every previously
reachable courtyard tile remains reachable. River cells are not walkable;
both banks, crossing and reception paths are reachable. Existing events,
arrival coordinates and map IDs are preserved.

Real-button mGBA tests walk both banks and the crossing, attempt to walk into
water and the outer forest, and return to Leon. Screenshots of the northern
bank, southern bank and crossing were visually reviewed, including tree caps,
trunks and side edges. Updated notice dialogue fits all three text fonts.

The first old-save test exposed the saved layout ID and cached old tiles.
A Rouen-only migration updates the layout and clears its cached map view when
the saved layout differs, preserving coordinates and all quest state. A real
v0.34 battery save made at (21,16), beside the old east boundary, loads at
that exact location and can immediately walk to the expanded bank. The normal
full runner skips the archived-ROM migration; --legacy enables that check.

Normal Save -> cold boot -> Continue passes on the far bank and four existing
Rouen checkpoints. The complete Rouen travel regression also passes boarding,
return and Celebi No/B, welcome, journal/map context and resumption of a real
modern rail booking. The full runner now includes riverside walking and 174
cold-save cases. No new quest stage or reward is introduced in this release.


## v0.36 - Rouen route-book recovery (2026-09-18)

Focused final-ROM checks; the full integration suite was not rerun. Real
mGBA button input covers the arrival prerequisite, Leon's No/B, acceptance,
reminder, far-bank pickup, return and repeat dialogue. Pickup visibility is
checked nearby before acceptance, while active, after collection and after
returning. Travel through Amiens and Celebi preserves progress. Four journal
leads and unchanged party, inventory, money and modern progress are checked.
A full Items-pocket fixture still permits collection and completion without
consuming or adding inventory items.

Five normal Save -> cold boot -> Continue stages (ready, active, found,
present-day detour and completed) resume to completion and verify that the
pickup stays removed. The save verifier checks the new variable in every
case. The full runner includes this quest and 179 cold-save checkpoints.

A standalone migration test creates an actual v0.35 battery save beside Leon
using the archived ROM, then loads the new ROM, accepts immediately and
collects the newly spawned book without leaving the map. The new object
template is refreshed for old Rouen saves and its temporary visibility flag
is restored from persistent quest progress. The archived-ROM check remains
separate from the normal full runner.

The prior Rouen travel regression passes No/B choices, welcome, both exits,
map/journal context and resuming an actual modern rail booking. All 35 custom
maps pass static checks, including the pickup's accessible approach. Dialogue
fits the 216-pixel text area (216 maximum); journal text fits 226 pixels
(214 maximum). The pickup and active-journal screenshots were inspected.


## v0.37 - Rouen party care (2026-09-18)

Focused final-ROM mGBA checks; the entire integration suite was not rerun.
Returning the route book unlocks free care but does not automatically heal.
No/B preserves tired-party health. Yes and repeat use restore HP, status
and PP. Care remains available after the Amiens return route and a Celebi
round trip. An existing completed route-book battery save unlocks it directly.
A six-member fixture with burns, empty PP and a fainted slot verifies whole-
party healing. A full Items pocket does not block care. Non-health Pokemon
identity, inventory, money and story variables remain unchanged.

Two normal Save -> cold boot -> Continue cases preserve tired/rested health
and permit care afterward. The route-book regression passes its request,
pickup visibility, return, No/B, repeats, travel, full Bag and journal checks.
The full runner includes Rouen care and 181 cold-save checkpoints.
Dialogue fits 216 pixels; map/journal text fits 226 pixels. The care offer
and completed journal guidance were visually inspected. An initial test
started before the delayed build finished and saw the old behavior; all
reported tests were rerun on the completed final ROM and passed.


## v0.38 - Paged historical records (2026-09-18)

Focused final-ROM checks; not a complete integration-suite rerun. Historical
records now show ten entries on page one and three on page two. New bits
record the delivered Amiens bulletin, Rouen welcome and returned route book.
The existing u16 milestone mask holds all thirteen entries. No new save
variable is needed; completed older quests automatically populate the list.

Five real battery-save stages (empty, Amiens account, Rouen arrival, Rouen
welcome and route-book complete) pass mask checks, both paging directions,
page wrap, lead/records toggle, topic reset, map round trip and read-only
exit. The second page displays incomplete and completed entries correctly
in visually inspected screenshots. The regional topic stays on one page.
Two normal Save -> cold boot -> Continue cases preserve empty/full progress
and allow the same paging checks afterward.

All 27 earlier historical journal cases and registered-map B/START exits
pass. The regional journal suite passes 28 saved cases plus targeted trainer
and stamp fixtures. Expected masks in affected newer quest tests now include
the additional completion bits. The full runner includes paging checks and
183 cold-save checkpoints. All journal text fits the 226-pixel area.


## v0.39 - Historical Le Havre connection (2026-09-18)

Focused final-ROM mGBA verification, not a full-suite rerun. Real button input
passes the route-book prerequisite, Rouen boarding No/B, port arrival,
captain welcome and return No/B, repeat visits, Celebi choices and unfinished
re-entry. The blocked north entrance prevents accidental travel into an
unconnected map. The port label and journal objectives are verified, and
paging checks confirm the fourteenth milestone with mask 16383. Screenshots
of the harbor, map label and second records page were visually inspected.

Four normal Save -> cold boot -> Continue cases resume before departure,
after arrival, after a present-day detour and after the welcome. A separate
migration test makes an actual archived v0.38 battery save beside the new
Rouen clerk and successfully boards immediately on the new ROM. Its object
template is restored for old saves. New map, region and layout entries are
appended; existing identifiers and Rouen event positions are retained.

A genuine modern rail booking plus explicit historical-unlock fixtures
survives the port journey and resumes afterward. The Rouen care regression
passes its gate, both return routes, No/B, old completed saves, six-member
healing and full Bag. All 36 custom maps pass bounds and path checks; the
validator selects harbor metatile attributes for harbor layouts. Dialogue
fits 216 pixels and journal text fits 226 pixels. The full runner includes
Le Havre before paging tests and now covers 187 cold-save checkpoints.


## v0.40 Le Havre dock instructions

The final ROM built successfully. Focused mGBA input tests passed the welcome
gate, early notice and captain interactions, request No/B, all three task
steps, repeated conversations, both return routes and four journal leads.
The completed journal has fifteen milestones (mask 32767); its second page
was visually checked with all five rows visible and marked DONE. The notice
interaction was also visually checked at the closed entrance.

Five normal Save -> cold boot -> Continue cases passed: ready, accepted,
notice read, returned to the present and completed. A genuine archived
v0.39 save made beside the new worker starts and completes the task on the
new ROM without leaving the map. The prior Le Havre travel regression also
passed, including preservation and resumption of a real modern rail booking.

All 36 custom-map bounds/path checks passed, including the worker approach.
Dialogue width checks pass at 216 pixels; journal text fits 226 pixels.
The full runner now includes this task and 192 cold-save checkpoints.
This release ran the focused tests above, not the entire suite.


## v0.41 Le Havre dockworker care

The final ROM built successfully. Focused mGBA input tests passed the
dock-task gate, completion without automatic healing, No/B, free repeat
healing of HP/status/PP, and both return routes. An existing completed
v0.40 battery-save checkpoint unlocks care immediately. Targeted health
fixtures exercised damage, burn and depleted PP; an explicit six-member
party/full Bag fixture included a fainted slot. Healing preserved Pokemon
identity, inventory, money, rail booking and quest progress.

The full dock-instructions regression passed its welcome gate, early
interactions, request choices, repeated conversations, four leads and
fifteen-record paging. Seven normal Save -> cold boot -> Continue checks
passed: tired/rested care states and all five dock-task checkpoints.
The care cases verify health survives reloading and care remains usable.

The care offer and updated journal lead were visually checked in mGBA
screenshots. Dialogue fits 216 pixels; journal text fits 226 pixels.
The full runner now includes dock care and 194 cold-save checkpoints.
This release ran the focused checks above, not the entire suite.


## v0.42 Ada's port account

The final ROM built successfully. Focused mGBA input tests passed the dock
confirmation prerequisite, an actual Oxford rail journey, No/B, recording
the account and repeated reports. Party, items and other quest variables
remain unchanged. An existing completed dock-task battery checkpoint can
report immediately. A real Le Havre revisit retains the account and free
dockworker care; returning to Ada again retains the recorded report.

Three normal Save -> cold boot -> Continue checks passed: before reporting,
after reporting and after returning to the port. The new account variable
is included in journal read-only snapshots and save preservation checks.
Ada's earlier Amiens account regression also passed its gates, choices,
journey, report, journal and revisit/care checks.

Eight historical journal states passed page wrapping, lead toggling, topic
reset and read-only exits. All sixteen completed milestones produce 65535;
the existing unsigned rendering handles bit 15 correctly. Screenshots of
the finished lead and second page were inspected: six DONE rows fit with
the controls visible. Dialogue fits 216 pixels; journal text fits 226.
The full runner now includes the port report and 197 cold-save checkpoints.
This release ran the focused checks above, not the entire suite.


## v0.43 Celebi direct port revisits

The final ROM built successfully. Focused mGBA input tests passed the port
account gate, the original refuge route before the unlock, initial No/B,
destination-menu Exit/B, both destination choices and repeated direct port
visits. Existing recorded-account battery saves unlock the menu immediately.
All tested trips preserve party, inventory, money and quest variables.
Dockworker care, the Rouen return and the Celebi return remain functional.

A genuine pending modern rail booking survived the shortcut and resumed
afterward. That case uses an explicit historical-unlock fixture on the
existing rail itinerary; the other unlock case uses the recorded-account
checkpoint. Three normal Save -> cold boot -> Continue cases passed in the
forest, at direct port arrival and after returning to the forest, with the
shortcut usable after each reload.

The port-account regression also passed its prerequisite, real Oxford trip,
No/B, report/repeat, sixteen-record paging and normal-route port revisit.
The destination menu was visually inspected; its labels and underlying
dialogue fit. Dialogue checks fit 216 pixels; journal text fits 226 pixels.
The full runner now includes the shortcut and 200 cold-save checkpoints.
This release ran these focused checks, not the entire suite.


## v0.44 Southampton crossing and reception

The final ROM built successfully after shortening one over-width dialogue
line. Focused mGBA input tests passed the recorded-account gate, clerk No/B,
crossing, arrival, host welcome and return choices, repeated visits, blocked
north entrance, both return routes and dockworker care after returning.
The historical Southampton map correctly uses England's modern reference
node. A genuine modern rail booking survived the journey and resumed;
that case uses explicit historical-unlock fixtures on a real itinerary.

A genuine v0.43 battery save made beside the future ferry clerk boarded
immediately on the new ROM. The new object's template is restored on load;
existing map, layout and region identifiers remain stable with new entries
appended. Four normal Save -> cold boot -> Continue cases passed before
departure, after arrival, after a present-day detour and after the welcome.

The journal now carries a 32-bit completion mask across two task fields.
Nine old/new progress states passed paging, topic reset, lead toggling and
read-only exits, including all seventeen records (131071). The high word
clears for regional records and restores for the historical topic. The new
map, completed lead and second records page were visually inspected; all
seven second-page records and controls fit. All 37 map path checks passed.
Dialogue fits 216 pixels and journal text fits 226 pixels.

The previous direct-port shortcut regression passed its choices, returns,
care and real rail-booking resumption. Concurrent cancellation tests exposed
a shared temporary snapshot filename; each process now uses its own file,
and the Southampton suite passed on rerun. The full runner includes this
chapter and 204 cold-save checkpoints. This release ran the focused tests
above, not the entire suite.


## v0.45 Southampton luggage task

The final ROM built successfully. Focused mGBA input tests passed the host
welcome gate, request No/B, acceptance, reminder, pickup and return. The
pickup appears only while requested, disappears when collected and stays
hidden after completion and revisits. Both return routes work during the
task, including a present-day detour while carrying the bag. An explicit
full Bag fixture still allows collection and return without altering the
inventory or party. Repeated conversations do not duplicate progress.

A genuine v0.44 battery save made beside the new worker starts and completes
the task without leaving the map. The worker and pickup templates refresh
on load; visibility derives from the saved quest variable. Five normal
Save -> cold boot -> Continue cases passed: ready, active, found, returned
to the present and complete. Each resumes the task or verifies completion.

Four journal leads and the eighteenth record passed. Ten journal progress
states passed paging, topic reset and read-only exits, including mask
262143 for all eighteen milestones. Pickup dialogue and the eight completed
rows on page two were visually inspected. Dialogue fits 216 pixels and
journal text fits 226 pixels. All 37 map path checks passed.

The Southampton travel regression passed its gates, welcome, choices,
return routes, care, historical England map context and real modern rail
booking resumption. The full runner includes luggage and 209 cold-save
checkpoints. This release ran these focused tests, not the entire suite.


## v0.46 Southampton party care

The final ROM built successfully. Focused mGBA input tests passed the
luggage-task prerequisite, hand-in without automatic healing, No/B and
repeat free healing of HP/status/PP. Both return routes retain care. An
existing completed luggage battery save unlocks care immediately. Targeted
health fixtures exercise damage, burn and depleted PP; a six-member party
fixture includes a fainted slot and a full Bag. Healing preserves Pokemon
identity, inventory, money and all historical/regional quest variables.

Two normal Save -> cold boot -> Continue cases passed, verifying damaged
and healed health data survive and care remains usable after reloading.
The luggage regression passed its welcome gate, choices, pickup visibility,
return, repeats, both travel routes, four leads, eighteenth milestone,
paging and full Bag handling. The care menu and updated journal lead were
visually inspected. Dialogue fits 216 pixels and journal text fits 226.
The full runner now includes Southampton care and 211 cold-save checkpoints.
This release ran the focused checks above, not the entire suite.


## v0.47 Direct Southampton revisits

The final ROM built successfully. Focused mGBA input tests passed the
luggage-completion gate, initial No/B, destination Exit/B, all three
destinations and repeated direct Southampton visits. The pre-unlock menu
still exits at its original third entry. Existing completed luggage battery
saves unlock the expanded menu immediately. Every trip preserves party,
inventory, money and all saved historical/regional quest variables.

Southampton care and both return routes passed. A genuine modern rail
booking survived direct Southampton travel and resumed afterward, with
explicit historical-unlock fixtures on the real pending itinerary. Three
normal Save -> cold boot -> Continue cases passed in the forest, at direct
arrival and after returning, with the shortcut and care usable after reload.

The earlier Le Havre shortcut regression passed its gate, choices, routes,
care and rail-booking resumption. The luggage regression passed its gate,
choices, pickup/return, visibility, repeats, full Bag case, journal leads
and eighteen-record paging. The expanded destination menu was visually
inspected. Dialogue fits 216 pixels; journal text fits 226 pixels.
The full runner now includes the shortcut and 214 cold-save checkpoints.
This release ran these focused tests, not the entire suite.


## v0.48 Southampton account

The final ROM built successfully. Focused mGBA input tests passed the
luggage prerequisite, actual Oxford journey, No/B, recording and repeated
reports. Party, inventory, money and previous quest progress are preserved.
An existing completed luggage battery checkpoint can report immediately.
A direct Southampton revisit retains the report and free party care; a
second Oxford visit retains the recorded account.

Three normal Save -> cold boot -> Continue cases passed before reporting,
after reporting and after revisiting Southampton. The new variable is
included in save preservation and read-only journal snapshots. Ada's earlier
Le Havre report regression passed its prerequisite, choices, real journey,
report/repeats, journal and revisit/care behavior.

Eleven historical progress states passed paging, topic reset, lead toggling
and read-only exit. All nineteen milestones produce mask 524287. The second
page's nine DONE rows and completed lead were visually inspected with no
clipping. Dialogue fits 216 pixels; journal text fits 226 pixels.
The full runner now includes this account and 217 cold-save checkpoints.
This release ran the focused checks above, not the entire suite.


## v0.49 Historical London reception

The final ROM built successfully. Focused mGBA input tests passed the
Southampton-account prerequisite, boarding No/B, arrival, Rose's welcome,
repeated conversations and both exits. The return guide works before and
after the welcome, and unfinished visits resume after a Celebi detour.
Southampton care remains usable after returning. London uses the historical
map label and modern England reference correctly. A real modern rail
booking survived the London journey and resumed; that case uses explicit
historical-unlock fixtures on a genuine pending itinerary.

A genuine v0.48 battery save made beside the future transport clerk boarded
and checked in immediately on the new ROM. Its template is restored on load;
map, layout and region identifiers are appended. Four normal Save -> cold
boot -> Continue cases passed before departure, after arrival, after a
present-day detour and after the welcome. The London variable is included
in save preservation and journal read-only snapshots.

Twelve historical journal states passed page wrapping, lead toggling, topic
reset and read-only exit. All twenty milestones produce mask 1048575. The
arrival scene, historical map and all ten second-page DONE rows were
visually inspected. All 38 map path checks passed after adding London's
return guide to the validator. Dialogue fits 216 pixels; journal fits 226.

The direct Southampton shortcut regression passed its gates, all choices,
returns, care and real rail-booking resumption. The full runner includes
London and 221 cold-save checkpoints. This release ran these focused tests,
not the entire suite.


## v0.50 Geography and World Options foundation

ROM build passed. Emulator input tests passed map-board item grant and
duplicate protection, all eight map selections, cosmetic identity/party
preservation, normal Save/cold Continue preferences, restoration of the
original avatar, real Bag registration, SELECT opening and START return,
cycling avatar changes and dismount. The first movement test used a stale
save-block address after menu transitions; reading the live pointer fixed
the test and confirmed identity preservation. All 38 static map path checks
passed. Geographic data generation is byte-for-byte reproducible. Map,
options and avatar screenshots were inspected. No full-suite run, surfing
regression, or town-layout overhaul is claimed by this checkpoint.


## v0.51 Capital landmark districts

The release adds London/Paris/Berlin walking-map districts and independent
landmark tilesets. Each capital was built and tested before the next. Static
checks cover all old traversable positions, unchanged land/water/elevation,
GBA metatile/palette limits, and all 38 existing map path/link checks. Real
input tests compare every loaded capital map tile with its authored data,
walk the new districts, read signs, cross bridges, save normally and cold
Continue. Berlin's central Gate passage is traversable. London also checks
the clinic/station and an old surfing save; Paris and Berlin reconnect to
the countryside. Screenshots were inspected for all six landmark sprites.

The surfing check exposed the existing SavedMapViewIsEmpty out-of-bounds
read: clearing the cache could still appear nonempty, restoring zero tiles.
The loop now uses the actual array bound. The same old battery dismounted
correctly in v0.50, failed before this fix, and passes after it. All final
capital reload tests now check the complete terrain buffer to catch this.

Early test-harness corrections accounted for legitimate walking friendship
gains and the clinic's central exit tile. The final ROM was then retested
for all three districts, World Options persistence, registered-item use and
cycling avatar continuity. The historical London regression was also run.
This is a focused regression pass; the entire project suite was not run.
