EuropeChantillyStation_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeChantillyStation_OnTransition
	.byte 0

EuropeChantillyStation_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	end

EuropeChantillyStation_Clerk::
	setvar VAR_0x8004, 4
	goto Europe_Train
