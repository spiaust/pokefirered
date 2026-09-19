EuropeLuggage_Restore::
	addobject 6
	addobject 4
	goto_if_eq VAR_EUROPE_LUGGAGE, 1, EuropeLuggage_Show
	setflag FLAG_TEMP_5
	removeobject 5
	end
EuropeLuggage_Show::
	clearflag FLAG_TEMP_5
	addobject 5
	end
EuropeLuggage_Worker::
	lock
	faceplayer
	goto_if_ne VAR_EUROPE_SOUTHAMPTON, 2, EuropeLuggage_Locked
	goto_if_eq VAR_EUROPE_LUGGAGE, 3, EuropeLuggage_Done
	goto_if_eq VAR_EUROPE_LUGGAGE, 2, EuropeLuggage_Return
	goto_if_eq VAR_EUROPE_LUGGAGE, 1, EuropeLuggage_Reminder
	msgbox EuropeLuggage_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeLuggage_Later
	setvar VAR_EUROPE_LUGGAGE, 1
	clearflag FLAG_TEMP_5
	addobject 5
EuropeLuggage_Reminder::
	msgbox EuropeLuggage_Text_Reminder
	goto EuropeCelebi_End
EuropeLuggage_Locked::
	msgbox EuropeLuggage_Text_Locked
	goto EuropeCelebi_End
EuropeLuggage_Later::
	msgbox EuropeLuggage_Text_Later
	goto EuropeCelebi_End
EuropeLuggage_Pickup::
	lock
	faceplayer
	goto_if_ne VAR_EUROPE_LUGGAGE, 1, EuropeCelebi_End
	msgbox EuropeLuggage_Text_Found
	setvar VAR_EUROPE_LUGGAGE, 2
	setflag FLAG_TEMP_5
	removeobject 5
	goto EuropeCelebi_End
EuropeLuggage_Return::
	msgbox EuropeLuggage_Text_Return
	setvar VAR_EUROPE_LUGGAGE, 3
	msgbox EuropeLuggage_Text_Unlocked
	goto EuropeCelebi_End
EuropeLuggage_Done::
	msgbox EuropeLuggage_Text_Rest, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeLuggage_NotNow
	closemessage
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox EuropeLuggage_Text_Healed
	goto EuropeCelebi_End
EuropeLuggage_NotNow::
	msgbox EuropeLuggage_Text_NotNow
	goto EuropeCelebi_End
EuropeLuggage_Text_Locked::
	.string "Please speak to the host first.\n"
	.string "He is waiting below the pier.$"
EuropeLuggage_Text_Offer::
	.string "One traveler has misplaced a bag\n"
	.string "with a green label.\p"
	.string "It was set down on the left quay.\n"
	.string "Will you look for it?$"
EuropeLuggage_Text_Reminder::
	.string "Look left of the closed entrance.\n"
	.string "Bring the green-labeled bag here.$"
EuropeLuggage_Text_Later::
	.string "All right. I will keep looking.\n"
	.string "Ask again if you have time.$"
EuropeLuggage_Text_Found::
	.string "You find the green-labeled bag.\n"
	.string "Its clasp is still fastened.\p"
	.string "You carry it carefully without\n"
	.string "opening it. Return it to the worker.$"
EuropeLuggage_Text_Return::
	.string "That is the missing bag!\n"
	.string "I will bring it to its owner.\p"
	.string "The traveler thanks you. Having\n"
	.string "their own things helps them settle.$"
EuropeLuggage_Text_Unlocked::
	.string "We can help your team rest here.\n"
	.string "Speak to me whenever they need care.\p"
	.string "There is no charge. CELEBI can now\n"
	.string "bring you straight back here, too.$"
EuropeLuggage_Text_Rest::
	.string "The traveler has their bag again.\n"
	.string "Now let us help your team.\p"
	.string "Let your POKEMON rest here?\n"
	.string "There is no charge.$"
EuropeLuggage_Text_Healed::
	.string "Your POKEMON are fully rested.\p"
	.string "Take your time. You and your team\n"
	.string "are welcome at our reception.$"
EuropeLuggage_Text_NotNow::
	.string "Of course. Come back whenever\n"
	.string "your team needs a quiet moment.$"
