EuropeLondonPast_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeLondonPast_Transition
	.byte 0
EuropeLondonPast_Transition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	end
EuropeLondonPast_Clerk::
	lock
	faceplayer
	goto_if_ne VAR_EUROPE_LUGGAGE, 3, EuropeLondonPast_Locked
	msgbox EuropeLondonPast_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiens_Stay
	msgbox EuropeLondonPast_Text_Journey
	compare VAR_EUROPE_LONDON_PAST, 0
	call_if_eq EuropeLondonPast_First
	closemessage
	warp MAP_EUROPE_LONDON_PAST, 10, 16
	waitstate
	releaseall
	end
EuropeLondonPast_First::
	setvar VAR_EUROPE_LONDON_PAST, 1
	return
EuropeLondonPast_Locked::
	msgbox EuropeLondonPast_Text_Locked
	goto EuropeCelebi_End
EuropeLondonPast_Rose::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_LONDON_PAST, 2, EuropeLondonPast_Welcomed
	msgbox EuropeLondonPast_Text_Welcome
	setvar VAR_EUROPE_LONDON_PAST, 2
	goto EuropeCelebi_End
EuropeLondonPast_Welcomed::
	msgbox EuropeLondonPast_Text_Welcomed
	goto EuropeCelebi_End
EuropeLondonPast_Return::
	lock
	faceplayer
	msgbox EuropeLondonPast_Text_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiens_Stay
	closemessage
	warp MAP_EUROPE_SOUTHAMPTON_PAST, 8, 5
	waitstate
	releaseall
	end
EuropeLondonPast_Sign::
	msgbox EuropeLondonPast_Text_Sign, MSGBOX_SIGN
	end
EuropeLondonPast_Text_Locked::
	.string "We are waiting for the missing\n"
	.string "luggage to be returned. Speak to\p"
	.string "the reception worker and help the\n"
	.string "group get ready before we leave.$"
EuropeLondonPast_Text_Offer::
	.string "Transport to LONDON is ready.\n"
	.string "ROSE will welcome you at reception.\p"
	.string "The guide there can bring you back.\n"
	.string "Travel to LONDON? There is no charge.$"
EuropeLondonPast_Text_Journey::
	.string "You join the onward transport.\n"
	.string "The port gives way to inland roads.\p"
	.string "At LONDON, the group gathers\n"
	.string "in a quiet reception courtyard.$"
EuropeLondonPast_Text_Welcome::
	.string "ROSE: Welcome. Your companions can\n"
	.string "rest together here. From CHANTILLY\p"
	.string "to SOUTHAMPTON, people kept this\n"
	.string "route open through small acts of\p"
	.string "care. You helped that chain hold.\n"
	.string "Tell ADA what you learned when you\p"
	.string "return.$"
EuropeLondonPast_Text_Welcomed::
	.string "ROSE: This part of the journey is\n"
	.string "complete. Rest, explore, or visit\p"
	.string "the friends you helped. The guide\n"
	.string "returns to SOUTHAMPTON. CELEBI\p"
	.string "will take you home to ADA.$"
EuropeLondonPast_Text_Return::
	.string "Return to SOUTHAMPTON reception?\n"
	.string "The worker there offers party care.$"
EuropeLondonPast_Text_Sign::
	.string "LONDON RECEPTION COURTYARD\p"
	.string "Please speak to ROSE on the left.\n"
	.string "Wait here with your companions.$"

EuropeLondonPast_RealismPalace::
	msgbox EuropeLondonPast_RealismPalaceText, MSGBOX_SIGN
	end

EuropeLondonPast_RealismPalaceText::
	.string "PALACE OF WESTMINSTER\n"
	.string "The clock tower beside the THAMES.$"

EuropeLondonPast_RealismSquare::
	msgbox EuropeLondonPast_RealismSquareText, MSGBOX_SIGN
	end

EuropeLondonPast_RealismSquareText::
	.string "PARLIAMENT SQUARE\n"
	.string "WHITEHALL leads north from here.$"

EuropeLondonPast_RealismWestminster::
	msgbox EuropeLondonPast_RealismWestminsterText, MSGBOX_SIGN
	end

EuropeLondonPast_RealismWestminsterText::
	.string "WESTMINSTER BRIDGE\n"
	.string "Cross the THAMES by Parliament.$"

EuropeLondonPast_RealismLambeth::
	msgbox EuropeLondonPast_RealismLambethText, MSGBOX_SIGN
	end

EuropeLondonPast_RealismLambethText::
	.string "LAMBETH BRIDGE\n"
	.string "The southern river crossing.$"
