EuropeSouthAccount_Ada::
	goto_if_eq VAR_EUROPE_SOUTH_ACCOUNT, 1, EuropeSouthAccount_Archived
	msgbox EuropeSouthAccount_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeSouthAccount_Later
	msgbox EuropeSouthAccount_Text_Record
	setvar VAR_EUROPE_SOUTH_ACCOUNT, 1
EuropeSouthAccount_Archived::
	msgbox EuropeSouthAccount_Text_Archived
	goto EuropeCelebi_End
EuropeSouthAccount_Later::
	msgbox EuropeSouthAccount_Text_Later
	goto EuropeCelebi_End
EuropeSouthAccount_Text_Offer::
	.string "ADA: You visited SOUTHAMPTON?\n"
	.string "Tell me about the reception.\p"
	.string "May I record your visit in\n"
	.string "our journey notes?$"
EuropeSouthAccount_Text_Record::
	.string "You describe the crossing and\n"
	.string "the host who recorded your arrival.\p"
	.string "You tell ADA about the lost bag\n"
	.string "and its relieved owner.\p"
	.string "ADA: We often remember journeys\n"
	.string "by their destinations.\p"
	.string "But finding a familiar belonging\n"
	.string "can matter just as much on arrival.\p"
	.string "I will record what you witnessed.$"
EuropeSouthAccount_Text_Archived::
	.string "ADA: The SOUTHAMPTON account\n"
	.string "is recorded. Thank you.\p"
	.string "CELEBI can take you back directly.\n"
	.string "The reception's care remains open.$"
EuropeSouthAccount_Text_Later::
	.string "ADA: Of course. Come back when\n"
	.string "you are ready to tell the story.$"
