EuropeDoverPort_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeDoverPort_OnTransition
	.byte 0
EuropeDoverPort_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_LONDON
	end

EuropeDoverPort_RealismCastle::
	msgbox EuropeDoverPort_RealismCastleText, MSGBOX_SIGN
	end

EuropeDoverPort_RealismCastleText::
	.string "DOVER CASTLE\n"
	.string "The Great Tower above the harbor.$"

EuropeDoverPort_RealismCliffs::
	msgbox EuropeDoverPort_RealismCliffsText, MSGBOX_SIGN
	end

EuropeDoverPort_RealismCliffsText::
	.string "WHITE CLIFFS OF DOVER\n"
	.string "Chalk cliffs above the CHANNEL.$"

EuropeDoverPort_RealismHarbor::
	msgbox EuropeDoverPort_RealismHarborText, MSGBOX_SIGN
	end

EuropeDoverPort_RealismHarborText::
	.string "DOVER SEAFRONT\n"
	.string "Follow the quay to the ferry.$"
