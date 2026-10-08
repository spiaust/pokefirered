EuropeParisCountryside_MapScripts::
	.byte 0

EuropeTrail_Camille::
	lock
	faceplayer
	goto_if_defeated TRAINER_EUROPE_CAMILLE, EuropeTrail_Camille_After
	msgbox EuropeTrail_Camille_Ask, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeTrail_Decline
	trainerbattle_single TRAINER_EUROPE_CAMILLE, EuropeTrail_Camille_Intro, EuropeTrail_Camille_Lose
EuropeTrail_Camille_After::
	msgbox EuropeTrail_Camille_Done
	call EuropeTrail_Report
	release
	end

EuropeTrail_Camille_Ask::
	.string "I'm CAMILLE, a local trail trainer.\p"
	.string "Would you like a friendly battle?\n"
	.string "My two partners are ready!$"

EuropeTrail_Camille_Intro::
	.string "A friendly match in the gardens?$"

EuropeTrail_Camille_Lose::
	.string "Your partner has real spirit!$"

EuropeTrail_Camille_Done::
	.string "Well battled! Our match is recorded.\p"
	.string "Look for another trail trainer in\n"
	.string "each country's countryside.$"
