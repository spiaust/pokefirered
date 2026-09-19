EuropeChantillyPastPost_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeChantillyPastPost_OnTransition
	.byte 0
EuropeChantillyPastPost_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	end

EuropeChantillyPastPost_RealismStation::
	msgbox EuropeChantillyPastPost_RealismStationText, MSGBOX_SIGN
	end

EuropeChantillyPastPost_RealismStationText::
	.string "CHANTILLY STATION - 1940\n"
	.string "The notice handles onward travel.$"

EuropeChantillyPastPost_RealismPlatform::
	msgbox EuropeChantillyPastPost_RealismPlatformText, MSGBOX_SIGN
	end

EuropeChantillyPastPost_RealismPlatformText::
	.string "STATION FORECOURT\n"
	.string "The dispatcher waits to the west.$"

EuropeChantillyPastPost_RealismReturn::
	msgbox EuropeChantillyPastPost_RealismReturnText, MSGBOX_SIGN
	end

EuropeChantillyPastPost_RealismReturnText::
	.string "STATION APPROACH\n"
	.string "Return west for the refuge guide.$"
