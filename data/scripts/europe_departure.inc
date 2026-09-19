@ Departure news: read the notice, verify it, and deliver it to the refuge.
EuropeDeparture_Guide::
	lock
	faceplayer
	goto_if_ne VAR_EUROPE_PAST_STORY, 4, EuropeDeparture_NotReady
	msgbox EuropeDeparture_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeTime_Stay
	compare VAR_EUROPE_DEPARTURE_STORY, 0
	call_if_eq EuropeDeparture_Start
	msgbox EuropeDeparture_Text_Walk
	closemessage
	warp MAP_EUROPE_CHANTILLY_PAST_POST, 5, 10
	waitstate
	releaseall
	end
EuropeDeparture_Start::
	setvar VAR_EUROPE_DEPARTURE_STORY, 1
	return
EuropeDeparture_NotReady::
	msgbox EuropeDeparture_Text_NotReady
	goto EuropeCelebi_End
EuropeDeparture_ReturnGuide::
	lock
	faceplayer
	msgbox EuropeDeparture_Text_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeTime_Stay
	msgbox EuropeDeparture_Text_Walk
	closemessage
	warp MAP_EUROPE_CHANTILLY_PAST, 12, 9
	waitstate
	releaseall
	end
EuropeDeparture_Notice::
	lockall
	goto_if_eq VAR_EUROPE_DEPARTURE_STORY, 4, EuropeEvac_Board
	msgbox EuropeDeparture_Text_Notice
	goto_if_ne VAR_EUROPE_DEPARTURE_STORY, 1, EuropeDeparture_NoticeEnd
	setvar VAR_EUROPE_DEPARTURE_STORY, 2
	msgbox EuropeDeparture_Text_Noted
EuropeDeparture_NoticeEnd::
	releaseall
	end
EuropeDeparture_Dispatcher::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_DEPARTURE_STORY, 4, EuropeDeparture_DispatcherDone
	goto_if_eq VAR_EUROPE_DEPARTURE_STORY, 3, EuropeDeparture_Carry
	goto_if_ne VAR_EUROPE_DEPARTURE_STORY, 2, EuropeDeparture_ReadFirst
	msgbox EuropeDeparture_Text_Confirm
	setvar VAR_EUROPE_DEPARTURE_STORY, 3
EuropeDeparture_Carry::
	msgbox EuropeDeparture_Text_Carry
	goto EuropeCelebi_End
EuropeDeparture_ReadFirst::
	msgbox EuropeDeparture_Text_ReadFirst
	goto EuropeCelebi_End
EuropeDeparture_DispatcherDone::
	goto_if_ge VAR_EUROPE_RELIEF_STORY, 1, EuropeRelief_Dispatcher
	msgbox EuropeDeparture_Text_DispatcherDone
	goto EuropeCelebi_End
EuropeDeparture_Report::
	msgbox EuropeDeparture_Text_Report
	setvar VAR_EUROPE_DEPARTURE_STORY, 4
EuropeDeparture_RefugeDone::
	goto_if_ge VAR_EUROPE_EVAC_STORY, 1, EuropeEvac_Refuge
	msgbox EuropeDeparture_Text_RefugeDone
	goto EuropeCelebi_End
EuropeDeparture_ChildDone::
	msgbox EuropeDeparture_Text_ChildDone
	goto EuropeCelebi_End
EuropeDeparture_AdaDone::
	goto_if_eq VAR_EUROPE_EVAC_STORY, 2, EuropeEvac_Ada
	msgbox EuropeDeparture_Text_AdaDone
	goto EuropeCelebi_End

EuropeDeparture_Text_NotReady::
	.string "The keeper is helping that child.\n"
	.string "Please see what they need first.$"
EuropeDeparture_Text_Offer::
	.string "I can guide you to the station post.\n"
	.string "The keeper needs departure news.\p"
	.string "Read the notice there, then ask the\n"
	.string "dispatcher to confirm its message.\p"
	.string "CELEBI will follow and wait nearby.\n"
	.string "Visit the station post?$"
EuropeDeparture_Text_Walk::
	.string "The guide leads you along the path.$"
EuropeDeparture_Text_Return::
	.string "The refuge is a short walk away.\n"
	.string "Return there with me?$"
EuropeDeparture_Text_Notice::
	.string "STATION POST - 1940\p"
	.string "Families: wait at the refuge.\n"
	.string "Keep people and POKEMON together.\p"
	.string "Ask the dispatcher for the latest\n"
	.string "news before moving to a platform.$"
EuropeDeparture_Text_Noted::
	.string "You copy the instructions.\n"
	.string "Now check with the dispatcher.$"
EuropeDeparture_Text_ReadFirst::
	.string "Please read the notice northeast\n"
	.string "of me. Then we can check your notes.$"
EuropeDeparture_Text_Confirm::
	.string "Those instructions are still right.\n"
	.string "A departure time is not confirmed.\p"
	.string "Tell the keeper to keep everyone\n"
	.string "together inside the refuge.\p"
	.string "I'll send a guide when we have news.\n"
	.string "Nobody should wait alone outside.$"
EuropeDeparture_Text_Carry::
	.string "Please take that message back\n"
	.string "to the keeper at the refuge.$"
EuropeDeparture_Text_DispatcherDone::
	.string "A train to BEAUVAIS is now ready.\n"
	.string "Read the board to join the journey.$"
EuropeDeparture_Text_Report::
	.string "No departure yet? Thank you for\n"
	.string "asking instead of trusting rumors.\p"
	.string "I'll gather everyone here and wait\n"
	.string "for the station guide's message.$"
EuropeDeparture_Text_RefugeDone::
	.string "ELISE and EEVEE can stay together.\n"
	.string "We know where to wait safely now.\p"
	.string "Your green friend is waiting too.\n"
	.string "Go home whenever you need to.$"
EuropeDeparture_Text_ChildDone::
	.string "ELISE: The keeper told me your news.\n"
	.string "We'll wait here together.\p"
	.string "EEVEE is resting in its blanket.\n"
	.string "Thank you for coming back for us.$"
EuropeDeparture_Text_AdaDone::
	.string "ADA: You brought them clear news\n"
	.string "when everything felt uncertain.\p"
	.string "A small act can mean a great deal.\n"
	.string "CELEBI still knows the way to them.$"
