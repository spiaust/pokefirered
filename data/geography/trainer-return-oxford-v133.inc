EuropeOxfordTrail_MapScripts::
	.byte 0

EuropeOxfordTrail_Sign::
	msgbox EuropeOxfordTrail_Text_Directions, MSGBOX_SIGN
	end

EuropeOxfordTrail_Text_Directions::
	.string "NORTH: OXFORD\nSOUTH: ENGLISH MEADOW and LONDON\p"
	.string "The middle path is clear for bikes.\n"
	.string "Wild POKEMON live in the tall grass.\p"
	.string "Need free healing? Head north.\n"
	.string "Next town: OXFORD.\p"
	.string "Free clinic: west side of the square.\n"
	.string "Supplies: shop in the town station.$"

EuropeTrail_Alice::
	lock
	faceplayer
	goto_if_defeated TRAINER_EUROPE_ALICE, EuropeTrail_Alice_After
	msgbox EuropeTrail_Alice_Ask, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeTrail_Alice_Decline
	trainerbattle_single TRAINER_EUROPE_ALICE, EuropeTrail_Alice_Intro, EuropeTrail_Alice_Lose
EuropeTrail_Alice_After::
	msgbox EuropeTrail_Alice_Done
	release
	end
EuropeTrail_Alice_Ask::
	.string "I'm ALICE! My trail team is ready.\p"
	.string "You can say No and come back later.\n"
	.string "The town clinic heals teams for free.\p"
	.string "Would you like a friendly battle?$"
EuropeTrail_Alice_Intro::
	.string "Let's see how far we've come!$"
EuropeTrail_Alice_Lose::
	.string "A fine journey together!$"
EuropeTrail_Alice_Done::
	.string "Our match is recorded! Visit the\n"
	.string "OXFORD guide for your reward.$"

EuropeTrail_Alice_Decline::
	msgbox EuropeTrail_Alice_DeclineText
	release
	end
EuropeTrail_Alice_DeclineText::
	.string "No hurry! Heal at the town clinic,\n"
	.string "then come back when you're ready.\p"
	.string "Follow the clear path north.\n"
	.string "Next town: OXFORD.\p"
	.string "Free clinic: west side of the square.$"
