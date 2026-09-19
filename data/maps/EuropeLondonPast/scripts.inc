EuropeLondonPast_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeLondonPast_Transition
	.byte 0
EuropeLondonPast_Transition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	end
EuropeLondonPast_Clerk::
	lock
	faceplayer
	goto_if_ne VAR_EUROPE_SOUTH_ACCOUNT, 1, EuropeLondonPast_Locked
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
	.string "Before traveling farther, tell ADA\n"
	.string "about SOUTHAMPTON reception.\p"
	.string "Your green friend can take you back\n"
	.string "to the present.$"
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
	.string "ROSE: Welcome to LONDON reception.\n"
	.string "You came from SOUTHAMPTON?\p"
	.string "Your arrival is recorded. Stay in\n"
	.string "the courtyard while we get ready.\p"
	.string "The guide can arrange your return.\n"
	.string "Your green friend is waiting too.$"
EuropeLondonPast_Text_Welcomed::
	.string "ROSE: Take your time here.\n"
	.string "Your group can wait together.\p"
	.string "The guide returns to SOUTHAMPTON.\n"
	.string "Your green friend knows another way.$"
EuropeLondonPast_Text_Return::
	.string "Return to SOUTHAMPTON reception?\n"
	.string "The worker there offers party care.$"
EuropeLondonPast_Text_Sign::
	.string "LONDON RECEPTION COURTYARD\p"
	.string "Please speak to ROSE on the left.\n"
	.string "Wait here with your companions.$"
