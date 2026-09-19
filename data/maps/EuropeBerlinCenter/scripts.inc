EuropeBerlinCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeBerlinCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

EuropeBerlinCenter_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_BERLIN
	end

EuropeBerlinCenter_Nurse::
	lock
	faceplayer
	call EventScript_PkmnCenterNurse
	release
	end
