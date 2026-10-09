EuropeAmiensNews_Porter::
	goto_if_eq VAR_EUROPE_AMIENS_NEWS, 4, EuropeAmiensNews_Done
	goto_if_eq VAR_EUROPE_AMIENS_NEWS, 3, EuropeAmiensNews_Checked
	goto_if_eq VAR_EUROPE_AMIENS_NEWS, 2, EuropeAmiensNews_Check
	goto_if_eq VAR_EUROPE_AMIENS_NEWS, 1, EuropeAmiensNews_Reminder
	msgbox EuropeAmiensNews_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiensNews_Decline
	setvar VAR_EUROPE_AMIENS_NEWS, 1
EuropeAmiensNews_Reminder::
	msgbox EuropeAmiensNews_Text_Reminder
	goto EuropeCelebi_End
EuropeAmiensNews_Decline::
	msgbox EuropeAmiensNews_Text_Decline
	goto EuropeCelebi_End
EuropeAmiensNews_Check::
	msgbox EuropeAmiensNews_Text_Check
	setvar VAR_EUROPE_AMIENS_NEWS, 3
EuropeAmiensNews_Checked::
	msgbox EuropeAmiensNews_Text_Checked
	goto EuropeCelebi_End
EuropeAmiensNews_Done::
	goto EuropeRouen_Offer
EuropeAmiensNews_Board::
	goto_if_eq VAR_EUROPE_AMIENS_NEWS, 4, EuropeRouen_DepartureNotice
	msgbox EuropeAmiensNews_Text_Board
	goto_if_ne VAR_EUROPE_AMIENS_NEWS, 1, EuropeAmiens_NoticeEnd
	setvar VAR_EUROPE_AMIENS_NEWS, 2
	msgbox EuropeAmiensNews_Text_Noted
	goto EuropeAmiens_NoticeEnd
EuropeAmiensNews_Deliver::
	msgbox EuropeAmiensNews_Text_Deliver
	setvar VAR_EUROPE_AMIENS_NEWS, 4
	goto EuropeReunion_Done
EuropeAmiensNews_Text_Offer::
	.string "There is a new travel bulletin.\n"
	.string "NORA needs the checked instructions.\p"
	.string "Will you copy the northeast notice\n"
	.string "and check it with me first?$"
EuropeAmiensNews_Text_Reminder::
	.string "Read the northeast noticeboard.\n"
	.string "Bring the exact instructions here.$"
EuropeAmiensNews_Text_Decline::
	.string "All right. I will be here\n"
	.string "when you are ready.$"
EuropeAmiensNews_Text_Board::
	.string "AMIENS TRAVEL BULLETIN\p"
	.string "No onward service is confirmed yet.\n"
	.string "Wait in the reception courtyard.\p"
	.string "Keep people and POKEMON together.\n"
	.string "NORA will call each group in turn.\p"
	.string "The return service remains open.$"
EuropeAmiensNews_Text_Noted::
	.string "You copy the waiting instructions.\n"
	.string "Check them with the porter.$"
EuropeAmiensNews_Text_Check::
	.string "That is the current bulletin.\n"
	.string "No departure time is promised.\p"
	.string "Please tell NORA to keep groups\n"
	.string "together here until they are called.$"
EuropeAmiensNews_Text_Checked::
	.string "Take the checked news to NORA\n"
	.string "beside the west courtyard path.$"
EuropeAmiensNews_Text_Deliver::
	.string "NORA: Thank you for checking.\n"
	.string "I will keep the groups together.\p"
	.string "MIRA and MEOWTH can wait here\n"
	.string "without risking another separation.\p"
	.string "Our return guide is still available.\n"
	.string "Your team can rest while we wait.$"
EuropeAmiensNews_Text_Done::
	.string "NORA has the confirmed instructions.\n"
	.string "We will wait for reliable news.$"
