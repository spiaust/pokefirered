EuropeReunion_Restore::
	addobject 4
	addobject 5
	setflag FLAG_TEMP_4
	clearflag FLAG_TEMP_3
	goto_if_eq VAR_EUROPE_REUNION_STORY, 6, EuropeReunion_RestoreHome
	addobject 6
	removeobject 7
	end
EuropeReunion_RestoreHome::
	setflag FLAG_TEMP_3
	clearflag FLAG_TEMP_4
	removeobject 6
	addobject 7
	end
EuropeReunion_Nora::
	goto_if_eq VAR_EUROPE_AMIENS_NEWS, 3, EuropeAmiensNews_Deliver
	goto_if_eq VAR_EUROPE_REUNION_STORY, 6, EuropeReunion_Done
	goto_if_eq VAR_EUROPE_REUNION_STORY, 5, EuropeReunion_Verified
	goto_if_eq VAR_EUROPE_REUNION_STORY, 4, EuropeReunion_Verify
	goto_if_ne VAR_EUROPE_REUNION_STORY, 0, EuropeReunion_Reminder
	msgbox EuropeReunion_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeReunion_Decline
	setvar VAR_EUROPE_REUNION_STORY, 1
EuropeReunion_Reminder::
	msgbox EuropeReunion_Text_Reminder
	goto EuropeCelebi_End
EuropeReunion_Decline::
	msgbox EuropeReunion_Text_Decline
	goto EuropeCelebi_End
EuropeReunion_Verify::
	msgbox EuropeReunion_Text_Verify
	setvar VAR_EUROPE_REUNION_STORY, 5
EuropeReunion_Verified::
	msgbox EuropeReunion_Text_Verified
	goto EuropeCelebi_End
EuropeReunion_Done::
	msgbox EuropeReunion_Text_Rest, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeReunion_NotNow
	closemessage
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox EuropeReunion_Text_Healed
	goto EuropeCelebi_End
EuropeReunion_NotNow::
	msgbox EuropeReunion_Text_NotNow
	goto EuropeCelebi_End
EuropeReunion_Mira::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_REUNION_STORY, 6, EuropeReunion_MiraDone
	goto_if_eq VAR_EUROPE_REUNION_STORY, 5, EuropeReunion_Reunite
	goto_if_eq VAR_EUROPE_REUNION_STORY, 0, EuropeReunion_NotStarted
	msgbox EuropeReunion_Text_Mira
	goto_if_eq VAR_EUROPE_REUNION_STORY, 3, EuropeReunion_Both
	goto_if_ne VAR_EUROPE_REUNION_STORY, 1, EuropeCelebi_End
	setvar VAR_EUROPE_REUNION_STORY, 2
	goto EuropeCelebi_End
EuropeReunion_Porter::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_REUNION_STORY, 6, EuropeReunion_PorterDone
	goto_if_eq VAR_EUROPE_REUNION_STORY, 0, EuropeReunion_NotStarted
	msgbox EuropeReunion_Text_Porter
	goto_if_eq VAR_EUROPE_REUNION_STORY, 2, EuropeReunion_Both
	goto_if_ne VAR_EUROPE_REUNION_STORY, 1, EuropeCelebi_End
	setvar VAR_EUROPE_REUNION_STORY, 3
	goto EuropeCelebi_End
EuropeReunion_Both::
	setvar VAR_EUROPE_REUNION_STORY, 4
	msgbox EuropeReunion_Text_Both
	goto EuropeCelebi_End
EuropeReunion_NotStarted::
	msgbox EuropeReunion_Text_NotStarted
	goto EuropeCelebi_End
EuropeReunion_Reunite::
	msgbox EuropeReunion_Text_Reunite
	setvar VAR_EUROPE_REUNION_STORY, 6
	setflag FLAG_TEMP_3
	clearflag FLAG_TEMP_4
	removeobject 6
	addobject 7
	playmoncry SPECIES_MEOWTH, 0
	waitmoncry
EuropeReunion_MiraDone::
	msgbox EuropeReunion_Text_MiraDone
	goto EuropeCelebi_End
EuropeReunion_PorterDone::
	goto_if_eq VAR_EUROPE_AMIENS_ACCOUNT, 1, EuropeAmiensNews_Porter
	msgbox EuropeReunion_Text_PorterDone
	goto EuropeCelebi_End
EuropeReunion_Meowth::
	lock
	faceplayer
	playmoncry SPECIES_MEOWTH, 0
	waitmoncry
	goto_if_eq VAR_EUROPE_REUNION_STORY, 6, EuropeReunion_CatHome
	msgbox EuropeReunion_Text_CatWaiting
	goto EuropeCelebi_End
EuropeReunion_CatHome::
	msgbox EuropeReunion_Text_CatHome
	goto EuropeCelebi_End

EuropeReunion_Text_Offer::
	.string "NORA: MIRA is missing her MEOWTH.\n"
	.string "A porter is caring for one nearby.\p"
	.string "We should check both descriptions\n"
	.string "before telling her it is her partner.\p"
	.string "Will you help compare their reports?$"
EuropeReunion_Text_Reminder::
	.string "Speak to MIRA on the north path\n"
	.string "and the porter on the east side.\p"
	.string "You can visit them in either order.\n"
	.string "Bring both descriptions back to me.$"
EuropeReunion_Text_Decline::
	.string "NORA: That's all right. Ask again\n"
	.string "when you are ready.$"
EuropeReunion_Text_Mira::
	.string "MIRA: My MEOWTH wears a blue ribbon.\n"
	.string "It rubs its coin when it is nervous.\p"
	.string "We were separated at the platform.\n"
	.string "Please tell NORA what I've said.$"
EuropeReunion_Text_Porter::
	.string "This MEOWTH has a blue ribbon.\n"
	.string "It keeps rubbing the coin on its head.\p"
	.string "I'll stay with it until NORA checks\n"
	.string "who has been looking for it.$"
EuropeReunion_Text_Both::
	.string "Both descriptions are recorded.\n"
	.string "Return to NORA by the west path.$"
EuropeReunion_Text_NotStarted::
	.string "NORA is coordinating the reunions.\n"
	.string "Please speak with her first.$"
EuropeReunion_Text_Verify::
	.string "NORA: The ribbon and nervous habit\n"
	.string "match MIRA's description.\p"
	.string "I'll ask the porter to bring MEOWTH\n"
	.string "over while you give MIRA the news.$"
EuropeReunion_Text_Verified::
	.string "NORA: Speak to MIRA on the north\n"
	.string "path. We have checked both reports.$"
EuropeReunion_Text_Reunite::
	.string "MIRA: You found my partner?\n"
	.string "The porter brings MEOWTH over.\p"
	.string "MEOWTH hears her voice and runs\n"
	.string "straight to her side.$"
EuropeReunion_Text_MiraDone::
	.string "MIRA: There you are, little one.\n"
	.string "Thank you for checking carefully.\p"
	.string "We'll wait together from now on.\p"
	.string "NORA can help your team rest.\n"
	.string "Please take care of yourselves too.$"
EuropeReunion_Text_PorterDone::
	.string "MEOWTH is back with MIRA.\n"
	.string "I'm glad we checked before moving.$"
EuropeReunion_Text_Rest::
	.string "NORA: MIRA and MEOWTH are together.\n"
	.string "You have earned a quiet moment too.\p"
	.string "We can care for your whole team.\n"
	.string "There is no charge. Rest here?$"
EuropeReunion_Text_NotNow::
	.string "NORA: Come back whenever you need.\n"
	.string "We will keep a place for your team.$"
EuropeReunion_Text_Healed::
	.string "Your POKEMON are fully rested.\p"
	.string "NORA: Thank you for helping MIRA.\n"
	.string "You and your team are welcome here.$"
EuropeReunion_Text_CatWaiting::
	.string "MEOWTH rubs its coin and looks\n"
	.string "toward the people on the north path.$"
EuropeReunion_Text_CatHome::
	.string "MEOWTH purrs beside MIRA.\n"
	.string "Its blue ribbon flutters in the breeze.$"
