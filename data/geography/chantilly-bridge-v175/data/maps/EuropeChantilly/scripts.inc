EuropeChantilly_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeChantilly_OnTransition
	.byte 0

EuropeChantilly_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	end

EuropeChantilly_Guide::
	lock
	faceplayer
	msgbox EuropeChantilly_Text_Welcome
	goto EuropeChallenge_Chantilly

EuropeChantilly_ClinicSign::
	msgbox EuropeParis_Text_Clinic, MSGBOX_SIGN
	end

EuropeChantilly_StationSign::
	msgbox EuropeChantilly_Text_Station, MSGBOX_SIGN
	end

EuropeChantilly_RouteSign::
	msgbox EuropeChantilly_Text_Route, MSGBOX_SIGN
	end

EuropeChantilly_Landmark::
	msgbox EuropeChantilly_Text_Landmark, MSGBOX_SIGN
	end

EuropeChantilly_Text_Welcome::
	.string "Welcome to CHANTILLY! Enjoy the\n"
	.string "gardens after your forest journey.\p"
	.string "The clinic can heal your partners.\n"
	.string "Our station has trains and supplies.\p"
	.string "Walk south to PARIS through the\n"
	.string "forest, or take the train back.\p"
	.string "The stamp tour still visits\n"
	.string "LONDON, PARIS, and BERLIN.$"

EuropeChantilly_Text_Station::
	.string "CHANTILLY STATION\nEuropean rail ticket office.\p"
	.string "GYM: north of the town square.\n"
	.string "REMY waits west of the town guide.$"

EuropeChantilly_Text_Route::
	.string "SOUTH: CHANTILLY FOREST\nThen FRENCH GARDENS and PARIS.$"

EuropeChantilly_Text_Landmark::
	.string "CHANTILLY GARDEN WALK\nFlowers welcome weary travelers.$"

EuropeChallenge_Chantilly::
	goto_if_eq VAR_EUROPE_FRANCE_CHALLENGE, 1, EuropeChallenge_Complete
	setvar VAR_0x8005, 0
	call_if_defeated TRAINER_EUROPE_CAMILLE, EuropeTour_CountStamp
	call_if_defeated TRAINER_EUROPE_LUCIE, EuropeTour_CountStamp
	goto_if_eq VAR_0x8005, 2, EuropeChallenge_Chantilly_Reward
	buffernumberstring STR_VAR_1, VAR_0x8005
	goto_if_defeated TRAINER_EUROPE_CAMILLE, EuropeChallenge_Chantilly_NeedExtended
	goto_if_defeated TRAINER_EUROPE_LUCIE, EuropeChallenge_Chantilly_NeedLocal
	msgbox EuropeChallenge_Chantilly_Progress
	release
	end
EuropeChallenge_Chantilly_Reward::
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeChallenge_BagFull
	msgbox EuropeChallenge_Text_Reward
	giveitem ITEM_RARE_CANDY, 1
	setvar VAR_EUROPE_FRANCE_CHALLENGE, 1
	goto EuropeChallenge_Complete
EuropeChallenge_Chantilly_Progress::
	.string "Regional trail wins: {STR_VAR_1} of 2.\p"
	.string "Meet CAMILLE in FRENCH GARDENS.\n"
	.string "Meet LUCIE on this town's trail.\p"
	.string "Win both friendly matches, then\n"
	.string "return here for one RARE CANDY!$"

EuropeChantilly_GymSign::
	msgbox EuropeChantilly_Text_GymSign, MSGBOX_SIGN
	end

EuropeChantilly_RealismChateau::
	msgbox EuropeChantilly_RealismChateauText, MSGBOX_SIGN
	end

EuropeChantilly_RealismChateauText::
	.string "CHATEAU DE CHANTILLY\n"
	.string "Cross the moat to the chateau court.$"

EuropeChantilly_RealismStables::
	msgbox EuropeChantilly_RealismStablesText, MSGBOX_SIGN
	end

EuropeChantilly_RealismStablesText::
	.string "GRANDES ECURIES\n"
	.string "The estate's historic Great Stables.$"

EuropeChantilly_RealismGardens::
	msgbox EuropeChantilly_RealismGardensText, MSGBOX_SIGN
	end

EuropeChantilly_RealismGardensText::
	.string "FORMAL GARDENS / GRAND CANAL\n"
	.string "Paths follow the garden axes.$"

EuropeChantilly_Text_GymSign::
	.string "CHANTILLY GYM\n"
	.string "LEADER: MARINE\p"
	.string "Teamwork that turns the tide.\p"
	.string "Complete CELINE's survey, then\n"
	.string "collect her reward in PARIS.$"

EuropeChallenge_Chantilly_NeedExtended::
	msgbox EuropeChallenge_Chantilly_NeedExtendedText
	release
	end
EuropeChallenge_Chantilly_NeedExtendedText::
	.string "Regional trail wins: {STR_VAR_1} of 2.\p"
	.string "Next: LUCIE in CHANTILLY FOREST.\p"
	.string "Follow the clear path south of town.\p"
	.string "Win that match, then return here.\n"
	.string "Both wins earn one RARE CANDY.$"
EuropeChallenge_Chantilly_NeedLocal::
	msgbox EuropeChallenge_Chantilly_NeedLocalText
	release
	end
EuropeChallenge_Chantilly_NeedLocalText::
	.string "Regional trail wins: {STR_VAR_1} of 2.\p"
	.string "Next: CAMILLE in FRENCH GARDENS.\p"
	.string "Go south through this town's trail.\n"
	.string "Continue south into the countryside.\p"
	.string "Win that match, then return here.\n"
	.string "Both wins earn one RARE CANDY.$"
