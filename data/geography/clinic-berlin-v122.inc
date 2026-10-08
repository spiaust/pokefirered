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
	.string "BERLIN STATION\nEuropean rail ticket office.\p"
	.string "BERLIN: THREE COURTYARD ROOMS\n"
	.string "Follow the south paths, then east.\p"
	.string "Travel map: select this city.\n"
	.string "Press R for Places, then L for Rooms.$"

EuropeBerlin_Text_Route::
	.string "NORTH: GERMAN WOODLAND\nThen HAVEL TRAIL to ORANIENBURG.\p"
	.string "Cycle along the clear middle path.\n"
	.string "Wild POKEMON live in the tall grass.\p"
	.string "BERLIN VISITOR ROOMS\n"
	.string "East courtyard: three visitor rooms.\p"
	.string "Travel map: select this city.\n"
	.string "Press R for Places, then L for Rooms.$"

EuropeBerlin_Landmark::
	msgbox EuropeBerlin_Text_Landmark, MSGBOX_SIGN
	end

EuropeBerlin_Text_Landmark::
	.string "TIERGARTEN WALK\n"
	.string "A green retreat in busy BERLIN.$"

EuropeBerlin_RealismReichstag::
	msgbox EuropeBerlin_RealismReichstagText, MSGBOX_SIGN
	end

EuropeBerlin_RealismReichstagText::
	.string "REICHSTAG\n"
	.string "The SPREE runs north of here.\p"
	.string "Visitor archive: face the south door.\n"
	.string "Press A to speak to the curator.$"

EuropeBerlin_RealismGate::
	msgbox EuropeBerlin_RealismGateText, MSGBOX_SIGN
	end

EuropeBerlin_RealismGateText::
	.string "BRANDENBURG GATE\n"
	.string "UNTER DEN LINDEN leads east.\p"
	.string "Visitor room: face the west pillar.\n"
	.string "Press A from the path to visit.$"

EuropeBerlin_RealismTiergarten::
	msgbox EuropeBerlin_RealismTiergartenText, MSGBOX_SIGN
	end

EuropeBerlin_RealismTiergartenText::
	.string "TIERGARTEN\n"
	.string "Garden paths west of the GATE.$"

EuropeBerlin_RealismBoulevard::
	msgbox EuropeBerlin_RealismBoulevardText, MSGBOX_SIGN
	end

EuropeBerlin_RealismBoulevardText::
	.string "UNTER DEN LINDEN APPROACH\n"
	.string "West: BRANDENBURG GATE.\p"
	.string "East: the residential court.\n"
	.string "Use the side lanes to circle it.$"

EuropeBerlin_RealismCourt::
	msgbox EuropeBerlin_RealismCourtText, MSGBOX_SIGN
	end

EuropeBerlin_RealismCourtText::
	.string "COURTYARD VISITOR ROOMS\n"
	.string "West: home. Middle: reading room.\p"
	.string "East: the garden workroom.\n"
	.string "Face a door and press A to visit.\p"
	.string "COURTYARD NOTES\n"
	.string "Seed and watering notes: workroom.\p"
	.string "Garden log: middle reading room.\n"
	.string "Share a memory in the western home.\p"
	.string "Return west along the main road.\n"
	.string "The GATE visitor room is on the west.$"

EuropeBerlin_CourtGardener::
	lock
	faceplayer
	msgbox EuropeBerlin_CourtGardenerText, MSGBOX_DEFAULT
	release
	end

EuropeBerlin_CourtGardenerText::
	.string "I tend these flowers with my ODDISH.\n"
	.string "Care makes a place feel like home.\p"
	.string "The lane south of us loops back\n"
	.string "to the BRANDENBURG GATE.$"

EuropeBerlin_CourtNeighbor::
	lock
	faceplayer
	msgbox EuropeBerlin_CourtNeighborText, MSGBOX_DEFAULT
	release
	end

EuropeBerlin_CourtNeighborText::
	.string "PIKACHU keeps me company here.\n"
	.string "All three doors welcome visitors.\p"
	.string "West: home. Middle: reading room.\n"
	.string "East: the garden workroom.$"

EuropeBerlin_CourtPikachu::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PIKACHU, CRY_MODE_NORMAL
	msgbox EuropeBerlin_CourtPikachuText, MSGBOX_DEFAULT
	waitmoncry
	release
	end

EuropeBerlin_CourtPikachuText::
	.string "PIKACHU: Pika! Pika!$"
