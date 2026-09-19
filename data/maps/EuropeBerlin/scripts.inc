EuropeBerlin_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeBerlin_OnTransition
	.byte 0

EuropeBerlin_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_BERLIN
	end

EuropeBerlin_Guide::
	lock
	faceplayer
	msgbox EuropeBerlin_Text_Welcome
	goto EuropeTour_Berlin

EuropeBerlin_ClinicSign::
	msgbox EuropeBerlin_Text_Clinic, MSGBOX_SIGN
	end

EuropeBerlin_StationSign::
	msgbox EuropeBerlin_Text_Station, MSGBOX_SIGN
	end

EuropeBerlin_RouteSign::
	msgbox EuropeBerlin_Text_Route, MSGBOX_SIGN
	end

EuropeBerlin_Text_Welcome::
	.string "Welcome to BERLIN!\n"
	.string "The countryside lies to the north.\p"
	.string "Heal at the clinic. The station has\n"
	.string "trains and traveling supplies.$"

EuropeBerlin_Text_Clinic::
	.string "POKEMON CLINIC\nFree care for traveling partners.$"

EuropeBerlin_Text_Station::
	.string "BERLIN STATION\nEuropean rail ticket office.$"

EuropeBerlin_Text_Route::
	.string "NORTH: GERMAN WOODLAND\nThen HAVEL TRAIL to ORANIENBURG.\p"
	.string "Cycle along the clear middle path.\n"
	.string "Wild POKEMON live in the tall grass.$"

EuropeBerlin_Landmark::
	msgbox EuropeBerlin_Text_Landmark, MSGBOX_SIGN
	end

EuropeBerlin_Text_Landmark::
	.string "TIERGARTEN WALK\n"
	.string "A green retreat in busy BERLIN.$"
