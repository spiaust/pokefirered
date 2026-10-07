EuropeLondonStation_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeLondonStation_OnTransition
	.byte 0

EuropeLondonStation_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_LONDON
	end

EuropeLondonStation_Clerk::
	setvar VAR_0x8004, 0
	goto Europe_Train

EuropeLondonStation_LocalBoard::
 lockall
 msgbox EuropeLondonStation_LocalBoardText, MSGBOX_DEFAULT
 releaseall
 end

EuropeLondonStation_LocalBoardText::
 .string "LOCAL WALKS / LONDON\n"
 .string "Exit south for the THAMES paths.\p"
 .string "Follow the east lane for both homes.\n"
 .string "West: album. East: reading room.$"
