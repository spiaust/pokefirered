EuropeParisCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeParisCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

EuropeParisCenter_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_PARIS
	end

EuropeParisCenter_Nurse::
	lock
	faceplayer
	call EventScript_PkmnCenterNurse
	release
	end
