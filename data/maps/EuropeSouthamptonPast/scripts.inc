EuropeSouthamptonPast_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EuropeSouthampton_Transition
	map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, EuropeLuggage_Restore
	.byte 0
EuropeSouthampton_Transition::
	setrespawn HEAL_LOCATION_EUROPE_CHANTILLY
	goto EuropeLuggage_Restore
EuropeSouthampton_Clerk::
	lock
	faceplayer
	goto_if_ne VAR_EUROPE_DOCK_CHECK, 3, EuropeSouthampton_Locked
	msgbox EuropeSouthampton_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiens_Stay
	msgbox EuropeSouthampton_Text_Crossing
	compare VAR_EUROPE_SOUTHAMPTON, 0
	call_if_eq EuropeSouthampton_First
	closemessage
	warp MAP_EUROPE_SOUTHAMPTON_PAST, 8, 5
	waitstate
	releaseall
	end
EuropeSouthampton_First::
	setvar VAR_EUROPE_SOUTHAMPTON, 1
	return
EuropeSouthampton_Locked::
	msgbox EuropeSouthampton_Text_Locked
	goto EuropeCelebi_End
EuropeSouthampton_Host::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_SOUTHAMPTON, 2, EuropeSouthampton_Return
	msgbox EuropeSouthampton_Text_Welcome
	setvar VAR_EUROPE_SOUTHAMPTON, 2
EuropeSouthampton_Return::
	msgbox EuropeSouthampton_Text_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeAmiens_Stay
	closemessage
	warp MAP_EUROPE_LE_HAVRE_PAST, 8, 5
	waitstate
	releaseall
	end
EuropeSouthampton_Text_Locked::
	.string "The captain must confirm the dock\n"
	.string "instructions before this group can\p"
	.string "board. Speak to the dockworker,\n"
	.string "read the notice, then ask the\p"
	.string "captain.$"
EuropeSouthampton_Text_Offer::
	.string "A crossing to SOUTHAMPTON is ready.\n"
	.string "The reception host can send you back.\p"
	.string "There is no charge for the trip.\n"
	.string "Travel to SOUTHAMPTON?$"
EuropeSouthampton_Text_Crossing::
	.string "You board with the waiting group.\n"
	.string "The harbor slowly slips from view.\p"
	.string "After the crossing, a reception\n"
	.string "host meets you at SOUTHAMPTON.$"
EuropeSouthampton_Text_Welcome::
	.string "Welcome to SOUTHAMPTON reception.\n"
	.string "You came from LE HAVRE?\p"
	.string "Your arrival is recorded. Stay with\n"
	.string "your companions while we prepare.\p"
	.string "I can arrange a return to LE HAVRE.\n"
	.string "Your green friend knows another way.$"
EuropeSouthampton_Text_Return::
	.string "The LE HAVRE return is available.\n"
	.string "The dockworker offers party care.\p"
	.string "Return to LE HAVRE?$"

EuropeSouthamptonPast_RealismBargate::
	msgbox EuropeSouthamptonPast_RealismBargateText, MSGBOX_SIGN
	end

EuropeSouthamptonPast_RealismBargateText::
	.string "BARGATE\n"
	.string "The northern gate of the old town.$"

EuropeSouthamptonPast_RealismTudor::
	msgbox EuropeSouthamptonPast_RealismTudorText, MSGBOX_SIGN
	end

EuropeSouthamptonPast_RealismTudorText::
	.string "TUDOR HOUSE\n"
	.string "Timber framing beside the old lanes.$"

EuropeSouthamptonPast_RealismWalls::
	msgbox EuropeSouthamptonPast_RealismWallsText, MSGBOX_SIGN
	end

EuropeSouthamptonPast_RealismWallsText::
	.string "WESTERN TOWN WALLS\n"
	.string "Follow the lane towards TOWN QUAY.$"

EuropeSouthamptonPast_RealismQuay::
	msgbox EuropeSouthamptonPast_RealismQuayText, MSGBOX_SIGN
	end

EuropeSouthamptonPast_RealismQuayText::
	.string "TOWN QUAY\n"
	.string "The waterfront south of HIGH STREET.$"
