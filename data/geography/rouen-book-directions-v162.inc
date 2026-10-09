EuropeRouenBook_Restore::
	addobject 5
	goto_if_eq VAR_EUROPE_ROUEN_BOOK, 1, EuropeRouenBook_Show
	setflag FLAG_TEMP_5
	removeobject 4
	end
EuropeRouenBook_Show::
	clearflag FLAG_TEMP_5
	addobject 4
	end
EuropeRouenBook_Leon::
	goto_if_eq VAR_EUROPE_ROUEN_BOOK, 3, EuropeRouenBook_Done
	goto_if_eq VAR_EUROPE_ROUEN_BOOK, 2, EuropeRouenBook_Return
	goto_if_eq VAR_EUROPE_ROUEN_BOOK, 1, EuropeRouenBook_Reminder
	msgbox EuropeRouenBook_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeRouenBook_Decline
	setvar VAR_EUROPE_ROUEN_BOOK, 1
	clearflag FLAG_TEMP_5
	addobject 4
EuropeRouenBook_Reminder::
	msgbox EuropeRouenBook_Text_Reminder
	goto EuropeCelebi_End
EuropeRouenBook_Decline::
	msgbox EuropeRouenBook_Text_Decline
	goto EuropeCelebi_End
EuropeRouenBook_Return::
	msgbox EuropeRouenBook_Text_Return
	setvar VAR_EUROPE_ROUEN_BOOK, 3
	msgbox EuropeRouenBook_Text_Unlocked
	goto EuropeCelebi_End
EuropeRouenBook_Done::
	msgbox EuropeRouenBook_Text_Rest, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeRouenBook_NotNow
	closemessage
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox EuropeRouenBook_Text_Healed
	goto EuropeCelebi_End
EuropeRouenBook_NotNow::
	msgbox EuropeRouenBook_Text_NotNow
	goto EuropeCelebi_End
EuropeRouenBook_Pickup::
	lock
	faceplayer
	goto_if_ne VAR_EUROPE_ROUEN_BOOK, 1, EuropeCelebi_End
	msgbox EuropeRouenBook_Text_Found
	setvar VAR_EUROPE_ROUEN_BOOK, 2
	setflag FLAG_TEMP_5
	removeobject 4
	goto EuropeCelebi_End
EuropeRouenBook_Text_Offer::
	.string "LEON: Our route book is missing.\n"
	.string "It lists the reception paths.\p"
	.string "I last used it on the far bank,\n"
	.string "north of the paved crossing.\p"
	.string "Will you look for its wrapped cover?$"
EuropeRouenBook_Text_Reminder::
	.string "Follow the east path to the water.\n"
	.string "Use the crossing, then turn north.\p"
	.string "Bring the wrapped book back to me.\n"
	.string "Please stay on the bank.$"
EuropeRouenBook_Text_Decline::
	.string "LEON: Take your time. I will stay\n"
	.string "here if you decide to help.$"
EuropeRouenBook_Text_Found::
	.string "You find a book in a waxed cover.\n"
	.string "Its pages are dry and intact.\p"
	.string "You keep it with your journey notes.\n"
	.string "Return it to LEON on the west path.$"
EuropeRouenBook_Text_Return::
	.string "LEON: That's our route book!\n"
	.string "The cover kept the pages dry.\p"
	.string "Now I can check the reception paths\n"
	.string "before sending anyone across.\p"
	.string "Thank you for bringing it back.$"
EuropeRouenBook_Text_Done::
	.string "LEON: The route book is safe here.\n"
	.string "Clear directions help us stay together.\p"
	.string "You can revisit AMIENS with the guide\n"
	.string "or return with your green companion.$"

EuropeRouenBook_Text_Unlocked::
	.string "LEON: We can care for your team here.\n"
	.string "Speak to me whenever they need rest.\p"
	.string "There is no charge. Thank you for\n"
	.string "helping us recover the route book.$"
EuropeRouenBook_Text_Rest::
	.string "LEON: Welcome back. Our care corner\n"
	.string "is ready for your whole team.\p"
	.string "Let your POKEMON rest here?\n"
	.string "There is no charge.$"
EuropeRouenBook_Text_Healed::
	.string "Your POKEMON are fully rested.\p"
	.string "LEON: Take your time before leaving.\n"
	.string "You and your team are welcome here.$"
EuropeRouenBook_Text_NotNow::
	.string "LEON: Of course. Come back whenever\n"
	.string "your team needs a quiet moment.$"
