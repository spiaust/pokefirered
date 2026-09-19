EuropeCalaisPort_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeCalaisPort_OnTransition
	.byte 0
EuropeCalaisPort_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_PARIS
	end

EuropeCalaisPort_RealismHall::
	msgbox EuropeCalaisPort_RealismHallText, MSGBOX_SIGN
	end

EuropeCalaisPort_RealismHallText::
	.string "CALAIS TOWN HALL / BELFRY\n"
	.string "The red-brick civic landmark.$"

EuropeCalaisPort_RealismLighthouse::
	msgbox EuropeCalaisPort_RealismLighthouseText, MSGBOX_SIGN
	end

EuropeCalaisPort_RealismLighthouseText::
	.string "CALAIS LIGHTHOUSE\n"
	.string "Above the COURGAIN MARITIME.$"

EuropeCalaisPort_RealismSeafront::
	msgbox EuropeCalaisPort_RealismSeafrontText, MSGBOX_SIGN
	end

EuropeCalaisPort_RealismSeafrontText::
	.string "CALAIS SEAFRONT\n"
	.string "The CHANNEL lies to the north.$"
