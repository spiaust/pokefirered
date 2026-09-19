EuropeOranienburgCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeOranienburgCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

EuropeOranienburgCenter_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_ORANIENBURG
	end

EuropeOranienburgCenter_Nurse::
	lock
	faceplayer
	call EventScript_PkmnCenterNurse
	release
	end
