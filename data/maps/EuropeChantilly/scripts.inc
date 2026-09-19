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
	.string "CHANTILLY STATION\nEuropean rail ticket office.$"

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
	msgbox EuropeChantillyGym_Text_Statue, MSGBOX_SIGN
	end
