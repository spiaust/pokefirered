EuropeBerlinStation_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeBerlinStation_OnTransition
	.byte 0

EuropeBerlinStation_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_BERLIN
	end

EuropeBerlinStation_Clerk::
	setvar VAR_0x8004, 2
	goto Europe_Train
