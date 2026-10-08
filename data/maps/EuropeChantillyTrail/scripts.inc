EuropeChantillyTrail_MapScripts::
	.byte 0

EuropeChantillyTrail_Sign::
	msgbox EuropeChantillyTrail_Text_Directions, MSGBOX_SIGN
	end

EuropeChantillyTrail_Text_Directions::
	.string "NORTH: CHANTILLY\nSOUTH: FRENCH GARDENS and PARIS\p"
	.string "Cycle along the clear middle path.\n"
	.string "Wild POKEMON live in the tall grass.\p"
	.string "Need free healing? Head north.\n"
	.string "Next town: CHANTILLY.\p"
	.string "Free clinic: west side of the square.\n"
	.string "Supplies: shop in the town station.$"

EuropeTrail_Lucie::
	lock
	faceplayer
	goto_if_defeated TRAINER_EUROPE_LUCIE, EuropeTrail_Lucie_After
	msgbox EuropeTrail_Lucie_Ask, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeTrail_Lucie_Decline
	trainerbattle_single TRAINER_EUROPE_LUCIE, EuropeTrail_Lucie_Intro, EuropeTrail_Lucie_Lose
EuropeTrail_Lucie_After::
	msgbox EuropeTrail_Lucie_Done
	release
	end
EuropeTrail_Lucie_Ask::
	.string "I'm LUCIE! My trail team is ready.\p"
	.string "You can say No and come back later.\n"
	.string "The town clinic heals teams for free.\p"
	.string "Would you like a friendly battle?$"
EuropeTrail_Lucie_Intro::
	.string "Let's see how far we've come!$"
EuropeTrail_Lucie_Lose::
	.string "A fine journey together!$"
EuropeTrail_Lucie_Done::
	.string "Our match is recorded! Visit the\n"
	.string "CHANTILLY guide for your reward.\p"
	.string "Follow the clear path north to town.\n"
	.string "The guide waits in the town square.\p"
	.string "Both regional wins earn a RARE CANDY.\n"
	.string "Free clinic: west side of the square.$"

EuropeTrail_Lucie_Decline::
	msgbox EuropeTrail_Lucie_DeclineText
	release
	end
EuropeTrail_Lucie_DeclineText::
	.string "No hurry! Heal at the town clinic,\n"
	.string "then come back when you're ready.\p"
	.string "Follow the clear path north.\n"
	.string "Next town: CHANTILLY.\p"
	.string "Free clinic: west side of the square.$"
