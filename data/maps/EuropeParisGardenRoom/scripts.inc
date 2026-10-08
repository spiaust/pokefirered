EuropeParisGardenRoom_MapScripts::
 .byte 0

EuropeParisGardenRoom_Enter::
 lockall
 msgbox EuropeParisGardenRoom_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeParisGardenRoom_End
 closemessage
 warp MAP_EUROPE_PARIS_GARDEN_ROOM, 5, 7
 waitstate
 releaseall
 end

EuropeParisGardenRoom_Exit::
 lockall
 warp MAP_EUROPE_PARIS, 55, 39
 waitstate
 releaseall
 end

EuropeParisGardenRoom_Host::
 lock
 faceplayer
 msgbox EuropeParisGardenRoom_HostText, MSGBOX_DEFAULT
 release
 end

EuropeParisGardenRoom_Notebook::
 lock
 msgbox EuropeParisGardenRoom_NotebookText, MSGBOX_DEFAULT
 release
 end

EuropeParisGardenRoom_Plan::
 lockall
 msgbox EuropeParisGardenRoom_PlanText, MSGBOX_DEFAULT
 releaseall
 end

EuropeParisGardenRoom_PlanText::
 .string "A plan for the neighborhood beds.\n"
 .string "Low flowers beside the public paths.\p"
 .string "Leave a quiet patch for POKEMON.\n"
 .string "Keep the walking loop open.$"

EuropeParisGardenRoom_Rota::
 lockall
 msgbox EuropeParisGardenRoom_RotaText, MSGBOX_DEFAULT
 releaseall
 end

EuropeParisGardenRoom_RotaText::
 .string "A rota of small garden tasks.\n"
 .string "One neighbor waters the flower beds.\p"
 .string "Another clears leaves from the path.\n"
 .string "The work is shared, a little daily.$"

EuropeParisGardenRoom_End::
 releaseall
 end

EuropeParisGardenRoom_EntryText::
 .string "A neighbor welcomes visitors.\n"
 .string "Visit the garden workroom?$"

EuropeParisGardenRoom_HostText::
 .string "Welcome to our garden workroom.\n"
 .string "We plan the flower beds together.\p"
 .string "Both benches hold our garden plans.\n"
 .string "Take a look; everyone can help.\p"
 .string "Leave south; follow the lane west.\n"
 .string "The promenade leads to the EIFFEL.$"

EuropeParisGardenRoom_NotebookText::
 .string "A notebook of shared garden plans.\n"
 .string "Give resting POKEMON a quiet space.\p"
 .string "Keep the promenade clear for walkers.\n"
 .string "Share the work and enjoy the flowers.$"
