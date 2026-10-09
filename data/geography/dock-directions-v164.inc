EuropeDockCheck_Restore::
	addobject 5
	addobject 4
	end
EuropeDockCheck_Worker::
	lock
	faceplayer
	goto_if_ne VAR_EUROPE_LE_HAVRE_STORY, 2, EuropeDockCheck_Locked
	goto_if_eq VAR_EUROPE_DOCK_CHECK, 3, EuropeDockCheck_Done
	goto_if_eq VAR_EUROPE_DOCK_CHECK, 2, EuropeDockCheck_Ready
	goto_if_eq VAR_EUROPE_DOCK_CHECK, 1, EuropeDockCheck_Reminder
	msgbox EuropeDockCheck_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeDockCheck_Decline
	setvar VAR_EUROPE_DOCK_CHECK, 1
EuropeDockCheck_Reminder::
	msgbox EuropeDockCheck_Text_Reminder
	goto EuropeCelebi_End
EuropeDockCheck_Locked::
	msgbox EuropeDockCheck_Text_Locked
	goto EuropeCelebi_End
EuropeDockCheck_Decline::
	msgbox EuropeDockCheck_Text_Decline
	goto EuropeCelebi_End
EuropeDockCheck_Ready::
	msgbox EuropeDockCheck_Text_Ready
	goto EuropeCelebi_End
EuropeDockCheck_Done::
	msgbox EuropeDockCheck_Text_Rest, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeDockCheck_NotNow
	closemessage
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox EuropeDockCheck_Text_Healed
	goto EuropeCelebi_End
EuropeDockCheck_NotNow::
	msgbox EuropeDockCheck_Text_NotNow
	goto EuropeCelebi_End
EuropeDockCheck_Notice::
	lockall
	msgbox EuropeDockCheck_Text_Notice
	goto_if_ne VAR_EUROPE_DOCK_CHECK, 1, EuropeAmiens_NoticeEnd
	setvar VAR_EUROPE_DOCK_CHECK, 2
	msgbox EuropeDockCheck_Text_Ready
	goto EuropeAmiens_NoticeEnd
EuropeDockCheck_Confirm::
	msgbox EuropeDockCheck_Text_Confirm
	setvar VAR_EUROPE_DOCK_CHECK, 3
	msgbox EuropeDockCheck_Text_Unlocked
	goto EuropeLeHavre_Return
EuropeDockCheck_Text_Locked::
	.string "Please report to the captain first.\n"
	.string "He is waiting below the pier.$"
EuropeDockCheck_Text_Offer::
	.string "The entrance is closed, but a notice\n"
	.string "is posted beside its door.\p"
	.string "Will you read the instructions\n"
	.string "and check them with the captain?$"
EuropeDockCheck_Text_Reminder::
	.string "Read the notice at the closed door.\n"
	.string "Then speak to the captain below.$"
EuropeDockCheck_Text_Decline::
	.string "All right. Ask again if you\n"
	.string "have time to help.$"
EuropeDockCheck_Text_Notice::
	.string "PORT RECEPTION INSTRUCTIONS\p"
	.string "Keep your traveling group together.\n"
	.string "Wait until the captain calls you.\p"
	.string "Keep the gangway clear. Do not\n"
	.string "board the waiting boat on your own.\p"
	.string "The ROUEN return service stays open.$"
EuropeDockCheck_Text_Ready::
	.string "Check the instructions with the\n"
	.string "captain below the pier.$"
EuropeDockCheck_Text_Confirm::
	.string "That's correct. I will call groups\n"
	.string "when it is time to move.\p"
	.string "Thank you for checking the notice.\n"
	.string "Your companions can wait together.\p"
	.string "I can still arrange your return\n"
	.string "to ROUEN whenever you need.$"
EuropeDockCheck_Text_Unlocked::
	.string "The dockworker can help your team\n"
	.string "rest while you wait.\p"
	.string "Speak to him for free party care.$"
EuropeDockCheck_Text_Rest::
	.string "Thank you for checking the notice.\n"
	.string "We have a quiet spot for your team.\p"
	.string "Let your POKEMON rest here?\n"
	.string "There is no charge.$"
EuropeDockCheck_Text_Healed::
	.string "Your POKEMON are fully rested.\p"
	.string "Take your time. The captain can\n"
	.string "arrange your return when you wish.$"
EuropeDockCheck_Text_NotNow::
	.string "Of course. Come back whenever\n"
	.string "your team needs a rest.$"
