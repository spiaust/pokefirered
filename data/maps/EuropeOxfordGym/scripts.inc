EuropeOxfordGym_MapScripts::
	.byte 0

EuropeOxfordGym_Leader::
	lock
	faceplayer
	goto_if_defeated TRAINER_EUROPE_LEADER_ELLIS, EuropeOxfordGym_Reward
	goto_if_ne VAR_EUROPE_ENGLAND_STORY, 2, EuropeOxfordGym_NotReady
	msgbox EuropeOxfordGym_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeOxfordGym_Decline
	trainerbattle_single TRAINER_EUROPE_LEADER_ELLIS, EuropeOxfordGym_Text_Intro, EuropeOxfordGym_Text_Defeat, EuropeOxfordGym_Victory
	goto EuropeOxfordGym_Reward
EuropeOxfordGym_Victory::
	setflag FLAG_BADGE01_GET
	msgbox EuropeOxfordGym_Text_Badge
EuropeOxfordGym_Reward::
	goto_if_eq VAR_EUROPE_OXFORD_TM, 1, EuropeOxfordGym_Complete
	checkitem ITEM_TM_CASE, 1
	goto_if_eq VAR_RESULT, TRUE, EuropeOxfordGym_CheckTM
	checkitemspace ITEM_TM_CASE, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeOxfordGym_Full
EuropeOxfordGym_CheckTM::
	checkitemspace ITEM_TM39, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeOxfordGym_Full
	giveitem ITEM_TM39, 1
	setvar VAR_EUROPE_OXFORD_TM, 1
EuropeOxfordGym_Complete::
	msgbox EuropeOxfordGym_Text_Complete
	goto EuropeOxfordGym_End
EuropeOxfordGym_Full::
	msgbox EuropeOxfordGym_Text_Full
	goto EuropeOxfordGym_End
EuropeOxfordGym_NotReady::
	msgbox EuropeOxfordGym_Text_NotReady
	goto EuropeOxfordGym_End
EuropeOxfordGym_Decline::
	msgbox EuropeOxfordGym_Text_Decline
EuropeOxfordGym_End::
	release
	end

EuropeOxfordGym_Guide::
	lock
	faceplayer
	msgbox EuropeOxfordGym_Text_Advice
	goto EuropeOxfordGym_End
EuropeOxfordGym_Statue::
	lockall
	goto_if_defeated TRAINER_EUROPE_LEADER_ELLIS, EuropeOxfordGym_Winner
	msgbox EuropeOxfordGym_Text_Statue
	releaseall
	end
EuropeOxfordGym_Winner::
	msgbox EuropeOxfordGym_Text_Winner
	releaseall
	end
EuropeOxfordGym_Text_Offer::
	.string "I'm ELLIS, OXFORD's GYM LEADER.\p"
	.string "OAK's study taught you to travel\n"
	.string "and grow alongside your partners.\p"
	.string "Now test that bond against ROCK!\n"
	.string "Are you ready for a GYM battle?$"
EuropeOxfordGym_Text_Intro::
	.string "Build your victory on solid ground!$"
EuropeOxfordGym_Text_Defeat::
	.string "Your teamwork has a firm foundation!$"
EuropeOxfordGym_Text_Badge::
	.string "You've earned the BOULDERBADGE!\p"
	.string "Your first badge is now recorded\n"
	.string "on your TRAINER CARD.$"
EuropeOxfordGym_Text_Complete::
	.string "TM39 teaches ROCK TOMB.\n"
	.string "It damages and slows the target.\p"
	.string "A TM can be used only once.\n"
	.string "Choose its partner with care!\p"
	.string "CELINE in PARIS seeks field helpers.\n"
	.string "Your badge is a good introduction!$"
EuropeOxfordGym_Text_Full::
	.string "Your badge is safe! Make room\n"
	.string "for TM39, then speak to me again.$"
EuropeOxfordGym_Text_NotReady::
	.string "Before this match, finish OAK's\n"
	.string "ENGLAND field study.\p"
	.string "His aide waits in LONDON's square.\n"
	.string "Return after delivering your report.$"
EuropeOxfordGym_Text_Decline::
	.string "Prepare your team. I'll wait here.\n"
	.string "The clinic offers free healing.$"
EuropeOxfordGym_Text_Advice::
	.string "ELLIS uses ROCK-type partners:\n"
	.string "GEODUDE Lv.10 and ONIX Lv.12.\p"
	.string "GRASS and WATER moves work well.\n"
	.string "TACKLE alone will be a tough climb!\p"
	.string "ODDISH lives on the English trails.\n"
	.string "Raise a team and bring POTIONS.\p"
	.string "First, finish OAK's field study\n"
	.string "and report to his LONDON aide.$"
EuropeOxfordGym_Text_Statue::
	.string "OXFORD GYM\nLEADER: ELLIS\p"
	.string "A firm foundation for every team.$"
EuropeOxfordGym_Text_Winner::
	.string "OXFORD GYM\nLEADER: ELLIS\p"
	.string "Winning trainer: {PLAYER}$"
