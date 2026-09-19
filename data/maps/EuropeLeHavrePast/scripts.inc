EuropeLeHavrePast_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeLeHavre_Transition
	map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, EuropeDockCheck_Restore
	.byte 0
EuropeLeHavre_Transition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	goto EuropeDockCheck_Restore
EuropeLeHavre_Clerk::
	lock
	faceplayer
	goto_if_ne VAR_EUROPE_ROUEN_BOOK, 3, EuropeLeHavre_Locked
	msgbox EuropeLeHavre_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiens_Stay
	msgbox EuropeLeHavre_Text_Journey
	compare VAR_EUROPE_LE_HAVRE_STORY, 0
	call_if_eq EuropeLeHavre_FirstVisit
	closemessage
	warp MAP_EUROPE_LE_HAVRE_PAST, 8, 5
	waitstate
	releaseall
	end
EuropeLeHavre_FirstVisit::
	setvar VAR_EUROPE_LE_HAVRE_STORY, 1
	return
EuropeLeHavre_Locked::
	msgbox EuropeLeHavre_Text_Locked
	goto EuropeCelebi_End
EuropeLeHavre_Captain::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_DOCK_CHECK, 2, EuropeDockCheck_Confirm
	goto_if_eq VAR_EUROPE_LE_HAVRE_STORY, 2, EuropeLeHavre_Return
	msgbox EuropeLeHavre_Text_Welcome
	setvar VAR_EUROPE_LE_HAVRE_STORY, 2
EuropeLeHavre_Return::
	msgbox EuropeLeHavre_Text_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiens_Stay
	closemessage
	warp MAP_EUROPE_ROUEN_PAST, 10, 16
	waitstate
	releaseall
	end
EuropeLeHavre_Text_Locked::
	.string "LEON needs the reception route book\n"
	.string "before I can arrange onward travel.\p"
	.string "Please speak to him on the west path.$"
EuropeLeHavre_Text_Offer::
	.string "The route book is back with LEON.\n"
	.string "A connection to LE HAVRE is ready.\p"
	.string "The port captain can bring you back.\n"
	.string "There is no charge for the journey.\p"
	.string "Travel to LE HAVRE?$"
EuropeLeHavre_Text_Journey::
	.string "You join the onward transport.\n"
	.string "The countryside gives way to docks.\p"
	.string "At LE HAVRE, a captain welcomes\n"
	.string "travelers beside the waiting boat.$"
EuropeLeHavre_Text_Welcome::
	.string "Welcome to LE HAVRE reception.\n"
	.string "You came from LEON in ROUEN?\p"
	.string "Your arrival is recorded. Wait here\n"
	.string "with your traveling companions.\p"
	.string "I can arrange a return to ROUEN.\n"
	.string "Your green friend knows another way.$"
EuropeLeHavre_Text_Return::
	.string "The return service to ROUEN is open.\n"
	.string "LEON can help your team rest there.\p"
	.string "Return to ROUEN?$"
