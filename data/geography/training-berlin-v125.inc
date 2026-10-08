EuropeBerlinCountryside_MapScripts::
	.byte 0

EuropeTrail_Felix::
	lock
	faceplayer
	goto_if_defeated TRAINER_EUROPE_FELIX, EuropeTrail_Felix_After
	msgbox EuropeTrail_Felix_Ask, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeTrail_Decline
	trainerbattle_single TRAINER_EUROPE_FELIX, EuropeTrail_Felix_Intro, EuropeTrail_Felix_Lose
EuropeTrail_Felix_After::
	msgbox EuropeTrail_Felix_Done
	call EuropeTrail_Report
	release
	end

EuropeTrail_Felix_Ask::
	.string "I'm FELIX, a local trail trainer.\p"
	.string "Would you like a friendly battle?\n"
	.string "My two partners are ready!$"

EuropeTrail_Felix_Intro::
	.string "My partners love these woodlands!$"

EuropeTrail_Felix_Lose::
	.string "That was a great trail battle!$"

EuropeTrail_Felix_Done::
	.string "Well battled! Our match is recorded.\p"
	.string "Look for another trail trainer in\n"
	.string "each country's countryside.$"
