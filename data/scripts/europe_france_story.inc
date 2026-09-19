@ France chapter one: either-order field observations, then a reviewed report.
EuropeFrance_Celine::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 6, EuropeFrance_Complete
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 5, EuropeFrance_Reward
	goto_if_ne VAR_EUROPE_FRANCE_STORY, 0, EuropeFrance_Progress
	goto_if_unset FLAG_BADGE01_GET, EuropeFrance_FirstBadge
	msgbox EuropeFrance_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeFrance_Decline
	setvar VAR_EUROPE_FRANCE_STORY, 1
	msgbox EuropeFrance_Text_Accepted
	goto EuropeFrance_End
EuropeFrance_FirstBadge::
	msgbox EuropeFrance_Text_FirstBadge
	goto EuropeFrance_End
EuropeFrance_Decline::
	msgbox EuropeFrance_Text_Decline
	goto EuropeFrance_End
EuropeFrance_Progress::
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 2, EuropeFrance_NeedForest
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 3, EuropeFrance_NeedGardens
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 4, EuropeFrance_NeedReview
	msgbox EuropeFrance_Text_BothSites
	goto EuropeFrance_End
EuropeFrance_NeedForest::
	msgbox EuropeFrance_Text_NeedForest
	goto EuropeFrance_End
EuropeFrance_NeedGardens::
	msgbox EuropeFrance_Text_NeedGardens
	goto EuropeFrance_End
EuropeFrance_NeedReview::
	msgbox EuropeFrance_Text_NeedReview
	goto EuropeFrance_End
EuropeFrance_Reward::
	checkitemspace ITEM_MIRACLE_SEED, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeFrance_BagFull
	msgbox EuropeFrance_Text_Reward
	giveitem ITEM_MIRACLE_SEED, 1
	setvar VAR_EUROPE_FRANCE_STORY, 6
EuropeFrance_Complete::
	msgbox EuropeFrance_Text_Complete
	goto EuropeFrance_End
EuropeFrance_BagFull::
	msgbox EuropeFrance_Text_BagFull
EuropeFrance_End::
	release
	end

EuropeFrance_Remy::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 0, EuropeFrance_NotStarted
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 6, EuropeFrance_RemyComplete
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 5, EuropeFrance_ReturnReport
	goto_if_ne VAR_EUROPE_FRANCE_STORY, 4, EuropeFrance_Progress
	msgbox EuropeFrance_Text_Review
	setvar VAR_EUROPE_FRANCE_STORY, 5
EuropeFrance_ReturnReport::
	msgbox EuropeFrance_Text_ReturnReport
	goto EuropeFrance_End
EuropeFrance_NotStarted::
	msgbox EuropeFrance_Text_NotStarted
	goto EuropeFrance_End
EuropeFrance_RemyComplete::
	msgbox EuropeFrance_Text_RemyComplete
	goto EuropeFrance_End

EuropeFrance_Gardens::
	lockall
	msgbox EuropeFrance_Text_Gardens
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 0, EuropeFrance_MarkerInactive
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 1, EuropeFrance_RecordGardens
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 3, EuropeFrance_RecordBoth
	goto EuropeFrance_MarkerRecorded
EuropeFrance_RecordGardens::
	setvar VAR_EUROPE_FRANCE_STORY, 2
	goto EuropeFrance_NoteSaved
EuropeFrance_Forest::
	lockall
	msgbox EuropeFrance_Text_Forest
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 0, EuropeFrance_MarkerInactive
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 1, EuropeFrance_RecordForest
	goto_if_eq VAR_EUROPE_FRANCE_STORY, 2, EuropeFrance_RecordBoth
	goto EuropeFrance_MarkerRecorded
EuropeFrance_RecordForest::
	setvar VAR_EUROPE_FRANCE_STORY, 3
	goto EuropeFrance_NoteSaved
EuropeFrance_RecordBoth::
	setvar VAR_EUROPE_FRANCE_STORY, 4
EuropeFrance_NoteSaved::
	msgbox EuropeFrance_Text_NoteSaved
	releaseall
	end
EuropeFrance_MarkerRecorded::
	msgbox EuropeFrance_Text_MarkerRecorded
	releaseall
	end
EuropeFrance_MarkerInactive::
	msgbox EuropeFrance_Text_MarkerInactive
	releaseall
	end

EuropeFrance_Text_Offer::
	.string "I'm CELINE, a botanist. Your badge\n"
	.string "shows you can care for a team.\p"
	.string "Our gardens and forests welcome\n"
	.string "different POKEMON. Let's study why!\p"
	.string "Will you help with our garden survey?$"
EuropeFrance_Text_Accepted::
	.string "Read the two study markers beside\n"
	.string "the main paths, in either order.\p"
	.string "One is in FRENCH GARDENS. The other\n"
	.string "is in CHANTILLY FOREST's clearing.\p"
	.string "Then meet REMY in CHANTILLY's square.\n"
	.string "Bring his reviewed report to me.$"
EuropeFrance_Text_FirstBadge::
	.string "I'm CELINE. I study the gardens\n"
	.string "and forests of FRANCE.\p"
	.string "Earn your first badge at OXFORD GYM,\n"
	.string "then help with our field survey!$"
EuropeFrance_Text_Decline::
	.string "Come back when you're ready.\n"
	.string "There is always more to observe!$"
EuropeFrance_Text_BothSites::
	.string "Read both study markers beside the\n"
	.string "paths through the French routes.\p"
	.string "FRENCH GARDENS is north of PARIS.\n"
	.string "CHANTILLY FOREST lies beyond it.$"
EuropeFrance_Text_NeedForest::
	.string "Your garden notes are recorded.\p"
	.string "Find the study marker in the\n"
	.string "middle of CHANTILLY FOREST.\p"
	.string "Then visit REMY in CHANTILLY.$"
EuropeFrance_Text_NeedGardens::
	.string "Your forest notes are recorded.\p"
	.string "Read the FRENCH GARDENS study marker\n"
	.string "beside the path north of PARIS.\p"
	.string "Then visit REMY in CHANTILLY.$"
EuropeFrance_Text_NeedReview::
	.string "Both sites are recorded! Take your\n"
	.string "notes to REMY in CHANTILLY's square.\p"
	.string "He waits west of the town guide.$"
EuropeFrance_Text_NotStarted::
	.string "I'm REMY, a gardener. CELINE in\n"
	.string "PARIS is organizing a field survey.\p"
	.string "Speak to her west of the city guide.$"
EuropeFrance_Text_Review::
	.string "REMY: Sunlit gardens shelter ODDISH.\n"
	.string "The forest offers cover for bugs.\p"
	.string "Different places support different\n"
	.string "partners. Your notes show us both!\p"
	.string "I've reviewed your survey report.$"
EuropeFrance_Text_ReturnReport::
	.string "Take the reviewed report to CELINE\n"
	.string "in PARIS. Walk south or use the train.$"
EuropeFrance_Text_Reward::
	.string "CELINE: REMY's report is excellent!\n"
	.string "Thank you for visiting both sites.\p"
	.string "This MIRACLE SEED is for your team.$"
EuropeFrance_Text_Complete::
	.string "The French garden survey is complete!\p"
	.string "Let a partner hold MIRACLE SEED\n"
	.string "to strengthen its GRASS-type moves.\p"
	.string "MARINE awaits at CHANTILLY GYM.\n"
	.string "Look north of the town square!$"
EuropeFrance_Text_RemyComplete::
	.string "REMY: CELINE received your report.\n"
	.string "Try MARINE at CHANTILLY GYM next!$"
EuropeFrance_Text_BagFull::
	.string "Your survey is complete, but your\n"
	.string "BAG's ITEMS pocket is full.\p"
	.string "Make room and return to CELINE.\n"
	.string "Your MIRACLE SEED will be waiting!$"
EuropeFrance_Text_Gardens::
	.string "FRENCH GARDENS STUDY MARKER\p"
	.string "Light reaches the low plants here.\n"
	.string "ODDISH shelters among the leaves.$"
EuropeFrance_Text_Forest::
	.string "CHANTILLY FOREST STUDY MARKER\p"
	.string "Trees shelter the plants below.\n"
	.string "CATERPIE hides among their leaves.$"
EuropeFrance_Text_NoteSaved::
	.string "You recorded this site's notes!\n"
	.string "REMY in CHANTILLY reviews both.$"
EuropeFrance_Text_MarkerRecorded::
	.string "This site's notes are already\n"
	.string "recorded in your survey.$"
EuropeFrance_Text_MarkerInactive::
	.string "Ask CELINE in PARIS about the survey.$"
