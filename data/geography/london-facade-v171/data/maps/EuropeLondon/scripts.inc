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
	.string "POKEMON CLINIC\nFree care for traveling partners.\p"
	.string "Enter the door beside this sign.\n"
	.string "Talk to the nurse to heal your team.$"

EuropeLondon_Text_Station::
	.string "LONDON STATION\nEuropean rail ticket office.\p"
	.string "LONDON: HOME AND READING ROOM\n"
	.string "Follow the south paths, then east.\p"
	.string "Travel map: select this city.\n"
	.string "Press R for Places, then L for Rooms.$"

EuropeLondon_Text_Route::
	.string "NORTH: ENGLISH MEADOW\nContinue along the trail to OXFORD.\p"
	.string "Wild POKEMON live in the tall grass.\n"
	.string "The middle path is clear for bikes.\p"
	.string "Look for OLIVER on the north route.\n"
	.string "Battles are optional. You can say No.\p"
	.string "Free clinic: west side of the square.\n"
	.string "Supplies: shop inside the station.\p"
	.string "LONDON VISITOR ROOMS\n"
	.string "East lane: home and reading room.\p"
	.string "Travel map: select this city.\n"
	.string "Press R for Places, then L for Rooms.$"

EuropeLondon_Landmark::
	msgbox EuropeLondon_Text_Landmark, MSGBOX_SIGN
	end

EuropeLondon_Text_Landmark::
	.string "THAMES PROMENADE\n"
	.string "Cross south to WESTMINSTER.\p"
	.string "PARLIAMENT and the LONDON EYE\n"
	.string "stand on opposite riverbanks.$"

EuropeLondon_RealismWhitehall::
	msgbox EuropeLondon_RealismTextWhitehall, MSGBOX_SIGN
	end

EuropeLondon_RealismTextWhitehall::
	.string "WHITEHALL / PARLIAMENT SQUARE\n"
	.string "Clock tower and PARLIAMENT: south.$"

EuropeLondon_RealismParliament::
	msgbox EuropeLondon_RealismTextParliament, MSGBOX_SIGN
	end

EuropeLondon_RealismTextParliament::
	.string "PALACE OF WESTMINSTER\n"
	.string "The clock tower houses BIG BEN.\p"
	.string "WESTMINSTER BRIDGE leads east\n"
	.string "to the LONDON EYE and SOUTH BANK.\p"
	.string "Look for the green bridge rails.\n"
	.string "LAMBETH's red crossing lies south.\p"
	.string "Visitor room: face the south door.\n"
	.string "Press A to ask about visiting.$"

EuropeLondon_RealismEye::
	msgbox EuropeLondon_RealismTextEye, MSGBOX_SIGN
	end

EuropeLondon_RealismTextEye::
	.string "LONDON EYE\n"
	.string "Visitor gallery: face the south base.\p"
	.string "Press A to ask about visiting.\n"
	.string "The THAMES flows to the west.$"

EuropeLondon_RealismGardens::
	msgbox EuropeLondon_RealismTextGardens, MSGBOX_SIGN
	end

EuropeLondon_RealismTextGardens::
	.string "JUBILEE GARDENS\n"
	.string "Follow the SOUTH BANK riverside path.\p"
	.string "The garden loop rejoins the walk\n"
	.string "toward the red LAMBETH crossing.$"

EuropeLondon_GardenVisitor::
	lock
	faceplayer
	msgbox EuropeLondon_GardenVisitorText, MSGBOX_DEFAULT
	release
	end

EuropeLondon_GardenVisitorText::
	.string "JIGGLYPUFF likes this quiet garden.\n"
	.string "We give resting POKEMON room.\p"
	.string "The EYE gallery has garden sketches.\n"
	.string "Follow the riverside path north.$"

EuropeLondon_GardenJigglypuff::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_JIGGLYPUFF, CRY_MODE_NORMAL
	msgbox EuropeLondon_GardenJigglypuffText, MSGBOX_DEFAULT
	waitmoncry
	release
	end

EuropeLondon_GardenJigglypuffText::
	.string "JIGGLYPUFF: Jiggly! Puff!$"

EuropeLondon_RealismSideStreet::
	msgbox EuropeLondon_RealismSideStreetText, MSGBOX_SIGN
	end

EuropeLondon_RealismSideStreetText::
	.string "GARDEN SIDE LANE\n"
	.string "West: the EYE and riverside paths.\p"
	.string "Follow the southern loop around\n"
	.string "the flower beds and homes.$"

EuropeLondon_RealismHomes::
	msgbox EuropeLondon_RealismHomesText, MSGBOX_SIGN
	end

EuropeLondon_RealismHomesText::
	.string "RESIDENTIAL LANE\n"
	.string "West: open sitting room.\p"
	.string "East: open reading room.\n"
	.string "Face either door and press A.\p"
	.string "Return west along the garden lane.\n"
	.string "The EYE gallery welcomes visitors.$"
