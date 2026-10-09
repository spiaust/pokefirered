@ A supply run unlocks repeatable rest at the historical reception.
EuropeRelief_Host::
	goto_if_eq VAR_EUROPE_RELIEF_STORY, 3, EuropeRelief_Rest
	goto_if_eq VAR_EUROPE_RELIEF_STORY, 2, EuropeRelief_Deliver
	goto_if_eq VAR_EUROPE_RELIEF_STORY, 1, EuropeRelief_Directions
	msgbox EuropeRelief_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeRelief_Decline
	setvar VAR_EUROPE_RELIEF_STORY, 1
EuropeRelief_Directions::
	msgbox EuropeRelief_Text_Directions
	goto EuropeCelebi_End
EuropeRelief_Decline::
	msgbox EuropeRelief_Text_Decline
	goto EuropeCelebi_End
EuropeRelief_Dispatcher::
	goto_if_eq VAR_EUROPE_RELIEF_STORY, 3, EuropeRelief_DispatcherDone
	goto_if_eq VAR_EUROPE_RELIEF_STORY, 2, EuropeRelief_Parcel
	msgbox EuropeRelief_Text_Collect
	setvar VAR_EUROPE_RELIEF_STORY, 2
EuropeRelief_Parcel::
	msgbox EuropeRelief_Text_Parcel
	goto EuropeCelebi_End
EuropeRelief_DispatcherDone::
	goto_if_eq VAR_EUROPE_GARDEN_STORY, 3, EuropeAmiens_Offer
	msgbox EuropeRelief_Text_DispatcherDone
	goto EuropeCelebi_End
EuropeRelief_Deliver::
	msgbox EuropeRelief_Text_Deliver
	setvar VAR_EUROPE_RELIEF_STORY, 3
	msgbox EuropeRelief_Text_Unlocked
	goto EuropeCelebi_End
EuropeRelief_Rest::
	msgbox EuropeRelief_Text_Rest, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeRelief_NotNow
	closemessage
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox EuropeRelief_Text_Healed
	goto EuropeCelebi_End
EuropeRelief_NotNow::
	msgbox EuropeRelief_Text_NotNow
	goto EuropeCelebi_End

EuropeRelief_Text_Offer::
	.string "More travelers need a place to rest.\n"
	.string "We are setting up a care corner.\p"
	.string "The CHANTILLY dispatcher has clean\n"
	.string "bedding and POKEMON supplies for us.\p"
	.string "Could you collect the parcel?$"
EuropeRelief_Text_Directions::
	.string "Take the south return service.\n"
	.string "Ask the station dispatcher for it.\p"
	.string "Then read the board to return here.\n"
	.string "I'll keep a place for the supplies.$"
EuropeRelief_Text_Decline::
	.string "Of course. Speak to me when\n"
	.string "you are ready to help.$"
EuropeRelief_Text_Collect::
	.string "Supplies for BEAUVAIS? Here they are.\n"
	.string "You take the sealed care parcel.\p"
	.string "There is no charge. Thank you for\n"
	.string "getting it to the people waiting.$"
EuropeRelief_Text_Parcel::
	.string "The parcel is ready for the host.\n"
	.string "Read the board to ride to BEAUVAIS.$"
EuropeRelief_Text_DispatcherDone::
	.string "The care corner is open? Good news!\n"
	.string "You can rest at BEAUVAIS now.\p"
	.string "Read the board whenever you want\n"
	.string "to take the train there.$"
EuropeRelief_Text_Deliver::
	.string "You hand the care parcel to the host.\p"
	.string "Thank you! Clean bedding and supplies\n"
	.string "will help us care for tired POKEMON.$"
EuropeRelief_Text_Unlocked::
	.string "Our care corner is ready. Speak to\n"
	.string "me whenever your team needs rest.\p"
	.string "You and your POKEMON are welcome.\n"
	.string "There is no charge.$"
EuropeRelief_Text_Rest::
	.string "Welcome back to our care corner.\n"
	.string "Let your POKEMON rest here?$"
EuropeRelief_Text_NotNow::
	.string "Come back whenever you need to.\n"
	.string "Take care on your travels.$"
EuropeRelief_Text_Healed::
	.string "Your POKEMON are fully rested.\n"
	.string "You can stay as long as you need.$"
