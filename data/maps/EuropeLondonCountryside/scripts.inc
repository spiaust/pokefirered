EuropeLondonCountryside_MapScripts::
	.byte 0

EuropeTrail_Oliver::
	lock
	faceplayer
	goto_if_defeated TRAINER_EUROPE_OLIVER, EuropeTrail_Oliver_After
	msgbox EuropeTrail_Oliver_Ask, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeTrail_Decline
	trainerbattle_single TRAINER_EUROPE_OLIVER, EuropeTrail_Oliver_Intro, EuropeTrail_Oliver_Lose
EuropeTrail_Oliver_After::
	msgbox EuropeTrail_Oliver_Done
	call EuropeTrail_Report
	release
	end

EuropeTrail_Oliver_Ask::
	.string "I'm OLIVER, a local trail trainer.\p"
	.string "You can say No and come back later.\n"
	.string "The town clinic heals teams for free.\p"
	.string "Would you like a friendly battle?\n"
	.string "My two partners are ready!$"

EuropeTrail_Oliver_Intro::
	.string "The meadow is full of surprises!$"

EuropeTrail_Oliver_Lose::
	.string "We learned something new today!$"

EuropeTrail_Oliver_Done::
	.string "Well battled! Our match is recorded.\p"
	.string "Look for another trail trainer in\n"
	.string "each country's countryside.\p"
	.string "Head north to OXFORD TRAIL.\n"
	.string "Meet ALICE for an optional match.\p"
	.string "OXFORD guide: one RARE CANDY.\n"
	.string "Win both matches to claim the reward.$"
