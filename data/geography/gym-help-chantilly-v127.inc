EuropeChantillyGym_MapScripts::
	.byte 0

EuropeChantillyGym_Leader::
	lock
	faceplayer
	goto_if_defeated TRAINER_EUROPE_LEADER_MARINE, EuropeChantillyGym_Reward
	goto_if_ne VAR_EUROPE_FRANCE_STORY, 6, EuropeChantillyGym_NotReady
	msgbox EuropeChantillyGym_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeChantillyGym_Decline
	trainerbattle_single TRAINER_EUROPE_LEADER_MARINE, EuropeChantillyGym_Text_Intro, EuropeChantillyGym_Text_Defeat, EuropeChantillyGym_Victory
	goto EuropeChantillyGym_Reward
EuropeChantillyGym_Victory::
	setflag FLAG_BADGE02_GET
	msgbox EuropeChantillyGym_Text_Badge
EuropeChantillyGym_Reward::
	goto_if_eq VAR_EUROPE_CHANTILLY_TM, 1, EuropeChantillyGym_Complete
	checkitem ITEM_TM_CASE, 1
	goto_if_eq VAR_RESULT, TRUE, EuropeChantillyGym_CheckTM
	checkitemspace ITEM_TM_CASE, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeChantillyGym_Full
EuropeChantillyGym_CheckTM::
	checkitemspace ITEM_TM03, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeChantillyGym_Full
	giveitem ITEM_TM03, 1
	setvar VAR_EUROPE_CHANTILLY_TM, 1
EuropeChantillyGym_Complete::
	msgbox EuropeChantillyGym_Text_Complete
	goto EuropeChantillyGym_End
EuropeChantillyGym_Full::
	msgbox EuropeChantillyGym_Text_Full
	goto EuropeChantillyGym_End
EuropeChantillyGym_NotReady::
	msgbox EuropeChantillyGym_Text_NotReady
	goto EuropeChantillyGym_End
EuropeChantillyGym_Decline::
	msgbox EuropeChantillyGym_Text_Decline
EuropeChantillyGym_End::
	release
	end

EuropeChantillyGym_Guide::
	lock
	faceplayer
	msgbox EuropeChantillyGym_Text_Advice
	goto EuropeChantillyGym_End
EuropeChantillyGym_Statue::
	lockall
	goto_if_defeated TRAINER_EUROPE_LEADER_MARINE, EuropeChantillyGym_Winner
	msgbox EuropeChantillyGym_Text_Statue
	releaseall
	end
EuropeChantillyGym_Winner::
	msgbox EuropeChantillyGym_Text_Winner
	releaseall
	end
EuropeChantillyGym_Text_Offer::
	.string "I'm MARINE, CHANTILLY's GYM LEADER.\n"
	.string "Your survey explored our habitats.\p"
	.string "Now meet my WATER-type partners!\n"
	.string "Are you ready for a GYM battle?$"
EuropeChantillyGym_Text_Intro::
	.string "Let's make a splash!$"
EuropeChantillyGym_Text_Defeat::
	.string "Your teamwork turned the tide!$"
EuropeChantillyGym_Text_Badge::
	.string "You've earned the CASCADEBADGE!\n"
	.string "Your second badge is now recorded\p"
	.string "on your TRAINER CARD.$"
EuropeChantillyGym_Text_Complete::
	.string "TM03 teaches WATER PULSE.\n"
	.string "It may confuse the target.\p"
	.string "A TM can be used only once.\n"
	.string "Choose its partner with care!\p"
	.string "LENA needs a courier in BERLIN.\n"
	.string "Find her west of the city guide!$"
EuropeChantillyGym_Text_Full::
	.string "Your badge is safe! Make room\n"
	.string "for TM03, then speak to me again.$"
EuropeChantillyGym_Text_NotReady::
	.string "First, finish CELINE's garden survey.\n"
	.string "She waits west of PARIS's guide.\p"
	.string "Let REMY review both study notes,\n"
	.string "then collect your reward in PARIS.$"
EuropeChantillyGym_Text_Decline::
	.string "Prepare your team. I'll wait here.\n"
	.string "The clinic offers free healing.$"
EuropeChantillyGym_Text_Advice::
	.string "MARINE uses WATER-type partners:\n"
	.string "PSYDUCK Lv.12 and HORSEA Lv.14.\p"
	.string "GRASS and ELECTRIC moves work well.\n"
	.string "Raise a team and bring POTIONS.\p"
	.string "First, complete CELINE's survey\n"
	.string "and collect her reward in PARIS.$"
EuropeChantillyGym_Text_Statue::
	.string "CHANTILLY GYM\n"
	.string "LEADER: MARINE\p"
	.string "Teamwork that turns the tide.$"
EuropeChantillyGym_Text_Winner::
	.string "CHANTILLY GYM\n"
	.string "LEADER: MARINE\p"
	.string "Winning trainer: {PLAYER}$"
