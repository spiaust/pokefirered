@ A present-day account closes the Amiens reunion chapter.
EuropeAmiensAccount_Ada::
	goto_if_eq VAR_EUROPE_AMIENS_ACCOUNT, 1, EuropeAmiensAccount_Archived
	msgbox EuropeAmiensAccount_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiensAccount_Later
	msgbox EuropeAmiensAccount_Text_Record
	setvar VAR_EUROPE_AMIENS_ACCOUNT, 1
EuropeAmiensAccount_Archived::
	msgbox EuropeAmiensAccount_Text_Archived
	goto EuropeCelebi_End
EuropeAmiensAccount_Later::
	msgbox EuropeAmiensAccount_Text_Later
	goto EuropeCelebi_End
EuropeAmiensAccount_Text_Offer::
	.string "ADA: You have been to AMIENS?\n"
	.string "Tell me about the people you met.\p"
	.string "May I record MIRA and MEOWTH's\n"
	.string "reunion in our journey notes?$"
EuropeAmiensAccount_Text_Record::
	.string "You describe the blue ribbon and\n"
	.string "MEOWTH rubbing its coin.\p"
	.string "ADA: Two reports, checked with care,\n"
	.string "helped NORA bring them together.\p"
	.string "I'll record what you witnessed.\n"
	.string "Their small story matters too.$"
EuropeAmiensAccount_Text_Archived::
	.string "ADA: The AMIENS account is recorded.\n"
	.string "Thank you for sharing their story.\p"
	.string "CELEBI can take you back to visit.\n"
	.string "NORA's care corner remains open.$"
EuropeAmiensAccount_Text_Later::
	.string "ADA: Of course. Come back when\n"
	.string "you are ready to tell the story.$"
