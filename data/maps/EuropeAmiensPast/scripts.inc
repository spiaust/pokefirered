EuropeAmiensPast_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeAmiens_OnTransition
	map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, EuropeReunion_Restore
	.byte 0
EuropeAmiens_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	goto EuropeReunion_Restore
EuropeAmiens_Offer::
	msgbox EuropeAmiens_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiens_Stay
	msgbox EuropeAmiens_Text_Journey
	compare VAR_EUROPE_AMIENS_STORY, 0
	call_if_eq EuropeAmiens_FirstVisit
	closemessage
	warp MAP_EUROPE_AMIENS_PAST, 10, 16
	waitstate
	releaseall
	end
EuropeAmiens_FirstVisit::
	setvar VAR_EUROPE_AMIENS_STORY, 1
	return
EuropeAmiens_Stay::
	msgbox EuropeAmiens_Text_Stay
	goto EuropeCelebi_End
EuropeAmiens_Return::
	lock
	faceplayer
	msgbox EuropeAmiens_Text_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiens_Stay
	closemessage
	warp MAP_EUROPE_CHANTILLY_PAST_POST, 5, 10
	waitstate
	releaseall
	end
EuropeAmiens_Nora::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_AMIENS_STORY, 4, EuropeReunion_Nora
	goto_if_eq VAR_EUROPE_AMIENS_STORY, 3, EuropeAmiens_Confirm
	goto_if_eq VAR_EUROPE_AMIENS_STORY, 2, EuropeAmiens_Reminder
	msgbox EuropeAmiens_Text_Welcome
	setvar VAR_EUROPE_AMIENS_STORY, 2
EuropeAmiens_Reminder::
	msgbox EuropeAmiens_Text_Reminder
	goto EuropeCelebi_End
EuropeAmiens_Notice::
	lockall
	goto_if_ge VAR_EUROPE_AMIENS_NEWS, 1, EuropeAmiensNews_Board
	msgbox EuropeAmiens_Text_Notice
	goto_if_ne VAR_EUROPE_AMIENS_STORY, 2, EuropeAmiens_NoticeEnd
	setvar VAR_EUROPE_AMIENS_STORY, 3
	msgbox EuropeAmiens_Text_Noted
EuropeAmiens_NoticeEnd::
	releaseall
	end
EuropeAmiens_Confirm::
	msgbox EuropeAmiens_Text_Confirm
	setvar VAR_EUROPE_AMIENS_STORY, 4
EuropeAmiens_Done::
	msgbox EuropeAmiens_Text_Done
	goto EuropeCelebi_End

EuropeAmiens_Text_Offer::
	.string "An onward train is ready for AMIENS.\n"
	.string "NORA is welcoming travelers there.\p"
	.string "A guide can bring you back here.\n"
	.string "CELEBI will wait near your arrival.\p"
	.string "Would you like to board?$"
EuropeAmiens_Text_Journey::
	.string "The train carries you to AMIENS.\n"
	.string "You step into a reception courtyard.\p"
	.string "Travelers wait beside a noticeboard.\n"
	.string "A volunteer waves you over.$"
EuropeAmiens_Text_Stay::
	.string "You stay where you are.\n"
	.string "Ask again when you are ready.$"
EuropeAmiens_Text_Return::
	.string "I can take you back to the\n"
	.string "CHANTILLY station post.\p"
	.string "Take the return service?$"
EuropeAmiens_Text_Welcome::
	.string "NORA: Welcome to AMIENS. We help\n"
	.string "travelers find a place to wait.\p"
	.string "People and POKEMON need clear\n"
	.string "meeting points after a journey.\p"
	.string "Please read our northeast notice,\n"
	.string "then come back and check it with me.$"
EuropeAmiens_Text_Reminder::
	.string "NORA: The board is beside the\n"
	.string "northeast trees. Read it, then return.\p"
	.string "If you need to leave, the guide and\n"
	.string "CELEBI wait near the south path.$"
EuropeAmiens_Text_Notice::
	.string "AMIENS RECEPTION - 1940\p"
	.string "Wait in the courtyard with your\n"
	.string "traveling companions and POKEMON.\p"
	.string "If you are separated, tell NORA.\n"
	.string "She records names by the west path.\p"
	.string "Ask before leaving to search alone.$"
EuropeAmiens_Text_Noted::
	.string "You copy the meeting instructions.\n"
	.string "Return to NORA to confirm them.$"
EuropeAmiens_Text_Confirm::
	.string "NORA: That's right. Wait together,\n"
	.string "and tell me if someone is missing.\p"
	.string "Thank you for checking the notice.\n"
	.string "Now you know where to find help.$"
EuropeAmiens_Text_Done::
	.string "NORA: Your arrival is recorded.\n"
	.string "Rest here with your team a while.\p"
	.string "The guide can return you to the post.\n"
	.string "Your green friend knows another way.$"
