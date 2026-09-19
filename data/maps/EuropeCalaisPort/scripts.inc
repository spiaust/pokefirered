EuropeCalaisPort_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeCalaisPort_OnTransition
	.byte 0
EuropeCalaisPort_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_PARIS
	end
