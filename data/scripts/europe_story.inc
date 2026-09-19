@ England chapter one: Oak's field study. Both NPCs leave travel unrestricted.
EuropeStory_Aide::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_ENGLAND_STORY, 2, EuropeStory_Complete
	goto_if_eq VAR_EUROPE_ENGLAND_STORY, 1, EuropeStory_Report
	msgbox EuropeStory_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeStory_Decline
	setvar VAR_EUROPE_ENGLAND_STORY, 1
	msgbox EuropeStory_Text_Accepted
	goto EuropeStory_End
EuropeStory_Report::
	goto_if_defeated TRAINER_EUROPE_RIVAL_OXFORD, EuropeStory_Reward
	msgbox EuropeStory_Text_Progress
	goto EuropeStory_End
EuropeStory_Decline::
	msgbox EuropeStory_Text_Decline
	goto EuropeStory_End
EuropeStory_Reward::
	checkitemspace ITEM_SOOTHE_BELL, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeStory_BagFull
	msgbox EuropeStory_Text_Reward
	giveitem ITEM_SOOTHE_BELL, 1
	setvar VAR_EUROPE_ENGLAND_STORY, 2
EuropeStory_Complete::
	msgbox EuropeStory_Text_Complete
	goto EuropeStory_End
EuropeStory_BagFull::
	msgbox EuropeStory_Text_BagFull
EuropeStory_End::
	release
	end

EuropeStory_Rival::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_ENGLAND_STORY, 0, EuropeStory_NotStarted
	goto_if_defeated TRAINER_EUROPE_RIVAL_OXFORD, EuropeStory_RivalDone
	goto_if_defeated TRAINER_EUROPE_OLIVER, EuropeStory_CheckAlice
	msgbox EuropeStory_Text_MeetOliver
	goto EuropeStory_End
EuropeStory_CheckAlice::
	goto_if_defeated TRAINER_EUROPE_ALICE, EuropeStory_RivalReady
	msgbox EuropeStory_Text_MeetAlice
	goto EuropeStory_End
EuropeStory_RivalReady::
	msgbox EuropeStory_Text_BattleOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeStory_BattleDecline
	trainerbattle_single TRAINER_EUROPE_RIVAL_OXFORD, EuropeStory_Text_BattleIntro, EuropeStory_Text_BattleLose
EuropeStory_RivalDone::
	goto_if_eq VAR_EUROPE_ENGLAND_STORY, 2, EuropeStory_RivalComplete
	msgbox EuropeStory_Text_Return
	goto EuropeStory_End
EuropeStory_RivalComplete::
	msgbox EuropeStory_Text_RivalComplete
	goto EuropeStory_End
EuropeStory_NotStarted::
	msgbox EuropeStory_Text_NotStarted
	goto EuropeStory_End
EuropeStory_BattleDecline::
	msgbox EuropeStory_Text_BattleDecline
	goto EuropeStory_End

EuropeStory_Text_Offer::
	.string "I'm an aide to PROFESSOR OAK.\p"
	.string "OAK wants to learn how traveling\n"
	.string "partners grow together.\p"
	.string "Will you join our ENGLAND study?$"
EuropeStory_Text_Accepted::
	.string "Thank you! Battle OLIVER in the\n"
	.string "meadow and ALICE on OXFORD TRAIL.\p"
	.string "Then meet {RIVAL} in OXFORD.\n"
	.string "Your rival is helping us, too!\p"
	.string "Win that match, then report here.\n"
	.string "Earlier trail wins count, too.$"
EuropeStory_Text_Progress::
	.string "Our study follows your team's bond.\p"
	.string "Beat OLIVER and ALICE, then meet\n"
	.string "{RIVAL} in OXFORD's square.\p"
	.string "After your rival match, return here.\n"
	.string "The clinic can heal your team.$"
EuropeStory_Text_Decline::
	.string "No hurry! I will be here when you\n"
	.string "want to join the field study.$"
EuropeStory_Text_NotStarted::
	.string "{RIVAL}: Hey, {PLAYER}! OAK sent\n"
	.string "me to meet traveling trainers.\p"
	.string "Talk to his aide in LONDON's square.\n"
	.string "Then we'll compare our teams!$"
EuropeStory_Text_MeetOliver::
	.string "{RIVAL}: First, try OLIVER's match\n"
	.string "in ENGLISH MEADOW, south of here.\p"
	.string "He'll help you get ready for us!$"
EuropeStory_Text_MeetAlice::
	.string "{RIVAL}: You beat OLIVER! Now meet\n"
	.string "ALICE on OXFORD TRAIL to the south.\p"
	.string "Come back after that match!$"
EuropeStory_Text_BattleOffer::
	.string "{RIVAL}: Both trail matches won!\n"
	.string "Let's show OAK what we've learned.\p"
	.string "My PIDGEY and EEVEE are ready.\n"
	.string "Shall we battle?$"
EuropeStory_Text_BattleDecline::
	.string "{RIVAL}: Sure, take your time.\n"
	.string "The clinic is just over there.$"
EuropeStory_Text_BattleIntro::
	.string "Our partners have come a long way!$"
EuropeStory_Text_BattleLose::
	.string "You've earned it! Let's send OAK\n"
	.string "a report through his LONDON aide.$"
EuropeStory_Text_Return::
	.string "{RIVAL}: Great match! Our results\n"
	.string "are ready for OAK's field study.\p"
	.string "Report to his aide in LONDON.\n"
	.string "Walk south, or take the train.$"
EuropeStory_Text_Reward::
	.string "Your rival sent a glowing report!\n"
	.string "OAK will be pleased with your work.\p"
	.string "A team's bond grows with its journey.\n"
	.string "Here is a SOOTHE BELL to help!$"
EuropeStory_Text_Complete::
	.string "OAK's ENGLAND field study is done!\p"
	.string "Let a partner hold the SOOTHE BELL.\n"
	.string "It helps friendship grow faster.\p"
	.string "ELLIS awaits at OXFORD GYM.\n"
	.string "Look north of the town square!$"
EuropeStory_Text_RivalComplete::
	.string "{RIVAL}: OAK received our report!\n"
	.string "Try ELLIS at OXFORD GYM next!$"
EuropeStory_Text_BagFull::
	.string "Your report is ready for OAK!\n"
	.string "Your BAG's ITEMS pocket is full.\p"
	.string "Make room and come back here.\n"
	.string "I'll keep your SOOTHE BELL safe.$"
