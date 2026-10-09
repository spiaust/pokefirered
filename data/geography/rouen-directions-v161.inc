EuropeRouenPast_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeRouen_OnTransition
	map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, EuropeRouenBook_Restore
	.byte 0
EuropeRouen_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	goto EuropeRouenBook_Restore
EuropeRouen_Offer::
	msgbox EuropeRouen_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiens_Stay
	msgbox EuropeRouen_Text_Journey
	compare VAR_EUROPE_ROUEN_STORY, 0
	call_if_eq EuropeRouen_FirstVisit
	closemessage
	warp MAP_EUROPE_ROUEN_PAST, 10, 16
	waitstate
	releaseall
	end
EuropeRouen_FirstVisit::
	setvar VAR_EUROPE_ROUEN_STORY, 1
	return
EuropeRouen_Return::
	lock
	faceplayer
	msgbox EuropeRouen_Text_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiens_Stay
	closemessage
	warp MAP_EUROPE_AMIENS_PAST, 10, 16
	waitstate
	releaseall
	end
EuropeRouen_Leon::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_ROUEN_STORY, 2, EuropeRouenBook_Leon
	msgbox EuropeRouen_Text_Welcome
	setvar VAR_EUROPE_ROUEN_STORY, 2
EuropeRouen_Welcomed::
	msgbox EuropeRouen_Text_Welcomed
	goto EuropeCelebi_End
EuropeRouen_Notice::
	lockall
	msgbox EuropeRouen_Text_Notice
	goto EuropeAmiens_NoticeEnd
EuropeRouen_DepartureNotice::
	msgbox EuropeRouen_Text_DepartureNotice
	goto EuropeAmiens_NoticeEnd
EuropeRouen_Text_Offer::
	.string "NORA has the waiting plan. Now a\n"
	.string "service to ROUEN has been confirmed.\p"
	.string "LEON will meet you at reception.\n"
	.string "A guide there can bring you back.\p"
	.string "Travel to ROUEN?$"
EuropeRouen_Text_Journey::
	.string "You board the onward train.\n"
	.string "Fields pass beyond the window.\p"
	.string "At ROUEN, a guide leads you into\n"
	.string "a quiet reception courtyard.$"
EuropeRouen_Text_Return::
	.string "I can take you back to AMIENS.\n"
	.string "NORA's care corner is still open.\p"
	.string "Take the return service?$"
EuropeRouen_Text_Welcome::
	.string "LEON: Welcome to ROUEN. You came\n"
	.string "from NORA's reception in AMIENS?\p"
	.string "We keep arrivals together here.\n"
	.string "I will record where you came from.\p"
	.string "There is no need to rush away.\n"
	.string "Take a moment to find your bearings.$"
EuropeRouen_Text_Welcomed::
	.string "LEON: Your arrival is recorded.\n"
	.string "The south guide returns to AMIENS.\p"
	.string "Your green companion is waiting\n"
	.string "beside the path where you arrived.$"
EuropeRouen_Text_Notice::
	.string "ROUEN RECEPTION - 1940\p"
	.string "Report to LEON on the west path.\n"
	.string "Keep your traveling group together.\p"
	.string "The east path reaches the riverside.\n"
	.string "Use the paved crossing to walk over.\p"
	.string "Ask the south guide about returning\n"
	.string "to AMIENS. There is no charge.$"
EuropeRouen_Text_DepartureNotice::
	.string "ONWARD SERVICE: ROUEN\p"
	.string "The porter on the east side can\n"
	.string "help you board the confirmed train.\p"
	.string "Return services remain available.$"

EuropeRouenPast_RealismCathedral::
	msgbox EuropeRouenPast_RealismCathedralText, MSGBOX_SIGN
	end

EuropeRouenPast_RealismCathedralText::
	.string "NOTRE-DAME DE ROUEN\n"
	.string "The cathedral north of the SEINE.$"

EuropeRouenPast_RealismClock::
	msgbox EuropeRouenPast_RealismClockText, MSGBOX_SIGN
	end

EuropeRouenPast_RealismClockText::
	.string "GROS-HORLOGE\n"
	.string "The clock west of the cathedral.$"

EuropeRouenPast_RealismSeine::
	msgbox EuropeRouenPast_RealismSeineText, MSGBOX_SIGN
	end

EuropeRouenPast_RealismSeineText::
	.string "SEINE QUAYS\n"
	.string "Follow the paths along both banks.$"
