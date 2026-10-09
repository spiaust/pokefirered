EuropeBeauvaisGarden_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeGarden_OnTransition
	map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, EuropeGarden_Restore
	.byte 0
EuropeGarden_OnTransition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
EuropeGarden_Restore::
	setflag FLAG_TEMP_2
	clearflag FLAG_TEMP_1
	goto_if_ge VAR_EUROPE_GARDEN_STORY, 2, EuropeGarden_BirdFound
	addobject 4
	removeobject 5
	end
EuropeGarden_BirdFound::
	setflag FLAG_TEMP_1
	removeobject 4
	goto_if_eq VAR_EUROPE_GARDEN_STORY, 3, EuropeGarden_Reunited
	removeobject 5
	end
EuropeGarden_Reunited::
	clearflag FLAG_TEMP_2
	addobject 5
	end

EuropeGarden_Offer::
	msgbox EuropeGarden_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeGarden_Stay
	closemessage
	warp MAP_EUROPE_BEAUVAIS_GARDEN, 10, 16
	waitstate
	releaseall
	end
EuropeGarden_Stay::
	msgbox EuropeGarden_Text_Stay
	goto EuropeCelebi_End
EuropeGarden_Return::
	lock
	faceplayer
	msgbox EuropeGarden_Text_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeGarden_Stay
	closemessage
	warp MAP_EUROPE_BEAUVAIS_PAST, 4, 7
	waitstate
	releaseall
	end
EuropeGarden_Luc::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_GARDEN_STORY, 3, EuropeGarden_LucDone
	goto_if_eq VAR_EUROPE_GARDEN_STORY, 2, EuropeGarden_Reunite
	goto_if_eq VAR_EUROPE_GARDEN_STORY, 1, EuropeGarden_Hint
	msgbox EuropeGarden_Text_Luc, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeGarden_Decline
	setvar VAR_EUROPE_GARDEN_STORY, 1
EuropeGarden_Hint::
	msgbox EuropeGarden_Text_Hint
	goto EuropeCelebi_End
EuropeGarden_Decline::
	msgbox EuropeGarden_Text_Decline
	goto EuropeCelebi_End
EuropeGarden_Reunite::
	msgbox EuropeGarden_Text_Reunite
	setvar VAR_EUROPE_GARDEN_STORY, 3
	clearflag FLAG_TEMP_2
	addobject 5
	playmoncry SPECIES_PIDGEY, 0
	waitmoncry
EuropeGarden_LucDone::
	msgbox EuropeGarden_Text_LucDone
	goto EuropeCelebi_End
EuropeGarden_Pidgey::
	lock
	faceplayer
	playmoncry SPECIES_PIDGEY, 0
	waitmoncry
	goto_if_ne VAR_EUROPE_GARDEN_STORY, 1, EuropeGarden_Shy
	msgbox EuropeGarden_Text_Found
	setvar VAR_EUROPE_GARDEN_STORY, 2
	setflag FLAG_TEMP_1
	removeobject 4
	msgbox EuropeGarden_Text_Carry
	goto EuropeCelebi_End
EuropeGarden_Shy::
	msgbox EuropeGarden_Text_Shy
	goto EuropeCelebi_End
EuropeGarden_PidgeyHome::
	lock
	faceplayer
	playmoncry SPECIES_PIDGEY, 0
	waitmoncry
	msgbox EuropeGarden_Text_PidgeyHome
	goto EuropeCelebi_End
EuropeGarden_Sign::
	lockall
	msgbox EuropeGarden_Text_Sign
	goto EuropeCelebi_End

EuropeGarden_Text_Offer::
	.string "ELISE: There is a quiet garden\n"
	.string "beside reception. LUC is there.\p"
	.string "A guide can bring you back, and\n"
	.string "CELEBI will wait near the entrance.\p"
	.string "Would you like to visit the garden?$"
EuropeGarden_Text_Stay::
	.string "Take your time. You can go\n"
	.string "whenever you are ready.$"
EuropeGarden_Text_Return::
	.string "Reception is just along the path.\n"
	.string "Shall I take you back?$"
EuropeGarden_Text_Luc::
	.string "LUC: My PIDGEY flew into the trees\n"
	.string "when a train sounded its whistle.\p"
	.string "It knows a tune I whistle at home.\n"
	.string "Will you help me find it?$"
EuropeGarden_Text_Hint::
	.string "LUC whistles three gentle notes.\n"
	.string "You remember the little tune.\p"
	.string "Look by the trees in the northeast.\n"
	.string "Approach slowly so it isn't startled.$"
EuropeGarden_Text_Decline::
	.string "LUC: I'll wait here. Please come\n"
	.string "back if you have time.$"
EuropeGarden_Text_Shy::
	.string "PIDGEY watches you from the trees.\n"
	.string "It seems to be listening for someone.$"
EuropeGarden_Text_Found::
	.string "You whistle LUC's gentle tune.\n"
	.string "PIDGEY tilts its head and answers.\p"
	.string "It settles on your shoulder.$"
EuropeGarden_Text_Carry::
	.string "Bring PIDGEY back to LUC\n"
	.string "on the west side of the garden.$"
EuropeGarden_Text_Reunite::
	.string "LUC: There you are!\n"
	.string "PIDGEY flutters down beside him.\p"
	.string "Thank you for being gentle.\n"
	.string "I was afraid we'd be separated.$"
EuropeGarden_Text_LucDone::
	.string "LUC: We'll stay near reception.\n"
	.string "It feels better to wait together.\p"
	.string "The CHANTILLY dispatcher knows\n"
	.string "about an onward train to AMIENS.$"
EuropeGarden_Text_PidgeyHome::
	.string "PIDGEY chirps along with LUC's tune.\n"
	.string "It looks calm beside its friend.$"
EuropeGarden_Text_Sign::
	.string "BEAUVAIS RECEPTION GARDEN\p"
	.string "Please give resting POKEMON space.\n"
	.string "The guide can take you to reception.\p"
	.string "CELEBI waits near the south path.$"

EuropeBeauvaisGarden_RealismCathedral::
	msgbox EuropeBeauvaisGarden_RealismCathedralText, MSGBOX_SIGN
	end

EuropeBeauvaisGarden_RealismCathedralText::
	.string "SAINT-PIERRE - BEAUVAIS\n"
	.string "The Gothic choir and transept.$"

EuropeBeauvaisGarden_RealismPalace::
	msgbox EuropeBeauvaisGarden_RealismPalaceText, MSGBOX_SIGN
	end

EuropeBeauvaisGarden_RealismPalaceText::
	.string "EPISCOPAL PALACE GATE\n"
	.string "Two towers beside the cathedral.$"

EuropeBeauvaisGarden_RealismRiver::
	msgbox EuropeBeauvaisGarden_RealismRiverText, MSGBOX_SIGN
	end

EuropeBeauvaisGarden_RealismRiverText::
	.string "THERAIN RIVERSIDE\n"
	.string "Cross the bridges to the south bank.$"
