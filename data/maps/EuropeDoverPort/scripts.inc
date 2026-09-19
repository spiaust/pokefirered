EuropeDoverPort_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeDoverPort_OnTransition
	.byte 0
EuropeDoverPort_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_LONDON
	end
