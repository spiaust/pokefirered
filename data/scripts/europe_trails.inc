EuropeTrail_Decline::
	msgbox EuropeTrail_Text_Decline
	release
	end

EuropeTrail_Report::
	setvar VAR_0x8005, 0
	call_if_defeated TRAINER_EUROPE_OLIVER, EuropeTour_CountStamp
	call_if_defeated TRAINER_EUROPE_CAMILLE, EuropeTour_CountStamp
	call_if_defeated TRAINER_EUROPE_FELIX, EuropeTour_CountStamp
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox EuropeTrail_Text_Progress
	call_if_eq VAR_0x8005, 3, EuropeTrail_Congratulate
	return

EuropeTrail_Congratulate::
	msgbox EuropeTrail_Text_Complete
	return

EuropeTrail_Text_Decline::
	.string "No hurry! Heal at the city clinic,\n"
	.string "then come back when you're ready.$"

EuropeTrail_Text_Progress::
	.string "Trail victories: {STR_VAR_1} of 3.\p"
	.string "Find OLIVER in ENGLISH MEADOW,\n"
	.string "CAMILLE in FRENCH GARDENS,\l"
	.string "and FELIX in GERMAN WOODLAND.$"

EuropeTrail_Text_Complete::
	.string "You beat all three trail trainers!\n"
	.string "Your team is growing stronger.\p"
	.string "Keep training and catching POKEMON\n"
	.string "for the next leg of your journey!$"
