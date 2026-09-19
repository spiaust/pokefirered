@ The city guide owns the field lock before entering these scripts.
EuropeTour_London::
	goto_if_eq VAR_EUROPE_STAMP_LONDON, 1, EuropeTour_CheckProgress
	msgbox EuropeTour_Text_London
	setvar VAR_EUROPE_STAMP_LONDON, 1
	goto EuropeTour_CheckProgress

EuropeTour_Paris::
	goto_if_eq VAR_EUROPE_STAMP_PARIS, 1, EuropeTour_CheckProgress
	msgbox EuropeTour_Text_Paris
	setvar VAR_EUROPE_STAMP_PARIS, 1
	goto EuropeTour_CheckProgress

EuropeTour_Berlin::
	goto_if_eq VAR_EUROPE_STAMP_BERLIN, 1, EuropeTour_CheckProgress
	msgbox EuropeTour_Text_Berlin
	setvar VAR_EUROPE_STAMP_BERLIN, 1
	goto EuropeTour_CheckProgress

EuropeTour_CheckProgress::
	goto_if_eq VAR_EUROPE_TOUR_REWARDED, 1, EuropeTour_Complete
	setvar VAR_0x8005, 0
	call_if_eq VAR_EUROPE_STAMP_LONDON, 1, EuropeTour_CountStamp
	call_if_eq VAR_EUROPE_STAMP_PARIS, 1, EuropeTour_CountStamp
	call_if_eq VAR_EUROPE_STAMP_BERLIN, 1, EuropeTour_CountStamp
	goto_if_eq VAR_0x8005, 3, EuropeTour_Reward
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox EuropeTour_Text_Progress
	call_if_eq VAR_EUROPE_STAMP_LONDON, 0, EuropeTour_MissingLondon
	call_if_eq VAR_EUROPE_STAMP_PARIS, 0, EuropeTour_MissingParis
	call_if_eq VAR_EUROPE_STAMP_BERLIN, 0, EuropeTour_MissingBerlin
	release
	end

EuropeTour_CountStamp::
	addvar VAR_0x8005, 1
	return

EuropeTour_MissingLondon::
	msgbox EuropeTour_Text_MissingLondon
	return

EuropeTour_MissingParis::
	msgbox EuropeTour_Text_MissingParis
	return

EuropeTour_MissingBerlin::
	msgbox EuropeTour_Text_MissingBerlin
	return

EuropeTour_Reward::
	checkitemspace ITEM_EXP_SHARE, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeTour_BagFull
	msgbox EuropeTour_Text_Reward
	giveitem ITEM_EXP_SHARE, 1
	setvar VAR_EUROPE_TOUR_REWARDED, 1
	goto EuropeTour_Complete

EuropeTour_BagFull::
	msgbox EuropeTour_Text_BagFull
	release
	end

EuropeTour_Complete::
	msgbox EuropeTour_Text_Complete
	call EuropeTrail_Report
	release
	end

EuropeTour_Text_London::
	.string "A LONDON stamp for your tour!\p"
	.string "The Thames runs through this city.\n"
	.string "Its bridges link the two banks.$"

EuropeTour_Text_Paris::
	.string "A PARIS stamp for your tour!\p"
	.string "The Seine flows through PARIS.\n"
	.string "Its banks are lovely for a walk.$"

EuropeTour_Text_Berlin::
	.string "A BERLIN stamp for your tour!\p"
	.string "The Spree flows through BERLIN.\n"
	.string "There are many parks to explore.$"

EuropeTour_Text_Progress::
	.string "Tour stamps: {STR_VAR_1} of 3!\p"
	.string "Meet the guide in each city square.\n"
	.string "All three stamps earn EXP. SHARE!\p"
	.string "Take the train from the station\n"
	.string "to find your next guide.$"

EuropeTour_Text_MissingLondon::
	.string "You still need the LONDON stamp.$"

EuropeTour_Text_MissingParis::
	.string "You still need the PARIS stamp.$"

EuropeTour_Text_MissingBerlin::
	.string "You still need the BERLIN stamp.$"

EuropeTour_Text_Reward::
	.string "All three stamps! You've completed\n"
	.string "your first European Tour!\p"
	.string "Here is your EXP. SHARE.\n"
	.string "Raise a new traveling partner!$"

EuropeTour_Text_BagFull::
	.string "All three stamps are safe!\n"
	.string "Your BAG's ITEMS pocket is full.\p"
	.string "Make room, then ask any city guide\n"
	.string "for your EXP. SHARE.$"

EuropeTour_Text_Complete::
	.string "Your three-city tour is complete!\p"
	.string "Give EXP. SHARE to a POKEMON.\n"
	.string "It gains EXP. even without battling.\p"
	.string "Keep exploring the countryside\n"
	.string "and meeting new partners!$"
