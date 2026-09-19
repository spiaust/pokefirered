@ German signal-repair delivery. Mission cargo is tracked outside the Bag.
EuropeGermany_Lena::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_GERMANY_STORY, 3, EuropeGermany_Complete
	goto_if_eq VAR_EUROPE_GERMANY_STORY, 2, EuropeGermany_Reward
	goto_if_eq VAR_EUROPE_GERMANY_STORY, 1, EuropeGermany_Directions
	goto_if_unset FLAG_BADGE01_GET, EuropeGermany_Badges
	goto_if_unset FLAG_BADGE02_GET, EuropeGermany_Badges
	msgbox EuropeGermany_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeGermany_Decline
	setvar VAR_EUROPE_GERMANY_STORY, 1
	msgbox EuropeGermany_Text_Accepted
	goto EuropeGermany_End
EuropeGermany_Directions::
	msgbox EuropeGermany_Text_Directions
	goto EuropeGermany_End
EuropeGermany_Badges::
	msgbox EuropeGermany_Text_Badges
	goto EuropeGermany_End
EuropeGermany_Decline::
	msgbox EuropeGermany_Text_Decline
	goto EuropeGermany_End
EuropeGermany_Reward::
	checkitemspace ITEM_MAGNET, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeGermany_Full
	msgbox EuropeGermany_Text_Reward
	giveitem ITEM_MAGNET, 1
	setvar VAR_EUROPE_GERMANY_STORY, 3
EuropeGermany_Complete::
	msgbox EuropeGermany_Text_Complete
	goto EuropeGermany_End
EuropeGermany_Full::
	msgbox EuropeGermany_Text_Full
EuropeGermany_End::
	release
	end

EuropeGermany_Karl::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_GERMANY_STORY, 0, EuropeGermany_NotStarted
	goto_if_eq VAR_EUROPE_GERMANY_STORY, 3, EuropeGermany_KarlComplete
	goto_if_eq VAR_EUROPE_GERMANY_STORY, 2, EuropeGermany_Return
	msgbox EuropeGermany_Text_Delivered
	setvar VAR_EUROPE_GERMANY_STORY, 2
EuropeGermany_Return::
	msgbox EuropeGermany_Text_Return
	goto EuropeGermany_End
EuropeGermany_NotStarted::
	msgbox EuropeGermany_Text_NotStarted
	goto EuropeGermany_End
EuropeGermany_KarlComplete::
	msgbox EuropeGermany_Text_KarlComplete
	goto EuropeGermany_End

EuropeGermany_Text_Offer::
	.string "I'm LENA, a signal engineer.\n"
	.string "Two badges! You know these routes.\p"
	.string "KARL needs parts for a woodland\n"
	.string "trail beacon near ORANIENBURG.\p"
	.string "Will you deliver a repair parcel?$"

EuropeGermany_Text_Accepted::
	.string "You packed LENA's repair parcel!\n"
	.string "Mission cargo stays outside the BAG.\p"
	.string "Find KARL west of ORANIENBURG's\n"
	.string "town guide, then bring his report.$"

EuropeGermany_Text_Directions::
	.string "KARL waits west of ORANIENBURG's\n"
	.string "town guide with the damaged beacon.\p"
	.string "Take the train, or walk north\n"
	.string "through BERLIN WOODLAND and HAVEL.\p"
	.string "Your repair parcel is packed.\n"
	.string "Bring his report back to me!$"

EuropeGermany_Text_Badges::
	.string "I need a courier for a trail repair.\n"
	.string "First, earn two GYM badges.\p"
	.string "Visit ELLIS in OXFORD, then MARINE\n"
	.string "in CHANTILLY after their studies.$"

EuropeGermany_Text_Decline::
	.string "No hurry. The main paths are open.\n"
	.string "Come back when you're ready!$"

EuropeGermany_Text_Reward::
	.string "LENA: KARL restored the beacon!\n"
	.string "Reliable signals help companions\p"
	.string "find safe paths. A faulty relay at\n"
	.string "the REICHSTAG needs attention too.\p"
	.string "This MAGNET is for your team.$"

EuropeGermany_Text_Complete::
	.string "Let a partner hold the MAGNET\n"
	.string "to boost its ELECTRIC-type moves.\p"
	.string "Our repaired beacon helps travelers\n"
	.string "find the trail in fading light.\p"
	.string "Try CONRAD at ORANIENBURG GYM.\n"
	.string "Look north of the town square!$"

EuropeGermany_Text_Full::
	.string "Your report is delivered, but your\n"
	.string "BAG's ITEMS pocket is full.\p"
	.string "Make room and speak to me again.\n"
	.string "I'll keep your MAGNET safe.$"

EuropeGermany_Text_Delivered::
	.string "KARL: The repair parts from LENA!\n"
	.string "Now I can fix this trail beacon.\p"
	.string "A fresh coil and a tight connection\n"
	.string "should bring its light back.\p"
	.string "There! The beacon is working again.\n"
	.string "You received KARL's repair report.$"

EuropeGermany_Text_Return::
	.string "Take my report to LENA in BERLIN.\n"
	.string "She waits west of the city guide.\p"
	.string "Use the train, or walk south along\n"
	.string "HAVEL TRAIL and BERLIN WOODLAND.$"

EuropeGermany_Text_NotStarted::
	.string "I'm KARL. I maintain trail beacons.\n"
	.string "This one needs a replacement coil.\p"
	.string "LENA in BERLIN is preparing parts.\n"
	.string "Ask her west of the city guide.$"

EuropeGermany_Text_KarlComplete::
	.string "KARL: LENA received my report.\n"
	.string "The beacon is ready for the trail.\p"
	.string "CONRAD awaits at our GYM!$"
