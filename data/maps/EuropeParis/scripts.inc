EuropeParis_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeParis_OnTransition
	.byte 0

EuropeParis_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_PARIS
	end

EuropeParis_Guide::
	lock
	faceplayer
	msgbox EuropeParis_Text_Welcome
	goto EuropeTour_Paris

EuropeParis_ClinicSign::
	msgbox EuropeParis_Text_Clinic, MSGBOX_SIGN
	end

EuropeParis_StationSign::
	msgbox EuropeParis_Text_Station, MSGBOX_SIGN
	end

EuropeParis_RouteSign::
	msgbox EuropeParis_Text_Route, MSGBOX_SIGN
	end

EuropeParis_Text_Welcome::
	.string "Welcome to PARIS!\n"
	.string "The countryside lies to the north.\p"
	.string "Heal at the clinic. The station has\n"
	.string "trains and traveling supplies.\p"
	.string "CELINE waits west of this square.\n"
	.string "Ask her about the garden survey.$"

EuropeParis_Text_Clinic::
	.string "POKEMON CLINIC\nFree care for traveling partners.$"

EuropeParis_Text_Station::
	.string "PARIS STATION\nEuropean rail ticket office.$"

EuropeParis_Text_Route::
	.string "NORTH: FRENCH GARDENS\nThen CHANTILLY FOREST and town.\p"
	.string "Cycle along the clear middle path.\n"
	.string "Wild POKEMON live in the tall grass.$"

EuropeParis_Landmark::
	msgbox EuropeParis_Text_Landmark, MSGBOX_SIGN
	end

EuropeParis_Text_Landmark::
	.string "TUILERIES GARDENS\n"
	.string "Flowers and paths in central PARIS.$"
