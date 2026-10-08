EuropeChantillyTrail_MapScripts::
	.byte 0

EuropeChantillyTrail_Sign::
	msgbox EuropeChantillyTrail_Text_Directions, MSGBOX_SIGN
	end

EuropeChantillyTrail_Text_Directions::
	.string "NORTH: CHANTILLY\nSOUTH: FRENCH GARDENS and PARIS\p"
	.string "Cycle along the clear middle path.\n"
	.string "Wild POKEMON live in the tall grass.$"

EuropeTrail_Lucie::
	lock
	faceplayer
	goto_if_defeated TRAINER_EUROPE_LUCIE, EuropeTrail_Lucie_After
	msgbox EuropeTrail_Lucie_Ask, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeTrail_Decline
	trainerbattle_single TRAINER_EUROPE_LUCIE, EuropeTrail_Lucie_Intro, EuropeTrail_Lucie_Lose
EuropeTrail_Lucie_After::
	msgbox EuropeTrail_Lucie_Done
	release
	end
EuropeTrail_Lucie_Ask::
	.string "I'm LUCIE! My trail team is ready.\p"
	.string "Would you like a friendly battle?$"
EuropeTrail_Lucie_Intro::
	.string "Let's see how far we've come!$"
EuropeTrail_Lucie_Lose::
	.string "A fine journey together!$"
EuropeTrail_Lucie_Done::
	.string "Our match is recorded! Visit the\n"
	.string "CHANTILLY guide for your reward.$"
