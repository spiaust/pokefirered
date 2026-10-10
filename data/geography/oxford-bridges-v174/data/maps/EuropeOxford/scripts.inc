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
	.string "OXFORD STATION\nEuropean rail ticket office.\p"
	.string "GYM: north of the town square.\n"
	.string "ADA waits east of the town guide.$"

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
	goto_if_defeated TRAINER_EUROPE_OLIVER, EuropeChallenge_Oxford_NeedExtended
	goto_if_defeated TRAINER_EUROPE_ALICE, EuropeChallenge_Oxford_NeedLocal
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
	msgbox EuropeOxford_Text_GymSign, MSGBOX_SIGN
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

EuropeOxford_Text_GymSign::
	.string "OXFORD GYM\nLEADER: ELLIS\p"
	.string "A firm foundation for every team.\p"
	.string "Finish OAK's field study, then\n"
	.string "report to his LONDON aide.$"

EuropeChallenge_Oxford_NeedExtended::
	msgbox EuropeChallenge_Oxford_NeedExtendedText
	release
	end
EuropeChallenge_Oxford_NeedExtendedText::
	.string "Regional trail wins: {STR_VAR_1} of 2.\p"
	.string "Next: ALICE in OXFORD TRAIL.\p"
	.string "Follow the clear path south of town.\p"
	.string "Win that match, then return here.\n"
	.string "Both wins earn one RARE CANDY.$"
EuropeChallenge_Oxford_NeedLocal::
	msgbox EuropeChallenge_Oxford_NeedLocalText
	release
	end
EuropeChallenge_Oxford_NeedLocalText::
	.string "Regional trail wins: {STR_VAR_1} of 2.\p"
	.string "Next: OLIVER in ENGLISH MEADOW.\p"
	.string "Go south through this town's trail.\n"
	.string "Continue south into the countryside.\p"
	.string "Win that match, then return here.\n"
	.string "Both wins earn one RARE CANDY.$"
