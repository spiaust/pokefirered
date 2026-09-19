EuropeOranienburg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeOranienburg_OnTransition
	.byte 0

EuropeOranienburg_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_ORANIENBURG
	end

EuropeOranienburg_Guide::
	lock
	faceplayer
	msgbox EuropeOranienburg_Text_Welcome
	goto EuropeChallenge_Oranienburg

EuropeOranienburg_ClinicSign::
	msgbox EuropeBerlin_Text_Clinic, MSGBOX_SIGN
	end

EuropeOranienburg_StationSign::
	msgbox EuropeOranienburg_Text_Station, MSGBOX_SIGN
	end

EuropeOranienburg_RouteSign::
	msgbox EuropeOranienburg_Text_Route, MSGBOX_SIGN
	end

EuropeOranienburg_Landmark::
	msgbox EuropeOranienburg_Text_Landmark, MSGBOX_SIGN
	end

EuropeOranienburg_Text_Welcome::
	.string "Welcome to ORANIENBURG!\nRest your partners at our clinic.\p"
	.string "The southern trail leads through\n"
	.string "GERMAN WOODLAND back to BERLIN.\p"
	.string "Our station has trains and supplies\n"
	.string "for your next journey.\p"
	.string "The stamp tour still visits\n"
	.string "LONDON, PARIS, and BERLIN.$"

EuropeOranienburg_Text_Station::
	.string "ORANIENBURG STATION\nEuropean rail ticket office.$"

EuropeOranienburg_Text_Route::
	.string "SOUTH: HAVEL TRAIL\nThen GERMAN WOODLAND and BERLIN.$"

EuropeOranienburg_Text_Landmark::
	.string "ORANIENBURG PARK WALK\nA peaceful path beside the pond.$"

EuropeChallenge_Oranienburg::
	goto_if_eq VAR_EUROPE_GERMANY_CHALLENGE, 1, EuropeChallenge_Complete
	setvar VAR_0x8005, 0
	call_if_defeated TRAINER_EUROPE_FELIX, EuropeTour_CountStamp
	call_if_defeated TRAINER_EUROPE_OTTO, EuropeTour_CountStamp
	goto_if_eq VAR_0x8005, 2, EuropeChallenge_Oranienburg_Reward
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox EuropeChallenge_Oranienburg_Progress
	release
	end
EuropeChallenge_Oranienburg_Reward::
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeChallenge_BagFull
	msgbox EuropeChallenge_Text_Reward
	giveitem ITEM_RARE_CANDY, 1
	setvar VAR_EUROPE_GERMANY_CHALLENGE, 1
	goto EuropeChallenge_Complete
EuropeChallenge_Oranienburg_Progress::
	.string "Regional trail wins: {STR_VAR_1} of 2.\p"
	.string "Meet FELIX in GERMAN WOODLAND.\n"
	.string "Meet OTTO on this town's trail.\p"
	.string "Win both friendly matches, then\n"
	.string "return here for one RARE CANDY!$"

EuropeOranienburg_GymSign::
	msgbox EuropeOranienburgGym_Text_Statue, MSGBOX_SIGN
	end

EuropeOranienburg_RealismPalace::
	msgbox EuropeOranienburg_RealismPalaceText, MSGBOX_SIGN
	end

EuropeOranienburg_RealismPalaceText::
	.string "SCHLOSS ORANIENBURG\n"
	.string "The palace faces SCHLOSSPLATZ.$"

EuropeOranienburg_RealismPark::
	msgbox EuropeOranienburg_RealismParkText, MSGBOX_SIGN
	end

EuropeOranienburg_RealismParkText::
	.string "SCHLOSSPARK\n"
	.string "Garden paths west of the palace.$"

EuropeOranienburg_RealismHavel::
	msgbox EuropeOranienburg_RealismHavelText, MSGBOX_SIGN
	end

EuropeOranienburg_RealismHavelText::
	.string "HAVEL RIVERSIDE\n"
	.string "Cross the bridges to SCHLOSSPLATZ.$"
