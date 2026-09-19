EuropeOxfordCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeOxfordCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

EuropeOxfordCenter_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_OXFORD
	end

EuropeOxfordCenter_Nurse::
	lock
	faceplayer
	call EventScript_PkmnCenterNurse
	release
	end
