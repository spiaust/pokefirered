EuropeEvac_Board::
	msgbox EuropeEvac_Text_Board, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeEvac_Decline
	msgbox EuropeEvac_Text_Journey
	compare VAR_EUROPE_EVAC_STORY, 0
	call_if_eq EuropeEvac_FirstTrip
	closemessage
	warp MAP_EUROPE_BEAUVAIS_PAST, 4, 7
	waitstate
	releaseall
	end
EuropeEvac_FirstTrip::
	setvar VAR_EUROPE_EVAC_STORY, 1
	return
EuropeEvac_Decline::
	msgbox EuropeEvac_Text_Decline
	releaseall
	end
EuropeEvac_Host::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_EVAC_STORY, 2, EuropeEvac_HostDone
	msgbox EuropeEvac_Text_Welcome
	setvar VAR_EUROPE_EVAC_STORY, 2
EuropeEvac_HostDone::
	goto_if_eq VAR_EUROPE_MESSAGE_STORY, 4, EuropeRelief_Host
	msgbox EuropeEvac_Text_HostDone
	goto EuropeCelebi_End
EuropeEvac_Elise::
	lock
	faceplayer
	goto_if_ne VAR_EUROPE_EVAC_STORY, 2, EuropeEvac_CheckIn
	msgbox EuropeEvac_Text_Elise
	showmonpic SPECIES_EEVEE, 10, 3
	waitbuttonpress
	hidemonpic
	goto EuropeMessage_Offer
EuropeEvac_CheckIn::
	msgbox EuropeEvac_Text_CheckIn
	goto EuropeCelebi_End
EuropeEvac_Refuge::
	goto_if_eq VAR_EUROPE_MESSAGE_STORY, 1, EuropeMessage_Deliver
	goto_if_ge VAR_EUROPE_MESSAGE_STORY, 2, EuropeMessage_KeeperDone
	msgbox EuropeEvac_Text_Refuge
	goto EuropeCelebi_End
EuropeEvac_Ada::
	goto_if_ge VAR_EUROPE_MESSAGE_STORY, 3, EuropeMessage_Ada
	msgbox EuropeEvac_Text_Ada
	goto EuropeCelebi_End
EuropeEvac_Text_Board::
	.string "DEPARTURE: BEAUVAIS RECEPTION\n"
	.string "Families and POKEMON may board.\p"
	.string "CELEBI can bring you home from there.\n"
	.string "Board the train to BEAUVAIS?$"
EuropeEvac_Text_Journey::
	.string "You join the train to BEAUVAIS.\n"
	.string "ELISE and EEVEE have a place there.\p"
	.string "Fields pass beyond the windows.\n"
	.string "A host welcomes you at the next stop.$"
EuropeEvac_Text_Decline::
	.string "You stay at the station post.\n"
	.string "Read the board when you're ready.$"
EuropeEvac_Text_Welcome::
	.string "Welcome to BEAUVAIS reception.\n"
	.string "I'll record ELISE and EEVEE together.\p"
	.string "They have a warm place to rest.\n"
	.string "Thank you for seeing them here.$"
EuropeEvac_Text_HostDone::
	.string "ELISE and EEVEE are checked in.\n"
	.string "Speak to them before you leave.\p"
	.string "The south exit takes the return\n"
	.string "service to the CHANTILLY post.\p"
	.string "CELEBI by the entrance can take\n"
	.string "you directly to the present.$"
EuropeEvac_Text_CheckIn::
	.string "ELISE: We made it! Please speak\n"
	.string "to the host at the back to check in.$"
EuropeEvac_Text_Elise::
	.string "ELISE: EEVEE is warm and resting.\n"
	.string "We have a place together tonight.\p"
	.string "Thank you for staying with us.\n"
	.string "I'll remember your kindness.$"
EuropeEvac_Text_Refuge::
	.string "ELISE and EEVEE left for BEAUVAIS.\n"
	.string "You can visit via the station post.\p"
	.string "Thank you for helping them travel\n"
	.string "together. CELEBI is waiting for you.$"
EuropeEvac_Text_Ada::
	.string "ADA: ELISE and EEVEE found shelter.\n"
	.string "You helped them stay together.\p"
	.string "There are more stories in the past.\n"
	.string "For now, come home and rest.$"
