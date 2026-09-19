EuropeNavigation_Board::
	lockall
	goto_if_questlog EventScript_ReleaseEnd
	checkitem ITEM_TOWN_MAP, 1
	goto_if_eq VAR_RESULT, TRUE, EuropeNavigation_View
	giveitem ITEM_TOWN_MAP, 1
EuropeNavigation_View::
	checkitem ITEM_FAME_CHECKER, 1
	goto_if_eq VAR_RESULT, TRUE, EuropeNavigation_Open
	giveitem ITEM_FAME_CHECKER, 1
EuropeNavigation_Open::
	msgbox EuropeNavigation_Text_Board
	fadescreen FADE_TO_BLACK
	special ShowTownMap
	waitstate
	releaseall
	end

EuropeNavigation_Text_Board::
	.string "EUROPEAN TRAVEL MAP\p"
	.string "Browse cities with LEFT and RIGHT.\n"
	.string "Press B to return to your journey.$"
