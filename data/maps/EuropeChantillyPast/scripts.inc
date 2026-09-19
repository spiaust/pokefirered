EuropeChantillyPast_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeChantillyPast_OnTransition
	map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, EuropeChantillyPast_RestoreGuide
	.byte 0
EuropeChantillyPast_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	goto_if_ge VAR_EUROPE_EVAC_STORY, 1, EuropeChantillyPast_EliseAway
	end
EuropeChantillyPast_RestoreGuide::
	addobject 4
	goto_if_ge VAR_EUROPE_EVAC_STORY, 1, EuropeChantillyPast_EliseAway
	end
EuropeChantillyPast_EliseAway::
	setflag FLAG_TEMP_1
	removeobject 2
	end

EuropeChantillyPast_RealismChateau::
	msgbox EuropeChantillyPast_RealismChateauText, MSGBOX_SIGN
	end

EuropeChantillyPast_RealismChateauText::
	.string "CHATEAU DE CHANTILLY - 1940\n"
	.string "The moat surrounds the chateau.$"

EuropeChantillyPast_RealismStables::
	msgbox EuropeChantillyPast_RealismStablesText, MSGBOX_SIGN
	end

EuropeChantillyPast_RealismStablesText::
	.string "GRANDES ECURIES\n"
	.string "The Great Stables face the lawns.$"

EuropeChantillyPast_RealismPelouse::
	msgbox EuropeChantillyPast_RealismPelouseText, MSGBOX_SIGN
	end

EuropeChantillyPast_RealismPelouseText::
	.string "GRANDE PELOUSE\n"
	.string "Return west to the refuge.$"
