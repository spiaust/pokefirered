@ A fixed return anchor keeps past-world progress independent of present quests.
EuropeTime_Depart::
	goto_if_eq VAR_EUROPE_PORT_ACCOUNT, 1, EuropeTime_ReturnVisit
	msgbox EuropeTime_Text_Depart, MSGBOX_YESNO
EuropeTime_DepartChoice::
	goto_if_eq VAR_RESULT, NO, EuropeTime_Stay
	goto_if_eq VAR_EUROPE_PORT_ACCOUNT, 1, EuropeTime_Destinations
EuropeTime_Refuge::
	msgbox EuropeTime_Text_Crossing
	closemessage
	compare VAR_EUROPE_PAST_STORY, 0
	call_if_eq EuropeTime_FirstVisit
	warp MAP_EUROPE_CHANTILLY_PAST, 5, 10
	waitstate
	releaseall
	end
EuropeTime_FirstVisit::
	setvar VAR_EUROPE_PAST_STORY, 1
	return
EuropeTime_ReturnVisit::
	goto_if_eq VAR_EUROPE_LUGGAGE, 3, EuropeTime_SouthVisit
	msgbox EuropeTime_Text_ReturnVisit, MSGBOX_YESNO
	goto EuropeTime_DepartChoice
EuropeTime_SouthVisit::
	msgbox EuropeTime_Text_SouthVisit, MSGBOX_YESNO
	goto EuropeTime_DepartChoice
EuropeTime_Destinations::
	msgbox EuropeTime_Text_Destinations
	goto_if_eq VAR_EUROPE_LUGGAGE, 3, EuropeTime_SouthMenu
	multichoice 12, 1, MULTICHOICE_EUROPE_PAST, FALSE
	goto EuropeTime_DestinationChoice
EuropeTime_SouthMenu::
	multichoice 10, 1, MULTICHOICE_EUROPE_PAST_SOUTH, FALSE
EuropeTime_DestinationChoice::
	goto_if_eq VAR_RESULT, 0, EuropeTime_Refuge
	goto_if_eq VAR_RESULT, 2, EuropeTime_SouthDestination
	goto_if_ne VAR_RESULT, 1, EuropeTime_Stay
	msgbox EuropeTime_Text_Crossing
	closemessage
	warp MAP_EUROPE_LE_HAVRE_PAST, 8, 5
	waitstate
	releaseall
	end
EuropeTime_SouthDestination::
	goto_if_ne VAR_EUROPE_LUGGAGE, 3, EuropeTime_Stay
	msgbox EuropeTime_Text_Crossing
	closemessage
	warp MAP_EUROPE_SOUTHAMPTON_PAST, 8, 5
	waitstate
	releaseall
	end
EuropeTime_Return::
	lock
	faceplayer
	msgbox EuropeTime_Text_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeTime_Stay
	msgbox EuropeTime_Text_Crossing
	closemessage
	warp MAP_EUROPE_CHANTILLY_TRAIL, 15, 24
	waitstate
	releaseall
	end
EuropeTime_Stay::
	msgbox EuropeTime_Text_Stay
	release
	end

EuropeTime_Child::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_PAST_STORY, 4, EuropeTime_ChildSafe
	goto_if_eq VAR_EUROPE_PAST_STORY, 3, EuropeTime_Deliver
	msgbox EuropeTime_Text_Child
	showmonpic SPECIES_EEVEE, 10, 3
	waitbuttonpress
	hidemonpic
	setvar VAR_EUROPE_PAST_STORY, 2
	msgbox EuropeTime_Text_AskKeeper
	goto EuropeCelebi_End
EuropeTime_Deliver::
	msgbox EuropeTime_Text_Deliver
	setvar VAR_EUROPE_PAST_STORY, 4
EuropeTime_ChildSafe::
	goto_if_eq VAR_EUROPE_DEPARTURE_STORY, 4, EuropeDeparture_ChildDone
	msgbox EuropeTime_Text_Safe
	goto EuropeCelebi_End
EuropeTime_Keeper::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_PAST_STORY, 4, EuropeTime_KeeperDone
	goto_if_eq VAR_EUROPE_PAST_STORY, 3, EuropeTime_Carry
	goto_if_eq VAR_EUROPE_PAST_STORY, 2, EuropeTime_Blanket
	msgbox EuropeTime_Text_Welcome
	goto EuropeCelebi_End
EuropeTime_Blanket::
	msgbox EuropeTime_Text_Blanket
	setvar VAR_EUROPE_PAST_STORY, 3
EuropeTime_Carry::
	msgbox EuropeTime_Text_Carry
	goto EuropeCelebi_End
EuropeTime_KeeperDone::
	goto_if_eq VAR_EUROPE_DEPARTURE_STORY, 3, EuropeDeparture_Report
	goto_if_eq VAR_EUROPE_DEPARTURE_STORY, 4, EuropeDeparture_RefugeDone
	msgbox EuropeTime_Text_KeeperDone
	goto EuropeCelebi_End
EuropeTime_Sign::
	msgbox EuropeTime_Text_Sign, MSGBOX_SIGN
	end

EuropeTime_Text_Depart::
	.string "CELEBI offers to lead you through\n"
	.string "time to CHANTILLY in 1940.\p"
	.string "It will wait where you arrive.\n"
	.string "Speak to it there to return here.\p"
	.string "Your rail booking stays saved.\n"
	.string "Travel to the past?$"
EuropeTime_Text_ReturnVisit::
	.string "CELEBI remembers the port visit\n"
	.string "you recorded with ADA.\p"
	.string "It can now lead you to the refuge\n"
	.string "or straight to LE HAVRE.\p"
	.string "Travel to the past?$"
EuropeTime_Text_Destinations::
	.string "Where would you like to return?\n"
	.string "These places are all in 1940.$"
EuropeTime_Text_SouthVisit::
	.string "CELEBI can now lead you straight\n"
	.string "to SOUTHAMPTON reception, too.\p"
	.string "The refuge and LE HAVRE remain\n"
	.string "available as return points.\p"
	.string "Travel to the past?$"
EuropeTime_Text_Return::
	.string "CELEBI can take you back to the\n"
	.string "present-day forest now.\p"
	.string "Your work here will be remembered.\n"
	.string "Return to the present?$"
EuropeTime_Text_Crossing::
	.string "CELEBI's light surrounds your team.\n"
	.string "The world falls silent for a moment.$"
EuropeTime_Text_Stay::
	.string "CELEBI stays beside you.\n"
	.string "Speak to it when you're ready.$"
EuropeTime_Text_Child::
	.string "I'm ELISE. We're waiting for news\n"
	.string "of a train away from the fighting.\p"
	.string "My EEVEE is cold and frightened.\n"
	.string "I promised we would stay together.$"
EuropeTime_Text_AskKeeper::
	.string "Could you ask the refuge keeper\n"
	.string "beside me for something warm?$"
EuropeTime_Text_Welcome::
	.string "This courtyard is a station refuge.\n"
	.string "Families and POKEMON wait here.\p"
	.string "The little girl beside me seems\n"
	.string "worried. Please speak with her.$"
EuropeTime_Text_Blanket::
	.string "A blanket for EEVEE? Of course.\n"
	.string "Take this one to ELISE.\p"
	.string "You fold the blanket into your arms.$"
EuropeTime_Text_Carry::
	.string "ELISE is beside me. Please take\n"
	.string "the blanket to her and EEVEE.$"
EuropeTime_Text_Deliver::
	.string "ELISE wraps EEVEE in the blanket.\n"
	.string "It snuggles close and settles down.$"
EuropeTime_Text_Safe::
	.string "ELISE: Thank you! EEVEE is warmer.\n"
	.string "We can wait together now.\p"
	.string "The keeper is looking after us.\n"
	.string "I hope we meet again.$"
EuropeTime_Text_KeeperDone::
	.string "Thank you for helping ELISE.\n"
	.string "I'll keep them both safe here.\p"
	.string "The guide at the southeast corner\n"
	.string "can take you to the station post.\p"
	.string "Please bring back departure news.\n"
	.string "CELEBI can take you home any time.$"
EuropeTime_Text_Sign::
	.string "CHANTILLY STATION REFUGE - 1940\p"
	.string "Wait here for news of departures.\n"
	.string "Keep your POKEMON close.$"
