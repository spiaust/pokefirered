@ Ada records the player's port visit after the dock instructions are checked.
EuropePortAccount_Ada::
	goto_if_eq VAR_EUROPE_PORT_ACCOUNT, 1, EuropePortAccount_Archived
	msgbox EuropePortAccount_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropePortAccount_Later
	msgbox EuropePortAccount_Text_Record
	setvar VAR_EUROPE_PORT_ACCOUNT, 1
EuropePortAccount_Archived::
	msgbox EuropePortAccount_Text_Archived
	goto EuropeCelebi_End
EuropePortAccount_Later::
	msgbox EuropePortAccount_Text_Later
	goto EuropeCelebi_End
EuropePortAccount_Text_Offer::
	.string "ADA: You reached LE HAVRE?\n"
	.string "Tell me about your visit.\p"
	.string "May I record the port reception\n"
	.string "in our journey notes?$"
EuropePortAccount_Text_Record::
	.string "You describe LEON's route book,\n"
	.string "the quay and its waiting travelers.\p"
	.string "You explain how the captain checked\n"
	.string "the instructions on the notice.\p"
	.string "ADA: Clear directions and a place\n"
	.string "to rest helped everyone wait.\p"
	.string "We will record what you witnessed.\n"
	.string "Their onward journey is still ahead.$"
EuropePortAccount_Text_Archived::
	.string "ADA: The port account is recorded.\n"
	.string "Thank you for sharing what you saw.\p"
	.string "CELEBI now offers a direct port visit.\n"
	.string "The dockworker's care remains open.$"
EuropePortAccount_Text_Later::
	.string "ADA: Of course. Come back when\n"
	.string "you are ready to tell the story.$"
