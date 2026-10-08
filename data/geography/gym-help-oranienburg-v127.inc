EuropeOranienburgGym_MapScripts::
	.byte 0

EuropeOranienburgGym_Leader::
	lock
	faceplayer
	goto_if_defeated TRAINER_EUROPE_LEADER_CONRAD, EuropeOranienburgGym_Reward
	goto_if_ne VAR_EUROPE_GERMANY_STORY, 3, EuropeOranienburgGym_NotReady
	msgbox EuropeOranienburgGym_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeOranienburgGym_Decline
	trainerbattle_single TRAINER_EUROPE_LEADER_CONRAD, EuropeOranienburgGym_Text_Intro, EuropeOranienburgGym_Text_Defeat, EuropeOranienburgGym_Victory
	goto EuropeOranienburgGym_Reward
EuropeOranienburgGym_Victory::
	setflag FLAG_BADGE03_GET
	msgbox EuropeOranienburgGym_Text_Badge
EuropeOranienburgGym_Reward::
	goto_if_eq VAR_EUROPE_ORANIENBURG_TM, 1, EuropeOranienburgGym_Complete
	checkitem ITEM_TM_CASE, 1
	goto_if_eq VAR_RESULT, TRUE, EuropeOranienburgGym_CheckTM
	checkitemspace ITEM_TM_CASE, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeOranienburgGym_Full
EuropeOranienburgGym_CheckTM::
	checkitemspace ITEM_TM34, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeOranienburgGym_Full
	giveitem ITEM_TM34, 1
	setvar VAR_EUROPE_ORANIENBURG_TM, 1
EuropeOranienburgGym_Complete::
	msgbox EuropeOranienburgGym_Text_Complete
	goto EuropeOranienburgGym_End
EuropeOranienburgGym_Full::
	msgbox EuropeOranienburgGym_Text_Full
	goto EuropeOranienburgGym_End
EuropeOranienburgGym_NotReady::
	msgbox EuropeOranienburgGym_Text_NotReady
	goto EuropeOranienburgGym_End
EuropeOranienburgGym_Decline::
	msgbox EuropeOranienburgGym_Text_Decline
EuropeOranienburgGym_End::
	release
	end

EuropeOranienburgGym_Guide::
	lock
	faceplayer
	msgbox EuropeOranienburgGym_Text_Advice
	goto EuropeOranienburgGym_End
EuropeOranienburgGym_Statue::
	lockall
	goto_if_defeated TRAINER_EUROPE_LEADER_CONRAD, EuropeOranienburgGym_Winner
	msgbox EuropeOranienburgGym_Text_Statue
	releaseall
	end
EuropeOranienburgGym_Winner::
	msgbox EuropeOranienburgGym_Text_Winner
	releaseall
	end
EuropeOranienburgGym_Text_Offer::
	.string "I'm CONRAD, this town's GYM LEADER.\n"
	.string "LENA told me about your delivery.\p"
	.string "Reliable partners make connections!\n"
	.string "Ready for an ELECTRIC-type battle?$"
EuropeOranienburgGym_Text_Intro::
	.string "Let's put your teamwork to the test!$"
EuropeOranienburgGym_Text_Defeat::
	.string "Your team has a powerful connection!$"
EuropeOranienburgGym_Text_Badge::
	.string "You've earned the THUNDERBADGE!\n"
	.string "Your third badge is now recorded\p"
	.string "on your TRAINER CARD.$"
EuropeOranienburgGym_Text_Complete::
	.string "TM34 teaches SHOCK WAVE.\n"
	.string "Its electric attack never misses.\p"
	.string "GROUND types are still immune.\n"
	.string "A TM can be used only once.\p"
	.string "Three badges from three countries!\n"
	.string "River captains in LONDON and OXFORD\n"
	.string "now welcome you aboard for free!$"
EuropeOranienburgGym_Text_Full::
	.string "Your badge is safe! Make room\n"
	.string "for TM34, then speak to me again.$"
EuropeOranienburgGym_Text_NotReady::
	.string "First, finish LENA's delivery.\n"
	.string "She waits west of BERLIN's guide.\p"
	.string "Bring KARL's report back to her\n"
	.string "and collect your MAGNET reward.$"
EuropeOranienburgGym_Text_Decline::
	.string "Prepare your team. I'll wait here.\n"
	.string "The clinic offers free healing.$"
EuropeOranienburgGym_Text_Advice::
	.string "CONRAD uses ELECTRIC partners:\n"
	.string "VOLTORB Lv.14 and PIKACHU Lv.16.\p"
	.string "GROUND moves are strong here.\n"
	.string "GRASS resists ELECTRIC attacks.\p"
	.string "WATER and FLYING partners beware!\n"
	.string "Raise a team and bring POTIONS.\p"
	.string "First, finish LENA's delivery\n"
	.string "and collect her reward in BERLIN.$"
EuropeOranienburgGym_Text_Statue::
	.string "ORANIENBURG GYM\n"
	.string "LEADER: CONRAD\p"
	.string "Teamwork makes strong connections.$"
EuropeOranienburgGym_Text_Winner::
	.string "ORANIENBURG GYM\n"
	.string "LEADER: CONRAD\p"
	.string "Winning trainer: {PLAYER}$"
