@ Rental water rides use normal surfing state inferred from the arrival tile.
EuropeRide_London::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE03_GET, EuropeRide_Locked
	call EuropeRide_Offer
	goto_if_eq VAR_RESULT, NO, EuropeRide_Decline
	msgbox EuropeRide_Text_Board
	closemessage
	warp MAP_EUROPE_LONDON, 26, 19
	waitstate
	releaseall
	end
EuropeRide_Oxford::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE03_GET, EuropeRide_Locked
	call EuropeRide_Offer
	goto_if_eq VAR_RESULT, NO, EuropeRide_Decline
	msgbox EuropeRide_Text_Board
	closemessage
	warp MAP_EUROPE_OXFORD, 26, 19
	waitstate
	releaseall
	end
EuropeRide_Offer::
	msgbox EuropeRide_Text_Intro
	showmonpic SPECIES_LAPRAS, 10, 3
	waitbuttonpress
	hidemonpic
	msgbox EuropeRide_Text_Offer, MSGBOX_YESNO
	return
EuropeRide_Locked::
	msgbox EuropeRide_Text_Locked
	goto EuropeRide_End
EuropeRide_Decline::
	msgbox EuropeRide_Text_Decline
EuropeRide_End::
	release
	end

EuropeRide_Text_Intro::
	.string "Our LAPRAS love giving river rides!\n"
	.string "THUNDERBADGE holders ride for free.$"

EuropeRide_Text_Offer::
	.string "Steer with the direction buttons.\n"
	.string "Move onto the bank to dismount.\p"
	.string "No HM or party space is needed.\n"
	.string "Your rail booking stays saved.\p"
	.string "Would you like to borrow a LAPRAS?$"

EuropeRide_Text_Board::
	.string "LAPRAS is ready! Enjoy the water.\n"
	.string "Return to any clear bank to get off.$"

EuropeRide_Text_Locked::
	.string "We lend LAPRAS for river rides.\n"
	.string "Earn CONRAD's THUNDERBADGE first.\p"
	.string "Then you can steer on the water\n"
	.string "without teaching SURF to a partner!$"

EuropeRide_Text_Decline::
	.string "Come back whenever you'd like a ride!$"
