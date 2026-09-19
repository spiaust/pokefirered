@ Celebi prologue. Present-day progress stays separate from regional quests.
EuropeCelebi_Researcher::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_CELEBI_STORY, 3, EuropeCelebi_Complete
	goto_if_eq VAR_EUROPE_CELEBI_STORY, 2, EuropeCelebi_Report
	goto_if_eq VAR_EUROPE_CELEBI_STORY, 1, EuropeCelebi_Directions
	goto_if_unset FLAG_BADGE03_GET, EuropeCelebi_Locked
	msgbox EuropeCelebi_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeCelebi_Decline
	setvar VAR_EUROPE_CELEBI_STORY, 1
EuropeCelebi_Directions::
	msgbox EuropeCelebi_Text_Directions
	goto EuropeCelebi_End
EuropeCelebi_Locked::
	msgbox EuropeCelebi_Text_Locked
	goto EuropeCelebi_End
EuropeCelebi_Decline::
	msgbox EuropeCelebi_Text_Decline
	goto EuropeCelebi_End
EuropeCelebi_Report::
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, EuropeCelebi_Full
	msgbox EuropeCelebi_Text_Report
	giveitem ITEM_RARE_CANDY, 1
	setvar VAR_EUROPE_CELEBI_STORY, 3
EuropeCelebi_Complete::
	goto_if_eq VAR_EUROPE_LONDON_PAST, 2, EuropeCelebi_Conclusion
	goto_if_ne VAR_EUROPE_DOCK_CHECK, 3, EuropeCelebi_AfterPort
	goto_if_ne VAR_EUROPE_PORT_ACCOUNT, 1, EuropePortAccount_Ada
EuropeCelebi_AfterPort::
	goto_if_eq VAR_EUROPE_LUGGAGE, 3, EuropeSouthAccount_Ada
	goto_if_eq VAR_EUROPE_DOCK_CHECK, 3, EuropePortAccount_Ada
	goto_if_eq VAR_EUROPE_REUNION_STORY, 6, EuropeAmiensAccount_Ada
	goto_if_eq VAR_EUROPE_DEPARTURE_STORY, 4, EuropeDeparture_AdaDone
	msgbox EuropeCelebi_Text_Complete
	goto EuropeCelebi_End
EuropeCelebi_Full::
	msgbox EuropeCelebi_Text_Full
EuropeCelebi_End::
	release
	end

EuropeCelebi_Forest::
	lock
	faceplayer
	goto_if_eq VAR_EUROPE_CELEBI_STORY, 3, EuropeTime_Depart
	goto_if_eq VAR_EUROPE_CELEBI_STORY, 0, EuropeCelebi_Quiet
	goto_if_ne VAR_EUROPE_CELEBI_STORY, 1, EuropeCelebi_Remember
	msgbox EuropeCelebi_Text_Listen, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EuropeCelebi_Leave
	msgbox EuropeCelebi_Text_Appear
	showmonpic SPECIES_CELEBI, 10, 3
	waitbuttonpress
	hidemonpic
	msgbox EuropeCelebi_Text_Vision
	setvar VAR_EUROPE_CELEBI_STORY, 2
	msgbox EuropeCelebi_Text_Return
	goto EuropeCelebi_End
EuropeCelebi_Quiet::
	msgbox EuropeCelebi_Text_Quiet
	goto EuropeCelebi_End
EuropeCelebi_Remember::
	msgbox EuropeCelebi_Text_Remember
	goto EuropeCelebi_End
EuropeCelebi_Leave::
	msgbox EuropeCelebi_Text_Leave
	goto EuropeCelebi_End

EuropeCelebi_Text_Locked::
	.string "I'm ADA, a researcher of old paths.\n"
	.string "A strange visitor waits in France.\p"
	.string "Earn the THUNDERBADGE, then return.\n"
	.string "This journey needs a trained team.$"
EuropeCelebi_Text_Offer::
	.string "ADA: OAK sent me your route\n"
	.string "studies. Similar disturbances\p"
	.string "surround old landmarks. The\n"
	.string "records point to CHANTILLY. A\p"
	.string "green POKEMON waits there, and\n"
	.string "watches stop nearby. Will you\p"
	.string "investigate?$"
EuropeCelebi_Text_Directions::
	.string "Take the train to CHANTILLY. Walk\n"
	.string "south into CHANTILLY FOREST.\p"
	.string "Look beside the middle path, just\n"
	.string "south of the forest survey sign.\p"
	.string "Listen without trying to catch it.\n"
	.string "Then report to me here in OXFORD.$"
EuropeCelebi_Text_Decline::
	.string "ADA: Take your time. I'll wait\n"
	.string "here in OXFORD when you're ready.$"
EuropeCelebi_Text_Listen::
	.string "The green POKEMON tilts its head.\n"
	.string "The air shimmers around its wings.\p"
	.string "Stay still and listen?$"
EuropeCelebi_Text_Appear::
	.string "A soft cry echoes through the trees.\n"
	.string "CELEBI seems to recognize you!$"
EuropeCelebi_Text_Vision::
	.string "For an instant, the forest fades.\n"
	.string "You glimpse a dim station platform.\p"
	.string "A child holds an EEVEE close.\n"
	.string "A torn timetable reads: 1940.\p"
	.string "Then sunlight returns to the trees.\n"
	.string "Your feet have never left the path.$"
EuropeCelebi_Text_Return::
	.string "You record the vision in your notes.\n"
	.string "ADA in OXFORD should hear about this.$"
EuropeCelebi_Text_Quiet::
	.string "The little POKEMON watches quietly.\n"
	.string "Someone in OXFORD may know why.$"
EuropeCelebi_Text_Remember::
	.string "CELEBI waits beside the path.\n"
	.string "You remember the platform from 1940.\p"
	.string "ADA in OXFORD is studying the vision.$"
EuropeCelebi_Text_Leave::
	.string "You step back. The POKEMON waits\n"
	.string "patiently beside the forest path.$"
EuropeCelebi_Text_Report::
	.string "ADA: CELEBI showed you a route\n"
	.string "from 1940. People and their\p"
	.string "POKEMON were seeking safe places\n"
	.string "together. It is asking us to\p"
	.string "understand that journey. Record\n"
	.string "what you learn and help where you\p"
	.string "can. This is for your partner.$"
EuropeCelebi_Text_Complete::
	.string "ADA: Begin at the CHANTILLY\n"
	.string "refuge. Listen to the keeper\p"
	.string "before moving on. CELEBI will wait\n"
	.string "at each arrival point to bring you\p"
	.string "home. We are helping companions\n"
	.string "stay together, not trying to\p"
	.string "change the war.$"
EuropeCelebi_Text_Full::
	.string "ADA: Your report is safe. Make room\n"
	.string "in ITEMS for one RARE CANDY, then\p"
	.string "return so we can review your notes.$"

EuropeCelebi_Conclusion::
 msgbox EuropeCelebi_ConclusionText
 call EuropeCase_Synthesis
 goto_if_ne VAR_EUROPE_PORT_ACCOUNT, 1, EuropePortAccount_Ada
 goto_if_ne VAR_EUROPE_SOUTH_ACCOUNT, 1, EuropeSouthAccount_Ada
 goto EuropeCelebi_End
EuropeCelebi_ConclusionText::
 .string "ADA: Your account is complete.\p"
 .string "CELEBI showed us a chain of care,\n"
 .string "not a secret weapon or a lost prize.\p"
 .string "Safe shelter, honest news and people\n"
 .string "keeping their partners close.\p"
 .string "That is what our present-day routes\n"
 .string "need too. OAK can use these notes.\p"
 .string "Keep exploring the landmarks and\n"
 .string "helping the companions you meet.$"
