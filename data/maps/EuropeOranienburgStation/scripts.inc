EuropeOranienburgStation_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeOranienburgStation_OnTransition
	.byte 0

EuropeOranienburgStation_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_ORANIENBURG
	end

EuropeOranienburgStation_Clerk::
	setvar VAR_0x8004, 5
	goto Europe_Train

EuropeOranienburgStation_LocalBoard::
 lockall
 msgbox EuropeOranienburgStation_LocalBoardText, MSGBOX_DEFAULT
 releaseall
 end

EuropeOranienburgStation_LocalBoardText::
 .string "LOCAL WALKS / ORANIENBURG\n"
 .string "GYM: north of the town square.\p"
 .string "KARL waits west of the town guide.\n"
 .string "South: HAVEL TRAIL, then BERLIN.$"
