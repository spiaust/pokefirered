EuropeOxfordStation_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeOxfordStation_OnTransition
	.byte 0

EuropeOxfordStation_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_OXFORD
	end

EuropeOxfordStation_Clerk::
	setvar VAR_0x8004, 3
	goto Europe_Train

EuropeOxfordStation_LocalBoard::
 lockall
 msgbox EuropeOxfordStation_LocalBoardText, MSGBOX_DEFAULT
 releaseall
 end

EuropeOxfordStation_LocalBoardText::
 .string "LOCAL WALKS / OXFORD\n"
 .string "GYM: north of the town square.\p"
 .string "ADA waits east of the town guide.\n"
 .string "South: OXFORD TRAIL, then LONDON.$"
