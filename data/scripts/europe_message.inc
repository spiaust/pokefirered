@ The first historical arc closes with a message and a present-day account.
EuropeMessage_Offer::
	goto_if_eq VAR_EUROPE_MESSAGE_STORY, 1, EuropeMessage_Directions
	goto_if_eq VAR_EUROPE_MESSAGE_STORY, 2, EuropeMessage_Reply
	goto_if_ge VAR_EUROPE_MESSAGE_STORY, 3, EuropeMessage_EliseDone
	msgbox EuropeMessage_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeMessage_Decline
	setvar VAR_EUROPE_MESSAGE_STORY, 1
EuropeMessage_Directions::
	msgbox EuropeMessage_Text_Directions
	goto EuropeCelebi_End
EuropeMessage_Decline::
	msgbox EuropeMessage_Text_Decline
	goto EuropeCelebi_End
EuropeMessage_Deliver::
	msgbox EuropeMessage_Text_Deliver
	setvar VAR_EUROPE_MESSAGE_STORY, 2
EuropeMessage_KeeperDone::
	goto_if_ge VAR_EUROPE_MESSAGE_STORY, 3, EuropeMessage_KeeperReplied
	msgbox EuropeMessage_Text_KeeperDone
	goto EuropeCelebi_End
EuropeMessage_KeeperReplied::
	msgbox EuropeMessage_Text_KeeperReplied
	goto EuropeCelebi_End
EuropeMessage_Reply::
	msgbox EuropeMessage_Text_Reply
	setvar VAR_EUROPE_MESSAGE_STORY, 3
	msgbox EuropeMessage_Text_Report
	goto EuropeCelebi_End
EuropeMessage_EliseDone::
	goto_if_eq VAR_EUROPE_RELIEF_STORY, 3, EuropeGarden_Offer
	msgbox EuropeMessage_Text_EliseDone
	goto EuropeCelebi_End
EuropeMessage_Ada::
	goto_if_eq VAR_EUROPE_MESSAGE_STORY, 4, EuropeMessage_Archived
	checkitemspace ITEM_LUXURY_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeMessage_Full
	msgbox EuropeMessage_Text_Ada
	giveitem ITEM_LUXURY_BALL, 1
	setvar VAR_EUROPE_MESSAGE_STORY, 4
EuropeMessage_Archived::
	msgbox EuropeMessage_Text_Archived
	goto EuropeCelebi_End
EuropeMessage_Full::
	msgbox EuropeMessage_Text_Full
	goto EuropeCelebi_End

EuropeMessage_Text_Offer::
	.string "ELISE: The refuge keeper was kind\n"
	.string "to us. She must be wondering.\p"
	.string "Will you tell her that EEVEE and I\n"
	.string "arrived together and have shelter?$"
EuropeMessage_Text_Directions::
	.string "Take the south return service, then\n"
	.string "ask the guide to go to the refuge.\p"
	.string "Tell its keeper we're safe here.\n"
	.string "Please bring back her reply.$"
EuropeMessage_Text_Decline::
	.string "ELISE: That's all right. Ask me\n"
	.string "again when you have time.$"
EuropeMessage_Text_Deliver::
	.string "They arrived together? I'm relieved!\n"
	.string "Thank you for bringing their message.\p"
	.string "Tell ELISE that her kindness to\n"
	.string "EEVEE helped them both be brave.$"
EuropeMessage_Text_KeeperDone::
	.string "Please take my reply back to ELISE\n"
	.string "at BEAUVAIS reception.\p"
	.string "Knowing they have shelter gives\n"
	.string "everyone here a little more hope.$"
EuropeMessage_Text_Reply::
	.string "ELISE: I'm glad she knows.\n"
	.string "I'll remember what she said.\p"
	.string "You kept coming back for us.\n"
	.string "Thank you, from both of us.$"
EuropeMessage_Text_KeeperReplied::
	.string "Thank you for carrying both messages.\n"
	.string "ELISE knows we're thinking of her.\p"
	.string "You have done a kind thing.\n"
	.string "Rest when you need to.$"
EuropeMessage_Text_Report::
	.string "You record the keeper's reply.\n"
	.string "ADA in OXFORD should hear the story.$"
EuropeMessage_Text_EliseDone::
	.string "ELISE: EEVEE and I are resting here.\n"
	.string "Thank you for carrying our message.$"
EuropeMessage_Text_Ada::
	.string "ADA: A blanket, reliable news,\n"
	.string "a journey, and a message home.\p"
	.string "I'll record ELISE and EEVEE's story\n"
	.string "with your account of the refuge.\p"
	.string "This LUXURY BALL is for a new friend.\n"
	.string "Kindness belongs in every time.$"
EuropeMessage_Text_Archived::
	.string "ADA: Your first time-travel account\n"
	.string "is recorded. Take a well-earned rest.\p"
	.string "CELEBI can still take you back\n"
	.string "to visit ELISE and EEVEE.\p"
	.string "Ask the BEAUVAIS host if there\n"
	.string "is more you can do to help.$"
EuropeMessage_Text_Full::
	.string "ADA: Your account is safe. Make room\n"
	.string "in POKE BALLS for one LUXURY BALL,\p"
	.string "then return to collect it.$"
