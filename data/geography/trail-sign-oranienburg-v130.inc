EuropeOranienburgTrail_MapScripts::
	.byte 0

EuropeOranienburgTrail_Sign::
	msgbox EuropeOranienburgTrail_Text_Directions, MSGBOX_SIGN
	end

EuropeOranienburgTrail_Text_Directions::
	.string "NORTH: ORANIENBURG\nSOUTH: GERMAN WOODLAND and BERLIN\p"
	.string "Cycle along the clear middle path.\n"
	.string "Wild POKEMON live in the tall grass.$"

EuropeTrail_Otto::
	lock
	faceplayer
	goto_if_defeated TRAINER_EUROPE_OTTO, EuropeTrail_Otto_After
	msgbox EuropeTrail_Otto_Ask, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeTrail_Otto_Decline
	trainerbattle_single TRAINER_EUROPE_OTTO, EuropeTrail_Otto_Intro, EuropeTrail_Otto_Lose
EuropeTrail_Otto_After::
	msgbox EuropeTrail_Otto_Done
	release
	end
EuropeTrail_Otto_Ask::
	.string "I'm OTTO! My trail team is ready.\p"
	.string "You can say No and come back later.\n"
	.string "The town clinic heals teams for free.\p"
	.string "Would you like a friendly battle?$"
EuropeTrail_Otto_Intro::
	.string "Let's see how far we've come!$"
EuropeTrail_Otto_Lose::
	.string "A fine journey together!$"
EuropeTrail_Otto_Done::
	.string "Our match is recorded! Visit the\n"
	.string "ORANIENBURG guide for your reward.$"

EuropeTrail_Otto_Decline::
	msgbox EuropeTrail_Otto_DeclineText
	release
	end
EuropeTrail_Otto_DeclineText::
	.string "No hurry! Heal at the town clinic,\n"
	.string "then come back when you're ready.\p"
	.string "Follow the clear path north.\n"
	.string "Next town: ORANIENBURG.\p"
	.string "Free clinic: west side of the square.$"
