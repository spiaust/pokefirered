@ Station index: London 0, Paris 1, Berlin 2, Oxford 3, Chantilly 4, Oranienburg 5.
Europe_Train::
	lock
	faceplayer
	special EuropeRail_LoadJourney
	goto_if_eq VAR_RESULT, TRUE, Europe_Train_Resume
	msgbox Europe_Train_Text_Destination, MSGBOX_DEFAULT
	closemessage
	multichoice 17, 1, MULTICHOICE_EUROPE_TRAIN, FALSE
	goto_if_eq VAR_RESULT, SCR_MENU_CANCEL, Europe_Train_Exit
	goto_if_eq VAR_RESULT, 6, Europe_Train_Exit
	compare VAR_0x8004, VAR_RESULT
	goto_if_eq Europe_Train_AlreadyHere
	copyvar VAR_0x8005, VAR_RESULT
	special EuropeRail_PrepareJourney
	goto_if_eq VAR_RESULT, 0xFFFF, Europe_Train_Exit
	copyvar VAR_0x8006, VAR_RESULT
	msgbox Europe_Train_Text_Preview, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Europe_Train_Exit
	goto Europe_Train_Board

Europe_Train_Resume::
	special EuropeRail_PrepareJourney
	goto_if_eq VAR_RESULT, 0xFFFF, Europe_Train_Exit
	compare VAR_RESULT, VAR_0x8004
	goto_if_eq Europe_Train_ReachedOnFoot
	copyvar VAR_0x8006, VAR_RESULT
	msgbox Europe_Train_Text_Resume, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Europe_Train_Board
	msgbox Europe_Train_Text_Cancel, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Europe_Train_Exit
	setvar VAR_EUROPE_RAIL_DESTINATION, 0
	msgbox Europe_Train_Text_Canceled
	goto Europe_Train_Exit

Europe_Train_ReachedOnFoot::
	setvar VAR_EUROPE_RAIL_DESTINATION, 0
	msgbox Europe_Train_Text_Completed
	goto Europe_Train_Exit

Europe_Train_Board::
	copyvar VAR_EUROPE_RAIL_DESTINATION, VAR_0x8005
	addvar VAR_EUROPE_RAIL_DESTINATION, 1
	compare VAR_0x8006, VAR_0x8005
	call_if_eq Europe_Train_ClearBooking
	goto_if_eq VAR_EUROPE_RAIL_DESTINATION, 0, Europe_Train_FinalBoardMessage
	msgbox Europe_Train_Text_Board
	goto Europe_Train_Depart
Europe_Train_FinalBoardMessage::
	msgbox Europe_Train_Text_FinalBoard
Europe_Train_Depart::
	closemessage
	switch VAR_0x8006
	case 0, Europe_Train_London
	case 1, Europe_Train_Paris
	case 2, Europe_Train_Berlin
	case 3, Europe_Train_Oxford
	case 4, Europe_Train_Chantilly
	case 5, Europe_Train_Oranienburg
	goto Europe_Train_Exit

Europe_Train_ClearBooking::
	setvar VAR_EUROPE_RAIL_DESTINATION, 0
	return

Europe_Train_London::
	playse SE_DING_DONG
	warp MAP_EUROPE_LONDON_STATION, 4, 7
	waitstate
	releaseall
	end

Europe_Train_Paris::
	playse SE_DING_DONG
	warp MAP_EUROPE_PARIS_STATION, 4, 7
	waitstate
	releaseall
	end

Europe_Train_Berlin::
	playse SE_DING_DONG
	warp MAP_EUROPE_BERLIN_STATION, 4, 7
	waitstate
	releaseall
	end

Europe_Train_Oxford::
	playse SE_DING_DONG
	warp MAP_EUROPE_OXFORD_STATION, 4, 7
	waitstate
	releaseall
	end

Europe_Train_Chantilly::
	playse SE_DING_DONG
	warp MAP_EUROPE_CHANTILLY_STATION, 4, 7
	waitstate
	releaseall
	end

Europe_Train_Oranienburg::
	playse SE_DING_DONG
	warp MAP_EUROPE_ORANIENBURG_STATION, 4, 7
	waitstate
	releaseall
	end

Europe_Train_AlreadyHere::
	msgbox Europe_Train_Text_AlreadyHere, MSGBOX_DEFAULT
Europe_Train_Exit::
	closemessage
	release
	end

Europe_Train_Text_Destination::
	.string "Welcome to EUROPEAN RAIL!\n"
	.string "Where would you like to travel?$"

Europe_Train_Text_Preview::
	.string "Destination: {STR_VAR_1}\nNext stop: {STR_VAR_2}\p"
	.string "Trains remaining: {STR_VAR_3}.\nBoard the next train?$"

Europe_Train_Text_Resume::
	.string "Saved trip: {STR_VAR_1}\nNext stop: {STR_VAR_2}\p"
	.string "Trains remaining: {STR_VAR_3}.\nContinue your journey?$"

Europe_Train_Text_Cancel::
	.string "Cancel your saved journey?\nChoose NO to keep it for later.$"

Europe_Train_Text_Canceled::
	.string "Your saved journey is canceled.\nTalk to me to choose another trip.$"

Europe_Train_Text_Completed::
	.string "You've reached your destination!\nYour saved journey is complete.$"

Europe_Train_Text_Board::
	.string "Next stop: {STR_VAR_2}!\p"
	.string "At intermediate stops, explore or\n"
	.string "speak to the rail clerk to continue.$"

Europe_Train_Text_FinalBoard::
	.string "All aboard!\nNext stop: {STR_VAR_2}!$"

Europe_Train_Text_AlreadyHere::
	.string "You're already at that station!$"





