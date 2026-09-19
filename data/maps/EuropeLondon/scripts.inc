EuropeLondon_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeLondon_OnTransition
	.byte 0

EuropeLondon_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_LONDON
	end

EuropeLondon_Guide::
	lock
	faceplayer
	msgbox EuropeLondon_Text_Welcome
	goto EuropeTour_London

EuropeLondon_ClinicSign::
	msgbox EuropeLondon_Text_Clinic, MSGBOX_SIGN
	end

EuropeLondon_StationSign::
	msgbox EuropeLondon_Text_Station, MSGBOX_SIGN
	end

EuropeLondon_RouteSign::
	msgbox EuropeLondon_Text_Route, MSGBOX_SIGN
	end

EuropeLondon_Text_Welcome::
	.string "Welcome to LONDON!\n"
	.string "The countryside lies to the north.\p"
	.string "Heal at the clinic. The station has\n"
	.string "trains and traveling supplies.\p"
	.string "OAK's aide is west of this square.\n"
	.string "Ask about his ENGLAND field study.$"

EuropeLondon_Text_Clinic::
	.string "POKEMON CLINIC\nFree care for traveling partners.$"

EuropeLondon_Text_Station::
	.string "LONDON STATION\nEuropean rail ticket office.$"

EuropeLondon_Text_Route::
	.string "NORTH: ENGLISH MEADOW\nContinue along the trail to OXFORD.\p"
	.string "Wild POKEMON live in the tall grass.\n"
	.string "The middle path is clear for bikes.$"

EuropeLondon_Landmark::
	msgbox EuropeLondon_Text_Landmark, MSGBOX_SIGN
	end

EuropeLondon_Text_Landmark::
	.string "THAMES PROMENADE\n"
	.string "A riverside walk through LONDON.$"
