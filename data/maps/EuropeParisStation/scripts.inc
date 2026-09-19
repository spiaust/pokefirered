EuropeParisStation_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeParisStation_OnTransition
	.byte 0

EuropeParisStation_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_PARIS
	end

EuropeParisStation_Clerk::
	setvar VAR_0x8004, 1
	goto Europe_Train
