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
	.string "PARIS STATION\nEuropean rail ticket office.\p"
	.string "PARIS: SKETCHES AND GARDEN ROOM\n"
	.string "Follow the south paths, then east.\p"
	.string "Travel map: select this city.\n"
	.string "Press R for Places, then L for Rooms.$"

EuropeParis_Text_Route::
	.string "NORTH: FRENCH GARDENS\nThen CHANTILLY FOREST and town.\p"
	.string "Cycle along the clear middle path.\n"
	.string "Wild POKEMON live in the tall grass.\p"
	.string "PARIS VISITOR ROOMS\n"
	.string "East lane: sketches and garden room.\p"
	.string "Travel map: select this city.\n"
	.string "Press R for Places, then L for Rooms.$"

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
	.string "Visitor room: face the south base.\p"
	.string "Press A to ask about visiting.\n"
	.string "The SEINE lies to the north.$"

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

EuropeParis_RealismLane::
	msgbox EuropeParis_RealismLaneText, MSGBOX_SIGN
	end

EuropeParis_RealismLaneText::
	.string "PROMENADE SIDE LANE\n"
	.string "West: the river and EIFFEL gardens.\p"
	.string "The south path circles the flowers.\n"
	.string "Both homes welcome visitors.$"

EuropeParis_RealismHomes::
	msgbox EuropeParis_RealismHomesText, MSGBOX_SIGN
	end

EuropeParis_RealismHomesText::
	.string "NEIGHBORHOOD HOMES\n"
	.string "West: sketches. East: garden room.\p"
	.string "Face either door and press A.\n"
	.string "Return west for the island bridge.$"

EuropeParis_GardenObserver::
	lock
	faceplayer
	msgbox EuropeParis_GardenObserverText, MSGBOX_DEFAULT
	release
	end

EuropeParis_GardenObserverText::
	.string "PSYDUCK rests beside these flowers.\n"
	.string "I watch quietly and make notes.\p"
	.string "The EIFFEL visitor room has sketches.\n"
	.string "Follow the path north to visit.$"

EuropeParis_GardenPsyduck::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PSYDUCK, CRY_MODE_NORMAL
	msgbox EuropeParis_GardenPsyduckText, MSGBOX_DEFAULT
	waitmoncry
	release
	end

EuropeParis_GardenPsyduckText::
	.string "PSYDUCK: Psy? Psyduck!$"

EuropeParis_PromenadeArtist::
	lock
	faceplayer
	msgbox EuropeParis_PromenadeArtistText, MSGBOX_DEFAULT
	release
	end

EuropeParis_PromenadeArtistText::
	.string "I sketch the river from this bank.\n"
	.string "The light changes as people pass.\p"
	.string "I leave the path clear for walkers.\n"
	.string "A little space lets us all enjoy it.$"
