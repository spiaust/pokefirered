@ Independent cases: 0 unstarted, 1 accepted, 2/3 one clue, 4 both, 5 resolved, 6 rewarded.
EuropeCase_NotreDame_Enter::
 lockall
 msgbox EuropeCase_NotreDame_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 closemessage
 warp MAP_EUROPE_NOTREDAME, 10, 15
 waitstate
 releaseall
 end
EuropeCase_NotreDame_Exit::
 lockall
 warp MAP_EUROPE_PARIS, 28, 35
 waitstate
 releaseall
 end
EuropeCase_NotreDame_Curator::
 lock
 faceplayer
 goto_if_eq 0x40C0, 6, EuropeCase_NotreDame_Complete
 goto_if_eq 0x40C0, 5, EuropeCase_NotreDame_Reward
 goto_if_ne 0x40C0, 0, EuropeCase_NotreDame_Progress
 msgbox EuropeCase_NotreDame_OfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 setvar 0x40C0, 1
EuropeCase_NotreDame_Progress::
 msgbox EuropeCase_NotreDame_ProgressText
 goto EuropeCase_End
EuropeCase_NotreDame_Reward::
 checkitemspace ITEM_SPELL_TAG, 1
 goto_if_eq VAR_RESULT, FALSE, EuropeCase_Full
 msgbox EuropeCase_NotreDame_ThanksText
 giveitem ITEM_SPELL_TAG, 1
 setvar 0x40C0, 6
EuropeCase_NotreDame_Complete::
 msgbox EuropeCase_NotreDame_CompleteText
 call EuropeCase_Synthesis
 goto EuropeCase_End
EuropeCase_NotreDame_Resolve::
 lockall
 goto_if_ge 0x40C0, 5, EuropeCase_NotreDame_After
 goto_if_ne 0x40C0, 4, EuropeCase_NotreDame_NeedClues
 msgbox EuropeCase_NotreDame_ResolveText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 setvar 0x40C0, 5
 msgbox EuropeCase_NotreDame_ResultText
 goto EuropeCase_End
EuropeCase_NotreDame_NeedClues::
 msgbox EuropeCase_NeedCluesText
 goto EuropeCase_End
EuropeCase_NotreDame_After::
 msgbox EuropeCase_GastlyText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 setwildbattle SPECIES_GASTLY, 12
 dowildbattle
 releaseall
 end
EuropeCase_NotreDame_ClueA::
 lockall
 goto_if_eq 0x40C0, 0, EuropeCase_NotreDame_NeedClues
 msgbox EuropeCase_NotreDame_ClueAText
 goto_if_ge 0x40C0, 4, EuropeCase_End
 goto_if_eq 0x40C0, 3, EuropeCase_NotreDame_Both
 setvar 0x40C0, 2
 goto EuropeCase_End
EuropeCase_NotreDame_ClueAText::
	.string "The caretaker notes that the\n"
	.string "GASTLY appeared after a noisy\p"
	.string "repair began. They hide when the\n"
	.string "tools start.$"
EuropeCase_NotreDame_ClueB::
 lockall
 goto_if_eq 0x40C0, 0, EuropeCase_NotreDame_NeedClues
 msgbox EuropeCase_NotreDame_ClueBText
 goto_if_ge 0x40C0, 4, EuropeCase_End
 goto_if_eq 0x40C0, 2, EuropeCase_NotreDame_Both
 setvar 0x40C0, 3
 goto EuropeCase_End
EuropeCase_NotreDame_ClueBText::
	.string "An old route ledger describes\n"
	.string "quiet shelters for traveling\p"
	.string "people and POKEMON. A green\n"
	.string "visitor appears in its margins.$"
EuropeCase_NotreDame_Both::
 setvar 0x40C0, 4
 msgbox EuropeCase_BothText
 goto EuropeCase_End
EuropeCase_NotreDame_EntryText::
	.string "The Quiet Bells. Enter the\n"
	.string "landmark visitor area?$"
EuropeCase_NotreDame_OfferText::
	.string "GASTLY have gathered in the\n"
	.string "undercroft. Visitors think they\p"
	.string "are angry. Help me learn what is\n"
	.string "frightening them. Will you\p"
	.string "investigate?$"
EuropeCase_NotreDame_ProgressText::
	.string "Read the two records in the side\n"
	.string "aisles. Then speak to the\p"
	.string "attendant at the north end. Return\n"
	.string "here when the case is resolved.$"
EuropeCase_NotreDame_ResolveText::
	.string "The GASTLY need shelter, not\n"
	.string "chasing. Ask the caretaker to\p"
	.string "pause the noisy work?$"
EuropeCase_NotreDame_ResultText::
	.string "The tools fall silent. GASTLY\n"
	.string "drift into the quiet side aisle.\p"
	.string "Their restless calls become a\n"
	.string "gentle murmur.$"
EuropeCase_NotreDame_ThanksText::
	.string "You listened before acting. Keep\n"
	.string "this SPELL TAG. The old ledger\p"
	.string "mentions CHANTILLY; ADA in OXFORD\n"
	.string "studies such routes.$"
EuropeCase_NotreDame_CompleteText::
	.string "The Quiet Bells is resolved. Your\n"
	.string "field notes are safe. You can\p"
	.string "still explore this area and read\n"
	.string "its records.$"
EuropeCase_Westminster_Enter::
 lockall
 msgbox EuropeCase_Westminster_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 closemessage
 warp MAP_EUROPE_WESTMINSTER, 10, 15
 waitstate
 releaseall
 end
EuropeCase_Westminster_Exit::
 lockall
 warp MAP_EUROPE_LONDON, 14, 35
 waitstate
 releaseall
 end
EuropeCase_Westminster_Curator::
 lock
 faceplayer
 goto_if_eq 0x40C1, 6, EuropeCase_Westminster_Complete
 goto_if_eq 0x40C1, 5, EuropeCase_Westminster_Reward
 goto_if_ne 0x40C1, 0, EuropeCase_Westminster_Progress
 msgbox EuropeCase_Westminster_OfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 setvar 0x40C1, 1
EuropeCase_Westminster_Progress::
 msgbox EuropeCase_Westminster_ProgressText
 goto EuropeCase_End
EuropeCase_Westminster_Reward::
 checkitemspace ITEM_RARE_CANDY, 1
 goto_if_eq VAR_RESULT, FALSE, EuropeCase_Full
 msgbox EuropeCase_Westminster_ThanksText
 giveitem ITEM_RARE_CANDY, 1
 setvar 0x40C1, 6
EuropeCase_Westminster_Complete::
 msgbox EuropeCase_Westminster_CompleteText
 call EuropeCase_Synthesis
 goto EuropeCase_End
EuropeCase_Westminster_Resolve::
 lockall
 goto_if_ge 0x40C1, 5, EuropeCase_Westminster_After
 goto_if_ne 0x40C1, 4, EuropeCase_Westminster_NeedClues
 msgbox EuropeCase_Westminster_ResolveText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 setvar 0x40C1, 5
 msgbox EuropeCase_Westminster_ResultText
 goto EuropeCase_End
EuropeCase_Westminster_NeedClues::
 msgbox EuropeCase_NeedCluesText
 goto EuropeCase_End
EuropeCase_Westminster_After::
 msgbox EuropeCase_Westminster_ResultText
 goto EuropeCase_End
EuropeCase_Westminster_ClueA::
 lockall
 goto_if_eq 0x40C1, 0, EuropeCase_Westminster_NeedClues
 msgbox EuropeCase_Westminster_ClueAText
 goto_if_ge 0x40C1, 4, EuropeCase_End
 goto_if_eq 0x40C1, 3, EuropeCase_Westminster_Both
 setvar 0x40C1, 2
 goto EuropeCase_End
EuropeCase_Westminster_ClueAText::
	.string "The riverside keeper reports that\n"
	.string "repairs closed a sheltered\p"
	.string "passage. The flock returns there\n"
	.string "every evening.$"
EuropeCase_Westminster_ClueB::
 lockall
 goto_if_eq 0x40C1, 0, EuropeCase_Westminster_NeedClues
 msgbox EuropeCase_Westminster_ClueBText
 goto_if_ge 0x40C1, 4, EuropeCase_End
 goto_if_eq 0x40C1, 2, EuropeCase_Westminster_Both
 setvar 0x40C1, 3
 goto EuropeCase_End
EuropeCase_Westminster_ClueBText::
	.string "A reception ledger records\n"
	.string "travelers arriving from\p"
	.string "SOUTHAMPTON with their POKEMON.\n"
	.string "Keeping companions together helped\p"
	.string "them settle.$"
EuropeCase_Westminster_Both::
 setvar 0x40C1, 4
 msgbox EuropeCase_BothText
 goto EuropeCase_End
EuropeCase_Westminster_EntryText::
	.string "A Place to Rest. Enter the\n"
	.string "landmark visitor area?$"
EuropeCase_Westminster_OfferText::
	.string "A flock of HOOTHOOT is circling\n"
	.string "the river instead of resting. This\p"
	.string "visitor room holds old route\n"
	.string "records. Will you find out what\p"
	.string "they need?$"
EuropeCase_Westminster_ProgressText::
	.string "Read the two records in the side\n"
	.string "aisles. Then speak to the\p"
	.string "attendant at the north end. Return\n"
	.string "here when the case is resolved.$"
EuropeCase_Westminster_ResolveText::
	.string "Ask the keeper to reopen the safe\n"
	.string "shelter route before evening?$"
EuropeCase_Westminster_ResultText::
	.string "The keeper opens the sheltered\n"
	.string "passage. The flock settles beneath\p"
	.string "the eaves. A familiar route feels\n"
	.string "safe again.$"
EuropeCase_Westminster_ThanksText::
	.string "Thank you. Take a RARE CANDY for\n"
	.string "your team. The ledger links this\p"
	.string "place with SOUTHAMPTON and France.\n"
	.string "Share that clue with ADA.$"
EuropeCase_Westminster_CompleteText::
	.string "A Place to Rest is resolved. Your\n"
	.string "field notes are safe. You can\p"
	.string "still explore this area and read\n"
	.string "its records.$"
EuropeCase_Reichstag_Enter::
 lockall
 msgbox EuropeCase_Reichstag_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 closemessage
 warp MAP_EUROPE_REICHSTAG, 10, 15
 waitstate
 releaseall
 end
EuropeCase_Reichstag_Exit::
 lockall
 warp MAP_EUROPE_BERLIN, 21, 33
 waitstate
 releaseall
 end
EuropeCase_Reichstag_Curator::
 lock
 faceplayer
 goto_if_eq 0x40C2, 6, EuropeCase_Reichstag_Complete
 goto_if_eq 0x40C2, 5, EuropeCase_Reichstag_Reward
 goto_if_ne 0x40C2, 0, EuropeCase_Reichstag_Progress
 msgbox EuropeCase_Reichstag_OfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 setvar 0x40C2, 1
EuropeCase_Reichstag_Progress::
 msgbox EuropeCase_Reichstag_ProgressText
 goto EuropeCase_End
EuropeCase_Reichstag_Reward::
 checkitemspace ITEM_GREAT_BALL, 3
 goto_if_eq VAR_RESULT, FALSE, EuropeCase_Full
 msgbox EuropeCase_Reichstag_ThanksText
 giveitem ITEM_GREAT_BALL, 3
 setvar 0x40C2, 6
EuropeCase_Reichstag_Complete::
 msgbox EuropeCase_Reichstag_CompleteText
 call EuropeCase_Synthesis
 goto EuropeCase_End
EuropeCase_Reichstag_Resolve::
 lockall
 goto_if_ge 0x40C2, 5, EuropeCase_Reichstag_After
 goto_if_ne 0x40C2, 4, EuropeCase_Reichstag_NeedClues
 msgbox EuropeCase_Reichstag_ResolveText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 setvar 0x40C2, 5
 msgbox EuropeCase_Reichstag_ResultText
 goto EuropeCase_End
EuropeCase_Reichstag_NeedClues::
 msgbox EuropeCase_NeedCluesText
 goto EuropeCase_End
EuropeCase_Reichstag_After::
 msgbox EuropeCase_Reichstag_ResultText
 goto EuropeCase_End
EuropeCase_Reichstag_ClueA::
 lockall
 goto_if_eq 0x40C2, 0, EuropeCase_Reichstag_NeedClues
 msgbox EuropeCase_Reichstag_ClueAText
 goto_if_ge 0x40C2, 4, EuropeCase_End
 goto_if_eq 0x40C2, 3, EuropeCase_Reichstag_Both
 setvar 0x40C2, 2
 goto EuropeCase_End
EuropeCase_Reichstag_ClueAText::
	.string "The technician recorded a\n"
	.string "repeating pulse from the temporary\p"
	.string "relay. Nearby MAGNEMITE turn\n"
	.string "toward it whenever it sounds.$"
EuropeCase_Reichstag_ClueB::
 lockall
 goto_if_eq 0x40C2, 0, EuropeCase_Reichstag_NeedClues
 msgbox EuropeCase_Reichstag_ClueBText
 goto_if_ge 0x40C2, 4, EuropeCase_End
 goto_if_eq 0x40C2, 2, EuropeCase_Reichstag_Both
 setvar 0x40C2, 3
 goto EuropeCase_End
EuropeCase_Reichstag_ClueBText::
	.string "The archive describes how routes\n"
	.string "change when stations close. Safe\p"
	.string "paths depend on reliable signals\n"
	.string "and people sharing accurate news.$"
EuropeCase_Reichstag_Both::
 setvar 0x40C2, 4
 msgbox EuropeCase_BothText
 goto EuropeCase_End
EuropeCase_Reichstag_EntryText::
	.string "The Broken Signal. Enter the\n"
	.string "landmark visitor area?$"
EuropeCase_Reichstag_OfferText::
	.string "A temporary relay is drawing\n"
	.string "MAGNEMITE away from their usual\p"
	.string "route. Our visitor archive may\n"
	.string "help. Will you investigate?$"
EuropeCase_Reichstag_ProgressText::
	.string "Read the two records in the side\n"
	.string "aisles. Then speak to the\p"
	.string "attendant at the north end. Return\n"
	.string "here when the case is resolved.$"
EuropeCase_Reichstag_ResolveText::
	.string "Ask the technician to disconnect\n"
	.string "the faulty relay and restore the\p"
	.string "proper signal?$"
EuropeCase_Reichstag_ResultText::
	.string "The false pulse stops. MAGNEMITE\n"
	.string "return to the riverside route. The\p"
	.string "technician marks the safe path for\n"
	.string "future visitors.$"
EuropeCase_Reichstag_ThanksText::
	.string "These GREAT BALLS are for your\n"
	.string "travels. LENA and KARL maintain\p"
	.string "trail beacons too. ADA is\n"
	.string "comparing changes along old\p"
	.string "routes.$"
EuropeCase_Reichstag_CompleteText::
	.string "The Broken Signal is resolved.\n"
	.string "Your field notes are safe. You can\p"
	.string "still explore this area and read\n"
	.string "its records.$"
EuropeCase_Full::
 msgbox EuropeCase_FullText
EuropeCase_End::
 releaseall
 end
EuropeCase_Synthesis::
 compare 0x40C0, 6
 goto_if_ne EuropeCase_Return
 compare 0x40C1, 6
 goto_if_ne EuropeCase_Return
 compare 0x40C2, 6
 goto_if_ne EuropeCase_Return
 msgbox EuropeCase_SynthesisText
EuropeCase_Return::
 return
EuropeCase_Ledger::
 lockall
 msgbox EuropeCase_LedgerText
 compare 0x40C0, 6
 call_if_eq EuropeCase_NotreDame_Recorded
 compare 0x40C0, 6
 call_if_ne EuropeCase_NotreDame_Open
 compare 0x40C1, 6
 call_if_eq EuropeCase_Westminster_Recorded
 compare 0x40C1, 6
 call_if_ne EuropeCase_Westminster_Open
 compare 0x40C2, 6
 call_if_eq EuropeCase_Reichstag_Recorded
 compare 0x40C2, 6
 call_if_ne EuropeCase_Reichstag_Open
 call EuropeCase_Synthesis
 goto EuropeCase_End
EuropeCase_NotreDame_Recorded::
 msgbox EuropeCase_NotreDame_RecordedText
 return
EuropeCase_NotreDame_RecordedText::
	.string "PARIS: case resolved and reward\n"
	.string "collected.$"
EuropeCase_NotreDame_Open::
 msgbox EuropeCase_NotreDame_OpenText
 return
EuropeCase_NotreDame_OpenText::
	.string "PARIS: this case is still open.\n"
	.string "Speak to the landmark curator for\p"
	.string "directions.$"
EuropeCase_Westminster_Recorded::
 msgbox EuropeCase_Westminster_RecordedText
 return
EuropeCase_Westminster_RecordedText::
	.string "LONDON: case resolved and reward\n"
	.string "collected.$"
EuropeCase_Westminster_Open::
 msgbox EuropeCase_Westminster_OpenText
 return
EuropeCase_Westminster_OpenText::
	.string "LONDON: this case is still open.\n"
	.string "Speak to the landmark curator for\p"
	.string "directions.$"
EuropeCase_Reichstag_Recorded::
 msgbox EuropeCase_Reichstag_RecordedText
 return
EuropeCase_Reichstag_RecordedText::
	.string "BERLIN: case resolved and reward\n"
	.string "collected.$"
EuropeCase_Reichstag_Open::
 msgbox EuropeCase_Reichstag_OpenText
 return
EuropeCase_Reichstag_OpenText::
	.string "BERLIN: this case is still open.\n"
	.string "Speak to the landmark curator for\p"
	.string "directions.$"
EuropeCase_FullText::
	.string "Your case is resolved. Make room\n"
	.string "in the BAG for your reward, then\p"
	.string "speak to me again.$"
EuropeCase_NeedCluesText::
	.string "Speak to the curator near the\n"
	.string "entrance, then read both records\p"
	.string "before deciding what to do.$"
EuropeCase_BothText::
	.string "Both clues are recorded. Speak to\n"
	.string "the attendant at the north end.$"
EuropeCase_GastlyText::
	.string "A GASTLY approaches calmly. Meet\n"
	.string "it in an optional wild battle? You\p"
	.string "may catch it or leave.$"
EuropeCase_SynthesisText::
	.string "All three cases point to the same\n"
	.string "lesson: disturbed routes separate\p"
	.string "POKEMON from safe places. The old\n"
	.string "ledger names CHANTILLY and\p"
	.string "SOUTHAMPTON. Bring this pattern to\n"
	.string "ADA in OXFORD after earning the\p"
	.string "three regional badges.$"
EuropeCase_LedgerText::
	.string "LANDMARK FIELD NOTES. These cases\n"
	.string "are optional investigations\p"
	.string "alongside your regional studies.\n"
	.string "Each curator keeps your progress.$"
