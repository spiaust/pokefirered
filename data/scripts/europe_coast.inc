@ Channel crossing and coach connections. Existing rail bookings are preserved.
EuropeCoast_LondonCoach::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE03_GET, EuropeCoast_Locked
	msgbox EuropeCoast_Text_LondonCoach, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeCoast_Decline
	msgbox EuropeCoast_Text_CoachDepart
	closemessage
	warp MAP_EUROPE_DOVER_PORT, 8, 5
	waitstate
	releaseall
	end
EuropeCoast_DoverCaptain::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE03_GET, EuropeCoast_Locked
	msgbox EuropeCoast_Text_DoverOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeCoast_Decline
	msgbox EuropeCoast_Text_Sail
	closemessage
	playse SE_DING_DONG
	warp MAP_EUROPE_CALAIS_PORT, 8, 5
	waitstate
	releaseall
	end
EuropeCoast_ParisCoach::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE03_GET, EuropeCoast_Locked
	msgbox EuropeCoast_Text_ParisCoach, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeCoast_Decline
	msgbox EuropeCoast_Text_CoachDepart
	closemessage
	warp MAP_EUROPE_CALAIS_PORT, 8, 5
	waitstate
	releaseall
	end
EuropeCoast_CalaisCaptain::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE03_GET, EuropeCoast_Locked
	msgbox EuropeCoast_Text_CalaisOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeCoast_Decline
	msgbox EuropeCoast_Text_Sail
	closemessage
	playse SE_DING_DONG
	warp MAP_EUROPE_DOVER_PORT, 8, 5
	waitstate
	releaseall
	end
EuropeCoast_Locked::
	msgbox EuropeCoast_Text_Locked
	goto EuropeCoast_End
EuropeCoast_Decline::
	msgbox EuropeCoast_Text_Decline
EuropeCoast_End::
	release
	end

EuropeCoast_Text_LondonCoach::
	.string "Our coach goes to DOVER PORT.\n"
	.string "There, a ferry sails to CALAIS.\p"
	.string "THUNDERBADGE holders travel free.\n"
	.string "Your rail booking stays saved.\p"
	.string "Take the coach to DOVER?$"

EuropeCoast_Text_ParisCoach::
	.string "Our coach goes to CALAIS PORT.\n"
	.string "There, a ferry sails to DOVER.\p"
	.string "THUNDERBADGE holders travel free.\n"
	.string "Your rail booking stays saved.\p"
	.string "Take the coach to CALAIS?$"

EuropeCoast_Text_DoverOffer::
	.string "Welcome to DOVER PORT in ENGLAND!\n"
	.string "This ferry sails to CALAIS, FRANCE.\p"
	.string "For LONDON, leave through the north\n"
	.string "exit to catch the return coach.\p"
	.string "The crossing is free. Rail trips\n"
	.string "stay booked. Sail to CALAIS?$"

EuropeCoast_Text_CalaisOffer::
	.string "Welcome to CALAIS PORT in FRANCE!\n"
	.string "This ferry sails to DOVER, ENGLAND.\p"
	.string "For PARIS, leave through the north\n"
	.string "exit to catch the return coach.\p"
	.string "The crossing is free. Rail trips\n"
	.string "stay booked. Sail to DOVER?$"

EuropeCoast_Text_CoachDepart::
	.string "All aboard the coastal coach!\n"
	.string "The north port exit brings you back.$"

EuropeCoast_Text_Sail::
	.string "All aboard! Next stop: the coast\n"
	.string "on the other side of the Channel.$"

EuropeCoast_Text_Locked::
	.string "Our coaches and coastal ferries\n"
	.string "welcome THUNDERBADGE holders.\p"
	.string "Earn CONRAD's badge in ORANIENBURG.\n"
	.string "The regular trains are open now!$"

EuropeCoast_Text_Decline::
	.string "Take your time. We'll be here.\n"
	.string "Your saved rail trip is unchanged.$"
