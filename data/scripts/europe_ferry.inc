@ Direct riverboat trips; rail itineraries are deliberately untouched.
EuropeFerry_London::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE03_GET, EuropeFerry_Locked
	msgbox EuropeFerry_Text_ToOxford, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeFerry_Decline
	msgbox EuropeFerry_Text_Depart
	closemessage
	playse SE_DING_DONG
	warp MAP_EUROPE_OXFORD, 24, 16
	waitstate
	releaseall
	end
EuropeFerry_Oxford::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE03_GET, EuropeFerry_Locked
	msgbox EuropeFerry_Text_ToLondon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeFerry_Decline
	msgbox EuropeFerry_Text_Depart
	closemessage
	playse SE_DING_DONG
	warp MAP_EUROPE_LONDON, 24, 16
	waitstate
	releaseall
	end
EuropeFerry_Locked::
	msgbox EuropeFerry_Text_Locked
	goto EuropeFerry_End
EuropeFerry_Decline::
	msgbox EuropeFerry_Text_Decline
EuropeFerry_End::
	release
	end
EuropeFerry_LondonSign::
	msgbox EuropeFerry_Text_LondonSign, MSGBOX_SIGN
	end
EuropeFerry_OxfordSign::
	msgbox EuropeFerry_Text_OxfordSign, MSGBOX_SIGN
	end

EuropeFerry_Text_ToOxford::
	.string "Welcome to the riverboat landing!\n"
	.string "We sail directly to OXFORD.\p"
	.string "With your THUNDERBADGE, it's free.\n"
	.string "Any saved rail trip stays booked.\p"
	.string "Board the boat to OXFORD?$"

EuropeFerry_Text_ToLondon::
	.string "Welcome to the riverboat landing!\n"
	.string "We sail directly to LONDON.\p"
	.string "With your THUNDERBADGE, it's free.\n"
	.string "Any saved rail trip stays booked.\p"
	.string "Board the boat to LONDON?$"

EuropeFerry_Text_Depart::
	.string "All aboard! Enjoy the river crossing.$"

EuropeFerry_Text_Locked::
	.string "Our riverboats link LONDON\n"
	.string "and OXFORD.\p"
	.string "Earn the THUNDERBADGE from CONRAD\n"
	.string "in ORANIENBURG to ride for free.\p"
	.string "The trains and walking routes\n"
	.string "are open while you train!$"

EuropeFerry_Text_Decline::
	.string "We'll be here when you're ready.\n"
	.string "Your travel plans are unchanged.$"

EuropeFerry_Text_LondonSign::
	.string "LONDON RIVERBOAT LANDING\n"
	.string "Direct boat to OXFORD.\p"
	.string "Speak to the captain by the water.\n"
	.string "THUNDERBADGE holders ride free.\p"
	.string "LAPRAS rentals: beside the captain.$"

EuropeFerry_Text_OxfordSign::
	.string "OXFORD RIVERBOAT LANDING\n"
	.string "Direct boat to LONDON.\p"
	.string "Speak to the captain by the water.\n"
	.string "THUNDERBADGE holders ride free.\p"
	.string "LAPRAS rentals: beside the captain.$"
