EuropeChantillyCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeChantillyCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

EuropeChantillyCenter_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	end

EuropeChantillyCenter_Nurse::
	lock
	faceplayer
	call EventScript_PkmnCenterNurse
	release
	end
