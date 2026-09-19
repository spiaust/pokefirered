EuropeLondonCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeLondonCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

EuropeLondonCenter_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_LONDON
	end

EuropeLondonCenter_Nurse::
	lock
	faceplayer
	call EventScript_PkmnCenterNurse
	release
	end
