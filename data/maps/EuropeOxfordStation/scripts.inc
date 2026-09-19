EuropeOxfordStation_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeOxfordStation_OnTransition
	.byte 0

EuropeOxfordStation_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_OXFORD
	end

EuropeOxfordStation_Clerk::
	setvar VAR_0x8004, 3
	goto Europe_Train
