EuropeOxford_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeOxford_OnTransition
	.byte 0

EuropeOxford_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_OXFORD
	end

EuropeOxford_Guide::
	lock
	faceplayer
	msgbox EuropeOxford_Text_Welcome
	goto EuropeChallenge_Oxford

EuropeOxford_ClinicSign::
	msgbox EuropeLondon_Text_Clinic, MSGBOX_SIGN
	end

EuropeOxford_StationSign::
	msgbox EuropeOxford_Text_Station, MSGBOX_SIGN
	end

EuropeOxford_RouteSign::
	msgbox EuropeOxford_Text_Route, MSGBOX_SIGN
	end

EuropeOxford_Landmark::
	msgbox EuropeOxford_Text_Landmark, MSGBOX_SIGN
	end

EuropeOxford_Text_Welcome::
	.string "Welcome to OXFORD! Rest your team\n"
	.string "at the clinic after the long trail.\p"
	.string "Follow the path south through the\n"
	.string "meadow, or take a train to LONDON.\p"
	.string "The three-city stamp tour still\n"
	.string "visits LONDON, PARIS, and BERLIN.$"

EuropeOxford_Text_Station::
	.string "OXFORD STATION\nEuropean rail ticket office.$"

EuropeOxford_Text_Route::
	.string "SOUTH: OXFORD TRAIL\nThen ENGLISH MEADOW and LONDON.$"

EuropeOxford_Text_Landmark::
	.string "OXFORD GARDEN WALK\nA quiet rest for traveling partners.$"

EuropeChallenge_Oxford::
	goto_if_eq VAR_EUROPE_ENGLAND_CHALLENGE, 1, EuropeChallenge_Complete
	setvar VAR_0x8005, 0
	call_if_defeated TRAINER_EUROPE_OLIVER, EuropeTour_CountStamp
	call_if_defeated TRAINER_EUROPE_ALICE, EuropeTour_CountStamp
	goto_if_eq VAR_0x8005, 2, EuropeChallenge_Oxford_Reward
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox EuropeChallenge_Oxford_Progress
	release
	end
EuropeChallenge_Oxford_Reward::
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeChallenge_BagFull
	msgbox EuropeChallenge_Text_Reward
	giveitem ITEM_RARE_CANDY, 1
	setvar VAR_EUROPE_ENGLAND_CHALLENGE, 1
	goto EuropeChallenge_Complete
EuropeChallenge_Oxford_Progress::
	.string "Regional trail wins: {STR_VAR_1} of 2.\p"
	.string "Meet OLIVER in ENGLISH MEADOW.\n"
	.string "Meet ALICE on this town's trail.\p"
	.string "Win both friendly matches, then\n"
	.string "return here for one RARE CANDY!$"

EuropeOxford_GymSign::
	msgbox EuropeOxfordGym_Text_Statue, MSGBOX_SIGN
	end

EuropeOxford_RealismRadcliffe::
	msgbox EuropeOxford_RealismRadcliffeText, MSGBOX_SIGN
	end

EuropeOxford_RealismRadcliffeText::
	.string "RADCLIFFE SQUARE\n"
	.string "The domed RADCLIFFE CAMERA library.$"

EuropeOxford_RealismMagdalen::
	msgbox EuropeOxford_RealismMagdalenText, MSGBOX_SIGN
	end

EuropeOxford_RealismMagdalenText::
	.string "MAGDALEN TOWER / HIGH STREET\n"
	.string "MAGDALEN BRIDGE crosses the CHERWELL.$"

EuropeOxford_RealismMeadow::
	msgbox EuropeOxford_RealismMeadowText, MSGBOX_SIGN
	end

EuropeOxford_RealismMeadowText::
	.string "CHERWELL MEADOW PATH\n"
	.string "Follow the river back to HIGH STREET.$"
