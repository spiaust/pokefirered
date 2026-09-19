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
	.string "Ask her about the garden survey.\p"
	.string "NOTRE-DAME has a visitor entrance\n"
	.string "on its south side. Try the door.$"

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

EuropeParis_RealismEiffel::
	msgbox EuropeParis_RealismEiffelText, MSGBOX_SIGN
	end

EuropeParis_RealismEiffelText::
	.string "EIFFEL TOWER / CHAMP DE MARS\n"
	.string "The SEINE lies to the north.\p"
	.string "Garden paths circle the flower beds.\n"
	.string "The riverside walk continues east.$"

EuropeParis_RealismNotreDame::
	msgbox EuropeParis_RealismNotreDameText, MSGBOX_SIGN
	end

EuropeParis_RealismNotreDameText::
	.string "NOTRE-DAME / ILE DE LA CITE\n"
	.string "The cathedral stands on an island.\p"
	.string "Undercroft: face the south door.\n"
	.string "Press A to ask about visiting.$"

EuropeParis_RealismSeine::
	msgbox EuropeParis_RealismSeineText, MSGBOX_SIGN
	end

EuropeParis_RealismSeineText::
	.string "RIVES DE SEINE\n"
	.string "Cross the bridges to the LEFT BANK.\p"
	.string "Follow the promenade east for\n"
	.string "the bridge to NOTRE-DAME.$"
