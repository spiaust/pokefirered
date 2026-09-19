EuropeOranienburgStation_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeOranienburgStation_OnTransition
	.byte 0

EuropeOranienburgStation_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_ORANIENBURG
	end

EuropeOranienburgStation_Clerk::
	setvar VAR_0x8004, 5
	goto Europe_Train
